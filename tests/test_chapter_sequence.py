from __future__ import annotations

import inspect

import pytest

from engine.chapter_sequence import ChapterLessonReference, ChapterSequence


def _sequence() -> ChapterSequence:
    return ChapterSequence(
        key="chapter_1",
        title="Chapter 1",
        lessons=(
            ChapterLessonReference("lesson_a", "Lesson A"),
            ChapterLessonReference("lesson_b", "Lesson B"),
        ),
    )


def test_lesson_reference_normalizes_text() -> None:
    reference = ChapterLessonReference("  lesson_a  ", "  Lesson A  ")

    assert reference.key == "lesson_a"
    assert reference.title == "Lesson A"


@pytest.mark.parametrize("attribute", ["key", "title"])
def test_lesson_reference_rejects_non_string_text(attribute: str) -> None:
    values = {"key": "lesson", "title": "Lesson"}
    values[attribute] = 3

    with pytest.raises(TypeError):
        ChapterLessonReference(**values)


@pytest.mark.parametrize("attribute", ["key", "title"])
def test_lesson_reference_rejects_empty_text(attribute: str) -> None:
    values = {"key": "lesson", "title": "Lesson"}
    values[attribute] = "   "

    with pytest.raises(ValueError):
        ChapterLessonReference(**values)


def test_sequence_preserves_declared_order() -> None:
    sequence = _sequence()

    assert sequence.key == "chapter_1"
    assert sequence.title == "Chapter 1"
    assert sequence.lesson_keys == ("lesson_a", "lesson_b")
    assert sequence.lesson_titles == ("Lesson A", "Lesson B")
    assert tuple(sequence) == sequence.lessons


def test_sequence_supports_lookup_and_membership() -> None:
    sequence = _sequence()

    assert sequence.lesson("lesson_b").title == "Lesson B"
    assert sequence.has_lesson("lesson_a")
    assert "lesson_b" in sequence
    assert "missing" not in sequence


def test_sequence_supports_indexing_and_slicing() -> None:
    sequence = _sequence()

    assert sequence[0].key == "lesson_a"
    assert sequence[1:].__class__ is tuple
    assert tuple(lesson.key for lesson in sequence[1:]) == ("lesson_b",)


def test_sequence_rejects_duplicate_lesson_keys() -> None:
    with pytest.raises(ValueError, match="must be unique"):
        ChapterSequence(
            key="chapter",
            title="Chapter",
            lessons=(
                ChapterLessonReference("same", "First"),
                ChapterLessonReference("same", "Second"),
            ),
        )


def test_sequence_rejects_empty_or_invalid_lessons() -> None:
    with pytest.raises(ValueError, match="at least one lesson"):
        ChapterSequence(key="chapter", title="Chapter", lessons=())

    with pytest.raises(TypeError, match="ChapterLessonReference"):
        ChapterSequence(
            key="chapter",
            title="Chapter",
            lessons=("not a reference",),
        )


def test_sequence_lookup_reports_unknown_key() -> None:
    with pytest.raises(KeyError, match="unknown chapter lesson"):
        _sequence().lesson("missing")


def test_sequence_module_has_no_renderer_dependency() -> None:
    source = inspect.getsource(inspect.getmodule(ChapterSequence))

    assert "from manim" not in source
    assert "import manim" not in source
    assert "Scene" not in source
