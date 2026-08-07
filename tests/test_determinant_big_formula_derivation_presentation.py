from pathlib import Path

SCENE = Path("scenes/determinant_big_formula_derivation_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantBigFormulaDerivationPresentation(Scene):" in source()


def test_scene_has_selection_rule_card() -> None:
    text = source()
    assert "From a permutation to a product" in text
    assert "selection_rule_lines()" in text
    assert r"\sigma=(2\,3\,1)" in text
    assert r"a_{12}a_{23}a_{31}" in text


def test_scene_has_positive_pattern_card() -> None:
    text = source()
    assert "Even permutations give the three positive products" in text
    assert "positive_patterns()" in text
    assert "positive_sum_tex()" in text


def test_scene_has_negative_pattern_card() -> None:
    text = source()
    assert "Odd permutations give the three negative products" in text
    assert "negative_patterns()" in text
    assert "negative_sum_tex()" in text


def test_scene_has_assembled_formula_card() -> None:
    text = source()
    assert "Assemble the six terms" in text
    assert "The familiar 3x3 formula is exactly the Big Formula specialized to six permutations." in text
    assert "font_size=33" in text
    assert "final = VGroup(" in text


def test_scene_uses_three_balanced_pattern_cards() -> None:
    text = source()
    assert "x_positions = (-4.1, 0.0, 4.1)" in text
    assert "pattern_card" in text
    assert "font_size=27" in text
    assert "font_size=29" in text


def test_scene_clears_stage_individually() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_scene_final_blue_formula_matches_display_size_of_lines_above() -> None:
    text = source()
    assert 'blue_positive_terms = positive.copy().set_color(BLUE)' in text
    assert 'blue_negative_terms = negative.copy().set_color(BLUE)' in text
    assert 'det_prefix.scale(blue_positive_terms.height / det_prefix.height)' in text
    assert 'first_blue_line = VGroup(det_prefix, blue_positive_terms)' in text
    assert 'second_blue_line = blue_negative_terms' in text


def test_scene_displays_negative_products_with_minus_signs() -> None:
    text = source()
    assert 'prefix="-"' in text
    assert 'display_tex = rf"{prefix}{product_tex}" if prefix else product_tex' in text


def test_scene_blue_lines_reuse_scaled_green_red_geometry() -> None:
    text = source()
    assert 'blue_positive_terms = positive.copy().set_color(BLUE)' in text
    assert 'blue_negative_terms = negative.copy().set_color(BLUE)' in text
    assert 'final.move_to(np.array([0.0, -1.82, 0.0]))' in text
