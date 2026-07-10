#!/usr/bin/env python3
"""Verify that every asset a LaTeX document references exists on disk (read-only).

Starting from a main ``.tex`` file (given, or auto-detected via the same
main-file scoring heuristic used by ``find-main-tex.py``), this script follows
``\\input``/``\\include`` children recursively and, across every reached tex
file, collects the referenced assets:

* ``\\includegraphics[...]{path}`` -- considered FOUND if any of ``path`` or
  ``path`` + one of ``.pdf/.png/.jpg/.jpeg/.eps`` exists, resolved relative to
  the including file's directory, then any ``\\graphicspath`` directory, then
  the project root.
* ``\\input{bar}`` / ``\\include{bar}`` -- FOUND if ``bar`` or ``bar.tex``
  exists.
* ``\\bibliography{a,b}`` -- each comma-separated name plus ``.bib``.
* ``\\addbibresource{refs.bib}`` -- the exact name given.

Warnings (not errors) are emitted for absolute paths in ``\\includegraphics``,
Windows-style backslash separators in referenced paths, and detectable
case-only mismatches against files present on disk.

The script never modifies, creates (beyond stdout), or deletes any file, and
never shells out or touches the network. Exit code: 1 if any referenced asset
is missing, 0 if all resolve, 2 on a usage error.
"""
import argparse
import json
import re
from pathlib import Path

EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", "__pycache__", "node_modules",
    ".latex-build", "build", "dist", "_minted",
}

GRAPHICS_EXTS = [".pdf", ".png", ".jpg", ".jpeg", ".eps"]

MAIN_NAME_BONUS = {
    "main.tex": 30, "paper.tex": 25, "article.tex": 20,
    "manuscript.tex": 25, "ms.tex": 20, "thesis.tex": 25,
    "dissertation.tex": 25, "report.tex": 20, "book.tex": 20,
}

RE_DOCUMENTCLASS = re.compile(r"\\documentclass(?:\[[^\]]*\])?\{[^}]+\}")
RE_BEGIN_DOCUMENT = re.compile(r"\\begin\{document\}")
RE_TEX_ROOT = re.compile(r"%\s*!TEX\s+root\s*=\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
RE_TEX_ROOT_FLAG = re.compile(r"%\s*!TEX\s+root\s*=", re.IGNORECASE)
RE_TEX_PROGRAM = re.compile(r"%\s*!TEX\s+program\s*=", re.IGNORECASE)
RE_BIBLIOGRAPHY_DECL = re.compile(r"\\bibliography\{|\\addbibresource\{")
RE_FRONTMATTER = re.compile(r"\\maketitle|\\tableofcontents")

RE_INCLUDEGRAPHICS = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
RE_INPUT_INCLUDE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
RE_GRAPHICSPATH = re.compile(r"\\graphicspath\{(.+?)\}", re.DOTALL)
RE_GRAPHICSPATH_ITEM = re.compile(r"\{([^}]*)\}")
RE_BIBLIOGRAPHY = re.compile(r"\\bibliography\{([^}]+)\}")
RE_ADDBIBRESOURCE = re.compile(r"\\addbibresource(?:\[[^\]]*\])?\{([^}]+)\}")
RE_COMMENT = re.compile(r"(?<!\\)%.*$")


def should_skip(rel: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in rel.parts)


def read_text_safe(path: Path):
    try:
        return path.read_text(encoding="utf-8", errors="replace"), None
    except OSError as exc:
        return None, str(exc)


def strip_comments(text: str) -> str:
    """Remove line comments so commented-out references are ignored."""
    return "\n".join(RE_COMMENT.sub("", line) for line in text.splitlines())


def score_tex_text(name: str, text: str) -> int:
    score = 0
    if RE_DOCUMENTCLASS.search(text):
        score += 100
    if RE_BEGIN_DOCUMENT.search(text):
        score += 80
    if RE_TEX_ROOT_FLAG.search(text):
        score += 20
    if RE_TEX_PROGRAM.search(text):
        score += 10
    if name.lower() in MAIN_NAME_BONUS:
        score += MAIN_NAME_BONUS[name.lower()]
    if RE_BIBLIOGRAPHY_DECL.search(text):
        score += 10
    if RE_FRONTMATTER.search(text):
        score += 5
    return score


def autodetect_main(root: Path):
    best = None
    best_score = -1
    for path in root.rglob("*.tex"):
        rel = path.relative_to(root)
        if should_skip(rel):
            continue
        text, err = read_text_safe(path)
        if text is None:
            continue
        s = score_tex_text(path.name, text)
        if s > best_score:
            best_score = s
            best = path
    return best


def split_commalist(value: str):
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_graphicspath(text: str):
    dirs = []
    m = RE_GRAPHICSPATH.search(text)
    if m:
        for item in RE_GRAPHICSPATH_ITEM.findall(m.group(1)):
            item = item.strip()
            if item:
                dirs.append(item)
    return dirs


def case_insensitive_exists(cand: Path):
    """Return the actual on-disk path if cand exists case-insensitively.

    Returns (exists_exact, actual_path_or_none).
    """
    try:
        if cand.is_file():
            return True, cand
    except OSError:
        return False, None
    parent = cand.parent
    try:
        if not parent.is_dir():
            return False, None
        target = cand.name.lower()
        for child in parent.iterdir():
            if child.is_file() and child.name.lower() == target:
                return False, child
    except OSError:
        return False, None
    return False, None


def resolve_input(ref: str, tex_dir: Path, root: Path):
    """Resolve \\input/\\include: ref or ref.tex, relative to tex_dir then root."""
    ref_norm = ref.strip().replace("\\", "/")
    names = [ref_norm]
    if not ref_norm.lower().endswith(".tex"):
        names.append(ref_norm + ".tex")
    for base in (tex_dir, root):
        for name in names:
            cand = base / name
            try:
                if cand.is_file():
                    return cand
            except OSError:
                continue
    return None


def resolve_graphic(ref: str, tex_dir: Path, root: Path, graphics_dirs):
    """Resolve \\includegraphics honoring \\graphicspath. Returns (path, mismatch)."""
    ref_norm = ref.strip().replace("\\", "/")
    bases = [tex_dir]
    for gdir in graphics_dirs:
        gd = gdir.strip().replace("\\", "/")
        if gd:
            bases.append(tex_dir / gd)
            bases.append(root / gd)
    bases.append(root)
    stem_has_ext = Path(ref_norm).suffix.lower() in GRAPHICS_EXTS
    names = [ref_norm]
    if not stem_has_ext:
        names.extend([ref_norm + ext for ext in GRAPHICS_EXTS])
    case_hint = None
    for base in bases:
        for name in names:
            cand = base / name
            exact, actual = case_insensitive_exists(cand)
            if exact:
                return actual, None
            if actual is not None and case_hint is None:
                case_hint = (str(cand), str(actual))
    return None, case_hint


def resolve_bib(ref: str, tex_dir: Path, root: Path):
    ref_norm = ref.strip().replace("\\", "/")
    names = [ref_norm]
    if not ref_norm.lower().endswith(".bib"):
        names.append(ref_norm + ".bib")
    for base in (tex_dir, root):
        for name in names:
            cand = base / name
            try:
                if cand.is_file():
                    return cand
            except OSError:
                continue
    return None


def collect(main: Path, root: Path):
    """Walk input/include graph, returning findings dict."""
    found = []
    missing = []
    warnings = []
    visited = set()

    def visit(tex_path: Path):
        try:
            resolved = tex_path.resolve()
        except OSError:
            resolved = tex_path
        if resolved in visited:
            return
        visited.add(resolved)
        text, err = read_text_safe(tex_path)
        if text is None:
            warnings.append({
                "kind": "unreadable_tex",
                "path": _rel(tex_path, root),
                "detail": err,
            })
            return
        text = strip_comments(text)
        tex_dir = tex_path.parent
        gdirs = parse_graphicspath(text)

        # graphics
        for m in RE_INCLUDEGRAPHICS.finditer(text):
            ref = m.group(1).strip()
            if "\\" in m.group(1):
                warnings.append({
                    "kind": "windows_backslash_path",
                    "ref": ref,
                    "from": _rel(tex_path, root),
                })
            if _is_absolute_ref(ref):
                warnings.append({
                    "kind": "absolute_graphics_path",
                    "ref": ref,
                    "from": _rel(tex_path, root),
                })
            path, case_hint = resolve_graphic(ref, tex_dir, root, gdirs)
            if path is not None:
                found.append({
                    "kind": "graphic",
                    "ref": ref,
                    "from": _rel(tex_path, root),
                    "resolved": _rel(path, root),
                })
            else:
                missing.append({
                    "kind": "graphic",
                    "ref": ref,
                    "from": _rel(tex_path, root),
                })
                if case_hint is not None:
                    warnings.append({
                        "kind": "case_mismatch",
                        "ref": ref,
                        "from": _rel(tex_path, root),
                        "detail": f"nearest on disk: {case_hint[1]}",
                    })

        # inputs/includes
        for m in RE_INPUT_INCLUDE.finditer(text):
            ref = m.group(1).strip()
            if "\\" in m.group(1):
                warnings.append({
                    "kind": "windows_backslash_path",
                    "ref": ref,
                    "from": _rel(tex_path, root),
                })
            child = resolve_input(ref, tex_dir, root)
            if child is not None:
                found.append({
                    "kind": "input",
                    "ref": ref,
                    "from": _rel(tex_path, root),
                    "resolved": _rel(child, root),
                })
                visit(child)
            else:
                missing.append({
                    "kind": "input",
                    "ref": ref,
                    "from": _rel(tex_path, root),
                })

        # bibliography (bibtex-style, comma list)
        for m in RE_BIBLIOGRAPHY.finditer(text):
            for name in split_commalist(m.group(1)):
                path = resolve_bib(name, tex_dir, root)
                target = name if name.lower().endswith(".bib") else name + ".bib"
                if path is not None:
                    found.append({
                        "kind": "bib",
                        "ref": target,
                        "from": _rel(tex_path, root),
                        "resolved": _rel(path, root),
                    })
                else:
                    missing.append({
                        "kind": "bib",
                        "ref": target,
                        "from": _rel(tex_path, root),
                    })

        # addbibresource (biblatex, exact)
        for m in RE_ADDBIBRESOURCE.finditer(text):
            ref = m.group(1).strip()
            path = resolve_bib(ref, tex_dir, root)
            if path is not None:
                found.append({
                    "kind": "bib",
                    "ref": ref,
                    "from": _rel(tex_path, root),
                    "resolved": _rel(path, root),
                })
            else:
                missing.append({
                    "kind": "bib",
                    "ref": ref,
                    "from": _rel(tex_path, root),
                })

    visit(main)
    return {"found": found, "missing": missing, "warnings": warnings}


def _is_absolute_ref(ref: str) -> bool:
    r = ref.strip()
    if r.startswith("/") or r.startswith("\\"):
        return True
    # Windows drive-letter path, e.g. C:/ or C:\
    if len(r) >= 2 and r[1] == ":" and r[0].isalpha():
        return True
    return False


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root)).replace("\\", "/")
    except (ValueError, OSError):
        return str(path).replace("\\", "/")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check that referenced LaTeX assets exist (read-only)."
    )
    parser.add_argument(
        "main", nargs="?", default=None,
        help="Main .tex file (auto-detected in the current dir if omitted).",
    )
    parser.add_argument(
        "--root", default=None,
        help="Project root (defaults to the main file's directory).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    if args.main is not None:
        main_path = Path(args.main)
        if not main_path.exists():
            print(f"Main .tex file not found: {main_path}")
            return 2
        if main_path.is_dir():
            print(f"Expected a .tex file, got a directory: {main_path}")
            return 2
    else:
        cwd = Path(".").resolve()
        detected = autodetect_main(cwd)
        if detected is None:
            print("No .tex files found to auto-detect a main file.")
            return 2
        main_path = detected

    main_path = main_path.resolve()
    if args.root is not None:
        root = Path(args.root).resolve()
        if not root.is_dir():
            print(f"Project root is not a directory: {root}")
            return 2
    else:
        root = main_path.parent

    result = collect(main_path, root)
    result_out = {
        "main": _rel(main_path, root),
        "root": str(root),
        "counts": {
            "found": len(result["found"]),
            "missing": len(result["missing"]),
            "warnings": len(result["warnings"]),
        },
        **result,
    }

    if args.json:
        print(json.dumps(result_out, indent=2))
    else:
        print(f"Main file: {result_out['main']}")
        print(f"Project root: {root}")
        print()
        print(f"Found: {len(result['found'])}")
        print(f"Missing: {len(result['missing'])}")
        print(f"Warnings: {len(result['warnings'])}")
        if result["missing"]:
            print()
            print("MISSING assets:")
            for m in result["missing"]:
                print(f"  [{m['kind']}] {m['ref']} (referenced in {m['from']})")
        if result["warnings"]:
            print()
            print("Warnings:")
            for w in result["warnings"]:
                detail = f" -- {w['detail']}" if w.get("detail") else ""
                ref = w.get("ref", w.get("path", ""))
                frm = f" (in {w['from']})" if w.get("from") else ""
                print(f"  [{w['kind']}] {ref}{frm}{detail}")

    return 1 if result["missing"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
