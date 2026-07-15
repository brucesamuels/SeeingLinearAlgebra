"""Focused tests for Checkpoint 30 post-sweep reflection integration."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import VGroup  # noqa: E402

from engine.manim_equation_callout import ManimEquationCallout  # noqa: E402
from engine.manim_linear_combination_labels import (  # noqa: E402
    ManimLinearCombinationLabels,
)
from engine.manim_linear_combination_presentation import (  # noqa: E402
    ManimLinearCombinationPresentation,
)
from scenes.linear_combination_presentation_smoke import (  # noqa: E402
    SMOKE_END_COEFFICIENTS,
    SMOKE_REFLECTION_CAPTION,
    SMOKE_REFLECTION_EQUATION,
    SMOKE_VECTORS,
    build_linear_combination_equation_callout,
    build_linear_combination_post_sweep_reflection_callout,
    build_linear_combination_presentation_smoke_pipeline,
    build_linear_combination_prediction_prompt,
    update_labeled_linear_combination_presentation,
)


def _mobject_geometry(
    callout: ManimEquationCallout,
) -> tuple[np.ndarray, ...]:
    """Return fixed public geometry used to detect accidental movement."""

    return (
        callout.get_center().copy(),
        callout.equation_mobject.get_center().copy(),
        callout.panel_mobject.get_center().copy(),
        np.array([callout.width, callout.height], dtype=float),
    )


def test_reflection_states_the_span_conclusion_concisely() -> None:
    assert isinstance(SMOKE_REFLECTION_EQUATION, str)
    assert r"\operatorname{span}" in SMOKE_REFLECTION_EQUATION
    assert r"\mathbf{w}" in SMOKE_REFLECTION_EQUATION
    assert r"\mathbf{u}" in SMOKE_REFLECTION_EQUATION
    assert r"\mathbf{v}" in SMOKE_REFLECTION_EQUATION

    assert isinstance(SMOKE_REFLECTION_CAPTION, str)
    assert SMOKE_REFLECTION_CAPTION.strip()

    normalized_caption = SMOKE_REFLECTION_CAPTION.casefold()
    assert "coefficients" in normalized_caption
    assert "resultant" in normalized_caption
    assert "span" in normalized_caption


def test_reflection_builder_returns_the_proven_callout_component() -> None:
    reflection = build_linear_combination_post_sweep_reflection_callout()

    assert isinstance(reflection, ManimEquationCallout)
    assert reflection.equation_source == SMOKE_REFLECTION_EQUATION
    assert reflection.caption_text == SMOKE_REFLECTION_CAPTION
    assert reflection.caption_mobject is not None


def test_reflection_is_placed_in_the_upper_left_region() -> None:
    reflection = build_linear_combination_post_sweep_reflection_callout()
    center = reflection.get_center()

    assert center.shape == (3,)
    assert np.all(np.isfinite(center))
    assert center[0] < 0.0
    assert center[1] > 0.0


def test_reflection_is_distinct_from_existing_fixed_and_moving_components() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial = pipeline.display_path.snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    labels = ManimLinearCombinationLabels(initial)
    moving_group = VGroup(presentation, labels)

    equation_callout = build_linear_combination_equation_callout()
    prediction_prompt = build_linear_combination_prediction_prompt()
    reflection = build_linear_combination_post_sweep_reflection_callout()

    assert tuple(moving_group.submobjects) == (presentation, labels)
    assert reflection not in moving_group.submobjects
    assert reflection is not equation_callout
    assert reflection is not prediction_prompt
    assert reflection not in equation_callout.submobjects
    assert reflection not in prediction_prompt.submobjects


def test_moving_snapshot_updates_leave_the_reflection_unchanged() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial = pipeline.display_path.snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    labels = ManimLinearCombinationLabels(initial)
    reflection = build_linear_combination_post_sweep_reflection_callout()

    identities = (
        id(reflection),
        id(reflection.equation_mobject),
        id(reflection.caption_mobject),
        id(reflection.panel_mobject),
    )
    before = _mobject_geometry(reflection)

    update_labeled_linear_combination_presentation(
        presentation,
        labels,
        pipeline.display_path,
        1.0,
    )

    assert (
        id(reflection),
        id(reflection.equation_mobject),
        id(reflection.caption_mobject),
        id(reflection.panel_mobject),
    ) == identities

    after = _mobject_geometry(reflection)
    for actual, expected in zip(after, before, strict=True):
        np.testing.assert_allclose(actual, expected)


def test_final_snapshot_matches_the_displayed_linear_combination() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    final = pipeline.display_path.snapshot(1.0).linear_combination_snapshot

    expected_result = SMOKE_END_COEFFICIENTS @ SMOKE_VECTORS
    np.testing.assert_allclose(final.coefficients, SMOKE_END_COEFFICIENTS)
    np.testing.assert_allclose(final.result, expected_result)
    np.testing.assert_allclose(final.partial_sums[-1], final.result)
