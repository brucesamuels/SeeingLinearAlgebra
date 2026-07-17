"""Cross-format verification for generated lesson documentation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from engine.lesson_inventory import LessonInventory
from engine.lesson_inventory_json import lesson_inventory_to_dict


@dataclass(frozen=True, slots=True)
class LessonDocumentationVerification:
    """Result of validating generated Markdown and JSON documentation."""

    is_valid: bool
    errors: tuple[str, ...]
    lesson_count: int
    total_beat_count: int


def verify_lesson_documentation(
    inventory: LessonInventory,
    *,
    markdown_text: str,
    json_text: str,
    markdown_heading: str = "Seeing Linear Algebra Lesson Inventory",
) -> LessonDocumentationVerification:
    """Verify freshness and semantic consistency of both inventory formats."""
    if not isinstance(inventory, LessonInventory):
        raise TypeError("inventory must be a LessonInventory")
    if not isinstance(markdown_text, str):
        raise TypeError("markdown_text must be a string")
    if not isinstance(json_text, str):
        raise TypeError("json_text must be a string")

    errors: list[str] = []

    expected_markdown = inventory.to_markdown(heading=markdown_heading)
    if markdown_text != expected_markdown:
        errors.append("Markdown lesson inventory is missing or out of date")

    expected_payload = lesson_inventory_to_dict(inventory)

    try:
        actual_payload = json.loads(json_text)
    except json.JSONDecodeError as exc:
        errors.append(f"JSON lesson inventory is invalid: {exc.msg}")
        actual_payload = None

    if actual_payload is not None:
        if actual_payload != expected_payload:
            errors.append("JSON lesson inventory is missing or out of date")

        semantic_errors = _compare_markdown_and_json(
            markdown_text,
            actual_payload,
            inventory,
        )
        errors.extend(semantic_errors)

    return LessonDocumentationVerification(
        is_valid=not errors,
        errors=tuple(errors),
        lesson_count=inventory.lesson_count,
        total_beat_count=inventory.total_beat_count,
    )


def verify_lesson_documentation_files(
    inventory: LessonInventory,
    *,
    markdown_path: Path,
    json_path: Path,
    markdown_heading: str = "Seeing Linear Algebra Lesson Inventory",
) -> LessonDocumentationVerification:
    """Read both generated files and verify them against the inventory."""
    if not isinstance(markdown_path, Path):
        raise TypeError("markdown_path must be a Path")
    if not isinstance(json_path, Path):
        raise TypeError("json_path must be a Path")

    errors: list[str] = []

    if markdown_path.is_file():
        markdown_text = markdown_path.read_text(encoding="utf-8")
    else:
        markdown_text = ""
        errors.append(f"Markdown inventory file not found: {markdown_path}")

    if json_path.is_file():
        json_text = json_path.read_text(encoding="utf-8")
    else:
        json_text = ""
        errors.append(f"JSON inventory file not found: {json_path}")

    result = verify_lesson_documentation(
        inventory,
        markdown_text=markdown_text,
        json_text=json_text,
        markdown_heading=markdown_heading,
    )

    return LessonDocumentationVerification(
        is_valid=not errors and result.is_valid,
        errors=tuple(errors) + result.errors,
        lesson_count=result.lesson_count,
        total_beat_count=result.total_beat_count,
    )


def _compare_markdown_and_json(
    markdown_text: str,
    payload: dict[str, Any],
    inventory: LessonInventory,
) -> tuple[str, ...]:
    """Perform simple semantic cross-checks between generated formats."""
    errors: list[str] = []

    if payload.get("lesson_count") != inventory.lesson_count:
        errors.append("Markdown and JSON lesson counts are inconsistent")

    if payload.get("total_beat_count") != inventory.total_beat_count:
        errors.append("Markdown and JSON beat counts are inconsistent")

    lessons = payload.get("lessons")
    if not isinstance(lessons, list):
        errors.append("JSON lessons field is not a list")
        return tuple(errors)

    for entry in inventory.entries:
        if entry.title not in markdown_text:
            errors.append(
                f"Markdown inventory does not contain title: {entry.title!r}"
            )
        if f"`{entry.key}`" not in markdown_text:
            errors.append(
                f"Markdown inventory does not contain key: {entry.key!r}"
            )

        matching = [
            lesson for lesson in lessons
            if isinstance(lesson, dict) and lesson.get("key") == entry.key
        ]
        if len(matching) != 1:
            errors.append(
                f"JSON inventory does not contain exactly one lesson: "
                f"{entry.key!r}"
            )
            continue

        json_lesson = matching[0]
        if json_lesson.get("title") != entry.title:
            errors.append(
                f"JSON title mismatch for lesson: {entry.key!r}"
            )

        beats = json_lesson.get("beats")
        if not isinstance(beats, list):
            errors.append(
                f"JSON beats field is not a list for lesson: {entry.key!r}"
            )
            continue

        json_names = tuple(
            beat.get("name") for beat in beats if isinstance(beat, dict)
        )
        json_roles = tuple(
            beat.get("role") for beat in beats if isinstance(beat, dict)
        )

        if json_names != entry.beat_names:
            errors.append(
                f"JSON beat-name order mismatch for lesson: {entry.key!r}"
            )
        if json_roles != entry.beat_roles:
            errors.append(
                f"JSON beat-role order mismatch for lesson: {entry.key!r}"
            )

        for name, role in zip(entry.beat_names, entry.beat_roles):
            if f"`{name}`" not in markdown_text:
                errors.append(
                    f"Markdown inventory omits beat name: {name!r}"
                )
            if f"`{role}`" not in markdown_text:
                errors.append(
                    f"Markdown inventory omits beat role: {role!r}"
                )

    return tuple(errors)
