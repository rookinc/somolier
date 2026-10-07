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

## WIFF: the nose / lips

WIFF has an explicit valid-file-type list.

The stock Somolier distribution ships with exactly:

    .b32k

and nothing else.

A non-.b32k file fails WIFF under the stock configuration. It is SPIT before
identity issuance.

    WIFF FAIL -> SPIT -> no B32KID

The list is configuration, so deployments may explicitly add types without
changing the deterministic algorithm.

## SWIRL: identity issuance

Passing the lips earns entry to SWIRL. SWIRL seals the specimen and issues its
B32KID.

    WIFF PASS -> SWIRL(B32KID)

The reference B32KID is deterministic:

    B32KID = "b32kid:sha256:" + SHA256(input_bytes)

Every B32K packet must carry this SWIRL-issued B32KID.

## TASTE and DECIDER

TASTE normalizes/packetizes the named specimen. DECIDER returns SPIT or
SWALLOW and remains fail-closed.

## HOST and STREAM

Host placement occurs only after SWALLOW by default.

    SPIT    -> no allocation, no file persistence
    SWALLOW -> host allocation -> STREAM

STREAM is the canonical file-output verb.

## Development

    python -m pip install -e '.[dev]'
    pytest -q
    somolier-harness tests/fixtures

The harness treats rejected non-.b32k fixtures as successful fail-closed test
cases: they must receive no B32KID and no TASTE receipt.

## Status

Early reference implementation. B32K is the sole shipped WIFF file type and
the default packet backend. Production cryptographic SWIRL adapters remain
separate work.

## License

License selection is intentionally pending project-owner approval.
