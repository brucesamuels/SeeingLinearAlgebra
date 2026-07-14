"""Project topology-aware rank-collapse geometry into display space.

This module remains renderer-independent. It combines a
:class:`RankCollapseGeometryPath` with a :class:`LinearDisplayProjector`,
projects every transformed vertex, and returns ordinary
:class:`RankCollapseGeometrySnapshot` objects with unchanged topology.
"""

from __future__ import annotations

from numbers import Real
from typing import Iterable

from .rank_collapse_display import LinearDisplayProjector
from .rank_collapse_geometry import RankCollapseGeometrySnapshot
from .rank_collapse_geometry_path import RankCollapseGeometryPath


class RankCollapseGeometryDisplayAdapter:
    """Project geometry-path snapshots into a chosen display space."""

    __slots__ = ("_geometry_path", "_projector")

    def __init__(
        self,
        geometry_path: RankCollapseGeometryPath,
        projector: LinearDisplayProjector,
    ) -> None:
        if not isinstance(geometry_path, RankCollapseGeometryPath):
            raise TypeError(
                "geometry_path must be a RankCollapseGeometryPath instance"
            )
        if not isinstance(projector, LinearDisplayProjector):
            raise TypeError("projector must be a LinearDisplayProjector instance")
        if projector.input_dimension != geometry_path.codomain_dimension:
            raise ValueError(
                "projector input dimension must equal the geometry path "
                f"codomain dimension ({geometry_path.codomain_dimension})"
            )

        self._geometry_path = geometry_path
        self._projector = projector

    @property
    def geometry_path(self) -> RankCollapseGeometryPath:
        return self._geometry_path

    @property
    def projector(self) -> LinearDisplayProjector:
        return self._projector

    @property
    def vertex_count(self) -> int:
        return self._geometry_path.vertex_count

    @property
    def domain_dimension(self) -> int:
        return self._geometry_path.domain_dimension

    @property
    def codomain_dimension(self) -> int:
        return self._geometry_path.codomain_dimension

    @property
    def display_dimension(self) -> int:
        return self._projector.display_dimension

    def snapshot(self, progress: float) -> RankCollapseGeometrySnapshot:
        """Return one display-ready geometry snapshot."""
        geometry_snapshot = self._geometry_path.snapshot(progress)
        display_vertices = self._projector.project(geometry_snapshot.vertices)

        return RankCollapseGeometrySnapshot(
            t=geometry_snapshot.t,
            vertices=display_vertices,
            edges=geometry_snapshot.edges,
            polylines=geometry_snapshot.polylines,
        )

    def snapshots(
        self,
        progress_values: Iterable[Real],
    ) -> tuple[RankCollapseGeometrySnapshot, ...]:
        """Return display-ready snapshots in the requested order."""
        return tuple(self.snapshot(progress) for progress in progress_values)
