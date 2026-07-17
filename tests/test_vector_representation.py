from __future__ import annotations

import dataclasses

import numpy as np
import pytest

from engine.vector_representation import (
    VectorRepresentation,
    VectorRepresentationSnapshot,
)


def test_snapshot_synchronizes_all_views() -> None:
    representation = VectorRepresentation([3.0, 4.0])
    snapshot = representation.snapshot()

    np.testing.assert_allclose(snapshot.coordinates, [3.0, 4.0])
    assert snapshot.row_coordinates == (3.0, 4.0)
    assert snapshot.column_coordinates == ((3.0,), (4.0,))
    np.testing.assert_allclose(snapshot.origin, [0.0, 0.0])
    np.testing.assert_allclose(snapshot.endpoint, [3.0, 4.0])
    assert snapshot.magnitude == pytest.approx(5.0)
    assert snapshot.dimension == 2
    assert not snapshot.is_zero


def test_translation_changes_location_not_vector_coordinates() -> None:
    original = VectorRepresentation([2.0, -1.0])
    translated = original.translated_to([5.0, 3.0])

    np.testing.assert_allclose(
        translated.snapshot().coordinates,
        original.snapshot().coordinates,
    )
    np.testing.assert_allclose(translated.snapshot().origin, [5.0, 3.0])
    np.testing.assert_allclose(translated.snapshot().endpoint, [7.0, 2.0])


def test_scaling_reuses_vector_meaning() -> None:
    representation = VectorRepresentation([2.0, -3.0])

    np.testing.assert_allclose(
        representation.scaled(-0.5).snapshot().coordinates,
        [-1.0, 1.5],
    )


def test_zero_vector_is_detected() -> None:
    snapshot = VectorRepresentation([0.0, 0.0, 0.0]).snapshot()

    assert snapshot.is_zero
    assert snapshot.magnitude == pytest.approx(0.0)
    assert snapshot.dimension == 3


def test_dimension_is_not_restricted_to_two_or_three() -> None:
    snapshot = VectorRepresentation([1.0, 2.0, 3.0, 4.0]).snapshot()

    assert snapshot.dimension == 4
    assert snapshot.column_coordinates == (
        (1.0,),
        (2.0,),
        (3.0,),
        (4.0,),
    )


def test_arrays_are_read_only() -> None:
    snapshot = VectorRepresentation([1.0, 2.0]).snapshot()

    with pytest.raises(ValueError):
        snapshot.coordinates[0] = 9.0

    with pytest.raises(ValueError):
        snapshot.endpoint[0] = 9.0


@pytest.mark.parametrize(
    "coordinates",
    [
        [],
        [[1.0, 2.0]],
        [1.0, np.inf],
        [1.0, np.nan],
    ],
)
def test_invalid_coordinates_are_rejected(coordinates) -> None:
    with pytest.raises(ValueError):
        VectorRepresentation(coordinates)


def test_origin_shape_must_match_vector_shape() -> None:
    with pytest.raises(ValueError, match="origin shape"):
        VectorRepresentation([1.0, 2.0], origin=[0.0, 0.0, 0.0])


def test_snapshot_is_frozen() -> None:
    snapshot = VectorRepresentation([1.0, 2.0]).snapshot()

    with pytest.raises(dataclasses.FrozenInstanceError):
        snapshot.dimension = 7  # type: ignore[misc]


def test_snapshot_validates_endpoint_consistency() -> None:
    with pytest.raises(ValueError, match="endpoint"):
        VectorRepresentationSnapshot(
            coordinates=np.array([1.0, 2.0]),
            row_coordinates=(1.0, 2.0),
            column_coordinates=((1.0,), (2.0,)),
            origin=np.array([0.0, 0.0]),
            endpoint=np.array([2.0, 2.0]),
            magnitude=np.sqrt(5.0),
            dimension=2,
            is_zero=False,
        )
