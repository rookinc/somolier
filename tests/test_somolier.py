import pytest

from somolier import (
    B32KBackend,
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
    som = Somolier(B32KBackend())
    receipt = som.taste(payload)
    assert receipt.backend == "b32k"
    assert som.render(receipt) == payload


def test_wiff_does_not_reject_empty_but_flags_it():
    receipt = wiff(b"")
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
