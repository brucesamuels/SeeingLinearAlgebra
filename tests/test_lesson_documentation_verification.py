from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.lesson_catalog import LessonCatalog, LessonDescriptor
from engine.lesson_documentation_verification import (
    verify_lesson_documentation,
    verify_lesson_documentation_files,
)
from engine.lesson_inventory import LessonInventory
from engine.lesson_inventory_json import lesson_inventory_to_json
from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


def sample_inventory() -> LessonInventory:
    catalog = LessonCatalog(
        (
            LessonDescriptor(
                key="sample",
                title="Sample Lesson",
                sequence=LessonSequence(
                    (
                        LessonBeat("frame", LessonBeatRole.ORIENT),
                        LessonBeat("question", LessonBeatRole.PREDICT),
                    )
                ),
            ),
        )
    )
    return LessonInventory.from_catalog(catalog)


def valid_markdown(inventory: LessonInventory) -> str:
    return inventory.to_markdown(
        heading="Seeing Linear Algebra Lesson Inventory"
    )


def test_verification_accepts_current_consistent_formats() -> None:
    inventory = sample_inventory()

    result = verify_lesson_documentation(
        inventory,
        markdown_text=valid_markdown(inventory),
        json_text=lesson_inventory_to_json(inventory),
    )

    assert result.is_valid
    assert result.errors == ()
    assert result.lesson_count == 1
    assert result.total_beat_count == 2


def test_verification_detects_stale_markdown() -> None:
    inventory = sample_inventory()

    result = verify_lesson_documentation(
        inventory,
        markdown_text="# stale\n",
        json_text=lesson_inventory_to_json(inventory),
    )

    assert not result.is_valid
    assert any("Markdown" in error for error in result.errors)


def test_verification_detects_stale_json() -> None:
    inventory = sample_inventory()
    payload = json.loads(lesson_inventory_to_json(inventory))
    payload["total_beat_count"] = 99

    result = verify_lesson_documentation(
        inventory,
        markdown_text=valid_markdown(inventory),
        json_text=json.dumps(payload),
    )

    assert not result.is_valid
    assert any("JSON" in error for error in result.errors)


def test_verification_detects_invalid_json() -> None:
    inventory = sample_inventory()

    result = verify_lesson_documentation(
        inventory,
        markdown_text=valid_markdown(inventory),
        json_text="{not-json}\n",
    )

    assert not result.is_valid
    assert any("invalid" in error for error in result.errors)


def test_file_verification_reports_missing_files(tmp_path: Path) -> None:
    result = verify_lesson_documentation_files(
        sample_inventory(),
        markdown_path=tmp_path / "missing.md",
        json_path=tmp_path / "missing.json",
    )

    assert not result.is_valid
    assert any("not found" in error for error in result.errors)


def test_file_verification_accepts_current_files(tmp_path: Path) -> None:
    inventory = sample_inventory()
    markdown_path = tmp_path / "inventory.md"
    json_path = tmp_path / "inventory.json"

    markdown_path.write_text(valid_markdown(inventory), encoding="utf-8")
    json_path.write_text(
        lesson_inventory_to_json(inventory),
        encoding="utf-8",
    )

    result = verify_lesson_documentation_files(
        inventory,
        markdown_path=markdown_path,
        json_path=json_path,
    )

    assert result.is_valid


def test_verification_rejects_invalid_argument_types() -> None:
    inventory = sample_inventory()

    with pytest.raises(TypeError, match="LessonInventory"):
        verify_lesson_documentation(
            object(),  # type: ignore[arg-type]
            markdown_text="",
            json_text="",
        )

    with pytest.raises(TypeError, match="markdown_text"):
        verify_lesson_documentation(
            inventory,
            markdown_text=object(),  # type: ignore[arg-type]
            json_text="",
        )
