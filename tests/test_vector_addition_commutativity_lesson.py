from __future__ import annotations

from engine.lesson_sequence import LessonBeatRole, LessonSequence
from engine.vector_addition_commutativity_lesson import (
    VECTOR_ADDITION_COMMUTATIVITY_LESSON_SEQUENCE,
)


def test_commutativity_lesson_is_renderer_independent_sequence() -> None:
    assert isinstance(
        VECTOR_ADDITION_COMMUTATIVITY_LESSON_SEQUENCE,
        LessonSequence,
    )


def test_commutativity_lesson_declares_pedagogical_order() -> None:
    assert VECTOR_ADDITION_COMMUTATIVITY_LESSON_SEQUENCE.names == (
        "show_u_and_v_in_standard_position",
        "predict_effect_of_reversing_order",
        "construct_u_plus_v",
        "construct_v_plus_u",
        "compare_paths_and_endpoint",
        "state_commutative_property",
    )


def test_commutativity_lesson_uses_expected_roles() -> None:
    assert VECTOR_ADDITION_COMMUTATIVITY_LESSON_SEQUENCE.roles == (
        LessonBeatRole.ORIENT,
        LessonBeatRole.PREDICT,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.STABILIZE,
        LessonBeatRole.REFLECT,
    )
