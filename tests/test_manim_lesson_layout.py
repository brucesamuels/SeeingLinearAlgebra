from __future__ import annotations

import numpy as np
import pytest
from manim import Text, VGroup

from engine.manim_lesson_layout import LessonLayout


def test_layout_exposes_ordered_regions() -> None:
    layout = LessonLayout()

    assert layout.title_y > layout.question_y > layout.content_top_y
    assert layout.footer_y < 0
    np.testing.assert_allclose(layout.title_anchor, [0.0, 3.25, 0.0])
    np.testing.assert_allclose(layout.question_anchor, [0.0, 2.55, 0.0])


def test_layout_places_content_in_upper_left_safe_area() -> None:
    layout = LessonLayout()
    content = VGroup(
        Text("Heading"),
        Text("Line one"),
        Text("Line two"),
    ).arrange([0.0, -1.0, 0.0])

    layout.place_content(content)

    assert content.get_left()[0] == pytest.approx(
        layout.content_left_x,
        abs=1e-6,
    )
    assert content.get_top()[1] == pytest.approx(
        layout.content_top_y,
        abs=1e-6,
    )


def test_layout_scales_overheight_content() -> None:
    layout = LessonLayout(content_max_height=2.0)
    content = VGroup(
        *[Text(f"Line {index}") for index in range(8)]
    ).arrange([0.0, -1.0, 0.0], buff=0.2)

    layout.place_content(content)

    assert content.height <= 2.0 + 1e-6


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("content_max_height", 0.0),
        ("title_scale", 0.0),
        ("question_scale", -1.0),
        ("footer_scale", 0.0),
    ],
)
def test_layout_rejects_invalid_values(field: str, value: float) -> None:
    with pytest.raises(ValueError):
        LessonLayout(**{field: value})
