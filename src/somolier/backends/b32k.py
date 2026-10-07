from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable, Tuple


@dataclass(frozen=True, order=True)
class B32KAddress:
    index: int
    plane: int
    r: int
    c: int

    @classmethod
    def from_index(cls, index: int) -> "B32KAddress":
        if not 0 <= index <= 32767:
            raise ValueError("B32K index must be in [0, 32767]")
        z = index - 1 if index > 0 else 0
        plane = z // 1024
        within = z % 1024
        return cls(index=index, plane=plane, r=within // 32, c=within % 32)


@dataclass(frozen=True)
class B32KPacket:
    words: Tuple[int, ...]


class B32KBackend:
    """Default Somolier packet backend.

    v0.1 uses one B32K word per source byte. This is intentionally a
    reversible packetization primitive, not yet a semantic language codec.
    """

    name = "b32k"

    def encode(self, payload: bytes) -> B32KPacket:
        return B32KPacket(tuple(payload))

    def decode(self, packet: B32KPacket) -> bytes:
        if not self.validate(packet):
            raise ValueError("invalid B32K packet")
        if any(word > 255 for word in packet.words):
            raise ValueError("v0.1 byte packet contains non-byte B32K words")
        return bytes(packet.words)

    def validate(self, packet: B32KPacket) -> bool:
        return isinstance(packet, B32KPacket) and all(
            isinstance(word, int) and 0 <= word <= 32767
            for word in packet.words
        )

    def canonical_id(self, packet: B32KPacket) -> str:
        if not self.validate(packet):
            raise ValueError("invalid B32K packet")
        raw = b"".join(word.to_bytes(2, "big") for word in packet.words)
        return "b32k:sha256:" + sha256(raw).hexdigest()

    def addresses(self, packet: B32KPacket) -> Tuple[B32KAddress, ...]:
        return tuple(B32KAddress.from_index(word) for word in packet.words)
