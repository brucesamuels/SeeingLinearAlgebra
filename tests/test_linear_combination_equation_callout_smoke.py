"""Focused tests for Checkpoint 28 equation-callout integration."""

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
    SMOKE_EQUATION,
    SMOKE_EQUATION_CAPTION,
    SMOKE_RESULTANT_LABEL,
    SMOKE_TERM_LABELS,
    build_linear_combination_equation_callout,
    build_linear_combination_presentation_smoke_pipeline,
    update_labeled_linear_combination_presentation,
)


def _mobject_geometry(mobject: ManimEquationCallout) -> tuple[np.ndarray, ...]:
    """Return fixed public geometry used to detect accidental movement."""

    return (
        mobject.get_center().copy(),
        mobject.equation_mobject.get_center().copy(),
        mobject.panel_mobject.get_center().copy(),
        np.array([mobject.width, mobject.height], dtype=float),
    )


def test_smoke_equation_matches_the_displayed_segment_labels() -> None:
    expected = (
        rf"{SMOKE_RESULTANT_LABEL}="
        rf"{SMOKE_TERM_LABELS[0]}+{SMOKE_TERM_LABELS[1]}"
    )

    assert SMOKE_EQUATION == expected
    assert isinstance(SMOKE_EQUATION_CAPTION, str)
    assert SMOKE_EQUATION_CAPTION.strip()


def test_callout_builder_returns_the_proven_component() -> None:
    callout = build_linear_combination_equation_callout()

    assert isinstance(callout, ManimEquationCallout)
    assert callout.equation_source == SMOKE_EQUATION
    assert callout.caption_text == SMOKE_EQUATION_CAPTION
    assert callout.caption_mobject is not None


def test_callout_builder_places_the_component_in_the_lower_left_region() -> None:
    callout = build_linear_combination_equation_callout()

    assert callout.get_center()[0] < 0.0
    assert callout.get_center()[1] < 0.0


def test_callout_remains_outside_the_tracker_driven_moving_group() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial = pipeline.display_path.snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    labels = ManimLinearCombinationLabels(initial)
    callout = build_linear_combination_equation_callout()

    moving_group = VGroup(presentation, labels)

    assert tuple(moving_group.submobjects) == (presentation, labels)
    assert callout not in moving_group.submobjects


def test_moving_snapshot_updates_leave_the_callout_unchanged() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial = pipeline.display_path.snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    labels = ManimLinearCombinationLabels(initial)
    callout = build_linear_combination_equation_callout()

    identities = (
        id(callout),
        id(callout.equation_mobject),
        id(callout.caption_mobject),
        id(callout.panel_mobject),
    )
    before = _mobject_geometry(callout)

    update_labeled_linear_combination_presentation(
        presentation,
        labels,
        pipeline.display_path,
        0.75,
    )

    assert (
        id(callout),
        id(callout.equation_mobject),
        id(callout.caption_mobject),
        id(callout.panel_mobject),
    ) == identities
    after = _mobject_geometry(callout)
    for actual, expected in zip(after, before, strict=True):
        np.testing.assert_allclose(actual, expected)
