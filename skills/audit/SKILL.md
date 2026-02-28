---
name: audit
description: >
  Pre-push audit of your branch. Use when you're about to push, want a final review
  of everything that changed, or the user says "audit", "review before push",
  "pre-push check", or "what am I about to push".
---

# Audit

A manual, on-demand review of all changes on the current branch before they leave
your machine. This is not an incremental check (guardrails already does that). This
is a holistic sweep of the entire branch delta — the kind of review you'd do yourself
before opening a PR.

Invoke with `/audit`. Nothing fires automatically.

---

## What to audit

Determine the base branch (`main`, `master`, or the upstream tracking branch), then
review the full diff: `git diff <base>...HEAD` plus any uncommitted changes.

Work through each category below. Report findings grouped by category. Skip any
category that produces no findings.

### 1. Unintended changes

- Files modified that don't relate to the task
- Formatting-only diffs in files you didn't otherwise touch
- Changes to generated files (lock files are fine if dependencies changed)

### 2. Secrets and credentials

- API keys, tokens, passwords, connection strings in the diff
- Private keys or certificates
- `.env` files or equivalents staged for commit
- Hard-coded URLs pointing to internal/staging environments

### 3. Debug artifacts

- `console.log`, `debugger`, `print()`, `pp`, `binding.pry`, `dbg!` left in
  production code (test files are fine)
- Commented-out code blocks (small explanatory comments are fine)
- `TODO`, `FIXME`, `HACK`, `XXX` introduced in this branch

### 4. Test coverage

- New or modified production code without corresponding test changes
- Skipped or disabled tests (`.skip`, `@pytest.mark.skip`, `#[ignore]`)
- Test files that import but don't exercise new code paths

### 5. Build and suite

- Run the full test suite and report any failures
- Run the linter/formatter and report any violations
- Run the type checker if the project has one

### 6. Commit hygiene

- Commit messages that don't follow the project's conventions
- Fixup commits that should be squashed
- Commits containing unrelated changes that should be split

### 7. Integration check

- New modules that aren't imported anywhere
- New routes or endpoints that aren't registered
- New migrations that aren't referenced
- New dependencies that aren't used

### 8. Merge conflicts and rebase state

- Unresolved conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- Stale branch: base branch has moved significantly since branch point

---

## Output format

Summarize findings as a numbered list grouped by category. For each finding, include
the file path and line number. At the end, give one of:

- **Clean** — no findings, safe to push
- **Minor** — cosmetic or low-risk issues found (list them), push at your discretion
- **Blocking** — issues that should be fixed before pushing (list them)

If the user asks you to fix any findings, fix them. Otherwise, just report.
