"""Orchestrate topology-aware geometry through a rank-collapse path.

This renderer-independent layer combines :class:`RankCollapseGeometry` with
:class:`RankCollapsePath`. It transforms every geometry vertex through the
mathematical path and reattaches the geometry's unchanged connectivity to each
returned :class:`RankCollapseGeometrySnapshot`.
"""

from __future__ import annotations

from numbers import Real
from typing import Iterable

import numpy as np

from .rank_collapse import RankCollapse
from .rank_collapse_geometry import (
    RankCollapseGeometry,
    RankCollapseGeometrySnapshot,
)
from .rank_collapse_path import RankCollapsePath


class RankCollapseGeometryPath:
    """Combine static topology with a dimension-independent rank-collapse path."""

    __slots__ = ("_geometry", "_path")

    def __init__(
        self,
        geometry: RankCollapseGeometry,
        path: RankCollapsePath,
    ) -> None:
        if not isinstance(geometry, RankCollapseGeometry):
            raise TypeError("geometry must be a RankCollapseGeometry instance")
        if not isinstance(path, RankCollapsePath):
            raise TypeError("path must be a RankCollapsePath instance")

        path_points = path.input_points
        if path_points.shape != geometry.vertices.shape:
            raise ValueError(
                "path input_points must have the same shape as geometry vertices"
            )
        if not np.array_equal(path_points, geometry.vertices):
            raise ValueError("path input_points must match geometry vertices exactly")

        self._geometry = geometry
        self._path = path

    @classmethod
    def from_collapse(
        cls,
        geometry: RankCollapseGeometry,
        collapse: RankCollapse,
    ) -> "RankCollapseGeometryPath":
        """Build a path whose input points are exactly ``geometry.vertices``."""
        if not isinstance(geometry, RankCollapseGeometry):
            raise TypeError("geometry must be a RankCollapseGeometry instance")
        if not isinstance(collapse, RankCollapse):
            raise TypeError("collapse must be a RankCollapse instance")
        return cls(geometry, RankCollapsePath(collapse, geometry.vertices))

    @property
    def geometry(self) -> RankCollapseGeometry:
        return self._geometry

    @property
    def path(self) -> RankCollapsePath:
        return self._path

    @property
    def collapse(self) -> RankCollapse:
        return self._path.collapse

    @property
    def vertex_count(self) -> int:
        return self._geometry.vertex_count

    @property
    def domain_dimension(self) -> int:
        return self._path.domain_dimension

    @property
    def codomain_dimension(self) -> int:
        return self._path.codomain_dimension

    def snapshot(self, progress: float) -> RankCollapseGeometrySnapshot:
        """Transform all vertices and preserve topology at ``progress``."""
        path_snapshot = self._path.snapshot(progress)
        return self._geometry.snapshot(
            path_snapshot.output_points,
            t=path_snapshot.progress,
        )

    def snapshots(
        self,
        progress_values: Iterable[Real],
    ) -> tuple[RankCollapseGeometrySnapshot, ...]:
        """Return topology-preserving snapshots in the requested order."""
        return tuple(self.snapshot(progress) for progress in progress_values)
