from pathlib import Path

SCENE = Path("scenes/determinant_transpose_rule_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantTransposeRulePresentation(Scene):" in source()


def test_scene_constructs_explicit_multi_card_proof() -> None:
    text = source()
    assert 'banner = Text("Determinant of a Transpose", font_size=38)' in text
    assert 'subtitle = MathTex(r"\\det(A^T)=\\det(A)", font_size=31, color=GREY_B)' in text
    for call in (
        "self.show_theorem(banner)",
        "self.show_big_formula(banner)",
        "self.show_apply_to_transpose(banner)",
        "self.show_rewrite_product(banner)",
        "self.show_reindex_sum(banner)",
        "self.show_sign_invariance(banner)",
        "self.show_conclude(banner)",
        "self.show_takeaway(banner)",
    ):
        assert call in text


def test_card_three_uses_true_math_title_and_separate_vertical_zones() -> None:
    text = source()
    assert 'title = MathTex(r"\\text{Apply the formula to }A^T", font_size=27, color=YELLOW)' in text
    assert 'title.move_to(np.array([0.0, 2.38, 0.0]))' in text
    assert 'MathTex(lines[0], font_size=20, color=WHITE)' in text
    assert 'MathTex(lines[1], font_size=20, color=BLUE)' in text
    assert 'body.scale_to_fit_width(9.5)' in text
    assert 'body.move_to(np.array([0.0, -0.18, 0.0]))' in text
    assert 'r"\\text{Because }(A^T)_{i,\\sigma(i)}=a_{\\sigma(i),i}."' in text
    assert 'note.move_to(np.array([0.0, -2.55, 0.0]))' in text
    assert 'stage_title("Apply the formula to A^T"' not in text


def test_card_five_reserves_title_band_above_reindexed_sum() -> None:
    text = source()
    assert 'title = self.stage_title("Reindex the sum", size=22)' in text
    assert 'title.move_to(np.array([0.0, 2.52, 0.0]))' in text
    assert 'MathTex(lines[0], font_size=17, color=WHITE)' in text
    assert 'MathTex(lines[1], font_size=21, color=YELLOW)' in text
    assert 'MathTex(lines[2], font_size=18, color=BLUE)' in text
    assert 'body.scale_to_fit_width(9.4)' in text
    assert 'body.move_to(np.array([0.0, -0.62, 0.0]))' in text


def test_card_six_enlarges_sign_invariance_equation() -> None:
    text = source()
    assert 'title.move_to(np.array([0.0, 2.34, 0.0]))' in text
    assert 'formula = MathTex(lines[0], font_size=44, color=GREEN)' in text
    assert 'formula.move_to(np.array([0.0, 0.62, 0.0]))' in text
    assert 'note.move_to(np.array([0.0, -2.10, 0.0]))' in text


def test_card_seven_separates_heading_from_formula_stack() -> None:
    text = source()
    assert 'title = self.stage_title("Now recognize the Big Formula again", size=21)' in text
    assert 'title.move_to(np.array([0.0, 2.66, 0.0]))' in text
    assert 'MathTex(lines[0], font_size=17, color=WHITE)' in text
    assert 'MathTex(lines[1], font_size=28, color=BLUE)' in text
    assert 'MathTex(lines[2], font_size=36, color=GREEN)' in text
    assert 'body.scale_to_fit_width(9.6)' in text
    assert 'body.move_to(np.array([0.0, -0.72, 0.0]))' in text


def test_final_card_keeps_largest_statement_emphasis() -> None:
    text = source()
    assert 'title = self.stage_title("The big takeaway", size=28)' in text
    assert 'theorem = MathTex(theorem_tex(), font_size=48, color=GREEN)' in text


def test_scene_keeps_proof_content_and_safe_clear_pattern() -> None:
    text = source()
    assert "Start from the Big Formula" in text
    assert "Rewrite the product" in text
    assert "Inverse permutations keep the same sign" in text
    assert "Now recognize the Big Formula again" in text
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text
