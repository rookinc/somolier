from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .backend import PacketBackend
from .backends.b32k import B32KBackend
from .model import TasteReceipt, WiffReceipt


def wiff(payload: bytes, *, surface_type: str = "application/octet-stream") -> WiffReceipt:
    """Cheap pre-quarantine sniff. Never grants trust."""
    flags = () if payload else ("empty_payload",)
    return WiffReceipt(size_bytes=len(payload), surface_type=surface_type, flags=flags)


def swirl(payload: bytes) -> bytes:
    """Quarantine boundary placeholder.

    v0.1 returns an immutable byte copy. Production sealing belongs in a
    cryptographic adapter; this function deliberately does not invent crypto.
    """
    return bytes(payload)


@dataclass
class Somolier:
    backend: PacketBackend = B32KBackend()

    def taste(self, payload: bytes) -> TasteReceipt:
        packet = self.backend.encode(payload)
        if not self.backend.validate(packet):
            raise ValueError("packet backend rejected its own encoded packet")
        return TasteReceipt(
            backend=self.backend.name,
            canonical_id=self.backend.canonical_id(packet),
            packet=packet,
            source_size=len(payload),
            history={"source_bytes_preserved": True},
            flags=(),
        )

    def render(self, receipt: TasteReceipt) -> bytes:
        if receipt.backend != self.backend.name:
            raise ValueError("receipt backend does not match configured backend")
        return self.backend.decode(receipt.packet)
