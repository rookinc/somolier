from __future__ import annotations

from typing import Mapping, Sequence

from .model import DependencyState, PortStatus, ReadinessReceipt


def check_readiness(
    required_ports: Sequence[str],
    port_results: Mapping[str, DependencyState | str],
) -> ReadinessReceipt:
    """Build a deterministic fail-closed readiness receipt.

    Missing ports are treated as DISCONNECTED. Unknown string values are
    treated as FAILED instead of raising into a permissive path.
    """

    statuses = []
    for name in sorted(set(required_ports)):
        raw = port_results.get(name, DependencyState.DISCONNECTED)
        if isinstance(raw, DependencyState):
            state = raw
        else:
            try:
                state = DependencyState(str(raw))
            except ValueError:
                state = DependencyState.FAILED
        statuses.append(PortStatus(name=name, state=state))

    return ReadinessReceipt(
        required_ports=tuple(sorted(set(required_ports))),
        port_statuses=tuple(statuses),
    )
