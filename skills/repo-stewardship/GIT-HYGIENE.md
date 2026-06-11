# Git Hygiene

## Standard sync workflow

```bash
# 1. Inspect state
git status --short --branch
git remote -v

# 2. Fetch latest remote state
git fetch origin --prune

# 3. Detect default branch from origin/HEAD
DEFAULT_BRANCH="$(git symbolic-ref --short refs/remotes/origin/HEAD | sed 's|^origin/||')"

# 4. Update local default branch safely
git switch "$DEFAULT_BRANCH"
git pull --ff-only origin "$DEFAULT_BRANCH"

# 5. Return to feature branch
git switch "<FEATURE_BRANCH>"

# 6. Integrate per repo policy
git merge "origin/$DEFAULT_BRANCH"     # merge-commit policy
# OR:
# git rebase "origin/$DEFAULT_BRANCH"  # linear-history policy

# 7. Resolve conflicts if needed (see below)

# 8. Validate (project-native test command)

# 9. Push only after validation
git push origin "<FEATURE_BRANCH>"
```

`git pull --ff-only` updates only on fast-forward and fails on divergence — safer for automated agents than an implicit merge.

**Merge vs rebase:** merge when the repo accepts merge commits and branch history matters. Rebase when the repo requires linear history. Never rebase a branch already shared with others without user approval.

## Conflict handling

```bash
git status            # inspect conflicted files
# edit files
git add -A
git merge --continue  # or: git rebase --continue
```

Abort path:

```bash
git merge --abort     # or: git rebase --abort
```

### rerere

For repos with repeated integration branches or branch-per-feature testing:

```bash
git config rerere.enabled true
```

`git rerere` records manual conflict resolutions and reapplies them when the same conflict recurs. Must be enabled before it can assist.

## Branch model detection and behavior

| Model | Detect by | Agent behavior | Migration recommendation |
|-------|-----------|----------------|--------------------------|
| Git Flow | `develop`, `release/*`, `hotfix/*` | Work from `develop`; avoid direct main changes; release through release branches | Gradually reduce long-lived branch divergence |
| GitHub Flow | Short-lived branches from default | Small feature branches; sync often; PR to default | Shorten branch lifetime, speed up CI |
| Trunk-Based | Direct/near-direct trunk integration | Tiny changes, feature flags, high local validation, fast PRs | Feature flags for incomplete functionality |
| Branch-Per-Feature | Many ephemeral branches; repeated integration | rerere, automated rebuilds, test branches, cleanup proposals | Automate ephemeral branch lifecycle with retention rules |

Feature flags pair especially well with trunk-based development — incomplete code merges behind inactive code paths and activates later.

## Health checks

### Local state

```bash
git status --short --branch
git diff --stat
git diff --check
git branch -vv
git log --oneline --decorate -n 20
```

Classify:

```yaml
working_tree:
  clean: safe_to_continue
  dirty_user_changes: stop_and_report
  dirty_agent_changes: continue_if_task_related
  conflicted: enter_conflict_resolution_mode
```

### Branch freshness

```bash
git fetch origin --prune
git rev-list --left-right --count HEAD...@{upstream}
git log --oneline HEAD..origin/<DEFAULT_BRANCH>
```

```yaml
branch_freshness:
  current: 0 commits behind
  mildly_stale: 1-5 commits behind
  stale: 6-25 commits behind
  severely_stale: 26+ commits behind or default branch moved significantly
```

### Branch cleanup (read-only discovery)

```bash
git branch --merged <DEFAULT_BRANCH>
git branch --no-merged <DEFAULT_BRANCH>
git branch -r --merged origin/<DEFAULT_BRANCH>
```

Recommend cleanup; never delete local or remote branches without explicit authorization (Tier 3).

## Repo maturity levels

| Level | Signals | Behavior |
|-------|---------|----------|
| 0 — Unknown | Just acquired | Inspect only. No dependency installs until package manager known. No file changes until goal is clear. Produce repo profile. |
| 1 — Basic | Git exists; no/minimal CI; no protections; no changelog | Recommend baseline CI, local hooks, changelog. Conservative branch workflow. |
| 2 — CI-enabled | CI workflow, test/lint scripts, PR validation expected | Mirror CI commands locally. Modify/add tests. Preserve conventions. |
| 3 — Protected delivery | Protected default branch, required checks, review rules, release process | Never bypass PR. Never push to default. Review-ready PRs. Maintain changelog + SemVer. |
| 4 — Agent-ready | Clear DoR, good coverage, CI gates, hooks, changelog, release policy, feature flags, cleanup policy | Implement small changes autonomously within task boundaries. PRs with validation evidence. Flag ambiguity instead of guessing. Suggest backlog refinements. |

## Recommended repository files for agent readiness

```text
.
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── security.yml
│   │   └── release.yml
│   └── pull_request_template.md
├── .husky/
│   ├── pre-commit
│   └── commit-msg
├── docs/
│   ├── CONTRIBUTING.md
│   ├── RELEASE.md
│   ├── ARCHITECTURE.md
│   └── TESTING.md
├── CHANGELOG.md
├── CODEOWNERS
├── SECURITY.md
├── README.md
└── package.json / pyproject.toml / go.mod / etc.
```

GitHub branch protection and rulesets can enforce review and status-check requirements before code reaches protected branches; rulesets also control who can interact with selected branches/tags and can require workflows before merging.
