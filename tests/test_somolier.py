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


def test_every_wiff_mints_valid_b32kid():
    left = wiff(b"wine")
    right = wiff(b"wine")
    assert isinstance(left.b32kid, B32KID)
    assert str(left.b32kid).startswith("b32kid:sha256:")
    assert left.b32kid == right.b32kid


def test_b32k_round_trip_uses_wiff_id():
    payload = b"wine"
    wr = wiff(payload)
    som = Somolier(B32KBackend())
    receipt = som.taste(payload)
    assert receipt.backend == "b32k"
    assert receipt.packet.b32kid == wr.b32kid
    assert som.render(receipt) == payload


def test_b32k_requires_b32kid_at_backend_boundary():
    with pytest.raises(ValueError, match="require a B32KID"):
        B32KBackend().encode(b"wine")


def test_b32k_validation_accepts_valid_id():
    packet_id = wiff(b"abc").b32kid
    packet = B32KPacket(b32kid=packet_id, words=(1, 2, 3))
    assert B32KBackend().validate(packet)


def test_wiff_does_not_reject_empty_but_flags_it():
    receipt = wiff(b"")
    assert isinstance(receipt.b32kid, B32KID)
    assert "empty_payload" in receipt.flags


def test_swirl_placeholder_preserves_bytes():
    payload = b"abc"
    assert swirl(payload) == payload


def test_unregistered_decider_hates_everything():
    receipt = Somolier().taste(b"anything")
    decision = UnregisteredDecider().decide(receipt)
    assert decision.disposition is Disposition.SPIT


def test_registered_decider_requires_all_gates():
    receipt = Somolier().taste(b"wine")
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
    receipt = Somolier().taste(b"wine")
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


def test_missing_required_port_is_disconnected_and_spits():
    receipt = Somolier().taste(b"wine")
    decider = RegisteredDecider(
        authority="test-authority",
        required_gates=(),
        required_ports=("storage",),
    )
    decision = decider.decide(receipt, gate_results={}, port_results={})
    assert decision.disposition is Disposition.SPIT
    assert decision.unavailable_ports == ("storage",)
