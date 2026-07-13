"""Thin Manim adapter for display-ready rank-collapse geometry.

The renderer-independent engine owns vertices, topology, collapse paths, and
projection.  This module begins only after a geometry snapshot has display
coordinates.  Its sole job is to keep Manim VMobjects synchronized with that
snapshot.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeAlias

import numpy as np
from numpy.typing import NDArray
from manim import VGroup, VMobject

from engine.rank_collapse_geometry import RankCollapseGeometrySnapshot


FloatArray: TypeAlias = NDArray[np.float64]
Style: TypeAlias = Mapping[str, Any]


def _as_manim_points(vertices: FloatArray) -> FloatArray:
    """Pad one- or two-dimensional display vertices to Manim's 3D points."""

    dimension = int(vertices.shape[1])
    if dimension > 3:
        raise ValueError(
            "ManimRankCollapseGeometry requires display vertices in at most "
            f"3 dimensions; received dimension {dimension}. Project the "
            "geometry with LinearDisplayProjector before rendering."
        )

    points = np.zeros((vertices.shape[0], 3), dtype=float)
    points[:, :dimension] = vertices
    points.setflags(write=False)
    return points


class ManimRankCollapseGeometry(VGroup):
    """Render a fixed topology whose display vertices vary over time.

    The adapter deliberately accepts a ``RankCollapseGeometrySnapshot`` rather
    than a collapse path, matrix, or projector.  Consequently it has no role in
    deciding how coordinates evolve or how arbitrary-dimensional data reaches
    display space.
    """

    def __init__(
        self,
        snapshot: RankCollapseGeometrySnapshot,
        *,
        edge_style: Style | None = None,
        polyline_style: Style | None = None,
        **vgroup_kwargs: Any,
    ) -> None:
        super().__init__(**vgroup_kwargs)

        self._edges = snapshot.edges
        self._polylines = snapshot.polylines
        self._edge_style = dict(edge_style or {})
        self._polyline_style = dict(polyline_style or {})
        self._snapshot = snapshot
        self._display_vertices = _as_manim_points(snapshot.vertices)

        self._edge_mobjects = VGroup(
            *(
                VMobject(**self._edge_style)
                for _ in self._edges
            )
        )
        self._polyline_mobjects = VGroup(
            *(
                VMobject(**self._polyline_style)
                for _ in self._polylines
            )
        )

        self.add(self._edge_mobjects, self._polyline_mobjects)
        self.set_snapshot(snapshot)

    @property
    def snapshot(self) -> RankCollapseGeometrySnapshot:
        return self._snapshot

    @property
    def display_vertices(self) -> FloatArray:
        """Read-only N-by-3 points currently supplied to Manim."""

        return self._display_vertices

    @property
    def edge_mobjects(self) -> VGroup:
        return self._edge_mobjects

    @property
    def polyline_mobjects(self) -> VGroup:
        return self._polyline_mobjects

    def set_snapshot(
        self,
        snapshot: RankCollapseGeometrySnapshot,
    ) -> "ManimRankCollapseGeometry":
        """Update coordinates without rebuilding Manim objects or topology."""

        if snapshot.edges != self._edges:
            raise ValueError("snapshot edges must match the adapter's fixed topology")
        if snapshot.polylines != self._polylines:
            raise ValueError(
                "snapshot polylines must match the adapter's fixed topology"
            )

        points = _as_manim_points(snapshot.vertices)

        for mobject, (start, end) in zip(
            self._edge_mobjects,
            self._edges,
            strict=True,
        ):
            mobject.set_points_as_corners(points[[start, end]])

        for mobject, polyline in zip(
            self._polyline_mobjects,
            self._polylines,
            strict=True,
        ):
            mobject.set_points_as_corners(points[list(polyline)])

        self._snapshot = snapshot
        self._display_vertices = points
        return self
