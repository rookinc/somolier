# B32K Packet Identity

B32K requires every packet to carry a B32KID.

    B32KPacket = (B32KID, words)

## Two identities

B32K keeps event identity and content identity separate:

    B32KID       = ingestion-event / provenance identity
    canonical_id = content identity

The B32KID is host-issued before packetization and follows the event into the
packet. A B32K encoder MUST refuse to create a packet when no B32KID is
provided.

The canonical content ID remains a digest of packet words only. Therefore:

    same content, event A -> B32KID A, canonical ID X
    same content, event B -> B32KID B, canonical ID X

This is intentional. It allows provenance to distinguish repeated ingestion
without pretending repeated bytes are different content.

## Quarantine flow

    host allocates B32KID
        -> quarantine receipt
        -> sealed bytes
        -> B32K encode(bytes, B32KID)
        -> B32KPacket(B32KID, words)

Somolier's taste_quarantine() helper carries the quarantine B32KID into the
packet automatically.
