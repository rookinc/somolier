import pytest

from somolier import (
    B32KBackend,
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
        authority="test-hat",
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
