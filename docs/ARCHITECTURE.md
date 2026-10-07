# Somolier Architecture

Status: target architecture for the B32K conformance rebuild.

    INPUT
      |
      v
    WIFF        recognize only
      |
      v
    SWIRL       isolate/seal
      |
      v
    TASTE       validate/qualify
      |         establish subject genesis identity on PASS
      v
    DECIDE      fail-closed admission
     /    \
   SPIT  SWALLOW
    |       |
    |    build / compute admitted B32K representation
    |       |
    |    host placement
    |       |
    |     STREAM
    \       /
     CALLER RECEIPT
       (always has receipt_b32kid)

## B32K core beneath the stages

Somolier does not redefine B32K.

The B32K layer provides canonicalization N(x), 15-bit index and packing semantics, BLAKE3 payload digest, B32K handle construction, optional HTTPQ transport, and optional O-1 ledger receipt verification.

The Somolier stage machine decides when those primitives are invoked and how their results are exposed.

## Identity layers

    payload_digest    B32K BLAKE3 digest
    handle            B32K payload+context digest
    packet_id         B32K HTTPQ UUIDv7 envelope ID
    B32KID            Somolier handle-derived object label
    receipt_b32kid    identity of the caller receipt
    subject_b32kid    identity of the subject, if earned
    storage_location  host placement only

These names are never interchangeable.

## File/profile framing

.b32k and B32KV001 are Somolier profile conventions, not base B32K requirements, unless a future normative B32K artifact says otherwise.

A framing convention may help WIFF recognize a file, but it does not define canonical B32K identity.

## Persistence

    SPIT    -> caller receipt; no subject STREAM by default
    SWALLOW -> build/compute -> host placement -> STREAM -> caller receipt

The caller receipt is a logical Somolier profile object whose authoritative bytes are derived through B32K canonicalization.
