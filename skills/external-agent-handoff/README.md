# External Agent Handoff

Turns the output of an audit, review, or planning session into a paste-ready prompt for another AI agent — self-contained, addressed to a named destination, precondition-checked, and delivered without being asked.

## What it does

- Enforces a **destination header** on every handoff prompt: which agent, which project/session, which repo path and branch it must be pasted into
- Makes prompts **fully self-contained** — inlines the plan, diffs, specs, and decisions instead of referencing "the plan above" or a local file the recipient cannot open
- Requires **every template placeholder be filled**; an empty placeholder costs a full round-trip
- **Verifies pinned bases before pinning them** (`git fetch`, confirm HEAD) and includes a fallback instruction for when the base has moved
- Specifies a **scope guard and output contract**: what is in/out of scope, halt conditions, verdict structure, verification commands, evidence to return
- Holds a **role contract** — in audit/review/planning sessions, produce findings and prompts, do not implement unless the role is explicitly reassigned
- Ends the turn with the actual paste-ready text (plus an absolute file path for long prompts), never with "want me to draft it?"
- Ships a verification checklist and a common-failure-modes list for self-review before sending

## When to use

Handing off work produced in this session to another AI agent — an implementation brief for a coding agent, an external plan review by ChatGPT/GPT Pro or Gemini — when closing a slice, phase, or decision that another agent will implement, or when acting as auditor/planner while a different agent implements. For crafting a standalone prompt with no session-work handoff, use `meta-prompt-engineering` instead.

## What's inside

- [SKILL.md](SKILL.md) — role contract, five-step handoff workflow (address, self-contain, verify preconditions, scope/output contract, deliver), verification checklist, common failure modes
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/external-agent-handoff ~/.claude/skills/`
**Codex:** `cp -r skills/external-agent-handoff $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\external-agent-handoff "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\external-agent-handoff "$env:USERPROFILE\.codex\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
