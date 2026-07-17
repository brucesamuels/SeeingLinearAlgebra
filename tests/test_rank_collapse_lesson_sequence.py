from __future__ import annotations

from engine.lesson_sequence import LessonBeatRole, LessonSequence
from engine.rank_collapse_lesson_sequence import RANK_COLLAPSE_LESSON_SEQUENCE
from scenes.rank_collapse_geometry_smoke import RankCollapseGeometrySmoke


def test_rank_collapse_sequence_has_expected_pedagogical_progression() -> None:
    assert RANK_COLLAPSE_LESSON_SEQUENCE.names == (
        "establish_initial_geometry",
        "predict_rank_loss",
        "animate_rank_collapse",
        "stabilize_degenerate_state",
        "reflect_on_dimension_loss",
    )
    assert RANK_COLLAPSE_LESSON_SEQUENCE.roles == (
        LessonBeatRole.ORIENT,
        LessonBeatRole.PREDICT,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.STABILIZE,
        LessonBeatRole.REFLECT,
    )


def test_rank_collapse_scene_declares_sequence_metadata() -> None:
    assert isinstance(RankCollapseGeometrySmoke.LESSON_SEQUENCE, LessonSequence)
    assert RankCollapseGeometrySmoke.LESSON_SEQUENCE is RANK_COLLAPSE_LESSON_SEQUENCE


def test_rank_collapse_scene_retains_explicit_construct() -> None:
    assert "construct" in RankCollapseGeometrySmoke.__dict__
    assert callable(RankCollapseGeometrySmoke.__dict__["construct"])


def test_second_lesson_uses_same_role_vocabulary_without_shared_names() -> None:
    from engine.full_rank_3d_lesson_sequence import FULL_RANK_3D_LESSON_SEQUENCE

    assert (
        RANK_COLLAPSE_LESSON_SEQUENCE.roles
        == FULL_RANK_3D_LESSON_SEQUENCE.roles
    )
    assert (
        set(RANK_COLLAPSE_LESSON_SEQUENCE.names)
        .isdisjoint(FULL_RANK_3D_LESSON_SEQUENCE.names)
    )
