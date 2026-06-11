# Release Communication

## Changelog rules

1. Check for `CHANGELOG.md`.
2. Check for an `[Unreleased]` section.
3. Add user-facing changes under one of: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security** (Keep a Changelog sections).
4. Skip internal-only refactors unless they affect users, operators, maintainers, security, or compatibility.
5. Mark recalled releases as `[YANKED]` — never delete history.

## SemVer decision mapping

```yaml
semver_decision:
  major:
    trigger:
      - breaking API change
      - removed public behavior
      - incompatible config/schema change
  minor:
    trigger:
      - backward-compatible feature
      - new public capability
      - deprecation notice
  patch:
    trigger:
      - backward-compatible bug fix
      - security fix without breaking change
      - documentation correction for released behavior
```

MAJOR.MINOR.PATCH: incompatible API changes → major; backward-compatible functionality → minor; backward-compatible bug fixes → patch.

## PR readiness report

Produce before opening or updating any PR:

```yaml
pr_readiness:
  branch_synced_with_default: true|false
  working_tree_clean: true|false
  tests_passed: true|false
  lint_passed: true|false
  typecheck_passed: true|false
  security_scan_passed: true|false|not_configured
  coverage_delta: "+0.4%"
  changelog_updated: true|false|not_required
  docs_updated: true|false|not_required
  migrations_reviewed: true|false|not_required
  breaking_change: true|false
  semver_impact: major|minor|patch|none
```

## PR body template

```markdown
## Summary
- What changed:
- Why it changed:
- User or business value:

## Linked Work Item
- Issue/Ticket:

## Validation
- [ ] Format
- [ ] Lint
- [ ] Type check
- [ ] Unit tests
- [ ] Branch coverage
- [ ] Security scan
- [ ] E2E smoke test
- [ ] Manual verification

## Risk and Rollback
- Risk level:
- Risk areas:
- Rollback plan:

## Changelog / Versioning
- Changelog updated: Yes/No
- SemVer impact: major/minor/patch/none
- Breaking change: Yes/No

## Agent Notes
- Files changed:
- Decisions made:
- Follow-up work:
```
