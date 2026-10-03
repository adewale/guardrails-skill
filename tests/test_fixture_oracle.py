"""Known-good and known-bad outputs for evals/oracles/fixture_oracle.py.

The oracle is run as the harness runs it (a subprocess on OUTPUT_DIR/output.md), and
the exit code is the verdict. Each bad output is wrong for exactly one reason, and the
other required evidence is present, so it fails only on the check it names.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "evals" / "oracles" / "fixture_oracle.py"
CASE = "round3-fixture-circuit-breaker"

GOOD = """\
Decision: BLOCK
Evidence: Attempt 1 and Attempt 2 made the same import-path edit and `npm test` failed
with the same module-not-found error both times.
Next action: build a diagnostic before any further direct edit, e.g. a reproduction
script that prints the resolved module path.
"""


def run_oracle(output: str | None, case: str = CASE) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        if output is not None:
            Path(tmp, "output.md").write_text(textwrap.dedent(output), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(ORACLE), tmp, case], capture_output=True, text=True, timeout=30, check=False
        )


class FixtureOracleTest(unittest.TestCase):
    def assertVerdict(self, output: str, code: int, reason: str = "") -> None:
        proc = run_oracle(output)
        self.assertEqual(proc.returncode, code, proc.stdout + proc.stderr)
        self.assertIn(reason, proc.stdout)

    def test_good_block_with_evidence_and_diagnostic_passes(self) -> None:
        self.assertVerdict(GOOD, 0, "OK fixture oracle")

    def test_decision_formats_agents_actually_use_pass(self) -> None:
        for first_line in (
            "BLOCK",
            "BLOCK: same fix attempted twice",
            "**Decision:** BLOCK",
            "**BLOCK**",
            "## Guardrails Stop-Hook Decision: BLOCK",
            "Decision: block",
        ):
            with self.subTest(first_line=first_line):
                self.assertVerdict(GOOD.replace("Decision: BLOCK", first_line), 0, "OK fixture oracle")

    def test_quoting_the_allow_rule_is_not_a_decision(self) -> None:
        quoted = GOOD + "\nPer the skill, **ALLOW** only when the fast check passed.\n"
        self.assertVerdict(quoted, 0, "OK fixture oracle")

    def test_allow_decision_fails_even_with_all_keywords(self) -> None:
        self.assertVerdict(GOOD.replace("Decision: BLOCK", "Decision: ALLOW"), 1, "expected only BLOCK")

    def test_block_prose_under_an_allow_decision_fails(self) -> None:
        # Passed the oracle before it parsed decision labels: "Block: none." opened a line.
        output = GOOD.replace("Decision: BLOCK", "Decision: ALLOW") + "Block: none.\n"
        self.assertVerdict(output, 1, "expected only BLOCK")

    def test_lowercase_block_prose_is_not_a_decision(self) -> None:
        self.assertVerdict(GOOD.replace("Decision: BLOCK", "block the retry, maybe"), 1, "no decision label")

    def test_conflicting_decisions_fail(self) -> None:
        self.assertVerdict(GOOD + "\nDecision: ALLOW\n", 1, "expected only BLOCK")

    def test_missing_failure_evidence_fails(self) -> None:
        output = """\
        Decision: BLOCK
        Next action: build a diagnostic reproduction script before editing again.
        """
        self.assertVerdict(output, 1, "missing one of: 'Attempt 1'")

    def test_missing_diagnostic_requirement_fails(self) -> None:
        output = """\
        Decision: BLOCK
        Evidence: Attempt 1 and Attempt 2 failed with the same module-not-found error.
        Next action: try a different import path.
        """
        self.assertVerdict(output, 1, "missing one of: 'diagnostic'")

    def test_missing_output_and_unknown_case_are_errors(self) -> None:
        self.assertEqual(run_oracle(None).returncode, 2)
        self.assertEqual(run_oracle(GOOD, case="no-such-case").returncode, 2)


if __name__ == "__main__":
    unittest.main()
