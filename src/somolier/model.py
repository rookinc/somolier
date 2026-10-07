from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Tuple


class Stage(str, Enum):
    WIFF = "WIFF"
    SWIRL = "SWIRL"
    TASTE = "TASTE"
    DECIDER = "DECIDER"
    SPIT = "SPIT"
    SWALLOW = "SWALLOW"


class Disposition(str, Enum):
    SPIT = "SPIT"
    SWALLOW = "SWALLOW"


class DependencyState(str, Enum):
    READY = "READY"
    DISCONNECTED = "DISCONNECTED"
    FAILED = "FAILED"


@dataclass(frozen=True, order=True)
class B32KID:
    """Deterministic B32K identity minted by WIFF."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.startswith("b32kid:"):
            raise ValueError("B32KID must be a nonempty 'b32kid:' identifier")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class QuarantineAllocation:
    b32kid: B32KID
    location: str

    def __post_init__(self) -> None:
        if not self.location:
            raise ValueError("quarantine location/handle must be nonempty")


@dataclass(frozen=True)
class QuarantineReceipt:
    allocation: QuarantineAllocation
    source_digest: str
    artifacts: Tuple[str, ...]

    @property
    def b32kid(self) -> B32KID:
        return self.allocation.b32kid

    @property
    def location(self) -> str:
        return self.allocation.location


@dataclass(frozen=True)
class PortStatus:
    name: str
    state: DependencyState


@dataclass(frozen=True)
class ReadinessReceipt:
    required_ports: Tuple[str, ...]
    port_statuses: Tuple[PortStatus, ...]

    @property
    def ready(self) -> bool:
        status_by_name = {status.name: status.state for status in self.port_statuses}
        return all(
            status_by_name.get(name) is DependencyState.READY
            for name in self.required_ports
        )

    @property
    def unavailable_ports(self) -> Tuple[str, ...]:
        status_by_name = {status.name: status.state for status in self.port_statuses}
        return tuple(
            name
            for name in self.required_ports
            if status_by_name.get(name) is not DependencyState.READY
        )


@dataclass(frozen=True)
class WiffReceipt:
    b32kid: B32KID
    size_bytes: int
    surface_type: str
    flags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class TasteReceipt:
    backend: str
    canonical_id: str
    packet: Any
    source_size: int
    history: Mapping[str, Any]
    flags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class DecisionReceipt:
    disposition: Disposition
    authority: str | None
    passed_gates: Tuple[str, ...]
    failed_gates: Tuple[str, ...]
    reason: str
    unavailable_ports: Tuple[str, ...] = ()
