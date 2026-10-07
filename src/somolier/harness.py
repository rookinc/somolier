from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping, Protocol

from .decider import RegisteredDecider, UnregisteredDecider
from .model import DecisionReceipt, DependencyState, Disposition, TasteReceipt, WiffReceipt
from .pipeline import Somolier, swirl, wiff


class HarnessDecider(Protocol):
    def decide(self, receipt: TasteReceipt, **kwargs: Any) -> DecisionReceipt:
        ...


@dataclass(frozen=True)
class HarnessResult:
    case: str
    source_digest: str
    wiff: WiffReceipt
    taste: TasteReceipt | None
    decision: DecisionReceipt
    roundtrip_ok: bool
    evidence_preserved: bool
    receipt_stable: bool

    @property
    def passed(self) -> bool:
        if not self.wiff.accepted:
            return self.decision.disposition is Disposition.SPIT and self.taste is None
        return self.roundtrip_ok and self.evidence_preserved and self.receipt_stable

    def to_dict(self) -> dict[str, Any]:
        taste = None
        if self.taste is not None:
            taste = {
                "backend": self.taste.backend,
                "canonical_id": self.taste.canonical_id,
                "b32kid": str(self.taste.packet.b32kid),
                "source_size": self.taste.source_size,
                "history": dict(self.taste.history),
                "flags": list(self.taste.flags),
            }
        return {
            "case": self.case,
            "source_digest": self.source_digest,
            "wiff": {
                "accepted": self.wiff.accepted,
                "source_name": self.wiff.source_name,
                "extension": self.wiff.extension,
                "valid_file_types": list(self.wiff.valid_file_types),
                "size_bytes": self.wiff.size_bytes,
                "surface_type": self.wiff.surface_type,
                "flags": list(self.wiff.flags),
            },
            "taste": taste,
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


def run_case(
    case: str,
    payload: bytes,
    *,
    source_name: str | None = None,
    surface_type: str = "application/octet-stream",
    somolier: Somolier | None = None,
    decider: HarnessDecider | None = None,
    gate_results: Mapping[str, bool] | None = None,
    port_results: Mapping[str, DependencyState | str] | None = None,
) -> HarnessResult:
    som = somolier or Somolier()
    source_digest = sha256(payload).hexdigest()
    name = source_name or Path(case).name
    wr = wiff(payload, source_name=name, surface_type=surface_type)

    if not wr.accepted:
        return HarnessResult(
            case=case,
            source_digest=source_digest,
            wiff=wr,
            taste=None,
            decision=DecisionReceipt(
                disposition=Disposition.SPIT,
                authority=None,
                passed_gates=(),
                failed_gates=("wiff",),
                reason="WIFF rejected input before B32KID issuance",
            ),
            roundtrip_ok=False,
            evidence_preserved=True,
            receipt_stable=True,
        )

    sr1 = swirl(payload, wr)
    sr2 = swirl(payload, wr)
    tr1 = som.taste(sr1)
    tr2 = som.taste(sr2)

    roundtrip_ok = som.render(tr1) == payload
    evidence_preserved = sr1.sealed == payload
    receipt_stable = (
        sr1.b32kid == sr2.b32kid
        and tr1.canonical_id == tr2.canonical_id
        and tr1.packet.b32kid == sr1.b32kid
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
