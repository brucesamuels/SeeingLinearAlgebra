"""Smoke scene for the complete linear-combination trace pipeline.

Checkpoint 19 is an integration boundary.  It samples the established
renderer-independent geometry path, builds and projects one immutable resultant
trace, and combines that fixed trace with the existing in-place Manim arrow
updates.  No coefficient interpolation, linear-combination mathematics,
segment construction, trace construction, or display projection is reproduced
inside the Manim adapters.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import (
    BLUE_C,
    GREEN_C,
    ORANGE,
    YELLOW,
    FadeIn,
    NumberPlane,
    Scene,
    Text,
    UP,
    UpdateFromAlphaFunc,
    linear,
)

from engine.coefficient_sweep_path import CoefficientSweepPath
from engine.linear_combination import LinearCombination
from engine.linear_combination_geometry import LinearCombinationGeometry
from engine.linear_combination_geometry_display import (
    LinearCombinationGeometryDisplayAdapter,
)
from engine.linear_combination_geometry_path import LinearCombinationGeometryPath
from engine.linear_combination_trace import LinearCombinationTrace
from engine.linear_combination_trace_display import (
    LinearCombinationTraceDisplayAdapter,
)
from engine.manim_linear_combination_geometry import (
    ManimLinearCombinationGeometry,
)
from engine.manim_linear_combination_trace import ManimLinearCombinationTrace
from engine.rank_collapse_display import LinearDisplayProjector


SMOKE_VECTORS = np.array(
    [
        [2.0, 1.0],
        [-1.0, 2.0],
    ],
    dtype=float,
)
SMOKE_START_COEFFICIENTS = np.array([0.0, 0.0], dtype=float)
SMOKE_END_COEFFICIENTS = np.array([1.25, -0.75], dtype=float)
TRACE_SAMPLE_COUNT = 33
TRACE_PROGRESS_VALUES = np.linspace(
    0.0,
    1.0,
    TRACE_SAMPLE_COUNT,
    dtype=float,
)
TRACE_PROGRESS_VALUES.setflags(write=False)


@dataclass(frozen=True)
class LinearCombinationTraceSmokePipeline:
    """Objects composing the mathematical-to-Manim smoke-scene pipeline."""

    combination: LinearCombination
    coefficient_path: CoefficientSweepPath
    geometry: LinearCombinationGeometry
    geometry_path: LinearCombinationGeometryPath
    projector: LinearDisplayProjector
    display_path: LinearCombinationGeometryDisplayAdapter
    trace: LinearCombinationTrace
    trace_display_adapter: LinearCombinationTraceDisplayAdapter


def build_linear_combination_trace_smoke_pipeline() -> LinearCombinationTraceSmokePipeline:
    """Build the complete moving-geometry and fixed-trace display pipeline."""

    combination = LinearCombination(SMOKE_VECTORS)
    coefficient_path = CoefficientSweepPath(
        combination,
        SMOKE_START_COEFFICIENTS,
        SMOKE_END_COEFFICIENTS,
    )
    geometry = LinearCombinationGeometry()
    geometry_path = LinearCombinationGeometryPath(coefficient_path, geometry)
    projector = LinearDisplayProjector(np.eye(2, dtype=float))
    display_path = LinearCombinationGeometryDisplayAdapter(
        geometry_path,
        projector,
    )

    trace = LinearCombinationTrace(
        geometry_path.snapshot(float(progress))
        for progress in TRACE_PROGRESS_VALUES
    )
    trace_display_adapter = LinearCombinationTraceDisplayAdapter(
        trace,
        projector,
    )

    return LinearCombinationTraceSmokePipeline(
        combination=combination,
        coefficient_path=coefficient_path,
        geometry=geometry,
        geometry_path=geometry_path,
        projector=projector,
        display_path=display_path,
        trace=trace,
        trace_display_adapter=trace_display_adapter,
    )


def update_linear_combination_mobject(
    mobject: ManimLinearCombinationGeometry,
    display_path: LinearCombinationGeometryDisplayAdapter,
    progress: float,
) -> ManimLinearCombinationGeometry:
    """Request one display snapshot and update the existing arrow mobjects."""

    return mobject.update_from_snapshot(display_path.snapshot(progress))


class LinearCombinationTraceSmoke(Scene):
    """Animate linear-combination arrows over their completed resultant trace."""

    def construct(self) -> None:
        plane = NumberPlane(
            x_range=(-5.0, 5.0, 1.0),
            y_range=(-3.5, 3.5, 1.0),
            background_line_style={"stroke_opacity": 0.35},
        )
        title = Text(
            "Resultant trace of a coefficient sweep",
            font_size=30,
        ).to_edge(UP)

        pipeline = build_linear_combination_trace_smoke_pipeline()

        trace = ManimLinearCombinationTrace(
            pipeline.trace_display_adapter.snapshot(),
            segment_kwargs={"stroke_width": 5.0},
        )
        trace.set_color(ORANGE)
        trace.set_opacity(0.75)

        arrows = ManimLinearCombinationGeometry(
            pipeline.display_path.snapshot(0.0),
            term_arrow_kwargs={"stroke_width": 6.0},
            resultant_arrow_kwargs={"stroke_width": 8.0},
        )
        for arrow, color in zip(
            arrows.term_arrows,
            (BLUE_C, GREEN_C),
            strict=True,
        ):
            arrow.set_color(color)
        arrows.resultant_arrow.set_color(YELLOW)

        self.play(FadeIn(plane), FadeIn(title))
        self.play(FadeIn(trace))
        self.add(arrows)
        self.wait(0.25)
        self.play(
            UpdateFromAlphaFunc(
                arrows,
                lambda mobject, alpha: update_linear_combination_mobject(
                    mobject,
                    pipeline.display_path,
                    alpha,
                ),
            ),
            run_time=4.0,
            rate_func=linear,
        )
        self.wait(1.0)
