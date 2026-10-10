#!/usr/bin/env python3
"""Fail if SKILL.md exceeds its line budget, or if CLAUDE.md states a different budget.

SKILL.md is read in full whenever the skill loads, so its length is a context-token cost
paid on every use. The budget lives here and is restated in CLAUDE.md; this check keeps
the two in sync so the documented limit cannot drift from the enforced one.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "skills" / "guardrails" / "SKILL.md"
CLAUDE_MD = ROOT / "CLAUDE.md"
MAX_LINES = 275
BUDGET_RE = re.compile(r"SKILL\.md must stay at or under (\d+) lines")


def main() -> int:
    errors: list[str] = []
    lines = len(SKILL_MD.read_text(encoding="utf-8").splitlines())
    if lines > MAX_LINES:
        errors.append(
            f"{SKILL_MD.relative_to(ROOT)} is {lines} lines; the budget is {MAX_LINES}. "
            "Move catalog material to references/ or raise MAX_LINES (and CLAUDE.md) deliberately."
        )
    stated = BUDGET_RE.findall(CLAUDE_MD.read_text(encoding="utf-8"))
    if stated != [str(MAX_LINES)]:
        errors.append(
            f"CLAUDE.md must state the budget exactly once as 'SKILL.md must stay at or under {MAX_LINES} lines' "
            f"(found {stated or 'none'})"
        )
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"OK: {SKILL_MD.relative_to(ROOT)} is {lines}/{MAX_LINES} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
