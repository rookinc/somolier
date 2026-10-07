import pytest

from somolier import (
    B32KID,
    B32K_V1_MAGIC,
    DecisionReceipt,
    Disposition,
    FixedMemoryStoragePort,
    Somolier,
    Stage,
    caller_receipt,
    encode_caller_receipt,
    stream_swallowed,
    swirl,
    wiff,
)


def _file(body=b"wine"):
    return B32K_V1_MAGIC + body


def _swallowed(body=b"wine", name="wine.b32k"):
    payload = _file(body)
    wr = wiff(payload, source_name=name)
    sr = swirl(payload, wr)
    tr = Somolier().taste(sr)
    decision = DecisionReceipt(
        disposition=Disposition.SWALLOW,
        authority="test",
        passed_gates=(),
        failed_gates=(),
        reason="test admission",
    )
    return payload, wr, sr, tr, decision


def test_b32kid_requires_explicit_prefix():
    with pytest.raises(ValueError):
        B32KID("not-a-b32kid")


def test_host_placement_happens_only_after_swallow():
    payload, wr, sr, tr, decision = _swallowed()
    host = FixedMemoryStoragePort(location="memory://accepted/wine")
    stream_receipt = stream_swallowed(sr, wr, decision, host)
    returned = caller_receipt(
        wr,
        decision,
        swirl_receipt=sr,
        taste_receipt=tr,
        stream_receipt=stream_receipt,
    )
    encoded = encode_caller_receipt(returned)
    assert returned.stage is Stage.SWALLOW
    assert returned.b32kid == sr.b32kid
    assert returned.streamed_artifacts == stream_receipt.artifacts
    assert encoded.startswith(B32K_V1_MAGIC)
    assert host.read(stream_receipt.allocation, "wine.b32k") == payload
    stored_receipt = host.read(stream_receipt.allocation, "receipt.b32k")
    assert stored_receipt.startswith(B32K_V1_MAGIC)


def test_spit_cannot_stream_but_still_gets_b32k_caller_receipt():
    payload = _file()
    wr = wiff(payload, source_name="wine.b32k")
    sr = swirl(payload, wr)
    tr = Somolier().taste(sr)
    host = FixedMemoryStoragePort(location="memory://rejected/wine")
    decision = DecisionReceipt(
        disposition=Disposition.SPIT,
        authority=None,
        passed_gates=(),
        failed_gates=("policy",),
        reason="no",
    )
    with pytest.raises(ValueError, match="SWALLOW"):
        stream_swallowed(sr, wr, decision, host)
    returned = caller_receipt(
        wr, decision, swirl_receipt=sr, taste_receipt=tr
    )
    encoded = encode_caller_receipt(returned)
    assert returned.disposition is Disposition.SPIT
    assert returned.streamed_artifacts == ()
    assert encoded.startswith(B32K_V1_MAGIC)
    assert host.artifact_names() == ()
