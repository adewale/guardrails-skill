# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code skill — not a runnable codebase. There is no build system, package manager, test suite, or CI pipeline. The repository contains only markdown documentation and one bash template that together define quality gates for coding agents.

SKILL.md is the core artifact (~220 lines). Everything else supports it:
- `references/tool-building.md` — diagnostic tool/notation catalog with worked examples (loaded on demand by the circuit breaker)
- `references/language-defaults.md` — tool selection lookup table by ecosystem (JS/TS, Python, Rust, Go, Java)
- `assets/notation-templates/reproduction-script.sh` — bash scaffold for repro scripts

## Architecture

The skill defines **lifecycle hooks** that block agent progress until checks pass:

| Hook | Fires when | What runs |
|------|-----------|-----------|
| SessionStart | Agent boots | Discovery: git baseline, config inspection, test conventions, LESSONS_LEARNED.md, agent-tools/ |
| Stop | Agent returns control | Fast check (format, lint, types, unit tests). Circuit breaker after 2 failures |
| Commit | Any git commit | Full suite + secrets scan + integration/deployment check (is new code reachable?) |

The **circuit breaker** is the key enforcement mechanism: after 2 failed fix attempts, the agent must build a diagnostic tool or switch to a structured notation (from `references/tool-building.md`) rather than retrying. After attempt 3, the agent stops entirely and reports to the user.

**Config protection** prevents the agent from weakening its own guardrails (test scripts, lint config, CI definitions, coverage thresholds).

## Editing Guidelines

- SKILL.md must stay under ~250 lines. It's read by agents at session start; bloat wastes context tokens.
- The skill defines *when* checks run and *what to do when stuck*, not *how* to lint or test — agents already know that from training.
- References are loaded on demand, not eagerly. Keep this separation: SKILL.md for hooks/rules, references/ for catalogs.
- The reproduction-script.sh template follows a 4-phase pattern (Setup → Trigger → Check → Cleanup) with `set -euo pipefail`. Preserve this structure.
- The `language-defaults.md` table covers 5 ecosystems × 4 concern areas (testing, static analysis, security, infrastructure). Add new ecosystems as new columns, new concerns as new rows.
