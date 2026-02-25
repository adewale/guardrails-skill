# Skill vs Plugin: Tradeoff Analysis for guardrails-skill

The repo currently ships both formats — SKILL.md frontmatter hooks and
`.claude-plugin/hooks/hooks.json`. This document examines the tradeoffs of
leaning fully into the plugin model.

Reference: https://code.claude.com/docs/en/plugins

## What you gain by going plugin-only

| Benefit | Detail |
|---|---|
| **Richer hook events** | Plugins support events that SKILL.md frontmatter can't express: `PostToolUse`, `PostToolUseFailure`, `SubagentStart`, `SubagentStop`, `PreCompact`, `TaskCompleted`, `TeammateIdle`. Enables post-hoc verification (e.g., lint-on-save after `Write`). |
| **MCP server bundling** | A plugin can ship an `.mcp.json` that auto-starts MCP servers — e.g., a secrets-scanning server or a coverage-reporting tool. Skills can't do this. |
| **LSP server bundling** | Plugins can include `.lsp.json` for real-time code intelligence. Not relevant to guardrails today but available if needed. |
| **Custom agents** | Plugins can ship `agents/` — standalone subagents with their own system prompts and tool restrictions. The circuit-breaker diagnostic escalation could become a dedicated `diagnostic-agent`. |
| **`settings.json` defaults** | Plugins can set a default `agent` that takes over the main thread. A guardrails plugin could ship a hardened default agent. |
| **Scoped installation** | Plugins support `user`, `project`, `local`, and `managed` scopes. A team can pin guardrails at the project scope via `.claude/settings.json` checked into version control. Skills don't have this mechanism. |
| **Version-aware updates** | Plugin versions in `plugin.json` drive cache invalidation. Users get updates when you bump the version. Skills installed via `npx skills add` get whatever's on `main`. |
| **Marketplace distribution** | Plugins integrate with `/plugin install` and marketplace directories. More discoverable UX than `npx skills add`. |
| **`${CLAUDE_PLUGIN_ROOT}`** | Hook scripts can reference `${CLAUDE_PLUGIN_ROOT}` for portable paths. The `reproduction-script.sh` template could be invoked from hooks without hardcoding paths. |

## What you lose or compromise

| Cost | Detail |
|---|---|
| **Namespaced skill names** | Plugin skills become `/guardrails:guardrails` instead of `/guardrails`. Noisier for users; the namespace prevents conflicts but is pure overhead for a solo plugin with one skill. |
| **Dual maintenance of hooks** | Hooks are declared in both SKILL.md frontmatter (lines 10–34) and `.claude-plugin/hooks/hooks.json`. These are not identical — hooks.json has longer prompts and explicit timeouts. Keeping both means two sources of truth that can drift. |
| **Skill-based distribution breaks** | `npx skills add` and skills.sh rely on SKILL.md frontmatter. Stripping hooks from SKILL.md and relying entirely on hooks.json means users who install as a skill lose the hooks — which are the entire point. This cuts off the skills.sh distribution channel. |
| **Plugin caching copies files** | Marketplace-installed plugins are copied to `~/.claude/plugins/cache`. References (`tool-building.md`, `language-defaults.md`) work fine since they're inside the plugin directory, but symlinks to external files need care. |
| **Path traversal restriction** | Installed plugins can't reference files outside their directory tree. No impact today, but relevant if guardrails ever needs project-local config from outside the plugin root. |
| **No `once: true` in hooks.json** | SKILL.md SessionStart hook has `once: true` (line 17), ensuring discovery runs once per session. The hooks.json version doesn't set this. Verify the plugin hook system supports `once` — the docs don't mention it for hooks.json. |
| **Prompt hooks lack tool access** | Stop and PreToolUse hooks use `type: "prompt"`, which evaluates a prompt with an LLM but has no tool access. If any prompt hook ever needs to run a command (e.g., run `gitleaks` in the commit gate rather than checking whether it was run), it must be upgraded to an agent hook — increasing latency and cost. |
| **Requires Claude Code 1.0.33+** | Plugins need a minimum version. Skills work on older versions. Matters if your audience includes users on older Claude Code installs. |

## The core tension: dual-format distribution

The repo distributes through two incompatible channels:

1. **Skills channel** (skills.sh, `npx skills add`): reads SKILL.md frontmatter for hooks
2. **Plugin channel** (`/plugin install`, marketplaces): reads hooks.json for hooks

These have different hook declarations, different prompt lengths, and potentially
different behavior (the `once: true` discrepancy). Going plugin-only simplifies
this but cuts off the skills channel. Keeping both means maintaining two hook
definitions that must stay in sync.

## Options

### Option A: Plugin-only

Drop hooks from SKILL.md frontmatter. Rely entirely on hooks.json. Accept the
loss of the skills.sh distribution channel and the noisier `/guardrails:guardrails`
skill name. Gain richer hook events, MCP/LSP bundling, scoped installation, and
version-aware updates.

### Option B: Keep both, single source of truth

Keep both formats but treat one as canonical and derive the other. For example,
write a script that generates hooks.json from SKILL.md frontmatter (or vice
versa). This preserves both distribution channels at the cost of a build step.

### Option C: Status quo with sync discipline

Keep both formats, maintain them manually, and add a checklist item to verify
they match on each release. Simpler than a build step but prone to drift.

### Option D: Skills-only

Drop the plugin structure entirely. Simpler distribution via skills.sh and
`npx skills add`. Lose all plugin-specific capabilities (MCP, LSP, agents,
scoped installation, version-aware updates, richer hook events).
