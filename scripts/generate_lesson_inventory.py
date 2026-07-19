#!/usr/bin/env python3
"""Generate a Markdown lesson inventory from the canonical catalog."""

from __future__ import annotations

import argparse
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_REPO_ROOT))

from engine.lesson_inventory import LessonInventory
from engine.seeing_linear_algebra_lesson_catalog import (
    SEEING_LINEAR_ALGEBRA_LESSON_CATALOG,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the Seeing Linear Algebra lesson inventory."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("LESSON_INVENTORY.md"),
        help="output Markdown path",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the existing output is current without rewriting it",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inventory = LessonInventory.from_catalog(
        SEEING_LINEAR_ALGEBRA_LESSON_CATALOG
    )
    expected = inventory.to_markdown(
        heading="Seeing Linear Algebra Lesson Inventory"
    )

    output = args.output

    if args.check:
        if not output.is_file():
            raise SystemExit(f"inventory file not found: {output}")
        actual = output.read_text(encoding="utf-8")
        if actual != expected:
            raise SystemExit(
                f"inventory is out of date: {output}\n"
                "Run scripts/generate_lesson_inventory.py"
            )
        print(f"Inventory is current: {output}")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8")
    print(f"Wrote lesson inventory: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
