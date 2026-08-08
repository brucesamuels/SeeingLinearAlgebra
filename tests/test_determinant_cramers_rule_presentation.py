from pathlib import Path

SCENE = Path("scenes/determinant_cramers_rule_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantCramersRulePresentation(Scene):" in source()


def test_scene_begins_from_column_form() -> None:
    text = source()
    assert "Begin with Ax = b, written by columns" in text
    assert "column_equation_tex()" in text
    assert "replacement_definition_tex()" in text


def test_scene_derives_rule_using_determinant_linearity() -> None:
    text = source()
    assert "Why the replacement isolates x_k" in text
    assert "derivation_lines_tex()" in text
    assert "Use linearity in the replaced column." in text
    assert "repeat a column" in text


def test_scene_states_cramers_rule_formally() -> None:
    text = source()
    assert 'self.stage_title("Cramer\'s Rule", size=31)' in text
    assert "theorem_condition_tex()" in text
    assert "theorem_tex()" in text
    assert "definition = MathTex(" in text
    assert "A_k" in text
    assert "replacing column }k" in text
    assert "\\mathbf b" in text


def test_scene_works_complete_three_by_three_example() -> None:
    text = source()
    assert "A 3 x 3 example" in text
    assert "example_system_tex()" in text
    assert "replacement_matrices()" in text
    assert "replacement_determinants()" in text
    assert "example_ratios_tex()" in text


def test_scene_closes_with_solution_and_efficiency_note() -> None:
    text = source()
    assert "solution_vector()" in text
    assert "closing_lines()" in text
    assert "Divide by det(A)" in text



def test_derivation_card_places_title_equations_and_explanation_in_separate_bands() -> None:
    text = source()
    assert "title.move_to(np.array([0.0, 1.80, 0.0]))" in text
    assert 'equations = VGroup(first, second, key).arrange(np.array([0.0, -1.0, 0.0]), buff=0.30)' in text
    assert 'equations.move_to(np.array([0.0, 0.35, 0.0]))' in text
    assert 'key = MathTex(lines[2], font_size=28, color=GREEN)' in text
    assert 'key.scale(first.height / key.height)' in text
    assert 'equations.scale_to_fit_height(2.25)' in text
    assert 'Use linearity in the replaced column.' in text
    assert 'x_k' in text
    assert 'term keeps distinct columns.' in text
    assert 'explanation.move_to(np.array([0.0, -2.05, 0.0]))' in text


def test_solution_card_sequences_work_answer_and_footer() -> None:
    text = source()
    assert 'work.move_to(np.array([0.0, 0.15, 0.0]))' in text
    assert 'self.play(FadeOut(work))' in text
    assert 'answer.move_to(np.array([0.0, 0.35, 0.0]))' in text
    assert 'self.play(FadeOut(answer))' in text
    assert 'footer.move_to(np.array([0.0, -0.35, 0.0]))' in text


def test_content_titles_use_lower_shared_title_band() -> None:
    text = source()
    assert 'TITLE_Y = 2.05' in text
    assert 'def stage_title' in text


def test_scene_uses_safe_clear_pattern() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_example_card_moves_matrix_clear_of_title_and_green_det_line() -> None:
    text = source()
    assert 'title.move_to(np.array([0.0, 1.92, 0.0]))' in text
    assert 'system = MathTex(example_system_tex(), font_size=30, color=WHITE)' in text
    assert 'system.scale_to_fit_width(7.9)' in text
    assert 'system.move_to(np.array([0.0, -0.05, 0.0]))' in text
    assert 'det_line.move_to(np.array([0.0, -1.78, 0.0]))' in text
    assert 'cue.move_to(np.array([0.0, -2.55, 0.0]))' in text
