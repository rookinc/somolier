# Somolier

Somolier is a deterministic, fail-closed ingestion and normalization codec.

Its canonical ritual is:

    INPUT
      -> WIFF
      -> SWIRL
      -> TASTE
      -> DECIDE
      -> SPIT | SWALLOW
                   |
                 HOST
                   |
                 STREAM
          \___________/
                |
          CALLER RECEIPT (.b32k)

## WIFF: the nose

The stock valid-file-type list contains exactly:

    .b32k

The stock .b32k v1 raw-byte header is exactly:

    42 33 32 4B 56 30 30 31

ASCII:

    B32KV001

## Caller receipt format

Every completed handling attempt returns its receipt in .b32k format.

The wire form is:

    B32KV001 + canonical UTF-8 JSON body

The JSON body is deterministic: keys are sorted and compact separators are
used. It contains receipt kind, version, source name, stage, disposition,
reason, available identities, streamed artifact locations, and flags.

A WIFF rejection still produces a valid .b32k receipt, but its b32kid field is
null because the rejected input itself was never named.

Stored SWALLOW receipts are written as:

    receipt.b32k

No receipt.json file is part of the canonical output.

## HOST and STREAM

    SPIT    -> no allocation, no STREAM -> .b32k CALLER RECEIPT
    SWALLOW -> host allocation -> STREAM -> .b32k CALLER RECEIPT

STREAM is the canonical file-output verb.

## Development

    python -m pip install -e '.[dev]'
    pytest -q
    somolier-harness tests/fixtures

## Status

Early reference implementation. B32K is the sole shipped WIFF file type and
the default packet backend.

## License

License selection is intentionally pending project-owner approval.
