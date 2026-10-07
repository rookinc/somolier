# Security Policy and Boundary

Somolier is fail-closed by design and aligns its B32K security claims to the supplied B32K specification.

## Normative B32K security rules

- Canonicalization MUST occur before B32K hashing or signing.
- BLAKE3-256 is used where the B32K specification defines the normative payload digest or integrity hash.
- Private keys MUST never appear in logs or telemetry.
- Cryptographic roles MUST use separated keys and derivation labels when the corresponding crypto profile is enabled.
- HTTPQ AEAD, nonce, replay, timestamp, TLS, and error semantics MUST follow the B32K transport specification when HTTPQ is enabled.
- Receipt and Merkle-proof verification MUST be deterministic and side-effect-free.
- PPL is experimental/non-normative and MUST NOT be presented as adding secrecy.

## Somolier fail-closed rules

- WIFF does not execute payloads.
- SWIRL is an isolation/sealing boundary; no cryptographic protection is claimed unless a specified adapter is enabled and tested.
- TASTE performs qualification and MUST NOT persist the subject.
- DECIDE defaults to SPIT when required authority, gate, or dependency evidence is missing.
- SPIT does not allocate final subject persistence by default.
- SWALLOW is the only path to final host placement and STREAM.
- Unexpected parse, canonicalization, identity, integrity, dependency, or policy failures MUST NOT produce SWALLOW.
- Every final caller receipt must have its own independently verifiable receipt identity under the Somolier B32KID profile.

## Implementation status

The current repository is a prototype undergoing a B32K conformance rebuild. Security guarantees from unimplemented B32K sections MUST NOT be claimed merely because vocabulary or interfaces exist.
