from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256

from .backend import PacketBackend
from .backends.b32k import B32KBackend
from .model import B32KID, QuarantineReceipt, TasteReceipt, WiffReceipt
from .storage import StoragePort


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


def quarantine(
    payload: bytes,
    storage: StoragePort,
    *,
    surface_type: str = "application/octet-stream",
) -> QuarantineReceipt:
    """Ask the host where to quarantine one ingestion event.

    Somolier computes content identity, but the host supplies event identity
    (B32KID) and storage location through StoragePort.allocate().
    """

    source_digest = sha256(payload).hexdigest()
    wr = wiff(payload, surface_type=surface_type)
    metadata = {
        "source_digest": source_digest,
        "size_bytes": wr.size_bytes,
        "surface_type": wr.surface_type,
        "flags": list(wr.flags),
    }
    allocation = storage.allocate(
        source_digest=source_digest,
        metadata=metadata,
    )

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
        packet = self.backend.encode(payload, b32kid=b32kid)
        if not self.backend.validate(packet):
            raise ValueError("packet backend rejected its own encoded packet")
        history = {"source_bytes_preserved": True}
        if b32kid is not None:
            history["b32kid"] = str(b32kid)
        return TasteReceipt(
            backend=self.backend.name,
            canonical_id=self.backend.canonical_id(packet),
            packet=packet,
            source_size=len(payload),
            history=history,
            flags=(),
        )

    def taste_quarantine(self, receipt: QuarantineReceipt, storage: StoragePort) -> TasteReceipt:
        """Taste the host-sealed quarantine artifact using its event B32KID."""

        payload = storage.read(receipt.allocation, "sealed.bin")
        return self.taste(payload, b32kid=receipt.b32kid)

    def render(self, receipt: TasteReceipt) -> bytes:
        if receipt.backend != self.backend.name:
            raise ValueError("receipt backend does not match configured backend")
        return self.backend.decode(receipt.packet)
