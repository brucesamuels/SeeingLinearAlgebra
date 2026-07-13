import numpy as np
import pytest

from engine.rank_collapse import RankCollapse
from engine.rank_collapse_geometry import RankCollapseGeometry
from engine.rank_collapse_geometry_path import RankCollapseGeometryPath
from engine.rank_collapse_path import RankCollapsePath


def test_from_collapse_transforms_all_vertices_and_preserves_topology() -> None:
    geometry = RankCollapseGeometry(
        [[0.0, 0.0], [1.0, 1.0], [2.0, -1.0]],
        edges=[(0, 1)],
        polylines=[(0, 1, 2)],
    )
    geometry_path = RankCollapseGeometryPath.from_collapse(
        geometry,
        RankCollapse(np.diag([3.0, 2.0]), target_rank=1),
    )

    initial = geometry_path.snapshot(0.0)
    final = geometry_path.snapshot(1.0)

    np.testing.assert_allclose(
        initial.vertices,
        [[0.0, 0.0], [3.0, 2.0], [6.0, -2.0]],
    )
    np.testing.assert_allclose(
        final.vertices,
        [[0.0, 0.0], [3.0, 0.0], [6.0, 0.0]],
        atol=1e-12,
    )
    assert initial.edges == final.edges == geometry.edges
    assert initial.polylines == final.polylines == geometry.polylines


def test_rectangular_map_changes_ambient_dimension_without_changing_topology() -> None:
    geometry = RankCollapseGeometry(
        [[1.0, 0.0, 1.0], [0.0, 1.0, -1.0]],
        edges=[(0, 1)],
    )
    collapse = RankCollapse(
        [[1.0, 0.0, 0.0], [0.0, 2.0, 0.0]],
        target_rank=1,
    )
    geometry_path = RankCollapseGeometryPath.from_collapse(geometry, collapse)

    snapshot = geometry_path.snapshot(0.0)

    assert geometry_path.domain_dimension == 3
    assert geometry_path.codomain_dimension == 2
    assert snapshot.vertex_count == 2
    assert snapshot.ambient_dimension == 2
    assert snapshot.edges == ((0, 1),)
    np.testing.assert_allclose(snapshot.vertices, [[1.0, 0.0], [0.0, 2.0]])


def test_snapshots_preserve_requested_order_and_connectivity() -> None:
    geometry = RankCollapseGeometry(
        [[0.0, 0.0], [1.0, 1.0]],
        edges=[(0, 1)],
    )
    geometry_path = RankCollapseGeometryPath.from_collapse(
        geometry,
        RankCollapse(np.diag([4.0, 2.0]), target_rank=1),
    )

    snapshots = geometry_path.snapshots([1.0, 0.0, 0.5])

    assert tuple(snapshot.t for snapshot in snapshots) == (1.0, 0.0, 0.5)
    assert all(snapshot.edges == geometry.edges for snapshot in snapshots)


def test_explicit_path_accepts_matching_geometry_vertices() -> None:
    geometry = RankCollapseGeometry([[0.0, 0.0], [1.0, 1.0]])
    path = RankCollapsePath(
        RankCollapse(np.eye(2), target_rank=1),
        geometry.vertices.copy(),
    )

    geometry_path = RankCollapseGeometryPath(geometry, path)

    assert geometry_path.geometry is geometry
    assert geometry_path.path is path
    assert geometry_path.collapse is path.collapse
    assert geometry_path.vertex_count == 2


def test_explicit_path_rejects_different_input_vertices() -> None:
    geometry = RankCollapseGeometry([[0.0, 0.0], [1.0, 1.0]])
    path = RankCollapsePath(
        RankCollapse(np.eye(2), target_rank=1),
        [[0.0, 0.0], [2.0, 1.0]],
    )

    with pytest.raises(ValueError, match="must match geometry vertices exactly"):
        RankCollapseGeometryPath(geometry, path)


def test_component_types_are_validated() -> None:
    geometry = RankCollapseGeometry([[0.0, 0.0]])
    collapse = RankCollapse(np.eye(2), target_rank=1)
    path = RankCollapsePath(collapse, geometry.vertices)

    with pytest.raises(TypeError, match="geometry"):
        RankCollapseGeometryPath(np.zeros((1, 2)), path)
    with pytest.raises(TypeError, match="path"):
        RankCollapseGeometryPath(geometry, collapse)
    with pytest.raises(TypeError, match="collapse"):
        RankCollapseGeometryPath.from_collapse(geometry, np.eye(2))
