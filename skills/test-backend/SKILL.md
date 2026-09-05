---
name: test-backend
description: "Use when asked to test a backend or API, contract-test, security-test an API, load/performance-test, chaos/resilience-test, or verify server correctness — generic, stack-agnostic back-end / API testing process for any service: unit + integration (Testing Trophy, real deps via Testcontainers), API contract (request+response schema, Pact/Schemathesis, breaking-change detection), data invariants, resilience + chaos, OWASP API Security Top 10 (2023) incl. two-account BOLA testing, and load/SLO. Detects the project's language/stack and runs the matching commands. Pairs with playbook.md in this skill folder."
---

# /test-backend — portable back-end testing runner

Execute the **Back-end Testing Playbook** (`playbook.md`, same folder) against the current service and emit a findings report. Read it first. Works for any backend; a project-level `test-backend` overrides this when present.

**Scope:** an argument narrows to an endpoint/service (`/test-backend /api/orders`). No argument = the endpoint map from Phase 0.

## Phase 0 — Detect the stack (do this first)
Read manifests + config and pick commands. Detect:
- **Language/framework:** Node (Express/Fastify/Nest), Python (FastAPI/Django/Flask), Go, Java/Kotlin (Spring), Ruby (Rails), .NET, etc.
- **Test runner:** vitest/jest · pytest · go test · JUnit · rspec · xunit.
- **DB/ORM + cache/queue:** Prisma/TypeORM/Sequelize · SQLAlchemy/Django ORM · GORM · Hibernate; Redis/Postgres/Kafka.
- **Spec:** OpenAPI/Swagger · GraphQL SDL · protobuf — the contract source of truth.
- **Containers/load/DAST:** docker-compose / Testcontainers present? k6/JMeter/Gatling/Locust? OWASP ZAP?
Map to: lint, unit, integration, "start test deps", seed, load. If a tool is **absent**, degrade that phase to a manual checklist + one-line setup note — never fail the run, never silently pass it.
Read a project `TESTING.md` / `docs/testing/*` / the **Project appendix** in `playbook.md` and prefer its commands + auth model.

## Runbook (phase-gated — see playbook.md for the why)
1. **Scope & map** — endpoints × method × auth-context; deps; invariants; SLOs + critical journeys.
2. **Static base** — type-check/lint; schema = contract source of truth.
3. **Unit** — pure logic; independent golden master for critical math.
4. **Integration (widest)** — real DB/cache via Testcontainers/compose; in-process route injection; happy/validation/not-found/**auth boundary**; DB effects, seed determinism, cache + fallback.
5. **Contract** — request+response schema for every endpoint + every declared status code; spec-driven provider tests (Schemathesis/Dredd); consumer-driven (Pact) across services; breaking-change diff vs the committed spec.
6. **Data & invariants** — golden-master parity; deterministic IDs; ETL/sync idempotency + partial-failure isolation; migration safety.
7. **Resilience & chaos** — kill/slow/garble each dep; assert graceful degradation, error-shape, timeouts, retry/backoff, rate-limit; combine Load+Chaos where possible.
8. **Security — OWASP API Top 10 2023** — **BOLA two-account test** (A can't touch B's objects) + BOPLA/BFLA; injection (parameterized + schema, fuzz); **SSRF** on user-influenced fetches; resource caps + rate-limit (+ `trustProxy`); headers/CORS/no-leak; upstream-data sanitization. Optional ZAP DAST (passive first, non-prod, seed with the spec).
9. **Performance & SLO** — encode SLOs as load-tool thresholds (p95/p99, error rate); ramp-up→steady→ramp-down on critical journeys; cache + pool behavior under load. If no load tool → emit scenario + threshold table.
10. **Report** — `docs/testing/reports/<date>-backend.md` (or `./backend-test-report-<date>.md`); map security findings to OWASP API IDs; perf vs SLO; contract diffs explicit.

## Safety + discipline
- Run only against **local/test** instances. Active ZAP scans and load tests are attacks — never target production. Use a test env + deterministic seed.
- **Anti-degraded-pass:** any phase that couldn't run = **NOT VERIFIED** in the report, not "pass."

## Done when
Report written; security S0/S1 + broken invariants triaged; contract + parity green (or failures logged); severity counts + top findings printed. Un-run phases flagged NOT VERIFIED.
