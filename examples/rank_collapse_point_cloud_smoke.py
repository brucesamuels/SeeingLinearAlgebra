"""Low-quality smoke scene for Engine v0.3 RankCollapse.

Render from the repository root with:

    manim -pql examples/rank_collapse_point_cloud_smoke.py RankCollapsePointCloudSmoke
"""

import numpy as np
from manim import BLUE, NumberPlane, Scene, ValueTracker, linear

from engine.rank_collapse import RankCollapse
from engine.rank_collapse_path import RankCollapsePath
from engine.rank_collapse_display import (
    LinearDisplayProjector,
    RankCollapseDisplayAdapter,
)
from engine.visuals.rank_collapse_manim import ManimRankCollapsePointCloud


class RankCollapsePointCloudSmoke(Scene):
    """Show a two-dimensional point lattice continuously collapsing to a line."""

    def construct(self) -> None:
        matrix = np.array(
            [
                [1.35, 0.55],
                [-0.25, 1.10],
            ]
        )
        collapse = RankCollapse(matrix, target_rank=1)

        x_values = np.linspace(-2.5, 2.5, 17)
        y_values = np.linspace(-1.8, 1.8, 13)
        points = np.array([[x, y] for x in x_values for y in y_values])

        path = RankCollapsePath(collapse, points)
        projector = LinearDisplayProjector.from_axis_selector(
            input_dimension=2,
            axis_indices=[0, 1],
            scales=[1.15, 1.15],
        )
        display = RankCollapseDisplayAdapter(path, projector)
        manim_cloud = ManimRankCollapsePointCloud(display)

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.35},
        )
        progress = ValueTracker(0.0)
        cloud = manim_cloud.build_point_cloud(
            progress=0.0,
            point_kwargs={"radius": 0.035, "color": BLUE},
        )
        manim_cloud.bind_to_tracker(cloud, progress)

        self.add(plane, cloud)
        self.wait(0.5)
        self.play(
            progress.animate.set_value(1.0),
            run_time=4.0,
            rate_func=linear,
        )
        cloud.clear_updaters()
        self.wait(0.5)
