from pathlib import Path

SCENE_PATH = Path("scenes/vector_projection_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_uses_chapter_header_and_scene_class() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Projection onto a Vector"' in source
    assert "class VectorProjectionPresentation(Scene)" in source
    assert 'SCENE_REVISION = "cp153_r2_left_import_hotfix"' in source


def test_scene_has_six_cards() -> None:
    source = scene_source()
    for helper in (
        "_geometric_question_card",
        "_perpendicular_drop_card",
        "_derive_coefficient_card",
        "_formula_card",
        "_worked_example_card",
        "_orthogonal_residual_card",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_geometry_uses_projection_drop_and_right_angle_marker() -> None:
    source = scene_source()
    assert "DashedLine(" in source
    assert "_right_angle_marker" in source
    assert "self.snapshot.projection" in source
    assert "snapshot.residual" in source


def test_derivation_uses_perpendicular_residual_condition() -> None:
    source = scene_source()
    assert r"(\mathbf{x}-c\mathbf{u})\cdot\mathbf{u}=0" in source
    assert r"c=\frac{\mathbf{x}\cdot\mathbf{u}}{\mathbf{u}\cdot\mathbf{u}}" in source


def test_scene_includes_general_and_unit_projection_formulas() -> None:
    source = scene_source()
    assert "self.lesson.GENERAL_FORMULA" in source
    assert "self.lesson.UNIT_FORMULA" in source


def test_worked_example_uses_hand_friendly_data() -> None:
    source = scene_source()
    assert r"\mathbf{x}=(3,3),\quad \mathbf{u}=(4,1)" in source
    assert r"\mathbf{x}\cdot\mathbf{u}=15" in source
    assert r"\mathbf{u}\cdot\mathbf{u}=17" in source
    assert r"c=\frac{15}{17}" in source


def test_final_card_bridges_to_orthogonal_decomposition() -> None:
    source = scene_source()
    assert "Projection creates an orthogonal decomposition" in source
    assert "self.lesson.DECOMPOSITION" in source
    assert "self.lesson.ORTHOGONAL_RESIDUAL" in source


def test_scene_keeps_slower_pacing_from_approved_previous_lesson() -> None:
    source = scene_source()
    assert "TRANSITION_TIME = 1.35" in source
    assert "EMPHASIS_TIME = 1.15" in source
    assert "HOLD_TIME = 2.6" in source
    assert "LONG_HOLD_TIME = 3.0" in source


def test_scene_imports_every_direction_constant_used_by_worked_example() -> None:
    source = scene_source()
    import_block = source.split("from manim import (", 1)[1].split(")", 1)[0]
    assert "LEFT," in import_block
    assert ".shift(LEFT * 3.35 + DOWN * 0.65)" in source
