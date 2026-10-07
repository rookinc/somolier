from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Protocol, Tuple, runtime_checkable

from .model import B32KID, QuarantineAllocation


@runtime_checkable
class StoragePort(Protocol):
    """Host-provided quarantine placement interface.

    WIFF already minted the B32KID. The host chooses only the location/handle.

    File output uses the verb STREAM: Somolier streams named artifacts to the
    host-owned storage port.
    """

    name: str

    def allocate(
        self,
        *,
        b32kid: B32KID,
        source_digest: str,
        metadata: Mapping[str, Any],
    ) -> QuarantineAllocation:
        ...

    def stream(
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
    """Deterministic one-event storage adapter for tests/examples."""

    location: str
    name: str = "memory"
    _b32kid: B32KID | None = None
    _source_digest: str | None = None
    _artifacts: Dict[str, bytes] = field(default_factory=dict)

    def allocate(
        self,
        *,
        b32kid: B32KID,
        source_digest: str,
        metadata: Mapping[str, Any],
    ) -> QuarantineAllocation:
        if self._source_digest is None:
            self._source_digest = source_digest
            self._b32kid = b32kid
        elif self._source_digest != source_digest or self._b32kid != b32kid:
            raise ValueError(
                "FixedMemoryStoragePort is bound to one ingestion identity"
            )
        return QuarantineAllocation(
            b32kid=b32kid,
            location=self.location,
        )

    def stream(
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
        if allocation.b32kid != self._b32kid or allocation.location != self.location:
            raise ValueError("allocation does not belong to this storage port")
