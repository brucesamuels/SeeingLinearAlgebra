import numpy as np
import pytest

from engine.rank_collapse import RankCollapse
from engine.rank_collapse_path import RankCollapsePath
from engine.rank_collapse_display import (
    LinearDisplayProjector,
    RankCollapseDisplayAdapter,
)


def test_projector_projects_single_vector():
    projector = LinearDisplayProjector([[1.0, 0.0, 2.0], [0.0, -1.0, 0.0]])

    np.testing.assert_allclose(projector.project([3.0, 4.0, 5.0]), [13.0, -4.0])


def test_projector_projects_row_stored_vectors_with_offset():
    projector = LinearDisplayProjector(
        [[1.0, 0.0], [0.0, 1.0]],
        offset=[10.0, -1.0],
    )

    result = projector.project([[2.0, 3.0], [-1.0, 4.0]])

    np.testing.assert_allclose(result, [[12.0, 2.0], [9.0, 3.0]])


def test_axis_selector_builds_coordinate_projection():
    projector = LinearDisplayProjector.from_axis_selector(4, [0, 2], scales=[2.0, -1.0])

    np.testing.assert_allclose(
        projector.projection_matrix,
        np.array([[2.0, 0.0, 0.0, 0.0], [0.0, 0.0, -1.0, 0.0]]),
    )
    np.testing.assert_allclose(projector.project([1.0, 9.0, 3.0, 7.0]), [2.0, -3.0])


@pytest.mark.parametrize(
    "axis_indices",
    [
        [],
        [0, 0],
        [0, 4],
    ],
)
def test_invalid_axis_selector_arguments_raise(axis_indices):
    with pytest.raises((TypeError, ValueError)):
        LinearDisplayProjector.from_axis_selector(4, axis_indices)


@pytest.mark.parametrize(
    "matrix, offset",
    [
        (np.ones(3), None),
        (np.empty((0, 2)), None),
        ([[1.0, np.inf]], None),
        ([[1.0, 2.0]], [1.0, 2.0]),
        ([[1.0, 2.0]], [[1.0]]),
    ],
)
def test_invalid_projector_initialization_raises(matrix, offset):
    with pytest.raises(ValueError):
        LinearDisplayProjector(matrix, offset=offset)


@pytest.mark.parametrize(
    "vectors",
    [
        [1.0],
        [[1.0], [2.0]],
        [[[1.0, 2.0]]],
        [1.0, np.inf],
    ],
)
def test_invalid_project_arguments_raise(vectors):
    projector = LinearDisplayProjector([[1.0, 0.0], [0.0, 1.0]])

    with pytest.raises(ValueError):
        projector.project(vectors)


def test_adapter_projects_points_at_requested_progress():
    collapse = RankCollapse(np.diag([4.0, 2.0, 1.0]), target_rank=2)
    path = RankCollapsePath(collapse, [[1.0, 1.0, 1.0]])
    projector = LinearDisplayProjector.from_axis_selector(3, [0, 2])
    adapter = RankCollapseDisplayAdapter(path, projector)

    np.testing.assert_allclose(adapter.display_points_at(0.0), [[4.0, 1.0]])
    np.testing.assert_allclose(adapter.display_points_at(1.0), [[4.0, 0.0]], atol=1e-12)


def test_adapter_projects_basis_images():
    matrix = np.array([[2.0, 1.0], [0.0, 3.0], [4.0, 0.0]])
    collapse = RankCollapse(matrix, target_rank=1)
    path = RankCollapsePath(collapse, np.eye(2))
    projector = LinearDisplayProjector.from_axis_selector(3, [1, 2])
    adapter = RankCollapseDisplayAdapter(path, projector)

    np.testing.assert_allclose(
        adapter.display_basis_images_at(0.0),
        [[0.0, 4.0], [3.0, 0.0]],
        atol=1e-12,
    )


def test_display_trajectory_is_projected_correctly():
    collapse = RankCollapse(np.diag([5.0, 3.0, 2.0, 1.0]), target_rank=2)
    path = RankCollapsePath(collapse, np.eye(4))
    projector = LinearDisplayProjector.from_axis_selector(4, [0, 2, 3])
    adapter = RankCollapseDisplayAdapter(path, projector)

    result = adapter.display_trajectory([1.0, 1.0, 1.0, 1.0], [0.0, 0.5, 1.0])

    assert result.shape == (3, 3)
    np.testing.assert_allclose(result[0], [5.0, 2.0, 1.0])
    np.testing.assert_allclose(result[1], [5.0, 1.0, 0.5])
    np.testing.assert_allclose(result[2], [5.0, 0.0, 0.0])


def test_snapshot_is_consistent_with_path_and_projection():
    collapse = RankCollapse(np.diag([3.0, 2.0]), target_rank=1)
    path = RankCollapsePath(collapse, [[1.0, 1.0], [2.0, -1.0]])
    projector = LinearDisplayProjector([[1.0, 1.0]], offset=[10.0])
    adapter = RankCollapseDisplayAdapter(path, projector)

    snapshot = adapter.snapshot(1.0)

    assert snapshot.progress == 1.0
    assert snapshot.rank == 1
    assert snapshot.nullity == 1
    assert snapshot.display_dimension == 1
    np.testing.assert_allclose(snapshot.output_points, path.points_at(1.0))
    np.testing.assert_allclose(snapshot.display_points, adapter.display_points_at(1.0))
    np.testing.assert_allclose(
        snapshot.display_basis_images,
        adapter.display_basis_images_at(1.0),
    )
    np.testing.assert_allclose(snapshot.projection_matrix, projector.projection_matrix)
    np.testing.assert_allclose(snapshot.display_offset, projector.offset)


def test_snapshots_preserve_requested_order():
    collapse = RankCollapse(np.diag([2.0, 1.0]), target_rank=1)
    path = RankCollapsePath(collapse, [[1.0, 0.0]])
    projector = LinearDisplayProjector.from_axis_selector(2, [0])
    adapter = RankCollapseDisplayAdapter(path, projector)

    frames = adapter.snapshots([1.0, 0.0, 0.5])

    assert tuple(frame.progress for frame in frames) == (1.0, 0.0, 0.5)


def test_adapter_rejects_codomain_projector_mismatch():
    collapse = RankCollapse(np.eye(3), target_rank=2)
    path = RankCollapsePath(collapse, [[1.0, 0.0, 0.0]])
    projector = LinearDisplayProjector.from_axis_selector(2, [0])

    with pytest.raises(ValueError):
        RankCollapseDisplayAdapter(path, projector)


@pytest.mark.parametrize(
    "path, projector",
    [
        (np.eye(2), LinearDisplayProjector.from_axis_selector(2, [0])),
        (
            RankCollapsePath(RankCollapse(np.eye(2), target_rank=1), [[1.0, 0.0]]),
            np.eye(2),
        ),
    ],
)
def test_adapter_type_validation(path, projector):
    with pytest.raises(TypeError):
        RankCollapseDisplayAdapter(path, projector)
