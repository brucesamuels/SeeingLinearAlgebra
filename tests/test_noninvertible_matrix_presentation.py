from pathlib import Path

SCENE_PATH = Path("scenes/noninvertible_matrix_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_attempts_gauss_jordan_inversion_and_exposes_warning() -> None:
    source = scene_source()
    assert "Why Some Matrices Are Not Invertible" in source
    assert "Try the same Gauss-Jordan inversion process" in source
    assert "A dependent row creates the warning" in source
    assert "step.explanation" in source
    assert "Can later row operations create a third pivot?" in source


def test_scene_finishes_reduction_and_identifies_missing_pivot() -> None:
    source = scene_source()
    assert "for step in snapshot.steps[1:]" in source
    assert "The left block cannot become the identity" in source
    assert r"\operatorname{rank}(A)=2<3" in source
    assert "The third variable column has no pivot" in source
    assert "failure_matrix.get_columns()[2]" in source


def test_scene_interprets_ax_equals_i_as_three_unit_systems() -> None:
    source = scene_source()
    assert "AX = I requires three unit-vector systems" in source
    assert r"A\mathbf{{x}}_{index}=\mathbf{{e}}_{index}" in source
    assert 'verdict = Text("no solution"' in source
    assert 'verdict = Text("infinitely many solutions"' in source
    assert "No single matrix X can solve all three columns" in source


def test_scene_derives_nonzero_null_space_vector() -> None:
    source = scene_source()
    assert "The missing pivot creates a nonzero null-space vector" in source
    assert r"x-z=0" in source
    assert r"y+z=0" in source
    assert r"\mathbf{x}=t\begin{bmatrix}1\\-1\\1\end{bmatrix}" in source
    assert r"A\begin{bmatrix}1\\-1\\1\end{bmatrix}=\mathbf0" in source


def test_null_space_panel_is_positioned_below_heading_with_safe_gap() -> None:
    source = scene_source()
    assert "null_panel = self._null_space_panel(snapshot.left_rref, snapshot.null_space_tex)" in source
    assert "null_panel.next_to(null_heading, DOWN, buff=0.32)" in source
    assert "snapshot.null_space_tex).move_to(DOWN * 0.55)" not in source


def test_scene_connects_null_vector_to_dependent_columns() -> None:
    source = scene_source()
    assert "The same vector reveals dependent columns" in source
    assert r"\mathbf{c}_1-\mathbf{c}_2+\mathbf{c}_3=\mathbf0" in source
    assert "A nontrivial combination of the columns equals zero" in source


def test_scene_proves_nonzero_null_vector_rules_out_inverse() -> None:
    source = scene_source()
    assert "A nonzero null vector rules out an inverse" in source
    assert r"A\mathbf{v}=\mathbf0" in source
    assert r"\mathbf{v}\ne\mathbf0" in source
    assert r"\mathbf{v}=I\mathbf{v}=A^{-1}A\mathbf{v}=A^{-1}\mathbf0=\mathbf0" in source
    assert "Contradiction: an inverse cannot coexist with a nonzero null vector." in source


def test_scene_summarizes_equivalent_invertibility_tests() -> None:
    source = scene_source()
    assert "Equivalent tests for invertibility" in source
    assert "snapshot.equivalence_tex" in source
    assert "MathTex(lines[0]" in source
    assert "MathTex(lines[1]" in source
    assert "MathTex(lines[2]" in source
    assert "This matrix fails every equivalent invertibility test." in source


def test_scene_uses_direct_matrix_references_without_nested_indexes() -> None:
    source = scene_source()
    assert "next_panel, block_matrix = self._step_panel(first_step)" in source
    assert "next_panel, block_matrix = self._step_panel(step)" in source
    assert "return self._boxed(group), matrix" in source
    assert "next_panel[" not in source


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


def test_scene_class_and_file_names_match_cp123() -> None:
    source = scene_source()
    assert "class NoninvertibleMatrixPresentation(Scene)" in source


def test_cp123_scripts_export_repository_on_pythonpath() -> None:
    render_source = Path("scripts/render_cp123_noninvertible_matrix.zsh").read_text(encoding="utf-8")
    check_source = Path("scripts/check_cp123_noninvertible_matrix.zsh").read_text(encoding="utf-8")
    expected = 'export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"'
    assert expected in render_source
    assert expected in check_source
