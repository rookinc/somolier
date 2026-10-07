# Somolier

Somolier is a deterministic, fail-closed ingestion and normalization codec with
pluggable storage, packet, and Decider ports.

Its canonical ritual is:

    WIFF -> HOST STORAGE -> SWIRL -> TASTE -> DECIDER -> SPIT | SWALLOW

Somolier **describes and normalizes**. The Decider **admits or rejects**.

## Core promise

    same input + same config = same WIFF identity
    same input + same config + same dependency state = same processing result

There is no permissive disconnected mode: missing, DISCONNECTED, or FAILED
required dependencies produce SPIT.

## B32KID starts at WIFF

Every WIFF mints a valid B32KID immediately:

    B32KID = "b32kid:sha256:" + SHA256(input_bytes)

The same exact bytes produce the same B32KID on every host.

## Host storage

The host chooses placement; Somolier owns the storage verbs.

    allocate(...) -> location
    stream(allocation, artifact_name, payload) -> location
    read(allocation, artifact_name) -> bytes

The canonical file-output verb is **STREAM**. Somolier streams artifacts to a
host-owned destination without assuming whether that destination is a file,
blob, object, database record, pipe, or remote service.

## B32K packet law

Every B32K packet MUST carry its WIFF B32KID:

    bytes
      -> WIFF(B32KID)
      -> quarantine
      -> TASTE
      -> B32KPacket(B32KID, words)

The B32K backend refuses packet construction without a B32KID.

## Native packet backend

Somolier v0.1 ships with B32K as the default packet backend.

## King's Taster model

Nothing is consumed until it has earned SWALLOW.

## Test harness

Run:

    python -m pip install -e '.[dev]'
    pytest -q
    somolier-harness tests/fixtures

The harness checks deterministic WIFF/B32KID generation, B32K round trips,
STREAM storage output, evidence preservation, fail-closed Decider behavior,
disconnected ports, and host-independent quarantine identity.

## Status

Early reference implementation. B32K is bundled. Host storage is a placement
port, not an identity authority. Production cryptographic SWIRL adapters remain
separate work.

## License

License selection is intentionally pending project-owner approval.
