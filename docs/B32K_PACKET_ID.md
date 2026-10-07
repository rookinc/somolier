# B32K Identity Mapping for Somolier

This document replaces the prototype packet-ID policy.

## Normative B32K identities

B32K defines distinct concepts:

- payload digest: BLAKE3-256(N(x));
- handle: BLAKE3-256 over the B32K-HANDLE domain, version, lane, and payload digest;
- HTTPQ packet_id: 128-bit UUIDv7 identifying an envelope;
- O-1 receipt: ledger inclusion proof object.

Somolier MUST preserve these meanings.

## Somolier B32KID profile

B32KID is a Somolier profile extension. It is an object label derived from the normative B32K handle/genesis context.

It MUST NOT be implemented as b32kid:sha256:<bytes> and MUST NOT be described as a normative B32K field.

The exact serialized label is versioned in the Somolier conformance profile and must preserve enough context to distinguish it from HTTPQ packet_id and raw payload digest.

## Genesis semantics

TASTE PASS establishes the subject genesis object/receipt and its B32KID.

Every caller receipt is itself an object and therefore has its own receipt_b32kid, even when the subject failed before earning a subject_b32kid.

    receipt_b32kid  always present on valid receipt
    subject_b32kid  present only when subject identity was earned
