from __future__ import annotations

from pathlib import Path


SCENE_PATH = Path("scenes/gaussian_elimination_to_echelon_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_has_expected_title_and_goal() -> None:
    source = scene_source()
    assert "Gaussian Elimination: Reaching Echelon Form" in source
    assert "create zeros below each pivot" in source


def test_scene_uses_all_four_row_operations() -> None:
    source = scene_source()
    assert "snapshot.operations[0].label" in source
    assert "snapshot.operations[1].label" in source
    assert "snapshot.operations[2].label" in source
    assert "snapshot.operations[3].label" in source


def test_scene_highlights_source_and_target_rows() -> None:
    source = scene_source()
    assert "current_matrix.get_rows()[source_row]" in source
    assert "current_matrix.get_rows()[target_row]" in source
    assert "SurroundingRectangle" in source


def test_scene_asks_for_the_cleanest_second_pivot() -> None:
    source = scene_source()
    assert "Pause and Predict" in source
    assert "Which remaining row gives the cleanest second pivot?" in source


def test_scene_identifies_completed_first_pivot_column() -> None:
    source = scene_source()
    assert "The first pivot now has zeros beneath it." in source
    assert "current_matrix.get_columns()[0]" in source


def test_scene_marks_all_three_final_pivots() -> None:
    source = scene_source()
    assert "snapshot.pivot_positions" in source
    assert "PIVOT_COLORS" in source


def test_scene_defines_row_echelon_form() -> None:
    source = scene_source()
    assert "Nonzero rows come first." in source
    assert "Each pivot lies right of the pivot above." in source
    assert "Every entry below a pivot is zero." in source


def test_scene_points_forward_to_back_substitution() -> None:
    source = scene_source()
    assert "Gaussian elimination stops here. Back substitution comes next." in source


def test_scene_carries_each_replacement_heading_forward() -> None:
    source = scene_source()
    assert "current_matrix, current_display, stage_heading, operation_label = self._show_step" in source
    assert "return next_matrix, next_display, new_stage_heading, operation" in source
