from __future__ import annotations

import numpy as np
import pytest
from manim import NumberPlane

from engine.manim_vector_to_origin_display import ManimVectorToOriginDisplay
from engine.vector_to_origin_translation import VectorToOriginTranslation


def _display() -> tuple[ManimVectorToOriginDisplay, VectorToOriginTranslation]:
    path = VectorToOriginTranslation([2.0, 1.0], [5.0, 3.0])
    plane = NumberPlane(x_range=[-1, 6, 1], y_range=[-1, 4, 1])
    return ManimVectorToOriginDisplay(path.snapshot(0.0), plane), path


def test_display_owns_arrow_points_labels_and_formula() -> None:
    display, _ = _display()

    assert tuple(display.mobject) == (
        display.arrow,
        display.tail_dot,
        display.tip_dot,
        display.tail_label,
        display.tip_label,
        display.formula,
    )


def test_initial_sources_include_endpoint_coordinates_and_subtraction() -> None:
    display, _ = _display()

    assert "initial" in display.tail_label_source
    assert "2" in display.tail_label_source and "1" in display.tail_label_source
    assert "terminal" in display.tip_label_source
    assert "5" in display.tip_label_source and "3" in display.tip_label_source
    assert r"\mathbf{v}" in display.formula_source
    assert r"\Delta_{0}" in display.formula_source


def test_update_moves_existing_objects_and_updates_sources() -> None:
    display, path = _display()
    identities = tuple(id(mobject) for mobject in display.mobject)

    display.update_from_snapshot(path.snapshot(1.0))

    assert tuple(id(mobject) for mobject in display.mobject) == identities
    assert "0" in display.tail_label_source
    assert "3" in display.tip_label_source and "2" in display.tip_label_source
    assert r"\Delta_{1}" in display.formula_source
    assert np.allclose(display.snapshot.current_initial_point, [0.0, 0.0])


def test_display_rejects_non_two_dimensional_snapshot() -> None:
    path = VectorToOriginTranslation([1.0, 2.0, 3.0], [2.0, 4.0, 6.0])

    with pytest.raises(ValueError):
        ManimVectorToOriginDisplay(path.snapshot(0.0), NumberPlane())


def test_display_rejects_update_for_different_vector() -> None:
    display, _ = _display()
    other = VectorToOriginTranslation([2.0, 1.0], [6.0, 3.0])

    with pytest.raises(ValueError):
        display.update_from_snapshot(other.snapshot(0.5))


def test_update_uses_persistent_decimal_readouts() -> None:
    import inspect

    source = inspect.getsource(ManimVectorToOriginDisplay.update_from_snapshot)

    assert "set_value" in source
    assert "MathTex(" not in source
    assert ".become(" not in source
