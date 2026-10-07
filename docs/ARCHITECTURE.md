# Somolier Architecture

    incoming object
        |
       WIFF      nose: type + raw-byte header
        |
      SPIT <-----+ failed recognition
        |               |
        |          CALLER RECEIPT.b32k
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
 CALLER RECEIPT.b32k

## Receipt law

Caller receipts are B32K files.

    raw header: B32KV001
    body: canonical compact UTF-8 JSON

A WIFF failure gets a .b32k receipt with no B32KID for the rejected input.
A later receipt may carry the identities earned by later stages.

The persisted SWALLOW-side receipt is named:

    receipt.b32k

## WIFF / the nose

The shipped valid type registry contains one entry:

    extension: .b32k
    raw magic: 42 33 32 4B 56 30 30 31
    ASCII:     B32KV001

## DECIDE

DECIDE is the canonical admission verb and stage name.

## Persistence boundary

    SPIT    -> no allocation, no STREAM
    SWALLOW -> host allocation -> STREAM
