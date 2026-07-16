"""True full-rank native 3D linear-combination smoke scene.

Three independent vectors are drawn from a common origin, followed by their
wireframe parallelepiped and the resultant supplied by the existing
linear-combination pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import (
    Arrow3D,
    BLUE,
    DEGREES,
    FadeIn,
    GREEN,
    Line3D,
    MathTex,
    PURPLE,
    Text,
    ThreeDAxes,
    ThreeDScene,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.coefficient_sweep_path import CoefficientSweepPath
from engine.linear_combination import LinearCombination
from engine.linear_combination_geometry_display import (
    LinearCombinationGeometryDisplayAdapter,
    LinearCombinationGeometryDisplaySnapshot,
)
from engine.linear_combination_geometry_path import LinearCombinationGeometryPath
from engine.rank_collapse_display import LinearDisplayProjector


SMOKE_VECTORS = np.array(
    [
        [2.0, 0.5, 0.75],
        [-0.5, 1.75, 0.50],
        [0.50, -0.25, 1.75],
    ],
    dtype=float,
)
SMOKE_COEFFICIENTS = np.ones(3, dtype=float)
VECTOR_DRAW_RUN_TIME = 2.2


@dataclass(frozen=True, slots=True)
class Native3DFullRankPipeline:
    display_adapter: LinearCombinationGeometryDisplayAdapter
    final_snapshot: LinearCombinationGeometryDisplaySnapshot


def build_native_3d_full_rank_pipeline() -> Native3DFullRankPipeline:
    linear_combination = LinearCombination(SMOKE_VECTORS)
    coefficient_path = CoefficientSweepPath(
        linear_combination,
        np.zeros(3, dtype=float),
        SMOKE_COEFFICIENTS,
    )
    geometry_path = LinearCombinationGeometryPath(coefficient_path)
    projector = LinearDisplayProjector(np.eye(3, dtype=float))
    display_adapter = LinearCombinationGeometryDisplayAdapter(
        geometry_path,
        projector,
    )
    return Native3DFullRankPipeline(
        display_adapter=display_adapter,
        final_snapshot=display_adapter.snapshot(1.0),
    )


def _parallelepiped_edges(
    u: np.ndarray,
    v: np.ndarray,
    w: np.ndarray,
) -> tuple[tuple[np.ndarray, np.ndarray], ...]:
    vertices = {
        (i, j, k): i * u + j * v + k * w
        for i in (0, 1)
        for j in (0, 1)
        for k in (0, 1)
    }

    edges: list[tuple[np.ndarray, np.ndarray]] = []
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                if i == 0:
                    edges.append((vertices[(0, j, k)], vertices[(1, j, k)]))
                if j == 0:
                    edges.append((vertices[(i, 0, k)], vertices[(i, 1, k)]))
                if k == 0:
                    edges.append((vertices[(i, j, 0)], vertices[(i, j, 1)]))
    return tuple(edges)


def _shaft(
    start_point: np.ndarray,
    end_point: np.ndarray,
    *,
    color,
) -> Line3D:
    return Line3D(
        start=start_point,
        end=end_point,
        thickness=0.025,
        color=color,
    )


def _arrow(
    start_point: np.ndarray,
    end_point: np.ndarray,
    *,
    color,
    thickness: float = 0.04,
) -> Arrow3D:
    return Arrow3D(
        start=start_point,
        end=end_point,
        thickness=thickness,
        height=0.25,
        base_radius=0.08,
        resolution=12,
        color=color,
    )


class LinearCombinationNative3DSmoke(ThreeDScene):
    """Show three common-origin vectors, their box, and their resultant."""

    def construct(self) -> None:
        pipeline = build_native_3d_full_rank_pipeline()
        result = pipeline.final_snapshot.linear_combination_snapshot.result

        axes = ThreeDAxes(
            x_range=(-4.0, 5.0, 1.0),
            y_range=(-4.0, 5.0, 1.0),
            z_range=(-3.0, 5.0, 1.0),
            x_length=7.0,
            y_length=7.0,
            z_length=6.0,
        )

        axes_origin = axes.c2p(0.0, 0.0, 0.0)
        vector_points = tuple(
            axes.c2p(*vector)
            for vector in SMOKE_VECTORS
        )
        result_point = axes.c2p(*result)

        title = Text("Native 3D Full-Rank Linear Combination", font_size=30)
        title.to_edge(np.array([0.0, 1.0, 0.0]))

        result_label = MathTex(
            r"\mathbf{r}=\mathbf{u}+\mathbf{v}+\mathbf{w}",
            font_size=34,
            color=YELLOW,
        )
        result_label.to_corner(np.array([1.0, 1.0, 0.0]))
        result_label.set_opacity(0.0)

        self.set_camera_orientation(phi=68 * DEGREES, theta=-42 * DEGREES)
        self.add_fixed_in_frame_mobjects(title, result_label)
        self.play(FadeIn(axes), FadeIn(title))

        colors = (BLUE, GREEN, PURPLE)
        arrows: list[Arrow3D] = []

        for vector_point, color in zip(
            vector_points,
            colors,
            strict=True,
        ):
            shaft = _shaft(
                axes_origin,
                vector_point,
                color=color,
            )
            shaft.set_opacity(0.0)
            self.add(shaft)
            self.play(
                shaft.animate.set_opacity(1.0),
                run_time=VECTOR_DRAW_RUN_TIME,
            )

            arrow = _arrow(
                axes_origin,
                vector_point,
                color=color,
            )
            self.remove(shaft)
            self.add(arrow)
            arrows.append(arrow)
            self.wait(0.4)

        box = VGroup(
            *(
                Line3D(
                    start=axes.c2p(*start),
                    end=axes.c2p(*end),
                    thickness=0.007,
                    color=WHITE,
                ).set_opacity(0.28)
                for start, end in _parallelepiped_edges(*SMOKE_VECTORS)
            )
        )
        self.play(FadeIn(box), run_time=1.4)
        self.wait(0.6)

        resultant = _arrow(
            axes_origin,
            result_point,
            color=YELLOW,
            thickness=0.06,
        )
        self.play(
            FadeIn(resultant),
            result_label.animate.set_opacity(1.0),
            run_time=1.4,
        )
        self.wait(1.0)

        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
