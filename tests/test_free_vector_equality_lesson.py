from __future__ import annotations

from engine.free_vector_equality_lesson import (
    FREE_VECTOR_EQUALITY_LESSON_SEQUENCE,
)
from engine.lesson_sequence import LessonBeatRole


def test_free_vector_lesson_reuses_existing_roles() -> None:
    assert FREE_VECTOR_EQUALITY_LESSON_SEQUENCE.roles == (
        LessonBeatRole.ORIENT,
        LessonBeatRole.PREDICT,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.STABILIZE,
        LessonBeatRole.REFLECT,
    )


def test_free_vector_lesson_has_specific_beat_names() -> None:
    assert FREE_VECTOR_EQUALITY_LESSON_SEQUENCE.names == (
        "show_one_vector",
        "predict_after_translation",
        "translate_equal_copies",
        "compare_invariants",
        "define_free_vector_equality",
    )
