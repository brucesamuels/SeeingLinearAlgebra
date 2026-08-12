#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

OLD = "Properties of the Determinant"
NEW = "Methods of Computation"


def main() -> int:
    repo_root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    scene = repo_root / "scenes/determinant_elimination_presentation.py"

    if not scene.exists():
        print(f"Missing CP134 scene: {scene}", file=sys.stderr)
        return 2

    source = scene.read_text(encoding="utf-8")
    if OLD in source:
        scene.write_text(source.replace(OLD, NEW), encoding="utf-8")

    verified = scene.read_text(encoding="utf-8")
    if NEW not in verified or OLD in verified:
        print("CP134 banner patch verification failed.", file=sys.stderr)
        return 3

    for test in sorted((repo_root / "tests").glob("test*determinant*elimination*.py")):
        text = test.read_text(encoding="utf-8")
        if OLD in text:
            test.write_text(text.replace(OLD, NEW), encoding="utf-8")

    print(f"Verified CP134 banner: {NEW}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
