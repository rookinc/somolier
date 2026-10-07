import json

import pytest

from somolier import (
    B32KBackend,
    B32KID,
    B32KPacket,
    B32K_V1_MAGIC,
    DependencyState,
    Disposition,
    RegisteredDecider,
    Somolier,
    Stage,
    UnregisteredDecider,
    caller_receipt,
    encode_caller_receipt,
    swirl,
    wiff,
)


def _file(body=b"wine"):
    return B32K_V1_MAGIC + body


def _approved(body=b"wine", name="wine.b32k"):
    payload = _file(body)
    wr = wiff(payload, source_name=name)
    assert wr.accepted
    return payload, wr, swirl(payload, wr)


def test_stock_wiff_accepts_only_b32k_with_v1_raw_header():
    assert B32K_V1_MAGIC == bytes.fromhex("42 33 32 4B 56 30 30 31")
    assert wiff(_file(b"x"), source_name="x.b32k").accepted
    wrong_type = wiff(_file(b"x"), source_name="x.json")
    assert not wrong_type.accepted
    assert "unsupported_file_type" in wrong_type.flags
    bad_header = wiff(b"NOTB32K!" + b"x", source_name="x.b32k")
    assert not bad_header.accepted
    assert "invalid_file_header" in bad_header.flags


def test_wiff_rejection_returns_b32k_caller_receipt_without_id():
    wr = wiff(b"garbage", source_name="x.b32k")
    receipt = caller_receipt(wr)
    encoded = encode_caller_receipt(receipt)
    assert receipt.stage is Stage.WIFF
    assert receipt.disposition is Disposition.SPIT
    assert receipt.b32kid is None
    assert encoded.startswith(B32K_V1_MAGIC)
    body = json.loads(encoded[len(B32K_V1_MAGIC):].decode("utf-8"))
    assert body["kind"] == "somolier.caller_receipt"
    assert body["b32kid"] is None
    assert body["disposition"] == "SPIT"


def test_swirl_issues_b32kid_only_after_wiff_pass():
    payload, wr, sr = _approved()
    assert isinstance(sr.b32kid, B32KID)
    assert str(sr.b32kid).startswith("b32kid:sha256:")
    bad = wiff(b"x", source_name="x.txt")
    with pytest.raises(ValueError, match="passing WIFF"):
        swirl(b"x", bad)


def test_empty_b32k_fails_wiff():
    receipt = wiff(b"", source_name="empty.b32k")
    assert not receipt.accepted
    assert "empty_payload" in receipt.flags
    assert "invalid_file_header" in receipt.flags


def test_b32k_round_trip_uses_swirl_id():
    payload, wr, sr = _approved()
    som = Somolier(B32KBackend())
    receipt = som.taste(sr)
    assert receipt.packet.b32kid == sr.b32kid
    assert som.render(receipt) == payload


def test_decide_spit_returns_named_b32k_caller_receipt():
    payload, wr, sr = _approved()
    tr = Somolier().taste(sr)
    decision = UnregisteredDecider().decide(tr)
    receipt = caller_receipt(wr, decision, swirl_receipt=sr, taste_receipt=tr)
    encoded = encode_caller_receipt(receipt)
    assert receipt.stage is Stage.SPIT
    assert receipt.disposition is Disposition.SPIT
    assert receipt.b32kid == sr.b32kid
    assert receipt.canonical_id == tr.canonical_id
    assert encoded.startswith(B32K_V1_MAGIC)


def test_b32k_requires_b32kid_at_backend_boundary():
    with pytest.raises(ValueError, match="require a B32KID"):
        B32KBackend().encode(_file())


def test_b32k_validation_accepts_valid_id():
    payload, wr, sr = _approved(b"abc", "abc.b32k")
    packet = B32KPacket(b32kid=sr.b32kid, words=(1, 2, 3))
    assert B32KBackend().validate(packet)


def test_registered_decider_fails_closed_when_required_port_disconnected():
    payload, wr, sr = _approved()
    receipt = Somolier().taste(sr)
    decider = RegisteredDecider(
        authority="test-authority",
        required_gates=("integrity",),
        required_ports=("storage", "dictionary"),
    )
    decision = decider.decide(
        receipt,
        gate_results={"integrity": True},
        port_results={
            "storage": DependencyState.READY,
            "dictionary": DependencyState.DISCONNECTED,
        },
    )
    assert decision.disposition is Disposition.SPIT
    assert decision.unavailable_ports == ("dictionary",)
