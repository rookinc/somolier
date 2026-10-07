from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Tuple


class Stage(str, Enum):
    WIFF = "WIFF"
    SWIRL = "SWIRL"
    TASTE = "TASTE"
    DECIDER = "DECIDER"
    SPIT = "SPIT"
    SWALLOW = "SWALLOW"


class Disposition(str, Enum):
    SPIT = "SPIT"
    SWALLOW = "SWALLOW"


@dataclass(frozen=True)
class WiffReceipt:
    size_bytes: int
    surface_type: str
    flags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class TasteReceipt:
    backend: str
    canonical_id: str
    packet: Any
    source_size: int
    history: Mapping[str, Any]
    flags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class DecisionReceipt:
    disposition: Disposition
    authority: str | None
    passed_gates: Tuple[str, ...]
    failed_gates: Tuple[str, ...]
    reason: str
