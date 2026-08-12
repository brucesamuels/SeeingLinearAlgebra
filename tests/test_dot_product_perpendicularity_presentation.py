from pathlib import Path

SCENE_PATH = Path("scenes/dot_product_perpendicularity_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_uses_established_header_hierarchy_and_2d_geometry() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Dot Product and Perpendicularity"' in source
    assert "NumberPlane(" in source
    assert "ThreeDScene" not in source
    assert "ambient_camera" not in source


def test_scene_has_six_distinct_pedagogical_cards() -> None:
    source = scene_source()
    for helper in (
        "_transitional_question",
        "_coordinate_formula",
        "_geometric_formula",
        "_perpendicularity_test",
        "_sign_interpretation",
        "_takeaway",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_scene_contains_both_dot_product_formulas_and_final_theorem() -> None:
    source = scene_source()
    assert r"\mathbf{u}\cdot\mathbf{v}=u_1v_1+u_2v_2" in source
    assert r"\mathbf{u}\cdot\mathbf{v}=\|\mathbf{u}\|\,\|\mathbf{v}\|\cos\theta" in source
    assert r"\mathbf{u}\cdot\mathbf{v}=0" in source
    assert "FINAL_STATEMENT" in source


def test_scene_includes_sign_interpretation_and_projection_bridge() -> None:
    source = scene_source()
    assert r"\mathbf{u}\cdot\mathbf{v}>0" in source
    assert r"\mathbf{u}\cdot\mathbf{v}=0" in source
    assert r"\mathbf{u}\cdot\mathbf{v}<0" in source
    assert "Next: projection will isolate the component in a chosen direction." in source


def test_scene_keeps_math_and_explanatory_prose_in_separate_zones() -> None:
    source = scene_source()
    assert ".next_to(self.lesson_title_mobject, DOWN" in source
    assert ".to_edge(DOWN, buff=0.38)" in source or ".to_edge(DOWN, buff=0.42)" in source
    assert "scale_to_fit_width(12.4)" in source or "scale_to_fit_width(12.2)" in source


def test_scene_uses_standard_manim_primitives_for_geometry() -> None:
    source = scene_source()
    for token in ("Arrow(", "MathTex(", "Arc(", "RightAngle(", "SurroundingRectangle("):
        assert token in source



def test_card4_uses_explicit_split_layout_revision() -> None:
    source = scene_source()
    assert 'CP150_REVISION = "r6_verified_split_layout_test_fix"' in source
    assert 'x_length=4.7' in source
    assert '.move_to(LEFT * 3.05 + DOWN * 0.25)' in source
    assert 'derivation.move_to(RIGHT * 3.05 + UP * 0.35)' in source


def test_repository_scripts_verify_and_render_the_current_revision() -> None:
    check_source = Path("scripts/check_cp150_dot_product_perpendicularity.zsh").read_text(
        encoding="utf-8"
    )
    render_source = Path("scripts/render_cp150_dot_product_perpendicularity.zsh").read_text(
        encoding="utf-8"
    )
    assert 'r6_verified_split_layout_test_fix' in check_source
    assert 'CP150_r6_verified_preview.mp4' in render_source
