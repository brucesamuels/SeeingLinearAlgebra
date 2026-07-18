from __future__ import annotations

import inspect

from scenes.three_vector_addition_presentation import ThreeVectorAdditionPresentation


def test_three_vector_scene_uses_shorter_narrative_text() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert "Follow u, then v, then w." in source
    assert "narrative.move_to([3.95, 1.70, 0.0])" in source
