"""Checkpoint 71: one direction, two directions, and three-dimensional space."""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow3D,
    Create,
    DEGREES,
    Dot3D,
    DOWN,
    FadeIn,
    FadeOut,
    LaggedStart,
    LEFT,
    MathTex,
    Polygon,
    RIGHT,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
)

from engine.dimension_growth import DimensionGrowth
from engine.manim_dimension_growth import ManimDimensionGrowth

LESSON_QUESTION = "What can three vectors create in 3-space?"
LINE_IDEA = "One direction generates a line."
PLANE_IDEA = "A second independent direction generates a plane."
PREDICTION = "Will the third vector create a new dimension,\nor only move us within the old one?"
SPACE_IDEA = "A direction outside the plane moves the entire plane."
KEY_IDEA = "The span grows only when a vector adds a new direction."
FORMAL_SPAN = r"\operatorname{span}\{\mathbf u,\mathbf v,\mathbf w\}=\mathbb R^3"

U = np.array([2.0, 0.2, 0.0])
V = np.array([-0.45, 1.55, 0.0])
W = np.array([0.35, 0.25, 1.65])

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#9AA4B2"
ACCENT = "#4FC3F7"
U_COLOR = "#5DADE2"
V_COLOR = "#AF7AC5"
W_COLOR = "#F6C85F"
PLANE_COLOR = "#55D6BE"
SPACE_COLOR = "#F4A261"


class DimensionGrowthPresentation(ThreeDScene):
    """Build span visually from a line to a plane to three-dimensional space."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.92)

        model = DimensionGrowth(U, V, W)
        snapshot = model.snapshot(0.0)

        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-4, 4, 1),
            z_range=(-3, 3, 1),
            x_length=8.5,
            y_length=6.8,
            z_length=5.0,
            axis_config={"color": MUTED, "stroke_opacity": 0.55},
        )

        def map_point(coordinates: np.ndarray) -> np.ndarray:
            return axes.c2p(*coordinates)

        display = ManimDimensionGrowth(
            snapshot,
            map_point,
            u_kwargs={"color": U_COLOR, "thickness": 0.035, "height": 0.22, "base_radius": 0.075},
            v_kwargs={"color": V_COLOR, "thickness": 0.035, "height": 0.22, "base_radius": 0.075},
            w_kwargs={"color": W_COLOR, "thickness": 0.035, "height": 0.22, "base_radius": 0.075},
            plane_kwargs={
                "color": PLANE_COLOR,
                "fill_color": PLANE_COLOR,
                "fill_opacity": 0.18,
                "stroke_opacity": 0.38,
                "stroke_width": 1.4,
            },
        )

        title = Text(LESSON_QUESTION, font_size=38, color=TEXT).to_edge(UP, buff=0.28)
        line_idea = Text(LINE_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.32)
        plane_idea = Text(PLANE_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.32)
        prediction = VGroup(
            Text("PAUSE AND PREDICT", font_size=20, color=ACCENT),
            Text(PREDICTION, font_size=27, color=TEXT, line_spacing=0.9),
        ).arrange(DOWN, buff=0.12, aligned_edge=RIGHT).to_corner(UP + RIGHT, buff=0.45).shift(DOWN * 0.65)
        space_idea = Text(SPACE_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.32)
        key_idea = Text(KEY_IDEA, font_size=25, color=MUTED).to_edge(DOWN, buff=0.72)
        span_label = MathTex(FORMAL_SPAN, font_size=38, color=TEXT).to_edge(DOWN, buff=0.25)

        u_label = MathTex(r"\mathbf u", font_size=34, color=U_COLOR).move_to(map_point(U) + UP * 0.18)
        v_label = MathTex(r"\mathbf v", font_size=34, color=V_COLOR).move_to(map_point(V) + UP * 0.18)
        w_label = MathTex(r"\mathbf w", font_size=34, color=W_COLOR).move_to(map_point(W) + RIGHT * 0.18)

        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), Create(axes), run_time=1.5)

        # Stage 1: scalar multiples of u create a line.
        line_coefficients = np.linspace(-2.25, 2.25, 31)
        line_dots = display.dots_for(
            model.line_points(line_coefficients),
            radius=0.035,
            color=U_COLOR,
            fill_opacity=0.78,
        )
        self.play(Create(display.u_arrow), FadeIn(u_label))
        self.play(LaggedStart(*(FadeIn(dot) for dot in line_dots), lag_ratio=0.025), run_time=1.8)
        self.add_fixed_in_frame_mobjects(line_idea)
        self.play(FadeIn(line_idea, shift=UP * 0.12))
        self.wait(1.4)
        self.play(FadeOut(line_idea))

        # Stage 2: two independent directions create a plane.
        values = np.linspace(-2.0, 2.0, 13)
        plane_pairs = np.array([(a, b) for a in values for b in values], dtype=float)
        plane_dots = display.dots_for(
            model.plane_points(plane_pairs),
            radius=0.025,
            color=PLANE_COLOR,
            fill_opacity=0.42,
        )
        base_plane = Polygon(
            *(map_point(corner) for corner in snapshot.plane_corners),
            color=PLANE_COLOR,
            fill_color=PLANE_COLOR,
            fill_opacity=0.13,
            stroke_opacity=0.32,
            stroke_width=1.2,
        )
        self.play(Create(display.v_arrow), FadeIn(v_label))
        self.play(
            FadeOut(line_dots),
            FadeIn(base_plane),
            LaggedStart(*(FadeIn(dot) for dot in plane_dots), lag_ratio=0.006),
            run_time=2.3,
        )
        self.add_fixed_in_frame_mobjects(plane_idea)
        self.play(FadeIn(plane_idea, shift=UP * 0.12))
        self.wait(1.5)
        self.play(FadeOut(plane_idea))

        self.add_fixed_in_frame_mobjects(prediction)
        self.play(FadeIn(prediction, shift=LEFT * 0.12))
        self.wait(2.5)
        self.play(FadeOut(prediction))

        # Stage 3: w lies outside span{u,v}; copies of the plane at different
        # w-coefficients stack through space.
        self.play(Create(display.w_arrow), FadeIn(w_label))
        layer_coefficients = np.linspace(-1.55, 1.55, 9)
        layers = VGroup()
        for coefficient in layer_coefficients:
            layer_snapshot = model.snapshot(float(coefficient))
            layers.add(
                Polygon(
                    *(map_point(corner) for corner in layer_snapshot.translated_plane_corners),
                    color=PLANE_COLOR,
                    fill_color=PLANE_COLOR,
                    fill_opacity=0.065,
                    stroke_opacity=0.25,
                    stroke_width=1.0,
                )
            )

        self.play(
            LaggedStart(*(FadeIn(layer) for layer in layers), lag_ratio=0.12),
            run_time=3.1,
        )

        space_values = np.linspace(-1.6, 1.6, 7)
        triples = np.array(
            [(a, b, c) for a in space_values for b in space_values for c in space_values],
            dtype=float,
        )
        space_dots = display.dots_for(
            model.space_points(triples),
            radius=0.018,
            color=SPACE_COLOR,
            fill_opacity=0.28,
        )
        self.play(FadeIn(space_dots), run_time=1.8)
        self.add_fixed_in_frame_mobjects(space_idea)
        self.play(FadeIn(space_idea, shift=UP * 0.12))
        self.begin_ambient_camera_rotation(rate=0.08)
        self.wait(2.5)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(space_idea))

        self.add_fixed_in_frame_mobjects(key_idea, span_label)
        self.play(FadeIn(key_idea))
        self.play(FadeIn(span_label, shift=UP * 0.12))
        self.wait(2.5)
