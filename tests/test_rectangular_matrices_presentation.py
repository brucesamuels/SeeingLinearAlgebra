from __future__ import annotations

from pathlib import Path


SCENE_PATH = Path("scenes/rectangular_matrices_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_class_and_title_match_cp125() -> None:
    source = scene_source()
    assert "class RectangularMatricesPresentation(Scene)" in source
    assert 'Text("Rectangular Matrices and Ax = b"' in source


def test_scene_tracks_dimensions_rows_columns_and_map() -> None:
    source = scene_source()
    assert "snapshot.dimension_equation_tex" in source
    assert "snapshot.map_tex" in source
    assert "snapshot.equation_count_tex" in source
    assert "The dimensions must match" in source


def test_scene_compares_square_tall_and_wide_shapes() -> None:
    source = scene_source()
    assert "The shape of A changes the geometry" in source
    assert "for case in cases:" in source
    assert 'descriptor = Text("overdetermined"' in source
    assert 'descriptor = Text("underdetermined"' in source


def test_scene_uses_column_space_as_the_consistency_condition() -> None:
    source = scene_source()
    assert "Solving means reaching b with a column combination" in source
    assert "snapshot.column_combination_tex" in source
    assert "snapshot.consistency_tex" in source
    assert r"\operatorname{Col}(A)" in source
    assert "reachable_dot" in source
    assert "unreachable_dot" in source


def test_scene_connects_rank_and_nullity_to_geometry() -> None:
    source = scene_source()
    assert "Rank measures the dimension of the reachable set" in source
    assert "snapshot.rank_bound_tex" in source
    assert "snapshot.nullity_tex" in source
    assert "Rank counts independent output directions" in source


def test_tall_panel_distinguishes_reachable_and_unreachable_outputs() -> None:
    source = scene_source()
    assert "Tall matrices: fewer input directions than output directions" in source
    assert "case.geometry_summary" in source
    assert "a reachable b has at most one solution" in source
    assert "tall_inside" in source
    assert "tall_outside" in source


def test_wide_panel_shows_null_space_family_mapping_to_one_output() -> None:
    source = scene_source()
    assert "Wide matrices: extra input directions create a null space" in source
    assert r"\mathbf{x}_p+N(A)" in source
    assert "all three inputs map to the same output" in source
    assert "every b is reachable, but never uniquely" in source


def test_scene_includes_square_full_rank_comparison() -> None:
    source = scene_source()
    assert "Square full-rank matrices can be both onto and one-to-one" in source
    assert r"\text{For every }\mathbf{b}" in source
    assert r"\text{there is exactly one }\mathbf{x}" in source
    assert r"\exists!" not in source


def test_scene_warns_that_shape_alone_does_not_decide_consistency() -> None:
    source = scene_source()
    assert "Shape alone does not decide consistency" in source
    assert "More equations do not automatically mean inconsistency" in source
    assert "More unknowns do not automatically mean consistency" in source
    assert "snapshot.augmented_rank_tex" in source


def test_summary_states_full_rank_possibilities_and_general_rule() -> None:
    source = scene_source()
    assert "Full-rank possibilities for each matrix shape" in source
    assert '"Square": ("onto and one-to-one", "yes", "yes")' in source
    assert '"Tall": ("one-to-one, not onto", "no", "yes")' in source
    assert '"Wide": ("onto, not one-to-one", "yes", "no")' in source
    assert r"\mathbf{b}\in\operatorname{Col}(A)" in source
    assert "rank-deficient matrix reaches less" in source


def test_scene_uses_deliberate_timing_and_down_only_fit() -> None:
    source = scene_source()
    assert "TRANSITION = 2.20" in source
    assert "HIGHLIGHT = 1.35" in source
    assert "READ = 2.65" in source
    assert "EXPLANATION_FONT_SIZE = 21" in source
    assert "def _fit_down_only" in source
    assert "if mobject.width > max_width" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    source = scene_source()
    student_lines = [line for line in source.splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_cp125_scripts_export_repository_on_pythonpath() -> None:
    render_source = Path("scripts/render_cp125_rectangular_matrices.zsh").read_text(encoding="utf-8")
    check_source = Path("scripts/check_cp125_rectangular_matrices.zsh").read_text(encoding="utf-8")
    expected = 'export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"'
    assert expected in render_source
    assert expected in check_source


def test_highlight_boxes_fade_with_their_panels() -> None:
    source = scene_source()
    assert "FadeOut(reachable_box)" in source
    assert "FadeOut(unreachable_box)" in source
    assert "FadeOut(tall_inside_box)" in source
    assert "FadeOut(tall_outside_box)" in source
    assert "FadeOut(input_boxes)" in source
    assert "FadeOut(output_box)" in source


def test_highlight_boxes_are_not_reparented_after_creation() -> None:
    source = scene_source()
    assert "column_panel.add(reachable_box, unreachable_box)" not in source
    assert "tall_panel.add(tall_inside_box, tall_outside_box)" not in source
    assert "wide_panel.add(input_boxes, output_box)" not in source


def test_map_arrows_are_standard_centered_and_explicit() -> None:
    source = scene_source()
    assert "Arrow(" in source
    assert "start = left_box.get_right() + RIGHT * 0.22" in source
    assert "end = right_box.get_left() + LEFT * 0.22" in source
    assert r'MathTex(r"A"' in source
    assert r"\mathbf{x}\mapsto\mathbf{b}" in source
    assert "head_a = Line" not in source
    assert "head_b = Line" not in source
