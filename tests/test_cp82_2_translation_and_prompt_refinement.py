from pathlib import Path


SCENE = Path("scenes/what_does_a_linear_transformation_do_presentation.py")


def test_pause_and_predict_block_is_shifted_below_title() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "prompt.to_corner(LEFT + UP, buff=0.55)" in source
    assert "prompt.shift(0.55 * DOWN)" in source


def test_translation_updates_objects_without_deforming_grid() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "def update_objects_from_snapshot" in source
    assert 'if name == "Translation":' in source
    assert "tracker.update_objects_from_snapshot(transformed_snapshot)" in source
    assert "tracker.update_from_snapshot(transformed_snapshot)" in source


def test_translation_helper_does_not_update_grid_lines() -> None:
    source = SCENE.read_text(encoding="utf-8")
    helper_start = source.index("    def update_objects_from_snapshot")
    next_class = source.index("\n\n\nclass WhatDoesALinearTransformationDoPresentation", helper_start)
    helper = source[helper_start:next_class]
    assert "grid_lines" not in helper
    assert "origin_dot.move_to" in helper
    assert "figure.set_points_as_corners" in helper
