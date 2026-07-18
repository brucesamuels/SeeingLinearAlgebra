from __future__ import annotations

from engine.chapter_one_opening_sequence import (
    CHAPTER_ONE_OPENING_SEQUENCE,
)
from engine.chapter_sequence import ChapterSequence


def test_chapter_one_opening_is_a_chapter_sequence() -> None:
    assert isinstance(CHAPTER_ONE_OPENING_SEQUENCE, ChapterSequence)
    assert CHAPTER_ONE_OPENING_SEQUENCE.key == "chapter_1_opening"
    assert CHAPTER_ONE_OPENING_SEQUENCE.title == "Chapter 1: Vectors"


def test_chapter_one_opening_uses_the_approved_lesson_order() -> None:
    assert CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys == (
        "why_vectors",
        "vector_representation",
        "free_vector_equality",
        "placing_vector_at_origin",
    )

    assert CHAPTER_ONE_OPENING_SEQUENCE.lesson_titles == (
        "Why Vectors?",
        "What Is a Vector?",
        "Free Vectors and Equality",
        "Placing a Vector at the Origin",
    )


def test_chapter_one_opening_references_each_lesson_once() -> None:
    keys = CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys

    assert len(CHAPTER_ONE_OPENING_SEQUENCE) == 4
    assert len(set(keys)) == len(keys)
