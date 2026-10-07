from pathlib import Path

from somolier import Disposition, RegisteredDecider, UnregisteredDecider
from somolier.harness import run_case


FIXTURES = Path(__file__).parent / "fixtures"


def test_harness_same_bytes_same_receipt_identity():
    payload = (FIXTURES / "clean" / "hello.txt").read_bytes()
    left = run_case("left", payload)
    right = run_case("right", payload)
    assert left.source_digest == right.source_digest
    assert left.taste.canonical_id == right.taste.canonical_id
    assert left.receipt_stable


def test_harness_round_trip_and_evidence_preservation():
    payload = (FIXTURES / "clean" / "sample.json").read_bytes()
    result = run_case("sample-json", payload, surface_type="application/json")
    assert result.roundtrip_ok
    assert result.evidence_preserved
    assert result.passed


def test_harness_unregistered_decider_spits():
    payload = (FIXTURES / "clean" / "hello.txt").read_bytes()
    result = run_case("fail-closed", payload, decider=UnregisteredDecider())
    assert result.decision.disposition is Disposition.SPIT


def test_harness_registered_decider_only_swallows_all_pass():
    payload = (FIXTURES / "clean" / "hello.txt").read_bytes()
    decider = RegisteredDecider(
        authority="generic-test-authority",
        required_gates=("integrity", "policy"),
    )
    spit = run_case(
        "one-gate-fails",
        payload,
        decider=decider,
        gate_results={"integrity": True, "policy": False},
    )
    swallow = run_case(
        "all-gates-pass",
        payload,
        decider=decider,
        gate_results={"integrity": True, "policy": True},
    )
    assert spit.decision.disposition is Disposition.SPIT
    assert swallow.decision.disposition is Disposition.SWALLOW


def test_harness_empty_fixture_is_flagged_but_preserved():
    result = run_case("empty", b"")
    assert "empty_payload" in result.wiff.flags
    assert result.evidence_preserved
    assert result.roundtrip_ok
