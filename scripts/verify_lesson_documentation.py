#!/usr/bin/env python3
"""Verify all generated lesson documentation in one command."""

from __future__ import annotations

from pathlib import Path

from engine.lesson_documentation_verification import (
    verify_lesson_documentation_files,
)
from engine.lesson_inventory import LessonInventory
from engine.seeing_linear_algebra_lesson_catalog import (
    SEEING_LINEAR_ALGEBRA_LESSON_CATALOG,
)


def main() -> int:
    inventory = LessonInventory.from_catalog(
        SEEING_LINEAR_ALGEBRA_LESSON_CATALOG
    )
    result = verify_lesson_documentation_files(
        inventory,
        markdown_path=Path("LESSON_INVENTORY.md"),
        json_path=Path("LESSON_INVENTORY.json"),
    )

    if not result.is_valid:
        details = "\n".join(f"- {error}" for error in result.errors)
        raise SystemExit(
            "lesson documentation verification failed:\n" + details
        )

    print(
        "Lesson documentation verified: "
        f"{result.lesson_count} lessons, "
        f"{result.total_beat_count} beats"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
