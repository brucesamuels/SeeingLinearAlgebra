from pathlib import Path

SCENE_PATH = Path("scenes/multiple_right_hand_sides_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_introduces_multiple_systems_and_ax_equals_b() -> None:
    source = scene_source()
    assert "Multiple Right-Hand Sides" in source
    assert "Several systems share the same coefficient matrix" in source
    assert "Place all right-hand sides into one matrix" in source
    assert r"AX=B" in source
    assert r"X=\begin{bmatrix}\mathbf{x}_1&\mathbf{x}_2\end{bmatrix}" in source


def test_scene_animates_three_block_elimination_steps() -> None:
    source = scene_source()
    assert "snapshot.block_elimination_steps[0]" in source
    assert "for step in snapshot.block_elimination_steps[1:]" in source
    assert "self._block_step_panel(step" in source
    assert "The same row operation updates A and every column of B." in source
    assert "SurroundingRectangle(block_matrix.get_rows()[step.target_row]" in source


def test_scene_compares_repeated_reduction_and_single_block_reduction() -> None:
    source = scene_source()
    assert "Repeated reduction recomputes the same elimination" in source
    assert r"3+3=6\text{ coefficient-matrix elimination steps}" in source
    assert "One block reduction updates every right-hand side" in source
    assert r"[A\mid B]\longrightarrow[U\mid Y]" in source


def test_scene_solves_both_columns_and_verifies_ax_equals_b() -> None:
    source = scene_source()
    assert "Back substitution solves both columns together" in source
    assert r"x_{31}=1,\qquad x_{32}=-1" in source
    assert "Verify every solution column at once" in source
    assert r"A\mathbf{x}_1=\mathbf{b}_1" in source
    assert r"A\mathbf{x}_2=\mathbf{b}_2" in source


def test_scene_presents_lu_reuse_and_two_triangular_solves() -> None:
    source = scene_source()
    assert "LU stores the elimination for reuse" in source
    assert r"A=LU" in source
    assert "forward substitution" in source
    assert "back substitution" in source
    assert "A future right-hand side reuses L and U" in source


def test_scene_includes_exact_operation_count_comparison() -> None:
    source = scene_source()
    assert "Exact count for this 3 by 3 example" in source
    assert r"\text{factor }A:\ 13" in source
    assert r"\text{forward solve per column}:\ 6" in source
    assert r"\text{back solve per column}:\ 9" in source
    assert r"2(13+15)=56" in source
    assert r"13+2(15)=43" in source
    assert r"56-43=13" in source


def test_scene_includes_general_operation_count_formulae() -> None:
    source = scene_source()
    assert "For m right-hand sides, the cubic work should occur once" in source
    assert r"m\left(\frac{2}{3}n^3+2n^2\right)" in source
    assert r"\frac{2}{3}n^3+2mn^2" in source
    assert r"\text{savings}\approx(m-1)\frac{2}{3}n^3" in source


def test_scene_distinguishes_block_reduction_from_reusable_lu() -> None:
    source = scene_source()
    assert "Block reduction and LU reuse perform the same arithmetic" in source
    assert "All columns known now" in source
    assert "Columns may arrive later" in source
    assert "same arithmetic count when all right-hand sides are known" in source
    assert "LU is reusable" in source


def test_explanatory_text_uses_consistent_size_and_down_only_fit() -> None:
    source = scene_source()
    assert "EXPLANATION_FONT_SIZE = 21" in source
    assert "def _fit_down_only" in source
    assert "if mobject.width > max_width" in source
    assert "mobject.scale_to_fit_width(max_width)" in source


def test_panel_helpers_return_direct_matrix_references() -> None:
    source = scene_source()
    assert "next_panel, block_matrix = self._block_step_panel" in source
    assert "return panel, after_matrix" in source
    assert "next_panel[" not in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    source = scene_source()
    student_lines = [line for line in source.splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_scene_and_scripts_use_cp121_names() -> None:
    source = scene_source()
    assert "class MultipleRightHandSidesPresentation(Scene)" in source


def test_scene_uses_slower_deliberate_transition_timings() -> None:
    source = scene_source()
    assert "TRANSITION = 2.25" in source
    assert "HIGHLIGHT = 1.45" in source
    assert "self.play(Write(title), FadeIn(subtitle), run_time=2.4)" in source
    assert "self.play(FadeOut(target_box), run_time=0.90)" in source
    assert "TRANSITION = 1.65" not in source
    assert "HIGHLIGHT = 1.10" not in source
