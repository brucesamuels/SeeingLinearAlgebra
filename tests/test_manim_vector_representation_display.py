from __future__ import annotations

import numpy as np
import pytest
from manim import Arrow, MathTex, Text, VGroup

from engine.manim_vector_representation_display import (
    ManimVectorRepresentationDisplay,
    VectorRepresentationDisplayStyle,
)
from engine.vector_representation import VectorRepresentation
from engine.vector_representation_display import (
    VectorRepresentationDisplayProjector,
)


def display_snapshot(coordinates=(3.0, 4.0), *, zero_annotation="zero vector"):
    return VectorRepresentationDisplayProjector(
        display_dimension=2,
        number_format=".1f",
        zero_annotation=zero_annotation,
    ).project(VectorRepresentation(coordinates).snapshot())


def test_adapter_builds_expected_mobject_types() -> None:
    display = ManimVectorRepresentationDisplay(display_snapshot())
    assert isinstance(display, VGroup)
    assert isinstance(display.arrow, Arrow)
    assert isinstance(display.row_coordinates, MathTex)
    assert isinstance(display.column_coordinates, MathTex)
    assert isinstance(display.magnitude_label, Text)
    assert isinstance(display.dimension_label, Text)
    assert isinstance(display.information_group, VGroup)


def test_arrow_uses_projected_origin_and_endpoint() -> None:
    display = ManimVectorRepresentationDisplay(display_snapshot((2.0, -1.0)))
    np.testing.assert_allclose(display.arrow.get_start(), [0.0, 0.0, 0.0])
    np.testing.assert_allclose(
        display.arrow.get_end(), [2.0, -1.0, 0.0], atol=1e-6
    )


def test_nonzero_vector_has_no_zero_annotation() -> None:
    display = ManimVectorRepresentationDisplay(display_snapshot((1.0, 2.0)))
    assert display.zero_annotation is None
    assert len(display.information_group) == 3


def test_zero_vector_builds_zero_annotation() -> None:
    display = ManimVectorRepresentationDisplay(
        display_snapshot((0.0, 0.0), zero_annotation="the zero vector")
    )
    assert isinstance(display.zero_annotation, Text)
    assert len(display.information_group) == 4


def test_adapter_retains_source_snapshot_identity() -> None:
    snapshot = display_snapshot()
    assert ManimVectorRepresentationDisplay(snapshot).snapshot is snapshot


def test_adapter_has_no_scene_execution_methods() -> None:
    display = ManimVectorRepresentationDisplay(display_snapshot())
    assert not hasattr(display, "play")
    assert not hasattr(display, "wait")
    assert not hasattr(display, "construct")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("coordinate_scale", 0.0),
        ("label_scale", -1.0),
        ("horizontal_gap", 0.0),
        ("vertical_gap", -0.5),
    ],
)
def test_style_rejects_nonpositive_layout_values(field: str, value: float) -> None:
    with pytest.raises(ValueError, match=field):
        VectorRepresentationDisplayStyle(**{field: value})


def test_adapter_rejects_invalid_snapshot_type() -> None:
    with pytest.raises(TypeError, match="VectorRepresentationDisplaySnapshot"):
        ManimVectorRepresentationDisplay(object())  # type: ignore[arg-type]
