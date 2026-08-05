from pathlib import Path

SCENE_PATH = Path("scenes/gauss_jordan_inverse_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_introduces_inverse_as_multiple_right_hand_sides() -> None:
    source = scene_source()
    assert "Inverse by Gauss-Jordan Elimination" in source
    assert "The inverse solves three systems at once" in source
    assert r"AX=I" in source
    assert r"A\mathbf{x}_1=\mathbf{e}_1" in source
    assert "The solution matrix X is precisely the inverse of A." in source


def test_scene_places_identity_beside_a_and_animates_four_steps() -> None:
    source = scene_source()
    assert "Place the identity matrix beside A" in source
    assert "snapshot.steps[0]" in source
    assert "for step in snapshot.steps[1:]" in source
    assert "self._step_panel(step)" in source
    assert "The highlighted row changes across the complete augmented matrix." in source
    assert "SurroundingRectangle(block_matrix.get_rows()[step.target_row]" in source


def test_scene_reads_inverse_from_completed_block() -> None:
    source = scene_source()
    assert "When the left side becomes I, the right side is the inverse" in source
    assert r"[A\mid I]\longrightarrow[I\mid A^{-1}]" in source
    assert r"A^{-1}=\begin{bmatrix}" in source
    assert r"\tfrac52" in source
    assert r"-\tfrac32" in source
    assert r"\tfrac12" in source


def test_scene_interprets_inverse_columns_as_unit_vector_solutions() -> None:
    source = scene_source()
    assert "Each inverse column solves one unit-vector system" in source
    assert "for index, (column, color) in enumerate" in source
    assert r"A\mathbf{{x}}_{index}=\mathbf{{e}}_{index}" in source
    assert "Reading the inverse by columns solves all three unit-vector systems." in source


def test_scene_verifies_both_inverse_products() -> None:
    source = scene_source()
    assert "Verify the inverse on the right" in source
    assert r"AA^{-1}=I" in source
    assert "Verify the inverse on the left" in source
    assert r"A^{-1}A=I" in source
    assert "The computed matrix works on both sides of A." in source


def test_scene_connects_inverse_to_elementary_matrix_product() -> None:
    source = scene_source()
    assert "The right half records the entire row-reduction product" in source
    assert r"E_4E_3E_2E_1[A\mid I]" in source
    assert r"A^{-1}=E_4E_3E_2E_1" in source
    assert "The same row operations that turn A into I turn I into the inverse." in source


def test_scene_summarizes_algorithm_and_previews_noninvertibility() -> None:
    source = scene_source()
    assert "Gauss-Jordan inversion is AX=B with B=I" in source
    assert "1. Augment A with the identity matrix." in source
    assert "2. Row-reduce the left side all the way to I." in source
    assert "3. Read A inverse from the right side." in source
    assert r"\text{A pivot in every column}\iff A^{-1}\text{ exists}" in source
    assert "If the left side cannot become I, the matrix is not invertible." in source


def test_scene_uses_direct_matrix_references_and_no_nested_panel_indexes() -> None:
    source = scene_source()
    assert "next_panel, block_matrix = self._step_panel(first_step)" in source
    assert "step_panel, block_matrix = self._step_panel(step)" in source
    assert "return self._boxed(group), matrix" in source
    assert "next_panel[" not in source


def test_fraction_matrices_receive_extra_vertical_spacing() -> None:
    source = scene_source()
    assert 'has_fraction = any("\\\\tfrac" in entry' in source
    assert "v_buff = 1.02 if has_fraction else 0.68" in source
    assert r'return rf"{sign}\tfrac' in source


def test_explanatory_text_uses_consistent_size_and_down_only_fit() -> None:
    source = scene_source()
    assert "EXPLANATION_FONT_SIZE = 21" in source
    assert "def _fit_down_only" in source
    assert "if mobject.width > max_width" in source
    assert "mobject.scale_to_fit_width(max_width)" in source


def test_scene_uses_deliberate_transition_timings() -> None:
    source = scene_source()
    assert "TRANSITION = 2.20" in source
    assert "HIGHLIGHT = 1.35" in source
    assert "self.play(Write(title), FadeIn(subtitle), run_time=2.4)" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    source = scene_source()
    student_lines = [line for line in source.splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_scene_class_and_file_names_match_cp122() -> None:
    source = scene_source()
    assert "class GaussJordanInversePresentation(Scene)" in source


def test_multiple_rhs_latex_has_spaces_after_qquad_boundaries() -> None:
    source = scene_source()
    assert '\\qquad"' not in source
    assert r'\qquad "' in source
    assert r'X=\begin{bmatrix}\mathbf{x}_1&\mathbf{x}_2&\mathbf{x}_3\end{bmatrix},\qquad ' in source
    assert r'A\mathbf{x}_1=\mathbf{e}_1,\qquad ' in source
    assert r'A\mathbf{x}_2=\mathbf{e}_2,\qquad ' in source
