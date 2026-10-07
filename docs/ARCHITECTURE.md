# Somolier Architecture

    incoming object
        |
       WIFF      the nose/lips gate
        |
      SPIT <-----+ failed type/admissibility
        |               |
        |          CALLER RECEIPT
        |
      PASS
        |
      SWIRL      sealing boundary + B32KID issuance
        |
      TASTE      deterministic normalization / packetization
        |
     Decider
       / \
    SPIT SWALLOW
     |       |
     |    StoragePort
     |       |
     |     STREAM
     |       |
     +-------+
        |
   CALLER RECEIPT

## Caller return law

Every completed handling attempt returns a receipt to the original caller.

WIFF rejection returns a receipt with no B32KID because the object never passed
the lips.

A named object that reaches the Decider returns a receipt carrying its B32KID,
canonical content ID when available, disposition, and reason.

After SWALLOW + STREAM, the caller receipt may also carry the host-returned
artifact locations.

    WIFF FAIL -> caller receipt, no B32KID
    DECIDER SPIT -> caller receipt + B32KID, no STREAM
    SWALLOW -> STREAM -> caller receipt + B32KID + streamed locations

The caller receipt is Somolier's canonical return value; it does not require a
persistent host record.

## WIFF / the nose

The stock distribution recognizes only:

    .b32k

A file that does not pass WIFF gets no B32KID.

## SWIRL identity boundary

    WIFF PASS -> SWIRL -> B32KID

## Persistence boundary

    SPIT    -> no allocation, no STREAM
    SWALLOW -> host allocation -> STREAM
