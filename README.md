# Somolier

Somolier is a deterministic, fail-closed file-ingestion and qualification service being rebuilt as a B32K-aligned reference implementation.

Public shape:

    somolier <filename>
        -> WIFF
        -> SWIRL
        -> TASTE
        -> DECIDE
        -> SPIT | SWALLOW
        -> caller receipt

## Conformance policy

The supplied B32K specification is authoritative for anything Somolier calls B32K.

Somolier adopts B32K canonical CBOR, 15-bit index/packing rules, BLAKE3 digest/handle semantics, HTTPQ terminology, and O-1 receipt semantics as specified.

Somolier-specific concepts such as WIFF/SWIRL/TASTE/DECIDE, B32KID, STREAM, the .b32k filename convention, and B32KV001 framing are profile extensions and are not represented as base B32K requirements.

The current code is a prototype under conformance rebuild. Do not infer full B32K compliance from the existing implementation.

See:

    docs/ba/CONFORMANCE_PROFILE.md
    docs/ba/REQUIREMENTS_INDEX.md
    docs/ba/DATA_DICTIONARY.md
    docs/ba/STATE_MACHINE.md
    docs/ba/TRACEABILITY_MATRIX.md

## Core policy

- WIFF recognizes; it does not execute.
- SWIRL isolates/seals.
- TASTE validates/qualifies and establishes subject genesis identity on PASS.
- DECIDE fails closed to SPIT unless all required evidence passes.
- SPIT does not persist the subject by default.
- SWALLOW owns final build/compute, host placement and STREAM.
- Every final caller receipt has its own receipt B32KID.
- B32KID is a Somolier handle-derived label; it is not HTTPQ packet_id.
- Canonical cryptographic authority is B32K N(x), not JSON formatting.

## Development

    python -m pip install -e '.[dev]'
    pytest -q
    somolier-harness tests/fixtures

The current tests exercise the prototype and will be replaced or expanded by normative B32K conformance vectors during the rebuild.

## License

Project license selection remains pending project-owner approval. The supplied B32K specification identifies its own license separately.
