from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .model import DecisionReceipt, Disposition, TasteReceipt


class UnregisteredDecider:
    """Fail-closed Decider: no authority means no appetite."""

    authority = None

    def decide(self, receipt: TasteReceipt) -> DecisionReceipt:
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

    def decide(
        self,
        receipt: TasteReceipt,
        *,
        gate_results: Mapping[str, bool],
    ) -> DecisionReceipt:
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
            reason="all required gates passed",
        )
