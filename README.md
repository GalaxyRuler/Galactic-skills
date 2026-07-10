# Galactic Skills

Public skills for [Claude Code](https://claude.ai/code) and [Codex](https://openai.com/codex) — privacy-scanned and generalized for anyone to install.

## What are skills?

Skills are instruction files that extend an AI coding agent with domain-specific workflows. Install a skill and the agent knows how to handle that task type automatically.

Every skill here ships in dual-runtime format: `SKILL.md` for Claude Code, `agents/openai.yaml` companion for Codex.

## Installing a skill

**Claude Code:**

```bash
# copy the skill folder into your skills directory
cp -r skills/<skill-name> ~/.claude/skills/
```

**Codex:**

```bash
cp -r skills/<skill-name> $CODEX_HOME/skills/
```

Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\<skill-name> "$env:USERPROFILE\.claude\skills\"   # Claude Code
Copy-Item -Recurse skills\<skill-name> "$env:USERPROFILE\.codex\skills\"    # Codex
```

## Skills

| Skill | Description |
|-------|-------------|
| [angel-investing](skills/angel-investing) | Investor-side early-stage evaluation OS — 5-minute screen, deal-specific Critical Success Factors with superpower/critical-flaw scoring, three-tier diligence, valuation & SAFE/convertible/term-sheet review, cap-table & dilution modeling, portfolio fit, and investment-memo generation |
| [consulting-engagements](skills/consulting-engagements) | Run a solo/small-practice B2B consulting engagement end to end — discovery, proposals/SOW, source-ledger research, issue trees, executive briefs/decks/decision memos, QA gates, and confidentiality controls, with a fabrication firewall and human-approval gates |
| [obsidian-writing](skills/obsidian-writing) | Write, edit, and organize an Obsidian vault — wikilinks/callouts/frontmatter, Dataview/Tasks/Bases dashboards, Canvas files, Templater automation, citation workflows, REST API/MCP control, and an optional anti-drift vault system (one-note-one-home routing, self-routing templates, project boards) |
| [powershell-safe-vars](skills/powershell-safe-vars) | PowerShell footgun catalog for AI-agent tool calls — automatic-variable collisions, quoting/heredoc traps, null-handling bugs, and the safe pattern for each |
| [repo-stewardship](skills/repo-stewardship) | Safely acquire, inspect, sync, validate, and prepare Git repositories for review or delivery — permission tiers, quality gates, changelog/SemVer discipline, PR readiness reports |
| [research-grounding](skills/research-grounding) | Forces a current web search before any recommendation, comparison, price, version, or "state-of-the-art" claim is presented as solid — search-and-cite workflow, red flags, rationalizations table |
| [rust-engineering](skills/rust-engineering) | Production-grade Rust engineering guidelines — ownership, type-driven design, error handling, async/concurrency, testing, security, and performance |
| [startup-consulting](skills/startup-consulting) | Evidence-based startup advisory from idea validation to scaling — stage classification, problem/customer discovery, bottom-up market sizing, unit economics, GTM, pricing, pitch-deck review, fundraising prep, and the scaling gate |
| [tauri-engineering](skills/tauri-engineering) | Tauri v2 engineering — guest-host architecture, IPC commands, ACL security, plugins, binary optimization, auto-updates, and CI/CD |
| [test-backend](skills/test-backend) | Stack-agnostic back-end/API testing — Testing Trophy unit+integration, contract testing (Pact/Schemathesis), data invariants, resilience/chaos, OWASP API Top 10, load/SLO |
| [test-ui](skills/test-ui) | Stack-agnostic UI testing — visual regression, responsive + cross-browser, WCAG 2.2 AA accessibility, component/state matrix, i18n/locale-integrity, design-token fidelity |
| [test-ux](skills/test-ux) | Stack-agnostic UX testing — Nielsen heuristic evaluation, task-based cognitive walkthroughs, journey/state analysis, content/i18n comprehension, real-user test-plan generator |
| [ux-engineering](skills/ux-engineering) | UX engineering and product design — JTBD research, information architecture, WCAG 2.2 AA accessibility, design systems, interaction design, HEART/SUS metrics |

## How skills get here

Each skill passes a privacy scan and generalization pass before publishing. Process details: [docs/PUBLISHING.md](docs/PUBLISHING.md).

## Contributing

Adapt freely — replace any `<placeholder>` values with your own config. PRs welcome if they pass the [quality bar](docs/PUBLISHING.md#quality-bar).

## License

[MIT](LICENSE)
