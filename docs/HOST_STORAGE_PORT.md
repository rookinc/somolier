# Host Storage Port and B32KID

Somolier does not choose quarantine paths.

It also does not ask the host to mint identity. Every WIFF deterministically
mints a valid B32KID from the exact incoming bytes:

    B32KID = "b32kid:sha256:" + SHA256(input_bytes)

The host StoragePort receives that B32KID and chooses only placement:

    WIFF(input) -> B32KID
    allocate(B32KID, source_digest, metadata)
        -> QuarantineAllocation(B32KID, location)

A storage adapter MUST preserve the supplied B32KID.

## Identity rule

    B32KID = deterministic WIFF identity
    location = host-owned placement

Therefore the same exact bytes produce the same B32KID regardless of which
host, filesystem, object store, or quarantine service receives them.

This preserves Somolier's core law:

    same input + same config = same identity

## Artifacts

The reference quarantine step asks the host to store:

    original.bin
    source.sha256
    wiff.json
    sealed.bin

The returned location remains opaque to Somolier.
