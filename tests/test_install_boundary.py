"""Teeth tests for scripts/check_install_boundary.py.

Each test copies the declared install metadata and skill tree into a scratch root, plants
one violation, and runs the real script there. The clean copy must pass, so a red result
is caused by the planted file and nothing else.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills", "guardrails")


class InstallBoundaryTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for rel in ("package.json", ".claude-plugin/marketplace.json", "scripts/check_install_boundary.py"):
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, self.root / rel)
        shutil.copytree(ROOT / SKILL, self.root / SKILL)

    def check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / "check_install_boundary.py")],
            capture_output=True, text=True, timeout=30, check=False,
        )

    def assertFailsNaming(self, needle: str) -> None:
        proc = self.check()
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(needle, proc.stderr)

    def test_clean_skill_tree_passes(self) -> None:
        proc = self.check()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("skills/guardrails", proc.stdout)

    def test_repo_only_directory_inside_skill_fails(self) -> None:
        for banned in (".git", ".github", "__pycache__", "eval-runs", "evals", "node_modules", "research",
                       "skill-development", "tests"):
            with self.subTest(banned=banned):
                planted = self.root / SKILL / "references" / banned / "x.md"
                planted.parent.mkdir(parents=True)
                try:
                    planted.write_text("repo-only\n", encoding="utf-8")
                    self.assertFailsNaming(f"{SKILL}/references/{banned}")
                finally:
                    shutil.rmtree(planted.parent)

    def test_banned_file_inside_skill_fails(self) -> None:
        for name in ("module.pyc", "module.pyo", ".DS_Store"):
            with self.subTest(name=name):
                planted = self.root / SKILL / "assets" / name
                try:
                    planted.write_bytes(b"\0")
                    self.assertFailsNaming(name)
                finally:
                    planted.unlink()

    def test_near_miss_names_pass(self) -> None:
        # Similar names that are not repo-only artifacts must not trip the check.
        (self.root / SKILL / "references" / "testing-notes.md").write_text("ok\n", encoding="utf-8")
        (self.root / SKILL / "assets" / "evals.md").write_text("ok\n", encoding="utf-8")
        self.assertEqual(self.check().returncode, 0)

    def test_missing_declared_skill_directory_fails(self) -> None:
        shutil.rmtree(self.root / SKILL)
        self.assertFailsNaming("directory does not exist")

    def test_invalid_install_metadata_is_an_error(self) -> None:
        (self.root / "package.json").write_text("{not json", encoding="utf-8")
        proc = self.check()
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("package.json is not valid JSON", proc.stderr)

    def test_missing_skill_md_fails(self) -> None:
        (self.root / SKILL / "SKILL.md").unlink()
        self.assertFailsNaming("missing SKILL.md")


if __name__ == "__main__":
    unittest.main()
