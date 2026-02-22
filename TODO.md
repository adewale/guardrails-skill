# TODO: Publishing and Distribution

Steps to get the guardrails skill discoverable across the ecosystem.

---

## Done

- [x] Create public GitHub repo (https://github.com/adewale/guardrails-skill)
- [x] Add MIT license
- [x] Add install instructions to README
- [x] Set repo description: "Quality gates wired into the Claude Code agent lifecycle"
- [x] Add GitHub topics: `claude-code`, `claude-code-skill`, `ai-agents`, `agent-skills`, `claude-skills`

## Validation

- [ ] **Fix agentskills spec validation error.** `agentskills validate` fails because
  the directory name `guardrails-skill` doesn't match `name: guardrails` in SKILL.md
  frontmatter. The spec requires these to match. Options:
  - Rename the repo to `guardrails` (less descriptive as a GitHub repo name)
  - Change the frontmatter to `name: guardrails-skill` (changes the `/guardrails` slash command to `/guardrails-skill`)
  - Accept the mismatch — validation passes when users install into `~/.claude/skills/guardrails`
- [ ] Re-run `agentskills validate` after deciding on the name

## skills.sh (Vercel)

skills.sh auto-indexes skills when users install them via the CLI. No manual submission.
Listing happens organically as installs accumulate.

- [x] Verify the skill installs cleanly: `npx skills add adewale/guardrails-skill`
- [x] Add `npx skills add` as an alternative install method in the README
- [x] Add skills.sh URL to README: https://skills.sh/adewale/guardrails-skill/guardrails
- [ ] Owner profile page (https://skills.sh/adewale) is 404 until the skill accumulates
  enough installs. Profile pages are generated once an owner has meaningful install activity.
- [ ] Reference: https://skills.sh/docs

## Claude Code Plugin Marketplace

Packaging as a plugin enables `/plugin marketplace add adewale/guardrails-skill` installation.
Requires restructuring the repo and adding manifest files.

- [ ] Evaluate whether plugin packaging is worth the structural change. Current structure
  has `SKILL.md` at root; plugin format requires `skills/guardrails/SKILL.md`. This
  would break existing install instructions and git-clone users.
- [ ] If yes: create `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`
- [ ] If yes: move `SKILL.md` to `skills/guardrails/SKILL.md`
- [ ] If yes: submit to `anthropics/claude-plugins-official` for verified listing
- [ ] Reference: https://code.claude.com/docs/en/plugins

## Awesome Lists

Each list has different submission requirements. **Do not submit until the repo has 10+ stars**
(required by travisvn, good practice for all).

### ComposioHQ/awesome-claude-skills (36.7k stars)
- Submit via: PR to `master` branch
- Category: Development & Code Tools
- Entry format:
  ```
  - [Guardrails](https://github.com/adewale/guardrails-skill) - Code quality verification gates wired into the agent lifecycle with lifecycle hooks, circuit breakers, config protection, and diagnostic escalation. *By [@adewale](https://github.com/adewale)*
  ```
- PR title: `Add Guardrails skill`
- [ ] Submit PR

### hesreallyhim/awesome-claude-code (24.6k stars)
- Submit via: **Issue form only** (not a PR — PRs are rejected)
- URL: https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml
- Category: Agent Skills
- Must be publicly available for at least 1 week before submitting
- Description for the form:
  > Code quality verification gates wired into the Claude Code agent lifecycle. Enforces
  > checks at every stop and commit, includes a circuit breaker that forces diagnostic
  > tool-building after repeated failures, protects test configs from weakening, and gates
  > high-risk operations. Ships with diagnostic escalation catalogs and language-specific
  > tool defaults.
- [ ] Wait 1 week after publish date
- [ ] Submit via issue form (must be submitted by a human, not AI)

### travisvn/awesome-claude-skills (7.5k stars)
- Submit via: PR to `main` branch
- Category: Community Skills > Individual Skills table
- **Requires 10+ GitHub stars** (auto-closed below threshold)
- Entry format (table row):
  ```
  | **[guardrails-skill](https://github.com/adewale/guardrails-skill)** | Code quality verification gates wired into the agent lifecycle with lifecycle hooks, circuit breakers, config protection, and diagnostic escalation |
  ```
- PR title: `Add guardrails-skill`
- PRs must not appear AI-generated
- [ ] Wait for 10+ stars
- [ ] Submit PR (write it yourself)

## Auto-Indexing Directories

These index public GitHub repos automatically. No submission needed, but some have thresholds.

- [ ] **skillsmp.com** — auto-indexes repos with 2+ stars. Should appear once the repo has 2 stars.
- [ ] **claude-plugins.dev** — auto-indexes from GitHub. No action needed.
- [ ] **skillhub.club** — auto-indexes. No action needed.

## Social

- [ ] Post on r/ClaudeCode (96k members)
- [ ] Share on X/Twitter with `#ClaudeCode` `#AgentSkills`
- [ ] Link from the blog posts referenced in the README (fuzzycomputer.com)
