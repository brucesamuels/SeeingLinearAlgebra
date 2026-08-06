from pathlib import Path

SCENE = Path("scenes/determinant_consequences_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantConsequencesPresentation(Scene):" in source()


def test_scene_has_running_context() -> None:
    text = source()
    assert "Properties of the Determinant" in text
    assert "Now we derive new consequences from the earlier properties." in text


def test_scene_includes_property_four() -> None:
    text = source()
    assert "Property 4: Equal rows imply determinant zero" in text
    assert r"\therefore\ \det\!\begin{bmatrix}a&b\\a&b\end{bmatrix}=0" in text


def test_scene_includes_property_five() -> None:
    text = source()
    assert "Property 5: A zero row implies determinant zero" in text
    assert r"\therefore\ D(0,r_2)=0" in text


def test_scene_includes_property_six() -> None:
    text = source()
    assert "Property 6: Adding a multiple of one row\\n" in text
    assert "to another leaves the determinant unchanged" in text
    assert r"r_1\to r_1-2r_2" in text
    assert r"D(r_1+kr_2,r_2)=D(r_1,r_2)+kD(r_2,r_2)" in text
    assert r"=D(r_1,r_2)" in text


def test_scene_includes_property_seven() -> None:
    text = source()
    assert "Property 7: Dependent rows imply determinant zero" in text
    assert r"D(r_1,r_2)=D(2r_2,r_2)=2D(r_2,r_2)" in text


def test_scene_has_summary_screen() -> None:
    text = source()
    assert "Summary so far" in text
    assert "These consequences will support elimination, triangular matrices, and invertibility." in text


def test_scene_clears_stage_individually() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_property_four_layout_distribution() -> None:
    text = source()
    assert "matrix.move_to(np.array([3.25, 1.3, 0.0]))" in text
    assert "general_statement.move_to(np.array([3.25, 0.1, 0.0]))" in text
    assert "negated_statement.move_to(np.array([3.25, -0.65, 0.0]))" in text
    assert "conclusion.move_to(np.array([3.25, -1.45, 0.0]))" in text


def test_property_six_layout_refinement() -> None:
    text = source()
    assert "label.move_to(np.array([0.0, 2.7, 0.0]))" in text
    assert "left_matrix.move_to(np.array([-3.6, 1.55, 0.0]))" in text
    assert "right_matrix.move_to(np.array([3.6, 1.55, 0.0]))" in text
    assert "operation.move_to(np.array([0.0, 1.55, 0.0]))" in text
    assert "left_det.move_to(np.array([-3.6, -2.55, 0.0]))" in text
    assert "right_det.move_to(np.array([3.6, -2.55, 0.0]))" in text
    assert "derivation_line_one.move_to(np.array([0.0, -3.0, 0.0]))" in text
    assert "derivation_line_two.move_to(np.array([0.0, -3.5, 0.0]))" in text
