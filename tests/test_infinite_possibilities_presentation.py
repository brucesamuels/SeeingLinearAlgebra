from __future__ import annotations

import inspect
from math import isclose

from scenes.infinite_possibilities_presentation import (
    InfinitePossibilitiesPresentation,
)


def test_scene_reuses_existing_linear_combination_engine() -> None:
    source = inspect.getsource(InfinitePossibilitiesPresentation)

    assert "LINEAR_COMBINATION = LinearCombination((U, V))" in source
    assert "CoefficientChoreography(" in source
    assert "self.LINEAR_COMBINATION.snapshot(coefficients)" in source


def test_scene_uses_shared_visual_identity() -> None:
    source = inspect.getsource(InfinitePossibilitiesPresentation)

    assert "ThemedText.lesson_title" in source
    assert "LessonLayout()" in source
    assert "SEEING_LINEAR_ALGEBRA_THEME" in source


def test_scene_moves_from_readable_examples_to_continuous_motion() -> None:
    source = inspect.getsource(InfinitePossibilitiesPresentation.construct)

    assert "Every coefficient pair creates another vector." in source
    assert "Now let the coefficients change continuously." in source
    assert "ValueTracker(0.0)" in source
    assert "always_redraw(" in source
    assert "TracedPath(" in source
    assert "time_tracker.animate.set_value(22.0)" in source
    assert "time_tracker.animate.set_value(52.0)" in source


def test_coefficient_motion_is_smooth_and_expanding() -> None:
    first = InfinitePossibilitiesPresentation.coefficient_pair(0.0)
    later = InfinitePossibilitiesPresentation.coefficient_pair(40.0)

    assert isclose(first[0], 0.0)
    assert abs(later[0]) <= 0.85 + 0.045 * 40.0 + 1.0e-12
    assert abs(later[1]) <= 0.85 + 0.045 * 40.0 + 1.0e-12


def test_scene_uses_motion_to_motivate_the_full_plane_reveal() -> None:
    source = inspect.getsource(InfinitePossibilitiesPresentation.construct)

    assert "Every point on this trail came from one choice of coefficients." in source
    assert "What if a and b can be any real numbers?" in source
    assert '"All of it."' in source
    assert "plane_wash = Rectangle(" in source
    assert "FadeOut(trail)" in source
    assert "FadeIn(plane_wash)" in source


def test_scene_remains_a_standalone_lesson() -> None:
    assert len(InfinitePossibilitiesPresentation.STORY) == 6
