from __future__ import annotations

from engine.full_rank_3d_lesson_sequence import FULL_RANK_3D_LESSON_SEQUENCE
from engine.lesson_sequence import LessonBeatRole, LessonSequence
from scenes.full_rank_linear_combination_3d_presentation import FullRankLinearCombination3DPresentation


def test_full_rank_3d_sequence_has_expected_pedagogical_progression() -> None:
    assert FULL_RANK_3D_LESSON_SEQUENCE.names == (
        "establish_3d_frame",
        "predict_combination_motion",
        "animate_independent_coefficients",
        "pin_exact_final_state",
        "reflect_on_full_rank_span",
    )
    assert FULL_RANK_3D_LESSON_SEQUENCE.roles == (
        LessonBeatRole.ORIENT,
        LessonBeatRole.PREDICT,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.STABILIZE,
        LessonBeatRole.REFLECT,
    )


def test_full_rank_3d_scene_declares_sequence_metadata() -> None:
    assert isinstance(FullRankLinearCombination3DPresentation.LESSON_SEQUENCE, LessonSequence)
    assert (
        FullRankLinearCombination3DPresentation.LESSON_SEQUENCE
        is FULL_RANK_3D_LESSON_SEQUENCE
    )


def test_sequence_metadata_does_not_replace_explicit_construct() -> None:
    assert "construct" in FullRankLinearCombination3DPresentation.__dict__
    assert callable(FullRankLinearCombination3DPresentation.__dict__["construct"])
