# Somolier B32K Conformance Profile

Status: policy baseline for the rebuild
Profile name: Somolier-B32K
Target source: supplied B32K Open Specification, closing metadata "Version 1.1.0 (Stable Draft — October 2025)"

## 1. Authority

Somolier treats the supplied B32K specification as normative for all concepts it names as B32K.

Where the current prototype conflicts with the B32K specification, the prototype is non-conformant and MUST be changed.

Somolier-specific behavior is permitted only as an explicit profile extension and MUST NOT redefine an existing B32K normative field.

The supplied document has a version-label inconsistency: the cover says v1.0.0 while the closing metadata says Version 1.1.0 Stable Draft. Somolier therefore records the implementation target as B32K-1.1.0-stable-draft while preserving that upstream ambiguity.

## 2. Normative B32K rules adopted

Somolier MUST implement these exactly when it claims B32K conformance:

- Index is an unsigned 15-bit value in [0, 32767].
- Canonicalization is N(x) = CBOR_Canonical(UTF8_NFC(x)).
- Canonical CBOR uses definite lengths, shortest integer representations, canonical encoded-key order, and no duplicate map keys.
- Non-finite floats are rejected by the supplied canonicalization profile.
- 15-bit indices are packed big-endian into a continuous bitstream and zero-padded to the next octet boundary.
- BLAKE3-256 is the normative payload digest and Merkle aggregation hash.
- B32K handle construction follows the specification's BLAKE3 domain-separated formula.
- HTTPQ packet_id is UUIDv7 when HTTPQ is enabled.
- HTTPQ AAD, AEAD, replay, nonce, and error-code behavior follow the normative transport sections when enabled.
- O-1 receipts follow Appendix C exactly when Somolier emits or verifies an O-1 receipt.
- Receipt and Merkle-proof verification are deterministic and side-effect-free.

## 3. Somolier profile extensions

The following are Somolier profile concepts, not base B32K requirements:

### 3.1 CLI

    somolier <filename>

One invocation consumes one file and returns one Somolier caller receipt.

### 3.2 Stage vocabulary

    WIFF -> SWIRL -> TASTE -> DECIDE -> SPIT | SWALLOW

WIFF recognizes without executing.
SWIRL establishes an isolation/sealing boundary.
TASTE validates/qualifies and, on PASS, establishes subject genesis identity.
DECIDE performs fail-closed admission.
SPIT rejects admission and does not persist the subject by default.
SWALLOW owns final build/compute, placement request, and STREAM.
STREAM is the Somolier file-output verb.

### 3.3 Filename and framing convention

The suffix .b32k and provisional outer magic B32KV001 are Somolier profile conventions unless a normative B32K source later defines them.

The canonical B32K body remains N(x), not filename suffix, magic bytes, JSON formatting, or host storage representation.

### 3.4 B32KID

B32KID is a Somolier profile label derived from a normative B32K handle, not SHA-256.

Conceptually:

    payload_digest = BLAKE3-256(N(x))
    handle = BLAKE3-256("B32K-HANDLE" || version || lane_id || payload_digest)
    B32KID = profile_label(handle, version, lane_id)

Its serialization MUST be versioned and MUST remain semantically distinct from HTTPQ packet_id and raw payload digest.

### 3.5 Caller receipt

A Somolier caller receipt is NOT an O-1 receipt unless it satisfies Appendix C exactly.

Every valid Somolier caller receipt MUST have its own receipt B32KID.

    receipt_b32kid  required
    subject_b32kid  optional

For a WIFF-rejected subject, receipt_b32kid exists while subject_b32kid does not.

Receipt identity MUST avoid circular self-hashing:
1. construct the genesis receipt body without receipt_b32kid;
2. canonicalize using B32K N(x);
3. derive the normative B32K handle in the configured profile context;
4. serialize the handle as receipt_b32kid;
5. attach it to the transmitted receipt;
6. validation recomputes and requires equality.

Human-readable JSON MAY be exposed as a view, but canonical CBOR bytes are authoritative.

## 4. Stage ownership

| Stage | Owns | MUST NOT own |
|---|---|---|
| WIFF | recognition/profile sniff | execution, identity issuance, persistence |
| SWIRL | isolation/sealing | subject identity issuance, admission, persistence |
| TASTE | structural/conformance validation; subject genesis identity on PASS | final admitted build, host persistence |
| DECIDE | SPIT/SWALLOW decision from explicit policy/dependency inputs | implicit policy inference |
| SPIT | caller receipt | subject persistence by default |
| SWALLOW | final build/compute; placement request; STREAM | bypass of DECIDE |

## 5. Transport and ledger scope

For the first conformance rebuild:
- canonicalization, 15-bit packing, BLAKE3 digest/handle, identity separation, caller receipts, and offline verification are CORE;
- HTTPQ is OPTIONAL/DEFERRED until explicitly enabled;
- O-1 ledger receipts are OPTIONAL/DEFERRED until explicitly enabled;
- PPL remains experimental/non-normative and is outside the core acceptance bar.

## 6. Conformance claim levels

- PROFILE-DRAFT: design documented; implementation may be incomplete.
- CORE-CONFORMANT: all enabled B32K core requirements and locked reference vectors pass.
- HTTPQ-CONFORMANT: CORE-CONFORMANT plus enabled HTTPQ requirements pass.
- O1-CONFORMANT: CORE-CONFORMANT plus enabled O-1 requirements pass.

Until the rebuild passes its conformance suite, the repository MUST describe itself as a prototype/profile draft.
