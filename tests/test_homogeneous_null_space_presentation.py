from pathlib import Path

SCENE_PATH = Path("scenes/homogeneous_null_space_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_introduces_homogeneous_system_and_zero_solution() -> None:
    source = scene_source()
    assert "Homogeneous Systems and the Null Space" in source
    assert "A homogeneous system has the form A x = 0" in source
    assert "The zero vector is always a solution" in source
    assert r"A\mathbf{x}=\mathbf{0}" in source


def test_scene_asks_about_nonzero_solutions_and_uses_free_variable() -> None:
    source = scene_source()
    assert "Can a homogeneous system have a nonzero solution?" in source
    assert "A free variable can produce nonzero solutions" in source
    assert "matrix.get_columns()[2]" in source
    assert "Let the free variable be z = t" in source


def test_scene_uses_strang_special_solution_and_defines_null_space() -> None:
    source = scene_source()
    assert "Strang's special solution" in source
    assert "Set the free variable to 1" in source
    assert r"\mathbf{s}=\begin{bmatrix}-2\\1\\1\end{bmatrix}" in source
    assert "The null space of A" in source
    assert r"N(A)=\{\mathbf{x}:A\mathbf{x}=\mathbf{0}\}" in source
    assert "All multiples of the special solution form a line through the origin." in source


def test_scene_adds_rank_one_example_with_two_free_variables() -> None:
    source = scene_source()
    assert "A rank-1 system with two free variables" in source
    assert "Now there are two free variables" in source
    assert "Choose values for the two free variables" in source
    assert "snapshot.rank_one_scalar_equations_tex" in source
    assert "Choose values for the two free variables" in source
    assert "rank_matrix.get_columns()[1]" in source or "rank_matrix.get_columns()[2]" in source


def test_scene_introduces_particular_and_two_special_solutions_explicitly() -> None:
    source = scene_source()
    assert "Introduce the particular solution explicitly" in source
    assert "One particular solution plus two special solutions" in source
    assert "particular\\nsolution" in source
    assert "special\\nsolution 1" in source
    assert "special\\nsolution 2" in source
    assert r"\begin{bmatrix}3\\0\\0\end{bmatrix}" in source
    assert r"\begin{bmatrix}-2\\1\\0\end{bmatrix}" in source
    assert r"\begin{bmatrix}1\\0\\1\end{bmatrix}" in source


def test_scene_compares_homogeneous_and_nonhomogeneous_structure() -> None:
    source = scene_source()
    assert "Homogeneous vs. nonhomogeneous structure" in source
    assert "Homogeneous: A x = 0" in source
    assert "Nonhomogeneous: A x = b" in source
    assert r"\mathbf{x}=s\mathbf{s}_1+t\mathbf{s}_2" in source
    assert r"\mathbf{x}=\mathbf{x}_p+s\mathbf{s}_1+t\mathbf{s}_2" in source
    assert "The null-space directions stay the same" in source


def test_first_card_labels_are_aligned_to_matrix_columns_and_null_space_layout_is_separated() -> None:
    source = scene_source()
    assert "variable_labels = self._variable_labels(matrix)" in source
    assert "label.move_to([column.get_center()[0], matrix.get_top()[1] + 0.22, 0])" in source
    assert "display.move_to(LEFT * 3.05 + DOWN * 0.28)" in source
    assert "null_panel = self._null_space_panel(snapshot.null_space_span_tex).move_to(RIGHT * 3.20 + UP * 0.18)" in source
    assert "geometry = self._null_space_geometry().move_to(LEFT * 3.00 + DOWN * 0.55)" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    student_lines = [line for line in scene_source().splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_decomposition_highlights_individual_equation_terms() -> None:
    source = scene_source()
    assert "decomposition[1][1][1]" in source
    assert "decomposition[1][1][3]" in source
    assert "decomposition[1][1][5]" in source
    assert "decomposition[1][3]" not in source
    assert "decomposition[1][5]" not in source


def test_decomposition_panel_expands_to_include_label_band() -> None:
    source = scene_source()
    assert 'label_band = Line(LEFT * 4.8, RIGHT * 4.8, stroke_opacity=0).set_height(0.75)' in source
    assert 'group = VGroup(heading, equation, label_band, note).arrange(DOWN, buff=0.34)' in source
    assert 'box = SurroundingRectangle(VGroup(group, particular_label, first_special_label, second_special_label), color=YELLOW, buff=0.18)' in source


def test_decomposition_labels_live_inside_the_panel_and_reveal_sequentially() -> None:
    source = scene_source()
    assert 'for label in decomposition[2:5]:' in source
    assert 'label.set_opacity(0)' in source
    assert 'particular_label = decomposition[2]' in source
    assert 'first_special_label = decomposition[3]' in source
    assert 'second_special_label = decomposition[4]' in source
    assert 'particular_label.animate.set_opacity(1)' in source
    assert 'first_special_label.animate.set_opacity(1)' in source
    assert 'second_special_label.animate.set_opacity(1)' in source
