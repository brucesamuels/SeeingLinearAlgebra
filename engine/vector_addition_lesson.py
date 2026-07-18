"""Pedagogical metadata for the introductory vector-addition lesson."""

from __future__ import annotations

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


VECTOR_ADDITION_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat("show_vectors_in_standard_position", LessonBeatRole.ORIENT),
        LessonBeat("predict_second_tail", LessonBeatRole.PREDICT),
        LessonBeat("translate_second_vector", LessonBeatRole.OBSERVE),
        LessonBeat("draw_resultant_and_compute", LessonBeatRole.STABILIZE),
        LessonBeat("reveal_parallelogram", LessonBeatRole.OBSERVE),
        LessonBeat("interpret_successive_displacements", LessonBeatRole.REFLECT),
    )
)
