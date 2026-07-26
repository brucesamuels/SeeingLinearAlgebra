import numpy as np
import pytest

from engine.subspace_test import SubspaceTest


def test_plane_through_origin_passes_subspace_test() -> None:
    snapshot = SubspaceTest().through_origin()
    assert snapshot.contains_origin
    assert snapshot.closed_under_addition
    assert snapshot.closed_under_scaling
    assert snapshot.is_subspace


def test_shifted_plane_fails_all_three_checks() -> None:
    snapshot = SubspaceTest().shifted()
    assert not snapshot.contains_origin
    assert not snapshot.closed_under_addition
    assert not snapshot.closed_under_scaling
    assert not snapshot.is_subspace


def test_shifted_sum_and_scaled_point_leave_plane() -> None:
    model = SubspaceTest()
    snapshot = model.shifted(scale=2.0)
    assert snapshot.sum_point[2] == pytest.approx(2.4)
    assert snapshot.scaled_point[2] == pytest.approx(2.4)
    assert snapshot.offset[2] == pytest.approx(1.2)


def test_plane_corners_are_coplanar_and_read_only() -> None:
    model = SubspaceTest()
    corners = model.plane_corners([0, 0, 1.2])
    assert np.allclose(corners[:, 2], 1.2)
    assert not corners.flags.writeable


def test_directions_must_be_independent() -> None:
    with pytest.raises(ValueError):
        SubspaceTest(direction_u=[1, 0, 0], direction_v=[2, 0, 0])
