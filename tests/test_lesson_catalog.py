from __future__ import annotations

import dataclasses
import importlib
import sys

import pytest

from engine.lesson_catalog import LessonCatalog, LessonDescriptor
from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


def sample_sequence(name: str) -> LessonSequence:
    return LessonSequence(
        (LessonBeat(name, LessonBeatRole.ORIENT),)
    )


def sample_catalog() -> LessonCatalog:
    return LessonCatalog(
        (
            LessonDescriptor(
                key="first",
                title="First Lesson",
                sequence=sample_sequence("first_beat"),
            ),
            LessonDescriptor(
                key="second",
                title="Second Lesson",
                sequence=sample_sequence("second_beat"),
            ),
        )
    )


def test_descriptor_is_frozen_and_normalizes_text() -> None:
    sequence = sample_sequence("frame")
    descriptor = LessonDescriptor("  key  ", "  A Lesson  ", sequence)

    assert descriptor.key == "key"
    assert descriptor.title == "A Lesson"
    assert descriptor.sequence is sequence

    with pytest.raises(dataclasses.FrozenInstanceError):
        descriptor.title = "Changed"  # type: ignore[misc]


@pytest.mark.parametrize("field,value", [
    ("key", ""),
    ("key", "  "),
    ("title", ""),
    ("title", "\n"),
])
def test_descriptor_rejects_empty_text(field: str, value: str) -> None:
    kwargs = {
        "key": "lesson",
        "title": "Lesson",
        "sequence": sample_sequence("frame"),
    }
    kwargs[field] = value

    with pytest.raises(ValueError, match="nonempty"):
        LessonDescriptor(**kwargs)


def test_descriptor_rejects_invalid_sequence() -> None:
    with pytest.raises(TypeError, match="LessonSequence"):
        LessonDescriptor("key", "Title", object())  # type: ignore[arg-type]


def test_catalog_preserves_order_and_identity() -> None:
    catalog = sample_catalog()

    assert catalog.keys == ("first", "second")
    assert catalog.titles == ("First Lesson", "Second Lesson")
    assert tuple(catalog) == catalog.lessons
    assert catalog[0] is catalog.lessons[0]
    assert len(catalog) == 2


def test_catalog_lookup_membership_and_normalization() -> None:
    catalog = sample_catalog()

    assert catalog.lesson(" first ") is catalog[0]
    assert catalog.has_lesson("second")
    assert "first" in catalog
    assert "missing" not in catalog


def test_catalog_rejects_unknown_key() -> None:
    with pytest.raises(KeyError, match="unknown lesson"):
        sample_catalog().lesson("missing")


def test_catalog_requires_at_least_one_lesson() -> None:
    with pytest.raises(ValueError, match="at least one"):
        LessonCatalog(())


def test_catalog_rejects_duplicate_normalized_keys() -> None:
    sequence = sample_sequence("frame")

    with pytest.raises(ValueError, match="unique"):
        LessonCatalog(
            (
                LessonDescriptor("same", "First", sequence),
                LessonDescriptor(" same ", "Second", sequence),
            )
        )


def test_catalog_rejects_non_descriptor_entries() -> None:
    with pytest.raises(TypeError, match="LessonDescriptor"):
        LessonCatalog((object(),))  # type: ignore[arg-type]


def test_catalog_public_collection_is_immutable() -> None:
    catalog = sample_catalog()

    assert isinstance(catalog.lessons, tuple)

    with pytest.raises(AttributeError):
        catalog.lessons = ()  # type: ignore[misc]


def test_catalog_imports_without_manim_or_numpy() -> None:
    sys.modules.pop("engine.lesson_catalog", None)
    before = set(sys.modules)

    module = importlib.import_module("engine.lesson_catalog")
    imported = set(sys.modules) - before

    assert module.LessonCatalog is not None
    assert not any(name == "manim" or name.startswith("manim.") for name in imported)
    assert not any(name == "numpy" or name.startswith("numpy.") for name in imported)
