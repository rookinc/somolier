# Somolier

Somolier is a deterministic, fail-closed ingestion and normalization codec with
pluggable storage, packet, and Decider ports.

Its canonical ritual is:

    WIFF -> HOST STORAGE -> SWIRL -> TASTE -> DECIDER -> SPIT | SWALLOW

Somolier **describes and normalizes**. The Decider **admits or rejects**.

## Core promise

    somolier(input, config, dependency_state, host_ports) -> output

For the same input, same configuration, same reported dependency state, and
same explicit host-port responses, Somolier produces the same output.

There is no permissive disconnected mode:

- unregistered Decider -> SPIT
- missing required dependency -> SPIT
- DISCONNECTED dependency -> SPIT
- FAILED dependency -> SPIT
- missing or failed required gate -> SPIT
- SWALLOW only when every required port is READY and every required gate passes

## Host storage and B32KID

Somolier never hardcodes a quarantine path. It asks the host StoragePort where
to put an ingestion event.

The host returns:

    B32KID  = unique ingestion-event identity
    location = opaque quarantine location/handle

Somolier separately computes SHA-256 content identity:

    SHA-256 = what bytes are these?
    B32KID  = which ingestion event is this?

The same content may therefore have the same SHA-256 and different B32KIDs on
different ingestion events.

## Native packet backend

Somolier v0.1 ships with **B32K** configured as the default packet backend.

    surface presentation -> Somolier -> B32K packet -> Decider

The backend remains pluggable so downstream projects can replace B32K without
changing the Somolier protocol.

## King's Taster model

The Somolier persona is the tasting surface. The security office underneath is
the King's Taster: nothing is consumed until it has earned SWALLOW.

## Test harness

Somolier ships a policy-neutral test harness with deterministic receipt checks,
B32K round-trip checks, evidence-preservation checks, fail-closed Decider
tests, disconnected-port tests, and host-storage/B32KID tests.

Run:

    python -m pip install -e '.[dev]'
    pytest -q
    somolier-harness tests/fixtures

The harness intentionally contains no RookOS, PAN, Hat, kiosk, or customer-policy
logic.

## Status

Early reference implementation. B32K is the bundled packet backend. Host
storage is a port, not protocol-owned placement. Production cryptographic
SWIRL adapters remain separate work.

## License

License selection is intentionally pending project-owner approval.
