from pathlib import Path

SCENE = Path("scenes/determinant_cofactor_expansion_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantCofactorExpansionPresentation(Scene):" in source()


def test_scene_starts_from_six_term_formula_not_cp136() -> None:
    text = source()
    assert "Start with the six-term determinant formula" in text
    assert "six_term_formula_lines()" in text
    assert "bridge_lines()" in text
    assert "CP136" not in text


def test_scene_groups_by_first_row_entries() -> None:
    text = source()
    assert "Group by the entries in the first row" in text
    assert "grouped_by_first_row_tex()" in text
    assert "The alternating + - + pattern" in text


def test_scene_reveals_three_minor_determinants() -> None:
    text = source()
    assert "Each parenthesis is a 2x2 determinant" in text
    assert "row_one_expansion_tex()" in text
    assert "minor_card" in text
    assert "delete row 1" in text


def test_scene_introduces_checkerboard_and_cofactors() -> None:
    text = source()
    assert "checkerboard signs" in text
    assert "checkerboard_signs()" in text
    assert "minor_definition_tex()" in text
    assert "cofactor_definition_tex()" in text
    assert "sign_origin_tex()" in text
    assert r"C_{11}=+M_{11}" in text
    assert r"C_{12}=-M_{12}" in text


def test_scene_generalizes_to_any_row_or_column() -> None:
    text = source()
    assert "Cofactor expansion" in text
    assert "first_row_cofactor_tex()" in text
    assert "general_row_expansion_tex()" in text
    assert "general_column_expansion_tex()" in text
    assert "works along any row or column" in text


def test_scene_avoids_stale_group_clear_pattern() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_scene_defines_minor_and_explains_negative_signs() -> None:
    text = source()
    assert "minor_definition_tex()" in text
    assert "sign_origin_tex()" in text


def test_scene_first_card_uses_identical_formula_font_size_and_common_scaling() -> None:
    text = source()
    assert 'line1 = MathTex(line1_tex, font_size=35, color=GREEN)' in text
    assert 'line2 = MathTex(line2_tex, font_size=35, color=RED)' in text
    assert "line2.scale(line1.height / line2.height)" not in text
    assert "max_width = max(line1.width, line2.width)" in text
    assert "if max_width > 11.2:" in text
    assert "line1.scale(scale_factor)" in text
    assert "line2.scale(scale_factor)" in text


def test_scene_refines_definition_layout() -> None:
    text = source()
    assert "signs.move_to(np.array([-4.5, 0.15, 0.0]))" in text
    assert "MathTex(minor_definition_tex(), font_size=30, color=WHITE)" in text
    assert "sign_origin_tex()" in text
    assert "These signs are inherited from the permutation signs." in text
    assert "definitions.move_to(np.array([2.1, 0.02, 0.0]))" in text
