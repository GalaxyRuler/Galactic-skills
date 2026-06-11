# Repo Acquisition and Discovery

## Repo Profile schema

Build this before changing anything:

```yaml
repo_profile:
  local_path: ""
  remote_provider: github|gitlab|bitbucket|generic
  default_branch: ""
  current_branch: ""
  tracking_branch: ""
  working_tree_state: clean|dirty|conflicted
  ahead_behind:
    ahead: 0
    behind: 0
  branch_model: git-flow|github-flow|trunk-based|branch-per-feature|unknown
  package_manager: npm|pnpm|yarn|pip|uv|poetry|go|maven|gradle|cargo|mixed|unknown
  ci_provider: github-actions|gitlab-ci|circleci|jenkins|azure|unknown
  test_commands: []
  lint_commands: []
  typecheck_commands: []
  security_commands: []
  changelog_present: true|false
  semver_source: package.json|pyproject.toml|pom.xml|Cargo.toml|manual|unknown
  protected_branch_rules_known: true|false
  risk_level: low|medium|high
```

Use `git status --short --branch` for ahead/behind and working-tree state.

## A. Clone a repository

Prefer provider-native tooling when it adds metadata. For GitHub:

```bash
gh repo clone OWNER/REPO
cd REPO
```

Fallback:

```bash
git clone <repo-url>
cd <repo-dir>
```

Then inspect:

```bash
git remote -v
git status --short --branch
git branch -a
git remote show origin
```

## B. Fork-and-clone workflow

Use when the agent lacks write access to upstream:

```bash
gh repo fork OWNER/REPO --clone
cd REPO
git remote -v
```

GitHub CLI adds the parent repository as an `upstream` remote — useful for syncing forked work against the source project.

## C. Existing local repo

```bash
git rev-parse --show-toplevel
git status --short --branch
git remote -v
```

If not a Git repo, stop and ask for a repo URL or local path.

## Default branch detection

Never assume `master`. Preferred detection:

```bash
git remote set-head origin --auto
git symbolic-ref refs/remotes/origin/HEAD
```

Fallback: `git remote show origin`.

Normalize: `refs/remotes/origin/main` → `main`, etc. Use the result as `DEFAULT_BRANCH` everywhere downstream.

## Tier 0 inspection commands (always allowed)

```bash
git status --short --branch
git remote -v
git branch -vv
git branch -r
git log --oneline --decorate --graph -n 30
git diff --stat
git diff --name-only
git fetch --dry-run
```
