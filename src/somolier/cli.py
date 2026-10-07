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
    wr = wiff(payload, source_name=args.path.name)
    print(
        f"      accepted={wr.accepted} ext={wr.extension} "
        f"valid={list(wr.valid_file_types)} flags={list(wr.flags)}"
    )
    if not wr.accepted:
        print("[SPIT] rejected at WIFF; no B32KID issued")
        raise SystemExit(1)

    print("[2/4] SWIRL")
    sr = swirl(payload, wr)
    print(f"      b32kid={sr.b32kid}")

    print("[3/4] TASTE")
    som = Somolier()
    tr = som.taste(sr)
    print(f"      backend={tr.backend} content_id={tr.canonical_id}")

    print("[4/4] DECIDER")
    decision = UnregisteredDecider().decide(tr)
    print(f"      {decision.disposition.value}: {decision.reason}")
