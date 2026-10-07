# Somolier / B32K Data Dictionary

Status: policy baseline

| Term | Authority | Meaning | Algorithm / format |
|---|---|---|---|
| Index | B32K | authoritative symbol identity | uint15, 0..32767 |
| N(x) | B32K | canonical structured-object bytes | UTF-8 NFC then canonical CBOR |
| payload_digest | B32K | digest of canonical payload | BLAKE3-256(N(x)) |
| handle | B32K | digest binding payload to version/lane context | BLAKE3-256("B32K-HANDLE" || version || lane_id || payload_digest) |
| packet_id | B32K HTTPQ | envelope correlation/replay identifier | UUIDv7, 128 bit |
| seq_no | B32K HTTPQ | per-lane ordering value | uint64 |
| O-1 receipt | B32K | ledger inclusion proof object | Appendix C schema |
| B32KID | Somolier profile | object label derived from a B32K handle/genesis context | profile-versioned handle serialization |
| receipt_b32kid | Somolier profile | B32KID of the caller receipt itself | required on every valid caller receipt |
| subject_b32kid | Somolier profile | B32KID of the subject discussed by a receipt | optional; absent before subject earns identity |
| storage_location | host | opaque placement handle returned after SWALLOW | host-defined |
| CallerReceipt | Somolier profile | deterministic result of one invocation | authoritative bytes use N(x) |

## Identity invariants

1. packet_id and B32KID are distinct.
2. payload_digest and handle are distinct.
3. B32KID MUST be handle-derived and MUST NOT be SHA-256 presented as B32K identity.
4. Every valid caller receipt has receipt_b32kid.
5. subject_b32kid exists only after the subject passes TASTE.
6. A WIFF rejection may therefore have receipt_b32kid present and subject_b32kid absent.
7. Host storage location never defines object identity.

## Receipt genesis rule

Let g be the receipt genesis body with no receipt_b32kid field.

    c = N(g)
    d = BLAKE3-256(c)
    h = BLAKE3-256("B32K-HANDLE" || version || lane_id || d)
    receipt_b32kid = profile_label(h, version, lane_id)

Verification recomputes from g and compares.
