# Somolier

Somolier is a deterministic, fail-closed ingestion and normalization codec with
a pluggable packet backend and an external Decider port.

Its canonical ritual is:

    WIFF -> SWIRL -> TASTE -> DECIDER -> SPIT | SWALLOW

Somolier **describes and normalizes**. The Decider **admits or rejects**.

## Core promise

    somolier(input, config, dependency_state) -> output

For the same input, same configuration, and same reported dependency state,
Somolier produces the same output.

There is no permissive disconnected mode:

- unregistered Decider -> SPIT
- missing required dependency -> SPIT
- DISCONNECTED dependency -> SPIT
- FAILED dependency -> SPIT
- missing or failed required gate -> SPIT
- SWALLOW only when every required port is READY and every required gate passes

## Native packet backend

Somolier v0.1 ships with **B32K** configured as the default packet backend.

    surface presentation -> Somolier -> B32K packet -> Decider

The backend remains pluggable so downstream projects can replace B32K without
changing the Somolier protocol.

## King's Taster model

The Somolier persona is the tasting surface. The security office underneath is
the King's Taster: nothing is consumed until it has earned SWALLOW.

## Test harness

Somolier ships a policy-neutral test harness with:

- golden fixtures
- deterministic receipt checks
- B32K round-trip checks
- evidence-preservation checks
- fail-closed Decider tests
- disconnected-port tests
- progress output suitable for Termux

Run:

    python -m pip install -e '.[dev]'
    pytest -q
    somolier-harness tests/fixtures

Machine-readable harness output:

    somolier-harness tests/fixtures --json

The harness intentionally contains no RookOS, PAN, Hat, kiosk, or customer-policy
logic.

## Status

Early reference implementation. The current B32K backend provides a reversible
byte-to-B32K packetization path. Higher-level semantic dictionaries and
production cryptographic SWIRL adapters remain separate work.

## Development

    python -m pip install -e '.[dev]'
    pytest -q

## License

License selection is intentionally pending project-owner approval.
