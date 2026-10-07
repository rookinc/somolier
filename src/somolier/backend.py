from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from .model import B32KID


@runtime_checkable
class PacketBackend(Protocol):
    name: str
    requires_b32kid: bool

    def encode(
        self,
        payload: bytes,
        *,
        b32kid: B32KID | None = None,
    ) -> Any:
        ...

    def decode(self, packet: Any) -> bytes:
        ...

    def canonical_id(self, packet: Any) -> str:
        ...

    def validate(self, packet: Any) -> bool:
        ...
