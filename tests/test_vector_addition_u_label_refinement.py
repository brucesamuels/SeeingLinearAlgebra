from __future__ import annotations

import inspect

from scenes.vector_addition_presentation import VectorAdditionPresentation


def test_u_label_is_raised_to_clear_the_x_axis() -> None:
    source = inspect.getsource(VectorAdditionPresentation.construct)

    assert (
        "first_label.next_to(first_arrow.get_center(), "
        "direction=[0.0, -1.0, 0.0])" in source
    )
    assert "first_label.shift([0.0, 0.18, 0.0])" in source
