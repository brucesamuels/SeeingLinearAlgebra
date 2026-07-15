"""Smoke scene for the complete linear-combination presentation pipeline.

Checkpoint 22 composes the established completed resultant trace, moving
linear-combination arrows, and synchronized coefficient/result readout in one
lesson-like frame.  The trace is sampled and projected once upstream.  Each
animation frame then requests exactly one
``LinearCombinationGeometryDisplaySnapshot``; the arrow adapter consumes its
projected geometry and the readout consumes its exact retained mathematical
snapshot.

No coefficient interpolation, vector arithmetic, tip-to-tail construction,
trace construction, or display projection is reproduced in this scene.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import (
    BLUE_C,
    DOWN,
    GREEN_C,
    LEFT,
    ORANGE,
    UR,
    YELLOW,
    FadeIn,
    NumberPlane,
    Scene,
    Text,
    UP,
    UpdateFromAlphaFunc,
    VGroup,
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
from engine.manim_linear_combination_readout import (
    ManimLinearCombinationReadout,
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
class LinearCombinationPresentationSmokePipeline:
    """Objects composing the complete smoke-scene presentation pipeline."""

    combination: LinearCombination
    coefficient_path: CoefficientSweepPath
    geometry: LinearCombinationGeometry
    geometry_path: LinearCombinationGeometryPath
    projector: LinearDisplayProjector
    display_path: LinearCombinationGeometryDisplayAdapter
    trace: LinearCombinationTrace
    trace_display_adapter: LinearCombinationTraceDisplayAdapter


def build_linear_combination_presentation_smoke_pipeline(
) -> LinearCombinationPresentationSmokePipeline:
    """Build the shared moving-geometry and completed-trace pipeline."""

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

    return LinearCombinationPresentationSmokePipeline(
        combination=combination,
        coefficient_path=coefficient_path,
        geometry=geometry,
        geometry_path=geometry_path,
        projector=projector,
        display_path=display_path,
        trace=trace,
        trace_display_adapter=trace_display_adapter,
    )


def update_linear_combination_presentation(
    mobject: VGroup,
    arrows: ManimLinearCombinationGeometry,
    readout: ManimLinearCombinationReadout,
    display_path: LinearCombinationGeometryDisplayAdapter,
    progress: float,
) -> VGroup:
    """Update moving presentation components from one shared frame snapshot.

    The completed trace is deliberately absent from this helper because its
    fixed line mobjects are constructed once and remain unchanged.
    """

    display_snapshot = display_path.snapshot(progress)
    arrows.update_from_snapshot(display_snapshot)
    readout.update_from_snapshot(display_snapshot.linear_combination_snapshot)
    return mobject


class LinearCombinationPresentationSmoke(Scene):
    """Show trace, moving arrows, and readout in one synchronized frame."""

    def construct(self) -> None:
        plane = NumberPlane(
            x_range=(-5.0, 5.0, 1.0),
            y_range=(-3.5, 3.5, 1.0),
            background_line_style={"stroke_opacity": 0.35},
        )
        title = Text(
            "A coefficient sweep in three synchronized views",
            font_size=30,
        ).to_edge(UP)

        pipeline = build_linear_combination_presentation_smoke_pipeline()
        trace_display_snapshot = pipeline.trace_display_adapter.snapshot()
        initial_display_snapshot = pipeline.display_path.snapshot(0.0)

        trace = ManimLinearCombinationTrace(
            trace_display_snapshot,
            segment_kwargs={"stroke_width": 5.0},
        )
        trace.set_color(ORANGE)
        trace.set_opacity(0.70)

        arrows = ManimLinearCombinationGeometry(
            initial_display_snapshot,
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

        readout = ManimLinearCombinationReadout(
            initial_display_snapshot.linear_combination_snapshot,
            num_decimal_places=2,
            include_sign=True,
            label_kwargs={"font_size": 30},
            matrix_kwargs={"v_buff": 0.35, "h_buff": 0.55},
        )
        readout.scale(0.72)
        readout.to_corner(UR)
        readout.shift(0.80 * DOWN + 0.20 * LEFT)

        animated_mobjects = VGroup(arrows, readout)

        self.play(FadeIn(plane), FadeIn(title))
        self.play(FadeIn(trace), FadeIn(animated_mobjects))
        self.wait(0.25)
        self.play(
            UpdateFromAlphaFunc(
                animated_mobjects,
                lambda mobject, alpha: update_linear_combination_presentation(
                    mobject,
                    arrows,
                    readout,
                    pipeline.display_path,
                    alpha,
                ),
            ),
            run_time=4.0,
            rate_func=linear,
        )
        self.wait(1.0)
