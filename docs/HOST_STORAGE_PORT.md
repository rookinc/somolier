# Host Storage Port and B32KID

Somolier does not choose quarantine paths and does not generate random event
identities.

The host provides both through the StoragePort:

    allocate(source_digest, metadata)
        -> QuarantineAllocation(B32KID, location)

## Identity split

    SHA-256 = content identity
    B32KID  = ingestion-event identity

The same bytes may therefore appear in multiple ingestion events:

    same SHA-256
    different B32KID

This is intentional provenance, not duplication error.

## Why B32KID is host-issued

Somolier is deterministic. Random or clock-derived IDs inside core would make
identical executions diverge. Event identity therefore enters through an
explicit host port and becomes part of the execution inputs.

For fixed:

    input bytes
    configuration
    dependency state
    host allocation

the quarantine result is deterministic.

## Artifacts

The reference quarantine step asks the host to store:

    original.bin
    source.sha256
    wiff.json
    sealed.bin

The returned location is opaque to Somolier. It may be a filesystem path,
object-store key, database handle, encrypted volume reference, remote service
URI, or another host-defined location.

The bundled FixedMemoryStoragePort exists only for deterministic tests and
examples.
