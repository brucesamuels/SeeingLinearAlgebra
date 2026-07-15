"""Smoke scene for synchronized linear-combination geometry and readout.

Checkpoint 21 integrates the established moving-arrow adapter with the
Checkpoint 20 coefficient/result readout.  Each animation frame requests one
``LinearCombinationGeometryDisplaySnapshot`` from the renderer-independent
display path.  The arrow adapter consumes its projected geometry, while the
readout consumes the exact retained mathematical snapshot.

No coefficient interpolation, vector arithmetic, tip-to-tail construction, or
display projection is reproduced in this scene.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import (
    BLUE_C,
    DOWN,
    GREEN_C,
    LEFT,
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
from engine.manim_linear_combination_geometry import (
    ManimLinearCombinationGeometry,
)
from engine.manim_linear_combination_readout import (
    ManimLinearCombinationReadout,
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
class LinearCombinationReadoutSmokePipeline:
    """Objects composing the mathematical-to-presentation smoke pipeline."""

    combination: LinearCombination
    coefficient_path: CoefficientSweepPath
    geometry: LinearCombinationGeometry
    geometry_path: LinearCombinationGeometryPath
    projector: LinearDisplayProjector
    display_path: LinearCombinationGeometryDisplayAdapter


def build_linear_combination_readout_smoke_pipeline(
) -> LinearCombinationReadoutSmokePipeline:
    """Build the existing coefficient, geometry, and display pipeline."""

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

    return LinearCombinationReadoutSmokePipeline(
        combination=combination,
        coefficient_path=coefficient_path,
        geometry=geometry,
        geometry_path=geometry_path,
        projector=projector,
        display_path=display_path,
    )


def update_linear_combination_mobjects(
    mobject: VGroup,
    arrows: ManimLinearCombinationGeometry,
    readout: ManimLinearCombinationReadout,
    display_path: LinearCombinationGeometryDisplayAdapter,
    progress: float,
) -> VGroup:
    """Update arrows and readout from one shared display snapshot.

    The display path is queried exactly once.  Its projected fields update the
    arrows, and its retained mathematical snapshot updates the numeric readout.
    """

    display_snapshot = display_path.snapshot(progress)
    arrows.update_from_snapshot(display_snapshot)
    readout.update_from_snapshot(display_snapshot.linear_combination_snapshot)
    return mobject


class LinearCombinationReadoutSmoke(Scene):
    """Animate synchronized arrows, coefficients, and resultant coordinates."""

    def construct(self) -> None:
        plane = NumberPlane(
            x_range=(-5.0, 5.0, 1.0),
            y_range=(-3.5, 3.5, 1.0),
            background_line_style={"stroke_opacity": 0.35},
        )
        title = Text(
            "Coefficients and resultant update together",
            font_size=30,
        ).to_edge(UP)

        pipeline = build_linear_combination_readout_smoke_pipeline()
        initial_display_snapshot = pipeline.display_path.snapshot(0.0)

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
        self.play(FadeIn(animated_mobjects))
        self.wait(0.25)
        self.play(
            UpdateFromAlphaFunc(
                animated_mobjects,
                lambda mobject, alpha: update_linear_combination_mobjects(
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
