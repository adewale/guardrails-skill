# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code skill and plugin, not an application. There is no build step and no runtime dependencies. The shipped content is markdown plus one bash template that together define quality gates for coding agents.

The skill lives in `skills/guardrails/`. SKILL.md is the core artifact (line budget below). Everything else supports it:
- `skills/guardrails/references/tool-building.md` — diagnostic tool/notation catalog with worked examples (loaded on demand by the circuit breaker)
- `skills/guardrails/references/language-defaults.md` — tool selection lookup table by ecosystem (JS/TS, Python, Rust, Go, Java)
- `skills/guardrails/assets/notation-templates/reproduction-script.sh` — bash scaffold for repro scripts

The repo is also a Claude Code plugin: `.claude-plugin/plugin.json` (its `hooks` field points at `.claude-plugin/hooks/hooks.json`) and `.claude-plugin/marketplace.json`.

Repo-only files (never installed):
- `package.json` — install metadata for skill installers (skill entry, supported harnesses). No dependencies or scripts.
- `evals/` — shared Skill Eval Harness manifest (`shared-benchmark.json`), fixtures, ablation patches and oracles. See `evals/shared-harness.md`.
- `scripts/` — the CI checks below.

## Checks (run these before committing; CI runs the same commands)

| Check | Command | Workflow |
|------|---------|----------|
| Install boundary (no repo-only files in `skills/guardrails/`) | `python3 scripts/check_install_boundary.py` | `install-boundary.yml` |
| SKILL.md line budget | `python3 scripts/check_skill_budget.py` | `install-boundary.yml` |
| Plugin + hooks schema (Claude Code's own validator) and hook registration | `python3 scripts/check_plugin.py` (needs the `claude` CLI; no model or credentials) | `plugin.yml` |
| Eval manifest, model-free | `uvx --from skill-eval-harness==0.6.0 skill-benchmark validate --strict-leakage --check-ablations evals/shared-benchmark.json` and `... audit-manifest evals/shared-benchmark.json --fail-on-blockers` | `eval-manifest.yml` |
| Lint | `uvx ruff@0.16.0 check .` | `ruff.yml` |
| Unit tests (eval oracle, install boundary) | `python3 -m unittest discover -s tests` | `tests.yml` |

None of these checks runs the hooks themselves. The hooks are `prompt`/`agent` hooks that need a model, so whether they fire and block is verified manually (README, "Verifying Installation").

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

- SKILL.md must stay at or under 275 lines (enforced by `scripts/check_skill_budget.py`). It's read in full whenever the skill loads; bloat wastes context tokens. Raise the budget only deliberately, in both places.
- The skill defines *when* checks run and *what to do when stuck*, not *how* to lint or test — agents already know that from training.
- References are loaded on demand, not eagerly. Keep this separation: SKILL.md for hooks/rules, references/ for catalogs.
- The reproduction-script.sh template follows a 4-phase pattern (Setup → Trigger → Check → Cleanup) with `set -euo pipefail`. Preserve this structure.
- The `language-defaults.md` table covers 5 ecosystems × 4 concern areas (testing, static analysis, security, infrastructure). Add new ecosystems as new columns, new concerns as new rows.
