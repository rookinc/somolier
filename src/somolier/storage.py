from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Protocol, Tuple, runtime_checkable

from .model import B32KID, QuarantineAllocation


@runtime_checkable
class StoragePort(Protocol):
    """Host-provided quarantine storage interface.

    Somolier never chooses a filesystem path. The host returns an opaque
    B32KID and location/handle for this ingestion event.
    """

    name: str

    def allocate(
        self,
        *,
        source_digest: str,
        metadata: Mapping[str, Any],
    ) -> QuarantineAllocation:
        ...

    def write(
        self,
        allocation: QuarantineAllocation,
        artifact_name: str,
        payload: bytes,
    ) -> str:
        ...

    def read(
        self,
        allocation: QuarantineAllocation,
        artifact_name: str,
    ) -> bytes:
        ...


@dataclass
class FixedMemoryStoragePort:
    """Deterministic one-event storage adapter for tests/examples.

    The host supplies both the B32KID and location. No random or ambient event
    identity is generated inside Somolier.
    """

    b32kid: B32KID
    location: str
    name: str = "memory"
    _source_digest: str | None = None
    _artifacts: Dict[str, bytes] = field(default_factory=dict)

    def allocate(
        self,
        *,
        source_digest: str,
        metadata: Mapping[str, Any],
    ) -> QuarantineAllocation:
        if self._source_digest is None:
            self._source_digest = source_digest
        elif self._source_digest != source_digest:
            raise ValueError(
                "FixedMemoryStoragePort is bound to one ingestion event"
            )
        return QuarantineAllocation(
            b32kid=self.b32kid,
            location=self.location,
        )

    def write(
        self,
        allocation: QuarantineAllocation,
        artifact_name: str,
        payload: bytes,
    ) -> str:
        self._require_allocation(allocation)
        if not artifact_name or "/" in artifact_name or "\\" in artifact_name:
            raise ValueError("artifact_name must be a single safe path segment")
        self._artifacts[artifact_name] = bytes(payload)
        return f"{self.location.rstrip('/')}/{artifact_name}"

    def read(
        self,
        allocation: QuarantineAllocation,
        artifact_name: str,
    ) -> bytes:
        self._require_allocation(allocation)
        return self._artifacts[artifact_name]

    def artifact_names(self) -> Tuple[str, ...]:
        return tuple(sorted(self._artifacts))

    def _require_allocation(self, allocation: QuarantineAllocation) -> None:
        if allocation.b32kid != self.b32kid or allocation.location != self.location:
            raise ValueError("allocation does not belong to this storage port")
