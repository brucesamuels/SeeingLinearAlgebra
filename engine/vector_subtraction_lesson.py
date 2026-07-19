"""Pedagogical metadata for subtraction as adding a negative vector."""

from __future__ import annotations

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


VECTOR_SUBTRACTION_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat(
            "show_u_and_v_in_standard_position",
            LessonBeatRole.ORIENT,
        ),
        LessonBeat(
            "predict_how_to_draw_subtraction",
            LessonBeatRole.PREDICT,
        ),
        LessonBeat(
            "reverse_v_to_form_negative_v",
            LessonBeatRole.OBSERVE,
        ),
        LessonBeat(
            "translate_negative_v_to_tip_of_u",
            LessonBeatRole.OBSERVE,
        ),
        LessonBeat(
            "compute_u_plus_negative_v",
            LessonBeatRole.STABILIZE,
        ),
        LessonBeat(
            "state_subtraction_as_addition",
            LessonBeatRole.REFLECT,
        ),
    )
)
