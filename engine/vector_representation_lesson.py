"""Pedagogical metadata for the introductory vector-representation lesson."""

from __future__ import annotations

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


VECTOR_REPRESENTATION_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat("introduce_geometric_arrow", LessonBeatRole.ORIENT),
        LessonBeat("predict_coordinate_change", LessonBeatRole.PREDICT),
        LessonBeat("synchronize_arrow_and_coordinates", LessonBeatRole.OBSERVE),
        LessonBeat("stabilize_equivalent_views", LessonBeatRole.STABILIZE),
        LessonBeat("reflect_on_vector_identity", LessonBeatRole.REFLECT),
    )
)
