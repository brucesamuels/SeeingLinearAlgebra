"""Pedagogical metadata for the free-vector equality lesson."""

from __future__ import annotations

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


FREE_VECTOR_EQUALITY_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat("show_one_vector", LessonBeatRole.ORIENT),
        LessonBeat("predict_after_translation", LessonBeatRole.PREDICT),
        LessonBeat("translate_equal_copies", LessonBeatRole.OBSERVE),
        LessonBeat("compare_invariants", LessonBeatRole.STABILIZE),
        LessonBeat("define_free_vector_equality", LessonBeatRole.REFLECT),
    )
)
