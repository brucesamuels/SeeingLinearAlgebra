"""Pedagogical metadata for the full-rank 3D presentation lesson.

This module contains no Manim imports and performs no scene execution.
"""

from __future__ import annotations

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


FULL_RANK_3D_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat("establish_3d_frame", LessonBeatRole.ORIENT),
        LessonBeat("predict_combination_motion", LessonBeatRole.PREDICT),
        LessonBeat("animate_independent_coefficients", LessonBeatRole.OBSERVE),
        LessonBeat("pin_exact_final_state", LessonBeatRole.STABILIZE),
        LessonBeat("reflect_on_full_rank_span", LessonBeatRole.REFLECT),
    )
)
