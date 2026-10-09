"""Static check that plugin.json points Claude Code at hooks.json.

The authoritative check is scripts/check_plugin.py (Claude Code's own validator plus a
throwaway install), which needs the `claude` CLI and runs by hand. This test keeps the
regression it guards against in CI for free: without the `hooks` field, the plugin
installs with 0 hooks, because .claude-plugin/hooks/hooks.json is not a default location.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
HOOKS_FILE = ROOT / ".claude-plugin" / "hooks" / "hooks.json"


class PluginManifestTest(unittest.TestCase):
    def test_hooks_field_resolves_to_hooks_json(self) -> None:
        manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
        self.assertIn("hooks", manifest)
        self.assertTrue(manifest["hooks"].startswith("./"), manifest["hooks"])
        self.assertEqual((ROOT / manifest["hooks"]).resolve(), HOOKS_FILE.resolve())

    def test_hooks_json_defines_the_documented_events(self) -> None:
        hooks = json.loads(HOOKS_FILE.read_text(encoding="utf-8"))["hooks"]
        self.assertEqual(set(hooks), {"SessionStart", "Stop", "PreToolUse"})
        for event, entries in hooks.items():
            self.assertTrue(entries, f"{event} has no hook entries")


if __name__ == "__main__":
    unittest.main()
