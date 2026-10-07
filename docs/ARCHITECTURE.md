# Somolier Architecture

    incoming object
        |
       WIFF      the nose/lips gate
        |
      SPIT <-----+ failed type/admissibility
        |
      PASS
        |
      SWIRL      sealing boundary + B32KID issuance
        |
      TASTE      deterministic normalization / packetization
        |
     Decider     external configured gates and dependency states
       / \
    SPIT SWALLOW
             |
          StoragePort
             |
           STREAM

## WIFF / the nose

WIFF owns a configured list of valid file types. The stock distribution ships
with exactly one valid type:

    .b32k

A file that does not pass WIFF gets no B32KID and does not proceed to SWIRL.

The valid type list is configuration, so a host may deliberately extend it,
but the shipped default remains .b32k only.

## SWIRL identity boundary

B32KID issuance occurs in SWIRL, never WIFF.

    WIFF PASS -> SWIRL -> B32KID

With the current deterministic reference implementation:

    B32KID = "b32kid:sha256:" + SHA256(input_bytes)

## Persistence boundary

Host placement is after the Decider. Default behavior is:

    SPIT    -> no allocation, no STREAM
    SWALLOW -> host allocation -> STREAM

Somolier therefore does not persist material it has already rejected unless a
future explicit retention policy says otherwise.

## Deterministic service law

For fixed bytes, valid-file-type configuration, dependency state, and Decider
inputs, Somolier follows the same algorithm and produces the same receipts.

## Packet backend

B32K is bundled and configured by default. Every B32K packet carries the
B32KID issued by SWIRL.
