from __future__ import annotations

from pathlib import Path


SCENE_PATH = Path("scenes/elimination_algorithm_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_has_algorithm_title_and_pivot_cycle() -> None:
    source = scene_source()
    assert "The Gaussian Elimination Algorithm" in source
    assert "Pivot cycle" in source
    assert "Find a nonzero pivot." in source
    assert "Swap it into position if needed." in source
    assert "Clear every entry below it." in source
    assert "Move one row down and one column right." in source
    assert "Repeat until no pivot remains." in source


def test_scene_explains_zero_candidate_and_row_search() -> None:
    source = scene_source()
    assert "The first candidate is zero" in source
    assert "algorithm searches below it" in source
    assert "snapshot.actions[0].label" in source


def test_scene_shrinks_the_active_region() -> None:
    source = scene_source()
    assert "_active_region_box" in source
    assert "start_row=0, start_column=0" in source
    assert "start_row=1, start_column=1" in source
    assert "start_row=2, start_column=2" in source
    assert "Shrink the active region" in source


def test_scene_displays_all_three_row_operations() -> None:
    source = scene_source()
    assert "snapshot.actions[0].label" in source
    assert "snapshot.actions[1].label" in source
    assert "snapshot.actions[2].label" in source


def test_scene_marks_when_no_swap_is_needed() -> None:
    source = scene_source()
    assert "No row swap is needed." in source
    assert "next candidate is already nonzero" in source


def test_scene_marks_final_pivots_and_echelon_form() -> None:
    source = scene_source()
    assert "snapshot.pivot_positions" in source
    assert "PIVOT_COLORS" in source
    assert "stop with row echelon form" in source
    assert "Each cycle creates one pivot" in source


def test_render_script_exports_repository_on_pythonpath() -> None:
    script = Path("scripts/render_cp111_elimination_algorithm.zsh").read_text(encoding="utf-8")
    assert 'PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"' in script
    assert "python -m manim" in script


def test_student_facing_text_omits_checkpoint_terms() -> None:
    source = scene_source()
    student_lines = [line for line in source.splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("cp111" not in line.lower() for line in student_lines)
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_operation_labels_stay_above_matrix_and_clear_of_checklist() -> None:
    source = scene_source()
    assert source.count(".move_to(self._operation_anchor())") == 2
    assert "return LEFT * 2.85 + UP * 1.02" in source
    assert '.move_to(UP * 0.93)' not in source
