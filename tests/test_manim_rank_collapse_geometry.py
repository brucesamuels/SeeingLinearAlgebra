import numpy as np
import pytest

from engine.rank_collapse_geometry import RankCollapseGeometry
from manim_adapters.rank_collapse_geometry import ManimRankCollapseGeometry


def test_adapter_builds_one_mobject_per_topology_item() -> None:
    geometry = RankCollapseGeometry(
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
        edges=[(0, 1), (1, 2)],
        polylines=[(0, 1, 2)],
    )

    adapter = ManimRankCollapseGeometry(geometry.source_snapshot())

    assert len(adapter.edge_mobjects) == 2
    assert len(adapter.polyline_mobjects) == 1
    assert adapter.snapshot.edges == geometry.edges
    assert adapter.snapshot.polylines == geometry.polylines


def test_adapter_pads_one_and_two_dimensional_vertices_for_manim() -> None:
    one_dimensional = RankCollapseGeometry([[0.0], [2.0]], edges=[(0, 1)])
    adapter = ManimRankCollapseGeometry(one_dimensional.source_snapshot())

    np.testing.assert_allclose(
        adapter.display_vertices,
        [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
    )

    two_dimensional_snapshot = one_dimensional.snapshot(
        [[0.0, 1.0], [2.0, 3.0]],
        t=0.5,
    )
    adapter.set_snapshot(two_dimensional_snapshot)

    np.testing.assert_allclose(
        adapter.display_vertices,
        [[0.0, 1.0, 0.0], [2.0, 3.0, 0.0]],
    )


def test_update_preserves_mobject_identity() -> None:
    geometry = RankCollapseGeometry(
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
        edges=[(0, 1)],
        polylines=[(0, 1, 2)],
    )
    adapter = ManimRankCollapseGeometry(geometry.source_snapshot())
    edge_id = id(adapter.edge_mobjects[0])
    polyline_id = id(adapter.polyline_mobjects[0])

    adapter.set_snapshot(
        geometry.snapshot(
            [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]],
            t=1.0,
        )
    )

    assert id(adapter.edge_mobjects[0]) == edge_id
    assert id(adapter.polyline_mobjects[0]) == polyline_id
    assert adapter.snapshot.t == 1.0


def test_adapter_rejects_more_than_three_display_dimensions() -> None:
    geometry = RankCollapseGeometry(np.zeros((2, 4)), edges=[(0, 1)])

    with pytest.raises(ValueError, match="LinearDisplayProjector"):
        ManimRankCollapseGeometry(geometry.source_snapshot())


def test_adapter_rejects_changed_topology() -> None:
    original = RankCollapseGeometry(
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
        edges=[(0, 1)],
    )
    changed = RankCollapseGeometry(
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
        edges=[(1, 2)],
    )
    adapter = ManimRankCollapseGeometry(original.source_snapshot())

    with pytest.raises(ValueError, match="edges"):
        adapter.set_snapshot(changed.source_snapshot())
