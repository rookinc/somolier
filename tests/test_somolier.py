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


def test_b32k_round_trip():
    payload = b"wine"
    packet_id = B32KID("b32kid:test-round-trip")
    som = Somolier(B32KBackend())
    receipt = som.taste(payload, b32kid=packet_id)
    assert receipt.backend == "b32k"
    assert receipt.packet.b32kid == packet_id
    assert som.render(receipt) == payload


def test_b32k_requires_b32kid():
    with pytest.raises(ValueError, match="require a B32KID"):
        B32KBackend().encode(b"wine")


def test_b32k_validation_rejects_packet_without_valid_id_shape():
    packet_id = B32KID("b32kid:test-validation")
    packet = B32KPacket(b32kid=packet_id, words=(1, 2, 3))
    assert B32KBackend().validate(packet)


def test_b32kid_does_not_change_content_canonical_id():
    backend = B32KBackend()
    left = backend.encode(b"same", b32kid=B32KID("b32kid:event-left"))
    right = backend.encode(b"same", b32kid=B32KID("b32kid:event-right"))
    assert left.b32kid != right.b32kid
    assert backend.canonical_id(left) == backend.canonical_id(right)


def test_wiff_does_not_reject_empty_but_flags_it():
    receipt = wiff(b"")
    assert "empty_payload" in receipt.flags


def test_swirl_placeholder_preserves_bytes():
    payload = b"abc"
    assert swirl(payload) == payload


def test_unregistered_decider_hates_everything():
    receipt = Somolier().taste(
        b"anything",
        b32kid=B32KID("b32kid:test-unregistered"),
    )
    decision = UnregisteredDecider().decide(receipt)
    assert decision.disposition is Disposition.SPIT


def test_registered_decider_requires_all_gates():
    receipt = Somolier().taste(
        b"wine",
        b32kid=B32KID("b32kid:test-gates"),
    )
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
    receipt = Somolier().taste(
        b"wine",
        b32kid=B32KID("b32kid:test-ports"),
    )
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
    receipt = Somolier().taste(
        b"wine",
        b32kid=B32KID("b32kid:test-missing-port"),
    )
    decider = RegisteredDecider(
        authority="test-authority",
        required_gates=(),
        required_ports=("storage",),
    )
    decision = decider.decide(receipt, gate_results={}, port_results={})
    assert decision.disposition is Disposition.SPIT
    assert decision.unavailable_ports == ("storage",)
