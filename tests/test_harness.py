from pathlib import Path

from somolier import (
    DependencyState,
    Disposition,
    RegisteredDecider,
    UnregisteredDecider,
)
from somolier.harness import run_case


FIXTURES = Path(__file__).parent / "fixtures"


def test_harness_b32k_round_trip():
    payload = b"hello b32k"
    result = run_case("hello.b32k", payload, source_name="hello.b32k")
    assert result.wiff.accepted
    assert result.taste is not None
    assert result.roundtrip_ok
    assert result.receipt_stable
    assert result.passed


def test_harness_rejects_non_b32k_before_id():
    result = run_case("hello.txt", b"hello", source_name="hello.txt")
    assert not result.wiff.accepted
    assert result.taste is None
    assert result.decision.disposition is Disposition.SPIT
    assert result.passed


def test_harness_registered_decider_only_swallows_all_pass():
    payload = b"hello"
    decider = RegisteredDecider(
        authority="generic-test-authority",
        required_gates=("integrity", "policy"),
        required_ports=("storage",),
    )
    swallow = run_case(
        "hello.b32k",
        payload,
        source_name="hello.b32k",
        decider=decider,
        gate_results={"integrity": True, "policy": True},
        port_results={"storage": DependencyState.READY},
    )
    disconnected = run_case(
        "hello.b32k",
        payload,
        source_name="hello.b32k",
        decider=decider,
        gate_results={"integrity": True, "policy": True},
        port_results={"storage": DependencyState.DISCONNECTED},
    )
    assert swallow.decision.disposition is Disposition.SWALLOW
    assert disconnected.decision.disposition is Disposition.SPIT
