from __future__ import annotations

from pathlib import Path


SCENE_PATH = Path("scenes/rectangular_system_solvability_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_class_and_title_match_cp126() -> None:
    source = scene_source()
    assert "class RectangularSystemSolvabilityPresentation(Scene)" in source
    assert '"Overdetermined and Underdetermined Systems"' in source


def test_scene_begins_with_general_column_space_and_rank_tests() -> None:
    source = scene_source()
    assert "One criterion governs every matrix shape" in source
    assert "snapshot.common_consistency_tex" in source
    assert "snapshot.augmented_rank_tex" in source
    assert "snapshot.solution_count_tex" in source


def test_overdetermined_geometry_shows_reachable_and_unreachable_outputs() -> None:
    source = scene_source()
    assert "the columns reach only part of the output space" in source
    assert r"\operatorname{Col}(A)" in source
    assert r"\mathbf{b}_{\rm good}" in source
    assert r"\mathbf{b}_{\rm bad}" in source
    assert "inside_box" in source
    assert "outside_box" in source


def test_compatible_overdetermined_system_reduces_to_zero_equals_zero() -> None:
    source = scene_source()
    assert "A compatible right-hand side gives one solution" in source
    assert "over.compatible_augmented_tex" in source
    assert "over.compatible_reduced_tex" in source
    assert r"0=0" in source
    assert r"\begin{bmatrix}2\\-1\end{bmatrix}" in source


def test_incompatible_overdetermined_system_displays_contradiction() -> None:
    source = scene_source()
    assert "An incompatible right-hand side creates a contradiction" in source
    assert "over.incompatible_augmented_tex" in source
    assert "over.incompatible_reduced_tex" in source
    assert r"0=-1" in source
    assert "outside the column space" in source


def test_full_column_rank_rule_distinguishes_none_from_unique() -> None:
    source = scene_source()
    assert "Full column rank gives at most one solution" in source
    assert "over.full_column_rank_tex" in source
    assert "exactly one solution" in source
    assert "no solution" in source
    assert r"\operatorname{rank}(A)\le n<m" in source


def test_underdetermined_example_introduces_free_parameter() -> None:
    source = scene_source()
    assert "Underdetermined: a free variable remains" in source
    assert "under.augmented_tex" in source
    assert r"x+z=2,\qquad y+z=-1" in source
    assert "under.parameter_equations_tex" in source


def test_complete_solution_is_particular_plus_null_space() -> None:
    source = scene_source()
    assert "One particular solution plus the null space" in source
    assert "under.complete_solution_tex" in source
    assert r"\mathbf{x}_p+N(A)" in source
    assert "Every point on the solution line maps to the same output" in source


def test_underdetermined_rule_states_no_or_infinitely_many_never_unique() -> None:
    source = scene_source()
    assert "Every consistent underdetermined system is nonunique" in source
    assert "under.full_row_rank_tex" in source
    assert "every right-hand side is reachable" in source
    assert "no solution or infinitely many" in source
    assert "never exactly one" in source


def test_rank_deficient_wide_counterexample_prevents_false_generalization() -> None:
    source = scene_source()
    assert "Wide does not automatically mean consistent" in source
    assert "under.deficient_augmented_tex" in source
    assert "under.deficient_reduced_tex" in source
    assert r"0=-2" in source
    assert r"\operatorname{rank}(\widetilde A)=1<m=2" in source


def test_summary_preserves_exact_conditions() -> None:
    source = scene_source()
    assert "The solvability conditions" in source
    assert "Full column rank:" in source
    assert "full row rank -> every b" in source
    assert "snapshot.common_consistency_tex" in source
    assert "snapshot.augmented_rank_tex" in source


def test_scene_uses_deliberate_timing_and_standard_centered_arrows() -> None:
    source = scene_source()
    assert "TRANSITION = 2.20" in source
    assert "HIGHLIGHT = 1.35" in source
    assert "READ = 2.75" in source
    assert "EXPLANATION_FONT_SIZE = 21" in source
    assert "Arrow(" in source
    assert "start = left_box.get_right() + RIGHT * 0.22" in source
    assert "end = right_box.get_left() + LEFT * 0.22" in source
    assert r"\mathbf{x}\mapsto\mathbf{b}" in source


def test_scene_uses_mathtex_for_mathematical_statements() -> None:
    source = scene_source()
    assert r"\operatorname{rank}" in source
    assert r"\dim N(A)" in source
    assert r"\notin\operatorname{Col}(A)" in source
    assert r"\exists!" not in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    source = scene_source()
    student_lines = [line for line in source.splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_cp126_scripts_export_repository_on_pythonpath() -> None:
    render_source = Path("scripts/render_cp126_rectangular_system_solvability.zsh").read_text(encoding="utf-8")
    check_source = Path("scripts/check_cp126_rectangular_system_solvability.zsh").read_text(encoding="utf-8")
    expected = 'export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"'
    assert expected in render_source
    assert expected in check_source


def test_overdetermined_panel_raises_heading_and_uses_a_3d_output_space() -> None:
    source = scene_source()
    assert 'over_geometry_heading.move_to(UP * 2.36)' in source
    assert 'over_geometry_panel = self._over_geometry_panel(snapshot.overdetermined).move_to(DOWN * 0.64)' in source
    assert 'def _space_box_3d(self, label_tex: str, width: float, height: float):' in source
    assert r'right = self._space_box_3d(r"\mathbb{R}^3", 4.55, 2.55)' in source



def test_3d_output_space_helper_imports_all_corner_constants() -> None:
    source = scene_source()
    for name in ("UL", "UR", "DL", "DR"):
        assert f"    {name}," in source
    assert "back.get_corner(UL)" in source
    assert "front.get_corner(DR)" in source


def test_overdetermined_domain_box_contains_axes_and_a_representative_input_vector() -> None:
    source = scene_source()
    assert "input_origin = left[0].get_center()" in source
    assert "input_axes = VGroup(" in source
    assert "input_vector = Arrow(" in source
    assert 'input_label = MathTex(r"\\mathbf{x}"' in source
    assert "input_axes," in source
    assert "input_vector," in source
    assert "input_label," in source
