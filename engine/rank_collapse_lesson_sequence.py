"""Pedagogical metadata for the rank-collapse presentation lesson.

This module is renderer-independent. It describes instructional intent without
executing scene methods, animations, or mathematical transformations.
"""

from __future__ import annotations

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


RANK_COLLAPSE_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat("establish_initial_geometry", LessonBeatRole.ORIENT),
        LessonBeat("predict_rank_loss", LessonBeatRole.PREDICT),
        LessonBeat("animate_rank_collapse", LessonBeatRole.OBSERVE),
        LessonBeat("stabilize_degenerate_state", LessonBeatRole.STABILIZE),
        LessonBeat("reflect_on_dimension_loss", LessonBeatRole.REFLECT),
    )
)
