from pathlib import Path

SCENE = Path("scenes/determinant_big_formula_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantBigFormulaPresentation(Scene):" in source()


def test_scene_has_context_banner() -> None:
    text = source()
    assert "Methods of Computation" in text
    assert "The Big Formula" in text


def test_scene_has_overview_card() -> None:
    text = source()
    assert "What does the determinant add up?" in text
    assert "The determinant sums signed products." in text
    assert "n_factorial_terms_statement(3)" in text


def test_scene_has_general_formula_card() -> None:
    text = source()
    assert "The general permutation formula" in text
    assert "big_formula_tex()" in text
    assert r"a_{11}" in text
    assert "big_formula_explanation_lines()" in text


def test_scene_lists_six_three_by_three_terms() -> None:
    text = source()
    assert "For 3x3 there are six permutation terms" in text
    assert "Even permutations: positive" in text
    assert "Odd permutations: negative" in text
    assert "positive_terms_3x3()" in text
    assert "negative_terms_3x3()" in text
    assert "Every term uses one entry from each row and each column." in text


def test_scene_has_familiar_formula_card() -> None:
    text = source()
    assert "The familiar 3x3 determinant formula" in text
    assert "grouped_formula_3x3_lines()" in text
    assert "final_line_1 = MathTex(" in text
    assert "final_line_2 = MathTex(" in text
    assert "The Big Formula explains where the six-term 3x3 rule comes from." in text


def test_scene_clears_stage_individually() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_scene_refines_general_formula_layout() -> None:
    text = source()
    assert 'matrix.move_to(np.array([-4.55, -0.7, 0.0]))' in text
    assert 'bullets.move_to(np.array([2.85, -0.8, 0.0]))' in text


def test_scene_enlarges_sigma_equations() -> None:
    text = source()
    assert 'font_size=30, color=GREEN' in text
    assert 'font_size=30, color=RED' in text
    assert 'positive_group.move_to(np.array([-3.15, 0.0, 0.0]))' in text
    assert 'negative_group.move_to(np.array([3.15, 0.0, 0.0]))' in text


def test_scene_wraps_long_sign_explanation_and_enlarges_sigma_lists() -> None:
    text = source()
    assert 'font_size=30, color=GREEN' in text
    assert 'font_size=30, color=RED' in text
    assert 'positive_group.move_to(np.array([-3.15, 0.0, 0.0]))' in text
    assert 'negative_group.move_to(np.array([3.15, 0.0, 0.0]))' in text


def test_scene_r5_matches_blue_lines_to_grouped_display_width() -> None:
    text = source()
    assert 'final_line_1 = MathTex(' in text
    assert 'final_line_2 = MathTex(' in text
    assert 'final_line_1.scale_to_fit_width(11.4)' in text
    assert 'final_line_2.scale_to_fit_width(11.4)' in text
    assert 'final_formula = VGroup(final_line_1, final_line_2).arrange(' in text
    assert 'np.array([0.0, -1.0, 0.0]), buff=0.10' in text
