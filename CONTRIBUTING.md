# Contributing

Somolier is being rebuilt as a small B32K-aligned reference implementation.

## Authority order

Changes MUST respect this precedence:

1. supplied B32K normative specification;
2. normative standards incorporated by that specification;
3. Somolier conformance profile;
4. Somolier requirements index;
5. architecture/design documents;
6. implementation;
7. tests.

A passing test does not override a normative requirement.

## Required invariants

1. B32K normative terms retain their B32K meanings.
2. Somolier extensions are labeled as profile extensions.
3. Canonical cryptographic representation uses B32K N(x), not ad-hoc JSON formatting.
4. BLAKE3 is used wherever B32K mandates it.
5. B32KID must not be confused with HTTPQ packet_id, raw payload digest, or host storage identity.
6. Protocol stage name is DECIDE.
7. WIFF recognizes, SWIRL isolates, TASTE qualifies/establishes subject genesis identity, DECIDE admits/rejects, and SWALLOW owns final build/compute/persistence.
8. SPIT never becomes permissive because a dependency is absent.
9. Caller receipt identity and subject identity remain distinct.
10. New conformance claims require traceability to code and tests.

## Change acceptance

A change touching canonicalization, packing, hashing, handle derivation, HTTPQ, or O-1 receipts MUST include or update normative conformance vectors.

Prototype behavior that conflicts with B32K SHOULD be deleted rather than preserved unless explicitly versioned as a legacy Somolier profile.
