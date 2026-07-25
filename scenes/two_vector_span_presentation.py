"""Checkpoint 69: two independent vectors sweep out a plane."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Create,
    DEGREES,
    DecimalNumber,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    LaggedStart,
    Line,
    MathTex,
    NumberPlane,
    Polygon,
    RIGHT,
    Text,
    ThreeDScene,
    TracedPath,
    UP,
    ValueTracker,
    VGroup,
    linear,
)

from engine.manim_two_vector_span import (
    ManimFixedCoefficientLine,
    ManimTwoVectorCombination,
)
from engine.two_vector_span import TwoVectorSpan


LESSON_QUESTION = "What changes when we add a second direction?"
PREDICTION_PROMPT = "Will the combinations leave gaps,\nform a grid, or fill the plane?"
FIRST_DISCOVERY = "Fix a.  Varying b traces one line parallel to v."
SECOND_DISCOVERY = "Changing a moves the entire line in the u direction."
SPAN_DEFINITION = (
    r"\operatorname{span}\{\mathbf u,\mathbf v\}="
    r"\{a\mathbf u+b\mathbf v:a,b\in\mathbb R\}"
)
KEY_IDEA = "Two independent directions generate the entire plane."
REFLECTION_PROMPT = "Why does every point in the plane have a recipe a u + b v?"

GENERATOR_U = np.array([2.0, 0.65])
GENERATOR_V = np.array([-0.55, 1.55])
B_EXTENT = 2.5
A_EXTENT = 2.25

BACKGROUND = "#0A0D13"
GRID = "#3A4256"
TEXT = "#E8EAED"
MUTED = "#9AA4B2"
ACCENT = "#4FC3F7"
U_COLOR = "#5DADE2"
V_COLOR = "#AF7AC5"
COMBINATION_COLOR = "#F6C85F"
FAMILY_COLOR = "#55D6BE"
ENDPOINT_COLOR = "#55D6BE"


class TwoVectorSpanPresentation(ThreeDScene):
    """Reveal a plane as a continuously translated family of parallel lines."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

        model = TwoVectorSpan(GENERATOR_U, GENERATOR_V)
        coefficient_a = ValueTracker(0.0)
        coefficient_b = ValueTracker(-B_EXTENT)

        title = Text(LESSON_QUESTION, font_size=38, color=TEXT).to_edge(UP, buff=0.32)
        plane = NumberPlane(
            x_range=(-7, 7, 1),
            y_range=(-4, 4, 1),
            x_length=12.5,
            y_length=7.0,
            background_line_style={
                "stroke_color": GRID,
                "stroke_width": 1.0,
                "stroke_opacity": 0.40,
            },
            axis_config={"stroke_color": MUTED, "stroke_width": 2.0},
        ).shift(DOWN * 0.25)

        def map_point(coordinates: np.ndarray) -> np.ndarray:
            return plane.c2p(*coordinates)

        origin = map_point(np.zeros(2))
        u_endpoint = map_point(GENERATOR_U)
        v_endpoint = map_point(GENERATOR_V)
        u_arrow = Arrow(origin, u_endpoint, buff=0.0, color=U_COLOR, stroke_width=7)
        v_arrow = Arrow(origin, v_endpoint, buff=0.0, color=V_COLOR, stroke_width=7)
        u_label = MathTex(r"\mathbf u", font_size=38, color=U_COLOR).next_to(u_endpoint, DOWN, buff=0.12)
        v_label = MathTex(r"\mathbf v", font_size=38, color=V_COLOR).next_to(v_endpoint, LEFT, buff=0.12)

        moving = ManimTwoVectorCombination(
            model.snapshot(coefficient_a.get_value(), coefficient_b.get_value()),
            map_point,
            arrow_kwargs={"color": COMBINATION_COLOR, "stroke_width": 8, "tip_length": 0.24},
            dot_kwargs={"color": TEXT, "radius": 0.065},
        )
        moving.mobject.add_updater(
            lambda _mob: moving.update_from_snapshot(
                model.snapshot(coefficient_a.get_value(), coefficient_b.get_value())
            )
        )

        moving_line = ManimFixedCoefficientLine(
            model.fixed_u_line(coefficient_a.get_value(), -B_EXTENT, B_EXTENT),
            map_point,
            line_kwargs={"color": FAMILY_COLOR, "stroke_width": 6},
        )
        moving_line.line.add_updater(
            lambda _line: moving_line.update_from_snapshot(
                model.fixed_u_line(coefficient_a.get_value(), -B_EXTENT, B_EXTENT)
            )
        )

        a_number = DecimalNumber(0.0, num_decimal_places=2, include_sign=True, font_size=30, color=U_COLOR)
        b_number = DecimalNumber(-B_EXTENT, num_decimal_places=2, include_sign=True, font_size=30, color=V_COLOR)
        a_number.add_updater(lambda number: number.set_value(coefficient_a.get_value()))
        b_number.add_updater(lambda number: number.set_value(coefficient_b.get_value()))
        readout = VGroup(
            MathTex(r"a=", font_size=30, color=TEXT),
            a_number,
            MathTex(r"\qquad b=", font_size=30, color=TEXT),
            b_number,
        ).arrange(RIGHT, buff=0.08).to_corner(UP + RIGHT, buff=0.42).shift(DOWN * 0.56)

        prediction = VGroup(
            Text("PAUSE AND PREDICT", font_size=20, color=ACCENT),
            Text(PREDICTION_PROMPT, font_size=28, color=TEXT, line_spacing=0.9),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        prediction.to_corner(UP + LEFT, buff=0.5).shift(DOWN * 0.7)

        endpoint_trace = TracedPath(
            moving.endpoint_dot.get_center,
            stroke_color=FAMILY_COLOR,
            stroke_width=6,
        )

        first_discovery = Text(FIRST_DISCOVERY, font_size=27, color=MUTED).to_edge(DOWN, buff=0.32)
        second_discovery = Text(SECOND_DISCOVERY, font_size=27, color=MUTED).to_edge(DOWN, buff=0.32)
        definition = MathTex(SPAN_DEFINITION, font_size=34, color=TEXT).to_edge(DOWN, buff=0.30)
        key_idea = Text(KEY_IDEA, font_size=24, color=MUTED).next_to(definition, UP, buff=0.32)

        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), Create(plane))
        self.play(Create(u_arrow), FadeIn(u_label), Create(v_arrow), FadeIn(v_label))

        self.add_fixed_in_frame_mobjects(prediction)
        self.play(FadeIn(prediction, shift=RIGHT * 0.15))
        self.wait(2.5)
        self.play(FadeOut(prediction))

        # Stage 1: with a fixed at zero, b moves continuously and its endpoint
        # reveals one line before the completed line object is introduced.
        self.add(endpoint_trace)
        self.add_fixed_in_frame_mobjects(readout)
        self.play(FadeIn(moving.mobject), FadeIn(readout))
        self.play(coefficient_b.animate.set_value(B_EXTENT), run_time=4.0, rate_func=linear)
        self.play(FadeOut(endpoint_trace), Create(moving_line.line), run_time=1.2)
        self.add_fixed_in_frame_mobjects(first_discovery)
        self.play(FadeIn(first_discovery, shift=UP * 0.12))
        self.wait(1.8)
        self.play(FadeOut(first_discovery))

        # Keep the whole line visible while the active point returns to b = 0.
        self.play(coefficient_b.animate.set_value(0.0), run_time=1.6, rate_func=linear)

        # Stage 2: moving a translates the entire b-line.  Retained samples make
        # the swept plane visible without replacing the continuous motion.
        retained_lines = VGroup()
        sample_values = np.linspace(-A_EXTENT, A_EXTENT, 17)
        for sample in sample_values:
            snapshot = model.fixed_u_line(float(sample), -B_EXTENT, B_EXTENT)
            retained_lines.add(
                Line(
                    map_point(snapshot.start),
                    map_point(snapshot.end),
                    color=FAMILY_COLOR,
                    stroke_width=2.1,
                    stroke_opacity=0.30,
                )
            )

        self.play(coefficient_a.animate.set_value(-A_EXTENT), run_time=2.4, rate_func=linear)
        for sample, retained in zip(sample_values, retained_lines):
            self.play(
                coefficient_a.animate.set_value(float(sample)),
                FadeIn(retained),
                run_time=0.30,
                rate_func=linear,
            )
        self.play(coefficient_a.animate.set_value(A_EXTENT), run_time=1.0, rate_func=linear)
        self.add_fixed_in_frame_mobjects(second_discovery)
        self.play(FadeIn(second_discovery, shift=UP * 0.12))
        self.wait(2.0)

        # Final visual resolution: each location is an endpoint of some
        # coefficient pair (a, b).  A sparse pass preserves the line-by-line
        # construction; an offset dense pass then closes the visual gaps.
        coefficient_a_values = np.linspace(-4.60, 4.60, 31)
        coefficient_b_values = np.linspace(-4.60, 4.60, 41)
        sparse_strips = VGroup()
        for a_value in coefficient_a_values:
            pairs = np.column_stack(
                (
                    np.full(coefficient_b_values.shape, a_value),
                    coefficient_b_values,
                )
            )
            strip = VGroup(
                *(
                    Dot(
                        map_point(endpoint),
                        radius=0.026,
                        color=ENDPOINT_COLOR,
                        fill_opacity=0.62,
                        stroke_width=0,
                    )
                    for endpoint in model.endpoints_for(pairs)
                )
            )
            sparse_strips.add(strip)

        a_step = float(coefficient_a_values[1] - coefficient_a_values[0])
        b_step = float(coefficient_b_values[1] - coefficient_b_values[0])
        dense_a_values = coefficient_a_values[:-1] + 0.5 * a_step
        dense_b_values = coefficient_b_values[:-1] + 0.5 * b_step
        dense_pairs = np.array(
            [(a_value, b_value) for a_value in dense_a_values for b_value in dense_b_values],
            dtype=float,
        )
        dense_endpoint_field = VGroup(
            *(
                Dot(
                    map_point(endpoint),
                    radius=0.018,
                    color=ENDPOINT_COLOR,
                    fill_opacity=0.46,
                    stroke_width=0,
                )
                for endpoint in model.endpoints_for(dense_pairs)
            )
        )

        # The final solid plane is still created from the same basis vectors.
        # In this revision, a 3D camera move reveals that the entire coordinate
        # world is one plane, without adding a third axis.
        plane_extent = 5.75
        plane_corners = model.endpoints_for(
            np.array(
                [
                    [-plane_extent, -plane_extent],
                    [plane_extent, -plane_extent],
                    [plane_extent, plane_extent],
                    [-plane_extent, plane_extent],
                ],
                dtype=float,
            )
        )
        solid_span_plane = Polygon(
            *(map_point(corner) for corner in plane_corners),
            color=FAMILY_COLOR,
            fill_color=FAMILY_COLOR,
            fill_opacity=0.26,
            stroke_color=FAMILY_COLOR,
            stroke_width=1.4,
            stroke_opacity=0.24,
        )

        sparse_strips.set_z_index(-1)
        dense_endpoint_field.set_z_index(-1)
        solid_span_plane.set_z_index(-2)
        plane.set_z_index(-3)

        self.play(FadeOut(second_discovery), run_time=0.5)
        self.play(
            LaggedStart(
                *(FadeIn(strip) for strip in sparse_strips),
                lag_ratio=0.045,
            ),
            run_time=2.8,
        )
        self.play(
            FadeIn(dense_endpoint_field),
            FadeOut(retained_lines),
            run_time=2.0,
        )
        self.wait(0.8)

        # Before the plane tilts, remove the completed b-line so the eye sees
        # the span itself rather than one lingering construction artifact.
        self.play(
            FadeIn(solid_span_plane),
            FadeOut(moving_line.line),
            run_time=1.4,
        )
        self.play(
            sparse_strips.animate.set_opacity(0.12),
            dense_endpoint_field.animate.set_opacity(0.14),
            run_time=1.1,
        )
        self.move_camera(phi=72 * DEGREES, theta=-58 * DEGREES, zoom=0.95, run_time=2.8)
        self.wait(1.0)

        # Return to a representative combination before naming the set.
        self.play(
            coefficient_a.animate.set_value(1.0),
            coefficient_b.animate.set_value(1.0),
            run_time=2.0,
            rate_func=linear,
        )

        moving.mobject.clear_updaters()
        moving_line.line.clear_updaters()
        a_number.clear_updaters()
        b_number.clear_updaters()
        moving.update_from_snapshot(model.snapshot(1.0, 1.0))
        moving_line.update_from_snapshot(model.fixed_u_line(1.0, -B_EXTENT, B_EXTENT))
        a_number.set_value(1.0)
        b_number.set_value(1.0)

        self.add_fixed_in_frame_mobjects(definition, key_idea)
        self.play(FadeIn(definition, shift=UP * 0.15))
        self.play(FadeIn(key_idea))
        self.wait(2.4)
