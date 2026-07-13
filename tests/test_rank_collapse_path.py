import numpy as np
import pytest

from engine.rank_collapse import RankCollapse
from engine.rank_collapse_path import RankCollapsePath


def test_points_are_transformed_at_requested_progress():
    collapse = RankCollapse(np.diag([3.0, 2.0]), target_rank=1)
    path = RankCollapsePath(collapse, [[1.0, 1.0], [2.0, -1.0]])

    np.testing.assert_allclose(
        path.points_at(0.0),
        [[3.0, 2.0], [6.0, -2.0]],
    )
    np.testing.assert_allclose(
        path.points_at(1.0),
        [[3.0, 0.0], [6.0, 0.0]],
        atol=1e-12,
    )


def test_rectangular_map_preserves_domain_and_codomain_dimensions():
    matrix = np.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0]])
    collapse = RankCollapse(matrix, target_rank=1)
    path = RankCollapsePath(collapse, [[1.0, 1.0, 1.0]])

    assert path.domain_dimension == 3
    assert path.codomain_dimension == 2
    assert path.points_at(0.0).shape == (1, 2)
    np.testing.assert_allclose(path.points_at(0.0), [[1.0, 2.0]])


def test_single_point_input_is_normalized_to_one_row():
    path = RankCollapsePath(RankCollapse(np.eye(4), target_rank=2), [1, 2, 3, 4])

    assert path.point_count == 1
    assert path.input_points.shape == (1, 4)


def test_basis_images_are_matrix_columns_stored_as_rows():
    matrix = np.array([[2.0, 1.0, 0.0], [0.0, 3.0, 4.0]])
    path = RankCollapsePath(RankCollapse(matrix, target_rank=1), np.eye(3))

    np.testing.assert_allclose(path.basis_images_at(0.0), matrix.T, atol=1e-12)


def test_snapshot_is_consistent_with_collapse_and_geometry():
    collapse = RankCollapse(np.diag([5.0, 2.0, 1.0]), target_rank=1)
    points = np.array([[1.0, 1.0, 1.0], [-1.0, 2.0, 0.0]])
    path = RankCollapsePath(collapse, points)
    snapshot = path.snapshot(1.0)

    assert snapshot.progress == 1.0
    assert snapshot.rank == 1
    assert snapshot.nullity == 2
    np.testing.assert_allclose(snapshot.matrix, collapse.matrix_at(1.0))
    np.testing.assert_allclose(snapshot.output_points, path.points_at(1.0))
    np.testing.assert_allclose(snapshot.basis_images, collapse.matrix_at(1.0).T)


def test_snapshots_preserve_requested_order():
    path = RankCollapsePath(
        RankCollapse(np.diag([4.0, 2.0]), target_rank=1),
        [[1.0, 1.0]],
    )

    frames = path.snapshots([1.0, 0.0, 0.5])

    assert tuple(frame.progress for frame in frames) == (1.0, 0.0, 0.5)


def test_trajectory_is_dimension_independent():
    collapse = RankCollapse(np.diag([4.0, 3.0, 2.0, 1.0]), target_rank=2)
    path = RankCollapsePath(collapse, np.eye(4))

    result = path.trajectory([1.0, 1.0, 1.0, 1.0], [0.0, 0.5, 1.0])

    assert result.shape == (3, 4)
    np.testing.assert_allclose(result[0], [4.0, 3.0, 2.0, 1.0])
    np.testing.assert_allclose(result[1], [4.0, 3.0, 1.0, 0.5])
    np.testing.assert_allclose(result[2], [4.0, 3.0, 0.0, 0.0])


def test_empty_trajectory_request_returns_correct_shape():
    path = RankCollapsePath(RankCollapse(np.eye(3), target_rank=1), [[0, 0, 0]])

    assert path.trajectory([1, 2, 3], []).shape == (0, 3)


def test_input_points_are_defensively_copied():
    points = np.array([[1.0, 2.0]])
    path = RankCollapsePath(RankCollapse(np.eye(2), target_rank=1), points)

    points[0, 0] = 99.0
    retrieved = path.input_points
    retrieved[0, 1] = 88.0

    np.testing.assert_allclose(path.input_points, [[1.0, 2.0]])


@pytest.mark.parametrize(
    "points",
    [
        [[1.0, 2.0]],
        [[[1.0, 2.0, 3.0]]],
        [[1.0, np.inf, 3.0]],
        np.empty((0, 3)),
    ],
)
def test_invalid_point_collections_raise(points):
    collapse = RankCollapse(np.eye(3), target_rank=1)

    with pytest.raises(ValueError):
        RankCollapsePath(collapse, points)


def test_invalid_collapse_type_raises():
    with pytest.raises(TypeError):
        RankCollapsePath(np.eye(2), [[1.0, 2.0]])


def test_trajectory_point_dimension_must_match_domain():
    path = RankCollapsePath(RankCollapse(np.eye(3), target_rank=1), [[0, 0, 0]])

    with pytest.raises(ValueError):
        path.trajectory([1.0, 2.0], [0.0, 1.0])
