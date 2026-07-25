import numpy as np
import pytest

from engine.dimension_growth import DimensionGrowth


U = np.array([2.0, 0.2, 0.0])
V = np.array([-0.45, 1.55, 0.0])
W = np.array([0.35, 0.25, 1.65])


def test_snapshot_records_line_plane_and_space_ranks() -> None:
    model = DimensionGrowth(U, V, W)
    snapshot = model.snapshot(0.75)

    assert snapshot.rank_uv == 2
    assert snapshot.rank_uvw == 3
    assert snapshot.volume > 0


def test_translated_plane_moves_only_in_w_direction() -> None:
    model = DimensionGrowth(U, V, W)
    snapshot = model.snapshot(1.25)

    expected = snapshot.plane_corners + 1.25 * W
    np.testing.assert_allclose(snapshot.translated_plane_corners, expected)


def test_line_plane_and_space_points_use_the_expected_coefficients() -> None:
    model = DimensionGrowth(U, V, W)

    np.testing.assert_allclose(model.line_points([0, 2]), [[0, 0, 0], 2 * U])
    np.testing.assert_allclose(model.plane_points([[1, -1]]), [U - V])
    np.testing.assert_allclose(model.space_points([[1, 2, -1]]), [U + 2 * V - W])


def test_third_generator_must_lie_outside_the_existing_plane() -> None:
    with pytest.raises(ValueError, match="outside"):
        DimensionGrowth(U, V, U + V)


def test_snapshot_arrays_are_read_only() -> None:
    snapshot = DimensionGrowth(U, V, W).snapshot(0)

    assert not snapshot.plane_corners.flags.writeable
    assert not snapshot.translated_plane_corners.flags.writeable
