"""Focused tests for Checkpoint 29 pause-and-predict integration."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import Text, VGroup  # noqa: E402

import scenes.linear_combination_presentation_smoke as smoke_scene  # noqa: E402
from engine.manim_linear_combination_labels import (  # noqa: E402
    ManimLinearCombinationLabels,
)
from engine.manim_linear_combination_presentation import (  # noqa: E402
    ManimLinearCombinationPresentation,
)
from scenes.linear_combination_presentation_smoke import (  # noqa: E402
    SMOKE_EQUATION,
    SMOKE_PREDICTION_PROMPT,
    SMOKE_TERM_LABELS,
    build_linear_combination_equation_callout,
    build_linear_combination_prediction_prompt,
    build_linear_combination_presentation_smoke_pipeline,
)


def test_prediction_prompt_is_a_nonempty_tip_to_tail_question() -> None:
    assert isinstance(SMOKE_PREDICTION_PROMPT, str)
    assert SMOKE_PREDICTION_PROMPT.strip()
    assert "second scaled vector" in SMOKE_PREDICTION_PROMPT
    assert "tip-to-tail" in SMOKE_PREDICTION_PROMPT
    assert SMOKE_PREDICTION_PROMPT.rstrip().endswith("?")


def test_prediction_builder_uses_the_established_scene_helper(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    sentinel = VGroup(Text("heading"), Text("question"))

    def fake_pause_and_predict(prompt: str) -> VGroup:
        calls.append(prompt)
        return sentinel

    monkeypatch.setattr(
        smoke_scene,
        "pause_and_predict",
        fake_pause_and_predict,
    )

    result = smoke_scene.build_linear_combination_prediction_prompt()

    assert result is sentinel
    assert calls == [SMOKE_PREDICTION_PROMPT]


def test_prediction_builder_preserves_the_helper_structure() -> None:
    prompt = build_linear_combination_prediction_prompt()

    assert isinstance(prompt, VGroup)
    assert len(prompt.submobjects) == 2

    heading, question = prompt.submobjects
    assert isinstance(heading, Text)
    assert isinstance(question, Text)

    # Manim's public ``Text.text`` representation does not preserve layout
    # whitespace consistently.  Verify the rendered wording while ignoring
    # spaces and line breaks rather than assuming constructor-text storage.
    assert "".join(heading.text.split()) == "PauseandPredict"
    assert "".join(question.text.split()) == "".join(
        SMOKE_PREDICTION_PROMPT.split()
    )


def test_prediction_prompt_is_placed_in_the_upper_left_region() -> None:
    prompt = build_linear_combination_prediction_prompt()
    center = prompt.get_center()

    assert center.shape == (3,)
    assert np.all(np.isfinite(center))
    assert center[0] < 0.0
    assert center[1] > 0.0


def test_prediction_prompt_is_not_part_of_the_moving_family_or_callout() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial = pipeline.display_path.snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    labels = ManimLinearCombinationLabels(initial)
    moving_group = VGroup(presentation, labels)

    prompt = build_linear_combination_prediction_prompt()
    callout = build_linear_combination_equation_callout()

    assert tuple(moving_group.submobjects) == (presentation, labels)
    assert prompt not in moving_group.submobjects
    assert prompt is not callout
    assert prompt not in callout.submobjects


def test_scalar_vector_terms_use_thin_typographic_spacing() -> None:
    assert SMOKE_TERM_LABELS == (
        r"a\,\mathbf{u}",
        r"b\,\mathbf{v}",
    )
    assert SMOKE_EQUATION == (
        r"\mathbf{w}=a\,\mathbf{u}+b\,\mathbf{v}"
    )
