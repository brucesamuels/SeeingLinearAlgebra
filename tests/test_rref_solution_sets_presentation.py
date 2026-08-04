from pathlib import Path

SCENE_PATH = Path("scenes/rref_solution_sets_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_presents_all_three_outcomes() -> None:
    source = scene_source()
    assert "Three Possible Solution Sets" in source
    assert "snapshot.cases[0].name" in source
    assert "snapshot.cases[1]" in source
    assert "snapshot.cases[2]" in source
    assert "ReplacementTransform(case_heading, no_heading)" in source
    assert "ReplacementTransform(no_heading, infinite_heading)" in source


def test_scene_explains_inconsistent_row() -> None:
    source = scene_source()
    assert "What does the last row say?" in source
    assert r'MathTex(r"0=1"' in source
    assert "This equation is impossible." in source


def test_scene_marks_free_variable_and_parameter() -> None:
    source = scene_source()
    assert "infinite_matrix.get_columns()[2]" in source
    assert "z is free" in source
    assert "one parameter generates infinitely many solutions" in source


def test_scene_uses_separated_left_and_right_layout() -> None:
    source = scene_source()
    assert "matrix_display.move_to(LEFT * 3.05 + DOWN * 0.22)" in source
    assert "interpretation = self._interpretation_panel(snapshot.cases[0]).move_to(RIGHT * 3.15 + DOWN * 0.10)" in source


def test_scene_finishes_with_three_summary_cards() -> None:
    source = scene_source()
    assert "What to look for in RREF" in source
    assert "Pivot in every\\nvariable column" in source
    assert "Contradictory row\\n0 = nonzero" in source
    assert "Consistent system\\nwith a free variable" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    student_lines = [line for line in scene_source().splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)
