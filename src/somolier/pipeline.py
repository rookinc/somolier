from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256

from .backend import PacketBackend
from .backends.b32k import B32KBackend
from .model import B32KID, QuarantineReceipt, TasteReceipt, WiffReceipt
from .storage import StoragePort


def _wiff_b32kid(payload: bytes) -> B32KID:
    """Mint a deterministic B32KID from the exact incoming bytes."""
    return B32KID("b32kid:sha256:" + sha256(payload).hexdigest())


def wiff(payload: bytes, *, surface_type: str = "application/octet-stream") -> WiffReceipt:
    """Cheap pre-quarantine sniff. Every WIFF mints a valid B32KID."""
    flags = () if payload else ("empty_payload",)
    return WiffReceipt(
        b32kid=_wiff_b32kid(payload),
        size_bytes=len(payload),
        surface_type=surface_type,
        flags=flags,
    )


def swirl(payload: bytes) -> bytes:
    """Quarantine boundary placeholder.

    v0.1 returns an immutable byte copy. Production sealing belongs in a
    cryptographic adapter; this function deliberately does not invent crypto.
    """
    return bytes(payload)


def quarantine(
    payload: bytes,
    storage: StoragePort,
    *,
    surface_type: str = "application/octet-stream",
) -> QuarantineReceipt:
    """WIFF identifies the object; the host chooses only quarantine placement."""

    source_digest = sha256(payload).hexdigest()
    wr = wiff(payload, surface_type=surface_type)
    metadata = {
        "b32kid": str(wr.b32kid),
        "source_digest": source_digest,
        "size_bytes": wr.size_bytes,
        "surface_type": wr.surface_type,
        "flags": list(wr.flags),
    }
    allocation = storage.allocate(
        b32kid=wr.b32kid,
        source_digest=source_digest,
        metadata=metadata,
    )
    if allocation.b32kid != wr.b32kid:
        raise ValueError("storage port changed the WIFF-minted B32KID")

    artifacts = []
    artifacts.append(storage.write(allocation, "original.bin", payload))
    artifacts.append(
        storage.write(
            allocation,
            "source.sha256",
            (source_digest + "\n").encode("ascii"),
        )
    )
    artifacts.append(
        storage.write(
            allocation,
            "wiff.json",
            (
                json.dumps(metadata, sort_keys=True, separators=(",", ":"))
                + "\n"
            ).encode("utf-8"),
        )
    )
    artifacts.append(storage.write(allocation, "sealed.bin", swirl(payload)))

    return QuarantineReceipt(
        allocation=allocation,
        source_digest=source_digest,
        artifacts=tuple(artifacts),
    )


@dataclass
class Somolier:
    backend: PacketBackend = B32KBackend()

    def taste(
        self,
        payload: bytes,
        *,
        b32kid: B32KID | None = None,
    ) -> TasteReceipt:
        packet_id = b32kid if b32kid is not None else wiff(payload).b32kid
        packet = self.backend.encode(payload, b32kid=packet_id)
        if not self.backend.validate(packet):
            raise ValueError("packet backend rejected its own encoded packet")
        history = {
            "source_bytes_preserved": True,
            "b32kid": str(packet_id),
        }
        return TasteReceipt(
            backend=self.backend.name,
            canonical_id=self.backend.canonical_id(packet),
            packet=packet,
            source_size=len(payload),
            history=history,
            flags=(),
        )

    def taste_quarantine(self, receipt: QuarantineReceipt, storage: StoragePort) -> TasteReceipt:
        """Taste the sealed quarantine artifact under its WIFF-minted B32KID."""
        payload = storage.read(receipt.allocation, "sealed.bin")
        return self.taste(payload, b32kid=receipt.b32kid)

    def render(self, receipt: TasteReceipt) -> bytes:
        if receipt.backend != self.backend.name:
            raise ValueError("receipt backend does not match configured backend")
        return self.backend.decode(receipt.packet)
