from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class PacketBackend(Protocol):
    name: str

    def encode(self, payload: bytes) -> Any:
        ...

    def decode(self, packet: Any) -> bytes:
        ...

    def canonical_id(self, packet: Any) -> str:
        ...

    def validate(self, packet: Any) -> bool:
        ...
