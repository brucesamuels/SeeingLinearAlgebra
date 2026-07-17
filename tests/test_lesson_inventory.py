from __future__ import annotations

import pytest

from engine.lesson_catalog import LessonCatalog, LessonDescriptor
from engine.lesson_inventory import LessonInventory, LessonInventoryEntry
from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


def sample_catalog() -> LessonCatalog:
    return LessonCatalog(
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


def test_inventory_entry_is_derived_from_descriptor() -> None:
    descriptor = sample_catalog()[0]

    entry = LessonInventoryEntry.from_descriptor(descriptor)

    assert entry.key == "sample"
    assert entry.title == "Sample Lesson"
    assert entry.beat_names == ("frame", "question")
    assert entry.beat_roles == ("orient", "predict")


def test_inventory_is_derived_in_catalog_order() -> None:
    inventory = LessonInventory.from_catalog(sample_catalog())

    assert inventory.lesson_count == 1
    assert inventory.total_beat_count == 2
    assert tuple(entry.key for entry in inventory.entries) == ("sample",)


def test_inventory_rejects_invalid_catalog() -> None:
    with pytest.raises(TypeError, match="LessonCatalog"):
        LessonInventory.from_catalog(object())  # type: ignore[arg-type]


def test_markdown_output_is_deterministic() -> None:
    inventory = LessonInventory.from_catalog(sample_catalog())

    assert inventory.to_markdown() == (
        "# Lesson Inventory\n"
        "\n"
        "Lessons: 1\n"
        "Total beats: 2\n"
        "\n"
        "## Sample Lesson\n"
        "\n"
        "Key: `sample`\n"
        "\n"
        "| # | Beat | Role |\n"
        "|---:|---|---|\n"
        "| 1 | `frame` | `orient` |\n"
        "| 2 | `question` | `predict` |\n"
    )


@pytest.mark.parametrize("heading", ["", " ", "\n"])
def test_markdown_rejects_empty_heading(heading: str) -> None:
    inventory = LessonInventory.from_catalog(sample_catalog())

    with pytest.raises(ValueError, match="nonempty"):
        inventory.to_markdown(heading=heading)


def test_inventory_has_no_execution_api() -> None:
    inventory = LessonInventory.from_catalog(sample_catalog())

    assert not hasattr(inventory, "run")
    assert not hasattr(inventory, "render")
    assert not hasattr(inventory, "execute")
