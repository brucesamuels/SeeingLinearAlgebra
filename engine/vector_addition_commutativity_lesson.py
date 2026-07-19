"""Pedagogical metadata for the commutativity of vector addition lesson."""

from __future__ import annotations

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


VECTOR_ADDITION_COMMUTATIVITY_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat(
            "show_u_and_v_in_standard_position",
            LessonBeatRole.ORIENT,
        ),
        LessonBeat(
            "predict_effect_of_reversing_order",
            LessonBeatRole.PREDICT,
        ),
        LessonBeat(
            "construct_u_plus_v",
            LessonBeatRole.OBSERVE,
        ),
        LessonBeat(
            "construct_v_plus_u",
            LessonBeatRole.OBSERVE,
        ),
        LessonBeat(
            "compare_paths_and_endpoint",
            LessonBeatRole.STABILIZE,
        ),
        LessonBeat(
            "state_commutative_property",
            LessonBeatRole.REFLECT,
        ),
    )
)
