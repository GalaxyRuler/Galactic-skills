# Consulting Engagements

Run a solo or small-practice B2B consulting engagement end to end — win, scope, diagnose, deliver, and QA — while treating every AI output as decision-support work product the consultant approves, never automatic truth.

## What it does

- Routes the full engagement lifecycle: `Intake → Scope → Research → Synthesis → Deliverable → QA → Human approval → Delivery → Memory update`
- Enforces a **fabrication firewall**: no market size, competitor fact, regulation, or citation ships unless it was actually retrieved — otherwise it's marked "source needed / unable to verify"
- Keeps facts, assumptions, and recommendations structurally separate
- Qualifies opportunities, runs structured discovery, and converts ambiguity into bounded proposals/SOWs with assumptions, exclusions, and scope-risk
- Maintains a source ledger and claim audit for every fact-sensitive deliverable
- Gates client data by confidentiality class, treats client documents as untrusted data (prompt-injection safe), and segregates engagements
- Runs 10 QA gates, a 1-5 scoring rubric, and an anti-genericity test before anything is "client-ready"
- Holds professional boundaries (legal/financial/HR/tax → issue-spot + escalate) and human-approval gates (no auto-send)
- Produces copy-paste deliverables: intake brief, proposal/SOW, decision memo, exec brief, deck storyline, weekly status, QA checklist, engagement memory

## When to use

Preparing a discovery call, writing a proposal or SOW, scoping work, planning research with a source ledger, structuring a problem into issue trees, drafting an executive brief / board deck / decision memo, QA-ing a client deliverable, reviewing client documents, or classifying client-data confidentiality. Triggers on discovery, intake, proposal/SOW, scope creep, source ledger, claim audit, executive brief, deck storyline, deliverable QA, stakeholder map, kickoff. Full trigger list in the `description` of [SKILL.md](SKILL.md).

**Not for:** venture/startup-specific advice (TAM, PMF, runway, fundraising) — use [startup-consulting](../startup-consulting); or binding legal/tax/regulated-financial advice and guaranteed outcomes — the skill escalates those to qualified humans.

## What's inside

- [SKILL.md](SKILL.md) — router: 10 operating laws, engagement workflow, module routing, red flags, escalation boundaries, completion gates
- [INTAKE-SCOPING.md](INTAKE-SCOPING.md) — opportunity qualification, discovery structure, intake form, completeness gate, proposal/SOW, pricing & scope-risk, kickoff
- [RESEARCH-EVIDENCE.md](RESEARCH-EVIDENCE.md) — fabrication firewall, research plan, source hierarchy, source ledger, claim audit, data classification, prompt-injection rules, document diagnosis
- [SYNTHESIS-DELIVERABLES.md](SYNTHESIS-DELIVERABLES.md) — issue trees, options & recommendation, bias controls, decision memo, brief, deck storyline, artifacts, style pass
- [QA-GOVERNANCE.md](QA-GOVERNANCE.md) — 10 QA gates, scoring rubric, anti-genericity test, professional boundaries + safer wording, approval points, version control, AI-use disclosure
- [TEMPLATES.md](TEMPLATES.md) — engagement control file, intake brief, proposal/SOW, source ledger, claim audit, decision memo, weekly status, QA checklist, engagement memory, naming convention
- `agents/openai.yaml` — Codex companion manifest

## Install

**Claude Code:** `cp -r skills/consulting-engagements ~/.claude/skills/`
**Codex:** `cp -r skills/consulting-engagements $CODEX_HOME/skills/`

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\consulting-engagements "$env:USERPROFILE\.claude\skills\"
```

Dual-runtime: `SKILL.md` drives Claude Code; `agents/openai.yaml` drives Codex.
