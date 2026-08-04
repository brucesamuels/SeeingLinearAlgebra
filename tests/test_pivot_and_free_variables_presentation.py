from pathlib import Path

SCENE_PATH = Path("scenes/pivot_and_free_variables_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_has_expected_title_and_message() -> None:
    source = scene_source()
    assert "Pivot and Free Variables" in source
    assert "infinite solution set" in source


def test_scene_marks_pivot_and_free_columns() -> None:
    source = scene_source()
    assert "Pivot columns: x and y" in source
    assert "No pivot in the z-column: z is free" in source
    assert "matrix.get_columns()[0]" in source
    assert "matrix.get_columns()[1]" in source
    assert "matrix.get_columns()[2]" in source


def test_scene_presents_both_textbook_and_strang_methods() -> None:
    source = scene_source()
    assert "Method 1: Let the free variable be z = t" in source
    assert "Textbook method" in source
    assert "Parametric vector form" in source
    assert "Method 2: Strang's special-solution viewpoint" in source
    assert "Strang's viewpoint" in source
    assert "Every solution = particular solution + t(special solution)" in source


def test_scene_explicitly_uses_z_zero_and_z_one_cards() -> None:
    source = scene_source()
    assert "Set z = 0" in source
    assert "Set z = 1" in source
    assert "particular solution:\\nset z = 0" in source
    assert "special solution:\\nset z = 1" in source


def test_scene_finishes_with_two_descriptions_one_solution_set() -> None:
    source = scene_source()
    assert "Two descriptions, one solution set" in source
    assert "If there were more free variables" in source


def test_scene_layout_separates_matrix_and_roles_panel() -> None:
    source = scene_source()
    assert "display.move_to(LEFT * 2.95 + DOWN * 0.22)" in source
    assert "roles_panel = self._roles_panel().move_to(RIGHT * 3.25 + DOWN * 0.10)" in source
    assert 'pivot_note = Text("Pivot columns: x and y", font_size=26, color=GREEN).move_to(LEFT * 2.95 + UP * 1.28)' in source
    assert 'free_note = Text("No pivot in the z-column: z is free", font_size=27, color=YELLOW).move_to(' in source
    assert "LEFT * 2.95 + UP * 1.28" in source
    assert "strang_panel = self._strang_panel().move_to(DOWN * 0.58)" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    student_lines = [line for line in scene_source().splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_variable_labels_are_positioned_from_the_matrix_columns() -> None:
    source = scene_source()
    assert "variable_labels = self._variable_labels(matrix)" in source
    assert "label.move_to([column.get_center()[0], matrix.get_top()[1] + 0.22, 0])" in source


def test_scene_removes_method_two_heading_and_raises_card_labels() -> None:
    source = scene_source()
    assert "particular solution:\\nset z = 0" in source
    assert "special solution:\\nset z = 1" in source
    assert "strang_panel[1][1][0], DOWN, buff=0.16" in source
    assert "strang_panel[1][1][1], DOWN, buff=0.16" in source
    assert "FadeOut(strang_heading)" in source
