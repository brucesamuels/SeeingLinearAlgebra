"""Thin Manim adapters for the dimension-growth lesson."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any
import numpy as np
from manim import Arrow3D, Dot3D, Polygon, VGroup

from engine.dimension_growth import DimensionGrowthSnapshot

PointMapper = Callable[[np.ndarray], np.ndarray]


class ManimDimensionGrowth:
    """Maintain generator arrows and one translated plane in place."""

    def __init__(
        self,
        snapshot: DimensionGrowthSnapshot,
        point_mapper: PointMapper,
        *,
        u_kwargs: Mapping[str, Any] | None = None,
        v_kwargs: Mapping[str, Any] | None = None,
        w_kwargs: Mapping[str, Any] | None = None,
        plane_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        self._map = point_mapper
        origin = self._point(np.zeros(3))
        self.u_arrow = Arrow3D(origin, self._point(snapshot.generator_u), **dict(u_kwargs or {}))
        self.v_arrow = Arrow3D(origin, self._point(snapshot.generator_v), **dict(v_kwargs or {}))
        self.w_arrow = Arrow3D(origin, self._point(snapshot.generator_w), **dict(w_kwargs or {}))
        self.translated_plane = Polygon(
            *(self._point(corner) for corner in snapshot.translated_plane_corners),
            **dict(plane_kwargs or {}),
        )
        self.mobject = VGroup(self.translated_plane, self.u_arrow, self.v_arrow, self.w_arrow)

    def update_translated_plane(self, snapshot: DimensionGrowthSnapshot) -> None:
        points = [self._point(corner) for corner in snapshot.translated_plane_corners]
        self.translated_plane.set_points_as_corners([*points, points[0]])

    def dots_for(self, points: np.ndarray, **dot_kwargs: Any) -> VGroup:
        return VGroup(*(Dot3D(self._point(point), **dot_kwargs) for point in points))

    def _point(self, coordinates: np.ndarray) -> np.ndarray:
        point = np.asarray(self._map(np.asarray(coordinates, dtype=float)), dtype=float)
        if point.shape != (3,) or not np.all(np.isfinite(point)):
            raise ValueError("point_mapper must return a finite 3D point")
        return point
