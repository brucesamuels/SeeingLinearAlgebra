"""Thin Manim adapter for the 3D rank-collapse lesson."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any
import numpy as np
from manim import Arrow, Dot3D, Line, VGroup

from engine.rank_collapse_3d import RankCollapse3DSnapshot

PointMapper = Callable[[np.ndarray], np.ndarray]


class ManimRankCollapse3D:
    """Maintain generators, endpoint samples, and cell edges in place."""

    _EDGES = ((0,1),(0,2),(0,3),(1,4),(1,5),(2,4),(2,6),(3,5),(3,6),(4,7),(5,7),(6,7))

    def __init__(
        self,
        snapshot: RankCollapse3DSnapshot,
        point_mapper: PointMapper,
        *,
        arrow_kwargs: tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]],
        dot_kwargs: Mapping[str, Any],
        edge_kwargs: Mapping[str, Any],
    ) -> None:
        self._map = point_mapper
        self._arrow_styles = tuple(self._flat_arrow_style(kwargs) for kwargs in arrow_kwargs)
        self._edge_style = self._flat_edge_style(edge_kwargs)
        origin = self._point(np.zeros(3))
        vectors = (snapshot.generator_u, snapshot.generator_v, snapshot.generator_w)

        # Flat VMobject arrows are used deliberately.  Arrow3D is a cylindrical
        # mesh and can roll around its own axis while its direction changes,
        # creating visible spinning artifacts.  These arrows still occupy the
        # correct 3D coordinates but have no axial orientation to spin.
        self.arrows = VGroup(*(
            Arrow(origin, self._point(vector), **style)
            for vector, style in zip(vectors, self._arrow_styles)
        ))
        self.dots = VGroup(*(
            Dot3D(self._point(point), **dict(dot_kwargs)) for point in snapshot.endpoints
        ))
        self.edges = VGroup(*(
            Line(
                self._point(snapshot.parallelepiped_corners[i]),
                self._point(snapshot.parallelepiped_corners[j]),
                **self._edge_style,
            )
            for i, j in self._EDGES
        ))
        self.mobject = VGroup(self.dots, self.edges, self.arrows)

    def update_from_snapshot(self, snapshot: RankCollapse3DSnapshot) -> None:
        origin = self._point(np.zeros(3))
        for arrow, vector in zip(
            self.arrows,
            (snapshot.generator_u, snapshot.generator_v, snapshot.generator_w),
        ):
            arrow.put_start_and_end_on(origin, self._point(vector))
        for dot, point in zip(self.dots, snapshot.endpoints):
            dot.move_to(self._point(point))
        for edge, (i, j) in zip(self.edges, self._EDGES):
            edge.put_start_and_end_on(
                self._point(snapshot.parallelepiped_corners[i]),
                self._point(snapshot.parallelepiped_corners[j]),
            )

    @staticmethod
    def _flat_arrow_style(kwargs: Mapping[str, Any]) -> dict[str, Any]:
        thickness = float(kwargs.get("thickness", 0.035))
        return {
            "color": kwargs.get("color"),
            "buff": 0.0,
            "stroke_width": max(3.0, 150.0 * thickness),
            "max_tip_length_to_length_ratio": 0.12,
            "max_stroke_width_to_length_ratio": 8.0,
        }

    @staticmethod
    def _flat_edge_style(kwargs: Mapping[str, Any]) -> dict[str, Any]:
        thickness = float(kwargs.get("thickness", 0.008))
        return {
            "color": kwargs.get("color"),
            "stroke_width": max(1.0, 140.0 * thickness),
        }

    def _point(self, coordinates: np.ndarray) -> np.ndarray:
        point = np.asarray(self._map(np.asarray(coordinates, dtype=float)), dtype=float)
        if point.shape != (3,) or not np.all(np.isfinite(point)):
            raise ValueError("point_mapper must return a finite 3D point")
        return point
