# Host Storage and STREAM Port

Host storage is a Somolier integration boundary, not a B32K identity authority.

## Ownership

Somolier owns protocol identity, canonical data/receipt semantics, and the STREAM verb.

The host owns placement, storage technology, retention policy outside Somolier core, and opaque location/handle format.

## Placement law

Final subject placement occurs only after DECIDE returns SWALLOW.

    SPIT    -> no final subject allocation by default
    SWALLOW -> allocate(...) -> STREAM(...)

The host MUST NOT rewrite a Somolier/B32K identity supplied with the admitted object.

## Interface

    allocate(identity, metadata) -> opaque location
    stream(allocation, artifact_name, bytes) -> opaque artifact location
    read(...) -> bytes

No filesystem path is hardcoded into the core protocol.

## B32K note

Storage bytes must preserve the canonical/admitted representation chosen by the enabled profile. Host placement does not participate in N(x), payload digest, B32K handle, packet_id, or B32KID derivation unless an explicit profile says otherwise.
