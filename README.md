# Somolier

Somolier is a fail-closed ingestion and normalization codec with a pluggable packet backend and an external Decider port.

Its canonical ritual is:

```text
WIFF -> SWIRL -> TASTE -> DECIDER -> SPIT | SWALLOW
```

Somolier **describes and normalizes**. The Decider **admits or rejects**.

## Default security law

- An unregistered Decider returns `SPIT` for every input.
- `SWALLOW` is reachable only when every required gate passes.
- `WIFF` never grants trust.
- `SWIRL` never grants admission.
- `TASTE` never decides truth.
- `SPIT` does not mean delete.
- `SWALLOW` does not mean unconditional trust.

## Native packet backend

Somolier v0.1 ships with **B32K** configured as the default packet backend.

```text
surface presentation -> Somolier -> B32K packet -> Decider
```

The backend remains pluggable so downstream projects can replace B32K without changing the Somolier protocol.

## King's Taster model

The Somolier persona is the tasting surface. The security office underneath is the King's Taster: nothing is consumed until it has earned `SWALLOW`.

## Status

Early reference implementation. The current B32K backend provides a reversible byte-to-B32K packetization path. Higher-level semantic dictionaries and production cryptographic SWIRL adapters remain separate work.

## Development

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## License

License selection is intentionally pending project-owner approval.
