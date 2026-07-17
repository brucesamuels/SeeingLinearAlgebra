from __future__ import annotations

from engine.lesson_sequence import LessonBeatRole
from engine.vector_representation_lesson import (
    VECTOR_REPRESENTATION_LESSON_SEQUENCE,
)


def test_vector_representation_lesson_uses_existing_role_vocabulary() -> None:
    assert VECTOR_REPRESENTATION_LESSON_SEQUENCE.roles == (
        LessonBeatRole.ORIENT,
        LessonBeatRole.PREDICT,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.STABILIZE,
        LessonBeatRole.REFLECT,
    )


def test_vector_representation_lesson_has_specific_beat_names() -> None:
    assert VECTOR_REPRESENTATION_LESSON_SEQUENCE.names == (
        "introduce_geometric_arrow",
        "predict_coordinate_change",
        "synchronize_arrow_and_coordinates",
        "stabilize_equivalent_views",
        "reflect_on_vector_identity",
    )
