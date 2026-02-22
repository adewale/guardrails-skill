# Tool Building and Notation — Reference

When the agent is stuck, the default behavior is to re-read the code and try again
harder. This rarely works. The code hasn't changed; re-reading it produces the same
mental model that led to the wrong fix. What the agent needs is *new information* or
a *different representation* of the problem.

Human developers do this instinctively. When confused about control flow, they add
logging. When confused about state, they draw a diagram. When a function has too many
branches to hold in their head, they build a truth table. The tool or notation isn't
the deliverable — it's scaffolding that makes the real fix possible.

Agents almost never do this unprompted. This reference tells the agent when and how.

## Table of Contents
- [Reactive: Circuit Breaker Escalation](#reactive-circuit-breaker-escalation)
- [Diagnostic Tool Catalog](#diagnostic-tool-catalog)
- [Notation Catalog](#notation-catalog)
- [Proactive: Task Class Recognition](#proactive-task-class-recognition)
- [Diagnostic Tools as Verification](#diagnostic-tools-as-verification)
- [The Agent Tool Library](#the-agent-tool-library)
- [Worked Examples](#worked-examples)

---

## Reactive: Circuit Breaker Escalation

The thrashing circuit breaker (defined in SKILL.md, Stop hook) mandates diagnostic
escalation after 2 failed attempts at the same fix. At that point, the agent chooses
from the diagnostic tool catalog or the notation catalog below.

The logic: if two direct-fix attempts failed, the agent's mental model of the problem
is wrong. Trying harder with the same model won't help. The agent needs either empirical
data (a diagnostic tool that shows what's actually happening) or a structured view (a
notation that makes the problem's shape visible).

## Diagnostic Tool Catalog

Each of these is a script that provides empirical data the agent doesn't currently have.

**Reproduction script** — Isolates the failure to a minimal, self-contained case.
This is always a valid first choice. If you don't have a reproduction script, build
one before trying anything else. A good reproduction script runs in seconds, requires
no manual setup, and produces a clear pass/fail result. It often becomes a test case.
Use the template at `assets/notation-templates/reproduction-script.sh`.

**Tracing harness** — Instruments a code path to show actual runtime flow, argument
values, and return values at each step. Build this when the agent's assumption about
*what code runs and in what order* keeps being wrong. The trace provides ground truth
that replaces guessing about execution flow.

**Schema/state checker** — Verifies that the current state of the database, config, or
environment matches what the code expects. Build this when failures seem environment-
dependent or when the agent suspects the problem is "the data doesn't look like the
code assumes." It can graduate into a permanent health check.

**Fixture generator** — Produces valid test data conforming to complex schemas. Build
this when hand-written fixtures might be subtly wrong (violating cross-field constraints,
missing required nested objects, using stale enum values). A generator is more reliable
than a human (or agent) manually constructing valid data.

**Dependency mapper** — Traces imports and call relationships to answer "what actually
calls this function?" or "what does this module depend on?" Build this when modifying
shared code and unsure of the blast radius. It directly feeds the integration/deployment
check at commit time.

## Notation Catalog

Each of these is a structured representation that makes the problem's shape visible.
Write the notation into a file (e.g., `debug-state-table.md`) so it survives across the
agent's context window and can be shared with the user.

**State transition table** — Format: State × Event → NewState + Actions. Use for code
with explicit state variables and transitions. Reveals missing transitions, dead states,
and impossible state combinations.

**Decision matrix / truth table** — Lists all input combinations for a function with
multiple boolean conditions. A 4-input function has 16 combinations; listing them reveals
which cases the code doesn't handle.

**Data flow diagram** — Format: Input → Transform A → Intermediate → Transform B →
Output, with sample values at each stage. Use for pipelines and chained transforms.
Plug in a concrete example and trace it through each step — the step where the value
goes wrong is where the bug is.

**Call site inventory** — Format: Caller → Method → Arguments → What it does with the
return value. Build this *before* modifying any function signature or public API. It
answers: "if I change this interface, what breaks?" Prevents the common "fixed the
function but broke 4 callers" failure.

**Invariant catalog** — Lists every property that should hold: "output length ≤ input
length", "round-trip serialization is identity", "balance never goes negative." Directly
generates property-based test cases. Building this notation *is* the design work for
property tests — externalized where the agent can review it.

## Proactive: Task Class Recognition

Don't wait for failure. Some problem shapes reliably benefit from tools or notations
built *before* writing production code. During planning, recognize these patterns and
build the scaffolding first:

| Problem shape | Signal | Build or find |
|---|---|---|
| Modifying a function's interface | Change touches a signature, return type, or public API | Call site inventory before changing anything |
| Complex conditional logic | Function with >3 boolean parameters or >4 branches | Decision matrix / truth table |
| State machine behavior | Code with explicit state variables and transitions | State transition table |
| Data transformation pipeline | Chained transforms with intermediate values | Data flow diagram with sample values at each stage |
| Unfamiliar codebase area | Agent is editing files in >3 directories it hasn't seen before | Codebase index: modules, exports, dependencies |
| Complex test data requirements | Schema with >5 fields, nested objects, or cross-field constraints | Fixture generator script |
| Repeated manual verification | Agent runs the same check >3 times during a session | Checker script in `script/agent-tools/` |
| Debugging integration failures | Unclear which services or modules interact | Dependency / interaction map |
| Performance investigation | Timing-sensitive or load-dependent behavior | Benchmarking harness with baseline measurements |

The proactive case is about *leverage*. A 20-line tracing script built in 2 minutes
can save 20 minutes of guessing. A call site inventory built before changing an API
prevents the "fixed the function but broke 4 callers" failure that triggers the
circuit breaker.

## Diagnostic Tools as Verification

Building a diagnostic tool is not a detour from the task — it is often the most
direct path to completing the task. A reproduction script that reliably triggers the
bug is itself a test case. A fixture generator produces artifacts the test suite
reuses. A tracing harness can become a permanent debugging utility.

Treat diagnostic tool creation as a legitimate work product:
- If the tool is reusable beyond the current task, persist it to `script/agent-tools/`
  with a one-line description comment at the top.
- If the tool revealed something non-obvious, record a lesson in `LESSONS_LEARNED.md`.
- If the tool evolved into a test case or test utility, move it into the test suite
  where it belongs.
- If the notation (state table, decision matrix) clarified the design, consider
  keeping it as documentation.

## The Agent Tool Library

Persist reusable tools to `script/agent-tools/`. This directory is the project's
accumulating toolkit — each session's diagnostic work becomes the next session's
proactive preparation.

**Structure:**
```
script/agent-tools/
├── trace-auth-flow.sh        # Instruments the auth middleware chain
├── validate-schema.py        # Checks DB schema matches migrations
├── generate-fixtures.py      # Produces valid test data for Order model
├── map-imports.sh            # Shows import graph for a given module
└── README.md                 # Index of tools with one-line descriptions
```

**Rules:**
- Every tool has a one-line description comment as its first line.
- Every tool is executable and exits non-zero on failure.
- `README.md` in the directory serves as the index. Update it when adding tools.
- At SessionStart, the agent reads this directory to know what's available.
- Before building a new tool, check: does one already exist in `script/agent-tools/`?
  Does the project already have a utility in `script/`, `bin/`, or `Makefile`? Is there
  a well-known CLI tool (`jq`, `ripgrep`, `hyperfine`, `strace`, `py-spy`, etc.)?
- Tools that rot (built for a code version that no longer exists) should be fixed or
  removed during periodic maintenance.

---

## Worked Examples

### Example 1: Circuit Breaker Fires During State Machine Debugging

**Context:** Agent is fixing a bug where an order status gets stuck in "processing."

**Attempt 1:** Agent reads the `OrderStateMachine` class, notices the "processing →
shipped" transition requires a tracking number, adds a default tracking number when
none is provided. Tests fail — the fix introduced a different bug where orders ship
without real tracking numbers.

**Attempt 2:** Agent reverts and instead tries to add a "processing → failed" timeout
transition. Tests still fail — a different test expects orders in "processing" to
eventually reach "shipped" without intervention.

**Circuit breaker fires.** The agent escalates before attempt 3.

**Agent builds a state transition table:**
```
| Current State | Event              | Next State  | Actions            |
|---------------|--------------------|-------------|--------------------|
| pending       | payment_confirmed  | processing  | notify_warehouse   |
| processing    | tracking_added     | shipped     | notify_customer    |
| processing    | ???                | ???         | ???                |
| shipped       | delivery_confirmed | delivered   | close_order        |
| *             | cancel_requested   | cancelled   | refund_payment     |
```

The table reveals the gap: there's no transition from "processing" when the warehouse
rejects the order. The fix isn't a timeout or a default tracking number — it's a new
`warehouse_rejected` event that transitions to a "fulfillment_failed" state.

**Attempt 3 (with diagnostic):** Agent adds the missing state and transition. Tests pass.

**Outcome:** Agent persists the state transition table as documentation alongside the
state machine class. Records a lesson: "When debugging state machine bugs, build a
transition table before attempting code changes."

### Example 2: Proactive Call Site Inventory Before API Change

**Context:** Agent is tasked with adding pagination to a `listUsers()` API endpoint.

**During planning:** Agent recognizes this matches "Modifying a function's interface"
in the proactive table. Before changing anything, it builds a call site inventory:

```
| Caller                    | Method      | Arguments    | Uses return value as      |
|---------------------------|-------------|--------------|---------------------------|
| UserController.index      | listUsers() | (none)       | Response body (all users) |
| AdminDashboard.getStats   | listUsers() | (none)       | .length for user count    |
| ExportService.generateCSV | listUsers() | (none)       | Iterates all for CSV rows |
| SeedScript.verify         | listUsers() | (none)       | Asserts count matches     |
```

The inventory reveals that `AdminDashboard.getStats` and `ExportService.generateCSV`
both depend on getting *all* users. Simply adding pagination would break them silently
(they'd get page 1 and think that's everything — no error, just wrong data).

**Agent's plan:** Add `listUsers({ page, perPage })` with backwards-compatible defaults
that return all users when no pagination is specified. Add `countUsers()` for the admin
dashboard. Update the export service to paginate through all pages.

**Outcome:** Without the inventory, the agent would likely have changed the signature,
updated the controller, written tests for pagination, and committed — passing all tests
because the admin dashboard and export service don't have tests that catch "got partial
data." The integration/deployment check might have caught the wiring gap, but the
*semantic* gap (code works but returns wrong results) would have shipped.

### Example 3: Reproduction Script Graduates to Test Suite

**Context:** Agent is debugging a flaky test that fails only when run in parallel.

**Circuit breaker fires** after two attempts at adding locks and sleep() calls.

**Agent builds a reproduction script** (`script/agent-tools/repro-parallel-user-create.sh`):
```bash
#!/bin/bash
# Reproduces race condition in user creation when two requests arrive simultaneously
for i in {1..20}; do
  (curl -s -X POST localhost:3000/api/users -d '{"email":"test@example.com"}' &
   curl -s -X POST localhost:3000/api/users -d '{"email":"test@example.com"}' &
   wait)
  DUPES=$(psql -t -c "SELECT COUNT(*) FROM users WHERE email='test@example.com'")
  if [ "$DUPES" -gt 1 ]; then
    echo "RACE CONDITION: $DUPES duplicate users created on iteration $i"
    psql -c "DELETE FROM users WHERE email='test@example.com'"
    exit 1
  fi
  psql -c "DELETE FROM users WHERE email='test@example.com'" > /dev/null
done
echo "No race condition detected in 20 iterations"
```

The script reliably reproduces the race condition in ~3 iterations. The fix is a unique
constraint on the email column plus an upsert pattern.

**Outcome:** The reproduction script's logic is extracted into an integration test
(`test_concurrent_user_creation`) that runs as part of the integration test suite. The
bash script stays in `script/agent-tools/` as a quick smoke test for similar race
conditions. Lesson recorded: "User creation endpoint lacks unique constraint — always
check for uniqueness constraints when debugging duplicate-record bugs."
