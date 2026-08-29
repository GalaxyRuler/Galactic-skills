#!/usr/bin/env python3
"""Lint a meta-prompt against the budget, duplication, capability-sync and test-ID rules.

Usage:
    python prompt_lint.py PROMPT.md [--budget 2000] [--max-instructions 40]
                          [--registry tools.json] [--dupe-threshold 0.15]
                          [--require-test-ids] [--json]
    python prompt_lint.py --selftest

Exit code 0 = all checks pass, 1 = at least one check failed, 2 = bad invocation.
Stdlib only. Intended for CI next to the prompt files it guards.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

# A rule line: a numbered/bulleted item, or any line carrying a normative keyword.
NORMATIVE = re.compile(r"\b(MUST|MUST NOT|NEVER|ALWAYS|SHALL|REQUIRED|DO NOT)\b")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")
TEST_ID = re.compile(r"\b[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+\b")  # META-TOOL-017, SEC-01
# Backticked identifiers that look like tool/function names rather than prose.
CODE_IDENT = re.compile(r"`([a-z][a-z0-9]*(?:[_.][a-z0-9]+)+(?:\(\))?)`")
INJECTED_REGISTRY = re.compile(r"\{\{\s*[a-z_]*tool[a-z_]*\s*\}\}", re.I)
FENCE = re.compile(r"^\s*```")


def estimate_tokens(text: str) -> int:
    """Rough token count. ponytail: chars/4 heuristic, +-20% on English prose;
    swap in the provider's real tokenizer if the budget is tight."""
    return round(len(text) / 4)


def strip_code_blocks(text: str) -> str:
    out, inside = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            inside = not inside
            continue
        if not inside:
            out.append(line)
    return "\n".join(out)


def rule_lines(text: str) -> list[str]:
    """Instruction-bearing lines, outside fenced blocks (templates are data, not rules)."""
    return [
        s
        for s in (ln.strip() for ln in strip_code_blocks(text).splitlines())
        if s and (LIST_ITEM.match(s) or NORMATIVE.search(s))
    ]


def _normalize(line: str) -> str:
    line = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line)
    line = re.sub(r"[`*_#>|]", "", line)
    return re.sub(r"[^a-z0-9 ]+", " ", line.lower()).strip()


def duplicate_pairs(rules: list[str], threshold: float = 0.85) -> list[tuple[str, str, float]]:
    """Near-duplicate rule pairs. ponytail: O(n^2) SequenceMatcher; fine to a few
    hundred rules, which is far past the point where the prompt is the real problem."""
    norm = [(_normalize(r), r) for r in rules]
    norm = [(n, r) for n, r in norm if len(n) > 20]
    found = []
    for i in range(len(norm)):
        for j in range(i + 1, len(norm)):
            ratio = difflib.SequenceMatcher(None, norm[i][0], norm[j][0]).ratio()
            if ratio >= threshold:
                found.append((norm[i][1], norm[j][1], round(ratio, 3)))
    return found


def load_registry(path: Path) -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("tools", [])
    names = set()
    for entry in data:
        names.add(entry if isinstance(entry, str) else entry.get("name", ""))
    return {n for n in names if n}


def undefined_capabilities(text: str, registry: set[str]) -> list[str]:
    mentioned = {m.rstrip("()") for m in CODE_IDENT.findall(text)}
    return sorted(mentioned - registry)


def untested_rules(rules: list[str]) -> list[str]:
    return [r for r in rules if NORMATIVE.search(r) and not TEST_ID.search(r)]


def lint(
    text: str,
    budget: int = 2000,
    max_instructions: int = 40,
    registry: set[str] | None = None,
    dupe_threshold: float = 0.15,
    require_test_ids: bool = False,
) -> dict:
    rules = rule_lines(text)
    tokens = estimate_tokens(text)
    dupes = duplicate_pairs(rules)
    dupe_ratio = round(len(dupes) / len(rules), 3) if rules else 0.0

    findings: list[str] = []
    if tokens > budget:
        findings.append(f"budget: ~{tokens} tokens exceeds budget {budget}")
    if len(rules) > max_instructions:
        findings.append(f"density: {len(rules)} instructions exceeds max {max_instructions}")
    if dupe_ratio > dupe_threshold:
        findings.append(f"duplication: ratio {dupe_ratio} exceeds threshold {dupe_threshold}")

    undefined: list[str] = []
    if registry is not None:
        if INJECTED_REGISTRY.search(text):
            findings.append("info: runtime-injected tool registry detected; capability check skipped")
        else:
            undefined = undefined_capabilities(text, registry)
            if undefined:
                findings.append(f"capability: not in registry -> {', '.join(undefined)}")

    untested: list[str] = []
    if require_test_ids:
        untested = untested_rules(rules)
        if untested:
            findings.append(f"coverage: {len(untested)} normative rule(s) carry no test ID")

    hard = [f for f in findings if not f.startswith("info:")]
    return {
        "tokens": tokens,
        "instructions": len(rules),
        "duplicate_ratio": dupe_ratio,
        "duplicates": dupes,
        "undefined_capabilities": undefined,
        "untested_rules": untested,
        "findings": findings,
        "ok": not hard,
    }


def _selftest() -> int:
    over = "\n".join(f"- Rule number {i} about doing a distinct thing properly." for i in range(60))
    r = lint(over, budget=10_000, max_instructions=40)
    assert r["instructions"] == 60, r["instructions"]
    assert any(f.startswith("density") for f in r["findings"]), r["findings"]
    assert not r["ok"]

    dup = (
        "- Never retry an identical failed call with unchanged arguments.\n"
        "- Never retry an identical failed call with unchanged argument.\n"
        "- Return the final structured result with relevant uncertainty stated.\n"
    )
    r = lint(dup, budget=10_000, max_instructions=40, dupe_threshold=0.15)
    assert r["duplicates"], "near-duplicate rules not detected"
    assert any(f.startswith("duplication") for f in r["findings"])

    reg = {"search_docs", "balance_lookup"}
    r = lint("Call `search_docs` then `delete_all.now`.", registry=reg, budget=10_000)
    assert r["undefined_capabilities"] == ["delete_all.now"], r["undefined_capabilities"]

    r = lint("Tools: {{tool_registry}}\nCall `search_docs`.", registry=reg, budget=10_000)
    assert r["undefined_capabilities"] == []
    assert any(f.startswith("info:") for f in r["findings"])
    assert r["ok"], "info findings must not fail the lint"

    r = lint("- You MUST validate the schema. [META-OUT-003]", require_test_ids=True, budget=10_000)
    assert r["untested_rules"] == []
    r = lint("- You MUST validate the schema.", require_test_ids=True, budget=10_000)
    assert len(r["untested_rules"]) == 1

    # Fenced templates are data, not rules.
    r = lint("```text\n- MUST do a thing\n```\nProse only.", budget=10_000)
    assert r["instructions"] == 0, r["instructions"]

    r = lint("x" * 12_000, budget=2000)
    assert any(f.startswith("budget") for f in r["findings"])

    print("selftest ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("prompt", nargs="?", help="path to the prompt file")
    p.add_argument("--budget", type=int, default=2000, help="max estimated tokens (default 2000)")
    p.add_argument("--max-instructions", type=int, default=40)
    p.add_argument("--registry", type=Path, help="JSON list of live tool names")
    p.add_argument("--dupe-threshold", type=float, default=0.15)
    p.add_argument("--require-test-ids", action="store_true")
    p.add_argument("--json", action="store_true", dest="as_json")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)

    if a.selftest:
        return _selftest()
    if not a.prompt:
        p.error("give a prompt file or --selftest")

    result = lint(
        Path(a.prompt).read_text(encoding="utf-8"),
        budget=a.budget,
        max_instructions=a.max_instructions,
        registry=load_registry(a.registry) if a.registry else None,
        dupe_threshold=a.dupe_threshold,
        require_test_ids=a.require_test_ids,
    )

    if a.as_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{a.prompt}: ~{result['tokens']} tokens, {result['instructions']} instructions, "
              f"duplicate ratio {result['duplicate_ratio']}")
        for f in result["findings"]:
            print(f"  {f}")
        for left, right, ratio in result["duplicates"]:
            print(f"  dupe {ratio}: {left[:70]!r} ~ {right[:70]!r}")
        for rule in result["untested_rules"]:
            print(f"  untested: {rule[:90]}")
        print("PASS" if result["ok"] else "FAIL")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
