#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", "__pycache__", "node_modules",
    ".latex-build", "build", "dist", "_minted"
}
MAIN_NAME_BONUS = {
    "main.tex": 30, "paper.tex": 25, "article.tex": 20,
    "manuscript.tex": 25, "ms.tex": 20, "thesis.tex": 25,
    "dissertation.tex": 25, "report.tex": 20, "book.tex": 20
}
def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)
def score_tex(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {"path": str(path), "score": -1, "reasons": [f"unreadable: {exc}"]}
    score = 0
    reasons = []
    if re.search(r"\\documentclass(?:\[[^\]]*\])?\{[^}]+\}", text):
        score += 100
        reasons.append("contains \\documentclass")
    if r"\begin{document}" in text:
        score += 80
        reasons.append("contains \\begin{document}")
    if re.search(r"%\s*!TEX\s+root\s*=", text, re.IGNORECASE):
        score += 20
        reasons.append("contains !TEX root directive")
    if re.search(r"%\s*!TEX\s+program\s*=", text, re.IGNORECASE):
        score += 10
        reasons.append("contains !TEX program directive")
    if path.name.lower() in MAIN_NAME_BONUS:
        score += MAIN_NAME_BONUS[path.name.lower()]
        reasons.append(f"common main filename: {path.name}")
    if re.search(r"\\bibliography\{|\\addbibresource\{", text):
        score += 10
        reasons.append("declares bibliography")
    if re.search(r"\\maketitle|\\tableofcontents", text):
        score += 5
        reasons.append("contains frontmatter command")
    if not reasons:
        reasons.append("no strong main-file signals")
    return {"path": str(path), "score": score, "reasons": reasons}
def main() -> int:
    parser = argparse.ArgumentParser(description="Rank likely LaTeX main files.")
    parser.add_argument("root", nargs="?", default=".", help="Project root")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    candidates = []
    for path in root.rglob("*.tex"):
        rel = path.relative_to(root)
        if should_skip(rel):
            continue
        candidates.append(score_tex(path))
    candidates.sort(key=lambda x: x["score"], reverse=True)
    output = {
        "root": str(root),
        "candidates": candidates,
        "best": candidates[0] if candidates else None
    }
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        if not candidates:
            print("No .tex files found.")
            return 1
        for c in candidates[:10]:
            print(f"{c['score']:>4}  {c['path']}")
            for reason in c["reasons"]:
                print(f"      - {reason}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
