from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .model import (
    DecisionReceipt,
    DependencyState,
    Disposition,
    TasteReceipt,
)
from .readiness import check_readiness


class UnregisteredDecider:
    """Fail-closed Decider: no authority means no appetite."""

    authority = None

    def decide(self, receipt: TasteReceipt, **_: object) -> DecisionReceipt:
        return DecisionReceipt(
            disposition=Disposition.SPIT,
            authority=None,
            passed_gates=(),
            failed_gates=("registered_authority",),
            reason="unregistered decider defaults to SPIT",
        )


@dataclass(frozen=True)
class RegisteredDecider:
    authority: str
    required_gates: tuple[str, ...]
    required_ports: tuple[str, ...] = ()

    def decide(
        self,
        receipt: TasteReceipt,
        *,
        gate_results: Mapping[str, bool],
        port_results: Mapping[str, DependencyState | str] | None = None,
    ) -> DecisionReceipt:
        readiness = check_readiness(
            self.required_ports,
            port_results or {},
        )
        if not readiness.ready:
            return DecisionReceipt(
                disposition=Disposition.SPIT,
                authority=self.authority,
                passed_gates=(),
                failed_gates=("required_ports_ready",),
                reason="required port unavailable; fail closed to SPIT",
                unavailable_ports=readiness.unavailable_ports,
            )

        passed = tuple(
            gate for gate in self.required_gates if gate_results.get(gate) is True
        )
        failed = tuple(
            gate for gate in self.required_gates if gate_results.get(gate) is not True
        )
        if failed:
            return DecisionReceipt(
                disposition=Disposition.SPIT,
                authority=self.authority,
                passed_gates=passed,
                failed_gates=failed,
                reason="one or more required gates did not pass",
            )
        return DecisionReceipt(
            disposition=Disposition.SWALLOW,
            authority=self.authority,
            passed_gates=passed,
            failed_gates=(),
            reason="all required ports are READY and all required gates passed",
        )
