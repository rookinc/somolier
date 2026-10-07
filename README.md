# Somolier

Somolier is a deterministic, fail-closed ingestion and normalization codec.

Its canonical ritual is:

    INPUT
      -> WIFF
      -> SWIRL
      -> TASTE
      -> DECIDER
      -> SPIT | SWALLOW
                   |
                 HOST
                   |
                 STREAM
          \___________/
                |
          CALLER RECEIPT

## WIFF: the nose / lips

The stock valid-file-type list contains exactly:

    .b32k

A non-.b32k file is SPIT before identity issuance.

    WIFF FAIL -> no B32KID -> CALLER RECEIPT

## SWIRL: identity issuance

    WIFF PASS -> SWIRL(B32KID)

Every B32K packet carries this SWIRL-issued B32KID.

## Caller receipt

Every completed handling attempt returns a canonical receipt to the original
caller.

A WIFF rejection returns disposition/reason/flags but no B32KID.

A specimen that reaches the Decider returns its B32KID and canonical content ID
with the SPIT/SWALLOW result.

After SWALLOW and STREAM, the receipt also carries the host-returned artifact
locations.

This return receipt is not persistence: SPIT still allocates no host storage by
default.

## HOST and STREAM

    SPIT    -> no allocation, no STREAM -> CALLER RECEIPT
    SWALLOW -> host allocation -> STREAM -> CALLER RECEIPT

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
