from __future__ import annotations

import dataclasses

import numpy as np
import pytest

from engine.vector_representation import VectorRepresentation
from engine.vector_representation_display import (
    VectorRepresentationDisplayProjector,
    VectorRepresentationDisplaySnapshot,
)


def test_projector_creates_synchronized_2d_display_snapshot() -> None:
    source = VectorRepresentation([3.0, 4.0]).snapshot()
    projector = VectorRepresentationDisplayProjector(
        display_dimension=2,
        number_format=".1f",
    )

    display = projector.project(source)

    np.testing.assert_allclose(display.projected_origin, [0.0, 0.0])
    np.testing.assert_allclose(display.projected_endpoint, [3.0, 4.0])
    np.testing.assert_allclose(display.projected_vector, [3.0, 4.0])
    assert display.row_text == "[3.0, 4.0]"
    assert display.column_entries == ("3.0", "4.0")
    assert display.magnitude_text == "magnitude = 5.0"
    assert display.dimension_text == "dimension = 2"
    assert display.zero_annotation is None
    assert display.source_dimension == 2
    assert display.display_dimension == 2


def test_projector_preserves_translated_origin() -> None:
    source = VectorRepresentation(
        [2.0, -1.0],
        origin=[5.0, 3.0],
    ).snapshot()

    display = VectorRepresentationDisplayProjector().project(source)

    np.testing.assert_allclose(display.projected_origin, [5.0, 3.0])
    np.testing.assert_allclose(display.projected_endpoint, [7.0, 2.0])
    np.testing.assert_allclose(
        display.projected_endpoint,
        display.projected_origin + display.projected_vector,
    )


def test_projector_can_project_higher_dimension_to_2d() -> None:
    source = VectorRepresentation([1.0, 2.0, 3.0, 4.0]).snapshot()

    display = VectorRepresentationDisplayProjector(
        display_dimension=2
    ).project(source)

    np.testing.assert_allclose(display.projected_vector, [1.0, 2.0])
    assert display.column_entries == ("1.00", "2.00", "3.00", "4.00")
    assert display.source_dimension == 4
    assert display.display_dimension == 2


def test_projector_can_create_3d_display_snapshot() -> None:
    source = VectorRepresentation([1.0, -2.0, 3.0]).snapshot()

    display = VectorRepresentationDisplayProjector(
        display_dimension=3,
        number_format=".0f",
    ).project(source)

    np.testing.assert_allclose(display.projected_vector, [1.0, -2.0, 3.0])
    assert display.row_text == "[1, -2, 3]"


def test_zero_vector_receives_annotation() -> None:
    source = VectorRepresentation([0.0, 0.0]).snapshot()

    display = VectorRepresentationDisplayProjector(
        zero_annotation="the zero vector"
    ).project(source)

    assert display.zero_annotation == "the zero vector"


def test_custom_magnitude_label_is_supported() -> None:
    source = VectorRepresentation([3.0, 4.0]).snapshot()

    display = VectorRepresentationDisplayProjector(
        magnitude_label="length",
        number_format=".2f",
    ).project(source)

    assert display.magnitude_text == "length = 5.00"


@pytest.mark.parametrize("display_dimension", [0, 1, 4])
def test_invalid_display_dimension_is_rejected(
    display_dimension: int,
) -> None:
    with pytest.raises(ValueError, match="2 or 3"):
        VectorRepresentationDisplayProjector(
            display_dimension=display_dimension
        )


def test_invalid_number_format_is_rejected() -> None:
    with pytest.raises(ValueError, match="number_format"):
        VectorRepresentationDisplayProjector(number_format="not-a-format")


def test_source_dimension_must_support_projection() -> None:
    source = VectorRepresentation([2.0, 3.0]).snapshot()
    projector = VectorRepresentationDisplayProjector(display_dimension=3)

    with pytest.raises(ValueError, match="smaller"):
        projector.project(source)


def test_projector_rejects_invalid_snapshot_type() -> None:
    with pytest.raises(TypeError, match="VectorRepresentationSnapshot"):
        VectorRepresentationDisplayProjector().project(object())  # type: ignore[arg-type]


def test_display_snapshot_is_frozen_and_arrays_are_read_only() -> None:
    display = VectorRepresentationDisplayProjector().project(
        VectorRepresentation([1.0, 2.0]).snapshot()
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        display.row_text = "changed"  # type: ignore[misc]

    with pytest.raises(ValueError):
        display.projected_endpoint[0] = 9.0


def test_display_snapshot_validates_endpoint_invariant() -> None:
    with pytest.raises(ValueError, match="projected_endpoint"):
        VectorRepresentationDisplaySnapshot(
            projected_origin=np.array([0.0, 0.0]),
            projected_endpoint=np.array([2.0, 2.0]),
            projected_vector=np.array([1.0, 2.0]),
            row_text="[1.00, 2.00]",
            column_entries=("1.00", "2.00"),
            magnitude_text="magnitude = 2.24",
            dimension_text="dimension = 2",
            zero_annotation=None,
            source_dimension=2,
            display_dimension=2,
        )
