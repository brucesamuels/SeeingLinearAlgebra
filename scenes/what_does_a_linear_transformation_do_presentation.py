"""CP82: geometry-first introduction to transformations."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    BLUE,
    Circle,
    DOWN,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    Line,
    ORIGIN,
    Polygon,
    RED,
    ReplacementTransform,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    linear,
)

from engine.planar_affine_transformation import (
    CANDIDATE_TRANSFORMATIONS,
    PlanarAffineSnapshot,
    PlanarTransformationGeometry,
)


TITLE = "What Does a Linear Transformation Do?"
PREDICTION_QUESTION = "Which of these preserve the linear structure?"
CLOSING_STATEMENT = "A linear transformation must fix the origin."
CLOSING_QUESTION = "What additional properties must it preserve?"

E1_COLOR = BLUE
E2_COLOR = GREEN
FIGURE_COLOR = YELLOW
ORIGIN_COLOR = RED
GRID_COLOR = "#46515F"
MUTED_COLOR = "#A7B0BA"


def _p(point: np.ndarray) -> np.ndarray:
    return np.array((point[0], point[1], 0.0), dtype=float)


class TransformationStage(VGroup):
    """Thin Manim adapter for one renderer-independent snapshot."""

    def __init__(self, snapshot: PlanarAffineSnapshot) -> None:
        self.grid_lines = VGroup(
            *[
                Line(_p(segment[0]), _p(segment[1]), color=GRID_COLOR, stroke_width=1.1)
                for segment in snapshot.grid_segments
            ]
        )
        self.origin_dot = Dot(_p(snapshot.origin), color=ORIGIN_COLOR, radius=0.075)
        self.origin_ring = Circle(radius=0.16, color=ORIGIN_COLOR, stroke_width=2).move_to(
            _p(snapshot.origin)
        )
        self.e1_arrow = Arrow(
            ORIGIN, _p(snapshot.basis_endpoints[0]), buff=0, color=E1_COLOR, stroke_width=5
        )
        self.e2_arrow = Arrow(
            ORIGIN, _p(snapshot.basis_endpoints[1]), buff=0, color=E2_COLOR, stroke_width=5
        )
        self.vector_arrow = Arrow(
            ORIGIN,
            _p(snapshot.vector_endpoints[0]),
            buff=0,
            color=WHITE,
            stroke_width=4,
        )
        self.figure = Polygon(
            *[_p(vertex) for vertex in snapshot.polygon_vertices],
            color=FIGURE_COLOR,
            fill_color=FIGURE_COLOR,
            fill_opacity=0.22,
            stroke_width=3,
        )
        super().__init__(
            self.grid_lines,
            self.figure,
            self.e1_arrow,
            self.e2_arrow,
            self.vector_arrow,
            self.origin_ring,
            self.origin_dot,
        )
        self._snapshot = snapshot

    @property
    def snapshot(self) -> PlanarAffineSnapshot:
        return self._snapshot

    def update_from_snapshot(self, snapshot: PlanarAffineSnapshot) -> None:
        for line, segment in zip(self.grid_lines, snapshot.grid_segments, strict=True):
            line.put_start_and_end_on(_p(segment[0]), _p(segment[1]))
        self.update_objects_from_snapshot(snapshot)

    def update_objects_from_snapshot(self, snapshot: PlanarAffineSnapshot) -> None:
        """Update vectors, origin marker, and figure while leaving the grid unchanged."""
        # In the translation example the coordinate origin remains fixed.
        # A separate image-of-origin marker is used when needed.
        self.origin_dot.move_to(_p(snapshot.origin))
        self.origin_ring.move_to(_p(snapshot.origin))
        self.e1_arrow.put_start_and_end_on(_p(snapshot.origin), _p(snapshot.basis_endpoints[0]))
        self.e2_arrow.put_start_and_end_on(_p(snapshot.origin), _p(snapshot.basis_endpoints[1]))
        self.vector_arrow.put_start_and_end_on(
            _p(snapshot.origin), _p(snapshot.vector_endpoints[0])
        )
        self.figure.set_points_as_corners(
            [_p(vertex) for vertex in snapshot.polygon_vertices]
            + [_p(snapshot.polygon_vertices[0])]
        )
        self._snapshot = snapshot


class WhatDoesALinearTransformationDoPresentation(Scene):
    """Survey several geometric actions before formally defining linearity."""

    def construct(self) -> None:
        geometry = PlanarTransformationGeometry(
            vector_endpoints=((2.2, 1.2),),
            polygon_vertices=(
                (-1.8, -0.9),
                (-0.2, -0.9),
                (-0.2, 0.25),
                (-1.0, 1.05),
                (-1.8, 0.25),
            ),
            grid_extent=4,
        )
        identity = CANDIDATE_TRANSFORMATIONS[0][1].interpolate(0.0)
        initial = geometry.snapshot(identity)
        stage = TransformationStage(initial).scale(0.78).shift(0.4 * RIGHT + 0.15 * DOWN)

        title = Text(TITLE, font_size=40, color=WHITE).to_edge(UP, buff=0.35)
        subtitle = Text(
            "Watch the whole plane—not only one vector.",
            font_size=24,
            color=MUTED_COLOR,
        ).next_to(title, DOWN, buff=0.18)

        self.play(FadeIn(title), FadeIn(subtitle))
        self.play(Create(stage.grid_lines), FadeIn(stage.figure))
        self.play(
            FadeIn(stage.e1_arrow),
            FadeIn(stage.e2_arrow),
            FadeIn(stage.vector_arrow),
            FadeIn(stage.origin_ring),
            FadeIn(stage.origin_dot),
        )
        self.wait(1.5)

        for name, transformation in CANDIDATE_TRANSFORMATIONS:
            label = Text(name, font_size=34, color=WHITE)
            origin_note = Text(
                "origin fixed" if transformation.fixes_origin else "origin moves",
                font_size=25,
                color=MUTED_COLOR if transformation.fixes_origin else ORIGIN_COLOR,
            )
            transformation_caption = VGroup(label, origin_note).arrange(
                DOWN,
                aligned_edge=LEFT,
                buff=0.12,
            )
            transformation_caption.to_corner(LEFT + UP, buff=0.55)
            transformation_caption.shift(0.55 * DOWN)
            self.play(FadeIn(transformation_caption))
            tracker = stage.copy()
            transformed_snapshot = geometry.snapshot(transformation, 1.0)
            if name == "Translation":
                # Keep coordinate origin fixed; display translated tail as T(0).
                tracker.update_objects_from_snapshot(transformed_snapshot)
            else:
                tracker.update_from_snapshot(transformed_snapshot)
            self.play(ReplacementTransform(stage, tracker), run_time=2.1, rate_func=linear)
            stage = tracker
            self.play(FadeIn(origin_note))
            self.wait(1.0 if name != "Translation" else 1.8)
            self.play(FadeOut(origin_note))
            reset = TransformationStage(initial).scale(0.78).shift(0.4 * RIGHT + 0.15 * DOWN)
            self.play(
                ReplacementTransform(stage, reset),
                FadeOut(transformation_caption),
                run_time=1.2,
            )
            stage = reset

        prompt = VGroup(
            Text("Pause and Predict", font_size=30, color=YELLOW),
            Text(PREDICTION_QUESTION, font_size=27, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        prompt.to_corner(LEFT + UP, buff=0.55)
        prompt.shift(0.55 * DOWN)
        self.play(FadeIn(prompt))
        self.wait(3.0)
        self.play(FadeOut(prompt))

        statement = Text(CLOSING_STATEMENT, font_size=31, color=WHITE)
        question = Text(CLOSING_QUESTION, font_size=28, color=YELLOW)
        conclusion = VGroup(statement, question).arrange(DOWN, buff=0.24)
        conclusion.to_edge(DOWN, buff=0.42)
        self.play(FadeIn(conclusion))
        self.wait(3.5)
