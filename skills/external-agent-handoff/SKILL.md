---
name: external-agent-handoff
description: Use when handing off work produced in this session to another AI agent — a Codex implementation brief, an external plan review by ChatGPT/GPT Pro or Gemini — when closing a slice/phase/decision that Codex will implement, or when acting as auditor/planner while another agent implements. For crafting or optimizing a standalone prompt with no session-work handoff, use meta-prompt-engineering instead.
---

# External Agent Handoff

## Overview

The user runs a standing multi-agent workflow: Claude audits, plans, and reviews; Codex implements; an external GPT reviews plans adversarially. The deliverable of an audit or planning session is a handoff prompt, not a commit. Handoff prompts must be self-contained, addressed, precondition-checked, and delivered ready to paste — every time, without being asked.

## When to use

Use this when:
- The user asks for "a prompt for Codex/ChatGPT/GPT/Gemini" or an external review of a plan.
- A slice, phase, plan, or decision closes and implementation belongs to Codex.
- You are auditing or reviewing work another agent implemented.

## Role contract

- In audit/review/planning sessions, do not implement. Produce findings, plans, and handoff prompts. Only implement when the user explicitly reassigns the role.
- When a slice or decision closes, draft the next handoff prompt automatically. Never end the turn with "want me to draft it?" — draft it.

## Workflow

1. Address the prompt
- Start the prompt with an explicit destination header: which agent, which project/session it must be pasted into.
- For Codex: name the target repo's full absolute path and expected branch at the top.
- This prevents wrong-session pastes and cross-project contamination.

2. Make it fully self-contained
- Assume the recipient has zero access to this session, this machine's files, or prior context.
- Inline everything needed: the full plan text, relevant diffs, specs, constraints, decisions. Never reference "the plan above" or a local file a cloud model cannot open.
- For cloud models with upload limits, state the limit handling: inline text, or a bundle within the size limit.
- If using a prompt template, fill every placeholder. An empty placeholder costs a full round-trip.

3. Verify preconditions before pinning them
- If the prompt pins a base commit or branch state, verify it is current first (`git fetch`, confirm HEAD) — stale pinned bases repeatedly block Codex runs.
- Include a fallback instruction for the recipient if the base has moved.

4. Specify scope and output contract
- Scope guard: what is in and out of scope; halt conditions if preconditions fail.
- Expected output format: verdict/report structure, verification commands the recipient must run, evidence to return.
- Apply the research-grounding skill to any significant recommendation before embedding it in the prompt.

5. Deliver it usably
- End the turn with the ready-to-paste prompt text in the message AND, for long prompts, a saved `.md` file with its absolute path.
- Number lines in review artifacts when the external reviewer needs to cite locations.
- Never close a handoff turn without giving the user the thing to send.

## Verification checklist

- Destination header names the agent and the target project/session.
- No local-only paths or "see above" references remain for cloud recipients.
- All template placeholders are filled.
- Any pinned base commit was freshly verified, with a fallback instruction included.
- Scope guard, halt rules, and expected output format are present.
- The turn ends with paste-ready text and (if saved) the absolute file path.

## Common failure modes

- Ending an audit turn with findings but no prompt to send, leaving the user with nothing to relay.
- Referencing local files or session context a cloud model cannot read.
- Pinning a base commit without checking it is still HEAD.
- Leaving a template placeholder empty so the recipient gets an incomplete plan.
- Omitting the destination, causing the user to paste the prompt into the wrong project session.
- Implementing changes during a session whose assigned role was auditor.
