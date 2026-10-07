from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterable, Mapping

from .backend import PacketBackend
from .backends.b32k import B32KBackend
from .model import (
    B32KID,
    CallerReceipt,
    DecisionReceipt,
    Disposition,
    QuarantineReceipt,
    Stage,
    SwirlReceipt,
    TasteReceipt,
    WiffReceipt,
)
from .storage import StoragePort


B32K_V1_MAGIC = b"B32KV001"
DEFAULT_VALID_FILE_TYPES = (".b32k",)
DEFAULT_FILE_HEADERS: Mapping[str, bytes] = {
    ".b32k": B32K_V1_MAGIC,
}


def _normalize_types(valid_file_types: Iterable[str]) -> tuple[str, ...]:
    normalized = []
    for value in valid_file_types:
        item = value.strip().lower()
        if not item.startswith("."):
            item = "." + item
        if item not in normalized:
            normalized.append(item)
    if not normalized:
        raise ValueError("WIFF requires at least one valid file type")
    return tuple(normalized)


def wiff(
    payload: bytes,
    *,
    source_name: str,
    surface_type: str = "application/octet-stream",
    valid_file_types: Iterable[str] = DEFAULT_VALID_FILE_TYPES,
    file_headers: Mapping[str, bytes] = DEFAULT_FILE_HEADERS,
) -> WiffReceipt:
    """The nose gate. WIFF does not issue IDs.

    A recognized file type must also match its configured raw-byte header.
    The stock distribution knows only .b32k with the B32KV001 header.
    """

    allowed = _normalize_types(valid_file_types)
    extension = Path(source_name).suffix.lower()
    flags = []

    if not payload:
        flags.append("empty_payload")

    if extension not in allowed:
        flags.append("unsupported_file_type")
    else:
        expected_header = file_headers.get(extension)
        if expected_header is None:
            flags.append("missing_header_rule")
        elif not payload.startswith(expected_header):
            flags.append("invalid_file_header")

    accepted = not flags
    return WiffReceipt(
        accepted=accepted,
        source_name=source_name,
        extension=extension,
        size_bytes=len(payload),
        surface_type=surface_type,
        valid_file_types=allowed,
        flags=tuple(flags),
    )


def swirl(payload: bytes, wiff_receipt: WiffReceipt) -> SwirlReceipt:
    """Seal a WIFF-approved specimen and issue its B32KID."""

    if not wiff_receipt.accepted:
        raise ValueError("SWIRL requires a passing WIFF receipt")
    digest = sha256(payload).hexdigest()
    return SwirlReceipt(
        b32kid=B32KID("b32kid:sha256:" + digest),
        sealed=bytes(payload),
        source_digest=digest,
    )


def caller_receipt(
    wiff_receipt: WiffReceipt,
    decision: DecisionReceipt | None = None,
    *,
    swirl_receipt: SwirlReceipt | None = None,
    taste_receipt: TasteReceipt | None = None,
    stream_receipt: QuarantineReceipt | None = None,
) -> CallerReceipt:
    """Build the canonical response for the original caller."""

    if not wiff_receipt.accepted:
        return CallerReceipt(
            source_name=wiff_receipt.source_name,
            stage=Stage.WIFF,
            disposition=Disposition.SPIT,
            reason="WIFF rejected input before B32KID issuance",
            flags=wiff_receipt.flags,
        )

    if swirl_receipt is None:
        raise ValueError("passing WIFF caller receipt requires SWIRL receipt")
    if decision is None:
        raise ValueError("post-WIFF caller receipt requires decision")

    stage = Stage.SWALLOW if decision.disposition is Disposition.SWALLOW else Stage.SPIT
    return CallerReceipt(
        source_name=wiff_receipt.source_name,
        stage=stage,
        disposition=decision.disposition,
        reason=decision.reason,
        b32kid=swirl_receipt.b32kid,
        canonical_id=taste_receipt.canonical_id if taste_receipt is not None else None,
        streamed_artifacts=(
            stream_receipt.artifacts if stream_receipt is not None else ()
        ),
        flags=wiff_receipt.flags,
    )


def stream_swallowed(
    swirl_receipt: SwirlReceipt,
    wiff_receipt: WiffReceipt,
    decision: DecisionReceipt,
    storage: StoragePort,
) -> QuarantineReceipt:
    """Persist only an admitted specimen."""

    if decision.disposition is not Disposition.SWALLOW:
        raise ValueError("STREAM requires SWALLOW")
    metadata = {
        "b32kid": str(swirl_receipt.b32kid),
        "source_digest": swirl_receipt.source_digest,
        "source_name": wiff_receipt.source_name,
        "extension": wiff_receipt.extension,
        "size_bytes": wiff_receipt.size_bytes,
        "surface_type": wiff_receipt.surface_type,
        "flags": list(wiff_receipt.flags),
    }
    allocation = storage.allocate(
        b32kid=swirl_receipt.b32kid,
        source_digest=swirl_receipt.source_digest,
        metadata=metadata,
    )
    if allocation.b32kid != swirl_receipt.b32kid:
        raise ValueError("storage port changed the SWIRL-issued B32KID")

    artifacts = (
        storage.stream(allocation, wiff_receipt.source_name, swirl_receipt.sealed),
        storage.stream(
            allocation,
            "receipt.json",
            (
                json.dumps(metadata, sort_keys=True, separators=(",", ":"))
                + "\n"
            ).encode("utf-8"),
        ),
    )
    return QuarantineReceipt(
        allocation=allocation,
        source_digest=swirl_receipt.source_digest,
        artifacts=artifacts,
    )


@dataclass
class Somolier:
    backend: PacketBackend = B32KBackend()

    def taste(self, receipt: SwirlReceipt) -> TasteReceipt:
        packet = self.backend.encode(receipt.sealed, b32kid=receipt.b32kid)
        if not self.backend.validate(packet):
            raise ValueError("packet backend rejected its own encoded packet")
        return TasteReceipt(
            backend=self.backend.name,
            canonical_id=self.backend.canonical_id(packet),
            packet=packet,
            source_size=len(receipt.sealed),
            history={
                "source_bytes_preserved": True,
                "b32kid": str(receipt.b32kid),
            },
            flags=(),
        )

    def render(self, receipt: TasteReceipt) -> bytes:
        if receipt.backend != self.backend.name:
            raise ValueError("receipt backend does not match configured backend")
        return self.backend.decode(receipt.packet)
