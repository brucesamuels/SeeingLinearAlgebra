from __future__ import annotations

import dataclasses

import pytest

from engine.chapter_outline import ChapterOutline, ChapterSection
from engine.lesson_catalog import LessonCatalog, LessonDescriptor
from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


def sample_catalog() -> LessonCatalog:
    sequence = LessonSequence(
        (LessonBeat("frame", LessonBeatRole.ORIENT),)
    )
    return LessonCatalog(
        (
            LessonDescriptor("known", "Known Lesson", sequence),
        )
    )


def sample_outline() -> ChapterOutline:
    return ChapterOutline(
        key="chapter",
        title="A Chapter",
        sections=(
            ChapterSection(
                key="first",
                title="First",
                purpose="Introduce the idea.",
            ),
            ChapterSection(
                key="second",
                title="Second",
                purpose="Develop the idea.",
                lesson_keys=("known",),
            ),
        ),
    )


def test_section_is_frozen_and_normalizes_fields() -> None:
    section = ChapterSection(
        key="  first  ",
        title="  First  ",
        purpose="  Introduce.  ",
        lesson_keys=("  known  ",),
    )

    assert section.key == "first"
    assert section.title == "First"
    assert section.purpose == "Introduce."
    assert section.lesson_keys == ("known",)

    with pytest.raises(dataclasses.FrozenInstanceError):
        section.title = "Changed"  # type: ignore[misc]


def test_section_rejects_duplicate_lesson_keys() -> None:
    with pytest.raises(ValueError, match="unique"):
        ChapterSection(
            key="section",
            title="Section",
            purpose="Purpose",
            lesson_keys=("known", " known "),
        )


def test_outline_preserves_order_and_supports_lookup() -> None:
    outline = sample_outline()

    assert outline.key == "chapter"
    assert outline.title == "A Chapter"
    assert outline.section_keys == ("first", "second")
    assert outline.section(" second ") is outline[1]
    assert tuple(outline) == outline.sections
    assert len(outline) == 2


def test_outline_collects_referenced_lesson_keys() -> None:
    assert sample_outline().referenced_lesson_keys == ("known",)


def test_outline_validates_references_against_catalog() -> None:
    outline = ChapterOutline(
        key="chapter",
        title="Chapter",
        sections=(
            ChapterSection(
                key="section",
                title="Section",
                purpose="Purpose",
                lesson_keys=("known", "missing"),
            ),
        ),
    )

    assert outline.validate_lesson_references(sample_catalog()) == ("missing",)


def test_outline_rejects_empty_or_duplicate_sections() -> None:
    with pytest.raises(ValueError, match="at least one"):
        ChapterOutline(key="chapter", title="Chapter", sections=())

    with pytest.raises(ValueError, match="unique"):
        ChapterOutline(
            key="chapter",
            title="Chapter",
            sections=(
                ChapterSection("same", "One", "Purpose"),
                ChapterSection(" same ", "Two", "Purpose"),
            ),
        )


def test_outline_has_no_execution_api() -> None:
    outline = sample_outline()

    assert not hasattr(outline, "run")
    assert not hasattr(outline, "render")
    assert not hasattr(outline, "transition")
