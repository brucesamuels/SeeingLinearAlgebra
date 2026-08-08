from pathlib import Path

SCENE = Path("scenes/determinant_adjugate_inverse_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantAdjugateInversePresentation(Scene):" in source()




def test_opening_subtitle_uses_mathtax_for_inverse_notation() -> None:
    text = source()
    assert 'subtitle = MathTex(r"\\text{The Adjugate and }A^{-1}", font_size=28, color=GREY_B)' in text

def test_scene_builds_adjugate_from_cofactors() -> None:
    text = source()
    assert "Build the adjugate from cofactors" in text
    assert "cofactor_signs()" in text
    assert "adjugate_definition_tex()" in text
    assert "checkerboard signs" in text


def test_scene_explains_core_identity() -> None:
    text = source()
    assert "Why A adj(A) becomes det(A) I" in text
    assert "identity_tex()" in text
    assert "diagonal_entry_tex()" in text
    assert "off_diagonal_entry_tex()" in text
    assert "two equal rows" in text


def test_scene_derives_inverse_formula() -> None:
    text = source()
    assert "When det(A) is nonzero, divide both sides" in text
    assert "inverse_formula_tex()" in text
    assert "adjugate is 'almost' the inverse" in text


def test_scene_works_a_two_by_two_example() -> None:
    text = source()
    assert "A 2 x 2 example recovers the familiar inverse formula" in text
    assert "example_matrix()" in text
    assert "example_cofactor_matrix()" in text
    assert "example_adjugate()" in text
    assert "example_inverse_formula_tex()" in text
    assert "example_product_tex()" in text


def test_scene_connects_back_to_cramers_rule() -> None:
    text = source()
    assert "This also explains Cramer's Rule" in text
    assert "cramer_connection_tex()" in text


def test_scene_ends_with_takeaway_card() -> None:
    text = source()
    assert "The big takeaway" in text
    assert "closing_lines()" in text
    assert "inverse_formula_tex()" in text


def test_scene_uses_safe_clear_pattern() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_two_by_two_example_card_uses_smaller_separated_layout() -> None:
    text = source()
    assert 'title = self.stage_title("A 2 x 2 example recovers the familiar inverse formula", size=28)' in text
    assert 'title.move_to(np.array([0.0, 2.32, 0.0]))' in text
    assert 'element_to_mobject_config={"font_size": 28}, h_buff=0.72, v_buff=0.55' in text
    assert ').arrange(np.array([1.0, 0.0, 0.0]), buff=0.62)' in text
    assert 'trio.scale_to_fit_width(8.8)' in text
    assert 'trio.move_to(np.array([0.0, 1.00, 0.0]))' in text
    assert 'formula = MathTex(example_inverse_formula_tex(), font_size=27, color=GREEN)' in text
    assert 'formula.scale_to_fit_width(9.4)' in text
    assert 'formula.move_to(np.array([0.0, -0.95, 0.0]))' in text
    assert 'product = MathTex(example_product_tex(), font_size=25, color=WHITE)' in text
    assert 'product.scale_to_fit_width(5.9)' in text
    assert 'product.move_to(np.array([0.0, -2.15, 0.0]))' in text


def test_takeaway_card_raises_yellow_title_for_clearance() -> None:
    text = source()
    assert 'title.move_to(np.array([0.0, 2.38, 0.0]))' in text
    assert 'summary.move_to(np.array([0.0, 0.10, 0.0]))' in text
    assert 'foot.move_to(np.array([0.0, -2.20, 0.0]))' in text
