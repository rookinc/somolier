import pytest

from somolier import (
    B32KID,
    DecisionReceipt,
    Disposition,
    FixedMemoryStoragePort,
    Somolier,
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
    receipt = stream_swallowed(sr, wr, decision, host)
    assert receipt.b32kid == sr.b32kid
    assert host.read(receipt.allocation, "wine.b32k") == b"wine"


def test_spit_cannot_stream():
    wr = wiff(b"wine", source_name="wine.b32k")
    sr = swirl(b"wine", wr)
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
    assert host.artifact_names() == ()


def test_storage_output_verb_is_stream():
    wr, sr, tr, decision = _swallowed(b"stream-me", "stream.b32k")
    host = FixedMemoryStoragePort(location="memory://q/stream")
    receipt = stream_swallowed(sr, wr, decision, host)
    assert any(item.endswith("/stream.b32k") for item in receipt.artifacts)
