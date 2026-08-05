from pathlib import Path

SCENE_PATH = Path("scenes/pivoting_pa_lu_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_introduces_zero_pivot_and_pause_to_predict() -> None:
    source = scene_source()
    assert "Pivoting and PA = LU" in source
    assert "A zero pivot stops ordinary elimination" in source
    assert r"\frac{2}{0}\quad\text{is undefined}" in source
    assert r"\det(A)={self._format_number(determinant)}\ne0" in source
    assert "Which row should move to the top?" in source


def test_scene_uses_permutation_matrix_to_swap_rows() -> None:
    source = scene_source()
    assert "Swap rows before eliminating" in source
    assert r"R_1\leftrightarrow R_2" in source
    assert "Applied to the full augmented system, P performs the row exchange" in source
    assert "snapshot.permutation_matrix" in source
    assert "snapshot.permuted_matrix" in source


def test_scene_animates_both_elimination_steps() -> None:
    source = scene_source()
    assert "for step in snapshot.steps:" in source
    assert "Now eliminate beneath the first pivot" in source
    assert "Eliminate beneath the second pivot" in source
    assert "step.operation_tex" in source
    assert "result_matrix.get_rows()[step.target_row]" in source


def test_scene_builds_pa_equals_lu_from_multipliers() -> None:
    source = scene_source()
    assert "Collect the elimination multipliers in L" in source
    assert "snapshot.factorization_tex" in source
    assert r"L_{31}=m_{31}=2,\qquad L_{32}=m_{32}=-3" in source
    assert "P records row exchanges, L records multipliers" in source


def test_scene_verifies_factorization_and_reconstructs_a() -> None:
    source = scene_source()
    assert "Verify PA = LU and recover A" in source
    assert r"LU=PA" in source
    assert r"P^{-1}=P^T=P" in source
    assert "snapshot.reconstruction_tex" in source
    assert 'MathTex(r"P^T", font_size=30, color=YELLOW)' in source
    assert 'MathTex(r"A=P^TLU", font_size=31, color=YELLOW)' in source
    assert "the original matrix is A = P^T L U" not in source


def test_scene_compares_tiny_pivot_with_partial_pivoting() -> None:
    source = scene_source()
    assert "A tiny pivot is legal—but risky" in source
    assert "Keep the tiny pivot" in source
    assert "Use partial pivoting" in source
    assert "snapshot.multiplier_without_pivoting" in source
    assert "snapshot.multiplier_with_pivoting" in source
    assert "snapshot.no_swap_second_entry" in source
    assert "snapshot.pivoted_second_entry" in source
    assert 'MathTex(rf"m=10^{{{large_power}}}"' in source
    assert 'MathTex(rf"m=10^{{-{epsilon_power}}}"' in source
    assert "Large multipliers can magnify roundoff" in source


def test_scene_states_partial_pivoting_algorithm() -> None:
    source = scene_source()
    assert "Partial pivoting chooses the largest available magnitude" in source
    assert "snapshot.partial_pivot_rule_tex" in source
    assert "find the largest magnitude at or below the pivot" in source
    assert "record the exchange in P" in source
    assert "store the multipliers in L" in source
    assert "reorders the multipliers already stored in L" in source


def test_summary_distinguishes_required_and_recommended_swaps() -> None:
    source = scene_source()
    assert "What pivoting changes—and what it preserves" in source
    assert r"a_{kk}=0" in source
    assert "row swap required" in source
    assert r"|a_{kk}|\ \text{very small}" in source
    assert "row swap usually safer" in source
    assert "Pivoting reorders equations; it does not change the solutions" in source


def test_scene_uses_direct_result_matrix_reference() -> None:
    source = scene_source()
    assert "step_panel, result_matrix = self._elimination_step_panel(step)" in source
    assert "return self._boxed(group), after" in source
    assert "step_panel[" not in source


def test_explanatory_text_uses_consistent_size_and_down_only_fit() -> None:
    source = scene_source()
    assert "EXPLANATION_FONT_SIZE = 21" in source
    assert "def _fit_down_only" in source
    assert "if mobject.width > max_width" in source
    assert "mobject.scale_to_fit_width(max_width)" in source


def test_algorithm_panel_is_positioned_below_heading_with_safe_gap() -> None:
    source = scene_source()
    assert "algorithm_panel.next_to(algorithm_heading, DOWN, buff=0.30)" in source


def test_scene_uses_deliberate_transition_timings() -> None:
    source = scene_source()
    assert "TRANSITION = 2.20" in source
    assert "HIGHLIGHT = 1.35" in source
    assert "self.play(Write(title), FadeIn(subtitle), run_time=2.4)" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    source = scene_source()
    student_lines = [line for line in source.splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_scene_class_and_file_names_match_cp124() -> None:
    source = scene_source()
    assert "class PivotingPALUPresentation(Scene)" in source


def test_cp124_scripts_export_repository_on_pythonpath() -> None:
    render_source = Path("scripts/render_cp124_pivoting_pa_lu.zsh").read_text(encoding="utf-8")
    check_source = Path("scripts/check_cp124_pivoting_pa_lu.zsh").read_text(encoding="utf-8")
    expected = 'export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"'
    assert expected in render_source
    assert expected in check_source


def test_scene_imports_numpy_for_runtime_matrix_verification() -> None:
    source = scene_source()
    assert "import numpy as np" in source
    assert "np.matmul(l_values, u_values)" in source
