from __future__ import annotations

import json

import pytest

from engine.lesson_catalog import LessonCatalog, LessonDescriptor
from engine.lesson_inventory import LessonInventory, LessonInventoryEntry
from engine.lesson_inventory_json import (
    lesson_inventory_to_dict,
    lesson_inventory_to_json,
    validate_lesson_inventory,
)
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


def test_validation_reports_valid_inventory() -> None:
    result = validate_lesson_inventory(sample_inventory())

    assert result.is_valid
    assert result.errors == ()
    assert result.lesson_count == 1
    assert result.total_beat_count == 2


def test_validation_detects_mismatched_beat_arrays() -> None:
    inventory = LessonInventory(
        (
            LessonInventoryEntry(
                key="broken",
                title="Broken",
                beat_names=("frame",),
                beat_roles=(),
            ),
        )
    )

    result = validate_lesson_inventory(inventory)

    assert not result.is_valid
    assert "mismatched beat names and roles" in result.errors[0]


def test_dict_export_has_stable_schema() -> None:
    payload = lesson_inventory_to_dict(sample_inventory())

    assert payload["schema_version"] == 1
    assert payload["lesson_count"] == 1
    assert payload["total_beat_count"] == 2
    assert payload["is_valid"] is True
    assert payload["errors"] == []
    assert payload["lessons"][0]["key"] == "sample"
    assert payload["lessons"][0]["beats"] == [
        {"index": 1, "name": "frame", "role": "orient"},
        {"index": 2, "name": "question", "role": "predict"},
    ]


def test_json_export_is_deterministic_and_parseable() -> None:
    text = lesson_inventory_to_json(sample_inventory())
    payload = json.loads(text)

    assert text.endswith("\n")
    assert payload["schema_version"] == 1
    assert payload["lessons"][0]["title"] == "Sample Lesson"


def test_json_export_rejects_negative_indent() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        lesson_inventory_to_json(sample_inventory(), indent=-1)


def test_validation_and_export_reject_invalid_types() -> None:
    with pytest.raises(TypeError, match="LessonInventory"):
        validate_lesson_inventory(object())  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="LessonInventory"):
        lesson_inventory_to_dict(object())  # type: ignore[arg-type]
