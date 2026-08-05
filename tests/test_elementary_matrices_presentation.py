from pathlib import Path

SCENE_PATH = Path("scenes/elementary_matrices_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_defines_elementary_matrix_and_three_operation_types() -> None:
    source = scene_source()
    assert "Elementary Matrices" in source
    assert "Start with the identity matrix" in source
    assert r"\xrightarrow{\text{one row operation}}" in source
    assert "There are three types of elementary matrices" in source
    assert "Interchange" in source
    assert "Scale" in source
    assert "Replace" in source


def test_scene_animates_forward_and_inverse_product_for_every_operation() -> None:
    source = scene_source()
    assert "self._show_forward_and_inverse" in source
    assert "self._product_panel(case)" in source
    assert "self._inverse_product_panel(case)" in source
    assert "The inverse elementary matrix restores the original matrix." in source
    assert "Undo the interchange with the same matrix" in source
    assert "Undo the scaling with the reciprocal factor" in source
    assert "Undo the replacement with the opposite multiple" in source


def test_inverse_product_panel_displays_explicit_matrix_multiplication() -> None:
    source = scene_source()
    assert 'left_label=r"E^{-1}"' in source
    assert 'middle_label="EA"' in source
    assert 'result_label="A"' in source
    assert "case.inverse_matrix" in source
    assert "case.product_matrix" in source
    assert "case.source_matrix" in source


def test_scene_explains_left_multiplication_as_row_combinations() -> None:
    source = scene_source()
    assert "Why the elementary matrix multiplies on the left" in source
    assert "left_multiplication_tex" in source
    assert r"(EA)_{3*}=2R_1+R_3" in source
    assert "Each row of E specifies the linear combination of rows of A" in source


def test_scene_contains_complete_four_step_row_reduction() -> None:
    source = scene_source()
    assert "A complete row reduction" in source
    assert "snapshot.reduction_steps" in source
    assert "Reduction step {step.index}" in source
    assert r"E_{step.index}" in source
    assert r"A_{step.index-1}" in source
    assert r"A_{step.index}" in source
    assert "self._reduction_step_panel(step)" in source


def test_scene_multiplies_elementary_matrices_into_entire_reduction_matrix() -> None:
    source = scene_source()
    assert "The four matrices multiply into one row-reduction matrix" in source
    assert "self._cumulative_products_panel(snapshot)" in source
    assert r"P_4=E_4E_3E_2E_1" in source
    assert "snapshot.cumulative_products" in source
    assert "The complete product reduces A to I" in source
    assert r"PA=I\quad\Longrightarrow\quad P=A^{-1}" in source


def test_scene_animates_reverse_sequence_of_inverse_elementary_matrices() -> None:
    source = scene_source()
    assert "Reverse the reduction with inverse elementary matrices" in source
    assert "snapshot.reverse_steps" in source
    assert "self._reverse_step_heading(reverse_position, original_index)" in source
    assert "self._reverse_step_panel(step)" in source
    assert r"E_4^{-1}\ \to\ E_3^{-1}\ \to\ E_2^{-1}\ \to\ E_1^{-1}" in source


def test_scene_states_forward_and_reverse_factorizations() -> None:
    source = scene_source()
    assert "Forward and reverse factorizations" in source
    assert r"A^{-1}=E_4E_3E_2E_1" in source
    assert r"A=E_1^{-1}E_2^{-1}E_3^{-1}E_4^{-1}" in source
    assert "The inverse of a product reverses the order of the factors." in source


def test_scene_preserves_slow_deliberate_timing() -> None:
    source = scene_source()
    assert "TRANSITION = 1.65" in source
    assert "HIGHLIGHT = 1.15" in source
    assert "READ = 2.2" in source
    assert 'self.play(Write(title), FadeIn(subtitle), run_time=1.9)' in source


def test_scene_headings_and_tall_panels_are_separated() -> None:
    source = scene_source()
    assert "HEADING_Y = 2.18" in source
    assert source.count("move_to(UP * self.HEADING_Y)") >= 10
    assert "self._reduction_overview_panel(snapshot).move_to(DOWN * 0.52)" in source
    assert "self._cumulative_products_panel(snapshot).move_to(DOWN * 0.74)" in source
    assert "self._factorization_panel(snapshot).move_to(DOWN * 0.58)" in source


def test_fraction_formatter_displays_simple_exact_fractions() -> None:
    source = scene_source()
    assert "Fraction(float(value)).limit_denominator(12)" in source
    assert r'return rf"{sign}\tfrac{{{numerator}}}{{{fraction.denominator}}}"' in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    student_lines = [line for line in scene_source().splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_reduction_panels_return_direct_result_matrix_references() -> None:
    source = scene_source()
    assert 'next_panel, result_matrix = self._reduction_step_panel(step)' in source
    assert 'next_panel, result_matrix = self._reverse_step_panel(step)' in source
    assert source.count('return panel, result') == 2
    assert 'next_panel[1][0][4]' not in source


def test_reduction_panels_are_positioned_after_unpacking() -> None:
    source = scene_source()
    assert source.count('next_panel.move_to(DOWN * 0.48)') >= 2


def test_short_explanatory_text_is_not_scaled_up_to_panel_width() -> None:
    source = scene_source()
    assert "EXPLANATION_FONT_SIZE = 21" in source
    assert "Text(explanation, font_size=ElementaryMatricesPresentation.EXPLANATION_FONT_SIZE)" in source
    assert "_shrink_to_fit_width(note, 10.9)" in source
    assert "if mobject.width > max_width:" in source
    assert "note.scale_to_fit_width(10.9)" not in source


def test_fractional_matrix_entries_use_compact_fractions_and_extra_row_spacing() -> None:
    source = scene_source()
    assert 'has_fraction = any(r"\\tfrac" in entry for row in formatted for entry in row)' in source
    assert "v_buff = 1.25 if has_fraction else 0.80" in source
    assert "Matrix(formatted, h_buff=0.95, v_buff=v_buff).scale(scale)" in source
    assert "_matrix_mobject(product, scale=0.40)" in source
    assert "_matrix_mobject(snapshot.reduction_matrix, scale=0.56)" in source


def test_explanatory_copy_uses_one_consistent_font_size() -> None:
    source = scene_source()
    assert source.count("font_size=ElementaryMatricesPresentation.EXPLANATION_FONT_SIZE") >= 6
    assert 'Text(explanation, font_size=21)' not in source


def test_reverse_step_headings_render_matrix_symbols_with_mathex() -> None:
    source = scene_source()
    assert 'prose = Text(f"Reverse step {reverse_position}: apply", font_size=29)' in source
    assert 'symbol = MathTex(rf"E_{{{original_index}}}^{{-1}}", font_size=31, color=RED)' in source
    assert 'VGroup(prose, symbol).arrange(RIGHT, buff=0.12)' in source
    assert 'f"Reverse step {reverse_position}: apply E_{original_index}⁻¹"' not in source


def test_cumulative_product_heading_clears_the_panel_boundary() -> None:
    source = scene_source()
    assert '"The four matrices multiply into one row-reduction matrix",' in source
    assert 'font_size=24,' in source
    assert ').move_to(UP * 2.32)' in source
    assert 'next_heading.scale_to_fit_width(10.8)' in source
    assert 'self._cumulative_products_panel(snapshot).move_to(DOWN * 0.74)' in source
