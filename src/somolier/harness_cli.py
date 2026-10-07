from __future__ import annotations

import argparse
import json
from pathlib import Path

from .harness import run_case


def _iter_files(path: Path):
    if path.is_file():
        yield path
        return
    for candidate in sorted(p for p in path.rglob("*") if p.is_file()):
        yield candidate


def main() -> None:
    parser = argparse.ArgumentParser(prog="somolier-harness")
    parser.add_argument("path", type=Path, help="fixture file or directory")
    parser.add_argument("--json", action="store_true", help="emit JSON per case")
    args = parser.parse_args()

    files = list(_iter_files(args.path))
    total = len(files)
    if total == 0:
        raise SystemExit("no fixture files found")

    failed = 0
    for i, path in enumerate(files, start=1):
        result = run_case(str(path), path.read_bytes())
        if args.json:
            print(json.dumps(result.to_dict(), sort_keys=True))
        else:
            mark = "PASS" if result.passed else "FAIL"
            print(
                f"[{i}/{total}] {mark} {path} "
                f"decision={result.decision.disposition.value} "
                f"id={result.taste.canonical_id}"
            )
        failed += 0 if result.passed else 1

    if failed:
        raise SystemExit(f"{failed}/{total} harness cases failed")
    if not args.json:
        print(f"All {total} Somolier harness cases passed.")


if __name__ == "__main__":
    main()
