from pathlib import Path

SCENE_PATH = Path("scenes/gauss_jordan_rref_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_has_expected_titles_and_contrast() -> None:
    source = scene_source()
    assert "Gauss–Jordan Elimination" in source
    assert "Start from row echelon form" in source
    assert "Two ways to finish solving" in source
    assert "Gaussian elimination" in source
    assert "Gauss–Jordan elimination" in source


def test_scene_explicitly_targets_rref_goals() -> None:
    source = scene_source()
    assert "RREF goals" in source
    assert "Scale each pivot to 1" in source
    assert "Clear above the bottom pivot" in source
    assert "Clear above the middle pivot" in source
    assert "Read the solution directly" in source


def test_scene_uses_known_operations_and_direct_readoff() -> None:
    source = scene_source()
    assert r'"R_3\\leftarrow -\\frac{1}{7}R_3"' in source or "step.label_tex" in source
    assert "Direct read-off" in source
    assert "Read the solution directly from RREF" in source
    assert "x=1" in source or "solution_tex" in source


def test_scene_keeps_operation_band_left_of_checklist() -> None:
    source = scene_source()
    assert 'heading = Text("Start from row echelon form", font_size=28).move_to(UP * 1.98)' in source
    assert 'new_heading = Text(step.description, font_size=27).move_to(UP * 1.98)' in source
    assert "display.move_to(LEFT * 2.85 + DOWN * 0.22)" in source
    assert "new_band.move_to(LEFT * 2.85 + UP * 1.28)" in source
    assert "checklist = self._checklist().move_to(RIGHT * 3.3 + DOWN * 0.02)" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    student_lines = [line for line in scene_source().splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_scene_removes_readoff_panel_before_final_comparison() -> None:
    source = scene_source()
    assert "current_checklist = readoff_panel" in source
    assert "FadeOut(current_checklist)" in source
