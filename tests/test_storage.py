import pytest

from somolier import (
    B32KID,
    DecisionReceipt,
    Disposition,
    FixedMemoryStoragePort,
    Somolier,
    Stage,
    caller_receipt,
    stream_swallowed,
    swirl,
    wiff,
)


def _swallowed(payload=b"wine", name="wine.b32k"):
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
    return wr, sr, tr, decision


def test_b32kid_requires_explicit_prefix():
    with pytest.raises(ValueError):
        B32KID("not-a-b32kid")


def test_host_placement_happens_only_after_swallow():
    wr, sr, tr, decision = _swallowed()
    host = FixedMemoryStoragePort(location="memory://accepted/wine")
    stream_receipt = stream_swallowed(sr, wr, decision, host)
    returned = caller_receipt(
        wr,
        decision,
        swirl_receipt=sr,
        taste_receipt=tr,
        stream_receipt=stream_receipt,
    )
    assert returned.stage is Stage.SWALLOW
    assert returned.b32kid == sr.b32kid
    assert returned.streamed_artifacts == stream_receipt.artifacts
    assert host.read(stream_receipt.allocation, "wine.b32k") == b"wine"


def test_spit_cannot_stream_but_still_gets_caller_receipt():
    wr = wiff(b"wine", source_name="wine.b32k")
    sr = swirl(b"wine", wr)
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
    assert returned.disposition is Disposition.SPIT
    assert returned.streamed_artifacts == ()
    assert host.artifact_names() == ()
