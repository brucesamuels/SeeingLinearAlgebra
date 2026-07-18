from __future__ import annotations

from engine.lesson_sequence import LessonBeatRole, LessonSequence
from engine.three_vector_addition_lesson import (
    THREE_VECTOR_ADDITION_LESSON_SEQUENCE,
)


def test_three_vector_addition_lesson_is_renderer_independent_sequence() -> None:
    assert isinstance(THREE_VECTOR_ADDITION_LESSON_SEQUENCE, LessonSequence)


def test_three_vector_addition_lesson_declares_the_pedagogical_order() -> None:
    assert THREE_VECTOR_ADDITION_LESSON_SEQUENCE.names == (
        'show_three_vectors_in_standard_position',
        'predict_successive_tail_placements',
        'translate_second_and_third_vectors',
        'draw_resultant_and_compute_sum',
        'reveal_parallelepiped',
        'interpret_three_vector_sum_in_space',
    )


def test_three_vector_addition_lesson_uses_expected_roles() -> None:
    assert THREE_VECTOR_ADDITION_LESSON_SEQUENCE.roles == (
        LessonBeatRole.ORIENT,
        LessonBeatRole.PREDICT,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.STABILIZE,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.REFLECT,
    )
