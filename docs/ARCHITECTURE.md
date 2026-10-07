# Somolier Architecture

    incoming object
        |
       WIFF      nose: type + raw-byte header
        |
      SPIT <-----+ failed recognition
        |               |
        |          CALLER RECEIPT
        |
      PASS
        |
      SWIRL      sealing boundary
        |
      TASTE      qualification
        |
      DECIDE     fail-closed admission
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

## WIFF / the nose

The shipped valid type registry contains one entry:

    extension: .b32k
    raw magic: 42 33 32 4B 56 30 30 31
    ASCII:     B32KV001

A stock WIFF passes only when the extension is .b32k and the first eight bytes
match B32KV001.

A file that merely has a .b32k suffix but the wrong raw header is rejected with
invalid_file_header and gets no B32KID.

## DECIDE

DECIDE is the canonical admission verb and stage name.

The implementation's policy objects may expose a decide(...) method, but the
protocol stage itself is DECIDE, not DECIDER.

## Caller return law

Every completed handling attempt returns a receipt to the original caller.

    WIFF FAIL -> caller receipt, no B32KID
    DECIDE -> SPIT -> caller receipt, no STREAM
    DECIDE -> SWALLOW -> STREAM -> caller receipt + streamed locations

## Persistence boundary

    SPIT    -> no allocation, no STREAM
    SWALLOW -> host allocation -> STREAM
