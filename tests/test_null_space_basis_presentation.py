from pathlib import Path

SCENE_PATH = Path("scenes/null_space_basis_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_introduces_basis_construction_from_free_variables() -> None:
    source = scene_source()
    assert "A Basis for the Null Space" in source
    assert "Build one special solution for each free variable." in source
    assert "The y- and z-columns have no pivots" in source
    assert "How many special solutions should two free variables produce?" in source


def test_scene_constructs_two_special_solutions() -> None:
    source = scene_source()
    assert "Turn on one free variable at a time" in source
    assert "Set y = 1, z = 0" in source
    assert "Set y = 0, z = 1" in source
    assert r"\mathbf{s}_1=\begin{bmatrix}-2\\1\\0\end{bmatrix}" in source
    assert r"\mathbf{s}_2=\begin{bmatrix}1\\0\\1\end{bmatrix}" in source


def test_scene_verifies_membership_spanning_and_independence() -> None:
    source = scene_source()
    assert "First check: both vectors lie in N(A)" in source
    assert "Second check: they span every null-space solution" in source
    assert "Every null-space vector is a combination" in source
    assert "Third check: the two vectors are independent" in source
    assert "second coordinate: }c_1=0" in source
    assert "third coordinate: }c_2=0" in source


def test_scene_concludes_basis_dimension_and_geometry() -> None:
    source = scene_source()
    assert "Therefore these vectors form a basis for N(A)" in source
    assert "Basis and dimension" in source
    assert r"\dim N(A)=2" in source
    assert "Two independent directions span a plane through the origin in R³." in source
    assert "Polygon(" in source


def test_scene_explains_free_variable_count_and_rank_nullity() -> None:
    source = scene_source()
    assert "Free variables determine null-space dimension" in source
    assert r"\#\text{ free variables}=\#\text{ basis vectors}=\dim N(A)" in source
    assert r"\operatorname{rank}A+\operatorname{nullity}A=3" in source
    assert "A particular solution is not part of a basis for N(A)" in source


def test_first_card_labels_align_to_matrix_columns() -> None:
    source = scene_source()
    assert "variable_labels = self._variable_labels(matrix)" in source
    assert "label.move_to([column.get_center()[0], matrix.get_top()[1] + 0.22, 0])" in source
    assert "display.move_to(LEFT * 3.10 + DOWN * 0.24)" in source


def test_special_solution_helper_returns_direct_vector_references() -> None:
    source = scene_source()
    assert "special_panel, first_vector, second_vector = self._special_solution_panel()" in source
    assert "return VGroup(box, group), first_vector, second_vector" in source
    assert "SurroundingRectangle(first_vector" in source
    assert "SurroundingRectangle(second_vector" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    student_lines = [line for line in scene_source().splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_affected_panels_do_not_repeat_the_scene_heading_inside_the_box() -> None:
    source = scene_source()
    assert 'heading = Text("One special solution for each free variable"' not in source
    assert 'heading = Text("Each special solution must satisfy A s = 0"' not in source
    assert 'heading = Text("Let y = s and z = t"' not in source
    assert 'heading = Text("Suppose a combination gives the zero vector"' not in source
    assert 'heading = Text("The pattern"' not in source


def test_affected_panels_are_lowered_below_the_scene_heading() -> None:
    source = scene_source()
    assert 'special_panel.move_to(DOWN * 0.28)' in source
    assert 'verify_panel = self._verification_panel().move_to(DOWN * 0.28)' in source
    assert 'span_panel = self._span_panel().move_to(DOWN * 0.30)' in source
    assert 'independent_panel = self._independence_panel().move_to(DOWN * 0.30)' in source
    assert 'summary_panel = self._summary_panel().move_to(DOWN * 0.42)' in source


def test_span_panel_retains_parameter_assignment_without_redundant_heading() -> None:
    source = scene_source()
    assert r'MathTex(r"y=s,\qquad z=t,\qquad x=-2s+t", font_size=35, color=YELLOW)' in source


def test_first_and_second_check_headings_are_raised_clear_of_their_boxes() -> None:
    source = scene_source()
    assert 'verify_heading = Text("First check: both vectors lie in N(A)", font_size=29).move_to(UP * 2.04)' in source
    assert 'span_heading = Text("Second check: they span every null-space solution", font_size=29).move_to(UP * 2.04)' in source
