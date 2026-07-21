from __future__ import annotations

from engine.chapter_one_opening_sequence import CHAPTER_ONE_OPENING_SEQUENCE
from engine.chapter_sequence import ChapterSequence


def test_chapter_one_opening_is_a_chapter_sequence() -> None:
    assert isinstance(CHAPTER_ONE_OPENING_SEQUENCE, ChapterSequence)
    assert CHAPTER_ONE_OPENING_SEQUENCE.key == "chapter_1_opening"


def test_complete_chapter_one_lesson_order() -> None:
    assert CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys == (
        "why_vectors",
        "vector_representation",
        "free_vector_equality",
        "placing_vector_at_origin",
        "special_vectors",
        "scalar_multiplication",
        "vector_addition",
        "vector_addition_commutativity",
        "vector_subtraction",
        "three_vector_addition",
        "infinite_possibilities",
    )


def test_special_vectors_and_infinite_possibilities_are_unique() -> None:
    keys = CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys

    assert len(keys) == 11
    assert len(set(keys)) == len(keys)
    assert keys.index("placing_vector_at_origin") + 1 == keys.index(
        "special_vectors"
    )
    assert keys.index("special_vectors") + 1 == keys.index(
        "scalar_multiplication"
    )
    assert keys[-1] == "infinite_possibilities"
