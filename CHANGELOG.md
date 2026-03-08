# Changelog

## [0.4.0] - 2026-03-08

### Added
- Bug fix retrospective enforcement in commit gate hook — requires detection gap analysis, concrete prevention, and pattern scan before allowing bug fix commits
- `once: true` on SessionStart hook to prevent redundant discovery runs

### Changed
- Removed duplicate hook definitions from SKILL.md frontmatter; `hooks.json` is now the single source of truth for lifecycle hooks
- Task completion enforcement in Stop hook — agent continues to next slice instead of handing off when planned work remains

### Fixed
- Marketplace source pointed to dead `/tmp` path; updated to GitHub repo

## [0.3.0] - 2026-02-24

### Added
- Lifecycle hooks (`hooks.json`) for automatic registration on install (SessionStart, Stop, Commit)
- Submissions tracker (`SUBMISSIONS.md`) for marketplace listing
- Verification steps in README

### Changed
- Extended `SKILL.md` with hook-related guidance and task completion enforcement in Stop hook
- Updated TODO to reflect completed publishing/distribution work

### Fixed
- Company URL in submissions doc

## [0.2.0] - 2026-02-22

### Added
- Claude Code plugin structure (`.claude-plugin/plugin.json`, `marketplace.json`)
- MIT license
- `CLAUDE.md` for Claude Code onboarding
- Install instructions in README
- `skills.sh` listing script
- TODO for publishing and distribution

### Changed
- Restructured repo: moved `SKILL.md` and references into `skills/guardrails/`

## [0.1.0] - 2026-02-22

### Added
- `SKILL.md` — core guardrails skill (~220 lines) with SessionStart, Stop, and Commit hooks
- `references/tool-building.md` — diagnostic tool/notation catalog with worked examples
- `references/language-defaults.md` — tool selection lookup table (JS/TS, Python, Rust, Go, Java)
- `assets/notation-templates/reproduction-script.sh` — bash scaffold for repro scripts
- `README.md` with project overview
