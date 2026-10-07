# Somolier Business Analysis Artifact Scan

Status: working analysis baseline
Scope: current `rookinc/somolier` main branch and the supplied B32K Open Specification
Purpose: preserve the useful Somolier product idea while rebuilding implementation claims against the actual B32K specification and explicit Somolier profile requirements.

## 1. Source-of-truth order

When sources disagree, use this order:

1. B32K Open Specification normative text.
2. Normative external standards referenced by B32K.
3. Explicit Somolier product/profile decisions.
4. Somolier requirements index.
5. Architecture/design documents.
6. Current implementation.
7. Tests and fixtures.

Code and tests are evidence of the prototype, not authority over the specification.

## 2. Product intent retained

The current prototype has established a useful product shape:

    somolier <filename>
        -> WIFF
        -> SWIRL
        -> TASTE
        -> DECIDE
        -> SPIT | SWALLOW
        -> caller receipt

Retain these product principles:

- one input, one deterministic processing algorithm;
- configuration supplies policy and adapters rather than hidden behavior;
- fail closed on missing or failed required dependencies;
- WIFF is recognition only and must not execute payload content;
- SWIRL is the isolation/sealing boundary;
- TASTE is the qualification/inspection stage;
- DECIDE is the admission verb;
- SPIT means reject admission;
- SWALLOW means the object may be built/computed/persisted under configured policy;
- STREAM is the file-output verb;
- host owns placement, Somolier owns protocol semantics;
- caller always receives a receipt;
- Somolier remains independent of RookOS/PAN policy.

These are Somolier profile requirements, not claims about the B32K base specification.

## 3. B32K specification baseline

The supplied B32K specification defines, among other things:

- authoritative 15-bit indices in [0, 32767];
- canonicalization N(x) using UTF-8 NFC plus canonical CBOR;
- definite-length canonical CBOR, shortest integer encodings, canonical map-key ordering, and no duplicate keys;
- big-endian bit-packing of 15-bit indices;
- BLAKE3-256 as the normative payload/integrity hash;
- an HTTPQ authenticated transport envelope with a UUIDv7 packet_id and a BLAKE3-derived handle;
- O-1 receipts for Merkle/ledger inclusion;
- deterministic, side-effect-free receipt verification;
- normative HTTPQ verification error codes.

The specification does not define a universal `kind` field.

The specification does not, in the supplied text, define the Somolier-specific filename extension `.b32k` or the provisional ASCII magic `B32KV001`. Those must be treated as Somolier profile conventions unless a later B32K specification artifact makes them normative.

## 4. Current repository artifact inventory

### Root and governance

| Artifact | Current role | Assessment | Action |
|---|---|---|---|
| `README.md` | product description | useful but reflects prototype semantics | REWRITE against requirements |
| `SECURITY.md` | security boundary | good fail-closed intent; stale persistence wording | REWRITE |
| `CONTRIBUTING.md` | contributor invariants | useful governance shell | REWRITE after target architecture |
| `pyproject.toml` | package metadata/CLI | good minimal packaging | KEEP, update dependencies/version later |
| `.github/workflows/test.yml` | CI | useful baseline | KEEP, expand conformance matrix |

### Architecture and protocol docs

| Artifact | Assessment | Action |
|---|---|---|
| `docs/ARCHITECTURE.md` | useful stage model, not yet spec-aligned | REWRITE |
| `docs/B32K_PACKET_ID.md` | materially conflicts with B32K spec: SHA-256/WIFF identity claims | RETIRE/REPLACE |
| `docs/DECIDER_PORT.md` | useful fail-closed policy concept; terminology now DECIDE | REWRITE |
| `docs/HOST_STORAGE_PORT.md` | useful host-placement abstraction; stale identity semantics | REWRITE |
| `docs/TEST_HARNESS.md` | useful harness intent; stale stage/retention assumptions | REWRITE |

### Registry

| Artifact | Assessment | Action |
|---|---|---|
| `registry/somolier_dictionary.v0.1.json` | prototype vocabulary; stale DECIDER and stage definitions | REPLACE with versioned profile registry |

### Source code

| Artifact | Assessment | Action |
|---|---|---|
| `backend.py` | useful plugin boundary | KEEP concept, redesign contract |
| `backends/b32k.py` | prototype byte-per-word codec; not B32K spec implementation | REPLACE |
| `model.py` | useful typed receipts/states; identity placement stale | REWRITE |
| `pipeline.py` | accumulated orchestration and prototype serialization | SPLIT into stage modules/service |
| `decider.py` | useful fail-closed logic | KEEP concept, rename protocol semantics to DECIDE |
| `readiness.py` | useful deterministic dependency-state logic | KEEP |
| `storage.py` | useful host placement + STREAM abstraction | KEEP concept |
| `dictionary.py` | stale terminology | REPLACE from registry |
| `cli.py` | correct public shape but manual pipeline composition | THIN to service entry point |
| `harness.py` | useful prototype harness | REBUILD against public service API |
| `harness_cli.py` | useful Termux progress surface | KEEP, rebuild on new harness |

### Tests and fixtures

| Artifact | Assessment | Action |
|---|---|---|
| `tests/test_*.py` | validates current prototype only | REWRITE incrementally |
| `tests/fixtures/clean/hello.b32k` | Somolier-profile fixture, not proven B32K-conformant | REPLACE with spec vectors |
| non-B32K fixtures | useful WIFF negative cases | KEEP |
| `tests/golden/v0.1.json` | stale SHA-256 prototype manifest | RETIRE |
| B32K Appendix A vectors | absent from repo | ADD as conformance fixtures |

## 5. Material prototype/spec gaps

### GAP-001 Canonicalization

Prototype: compact JSON and ad-hoc byte handling.
B32K: canonical CBOR over UTF-8 NFC normalized structured data.

Required correction: implement and test N(x) exactly.

### GAP-002 Hash function

Prototype: SHA-256 for B32KID/canonical IDs.
B32K: BLAKE3-256 is normative for payload digest and Merkle aggregation.

Required correction: remove any claim that SHA-256 identity is B32K normative. Use BLAKE3 where the B32K specification requires it.

### GAP-003 B32K packet encoding

Prototype: one integer word per source byte.
B32K: 15-bit indices packed big-endian into a continuous bitstream with zero padding to the nearest octet.

Required correction: replace backend encoding with normative 15-bit pack/unpack behavior and Appendix A test vectors.

### GAP-004 Identity vocabulary

Prototype: B32KID, canonical_id, source SHA-256, and packet identity overlap.
B32K: separates payload digest, handle, packet_id (UUIDv7), and O-1 receipt concepts.

Required correction: define a Somolier B32KID profile precisely, including how it relates to a normative B32K handle and genesis receipt, without renaming existing normative fields.

### GAP-005 Receipt format

Prototype: `B32KV001` + compact JSON with Somolier fields.
B32K: canonical CBOR is authoritative; O-1 receipt has a fixed normative schema and additionalProperties=false.

Required correction: do not call a Somolier caller receipt an O-1 receipt unless it conforms exactly. Define a separate Somolier receipt profile/container if needed, using B32K canonicalization.

### GAP-006 Filename and magic

Prototype: `.b32k` and `B32KV001` treated as B32K protocol facts.
Supplied B32K spec: neither appears.

Required correction: retain only as explicit Somolier profile conventions pending a normative B32K framing rule.

### GAP-007 Stage ownership

Prototype currently issues B32KID/builds packet/computes canonical identity before the agreed target stage boundaries.

Target product semantics:

    WIFF    recognize
    SWIRL   isolate/seal
    TASTE   inspect/qualify; issue genesis identity on PASS
    DECIDE  admit/reject
    SPIT    return receipt; no persistence by default
    SWALLOW build/compute; host placement; STREAM

Required correction: reassign code responsibilities accordingly.

### GAP-008 Caller receipt identity

Product decision: every valid Somolier receipt must possess its own B32KID; a receipt without one is invalid.

This must be implemented without confusing receipt identity with subject identity. The receipt may testify about an unnamed rejected subject while still having its own valid identity.

### GAP-009 Current documentation drift

Several documents still assert WIFF-issued identity, DECIDER terminology, quarantine-before-decision behavior, SHA-256 B32K identity, and JSON receipt framing.

Required correction: requirements index becomes the transition authority; stale docs should be replaced only as implementation reaches the corresponding requirement.

## 6. Business boundaries

### In scope for Somolier core

- deterministic single-file processing;
- configurable recognition profiles;
- isolation/sealing abstraction;
- B32K conformance processing;
- qualification and genesis receipt production;
- fail-closed DECIDE interface;
- B32K receipt return to caller;
- post-SWALLOW host placement and STREAM;
- deterministic offline verification;
- pluggable host adapters.

### Not inherently in Somolier core

- RookOS/PAN/Hat/kiosk semantics;
- customer business policy;
- ledger operation itself;
- key custody;
- TLS termination;
- remote storage ownership;
- arbitrary code execution;
- semantic truth adjudication.

These may be supplied by configured ports or higher-level services.

## 7. Source issues requiring explicit resolution

1. The supplied PDF front page says v1.0.0 while its closing metadata says Version 1.1.0 Stable Draft. The implementation must not silently choose a normative version; record the selected conformance target explicitly.
2. The PDF abstract says canonicalization combines UTF-8 NFC with canonical CBOR, while Appendix C describes O-1 receipts as JSON objects canonicalized under N(x). The implementation should model the logical object separately from the canonical CBOR bytes and treat human-readable JSON as a representation, not the signing/hash authority.
3. Somolier's B32KID/genesis-receipt concept is a profile extension unless and until incorporated into the B32K specification. It must never be presented as already normative B32K.

## 8. Recommended next artifacts

1. `docs/ba/REQUIREMENTS_INDEX.md` — traceable SHALL/SHOULD/MAY requirements.
2. `docs/ba/CONFORMANCE_PROFILE.md` — exact B32K version and Somolier extensions.
3. `docs/ba/DATA_DICTIONARY.md` — distinguish B32K handle, packet_id, B32KID, receipt ID, subject ID, and storage location.
4. `docs/ba/STATE_MACHINE.md` — stage preconditions/postconditions and failure exits.
5. `docs/ba/TRACEABILITY_MATRIX.md` — requirement -> source -> code -> test.
