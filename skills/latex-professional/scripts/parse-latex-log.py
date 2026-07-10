#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ERROR_PATTERNS = [
    ("latex_error", re.compile(r"^! LaTeX Error: (.+)$")),
    ("package_error", re.compile(r"^! Package ([^ ]+) Error: (.+)$")),
    ("tex_error", re.compile(r"^! (.+)$")),
    ("undefined_citation", re.compile(r"LaTeX Warning: Citation `([^']+)' .* undefined")),
    ("undefined_reference", re.compile(r"LaTeX Warning: Reference `([^']+)' .* undefined")),
    ("missing_file", re.compile(r"(?:File|LaTeX Error: File) `?([^'` ]+)'? not found")),
    ("bibtex_missing_db", re.compile(r"I couldn't open database file (.+)")),
    ("biblatex_error", re.compile(r"Package biblatex (?:Error|Warning): (.+)")),
    ("overfull_hbox", re.compile(r"Overfull \\hbox \(([^)]+)\)")),
    ("underfull_hbox", re.compile(r"Underfull \\hbox")),
]
def parse_log(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace").splitlines()
    findings = []
    for idx, line in enumerate(text):
        for kind, pat in ERROR_PATTERNS:
            m = pat.search(line)
            if m:
                context = text[max(0, idx-3): min(len(text), idx+6)]
                findings.append({
                    "kind": kind,
                    "line": idx + 1,
                    "message": line.strip(),
                    "groups": list(m.groups()),
                    "context": context
                })
                break
    first_fatal = next((f for f in findings if f["kind"] in {
        "latex_error", "package_error", "tex_error", "missing_file",
        "bibtex_missing_db", "biblatex_error"
    }), None)
    return {
        "log": str(path),
        "first_fatal_candidate": first_fatal,
        "findings": findings[:200],
        "counts": {
            "total_findings": len(findings),
            "fatal_candidates": sum(1 for f in findings if f["kind"] in {
                "latex_error", "package_error", "tex_error", "missing_file",
                "bibtex_missing_db", "biblatex_error"
            })
        }
    }
def main() -> int:
    parser = argparse.ArgumentParser(description="Parse LaTeX log for likely root causes.")
    parser.add_argument("logfile", help="Path to .log file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    path = Path(args.logfile)
    if not path.exists():
        print(f"Log file not found: {path}")
        return 2
    result = parse_log(path)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        first = result["first_fatal_candidate"]
        if first:
            print("First fatal candidate:")
            print(f"  {first['kind']} at log line {first['line']}")
            print(f"  {first['message']}")
        else:
            print("No fatal error candidate found.")
        print(f"Total findings: {result['counts']['total_findings']}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
