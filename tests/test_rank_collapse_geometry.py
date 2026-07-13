import numpy as np
import pytest

from engine.rank_collapse_geometry import (
    RankCollapseGeometry,
    RankCollapseGeometrySnapshot,
)


def test_geometry_stores_arbitrary_dimensional_vertices_and_topology() -> None:
    vertices = np.arange(20, dtype=float).reshape(5, 4)
    geometry = RankCollapseGeometry(
        vertices,
        edges=[(0, 1), (1, 2)],
        polylines=[(0, 1, 2), (2, 3, 4, 2)],
    )

    assert geometry.vertex_count == 5
    assert geometry.ambient_dimension == 4
    assert geometry.edges == ((0, 1), (1, 2))
    assert geometry.polylines == ((0, 1, 2), (2, 3, 4, 2))
    np.testing.assert_allclose(geometry.vertices, vertices)


def test_geometry_defensively_copies_source_vertices() -> None:
    vertices = np.array([[0.0, 0.0], [1.0, 0.0]])
    geometry = RankCollapseGeometry(vertices, edges=[(0, 1)])

    vertices[0, 0] = 99.0

    assert geometry.vertices[0, 0] == 0.0
    with pytest.raises(ValueError):
        geometry.vertices[0, 0] = 1.0


def test_snapshot_can_change_ambient_dimension_but_not_vertex_count() -> None:
    geometry = RankCollapseGeometry(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        edges=[(0, 1), (1, 2)],
    )

    collapsed_vertices = np.array([[0.0], [1.0], [0.5]])
    snapshot = geometry.snapshot(collapsed_vertices, t=1.0)

    assert snapshot.vertex_count == 3
    assert snapshot.ambient_dimension == 1
    assert snapshot.t == 1.0
    assert snapshot.edges == geometry.edges
    np.testing.assert_allclose(snapshot.vertices, collapsed_vertices)


def test_snapshot_rejects_a_changed_vertex_count() -> None:
    geometry = RankCollapseGeometry([[0.0, 0.0], [1.0, 0.0]])

    with pytest.raises(ValueError, match="exactly 2 vertices"):
        geometry.snapshot([[0.0], [1.0], [2.0]], t=0.5)


def test_source_snapshot_preserves_topology() -> None:
    geometry = RankCollapseGeometry(
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
        edges=[(0, 1)],
        polylines=[(0, 1, 2)],
    )

    snapshot = geometry.source_snapshot()

    assert snapshot.t == 0.0
    assert snapshot.edges == ((0, 1),)
    assert snapshot.polylines == ((0, 1, 2),)
    np.testing.assert_allclose(snapshot.vertices, geometry.vertices)


def test_snapshot_extracts_edge_and_polyline_coordinate_arrays() -> None:
    snapshot = RankCollapseGeometrySnapshot(
        t=0.25,
        vertices=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
            ]
        ),
        edges=((0, 2),),
        polylines=((0, 1, 2),),
    )

    edge_segments = snapshot.edge_segments()
    polyline_vertices = snapshot.polyline_vertices()

    assert edge_segments[0].shape == (2, 3)
    assert polyline_vertices[0].shape == (3, 3)
    np.testing.assert_allclose(edge_segments[0], snapshot.vertices[[0, 2]])
    np.testing.assert_allclose(polyline_vertices[0], snapshot.vertices[[0, 1, 2]])


def test_closed_polyline_is_allowed() -> None:
    geometry = RankCollapseGeometry(
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]],
        polylines=[(0, 1, 2, 3, 0)],
    )

    assert geometry.polylines == ((0, 1, 2, 3, 0),)


@pytest.mark.parametrize(
    "vertices",
    [
        [0.0, 1.0],
        [],
        np.empty((2, 0)),
        [[0.0, np.inf]],
        [[0.0, np.nan]],
    ],
)
def test_invalid_vertex_arrays_are_rejected(vertices) -> None:
    with pytest.raises(ValueError):
        RankCollapseGeometry(vertices)


@pytest.mark.parametrize(
    "edges, expected_exception",
    [
        ([(0,)], ValueError),
        ([(0, 1, 2)], ValueError),
        ([(0, 3)], IndexError),
        ([(-1, 1)], IndexError),
        ([(0.0, 1)], TypeError),
        ([(True, 1)], TypeError),
    ],
)
def test_invalid_edges_are_rejected(edges, expected_exception) -> None:
    with pytest.raises(expected_exception):
        RankCollapseGeometry(
            [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]],
            edges=edges,
        )


@pytest.mark.parametrize(
    "polylines, expected_exception",
    [
        ([(0,)], ValueError),
        ([(0, 3)], IndexError),
        ([(-1, 1)], IndexError),
        ([(0, 1.5)], TypeError),
        ([(False, 1)], TypeError),
    ],
)
def test_invalid_polylines_are_rejected(polylines, expected_exception) -> None:
    with pytest.raises(expected_exception):
        RankCollapseGeometry(
            [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]],
            polylines=polylines,
        )
