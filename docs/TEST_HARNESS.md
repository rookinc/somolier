# Somolier Conformance Harness

The harness exists to prove behavior against requirements, not to preserve prototype outputs.

## Required test layers

1. B32K normative vectors: canonicalization Appendix A, 15-bit packing, and established BLAKE3/handle vectors.
2. Somolier stage tests: WIFF, SWIRL, TASTE, DECIDE, SPIT, SWALLOW, STREAM.
3. Receipt tests: every final receipt has receipt_b32kid; identity recomputes; subject identity is absent before TASTE PASS; receipt and subject identities remain distinct.
4. Negative/security tests: malformed canonical data, duplicate keys, invalid indices, bad padding, changed receipts, identity mismatch, disconnected dependencies, and gate failure.

## Public entry-point rule

The primary harness MUST exercise:

    somolier <filename>

or the equivalent single public service function. It MUST NOT reproduce the state machine manually as its main conformance path.

## Output

Progress output SHOULD retain:

    [current/total] PASS|FAIL ...

for Termux/mobile use.

## Boundary

The harness contains no RookOS/PAN/Hat/kiosk policy. External authorization is represented only by generic test policy inputs.
