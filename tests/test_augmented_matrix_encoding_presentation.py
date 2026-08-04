from pathlib import Path


SCENE_PATH = Path("scenes/augmented_matrix_encoding_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_has_expected_title_and_system() -> None:
    source = scene_source()
    assert "From Equations to an Augmented Matrix" in source
    assert "Keep the numbers. Preserve their positions." in source
    assert r"x+y+z&=3" in source
    assert r"2x-y+z&=2" in source
    assert r"x+2y-z&=2" in source


def test_scene_makes_all_coefficients_visible_before_suppressing_symbols() -> None:
    source = scene_source()
    assert "Before suppressing the symbols, write every coefficient." in source
    assert "Make every coefficient visible" in source
    assert '("1", "x", "+", "1", "y", "+", "1", "z", "=", "3")' in source
    assert 'r"(-1)"' in source


def test_scene_moves_each_equation_row_into_the_augmented_matrix() -> None:
    source = scene_source()
    assert "target_rows = matrix.get_rows()" in source
    assert "numeric_sources" in source
    assert "ReplacementTransform(source.copy(), target)" in source
    assert "for equation_row, sources, target_row in zip(" in source
    assert "SurroundingRectangle(" in source


def test_scene_preserves_column_order_with_color_headers() -> None:
    source = scene_source()
    assert "COLUMN_COLORS = (BLUE, GREEN, RED, YELLOW)" in source
    assert 'MathTex("x", color=BLUE' in source
    assert 'MathTex("y", color=GREEN' in source
    assert 'MathTex("z", color=RED' in source
    assert r'MathTex(r"\mathbf{b}", color=YELLOW' in source
    assert "The divider separates coefficients from constants." in source


def test_scene_identifies_A_and_b_blocks() -> None:
    source = scene_source()
    assert "The first three columns are the coefficient matrix A." in source
    assert "The final column is the right-hand side b." in source
    assert "coefficient_entries = VGroup(*columns[:3])" in source
    assert "rhs_entries = columns[3]" in source


def test_scene_explains_zero_placeholder_for_missing_variable() -> None:
    source = scene_source()
    assert "How should x - z = 4 be recorded?" in source
    assert "A missing variable needs a zero placeholder" in source
    assert r"1x+0y+(-1)z=4" in source
    assert "Matrix([[1, 0, -1, 4]]" in source
    assert "The zero keeps y in its column." in source


def test_original_augmented_matrix_is_removed_before_missing_variable_text() -> None:
    source = scene_source()
    assert "FadeOut(matrix_heading)" in source
    assert "FadeOut(matrix.get_brackets())" in source
    assert "FadeOut(matrix.get_entries())" in source
    assert "FadeOut(separator)" in source
    assert "FadeOut(headers)" in source
    assert "matrix_heading.animate.scale" not in source
    assert "matrix_display.animate.scale" not in source
    assert source.index("FadeOut(matrix.get_entries())") < source.index(
        "self.play(FadeIn(missing_example), run_time=0.8)"
    )


def test_scene_hard_clears_matrix_before_conclusion_text() -> None:
    source = scene_source()
    assert "outgoing = [mob for mob in self.mobjects if mob is not title]" in source
    assert "*[FadeOut(mob) for mob in outgoing]" in source
    assert "self.clear()" in source
    assert "self.add(title)" in source
    assert "self.play(FadeIn(conclusion), run_time=0.8)" in source
    assert source.index("self.clear()") < source.index("self.add(title)")
    assert source.index("self.add(title)") < source.index(
        "self.play(FadeIn(conclusion), run_time=0.8)"
    )


def test_scene_concludes_with_preservation_conditions() -> None:
    source = scene_source()
    assert "the variable order is fixed," in source
    assert "every coefficient—including zero—is recorded," in source
    assert "and the final column remains the right-hand side." in source


def test_scene_intentionally_omits_row_operations() -> None:
    lowered = scene_source().lower()
    assert "gaussian elimination" not in lowered
    assert "gauss-jordan" not in lowered
    assert "row operation" not in lowered
    assert "echelon" not in lowered


def test_student_facing_content_fits_and_omits_checkpoint_language() -> None:
    source = scene_source()
    student_strings = [
        line for line in source.splitlines() if "Text(" in line or "MathTex(" in line
    ]
    assert all("checkpoint" not in line.lower() for line in student_strings)
    assert "conclusion.scale_to_fit_width(11.4)" in source
    assert "group.scale_to_fit_width(9.8)" in source
