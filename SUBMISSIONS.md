# Submissions and Listings

URLs, identifiers, and processes for every marketplace and directory where this skill
is listed or pending.

---

## Active Listings

### GitHub
- **Repo:** https://github.com/adewale/guardrails-skill
- **Topics:** `claude-code`, `claude-code-skill`, `ai-agents`, `agent-skills`, `claude-skills`
- **Latest release:** https://github.com/adewale/guardrails-skill/releases
- **To update:** Push to `main` and create a new release with `gh release create vX.Y`

### skills.sh (Vercel)
- **Skill page:** https://skills.sh/adewale/guardrails-skill/guardrails
- **Owner profile:** https://skills.sh/adewale (404 until enough installs accumulate)
- **Install command:** `npx skills add adewale/guardrails-skill`
- **How it works:** Auto-indexed via anonymous CLI telemetry when users install. No manual submission.
- **To update:** Push changes to GitHub. Users run `npx skills check` / `npx skills update`.

### Auto-Indexing Directories

These index public GitHub repos automatically. No submission required.

- **skillsmp.com** — auto-indexes repos with 2+ GitHub stars
- **claude-plugins.dev** — auto-indexes from GitHub
- **skillhub.club** — auto-indexes from GitHub

To update: push to GitHub. These sites re-index periodically.

---

## Submitted (Pending Review)

### ComposioHQ/awesome-claude-skills
- **PR:** https://github.com/ComposioHQ/awesome-claude-skills/pull/245
- **Category:** Development & Code Tools
- **Entry format:**
  ```
  - [Guardrails](https://github.com/adewale/guardrails-skill) - Code quality verification gates wired into the agent lifecycle with lifecycle hooks, circuit breakers, config protection, and diagnostic escalation. *By [@adewale](https://github.com/adewale)*
  ```
- **To update after merge:** Fork, create branch, edit the entry in README.md, submit PR
  to `master` with title like `Update Guardrails skill`.

---

## Not Yet Submitted (Waiting on Prerequisites)

### anthropics/claude-plugins-official
- **Submission method:** Google Form at https://clau.de/plugin-directory-submission
  (external PRs are auto-closed)
- **Required fields:**
  - Plugin Name: `guardrails`
  - Plugin Description: 50-100 words about code quality verification gates
  - Platform: Claude Code
  - GitHub repo link: https://github.com/adewale/guardrails-skill
  - Company/Organization URL: https://www.fuzzycomputer.com
  - Primary Contact Email: (your email)
  - Plugin Examples: at least 3 use cases
- **Status:** Not yet submitted. Fill out the form when ready.
- **To update after listing:** If listed with external repo source (most likely), just
  push to your own repo and bump `version` in `.claude-plugin/plugin.json`. Users get
  updates via `/plugin marketplace update`.

### hesreallyhim/awesome-claude-code
- **Submission method:** Issue form only (PRs are rejected)
- **URL:** https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml
- **Prerequisites:**
  - Repo must be publicly available for at least **1 week** (created Feb 22, 2026)
  - Must be submitted by a human, not AI
- **Earliest submission date:** March 1, 2026
- **Form fields:**
  - Display Name: Guardrails
  - Category: Agent Skills
  - Primary Link: https://github.com/adewale/guardrails-skill
  - Author Name: Ade Oshineye
  - Author Link: https://github.com/adewale
  - License: MIT
  - Description:
    > Code quality verification gates wired into the Claude Code agent lifecycle.
    > Enforces checks at every stop and commit, includes a circuit breaker that forces
    > diagnostic tool-building after repeated failures, protects test configs from
    > weakening, and gates high-risk operations.
  - Validate Claims: Install the skill and give Claude a task with a bug. After two
    failed fix attempts, observe that Claude builds a diagnostic tool instead of retrying.
  - Specific Task: "Fix this broken function" (with a function that has a subtle bug
    requiring diagnostic investigation)
- **To update after listing:** Submit a new issue with updated information. The bot and
  maintainer handle the PR.

### travisvn/awesome-claude-skills
- **Submission method:** PR to `main` branch
- **Prerequisites:**
  - Repo must have **10+ GitHub stars** (auto-closed below threshold)
  - PRs must not appear AI-generated
- **Entry format (table row):**
  ```
  | **[guardrails-skill](https://github.com/adewale/guardrails-skill)** | Code quality verification gates wired into the agent lifecycle with lifecycle hooks, circuit breakers, config protection, and diagnostic escalation |
  ```
- **PR title:** `Add guardrails-skill`
- **Status:** Waiting for 10+ stars.
- **To update after merge:** Fork, create branch, edit the table row, submit PR to `main`.

---

## Identifiers Across Platforms

| Platform | Identifier |
|----------|-----------|
| GitHub | `adewale/guardrails-skill` |
| skills.sh | `adewale/guardrails-skill/guardrails` |
| Claude Code plugin | `guardrails@guardrails-skill` |
| Skill name (frontmatter) | `guardrails` |
| Plugin name (plugin.json) | `guardrails` |
| Marketplace name (marketplace.json) | `guardrails-skill` |
