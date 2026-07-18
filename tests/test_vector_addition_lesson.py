from __future__ import annotations

from engine.lesson_sequence import LessonBeatRole, LessonSequence
from engine.vector_addition_lesson import VECTOR_ADDITION_LESSON_SEQUENCE


def test_vector_addition_lesson_is_renderer_independent_sequence() -> None:
    assert isinstance(VECTOR_ADDITION_LESSON_SEQUENCE, LessonSequence)


def test_vector_addition_lesson_declares_the_pedagogical_order() -> None:
    assert VECTOR_ADDITION_LESSON_SEQUENCE.names == (
        "show_vectors_in_standard_position",
        "predict_second_tail",
        "translate_second_vector",
        "draw_resultant_and_compute",
        "reveal_parallelogram",
        "interpret_successive_displacements",
    )


def test_vector_addition_lesson_uses_expected_roles() -> None:
    assert VECTOR_ADDITION_LESSON_SEQUENCE.roles == (
        LessonBeatRole.ORIENT,
        LessonBeatRole.PREDICT,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.STABILIZE,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.REFLECT,
    )
