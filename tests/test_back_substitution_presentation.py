from __future__ import annotations

from pathlib import Path


SCENE_PATH = Path("scenes/back_substitution_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_has_expected_title_and_subtitle() -> None:
    source = scene_source()
    assert "Back Substitution" in source
    assert "Start with the bottom row and work upward." in source


def test_scene_solves_for_z_then_y_then_x() -> None:
    source = scene_source()
    assert "Bottom row: solve for z" in source
    assert "Use z = 1 to solve for y" in source
    assert "Use y = 1 and z = 1 to solve for x" in source
    assert "step.equation_tex" in source
    assert "step.solved_tex" in source


def test_scene_uses_a_known_values_panel() -> None:
    source = scene_source()
    assert "Known values" in source
    assert "none yet" in source
    assert "MathTex(step.solved_tex" in source


def test_scene_verifies_solution_in_original_system() -> None:
    source = scene_source()
    assert "Verify the solution in the original system" in source
    assert "Original system" in source
    assert "Check with x = y = z = 1" in source
    assert r'"1+1+1=3"' in source
    assert r'"2(1)-1+1=2"' in source
    assert r'"1+2(1)-1=2"' in source


def test_scene_points_forward_from_echelon_form() -> None:
    source = scene_source()
    assert "Row echelon form from Gaussian elimination" in source
    assert "Back substitution recovers the unique solution (1, 1, 1)." in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    student_lines = [
        line
        for line in scene_source().splitlines()
        if "Text(" in line or "MathTex(" in line
    ]
    assert all("checkpoint" not in line.lower() for line in student_lines)


def test_render_script_exposes_repository_to_python() -> None:
    render_source = Path("scripts/render_cp110_back_substitution.zsh").read_text(encoding="utf-8")
    assert 'PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"' in render_source
    assert "python -m manim" in render_source


def test_verification_screen_removes_known_values_panel_before_checks() -> None:
    source = scene_source()
    assert "FadeOut(current_value_panel)" in source
    assert "FadeIn(current_value_panel)" not in source
    assert r'(x,y,z)=(1,1,1)' in source


def test_bottom_captions_do_not_crossfade_in_same_position() -> None:
    source = scene_source()
    assert "self.play(FadeOut(guidance), run_time=0.5)" in source
    assert "self.play(FadeIn(solve_note), run_time=0.7)" in source
