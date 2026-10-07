from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Mapping, Protocol

from .decider import RegisteredDecider, UnregisteredDecider
from .model import (
    B32KID,
    DecisionReceipt,
    DependencyState,
    TasteReceipt,
    WiffReceipt,
)
from .pipeline import Somolier, swirl, wiff


class HarnessDecider(Protocol):
    def decide(self, receipt: TasteReceipt, **kwargs: Any) -> DecisionReceipt:
        ...


@dataclass(frozen=True)
class HarnessResult:
    case: str
    source_digest: str
    wiff: WiffReceipt
    taste: TasteReceipt
    decision: DecisionReceipt
    roundtrip_ok: bool
    evidence_preserved: bool
    receipt_stable: bool

    @property
    def passed(self) -> bool:
        return self.roundtrip_ok and self.evidence_preserved and self.receipt_stable

    def to_dict(self) -> dict[str, Any]:
        return {
            "case": self.case,
            "source_digest": self.source_digest,
            "wiff": asdict(self.wiff),
            "taste": {
                "backend": self.taste.backend,
                "canonical_id": self.taste.canonical_id,
                "b32kid": str(self.taste.packet.b32kid),
                "source_size": self.taste.source_size,
                "history": dict(self.taste.history),
                "flags": list(self.taste.flags),
            },
            "decision": {
                "disposition": self.decision.disposition.value,
                "authority": self.decision.authority,
                "passed_gates": list(self.decision.passed_gates),
                "failed_gates": list(self.decision.failed_gates),
                "unavailable_ports": list(self.decision.unavailable_ports),
                "reason": self.decision.reason,
            },
            "roundtrip_ok": self.roundtrip_ok,
            "evidence_preserved": self.evidence_preserved,
            "receipt_stable": self.receipt_stable,
            "passed": self.passed,
        }


def _harness_b32kid(case: str, source_digest: str) -> B32KID:
    # Deterministic test-only event identity. Production identities are host-issued.
    case_digest = sha256(case.encode("utf-8")).hexdigest()[:16]
    return B32KID(f"b32kid:harness:{case_digest}:{source_digest[:16]}")


def run_case(
    case: str,
    payload: bytes,
    *,
    surface_type: str = "application/octet-stream",
    somolier: Somolier | None = None,
    decider: HarnessDecider | None = None,
    gate_results: Mapping[str, bool] | None = None,
    port_results: Mapping[str, DependencyState | str] | None = None,
    b32kid: B32KID | None = None,
) -> HarnessResult:
    """Run one deterministic Somolier harness case."""

    som = somolier or Somolier()
    source_digest = sha256(payload).hexdigest()
    packet_id = b32kid or _harness_b32kid(case, source_digest)

    wr = wiff(payload, surface_type=surface_type)
    sealed = swirl(payload)
    tr1 = som.taste(sealed, b32kid=packet_id)
    tr2 = som.taste(sealed, b32kid=packet_id)

    roundtrip_ok = som.render(tr1) == payload
    evidence_preserved = sealed == payload
    receipt_stable = (
        tr1.canonical_id == tr2.canonical_id
        and tr1.backend == tr2.backend
        and tr1.source_size == tr2.source_size
        and tr1.packet.b32kid == tr2.packet.b32kid
    )

    chosen = decider or UnregisteredDecider()
    if isinstance(chosen, RegisteredDecider):
        decision = chosen.decide(
            tr1,
            gate_results=dict(gate_results or {}),
            port_results=dict(port_results or {}),
        )
    else:
        decision = chosen.decide(tr1)

    return HarnessResult(
        case=case,
        source_digest=source_digest,
        wiff=wr,
        taste=tr1,
        decision=decision,
        roundtrip_ok=roundtrip_ok,
        evidence_preserved=evidence_preserved,
        receipt_stable=receipt_stable,
    )
