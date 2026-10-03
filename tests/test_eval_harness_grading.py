"""Grade a known-good and a known-bad round-3 output with the pinned Skill Eval Harness.

This exercises the seam the oracle unit tests cannot: that the manifest's `script`
assertion resolves `oracles/fixture_oracle.py`, passes `{output_dir}`, and that the
harness reads the oracle's exit code as the verdict. Model-free: `grade` only reads saved
outputs. Needs `uvx`; set SKILL_BENCHMARK to override the command.
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_fixture_oracle import GOOD

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evals" / "shared-benchmark.json"
CASE = "round3-fixture-circuit-breaker"
SKILL_BENCHMARK = os.environ.get("SKILL_BENCHMARK", "uvx --from skill-eval-harness==0.6.0 skill-benchmark")

# Passed every objective assertion of this case, the script oracle included, before the
# oracle parsed decision labels.
BAD = GOOD.replace("Decision: BLOCK", "Decision: ALLOW") + "Block: none.\n"


def script_verdict(output: str) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp, "runs", CASE, "with_skill")
        run_dir.mkdir(parents=True)
        (run_dir / "output.md").write_text(output, encoding="utf-8")
        out = Path(tmp, "grade.json")
        cmd = [*shlex.split(SKILL_BENCHMARK), "grade", str(MANIFEST), "--runs", str(Path(tmp, "runs")),
               "--allow-scripts", "--out", str(out)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600, check=False)
        if proc.returncode != 0:
            raise AssertionError(f"`{shlex.join(cmd)}` exited {proc.returncode}: {proc.stderr[-2000:]}")
        results = json.loads(out.read_text(encoding="utf-8"))["results"]
    graded = [
        a for r in results
        if r["case_id"] == CASE and r["variant"] == "with_skill" and not r["missing_output"]
        for a in r["assertions"] if a["name"] == "fixture-script-oracle"
    ]
    if len(graded) != 1:
        raise AssertionError(f"expected one graded fixture-script-oracle assertion, got {graded}")
    return graded[0]["passed"]


class HarnessScriptAssertionTest(unittest.TestCase):
    def test_harness_passes_good_output(self) -> None:
        self.assertIs(script_verdict(GOOD), True)

    def test_harness_fails_allow_decision(self) -> None:
        self.assertIs(script_verdict(BAD), False)


if __name__ == "__main__":
    unittest.main()
