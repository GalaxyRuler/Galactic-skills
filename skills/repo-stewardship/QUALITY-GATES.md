# Quality Gates

## Local gates (before commit/push)

Run cheapest first:

| Gate | Purpose | Example commands |
|------|---------|------------------|
| Format | Eliminate style churn | `npm run format`, `ruff format`, `prettier --check .` |
| Lint | Detect syntax/style defects | `npm run lint`, `ruff check`, `eslint .` |
| Type check | Catch structural defects | `tsc --noEmit`, `mypy`, `pyright` |
| Unit tests | Verify local behavior | `npm test`, `pytest`, `go test ./...` |
| Branch coverage | Validate decision paths | `pytest --cov --cov-branch`, `vitest --coverage` |
| Security scan | Vulnerable deps/code patterns | `npm audit`, `pip-audit`, `govulncheck`, SAST |
| Secret scan | Prevent credential leakage | `gitleaks`, `trufflehog` |
| Build | Confirm deployable artifact | `npm run build`, `go build ./...` |

## PR gates (CI before merge)

1. Install dependencies from lockfile
2. Lint
3. Type check
4. Unit tests
5. Branch coverage threshold
6. Security/dependency scan
7. Secret scan
8. Build/package
9. E2E smoke tests
10. Changelog/release-note validation when applicable

GitHub branch protection can require status checks before merging. Keep CI job names unique — ambiguous job names can block PRs when used as required checks.

**Organization-level:** repository rulesets control who can interact with branches/tags and can require workflows before merging.

## Local guardrails: Husky + lint-staged (JS/TS repos)

```bash
npm install --save-dev husky lint-staged
npx husky init
```

`package.json`:

```json
{
  "scripts": {
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "format": "prettier --check ."
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml,yaml}": ["prettier --write"]
  }
}
```

`.husky/pre-commit`:

```bash
npx lint-staged
npm run typecheck
npm test -- --runInBand
```

**Agent rule:** local hooks are helpful, but CI remains authoritative. Passing local hooks is not proof a PR is mergeable.

## Agentic E2E testing

AI agent generates or executes realistic end-to-end user journeys against a deployed or locally running application — actual UI/API behavior, not excessive mocks.

### Required controls

- Use sanitized test data.
- Never use production credentials.
- Never scrape or replay sensitive user traffic without approval.
- Store generated tests in the repo when stable.
- Separate exploratory findings from deterministic regression tests.
- Fail closed when authentication, billing, destructive actions, or PII are involved.

### Test artifact format

```yaml
e2e_scenario:
  name: "User can reset password"
  environment: "local"
  preconditions:
    - "Test user exists"
    - "Email capture service is running"
  steps:
    - "Open login page"
    - "Click forgot password"
    - "Submit test email"
    - "Open reset link from test mailbox"
    - "Set new password"
    - "Login with new password"
  assertions:
    - "Success message appears"
    - "Session is created"
    - "Old password no longer works"
  rollback:
    - "Delete test user"
```

## CI failure triage

Do not blindly patch. Classify first:

```yaml
ci_failure_triage:
  failure_type:
    - install_failure
    - lint_failure
    - type_failure
    - unit_test_failure
    - coverage_failure
    - security_failure
    - e2e_failure
    - flaky_test
    - infrastructure_failure
  first_failing_job: ""
  first_failing_step: ""
  likely_root_cause: ""
  local_reproduction_command: ""
  proposed_fix: ""
  confidence: low|medium|high
```

Workflow:

1. Read the first failing job.
2. Determine deterministic vs environmental.
3. Reproduce locally if possible.
4. Patch only the smallest responsible area.
5. Re-run the relevant local gate.
6. Re-run broader gates only after the targeted gate passes.
7. Update PR with cause and fix.
