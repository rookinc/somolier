# Somolier Test Harness v0.1

The harness exercises Somolier independently of RookOS or any other policy system.

## Core invariants

1. Same source bytes produce the same source digest.
2. Same source bytes under the same backend produce the same canonical packet identity.
3. Supported payloads round-trip exactly through the bundled B32K backend.
4. SWIRL v0.1 preserves the evidence bytes exactly.
5. An unregistered Decider always returns SPIT.
6. A registered Decider reaches SWALLOW only when every required gate passes.
7. Empty and malformed specimens remain testable evidence; the harness does not delete them.

## Run

    python -m pip install -e '.[dev]'
    pytest -q
    somolier-harness tests/fixtures

Machine-readable output:

    somolier-harness tests/fixtures --json

The CLI prints progress as [current/total] for phone and Termux use.

## Policy boundary

The harness ships no RookOS policy and knows nothing about PAN, Hats, kiosks,
or organization authority. RegisteredDecider in tests is a generic mock decision surface.
