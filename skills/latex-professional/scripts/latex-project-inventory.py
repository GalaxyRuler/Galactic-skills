#!/usr/bin/env python3
"""Inventory a LaTeX project tree (read-only).

Walks a project root and catalogs LaTeX-relevant files, then inspects every
``.tex`` file for the structural commands that describe how the project is
built: document class, packages, included graphics, ``\\input``/``\\include``
children, bibliography commands, engine hints (fontspec / polyglossia /
unicode-math / luacode), arara directives and ``% !TEX`` magic comments.

It also detects build systems at the root (``latexmkrc``, ``Makefile``, CI
workflow files, README build instructions) and guesses the bibliography
backend and the likely main file(s) using a light re-implementation of the
scoring heuristic in ``find-main-tex.py`` (the scripts are standalone and do
not import one another).

Output is JSON by default-friendly and also available as a human summary
(omit ``--json``). The script is strictly read-only: it never modifies,
creates (outside of stdout), or deletes any user file, and never shells out
or touches the network. Unreadable files are skipped with a recorded note.
"""
import argparse
import json
import re
from pathlib import Path

EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", "__pycache__", "node_modules",
    ".latex-build", "build", "dist", "_minted",
}

# File extensions we care to inventory (lower-cased, no leading dot).
TRACKED_EXTS = {
    "tex", "bib", "bbl", "bst", "sty", "cls",
    "png", "jpg", "jpeg", "pdf", "eps", "svg",
    "ind", "idx", "glo", "gls",
}

GRAPHICS_EXTS = [".pdf", ".png", ".jpg", ".jpeg", ".eps"]
INPUT_EXTS = [".tex"]

MAIN_NAME_BONUS = {
    "main.tex": 30, "paper.tex": 25, "article.tex": 20,
    "manuscript.tex": 25, "ms.tex": 20, "thesis.tex": 25,
    "dissertation.tex": 25, "report.tex": 20, "book.tex": 20,
}

# --- regexes -------------------------------------------------------------
RE_DOCUMENTCLASS = re.compile(r"\\documentclass(?:\[[^\]]*\])?\{([^}]+)\}")
RE_BEGIN_DOCUMENT = re.compile(r"\\begin\{document\}")
RE_USEPACKAGE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}")
RE_REQUIREPACKAGE = re.compile(r"\\RequirePackage(?:\[[^\]]*\])?\{([^}]+)\}")
RE_INCLUDEGRAPHICS = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
RE_INPUT_INCLUDE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
RE_INPUT_INCLUDE_BARE = re.compile(r"\\input\s+([^\s{}]+)")
RE_GRAPHICSPATH = re.compile(r"\\graphicspath\{(.+?)\}", re.DOTALL)
RE_GRAPHICSPATH_ITEM = re.compile(r"\{([^}]*)\}")
RE_BIBLIOGRAPHY = re.compile(r"\\bibliography\{([^}]+)\}")
RE_BIBLIOGRAPHYSTYLE = re.compile(r"\\bibliographystyle\{([^}]+)\}")
RE_ADDBIBRESOURCE = re.compile(r"\\addbibresource(?:\[[^\]]*\])?\{([^}]+)\}")
RE_PRINTBIBLIOGRAPHY = re.compile(r"\\printbibliography")
RE_TEX_ROOT = re.compile(r"%\s*!TEX\s+root\s*=", re.IGNORECASE)
RE_TEX_PROGRAM = re.compile(r"%\s*!TEX\s+program\s*=", re.IGNORECASE)
RE_TEX_MAGIC = re.compile(r"%\s*!TEX\s+(\S+)\s*=\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
RE_ARARA = re.compile(r"%\s*arara:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
RE_BIBLATEX_OPTS = re.compile(r"\\usepackage(?:\[([^\]]*)\])?\{biblatex\}")
RE_FRONTMATTER = re.compile(r"\\maketitle|\\tableofcontents")

# Engine hint packages/macros -> engine implication.
ENGINE_HINTS = {
    "fontspec": "xelatex_or_lualatex",
    "polyglossia": "xelatex_or_lualatex",
    "unicode-math": "xelatex_or_lualatex",
    "luacode": "lualatex",
    "luatextra": "lualatex",
}


def should_skip(rel: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in rel.parts)


def read_text_safe(path: Path):
    try:
        return path.read_text(encoding="utf-8", errors="replace"), None
    except OSError as exc:
        return None, str(exc)


def score_tex_text(name: str, text: str) -> dict:
    """Light re-implementation of find-main-tex scoring (kept standalone)."""
    score = 0
    reasons = []
    if RE_DOCUMENTCLASS.search(text):
        score += 100
        reasons.append("contains \\documentclass")
    if RE_BEGIN_DOCUMENT.search(text):
        score += 80
        reasons.append("contains \\begin{document}")
    if RE_TEX_ROOT.search(text):
        score += 20
        reasons.append("contains !TEX root directive")
    if RE_TEX_PROGRAM.search(text):
        score += 10
        reasons.append("contains !TEX program directive")
    if name.lower() in MAIN_NAME_BONUS:
        score += MAIN_NAME_BONUS[name.lower()]
        reasons.append(f"common main filename: {name}")
    if RE_BIBLIOGRAPHY.search(text) or RE_ADDBIBRESOURCE.search(text):
        score += 10
        reasons.append("declares bibliography")
    if RE_FRONTMATTER.search(text):
        score += 5
        reasons.append("contains frontmatter command")
    if not reasons:
        reasons.append("no strong main-file signals")
    return {"score": score, "reasons": reasons}


def split_commalist(value: str):
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_graphicspath(text: str):
    """Return list of graphics search dirs declared via \\graphicspath."""
    dirs = []
    m = RE_GRAPHICSPATH.search(text)
    if m:
        for item in RE_GRAPHICSPATH_ITEM.findall(m.group(1)):
            item = item.strip()
            if item:
                dirs.append(item)
    return dirs


def analyze_tex(path: Path, root: Path) -> dict:
    text, err = read_text_safe(path)
    rel = str(path.relative_to(root))
    if text is None:
        return {"path": rel, "unreadable": err}
    doc = RE_DOCUMENTCLASS.search(text)
    packages = []
    for m in RE_USEPACKAGE.finditer(text):
        packages.extend(split_commalist(m.group(1)))
    for m in RE_REQUIREPACKAGE.finditer(text):
        packages.extend(split_commalist(m.group(1)))
    graphics = [m.group(1).strip() for m in RE_INCLUDEGRAPHICS.finditer(text)]
    inputs = [m.group(1).strip() for m in RE_INPUT_INCLUDE.finditer(text)]
    bib_dbs = []
    for m in RE_BIBLIOGRAPHY.finditer(text):
        bib_dbs.extend(split_commalist(m.group(1)))
    addbib = [m.group(1).strip() for m in RE_ADDBIBRESOURCE.finditer(text)]
    bibstyles = [m.group(1).strip() for m in RE_BIBLIOGRAPHYSTYLE.finditer(text)]
    arara = [m.group(1).strip() for m in RE_ARARA.finditer(text)]
    magic = [
        {"key": m.group(1), "value": m.group(2).strip()}
        for m in RE_TEX_MAGIC.finditer(text)
    ]
    engine_hits = []
    for pkg in packages:
        if pkg in ENGINE_HINTS:
            engine_hits.append(pkg)
    return {
        "path": rel,
        "documentclass": doc.group(1) if doc else None,
        "packages": sorted(set(packages)),
        "includegraphics": graphics,
        "inputs": inputs,
        "graphicspath": parse_graphicspath(text),
        "bibliography_dbs": bib_dbs,
        "addbibresource": addbib,
        "bibliographystyle": bibstyles,
        "printbibliography": bool(RE_PRINTBIBLIOGRAPHY.search(text)),
        "arara": arara,
        "tex_magic": magic,
        "engine_hint_packages": engine_hits,
        "score": score_tex_text(path.name, text),
    }


def determine_engines(tex_infos):
    """Aggregate engine evidence across all tex files."""
    engines = []
    seen = set()
    for info in tex_infos:
        for pkg in info.get("engine_hint_packages", []):
            implied = ENGINE_HINTS.get(pkg, "xelatex_or_lualatex")
            key = (implied, pkg)
            if key in seen:
                continue
            seen.add(key)
            engines.append({
                "engine": implied,
                "evidence": f"package {pkg} in {info['path']}",
            })
        # TEX program magic comment is authoritative if present.
        for magic in info.get("tex_magic", []):
            if magic["key"].lower() == "program":
                prog = magic["value"].strip().lower()
                key = ("magic", prog, info["path"])
                if key not in seen:
                    seen.add(key)
                    engines.append({
                        "engine": prog,
                        "evidence": f"% !TEX program directive in {info['path']}",
                    })
    return engines


def determine_bib_backend(tex_infos):
    """Guess the bibliography backend with supporting evidence."""
    uses_biblatex = False
    biber = False
    bibtex_backend = False
    uses_natbib = False
    uses_bibcmd = False
    evidence = []
    for info in tex_infos:
        if "biblatex" in info.get("packages", []):
            uses_biblatex = True
            evidence.append(f"\\usepackage{{biblatex}} in {info['path']}")
        if "natbib" in info.get("packages", []):
            uses_natbib = True
            evidence.append(f"\\usepackage{{natbib}} in {info['path']}")
        if info.get("addbibresource") or info.get("printbibliography"):
            uses_biblatex = True
            evidence.append(f"biblatex commands in {info['path']}")
        if info.get("bibliography_dbs") or info.get("bibliographystyle"):
            uses_bibcmd = True
    # Inspect biblatex backend option across raw text is not stored; approximate
    # via presence of biber-specific hints already captured above.
    for info in tex_infos:
        for magic in info.get("tex_magic", []):
            if magic["key"].lower() == "ts-program" and "biber" in magic["value"].lower():
                biber = True
    if uses_biblatex:
        # Default biblatex backend is biber unless a bibtex backend is declared.
        if bibtex_backend:
            backend = "biblatex-bibtex"
        else:
            backend = "biblatex-biber"
    elif uses_natbib:
        backend = "natbib"
        evidence.append("natbib package present")
    elif uses_bibcmd:
        backend = "bibtex"
        evidence.append("\\bibliography/\\bibliographystyle present")
    else:
        backend = "unknown"
    _ = biber  # informational; biblatex defaults to biber regardless
    return {"backend": backend, "evidence": evidence}


def resolve_reference(ref: str, tex_dir: Path, root: Path, exts):
    """Return an existing path for ref trying exts, relative to tex_dir then root.

    ``ref`` may already include an extension. Absolute-ish paths are honored as
    given (relative to root). Returns the resolved Path or None.
    """
    ref = ref.strip()
    if not ref:
        return None
    ref_norm = ref.replace("\\", "/")
    candidates = []
    bases = [tex_dir, root]
    names = [ref_norm]
    # try extension completion only when ref has no known/likely extension
    stem_has_ext = bool(Path(ref_norm).suffix)
    if not stem_has_ext:
        names.extend([ref_norm + ext for ext in exts])
    else:
        # still allow completion in case the suffix is a false dot
        names.extend([ref_norm + ext for ext in exts])
    for base in bases:
        for name in names:
            candidates.append((base / name))
    for cand in candidates:
        try:
            if cand.is_file():
                return cand
        except OSError:
            continue
    return None


def resolve_graphic(ref: str, tex_dir: Path, root: Path, graphics_dirs):
    """Resolve an \\includegraphics reference honoring \\graphicspath dirs."""
    ref_norm = ref.strip().replace("\\", "/")
    search_bases = [tex_dir]
    for gdir in graphics_dirs:
        gd = gdir.strip().replace("\\", "/")
        if gd:
            search_bases.append(tex_dir / gd)
            search_bases.append(root / gd)
    search_bases.append(root)
    stem_has_ext = bool(Path(ref_norm).suffix)
    names = [ref_norm]
    if not stem_has_ext:
        names.extend([ref_norm + ext for ext in GRAPHICS_EXTS])
    else:
        names.extend([ref_norm + ext for ext in GRAPHICS_EXTS])
    for base in search_bases:
        for name in names:
            cand = base / name
            try:
                if cand.is_file():
                    return cand
            except OSError:
                continue
    return None


def detect_build_systems(root: Path):
    systems = []
    for name in ("latexmkrc", ".latexmkrc"):
        p = root / name
        if p.is_file():
            systems.append({"kind": "latexmk", "path": name})
    for name in ("Makefile", "makefile", "GNUmakefile"):
        p = root / name
        if p.is_file():
            systems.append({"kind": "make", "path": name})
    wf_dir = root / ".github" / "workflows"
    if wf_dir.is_dir():
        try:
            for wf in sorted(wf_dir.iterdir()):
                if wf.is_file() and wf.suffix.lower() in (".yml", ".yaml"):
                    systems.append({
                        "kind": "github-actions",
                        "path": str(wf.relative_to(root)).replace("\\", "/"),
                    })
        except OSError:
            pass
    gl = root / ".gitlab-ci.yml"
    if gl.is_file():
        systems.append({"kind": "gitlab-ci", "path": ".gitlab-ci.yml"})
    # README build instructions
    for readme in ("README.md", "README.rst", "README.txt", "README"):
        p = root / readme
        if p.is_file():
            text, err = read_text_safe(p)
            if text and re.search(r"latexmk|pdflatex|xelatex|lualatex|make\b|biber|bibtex",
                                   text, re.IGNORECASE):
                systems.append({"kind": "readme-instructions", "path": readme})
    return systems


def detect_submission_artifacts(root: Path, files_by_ext):
    artifacts = []
    for bbl in files_by_ext.get("bbl", []):
        artifacts.append({"kind": "bbl", "path": bbl})
    for ind in files_by_ext.get("ind", []):
        artifacts.append({"kind": "ind", "path": ind})
    # _minted directories / arXiv-style helpers
    try:
        for p in root.rglob("*"):
            rel = p.relative_to(root)
            if should_skip(rel.parent) and p.is_dir():
                # still surface _minted even if excluded from file walk
                pass
            if p.is_dir() and p.name == "_minted":
                artifacts.append({"kind": "_minted", "path": str(rel).replace("\\", "/")})
    except OSError:
        pass
    for name in ("00README.json", "00README.XXX", "00README.txt"):
        p = root / name
        if p.is_file():
            artifacts.append({"kind": "arxiv-readme", "path": name})
    anc = root / "anc"
    if anc.is_dir():
        artifacts.append({"kind": "arxiv-ancillary", "path": "anc"})
    return artifacts


def build_inventory(root: Path) -> dict:
    files_by_ext = {}
    tex_paths = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if should_skip(rel):
            continue
        if not path.is_file():
            continue
        ext = path.suffix.lower().lstrip(".")
        if ext in TRACKED_EXTS:
            files_by_ext.setdefault(ext, []).append(str(rel).replace("\\", "/"))
            if ext == "tex":
                tex_paths.append(path)
    for ext in files_by_ext:
        files_by_ext[ext].sort()

    tex_infos = []
    unreadable = []
    for tp in sorted(tex_paths):
        info = analyze_tex(tp, root)
        if "unreadable" in info:
            unreadable.append({"path": info["path"], "error": info["unreadable"]})
            continue
        tex_infos.append(info)

    # main candidates ranked by score
    main_candidates = sorted(
        (
            {"path": info["path"],
             "score": info["score"]["score"],
             "reasons": info["score"]["reasons"]}
            for info in tex_infos
        ),
        key=lambda x: x["score"],
        reverse=True,
    )

    # included files + missing references
    included_files = []
    missing = []
    for info in tex_infos:
        tex_dir = (root / info["path"]).parent
        gdirs = info.get("graphicspath", [])
        for g in info.get("includegraphics", []):
            resolved = resolve_graphic(g, tex_dir, root, gdirs)
            if resolved is not None:
                included_files.append({
                    "kind": "graphic",
                    "ref": g,
                    "from": info["path"],
                    "resolved": str(resolved.relative_to(root)).replace("\\", "/"),
                })
            else:
                missing.append({"kind": "graphic", "ref": g, "from": info["path"]})
        for inc in info.get("inputs", []):
            resolved = resolve_reference(inc, tex_dir, root, INPUT_EXTS)
            if resolved is not None:
                included_files.append({
                    "kind": "input",
                    "ref": inc,
                    "from": info["path"],
                    "resolved": str(resolved.relative_to(root)).replace("\\", "/"),
                })
            else:
                missing.append({"kind": "input", "ref": inc, "from": info["path"]})
        for bib in info.get("addbibresource", []):
            resolved = resolve_reference(bib, tex_dir, root, [".bib"])
            if resolved is not None:
                included_files.append({
                    "kind": "bib",
                    "ref": bib,
                    "from": info["path"],
                    "resolved": str(resolved.relative_to(root)).replace("\\", "/"),
                })
            else:
                missing.append({"kind": "bib", "ref": bib, "from": info["path"]})
        for bib in info.get("bibliography_dbs", []):
            resolved = resolve_reference(bib, tex_dir, root, [".bib"])
            if resolved is not None:
                included_files.append({
                    "kind": "bib",
                    "ref": bib,
                    "from": info["path"],
                    "resolved": str(resolved.relative_to(root)).replace("\\", "/"),
                })
            else:
                missing.append({"kind": "bib", "ref": bib + ".bib", "from": info["path"]})

    return {
        "root": str(root),
        "files_by_ext": files_by_ext,
        "main_candidates": main_candidates,
        "engines": determine_engines(tex_infos),
        "bibliography_backend": determine_bib_backend(tex_infos),
        "tex_files": tex_infos,
        "included_files": included_files,
        "missing_referenced_files": missing,
        "build_systems": detect_build_systems(root),
        "possible_submission_artifacts": detect_submission_artifacts(root, files_by_ext),
        "unreadable_files": unreadable,
    }


def print_summary(inv: dict):
    print(f"LaTeX project inventory for: {inv['root']}")
    print()
    counts = {ext: len(paths) for ext, paths in inv["files_by_ext"].items()}
    if counts:
        print("Files by extension:")
        for ext in sorted(counts):
            print(f"  .{ext}: {counts[ext]}")
    else:
        print("No LaTeX-relevant files found.")
    print()
    print("Main candidates:")
    if inv["main_candidates"]:
        for c in inv["main_candidates"][:5]:
            print(f"  {c['score']:>4}  {c['path']}")
    else:
        print("  (none)")
    print()
    backend = inv["bibliography_backend"]
    print(f"Bibliography backend: {backend['backend']}")
    for ev in backend["evidence"][:5]:
        print(f"  - {ev}")
    print()
    if inv["engines"]:
        print("Engine hints:")
        for e in inv["engines"]:
            print(f"  {e['engine']}: {e['evidence']}")
    else:
        print("Engine hints: none (pdflatex assumed)")
    print()
    if inv["build_systems"]:
        print("Build systems:")
        for b in inv["build_systems"]:
            print(f"  {b['kind']}: {b['path']}")
    else:
        print("Build systems: none detected")
    print()
    missing = inv["missing_referenced_files"]
    if missing:
        print(f"Missing referenced files: {len(missing)}")
        for m in missing[:20]:
            print(f"  [{m['kind']}] {m['ref']} (referenced in {m['from']})")
    else:
        print("Missing referenced files: none")
    if inv["possible_submission_artifacts"]:
        print()
        print("Possible submission artifacts:")
        for a in inv["possible_submission_artifacts"]:
            print(f"  {a['kind']}: {a['path']}")
    if inv["unreadable_files"]:
        print()
        print("Unreadable files (skipped):")
        for u in inv["unreadable_files"]:
            print(f"  {u['path']}: {u['error']}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory a LaTeX project (read-only)."
    )
    parser.add_argument("root", nargs="?", default=".", help="Project root")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--include-build",
        action="store_true",
        help="Include build/output directories in the walk.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Project root not found: {root}")
        return 2
    if not root.is_dir():
        print(f"Project root is not a directory: {root}")
        return 2

    global EXCLUDE_DIRS
    if args.include_build:
        EXCLUDE_DIRS = {".git", ".svn", ".hg", "__pycache__", "node_modules"}

    inv = build_inventory(root)
    if args.json:
        print(json.dumps(inv, indent=2))
    else:
        print_summary(inv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
