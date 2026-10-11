#!/usr/bin/env python3
"""Validate the Claude Code plugin with Claude Code itself, and prove the hooks register.

1. `claude plugin validate --json` on plugin.json and marketplace.json. Any error fails,
   and so does any warning (unknown hook event, unknown hook type, missing prompt, bad
   timeout, ... are warnings that Claude Code silently ignores at runtime), except the
   known "CLAUDE.md at the plugin root is not loaded" note: this repo's CLAUDE.md is for
   contributors, not plugin context.
2. Install the plugin from this checkout into a throwaway Claude Code config directory and
   check that `claude plugin details` lists exactly the hook events defined in hooks.json.
   If plugin.json does not point Claude Code at hooks.json, it registers no hooks (and
   step 1 never sees the hooks file), so this is the check that proves the hooks load.

No model call and no credentials are involved. Set CLAUDE_BIN to choose the CLI
(default: `claude`).
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
HOOKS_FILE = ROOT / ".claude-plugin" / "hooks" / "hooks.json"
IGNORED_WARNINGS = {("CLAUDE.md", "root")}


def claude(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [*shlex.split(os.environ.get("CLAUDE_BIN", "claude")), *args]
    return subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False)


def isolated_env(home: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("ANTHROPIC_", "CLAUDE_CODE_", "CLAUDE_CONFIG"))}
    env.update(
        HOME=str(home),
        CLAUDE_CONFIG_DIR=str(home / ".claude"),
        DISABLE_TELEMETRY="1",
        CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1",
    )
    return env


def validate(target: Path, env: dict[str, str]) -> list[str]:
    proc = claude("plugin", "validate", "--json", str(target), env=env)
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [f"{target.name}: `claude plugin validate` did not return JSON (exit {proc.returncode}): {proc.stderr.strip()[:500]}"]
    problems: list[str] = []
    for entry in [report.get("manifest") or {}, *(report.get("contents") or [])]:
        if not entry:
            continue
        file = Path(entry.get("file", ""))
        for error in entry.get("errors") or []:
            problems.append(f"{file.name}: error at {error.get('path')}: {error.get('message')}")
        for warning in entry.get("warnings") or []:
            if (file.name, warning.get("path")) in IGNORED_WARNINGS:
                continue
            problems.append(f"{file.name}: warning at {warning.get('path')}: {warning.get('message')}")
    if proc.returncode != 0 and not problems:
        problems.append(f"{target.name}: validate exited {proc.returncode}")
    return problems


def registered_hook_events(env: dict[str, str]) -> tuple[set[str] | None, str]:
    marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    plugin_id = f"{marketplace['plugins'][0]['name']}@{marketplace['name']}"
    for args in (("plugin", "marketplace", "add", str(ROOT)), ("plugin", "install", plugin_id), ("plugin", "details", plugin_id)):
        proc = claude(*args, env=env)
        if proc.returncode != 0:
            return None, f"`claude {' '.join(args)}` exited {proc.returncode}: {(proc.stderr or proc.stdout).strip()[:500]}"
    match = re.search(r"^\s*Hooks \((\d+)\)(.*)$", proc.stdout, re.MULTILINE)
    if not match:
        return None, f"no `Hooks (N)` line in `claude plugin details` output:\n{proc.stdout}"
    events = {e.strip() for e in match.group(2).split("(")[0].split(",") if e.strip()}
    return events, match.group(0).strip()


def main() -> int:
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="guardrails-plugin-check-") as tmp:
        env = isolated_env(Path(tmp))
        for target in (PLUGIN_MANIFEST, MARKETPLACE):
            problems += validate(target, env)
        expected = set(json.loads(HOOKS_FILE.read_text(encoding="utf-8"))["hooks"])
        events, evidence = registered_hook_events(env)
        if events is None:
            problems.append(evidence)
        elif events != expected:
            problems.append(f"installed plugin registers hook events {sorted(events)}; hooks.json defines {sorted(expected)} ({evidence})")
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print(f"OK: plugin and marketplace validate; installed plugin registers {evidence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
