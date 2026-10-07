# B32K Packet Identity

B32K requires every packet to carry a B32KID.

    B32KPacket = (B32KID, words)

## WIFF owns identity

Every WIFF generates a valid deterministic B32KID before quarantine or host
storage is consulted:

    B32KID = "b32kid:sha256:" + SHA256(input_bytes)

The host does not mint or alter it. The host only chooses storage placement.

The identity then follows the object through the chain:

    bytes
      -> WIFF(B32KID)
      -> host quarantine placement
      -> SWIRL
      -> TASTE
      -> B32KPacket(B32KID, words)

A B32K backend still rejects any packet construction without a B32KID.

## Canonical content identity

B32K currently also exposes canonical_id, the digest of the B32K word
representation. B32KID and canonical_id are both deterministic, but serve
different protocol roles:

    B32KID       = identity minted at first contact by WIFF
    canonical_id = identity of normalized B32K packet content
