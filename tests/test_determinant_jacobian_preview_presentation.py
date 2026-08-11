from pathlib import Path

SCENE = Path("scenes/determinant_jacobian_preview_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_and_card_sequence_exist() -> None:
    text = source()
    assert "class DeterminantJacobianPreviewPresentation(Scene):" in text
    for call in (
        "self.show_linear_scaling(banner)",
        "self.show_local_linearization(banner)",
        "self.show_jacobian_matrix(banner)",
        "self.show_linear_example(banner)",
        "self.show_polar_coordinates(banner)",
        "self.show_takeaway(banner)",
    ):
        assert call in text


def test_scene_visualizes_zooming_into_a_nonlinear_map() -> None:
    text = source()
    assert "focus = Polygon" in text
    assert "nonlinear_patch = Polygon" in text
    assert "linear_patch = Polygon" in text
    assert 'zoom_label = Text("zoom in on one tiny patch"' in text
    assert "zoom_patch = focus.copy()" in text
    assert "zoom_patch.target.scale(3.6)" in text
    assert 'zoom_patch.target.move_to(np.array([3.2,-0.15,0.0]))' in text
    assert "MoveToTarget(zoom_patch)" in text
    assert 'apply_label = Text("apply the nonlinear map"' in text
    assert "ReplacementTransform(zoom_patch, nonlinear_patch)" in text
    assert 'actual_label = Text("blue: actual nonlinear image"' in text
    assert 'approx_label = Text("green: Jacobian (linear) approximation"' in text
    assert "the nonlinear image and its linear approximation nearly agree" in text


def test_scene_card_three_uses_larger_jacobian_mathematics() -> None:
    text = source()
    assert 'jac = MathTex(jacobian_matrix_tex(), font_size=36, color=BLUE)' in text
    assert 'local = MathTex(local_area_tex(), font_size=38, color=GREEN)' in text


def test_polar_coordinate_card_has_balanced_formula_positions() -> None:
    text = source()
    assert 'title = self.stage_title("Polar coordinates give a nonlinear change of variables", size=22)' in text
    assert 'title.move_to(np.array([0.0, 2.70, 0.0]))' in text
    assert 'MathTex(lines[0], font_size=28, color=WHITE)' in text
    assert 'MathTex(lines[1], font_size=28, color=BLUE)' in text
    assert 'MathTex(lines[2], font_size=38, color=GREEN)' in text
    assert 'formulas.scale_to_fit_width(8.8)' in text
    assert 'formulas.move_to(np.array([0.0,-0.60,0.0]))' in text
    assert 'formulas[0].shift(np.array([0.0,-0.12,0.0]))' in text
    assert 'formulas[2].shift(np.array([0.0,0.12,0.0]))' in text
    assert "The local area scale depends on the radius r." not in text


def test_polar_area_sector_card_is_excluded_from_stack() -> None:
    text = source()
    assert "self.show_polar_area_element(banner)" not in text
    assert "def show_polar_area_element" not in text
    assert "Why does polar area contain a factor of r?" not in text


def test_final_card_keeps_largest_equation_emphasis() -> None:
    text = source()
    assert 'title = self.stage_title("The big takeaway", size=29)' in text
    assert 'font_size=44, color=GREEN' in text


def test_scene_uses_safe_clear_pattern() -> None:
    text = source()
    assert '*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]' in text
    assert "VGroup(*self.mobjects)" not in text
