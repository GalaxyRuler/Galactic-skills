#!/usr/bin/env python3
"""Lint BibTeX ``.bib`` databases for common problems (read-only).

Takes one or more ``.bib`` paths or a directory (default ``.``; a directory is
globbed recursively for ``*.bib``, skipping build/VCS directories). Each file is
read as UTF-8 with ``errors="replace"`` and scanned with an *approximate*
BibTeX entry parser.

Parser approximation (intentional, documented):
  * Entries are located by scanning for ``@type{key,`` (or ``@type(key,``).
  * The entry body is delimited by a brace/paren depth scan that also tracks
    top-level ``"..."`` quoted field values (a ``"`` only opens a string at
    brace-depth 0; inside ``{...}`` quotes are treated as literal, matching
    BibTeX). Braces inside quoted strings are ignored.
  * The citation key is the text up to the first top-level comma; field *names*
    are collected with a regex over the remaining body. This is not a full
    BibTeX grammar -- string concatenation, ``@string`` macro expansion, and
    cross-references are not resolved -- but it is robust enough to flag
    duplicate keys, unbalanced braces, and missing required fields.

Entry types ``comment``, ``string`` and ``preamble`` are parsed for brace
balance but excluded from key/field reporting.

Reported problems:
  * Duplicate citation keys across all inspected files (ERROR).
  * Unbalanced/unterminated entry braces (ERROR).
  * Missing required fields (WARNING):
      - ``article``            : title, year, and (author or editor)
      - ``book``               : title, year, and (author or editor)
      - ``inproceedings``/``conference`` : title, booktitle, year, and
        (author or editor)
    (``date`` satisfies the ``year`` requirement for biblatex databases.)

The script never modifies a ``.bib`` file, never shells out, and never touches
the network. Exit code: 1 if any duplicate keys or unbalanced braces are found,
0 otherwise (missing-field warnings alone do not fail), 2 on usage error.
"""
import argparse
import json
import re
from pathlib import Path

EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", "__pycache__", "node_modules",
    ".latex-build", "build", "dist", "_minted",
}

# Entry types that are not bibliographic references.
NON_ENTRY_TYPES = {"comment", "string", "preamble"}

RE_FIELD_NAME = re.compile(r"(?:^|,)\s*([A-Za-z][A-Za-z0-9_+-]*)\s*=", re.MULTILINE)

REQUIRED_FIELDS = {
    "article": {"title": True, "year": True, "author_or_editor": True},
    "book": {"title": True, "year": True, "author_or_editor": True},
    "inproceedings": {
        "title": True, "booktitle": True, "year": True, "author_or_editor": True,
    },
    "conference": {
        "title": True, "booktitle": True, "year": True, "author_or_editor": True,
    },
}


def read_text_safe(path: Path):
    try:
        return path.read_text(encoding="utf-8", errors="replace"), None
    except OSError as exc:
        return None, str(exc)


def parse_bib(text: str, filename: str):
    """Return (entries, brace_errors) using the approximate scanner.

    Each entry is a dict: file, key, type, fields (set of field names),
    line (1-indexed start line). brace_errors is a list of dicts describing
    unterminated entries.
    """
    entries = []
    brace_errors = []
    n = len(text)
    i = 0
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break
        # read type token
        j = at + 1
        while j < n and (text[j].isalnum() or text[j] in "_-"):
            j += 1
        etype = text[at + 1:j].strip().lower()
        if not etype:
            i = at + 1
            continue
        # skip whitespace to the opening delimiter
        k = j
        while k < n and text[k] in " \t\r\n":
            k += 1
        if k >= n or text[k] not in "{(":
            i = at + 1
            continue
        open_ch = text[k]
        # scan body respecting brace depth and top-level quotes
        depth = 0
        p = k + 1
        in_quote = False
        end = None
        while p < n:
            c = text[p]
            if in_quote:
                if c == '"':
                    in_quote = False
            elif c == '"' and depth == 0:
                in_quote = True
            elif c == "{":
                depth += 1
            elif c == "}":
                if depth == 0 and open_ch == "{":
                    end = p
                    break
                if depth > 0:
                    depth -= 1
            elif c == ")":
                if depth == 0 and open_ch == "(":
                    end = p
                    break
            p += 1

        line_no = text.count("\n", 0, at) + 1
        if end is None:
            body = text[k + 1:]
            brace_errors.append({
                "file": filename,
                "type": etype,
                "line": line_no,
                "detail": "unterminated entry (unbalanced braces or missing close)",
            })
            # cannot reliably continue past a broken entry
            break

        body = text[k + 1:end]
        # citation key = up to first top-level comma
        key_part, sep, fields_part = body.partition(",")
        key = key_part.strip()
        if etype in NON_ENTRY_TYPES:
            i = end + 1
            continue
        field_names = {
            m.group(1).lower() for m in RE_FIELD_NAME.finditer(sep + fields_part)
        }
        entries.append({
            "file": filename,
            "key": key,
            "type": etype,
            "line": line_no,
            "fields": field_names,
        })
        i = end + 1
    return entries, brace_errors


def missing_field_warnings(entry: dict):
    spec = REQUIRED_FIELDS.get(entry["type"])
    if not spec:
        return []
    fields = entry["fields"]
    warnings = []
    if spec.get("title") and "title" not in fields:
        warnings.append("missing title")
    if spec.get("booktitle") and "booktitle" not in fields:
        warnings.append("missing booktitle")
    if spec.get("year"):
        if "year" not in fields and "date" not in fields:
            warnings.append("missing year")
    if spec.get("author_or_editor"):
        if "author" not in fields and "editor" not in fields:
            warnings.append("missing author/editor")
    return warnings


def gather_bib_files(paths):
    """Expand args into a concrete list of .bib file paths, with errors."""
    files = []
    errors = []
    for raw in paths:
        p = Path(raw)
        if not p.exists():
            errors.append(f"path not found: {p}")
            continue
        if p.is_dir():
            for bib in sorted(p.rglob("*.bib")):
                rel = bib.relative_to(p)
                if any(part in EXCLUDE_DIRS for part in rel.parts):
                    continue
                files.append(bib)
        else:
            files.append(p)
    # de-dup while preserving order
    seen = set()
    unique = []
    for f in files:
        try:
            key = f.resolve()
        except OSError:
            key = f
        if key in seen:
            continue
        seen.add(key)
        unique.append(f)
    return unique, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lint BibTeX .bib databases (read-only)."
    )
    parser.add_argument(
        "paths", nargs="*", default=["."],
        help="One or more .bib files or a directory (default: current dir).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    paths = args.paths if args.paths else ["."]
    bib_files, path_errors = gather_bib_files(paths)

    if not bib_files and not path_errors:
        msg = "No .bib files found."
        if args.json:
            print(json.dumps({"error": msg, "files": []}, indent=2))
        else:
            print(msg)
        return 2 if path_errors else 0

    all_entries = []
    brace_errors = []
    unreadable = []
    per_file = []
    for bib in bib_files:
        text, err = read_text_safe(bib)
        fname = str(bib).replace("\\", "/")
        if text is None:
            unreadable.append({"file": fname, "error": err})
            continue
        entries, berrs = parse_bib(text, fname)
        all_entries.extend(entries)
        brace_errors.extend(berrs)
        per_file.append({"file": fname, "entry_count": len(entries)})

    # duplicate keys across all files
    key_index = {}
    for e in all_entries:
        if not e["key"]:
            continue
        key_index.setdefault(e["key"], []).append(
            {"file": e["file"], "line": e["line"], "type": e["type"]}
        )
    duplicates = [
        {"key": key, "occurrences": occ}
        for key, occ in sorted(key_index.items())
        if len(occ) > 1
    ]

    # missing-field warnings
    field_warnings = []
    for e in all_entries:
        warns = missing_field_warnings(e)
        if warns:
            field_warnings.append({
                "file": e["file"],
                "key": e["key"],
                "type": e["type"],
                "line": e["line"],
                "warnings": warns,
            })

    has_errors = bool(duplicates) or bool(brace_errors)
    result = {
        "files": per_file,
        "path_errors": path_errors,
        "unreadable_files": unreadable,
        "entry_count": len(all_entries),
        "duplicate_keys": duplicates,
        "brace_errors": brace_errors,
        "missing_field_warnings": field_warnings,
        "counts": {
            "duplicate_keys": len(duplicates),
            "brace_errors": len(brace_errors),
            "missing_field_warnings": len(field_warnings),
        },
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Inspected {len(per_file)} .bib file(s), {len(all_entries)} entries.")
        if path_errors:
            print()
            print("Path errors:")
            for pe in path_errors:
                print(f"  {pe}")
        if unreadable:
            print()
            print("Unreadable files:")
            for u in unreadable:
                print(f"  {u['file']}: {u['error']}")
        print()
        if duplicates:
            print(f"ERROR: {len(duplicates)} duplicate key(s):")
            for d in duplicates:
                locs = ", ".join(f"{o['file']}:{o['line']}" for o in d["occurrences"])
                print(f"  {d['key']} -> {locs}")
        else:
            print("Duplicate keys: none")
        print()
        if brace_errors:
            print(f"ERROR: {len(brace_errors)} unbalanced-brace ent(ies):")
            for b in brace_errors:
                print(f"  {b['file']}:{b['line']} ({b['type']}) {b['detail']}")
        else:
            print("Unbalanced braces: none")
        print()
        if field_warnings:
            print(f"WARNING: {len(field_warnings)} entr(ies) with missing fields:")
            for w in field_warnings:
                print(f"  {w['file']}:{w['line']} {w['type']} '{w['key']}': "
                      f"{', '.join(w['warnings'])}")
        else:
            print("Missing-field warnings: none")

    if path_errors and not bib_files:
        return 2
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
