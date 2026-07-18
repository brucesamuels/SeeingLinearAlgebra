"""Pedagogical metadata for the three-vector 3D addition lesson."""

from __future__ import annotations

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


THREE_VECTOR_ADDITION_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat('show_three_vectors_in_standard_position', LessonBeatRole.ORIENT),
        LessonBeat('predict_successive_tail_placements', LessonBeatRole.PREDICT),
        LessonBeat('translate_second_and_third_vectors', LessonBeatRole.OBSERVE),
        LessonBeat('draw_resultant_and_compute_sum', LessonBeatRole.STABILIZE),
        LessonBeat('reveal_parallelepiped', LessonBeatRole.OBSERVE),
        LessonBeat('interpret_three_vector_sum_in_space', LessonBeatRole.REFLECT),
    )
)
