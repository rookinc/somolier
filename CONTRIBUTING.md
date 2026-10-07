# Contributing

Somolier is intentionally small. Changes should preserve these invariants:

1. The packet backend remains pluggable.
2. B32K remains the bundled default backend for the v0.x reference implementation unless a versioned protocol change says otherwise.
3. Somolier does not grant admission.
4. Unregistered Deciders default to SPIT.
5. SWALLOW is earned only through explicit gates.
6. Surface presentation must not silently become canonical identity without an explicit mapping or backend rule.
