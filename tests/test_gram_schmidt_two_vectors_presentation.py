from pathlib import Path

SCENE_PATH = Path("scenes/gram_schmidt_two_vectors_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_header_and_revision() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Gram-Schmidt with Two Vectors"' in source
    assert 'SCENE_REVISION = "cp157_r6_card2_marker_natural_quadrant"' in source
    assert "class GramSchmidtTwoVectorsPresentation(Scene)" in source


def test_scene_has_six_cards() -> None:
    source = scene_source()
    for helper in (
        "_starting_pair_card",
        "_projection_card",
        "_subtract_projection_card",
        "_orthogonality_card",
        "_summary_card",
        "_bridge_card",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_scene_uses_square_plane_and_right_angle_marker() -> None:
    source = scene_source()
    assert "x_length=5.9" in source and "y_length=5.9" in source
    assert "def _right_angle_marker" in source
    assert "Create(right_angle)" in source


def test_projection_and_subtraction_equations_are_present() -> None:
    source = scene_source()
    for token in (
        r"\operatorname{proj}_{\mathbf u_1}\mathbf v_2",
        r"=2\mathbf u_1=(2,4)",
        r"=(4,3)-(2,4)",
        r"=(2,-1)",
        r"=2-2=0",
    ):
        assert token in source


def test_summary_and_bridge_cards_state_core_results() -> None:
    source = scene_source()
    for token in (
        "self.lesson.GENERAL_FORMULA",
        "self.lesson.SPAN_FACT",
        r"\mathbf e_1=\frac{\mathbf u_1}{\|\mathbf u_1\|}",
        r"\mathbf e_2=\frac{\mathbf u_2}{\|\mathbf u_2\|}",
    ):
        assert token in source


def test_projection_label_and_bridge_layout_refinement() -> None:
    source = scene_source()
    assert r"LEFT * 0.58 + UP * 0.62" in source
    assert r"arrange(DOWN, buff=0.28).move_to(DOWN * 0.42)" in source


def test_card2_uses_diagram_right_angle_marker_instead_of_formula_box() -> None:
    source = scene_source()
    assert 'SCENE_REVISION = "cp157_r6_card2_marker_natural_quadrant"' in source
    assert 'self.snapshot.projection,' in source
    assert '-self.snapshot.u1,' in source
    assert 'self.snapshot.v2 - self.snapshot.projection' in source
    assert 'Create(right_angle)' in source
    assert 'projection_box = SurroundingRectangle' not in source
    assert 'projection_fact = VGroup(' not in source



def test_card2_right_angle_marker_uses_visible_projection_ray() -> None:
    source = scene_source()
    assert "SCENE_REVISION = \"cp157_r6_card2_marker_natural_quadrant\"" in source
    assert "-self.snapshot.u1," in source
    assert "self.snapshot.v2 - self.snapshot.projection" in source
