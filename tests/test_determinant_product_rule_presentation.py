from pathlib import Path

SCENE = Path("scenes/determinant_product_rule_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantProductRulePresentation(Scene):" in source()


def test_scene_states_theorem_and_promises_proof() -> None:
    text = source()
    assert "What is det(AB)?" in text
    assert "We will prove why the determinant factors multiply." in text
    assert "theorem_tex()" in text


def test_scene_proves_elementary_matrix_case() -> None:
    text = source()
    assert "First let the left factor E be elementary" in text
    assert "elementary_cases()" in text
    assert "elementary_conclusion_tex()" in text
    assert "one row operation" in text


def test_scene_rebuilds_invertible_case_as_three_cards() -> None:
    text = source()
    assert "self.show_invertible_setup(banner)" in text
    assert "self.show_invertible_peel_off(banner)" in text
    assert "self.show_invertible_recognition(banner)" in text
    assert "Now suppose A is invertible" in text
    assert 'title.move_to(np.array([0.0, 2.32, 0.0]))' in text
    assert "Peel off the elementary matrices" in text
    assert "Recognize the product as det(A)" in text
    assert "Each E_i is one elementary row operation." in text
    assert 'MathTex(r"\\det(AB)=\\det(E_mE_{m-1}\\cdots E_1B)", font_size=29, color=WHITE)' in text
    assert 'MathTex(lines[2], font_size=38, color=GREEN)' in text


def test_scene_handles_singular_case() -> None:
    text = source()
    assert "What if A is singular?" in text
    assert "singular_case_tex()" in text


def test_scene_includes_consequences_and_takeaway() -> None:
    text = source()
    assert "Consequences of multiplicativity" in text
    assert "inverse_consequence_tex()" in text
    assert "power_consequence_tex()" in text
    assert "many_factors_tex()" in text
    assert "The big takeaway" in text


def test_scene_uses_safe_clear_pattern() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_scene_uses_refined_elementary_case_layout() -> None:
    text = source()
    assert 'title = self.stage_title("First let the left factor E be elementary", size=28)' in text
    assert 'MathTex(operation, font_size=24, color=WHITE)' in text
    assert 'rows.scale_to_fit_width(10.3)' in text
    assert 'conclusion = MathTex(elementary_conclusion_tex(), font_size=34, color=YELLOW)' in text


def test_scene_refines_singular_case_layout() -> None:
    text = source()
    assert 'title = self.stage_title("What if A is singular?", size=26)' in text
    assert 'MathTex(lines[0], font_size=27, color=WHITE)' in text
    assert 'body.scale_to_fit_width(9.9)' in text
    assert 'body.move_to(np.array([0.0, -0.45, 0.0]))' in text


def test_scene_refines_consequences_and_takeaway_layouts() -> None:
    text = source()
    assert 'title = self.stage_title("Consequences of multiplicativity", size=26)' in text
    assert 'inverse_block = VGroup(' in text
    assert 'powers_block = VGroup(' in text
    assert 'many_block = VGroup(' in text
    assert 'title = self.stage_title("The big takeaway", size=28)' in text
    assert 'theorem = MathTex(theorem_tex(), font_size=42, color=GREEN)' in text
