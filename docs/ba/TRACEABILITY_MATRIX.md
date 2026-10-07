# Somolier Traceability Matrix

Status: initial policy trace; implementation mappings are migration targets.

| Requirement area | B32K source | Somolier policy | Target implementation | Target tests |
|---|---|---|---|---|
| canonicalization N(x) | §2.2, §3 | CONFORMANCE_PROFILE | canonical.py | Appendix A vectors |
| 15-bit index range | §2.1 | REQUIREMENTS_INDEX | b32k/index.py | boundary tests |
| 15-bit packing | §2.3, App A.3 | REQUIREMENTS_INDEX | b32k/packing.py | pack/unpack vectors |
| BLAKE3 payload digest | §6.1, §7.4 | DATA_DICTIONARY | b32k/digest.py | digest vector |
| B32K handle | §5.1, §6.1 | DATA_DICTIONARY | b32k/handle.py | handle recomputation |
| packet_id UUIDv7 | §5.1 | DATA_DICTIONARY | deferred httpq/ | HTTPQ schema tests |
| O-1 receipt | §6.4, App C | CONFORMANCE_PROFILE | deferred o1/ | Appendix C tests |
| deterministic receipt verification | §6.6, §7.7 | CONFORMANCE_PROFILE | verify.py | side-effect-free tests |
| WIFF | Somolier profile | STATE_MACHINE | wiff.py | recognition negatives |
| SWIRL | Somolier profile | STATE_MACHINE | swirl.py | isolation tests |
| TASTE | Somolier profile | STATE_MACHINE | taste.py | genesis tests |
| DECIDE | Somolier profile | STATE_MACHINE | decide.py | fail-closed tests |
| SPIT/SWALLOW | Somolier profile | STATE_MACHINE | service.py | branch tests |
| STREAM | Somolier profile | HOST_STORAGE_PORT | storage.py | storage spy tests |
| caller receipt | Somolier profile using B32K primitives | DATA_DICTIONARY | receipt.py | recompute tests |
| public CLI | Somolier profile | REQUIREMENTS_INDEX | cli.py | end-to-end CLI |

A row becomes implemented only when code exists, tests cover it, normative vectors pass where applicable, and documentation no longer contradicts it.
