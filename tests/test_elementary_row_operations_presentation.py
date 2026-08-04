from pathlib import Path


SCENE_PATH = Path("scenes/elementary_row_operations_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_introduces_the_three_elementary_row_operations() -> None:
    source = scene_source()
    assert "Elementary Row Operations" in source
    assert "1. Swap two rows" in source
    assert "2. Scale one row" in source
    assert "3. Replace one row" in source
    assert r"R_1\leftrightarrow R_2" in source
    assert r"R_1\leftarrow 2R_1" in source
    assert r"R_2\leftarrow R_2-2R_1" in source


def test_scene_uses_the_same_system_for_each_operation() -> None:
    source = scene_source()
    assert source.count('self._equation_group((r"x+y=2", r"2x-y=1"))') >= 3
    assert "snapshot.base_augmented" in source
    assert "snapshot.swapped_augmented" in source
    assert "snapshot.scaled_augmented" in source
    assert "snapshot.replaced_augmented" in source


def test_scene_animates_operations_on_equations_and_augmented_matrix() -> None:
    source = scene_source()
    assert "ReplacementTransform(equations, swapped_equations)" in source
    assert "ReplacementTransform(matrix_display, swapped_display)" in source
    assert "ReplacementTransform(equations, scaled_equations)" in source
    assert "ReplacementTransform(matrix_display, scaled_display)" in source
    assert "ReplacementTransform(equations, replaced_equations)" in source
    assert "ReplacementTransform(matrix_display, replaced_display)" in source


def test_scene_highlights_rows_before_each_change() -> None:
    source = scene_source()
    assert "SurroundingRectangle(equations[0]" in source
    assert "SurroundingRectangle(equations[1]" in source
    assert "SurroundingRectangle(matrix.get_rows()[0]" in source
    assert "SurroundingRectangle(matrix.get_rows()[1]" in source
    assert "Create(equation_boxes)" in source
    assert "Create(matrix_boxes)" in source


def test_scene_explains_nonzero_scaling_and_row_replacement() -> None:
    source = scene_source()
    assert "Multiply the entire equation by the same nonzero number." in source
    assert "Reordering the equations changes no solution." in source
    assert r"(2x-y)-2(x+y)" in source
    assert r"=1-2(2)\quad\Longrightarrow\quad -3y=-3" in source
    assert r"-3y=-3" in source


def test_scene_includes_prediction_before_elimination_move() -> None:
    source = scene_source()
    assert "Pause and Predict" in source
    assert "Which multiple of row 1 should be added to row 2 to eliminate x?" in source
    assert source.index("Pause and Predict") < source.index(r"R_2\leftarrow R_2-2R_1")


def test_scene_repeatedly_emphasizes_preserved_solution() -> None:
    source = scene_source()
    assert source.count(r"(x,y)=(1,1)") >= 2
    assert "The common solution is still" in source
    assert "preserves the solution set" in source


def test_scene_concludes_with_general_legal_operations() -> None:
    source = scene_source()
    assert "Three legal moves" in source
    assert r"R_i\leftrightarrow R_j" in source
    assert r"R_i\leftarrow cR_i\qquad(c\ne 0)" in source
    assert r"R_i\leftarrow R_i+cR_j\qquad(i\ne j)" in source


def test_scene_stays_within_cp107_scope() -> None:
    lowered = scene_source().lower()
    assert "gauss-jordan" not in lowered
    assert "echelon form" not in lowered
    assert "elementary matrix" not in lowered
    assert "inverse matrix" not in lowered


def test_matrix_entries_are_formatted_without_decimal_noise() -> None:
    source = scene_source()
    assert "display_values = [" in source
    assert "str(int(round(float(value))))" in source
    assert 'f"{float(value):g}"' in source


def test_row_replacement_arithmetic_stays_beneath_equations_panel() -> None:
    source = scene_source()
    assert 'r"(2x-y)-2(x+y)"' in source
    assert 'r"=1-2(2)\\quad\\Longrightarrow\\quad -3y=-3"' in source
    assert "arithmetic.scale_to_fit_width(5.6)" in source
    assert "arithmetic.move_to(LEFT * 3.45 + DOWN * 1.55)" in source
    assert ").next_to(operation_heading, DOWN, buff=0.28)" not in source


def test_student_facing_content_omits_checkpoint_language_and_fits_frame() -> None:
    source = scene_source()
    student_strings = [
        line for line in source.splitlines() if "Text(" in line or "MathTex(" in line
    ]
    assert all("checkpoint" not in line.lower() for line in student_strings)
    assert "prompt.scale_to_fit_width(11.4)" in source
    assert "arithmetic.scale_to_fit_width(5.6)" in source
    assert "arithmetic.move_to(LEFT * 3.45 + DOWN * 1.55)" in source
    assert "final_group.scale_to_fit_width(11.4)" in source
