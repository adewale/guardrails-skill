#!/bin/bash
# Reproduction script: [describe what this reproduces]
# Built by agent during debugging session on [date]
#
# Usage: ./repro-[name].sh
# Expected: exits 0 if bug is NOT present, exits 1 if bug IS present
#
# This script should:
# 1. Set up minimal preconditions
# 2. Trigger the exact conditions that cause the bug
# 3. Check for the buggy behavior
# 4. Clean up after itself
# 5. Print a clear message about what happened

set -euo pipefail

# --- Setup ---
# Create any temporary state needed to reproduce the bug.
# Keep this minimal — the more setup, the less useful the repro.


# --- Trigger ---
# Execute the exact operation that causes the bug.


# --- Check ---
# Verify whether the bug is present.
# Exit 0 = bug not present (good), Exit 1 = bug present (bad)


# --- Cleanup ---
# Remove any temporary state.


echo "Reproduction complete."
