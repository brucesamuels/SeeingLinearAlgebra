import numpy as np
import pytest

from engine.rank_collapse import RankCollapse
from engine.rank_collapse_display import LinearDisplayProjector
from engine.rank_collapse_geometry import RankCollapseGeometry
from engine.rank_collapse_geometry_display import (
    RankCollapseGeometryDisplayAdapter,
)
from engine.rank_collapse_geometry_path import RankCollapseGeometryPath


def make_geometry_path() -> RankCollapseGeometryPath:
    geometry = RankCollapseGeometry(
        [[1.0, 0.0, 1.0], [0.0, 1.0, -1.0], [2.0, -1.0, 0.5]],
        edges=[(0, 1), (1, 2)],
        polylines=[(0, 1, 2)],
    )
    collapse = RankCollapse(
        [[2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 1.0]],
        target_rank=2,
    )
    return RankCollapseGeometryPath.from_collapse(geometry, collapse)


def test_snapshot_projects_vertices_and_preserves_topology() -> None:
    geometry_path = make_geometry_path()
    projector = LinearDisplayProjector.from_axis_selector(3, [0, 2])
    adapter = RankCollapseGeometryDisplayAdapter(geometry_path, projector)

    source = geometry_path.snapshot(0.0)
    display = adapter.snapshot(0.0)

    np.testing.assert_allclose(
        display.vertices,
        projector.project(source.vertices),
    )
    assert display.t == source.t
    assert display.edges == source.edges
    assert display.polylines == source.polylines


def test_projection_can_reduce_three_dimensions_to_two() -> None:
    geometry_path = make_geometry_path()
    projector = LinearDisplayProjector(
        [[1.0, 0.0, 1.0], [0.0, 2.0, 0.0]],
        offset=[10.0, -1.0],
    )
    adapter = RankCollapseGeometryDisplayAdapter(geometry_path, projector)

    snapshot = adapter.snapshot(1.0)

    assert snapshot.ambient_dimension == 2
    assert adapter.display_dimension == 2
    assert snapshot.vertex_count == geometry_path.vertex_count
    np.testing.assert_allclose(
        snapshot.vertices,
        projector.project(geometry_path.snapshot(1.0).vertices),
    )


def test_identity_projection_preserves_display_coordinates() -> None:
    geometry = RankCollapseGeometry(
        [[0.0, 0.0], [1.0, 1.0]],
        edges=[(0, 1)],
    )
    geometry_path = RankCollapseGeometryPath.from_collapse(
        geometry,
        RankCollapse(np.eye(2), target_rank=1),
    )
    projector = LinearDisplayProjector(np.eye(2))
    adapter = RankCollapseGeometryDisplayAdapter(geometry_path, projector)

    np.testing.assert_allclose(
        adapter.snapshot(0.5).vertices,
        geometry_path.snapshot(0.5).vertices,
    )


def test_snapshots_preserve_requested_order() -> None:
    geometry_path = make_geometry_path()
    projector = LinearDisplayProjector.from_axis_selector(3, [0, 1])
    adapter = RankCollapseGeometryDisplayAdapter(geometry_path, projector)

    snapshots = adapter.snapshots([1.0, 0.0, 0.25])

    assert tuple(snapshot.t for snapshot in snapshots) == (1.0, 0.0, 0.25)
    assert all(snapshot.edges == geometry_path.geometry.edges for snapshot in snapshots)
    assert all(
        snapshot.polylines == geometry_path.geometry.polylines
        for snapshot in snapshots
    )


def test_properties_expose_composed_dimensions_and_components() -> None:
    geometry_path = make_geometry_path()
    projector = LinearDisplayProjector.from_axis_selector(3, [0, 2])
    adapter = RankCollapseGeometryDisplayAdapter(geometry_path, projector)

    assert adapter.geometry_path is geometry_path
    assert adapter.projector is projector
    assert adapter.vertex_count == 3
    assert adapter.domain_dimension == 3
    assert adapter.codomain_dimension == 3
    assert adapter.display_dimension == 2


def test_constructor_validates_types_and_dimensions() -> None:
    geometry_path = make_geometry_path()
    valid_projector = LinearDisplayProjector.from_axis_selector(3, [0, 1])
    wrong_projector = LinearDisplayProjector.from_axis_selector(2, [0])

    with pytest.raises(TypeError, match="geometry_path"):
        RankCollapseGeometryDisplayAdapter(np.eye(3), valid_projector)
    with pytest.raises(TypeError, match="projector"):
        RankCollapseGeometryDisplayAdapter(geometry_path, np.eye(3))
    with pytest.raises(ValueError, match="codomain dimension"):
        RankCollapseGeometryDisplayAdapter(geometry_path, wrong_projector)
