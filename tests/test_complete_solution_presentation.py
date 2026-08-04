from pathlib import Path

SCENE_PATH = Path("scenes/complete_solution_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_introduces_two_part_structure() -> None:
    source = scene_source()
    assert "The Complete Solution" in source
    assert "One particular solution plus every null-space direction." in source
    assert "A complete solution has two parts" in source
    assert r"A\mathbf{x}_p=\mathbf{b}" in source
    assert r"A\mathbf{x}_n=\mathbf{0}" in source
    assert r"\mathbf{x}=\mathbf{x}_p+\mathbf{x}_n" in source


def test_scene_constructs_particular_and_null_space_parts() -> None:
    source = scene_source()
    assert "Choose one particular solution" in source
    assert "Set the free variables y and z equal to zero." in source
    assert r"y=0,\qquad z=0,\qquad x=3" in source
    assert "Add any vector from the associated null space" in source
    assert "The parameters s and t choose any direction within the null space." in source


def test_scene_combines_and_verifies_complete_solution() -> None:
    source = scene_source()
    assert "Combine the two parts" in source
    assert "This is the complete solution" in source
    assert "Why every vector in this form solves A x = b" in source
    assert "Adding a null-space vector does not change the right-hand side." in source
    assert "snapshot.verification_tex" in source


def test_scene_proves_converse_direction() -> None:
    source = scene_source()
    assert "Why every solution must have this form" in source
    assert "Every solution differs from the particular solution by a null-space vector." in source
    assert "snapshot.converse_tex" in source


def test_scene_visualizes_translation_of_null_space() -> None:
    source = scene_source()
    assert "Geometrically: translate the null space by xₚ" in source
    assert "All solutions form an affine plane parallel to N(A), passing through xₚ." in source
    assert "ThreeDAxes(" in source
    assert "Surface(" in source
    assert "lambda u, v: axes.c2p(-2 * u + v, u, v)" in source
    assert "lambda u, v: axes.c2p(3 - 2 * u + v, u, v)" in source
    assert r"\mathbf{x}_p+N(A)" in source


def test_scene_summarizes_complete_solution_pattern() -> None:
    source = scene_source()
    assert "The complete-solution pattern" in source
    assert r"\boxed{\mathbf{x}=\mathbf{x}_p+\mathbf{x}_n}" in source
    assert "1. Find one particular solution." in source
    assert "2. Find a basis for the null space." in source
    assert "3. Add every null-space combination" in source
    assert "Different particular solutions produce the same complete solution set." in source


def test_scene_headings_are_raised_clear_of_boxes() -> None:
    source = scene_source()
    assert 'particular_heading = Text("Choose one particular solution", font_size=30).move_to(UP * 2.04)' in source
    assert 'null_heading = Text("Add any vector from the associated null space", font_size=27).move_to(UP * 2.28)' in source
    assert 'combine_heading = Text("Combine the two parts", font_size=30).move_to(UP * 2.04)' in source
    assert 'verify_heading = Text("Why every vector in this form solves A x = b", font_size=29).move_to(UP * 2.04)' in source
    assert 'converse_heading = Text("Why every solution must have this form", font_size=29).move_to(UP * 2.04)' in source


def test_content_panels_do_not_repeat_scene_headings() -> None:
    source = scene_source()
    assert 'Text("Choose one particular solution"' not in source[source.index("def _particular_panel"):]
    assert 'Text("Add any vector from the associated null space"' not in source[source.index("def _null_part_panel"):]
    assert 'Text("Combine the two parts"' not in source[source.index("def _combine_panel"):]
    assert 'Text("Why every vector in this form solves A x = b"' not in source[source.index("def _verification_panel"):]


def test_first_card_labels_align_to_matrix_columns() -> None:
    source = scene_source()
    assert "variable_labels = self._variable_labels(matrix)" in source
    assert "label.move_to([column.get_center()[0], matrix.get_top()[1] + 0.22, 0])" in source
    assert "display.move_to(LEFT * 3.10 + DOWN * 0.25)" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    student_lines = [line for line in scene_source().splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_geometry_section_uses_fixed_overlay_with_3d_camera_motion() -> None:
    source = scene_source()
    assert 'self.add_fixed_in_frame_mobjects(title, subtitle)' in source
    assert 'self.add_fixed_in_frame_mobjects(geometry_heading, geometry_panel, geometry_footer)' in source
    assert 'self.set_camera_orientation(phi=68 * DEGREES, theta=-52 * DEGREES, zoom=0.92)' in source
    assert 'self.begin_ambient_camera_rotation(rate=0.08)' in source
    assert 'self.remove_fixed_in_frame_mobjects(geometry_heading, geometry_panel, geometry_footer)' in source


def test_combine_panel_has_dedicated_label_band_to_prevent_collisions() -> None:
    source = scene_source()
    assert 'label_band = Line(LEFT * 4.8, RIGHT * 4.8, stroke_opacity=0).set_height(0.60)' in source
    assert 'particular_label = Text("particular\\nsolution", font_size=18, color=BLUE)' in source
    assert 'null_label = Text("null-space\\ncombination", font_size=18, color=GREEN)' in source
    assert 'SurroundingRectangle(VGroup(group, particular_label, null_label), color=YELLOW, buff=0.20)' in source



def test_combine_panel_column_vectors_use_valid_latex_row_separators() -> None:
    source = scene_source()
    assert r'r"\begin{bmatrix}3\\0\\0\end{bmatrix}"' in source
    assert r'r"s\begin{bmatrix}-2\\1\\0\end{bmatrix}+t\begin{bmatrix}1\\0\\1\end{bmatrix}"' in source
    assert r'r"\begin{bmatrix}3\0\0\end{bmatrix}"' not in source
    assert r'r"s\begin{bmatrix}-2\1\0\end{bmatrix}+t\begin{bmatrix}1\0\1\end{bmatrix}"' not in source


def test_null_space_heading_and_panel_are_separated_to_avoid_overlap() -> None:
    source = scene_source()
    assert 'null_heading = Text("Add any vector from the associated null space", font_size=27).move_to(UP * 2.28)' in source
    assert 'null_panel = self._null_part_panel(snapshot.null_space_solution_tex).move_to(DOWN * 0.46)' in source


def test_pause_and_predict_prompt_is_reduced_and_lowered_clear_of_the_box() -> None:
    source = scene_source()
    assert 'Text("Pause and Predict", font_size=25, color=YELLOW)' in source
    assert 'Text("What is A(xₚ + xₙ) when Axₚ = b and Axₙ = 0?", font_size=22)' in source
    assert ').arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.10)' in source


def test_null_heading_is_nudged_up_and_pause_prompt_nudged_down() -> None:
    source = scene_source()
    assert 'null_heading = Text("Add any vector from the associated null space", font_size=27).move_to(UP * 2.28)' in source
    assert ').arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.10)' in source
