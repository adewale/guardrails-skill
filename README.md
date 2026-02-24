# Guardrails Skill

Quality gates wired into the agent lifecycle. Not guidance the agent might follow —
checks that block progress until they pass.

## The Idea

Most coding-agent instructions live in prompt space: prose rules the agent might follow,
might not. This skill moves constraints into environment space wherever possible. A lint
rule that fails the build in 20ms gives the agent unambiguous feedback at zero token
cost. A prose instruction competes for attention with everything else in the context
window. The skill focuses on the behaviors a coding agent wouldn't exhibit without being
told, and trusts the agent's training for everything else (what linting is, how to write
a unit test, which formatter to use).

The novel behaviors:

- **Lifecycle hooks** — `script/test_fast` runs on every stop, `script/test` runs on
  every commit. The agent can't declare success or commit code until checks pass.
- **Circuit breaker** — After 2 failed attempts at the same fix, the agent must build
  a diagnostic tool or switch to a structured notation before retrying. Stops thrashing.
- **Config protection** — The agent can't weaken its own tests to make them pass.
- **Integration check** — At commit time, verify new code is reachable (wired in), not
  just correct (tests pass).
- **Diagnostic escalation** — A catalog of tools and notations for when the agent is
  stuck, plus proactive recognition of problem shapes that benefit from scaffolding.
- **Lessons learned** — Knowledge persisted across sessions so the agent doesn't repeat
  mistakes.

## Install

```bash
npx skills add adewale/guardrails-skill
```

Or as a Claude Code [plugin](https://code.claude.com/docs/en/plugins):

```
/plugin marketplace add adewale/guardrails-skill
/plugin install guardrails@guardrails-skill
```

Or clone into your [Claude Code skills directory](https://code.claude.com/docs/en/skills):

```bash
# Personal (all projects)
git clone https://github.com/adewale/guardrails-skill ~/.claude/skills/guardrails

# Or project-level (one project only)
git clone https://github.com/adewale/guardrails-skill .claude/skills/guardrails
```

Browse on [skills.sh](https://skills.sh/adewale/guardrails-skill/guardrails).

## Structure

```
guardrails-skill/
├── .claude-plugin/
│   ├── plugin.json                        Plugin manifest
│   ├── marketplace.json                   Marketplace catalog
│   └── hooks/
│       └── hooks.json                     Lifecycle hooks (plugin path)
├── skills/
│   └── guardrails/
│       ├── SKILL.md                       ← Agent reads this (~200 lines)
│       ├── references/
│       │   ├── tool-building.md             Diagnostic tools, notations, worked examples
│       │   └── language-defaults.md         Tool selection table by ecosystem
│       └── assets/
│           └── notation-templates/
│               └── reproduction-script.sh   Bash scaffold for repro scripts
├── CLAUDE.md
├── LICENSE
└── README.md
```

SKILL.md is the core — everything the agent needs to know about when checks run and what
to do when stuck. The references are loaded on demand: `tool-building.md` when the circuit
breaker fires, `language-defaults.md` when writing test scripts for an unfamiliar ecosystem.

## Hooks

Hooks are registered automatically on installation — no manual setup needed. Both
installation paths (skill and plugin) wire the same four hooks:

| Hook | Event | Type | What it does |
|------|-------|------|-------------|
| Discovery | `SessionStart` | agent | Inspects project for existing config, test runners, conventions |
| Stop check | `Stop` | prompt | Verifies fast check ran, tests match code changes, circuit breaker respected |
| Commit gate | `PreToolUse` (Bash) | prompt | Blocks `git commit` until full suite passes, secrets scanned, code reachable |
| Config protection | `PreToolUse` (Edit/Write) | prompt | Blocks edits to lint/test/CI config — agent must propose changes to user |

- **Skill install** (`npx skills add` or git clone to `.claude/skills/`): hooks are
  declared in the SKILL.md frontmatter.
- **Plugin install** (`/plugin install`): hooks are declared in
  `.claude-plugin/hooks/hooks.json`.

View registered hooks in a session with `/hooks`.

## Testing This Skill

The skill doesn't ship eval files. Use the skill-creator if you want to run formal
evals. Key scenarios to test:

- **SessionStart:** Does the agent discover existing config and conventions before
  writing code? Does it create test scripts if they're missing?
- **Circuit breaker:** When the agent fails twice, does it build a diagnostic (state
  transition table, reproduction script, data flow diagram) instead of trying a third
  direct fix?
- **Proactive recognition:** Does the agent build a call site inventory before modifying
  a widely-used function? A decision matrix before implementing complex conditionals?
- **High-risk gating:** Does the agent stop and ask before destructive operations (DROP
  TABLE, data migrations, deployment actions)?
- **Integration check:** Does the agent verify new code is wired in (routes registered,
  modules imported) at commit time?

## References

- Matt Holden, "[Guardrail Coding](https://www.fuzzycomputer.com/posts/guardrail-coding)"
  (February 2026) — The guidance vs. guardrails distinction (prompt space vs. environment
  space) that shaped this skill's focus on enforcement hooks over prose instructions.
  Also: "[Onboarding AI Agents](https://www.fuzzycomputer.com/posts/onboarding)" for
  the quality gates concept, and "[Markdown Coding](https://www.fuzzycomputer.com/posts/markdown-coding)."
- Cai et al., "[Large Language Models as Tool Makers](https://arxiv.org/abs/2305.17126)"
  (2023) — LLM creates reusable Python tools; cheaper LLM uses them. Influenced the
  agent tool library and diagnostic-tool-graduation concepts.
- Wang et al., "[Voyager](https://arxiv.org/abs/2305.16291)" (2023) — Minecraft agent
  with ever-growing skill library. Influenced the persistent tool accumulation pattern.
- Yang et al., "[SWE-agent](https://arxiv.org/abs/2405.15793)" (2024) — Custom
  Agent-Computer Interface for coding agents. Influenced the reproduction-script-first
  diagnostic approach.
