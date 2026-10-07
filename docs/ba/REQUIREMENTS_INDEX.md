# Somolier Requirements Index

Status: baseline requirements index
Notation:
- MUST = mandatory for the target implementation.
- SHOULD = expected unless a documented exception exists.
- MAY = optional/profile-dependent.
- Source classes: B32K = supplied B32K specification; SOM = explicit Somolier product decision; BP = implementation/security best practice.

This index deliberately separates B32K normative requirements from Somolier profile requirements.

## Governance and conformance

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| GOV-001 | The implementation MUST declare the exact B32K specification version/profile it conforms to. | MUST | BP / source ambiguity | versioned conformance profile |
| GOV-002 | B32K normative requirements MUST take precedence over conflicting prototype behavior or documentation. | MUST | SOM | traceability review |
| GOV-003 | Somolier extensions MUST be explicitly labeled as profile extensions and MUST NOT be represented as normative B32K fields. | MUST | SOM/BP | profile registry |
| GOV-004 | Requirements MUST be traceable to code and tests before a feature is called conformant. | MUST | BP | traceability matrix |

## Public service contract

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| CLI-001 | The canonical CLI call MUST be `somolier <filename>`. | MUST | SOM | CLI test |
| CLI-002 | One invocation MUST process one input object and produce one caller receipt. | MUST | SOM | end-to-end test |
| CLI-003 | The same input, configuration, dependency states, and deterministic profile inputs MUST produce the same deterministic outputs, excluding fields explicitly defined by a selected nondeterministic profile. | MUST | SOM/BP | replay test |
| CLI-004 | The CLI SHOULD support machine-readable output without changing processing semantics. | SHOULD | BP | CLI JSON/bytes test |

## WIFF requirements

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| WIF-001 | WIFF MUST be a recognition/sniff stage and MUST NOT execute payload content. | MUST | SOM/BP | code inspection + hostile fixture |
| WIF-002 | WIFF MUST use an explicit configured recognition registry. | MUST | SOM | registry test |
| WIF-003 | The stock Somolier profile MAY recognize only `.b32k`; this is a Somolier filename convention, not a B32K normative rule. | MAY | SOM | profile doc |
| WIF-004 | Any raw magic/header rule such as `B32KV001` MUST be labeled a Somolier profile convention unless supported by a normative B32K source. | MUST | BP | profile doc |
| WIF-005 | WIFF failure MUST terminate subject processing before SWIRL/TASTE and before subject identity issuance. | MUST | SOM | negative test |
| WIF-006 | WIFF failure MUST still yield a valid caller receipt object. | MUST | SOM | negative receipt test |

## SWIRL requirements

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| SWR-001 | SWIRL MUST accept only a WIFF-approved subject. | MUST | SOM | precondition test |
| SWR-002 | SWIRL MUST establish the isolation/sealing boundary. | MUST | SOM | adapter contract |
| SWR-003 | SWIRL MUST NOT issue the subject B32KID in the target architecture. | MUST | SOM | stage ownership test |
| SWR-004 | SWIRL SHOULD preserve exact input bytes unless the selected sealing profile explicitly defines a reversible protected representation. | SHOULD | SOM/BP | round-trip evidence test |
| SWR-005 | Production cryptographic protection MUST NOT be claimed until a specified cryptographic adapter and conformance tests exist. | MUST | BP | docs/security review |

## B32K canonicalization and encoding

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| B32-001 | Canonicalization MUST implement N(x) = CBOR_Canonical(UTF8_NFC(x)). | MUST | B32K §2.2/§3 | Appendix A vectors |
| B32-002 | Text fields MUST be Unicode NFC before canonical encoding. | MUST | B32K §2.2/§3 | normalization vectors |
| B32-003 | Canonical CBOR MUST use definite-length arrays/maps, shortest integer encodings, canonical key ordering, and reject duplicate keys. | MUST | B32K §3 | malformed/vector tests |
| B32-004 | Non-finite floats MUST be rejected where the B32K canonicalization algorithm requires rejection. | MUST | B32K §3 | negative tests |
| B32-005 | B32K symbol indices MUST be unsigned integers in [0,32767]. | MUST | B32K §2.1 | boundary tests |
| B32-006 | 15-bit indices MUST be bit-packed big-endian into a continuous stream with zero padding to the next octet boundary. | MUST | B32K §2.3/App A | reference vector |
| B32-007 | The implementation MUST reproduce normative Appendix A canonicalization vectors byte-for-byte. | MUST | B32K App A | conformance suite |

## Hash, handle, and identity

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| ID-001 | BLAKE3-256 MUST be used where B32K specifies the normative payload digest or Merkle aggregation hash. | MUST | B32K §7.4/§6 | digest vectors |
| ID-002 | SHA-256 MUST NOT be described as the normative B32K payload/handle hash. | MUST | B32K §7.4 | code/doc scan |
| ID-003 | HTTPQ `packet_id` MUST be treated as the specification's 128-bit UUIDv7 envelope identifier when HTTPQ is implemented. | MUST | B32K §5.1 | schema test |
| ID-004 | The B32K `handle` MUST follow the specification's BLAKE3 construction when implemented. | MUST | B32K §5.1/§6.1 | recomputation test |
| ID-005 | Somolier MAY define `B32KID` as a profile-level object label/genesis-receipt identifier, but its derivation MUST be explicit and MUST NOT collide semantically with `packet_id`, `handle`, or payload digest. | MUST if used | SOM | data dictionary + vectors |
| ID-006 | Subject B32KID issuance MUST occur only after TASTE PASS. | MUST | SOM | state-machine test |
| ID-007 | Every valid Somolier caller receipt MUST have its own receipt B32KID. | MUST | SOM | receipt validator |
| ID-008 | A receipt about a WIFF-rejected subject MUST distinguish receipt identity from absent subject identity. | MUST | SOM | negative receipt vector |

## TASTE requirements

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| TAS-001 | TASTE MUST operate only on a successfully SWIRLed subject. | MUST | SOM | precondition test |
| TAS-002 | TASTE MUST perform the configured structural/conformance checks needed to qualify the subject. | MUST | SOM | qualification suite |
| TAS-003 | TASTE PASS MUST issue/bind the subject's genesis identity according to the approved B32KID profile. | MUST | SOM | genesis vector |
| TAS-004 | TASTE FAIL MUST SPIT and MUST NOT issue a subject B32KID. | MUST | SOM | negative test |
| TAS-005 | TASTE MUST NOT perform SWALLOW-only persistence or external side effects. | MUST | SOM/BP | side-effect test |

## DECIDE requirements

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| DEC-001 | The canonical protocol verb/stage name MUST be DECIDE. | MUST | SOM | terminology scan |
| DEC-002 | DECIDE MUST return exactly one admission disposition: SPIT or SWALLOW. | MUST | SOM | decision tests |
| DEC-003 | Missing required dependency state MUST be treated as unavailable and fail closed. | MUST | SOM/BP | disconnected test |
| DEC-004 | Unknown/failed dependency state MUST NOT produce SWALLOW. | MUST | SOM/BP | fault test |
| DEC-005 | Missing or failed required gates MUST produce SPIT. | MUST | SOM | gate tests |
| DEC-006 | An unregistered authority context MUST produce SPIT. | MUST | SOM | default test |

## SPIT and SWALLOW requirements

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| DSP-001 | SPIT MUST NOT allocate host persistence or STREAM the subject by default. | MUST | SOM | storage spy test |
| DSP-002 | SPIT MUST return a valid caller receipt. | MUST | SOM | receipt test |
| DSW-001 | SWALLOW MUST be reachable only after DECIDE authorizes admission. | MUST | SOM | state-machine test |
| DSW-002 | Packet build and canonical identity computation owned by the final admitted representation MUST occur in SWALLOW, not TASTE, under the target architecture. | MUST | SOM | stage ownership test |
| DSW-003 | Host placement MUST occur only after SWALLOW. | MUST | SOM | storage spy test |
| DSW-004 | STREAM MUST be the canonical Somolier file-output verb. | MUST | SOM | interface test |

## Storage requirements

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| STO-001 | Somolier MUST ask the host/storage adapter for placement rather than hardcode a path. | MUST | SOM | adapter test |
| STO-002 | Storage location/handle MUST be opaque to Somolier core. | MUST | SOM/BP | interface review |
| STO-003 | Storage adapters MUST NOT alter protocol identity supplied by Somolier. | MUST | SOM | mismatch test |
| STO-004 | Core processing MUST remain testable with an in-memory storage adapter. | SHOULD | BP | unit tests |

## Receipt requirements

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| RCP-001 | Every completed Somolier invocation MUST return a caller receipt. | MUST | SOM | end-to-end tests |
| RCP-002 | Every valid caller receipt MUST have a receipt B32KID. | MUST | SOM | schema/validator test |
| RCP-003 | Receipt identity MUST be independently recomputable from its approved genesis/canonical form without circular self-hashing. | MUST | SOM/BP | recomputation test |
| RCP-004 | Receipt fields MUST distinguish the receipt's identity from the subject's identity. | MUST | SOM | schema test |
| RCP-005 | A Somolier caller receipt MUST NOT be labeled a normative B32K O-1 receipt unless it satisfies the O-1 schema exactly. | MUST | B32K App C / SOM | schema test |
| RCP-006 | If O-1 receipts are supported, verification MUST reproduce the Merkle root/inclusion proof deterministically and reject failures. | MUST if supported | B32K §6/App C | Appendix C tests |
| RCP-007 | Receipt/proof verification MUST be pure, deterministic, and side-effect-free. | MUST | B32K §6.6/§7.7 | isolated verification tests |
| RCP-008 | Human-readable JSON MAY be exposed, but canonical cryptographic authority MUST use the B32K canonical representation rather than JSON formatting. | MUST | B32K §3/App C | round-trip test |

## HTTPQ requirements (deferred unless transport profile enabled)

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| HTQ-001 | HTTPQ AAD MUST include the normative fields and canonical CBOR encoding when HTTPQ is implemented. | MUST if enabled | B32K §5.1 | AAD vector |
| HTQ-002 | HTTPQ build/verify MUST follow the specified AEAD/handle construction and verification sequence. | MUST if enabled | B32K §5.3 | protocol tests |
| HTQ-003 | Replay protection MUST enforce packet_id and seq_no rules when HTTPQ stateful receiving is implemented. | MUST if enabled | B32K §7.3 | replay tests |
| HTQ-004 | HTTPQ failures MUST map to the normative error registry where applicable. | MUST if enabled | B32K App G | error tests |

## Harness and quality requirements

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| TST-001 | The harness MUST test the public service entry point rather than manually reproducing pipeline internals. | MUST | BP | harness refactor |
| TST-002 | Normative B32K Appendix A vectors MUST be included as locked conformance tests. | MUST | B32K App A | CI |
| TST-003 | Negative tests MUST cover malformed CBOR, duplicate keys, bad indices, bad padding, altered receipts, identity mismatch, and dependency disconnects. | MUST | B32K/SOM/BP | CI |
| TST-004 | Test output SHOULD retain progress indicators suitable for Termux. | SHOULD | SOM | harness CLI |
| TST-005 | CI SHOULD test the minimum supported Python and at least one current Python release. | SHOULD | BP | workflow |
| TST-006 | No test fixture may be called B32K-conformant solely because it has a `.b32k` suffix or Somolier magic bytes. | MUST | BP | fixture audit |

## Security requirements

| ID | Requirement | Priority | Source | Acceptance evidence |
|---|---|---:|---|---|
| SEC-001 | Canonicalization MUST precede B32K hashing/signing operations. | MUST | B32K §7.7 | ordering tests |
| SEC-002 | Private keys MUST never appear in logs or telemetry. | MUST | B32K §7.7 | logging tests |
| SEC-003 | Cryptographic roles MUST use separated keys/labels where the relevant B32K crypto profile is implemented. | MUST if enabled | B32K §4/§7.1 | crypto tests |
| SEC-004 | Production cryptography SHOULD rely on maintained audited libraries rather than hand-rolled primitives. | SHOULD | BP | dependency review |
| SEC-005 | Somolier MUST fail closed on parse, canonicalization, integrity, identity, policy, and required-dependency failures. | MUST | B32K/SOM | fault suite |

## Open requirements decisions

These are intentionally not resolved by the prototype:

- OQ-001: Which exact B32K version is Somolier targeting? The supplied PDF contains conflicting 1.0.0 / 1.1.0 labels.
- OQ-002: Is `.b32k` an official B32K media/file convention or a Somolier profile convention?
- OQ-003: Is `B32KV001` retained as a Somolier framing magic, replaced, or removed?
- OQ-004: Exact B32KID derivation from genesis receipt / normative handle.
- OQ-005: Exact schema for the Somolier caller receipt distinct from B32K O-1.
- OQ-006: Whether Somolier v1 implements HTTPQ now or treats it as an optional transport profile.
- OQ-007: Whether ledger/O-1 support is core, plugin, or deferred.
