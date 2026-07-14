"""Smoke scene for the complete linear-combination display pipeline.

Checkpoint 15 intentionally contains only scene orchestration.  Coefficient
interpolation, linear-combination mathematics, tip-to-tail geometry, and
display projection remain in their renderer-independent engine layers.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import (
    BLUE_C,
    GREEN_C,
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
from engine.manim_linear_combination_geometry import (
    ManimLinearCombinationGeometry,
)
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


@dataclass(frozen=True)
class LinearCombinationSmokePipeline:
    """Objects composing the renderer-independent smoke-scene pipeline."""

    combination: LinearCombination
    coefficient_path: CoefficientSweepPath
    geometry: LinearCombinationGeometry
    geometry_path: LinearCombinationGeometryPath
    projector: LinearDisplayProjector
    display_path: LinearCombinationGeometryDisplayAdapter


def build_linear_combination_smoke_pipeline() -> LinearCombinationSmokePipeline:
    """Build the complete mathematical-to-display path used by the scene."""

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

    return LinearCombinationSmokePipeline(
        combination=combination,
        coefficient_path=coefficient_path,
        geometry=geometry,
        geometry_path=geometry_path,
        projector=projector,
        display_path=display_path,
    )


def update_linear_combination_mobject(
    mobject: ManimLinearCombinationGeometry,
    display_path: LinearCombinationGeometryDisplayAdapter,
    progress: float,
) -> ManimLinearCombinationGeometry:
    """Request one display snapshot and apply it to existing Manim arrows."""

    return mobject.update_from_snapshot(display_path.snapshot(progress))


class LinearCombinationGeometrySmoke(Scene):
    """Animate two coefficient-scaled vectors and their resultant."""

    def construct(self) -> None:
        plane = NumberPlane(
            x_range=(-5.0, 5.0, 1.0),
            y_range=(-3.5, 3.5, 1.0),
            background_line_style={"stroke_opacity": 0.35},
        )
        title = Text(
            "Linear combination coefficient sweep",
            font_size=30,
        ).to_edge(UP)

        pipeline = build_linear_combination_smoke_pipeline()
        initial_snapshot = pipeline.display_path.snapshot(0.0)
        arrows = ManimLinearCombinationGeometry(
            initial_snapshot,
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
