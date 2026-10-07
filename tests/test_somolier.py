import pytest

from somolier import (
    B32KBackend,
    B32KID,
    B32KPacket,
    DependencyState,
    Disposition,
    RegisteredDecider,
    Somolier,
    UnregisteredDecider,
    swirl,
    wiff,
)


def _approved(payload=b"wine", name="wine.b32k"):
    wr = wiff(payload, source_name=name)
    assert wr.accepted
    return swirl(payload, wr)


def test_stock_wiff_accepts_only_b32k():
    assert wiff(b"x", source_name="x.b32k").accepted
    rejected = wiff(b"x", source_name="x.json")
    assert not rejected.accepted
    assert "unsupported_file_type" in rejected.flags


def test_wiff_does_not_issue_b32kid():
    receipt = wiff(b"x", source_name="x.b32k")
    assert not hasattr(receipt, "b32kid")


def test_swirl_issues_b32kid_only_after_wiff_pass():
    sr = _approved()
    assert isinstance(sr.b32kid, B32KID)
    assert str(sr.b32kid).startswith("b32kid:sha256:")
    bad = wiff(b"x", source_name="x.txt")
    with pytest.raises(ValueError, match="passing WIFF"):
        swirl(b"x", bad)


def test_empty_b32k_fails_wiff():
    receipt = wiff(b"", source_name="empty.b32k")
    assert not receipt.accepted
    assert "empty_payload" in receipt.flags


def test_b32k_round_trip_uses_swirl_id():
    sr = _approved()
    som = Somolier(B32KBackend())
    receipt = som.taste(sr)
    assert receipt.packet.b32kid == sr.b32kid
    assert som.render(receipt) == b"wine"


def test_b32k_requires_b32kid_at_backend_boundary():
    with pytest.raises(ValueError, match="require a B32KID"):
        B32KBackend().encode(b"wine")


def test_b32k_validation_accepts_valid_id():
    sr = _approved(b"abc", "abc.b32k")
    packet = B32KPacket(b32kid=sr.b32kid, words=(1, 2, 3))
    assert B32KBackend().validate(packet)


def test_unregistered_decider_hates_everything():
    receipt = Somolier().taste(_approved(b"anything", "anything.b32k"))
    decision = UnregisteredDecider().decide(receipt)
    assert decision.disposition is Disposition.SPIT


def test_registered_decider_requires_all_gates():
    receipt = Somolier().taste(_approved())
    decider = RegisteredDecider(
        authority="test-authority",
        required_gates=("integrity", "policy"),
    )
    assert decider.decide(
        receipt,
        gate_results={"integrity": True, "policy": False},
    ).disposition is Disposition.SPIT
    assert decider.decide(
        receipt,
        gate_results={"integrity": True, "policy": True},
    ).disposition is Disposition.SWALLOW


def test_registered_decider_fails_closed_when_required_port_disconnected():
    receipt = Somolier().taste(_approved())
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
