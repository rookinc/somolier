from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Tuple

from ..model import B32KID


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
    b32kid: B32KID
    words: Tuple[int, ...]


class B32KBackend:
    """Default Somolier packet backend.

    B32K requires every packet to carry a host-issued B32KID. The identifier is
    event identity; canonical_id remains content identity over the packet words.
    """

    name = "b32k"
    requires_b32kid = True

    def encode(
        self,
        payload: bytes,
        *,
        b32kid: B32KID | None = None,
    ) -> B32KPacket:
        if b32kid is None:
            raise ValueError("B32K packets require a B32KID")
        return B32KPacket(b32kid=b32kid, words=tuple(payload))

    def decode(self, packet: B32KPacket) -> bytes:
        if not self.validate(packet):
            raise ValueError("invalid B32K packet")
        if any(word > 255 for word in packet.words):
            raise ValueError("v0.1 byte packet contains non-byte B32K words")
        return bytes(packet.words)

    def validate(self, packet: B32KPacket) -> bool:
        return (
            isinstance(packet, B32KPacket)
            and isinstance(packet.b32kid, B32KID)
            and all(
                isinstance(word, int) and 0 <= word <= 32767
                for word in packet.words
            )
        )

    def canonical_id(self, packet: B32KPacket) -> str:
        if not self.validate(packet):
            raise ValueError("invalid B32K packet")
        raw = b"".join(word.to_bytes(2, "big") for word in packet.words)
        return "b32k:sha256:" + sha256(raw).hexdigest()

    def addresses(self, packet: B32KPacket) -> Tuple[B32KAddress, ...]:
        return tuple(B32KAddress.from_index(word) for word in packet.words)
