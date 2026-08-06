from pathlib import Path

SCENE = Path("scenes/determinant_properties_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantPropertiesPresentation(Scene):" in source()


def test_scene_has_persistent_context_banner() -> None:
    text = source()
    assert "Properties of the Determinant" in text
    assert "We are building a list of determinant properties." in text
    assert "self.play(FadeOut(subtitle))" in text


def test_scene_includes_property_one() -> None:
    text = source()
    assert "Property 1: det(I) = 1" in text
    assert r"\det(I)=1" in text


def test_scene_includes_property_two() -> None:
    text = source()
    assert "Property 2: Swapping two rows changes the sign" in text
    assert r"\det\!\begin{bmatrix}2&1\\1&2\end{bmatrix}=3" in text
    assert r"\det\!\begin{bmatrix}1&2\\2&1\end{bmatrix}" in text
    assert r"=-3" in text
    assert "reflection across y = x" in text
    assert "reflected_vertices = base.image_vertices[:, ::-1]" in text


def test_scene_includes_property_three_scaling() -> None:
    text = source()
    assert "Property 3a: Scaling one row scales the determinant" in text
    assert r"\det(2r_1,r_2)=2\det(A)=6" in text
    assert "left_det.move_to(np.array([-3.3, -2.75, 0.0]))" in text
    assert "right_det.move_to(np.array([1.7, -2.75, 0.0]))" in text


def test_scene_includes_property_three_additivity() -> None:
    text = source()
    assert "Property 3b: The determinant is additive in one row" in text
    assert r"D(u+s,r_2)=D(u,r_2)+D(s,r_2)" in text
    assert r"2+1=3" in text
    assert "font_size=36, color=YELLOW" in text
    assert "font_size=38, color=ORANGE" in text
    assert "self.play(Write(matrix_block[4]))" in text


def test_scene_has_summary_screen() -> None:
    text = source()
    assert "Summary so far" in text
    assert "Next we will derive more determinant consequences from these properties." in text


def test_scene_fades_mobjects_individually() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_additivity_panel_is_compact_and_inset() -> None:
    text = source()
    assert 'MathTex(r"r_1=u+s", font_size=36, color=WHITE)' in text
    assert 'MathTex(r"u=(1,0),\quad s=(1,1)", font_size=32, color=WHITE)' in text
    assert 'MathTex(r"r_2=(1,2)", font_size=32, color=WHITE)' in text
    assert 'MathTex(r"D(u+s,r_2)=D(u,r_2)+D(s,r_2)", font_size=36, color=YELLOW)' in text
    assert 'move_to(np.array([2.35, -0.2, 0.0]))' in text


def test_layout_refinement_moves_matrices_lower() -> None:
    text = source()
    assert "left_matrix.move_to(np.array([-3.4, 1.2, 0.0]))" in text
    assert "right_matrix.move_to(np.array([1.6, 1.2, 0.0]))" in text
    assert "label.move_to(np.array([0.0, 2.3, 0.0]))" in text
    assert "left_matrix.move_to(np.array([-3.3, 1.35, 0.0]))" in text
    assert "right_matrix.move_to(np.array([1.7, 1.35, 0.0]))" in text


def test_reflection_objects_are_confined_to_property_two() -> None:
    text = source()
    property_two = text.split("def show_property_two", 1)[1].split("def show_property_three_scaling", 1)[0]
    property_three = text.split("def show_property_three_scaling", 1)[1].split("def show_property_three_additivity", 1)[0]
    assert "reflection_line" in property_two
    assert "reflection_caption" in property_two
    assert "reflection_line" not in property_three
    assert "reflection_caption" not in property_three


def test_property_two_red_determinant_uses_side_by_side_layout() -> None:
    text = source()
    assert 'right_det_matrix = MathTex(' in text
    assert 'font_size=27, color=RED' in text
    assert 'right_det_value = MathTex(r"=-3", font_size=31, color=RED)' in text
    assert 'VGroup(right_det_matrix, right_det_value).arrange' in text
