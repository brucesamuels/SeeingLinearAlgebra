from pathlib import Path


SCENE_PATH = Path("scenes/linear_system_meaning_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_starts_with_a_planar_scaffold_and_lifts_to_three_dimensions() -> None:
    source = scene_source()
    assert "Axes(" in source
    assert "ThreeDAxes(" in source
    assert "In the plane, solving means finding where the graphs meet." in source
    assert "The same idea extends beyond the plane." in source
    assert "In three dimensions, the solution is where three planes meet." in source
    assert "self.play(FadeOut(planar_solution_label), run_time=0.4)" in source
    assert "In three dimensions, three equations can describe one common point." in source


def test_scene_includes_line_and_plane_geometry() -> None:
    source = scene_source()
    assert "class LinearSystemMeaningPresentation(ThreeDScene):" in source
    assert source.count("axes.plot(") == 1
    assert "for row_index, color in enumerate(self.LINE_COLORS)" in source
    assert source.count("Surface(") == 1
    assert "for row_index, color in enumerate(self.PLANE_COLORS)" in source
    assert "Dot(" in source
    assert "Dot3D(" in source


def test_scene_connects_the_system_to_equations_matrix_and_columns() -> None:
    source = scene_source()
    assert "System of equations" in source
    assert "Matrix equation" in source
    assert "The same system as a column combination" in source
    assert r"x\mathbf{a}_1+y\mathbf{a}_2+z\mathbf{a}_3=\mathbf{b}" in source


def test_scene_restores_a_front_facing_camera_before_algebra() -> None:
    source = scene_source()
    assert "self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=0.8)" in source


def test_scene_animates_row_by_column_multiplication_with_color_highlights() -> None:
    source = scene_source()
    assert "matrix_equation.animate.move_to(UP * 0.10).scale(1.15)" in source
    assert "Read the product row by column" in source
    assert "Each row of A dots with x to produce one entry of b." in source
    assert "Matrix(" in source
    assert "matrix_block.get_rows()" in source
    assert "vector_block.get_entries()" in source
    assert "rhs_block.get_entries()" in source
    assert "SurroundingRectangle(row, color=color" in source
    assert "row.animate.set_color(color)" in source
    assert "vector_entries.animate.set_color(color)" in source
    assert "rhs_entry.animate.set_color(color)" in source
    assert r"1(x)+1(y)+1(z)=3" in source
    assert r"2(x)-1(y)+1(z)=2" in source
    assert r"1(x)+2(y)-1(z)=2" in source
    assert "TransformMatchingTex" not in source


def test_scene_states_the_meaning_of_solving_ax_equals_b() -> None:
    source = scene_source()
    assert "The entries of x are coefficients." in source
    assert "Solving A x = b means finding those coefficients." in source
    assert "What do the entries of x control?" in source


def test_scene_intentionally_omits_elimination() -> None:
    lowered = scene_source().lower()
    assert "gaussian elimination" not in lowered
    assert "gauss-jordan" not in lowered
    assert "row reduction" not in lowered
    assert "row operation" not in lowered


def test_student_facing_scene_omits_checkpoint_language_and_fits_formulae() -> None:
    source = scene_source()
    student_strings = [
        line
        for line in source.splitlines()
        if "Text(" in line or "MathTex(" in line
    ]
    assert all("checkpoint" not in line.lower() for line in student_strings)
    assert "formula.scale_to_fit_width(11.6)" in source
    assert "group.scale_to_fit_width(11.5)" in source
