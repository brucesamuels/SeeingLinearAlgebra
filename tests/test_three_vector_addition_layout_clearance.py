from __future__ import annotations

import inspect

from scenes.three_vector_addition_presentation import ThreeVectorAdditionPresentation


def test_three_vector_scene_is_lowered_in_projected_vertical_directions() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert "axes.shift([-2.20, -1.85, -1.20])" in source
