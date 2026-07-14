"""Smoke scene for the full geometry-to-display rank-collapse pipeline."""

from __future__ import annotations

import numpy as np

from manim import BLUE, Scene, ValueTracker, linear

from engine.rank_collapse import RankCollapse
from engine.rank_collapse_display import LinearDisplayProjector
from engine.rank_collapse_geometry import RankCollapseGeometry
from engine.rank_collapse_geometry_display import (
    RankCollapseGeometryDisplayAdapter,
)
from engine.rank_collapse_geometry_path import RankCollapseGeometryPath
from manim_adapters.rank_collapse_geometry import ManimRankCollapseGeometry


def square_grid_geometry(
    *,
    side_length: float = 6.0,
    line_count: int = 9,
) -> RankCollapseGeometry:
    """Create one shared vertex lattice with horizontal and vertical polylines."""
    if line_count < 2:
        raise ValueError("line_count must be at least 2")

    coordinates = np.linspace(-side_length / 2.0, side_length / 2.0, line_count)
    vertices = np.array(
        [(x, y) for y in coordinates for x in coordinates],
        dtype=float,
    )

    def index(row: int, column: int) -> int:
        return row * line_count + column

    rows = [
        tuple(index(row, column) for column in range(line_count))
        for row in range(line_count)
    ]
    columns = [
        tuple(index(row, column) for row in range(line_count))
        for column in range(line_count)
    ]

    return RankCollapseGeometry(vertices, polylines=(*rows, *columns))


class RankCollapseGeometrySmoke(Scene):
    def construct(self) -> None:
        geometry = square_grid_geometry()
        collapse = RankCollapse(np.eye(2), target_rank=1)
        geometry_path = RankCollapseGeometryPath.from_collapse(
            geometry,
            collapse,
        )
        projector = LinearDisplayProjector(np.eye(2))
        display_path = RankCollapseGeometryDisplayAdapter(
            geometry_path,
            projector,
        )

        grid = ManimRankCollapseGeometry(
            display_path.snapshot(0.0),
            polyline_style={
                "stroke_color": BLUE,
                "stroke_width": 3.0,
                "stroke_opacity": 0.8,
            },
        )

        parameter = ValueTracker(0.0)

        def update_grid(adapter: ManimRankCollapseGeometry) -> None:
            adapter.set_snapshot(display_path.snapshot(parameter.get_value()))

        grid.add_updater(update_grid)
        self.add(grid)
        self.wait(0.5)
        self.play(
            parameter.animate.set_value(1.0),
            run_time=4.0,
            rate_func=linear,
        )
        grid.clear_updaters()
        self.wait(0.75)
