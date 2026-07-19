from __future__ import annotations

from engine.lesson_sequence import LessonBeatRole, LessonSequence
from engine.vector_subtraction_lesson import VECTOR_SUBTRACTION_LESSON_SEQUENCE


def test_vector_subtraction_lesson_is_renderer_independent_sequence() -> None:
    assert isinstance(VECTOR_SUBTRACTION_LESSON_SEQUENCE, LessonSequence)


def test_vector_subtraction_lesson_declares_pedagogical_order() -> None:
    assert VECTOR_SUBTRACTION_LESSON_SEQUENCE.names == (
        "show_u_and_v_in_standard_position",
        "predict_how_to_draw_subtraction",
        "reverse_v_to_form_negative_v",
        "translate_negative_v_to_tip_of_u",
        "compute_u_plus_negative_v",
        "state_subtraction_as_addition",
    )


def test_vector_subtraction_lesson_uses_expected_roles() -> None:
    assert VECTOR_SUBTRACTION_LESSON_SEQUENCE.roles == (
        LessonBeatRole.ORIENT,
        LessonBeatRole.PREDICT,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.STABILIZE,
        LessonBeatRole.REFLECT,
    )
