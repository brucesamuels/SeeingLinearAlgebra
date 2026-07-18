"""Pedagogical metadata for placing a vector at the origin."""

from __future__ import annotations

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


VECTOR_TO_ORIGIN_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat("show_general_vector", LessonBeatRole.ORIENT),
        LessonBeat("reveal_coordinate_system", LessonBeatRole.OBSERVE),
        LessonBeat("predict_origin_translation", LessonBeatRole.PREDICT),
        LessonBeat("translate_with_live_subtraction", LessonBeatRole.OBSERVE),
        LessonBeat("name_standard_position", LessonBeatRole.REFLECT),
    )
)
