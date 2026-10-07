# Somolier State Machine

Status: target architecture policy

## Public entry point

    somolier <filename> -> CallerReceipt

One invocation produces exactly one final caller receipt.

## State flow

    INPUT
      |
      v
    WIFF
      |
      v
    SWIRL
      |
      v
    TASTE
      |
      v
    DECIDE
     /    \
   SPIT  SWALLOW
    |       |
    |    BUILD/COMPUTE
    |       |
    |    HOST PLACEMENT
    |       |
    |     STREAM
    \       /
     CALLER RECEIPT

Every terminal path constructs a valid caller receipt with its own receipt_b32kid.

## WIFF

Recognizes configured framing/wrapper information without executing payloads.
Failure stops subject processing before SWIRL/TASTE and before subject identity issuance.

## SWIRL

Requires WIFF PASS.
Establishes isolated/sealed working representation.
MUST NOT issue subject_b32kid, decide admission, or allocate final persistence.

## TASTE

Requires SWIRL PASS.
Parses and validates the selected B32K/Somolier profile.
On PASS, derives subject genesis handle and subject_b32kid.
On FAIL, subject_b32kid is not issued.

## DECIDE

Requires TASTE PASS.
Consumes explicit authority, gates, dependencies, and TASTE evidence.
Missing, DISCONNECTED, FAILED, false, or unregistered required evidence fails closed to SPIT.
Exactly one disposition is returned: SPIT or SWALLOW.

## SPIT

Does not allocate final subject persistence or STREAM the subject by default.
Returns a valid caller receipt with receipt_b32kid.
Includes subject_b32kid only if already earned.

## SWALLOW

Requires DECIDE = SWALLOW.
Builds/computes final admitted representation and required canonical identities.
Requests host placement and STREAMs outputs.
Returns caller receipt with receipt_b32kid, subject_b32kid, and output locations as applicable.

## Failure policy

Unexpected errors fail closed and MUST NOT produce SWALLOW.
