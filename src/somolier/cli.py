from __future__ import annotations

import argparse
from pathlib import Path

from .decider import UnregisteredDecider
from .pipeline import Somolier, swirl, wiff


def main() -> None:
    parser = argparse.ArgumentParser(prog="somolier")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    payload = args.path.read_bytes()
    print("[1/4] WIFF")
    wr = wiff(payload)
    print(f"      size={wr.size_bytes} flags={list(wr.flags)}")

    print("[2/4] SWIRL")
    sealed = swirl(payload)

    print("[3/4] TASTE")
    som = Somolier()
    tr = som.taste(sealed)
    print(f"      backend={tr.backend} id={tr.canonical_id}")

    print("[4/4] DECIDER")
    decision = UnregisteredDecider().decide(tr)
    print(f"      {decision.disposition.value}: {decision.reason}")
