from __future__ import annotations

import pytest

from engine.manim_lesson_theme import (
    LessonTheme,
    LessonTiming,
    LessonTypography,
    SEEING_LINEAR_ALGEBRA_THEME,
)


def test_default_theme_exposes_semantic_roles() -> None:
    theme = SEEING_LINEAR_ALGEBRA_THEME

    assert theme.colors.geometry
    assert theme.colors.application
    assert theme.colors.definition
    assert theme.colors.reflection
    assert theme.colors.prediction
    assert theme.timing.quick < theme.timing.reflection


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("lesson_title_scale", 0.0),
        ("body_scale", -1.0),
    ],
)
def test_typography_rejects_nonpositive_scales(
    field: str,
    value: float,
) -> None:
    with pytest.raises(ValueError):
        LessonTypography(**{field: value})


def test_timing_rejects_nonpositive_values() -> None:
    with pytest.raises(ValueError):
        LessonTiming(quick=0.0)


def test_theme_is_composable() -> None:
    theme = LessonTheme(
        typography=LessonTypography(body_scale=0.5),
        timing=LessonTiming(normal=0.7),
    )

    assert theme.typography.body_scale == 0.5
    assert theme.timing.normal == 0.7
