from pathlib import Path

SCENE_PATH = Path("scenes/elimination_matrix_multiplication_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_bridges_from_elementary_matrices_to_elimination_product() -> None:
    source = scene_source()
    assert "Elimination as Matrix Multiplication" in source
    assert "Previously, we built the elementary building blocks" in source
    assert r"E_3E_2E_1A=U" in source


def test_scene_uses_three_explicit_elimination_steps() -> None:
    source = scene_source()
    assert "for step in snapshot.elimination_steps" in source
    assert "self._step_heading(step)" in source
    assert "self._step_panel(step)" in source
    assert "Left multiplication replaces one row" in source


def test_step_panel_returns_direct_result_matrix_reference() -> None:
    source = scene_source()
    assert "next_panel, result_matrix = self._step_panel(step)" in source
    assert "return VGroup(box, group), result_matrix" in source
    assert "next_panel[" not in source


def test_scene_composes_elimination_matrices_in_correct_order() -> None:
    source = scene_source()
    assert "Compose the three elimination matrices" in source
    assert "for step in reversed(snapshot.elimination_steps)" in source
    assert "The rightmost matrix acts first" in source


def test_scene_builds_combined_elimination_operator() -> None:
    source = scene_source()
    assert "Multiply them into one elimination operator" in source
    assert r"E=E_3E_2E_1" in source
    assert r"EA=U" in source
    assert "One lower-triangular matrix now performs all three elimination steps at once." in source


def test_scene_reverses_product_and_builds_l() -> None:
    source = scene_source()
    assert "Reverse the product to recover A from U" in source
    assert r"A=E^{-1}U" in source
    assert "The inverse product is lower triangular" in source
    assert r"L=E_1^{-1}E_2^{-1}E_3^{-1}" in source


def test_scene_connects_multipliers_to_entries_of_e_and_l() -> None:
    source = scene_source()
    assert "The multipliers move into L" in source
    assert r"(E_{step.index})_{{{i}{j}}}=-m_{{{i}{j}}}" in source
    assert r"L_{{{i}{j}}}=m_{{{i}{j}}}" in source
    assert "Elimination matrices store negative multipliers" in source


def test_scene_verifies_lu_and_summarizes() -> None:
    source = scene_source()
    assert "Verify the factorization by multiplying L and U" in source
    assert "Multiplying L by U exactly reconstructs the original matrix." in source
    assert "Elimination and factorization are the same process" in source
    assert "LU factorization is Gaussian elimination written as a matrix identity." in source


def test_explanatory_text_uses_consistent_font_size_and_down_only_fit() -> None:
    source = scene_source()
    assert "EXPLANATION_FONT_SIZE = 21" in source
    assert "def _fit_down_only" in source
    assert "if mobject.width > max_width" in source
    assert "mobject.scale_to_fit_width(max_width)" in source


def test_headings_and_panels_are_separated() -> None:
    source = scene_source()
    assert "HEADING_Y = 2.20" in source
    assert ".move_to(DOWN * 0.48)" in source
    assert ".move_to(DOWN * 0.50)" in source
    assert ".move_to(DOWN * 0.52)" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    source = scene_source()
    student_lines = [line for line in source.splitlines() if "Text(" in line or "MathTex(" in line]
    checkpoint_lines = [line for line in student_lines if "checkpoint" in line.lower()]
    assert checkpoint_lines == []


def test_render_class_and_scripts_use_cp120_names() -> None:
    source = scene_source()
    assert "class EliminationMatrixMultiplicationPresentation(Scene)" in source
