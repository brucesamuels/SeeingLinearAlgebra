"""CP75: the null space consists of the inputs that disappear."""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Create,
    DEGREES,
    DOWN,
    Dot3D,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    MathTex,
    Polygon,
    RIGHT,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    UpdateFromAlphaFunc,
    VGroup,
    WHITE,
)

from engine.null_space import NullSpace

TITLE = "Inputs That Disappear: The Null Space"
KEY_QUESTION = "Which inputs does A send to 0?"
KEY_IDEA = "Every multiple of the null vector disappears under A."
FINAL_IDEA = "The null space is a subspace of the input space."

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
INPUT_COLOR = "#4FC3F7"
OUTPUT_COLOR = "#81C995"
NULL_COLOR = "#F6C85F"
PLANE_COLOR = "#55D6BE"
ZERO_COLOR = "#F28B82"

MATRIX = np.array([
    [2.0, -0.5, 1.5],
    [0.5, 1.8, 2.3],
    [0.5, 0.8, 1.3],
])

GENERIC_INPUT = np.array([1.1, -0.6, 0.7])


class NullSpacePresentation(ThreeDScene):
    """Contrast generic inputs with the line of inputs that map to zero."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=66 * DEGREES, theta=-50 * DEGREES, zoom=0.90)

        model = NullSpace(MATRIX)
        null_vector = model.null_vector

        input_axes = ThreeDAxes(
            x_range=(-4, 4, 1),
            y_range=(-4, 4, 1),
            z_range=(-4, 4, 1),
            x_length=4.5,
            y_length=4.5,
            z_length=4.0,
        ).shift(LEFT * 3.3)
        output_axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-4, 4, 1),
            x_length=4.8,
            y_length=4.8,
            z_length=4.2,
        ).shift(RIGHT * 3.2)

        title = Text(TITLE, font_size=38, color=TEXT).to_edge(UP, buff=0.28)
        matrix_tex = MathTex(
            r"A=\begin{bmatrix}2&-0.5&1.5\\0.5&1.8&2.3\\0.5&0.8&1.3\end{bmatrix}",
            font_size=34,
            color=WHITE,
        ).to_corner(LEFT + UP, buff=0.42).shift(DOWN * 0.56)
        input_label = MathTex(r"\text{input space }\mathbf x", font_size=32, color=INPUT_COLOR).to_corner(LEFT + UP, buff=0.50).shift(RIGHT * 1.1 + DOWN * 1.55)
        output_label = MathTex(r"\text{output space }A\mathbf x", font_size=32, color=OUTPUT_COLOR).to_corner(RIGHT + UP, buff=0.50).shift(LEFT * 1.0 + DOWN * 1.55)

        self.add_fixed_in_frame_mobjects(title, matrix_tex, input_label, output_label)
        self.play(FadeIn(title), FadeIn(matrix_tex), FadeIn(input_label), FadeIn(output_label))
        self.play(FadeIn(input_axes), FadeIn(output_axes))

        generic_snapshot = model.snapshot(GENERIC_INPUT)
        input_arrow = self._arrow(GENERIC_INPUT, input_axes, INPUT_COLOR)
        output_arrow = self._arrow(generic_snapshot.output_vector, output_axes, OUTPUT_COLOR)
        input_dot = Dot3D(input_axes.c2p(*GENERIC_INPUT), radius=0.055, color=INPUT_COLOR)
        output_dot = Dot3D(output_axes.c2p(*generic_snapshot.output_vector), radius=0.055, color=OUTPUT_COLOR)
        self.play(Create(input_arrow), FadeIn(input_dot), Create(output_arrow), FadeIn(output_dot))

        question = Text(KEY_QUESTION, font_size=28, color=TEXT).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(question)
        self.play(FadeIn(question))
        self.wait(1.8)
        self.play(FadeOut(question))

        grid = np.linspace(-1.5, 1.5, 5)
        output_samples = np.array([(a, b, 0.0) for a in grid for b in grid], dtype=float)
        output_points = model.sample_outputs(output_samples)
        output_field = VGroup(*(
            Dot3D(output_axes.c2p(*point), radius=0.028, color=PLANE_COLOR, fill_opacity=0.46)
            for point in output_points
        ))

        columns = MATRIX.T
        u = columns[0] / np.linalg.norm(columns[0])
        v = columns[1] - np.dot(columns[1], u) * u
        v = v / np.linalg.norm(v)
        extent = 3.1
        corners = [
            -extent * u - extent * v,
            extent * u - extent * v,
            extent * u + extent * v,
            -extent * u + extent * v,
        ]
        output_plane = Polygon(
            *(output_axes.c2p(*point) for point in corners),
            color=PLANE_COLOR,
            fill_color=PLANE_COLOR,
            fill_opacity=0.11,
            stroke_opacity=0.22,
        )
        output_plane.set_z_index(-1)
        self.play(FadeIn(output_plane), FadeIn(output_field), run_time=1.8)

        self.play(FadeOut(input_arrow), FadeOut(input_dot), FadeOut(output_arrow), FadeOut(output_dot), run_time=1.0)

        null_line = self._line(null_vector, input_axes, NULL_COLOR)
        null_samples = model.scalar_multiples(np.linspace(-2.3, 2.3, 11))
        null_dots = VGroup(*(
            Dot3D(input_axes.c2p(*point), radius=0.032, color=NULL_COLOR, fill_opacity=0.58)
            for point in null_samples
        ))
        zero_dot = Dot3D(output_axes.c2p(0.0, 0.0, 0.0), radius=0.072, color=ZERO_COLOR)
        moving_input_segment = Line(
            input_axes.c2p(0, 0, 0),
            input_axes.c2p(*(-2.3 * null_vector)),
            color=NULL_COLOR,
            stroke_width=5,
        )
        moving_input_dot = Dot3D(input_axes.c2p(*(-2.3 * null_vector)), radius=0.060, color=NULL_COLOR)
        null_equation = MathTex(r"A\mathbf n=\mathbf 0", font_size=38, color=TEXT).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(null_equation)

        self.play(FadeIn(null_dots), run_time=1.6)
        self.wait(0.8)
        self.play(Create(null_line), null_dots.animate.set_opacity(0.42), run_time=2.4)
        self.wait(0.8)
        self.play(FadeIn(zero_dot), Create(moving_input_segment), FadeIn(moving_input_dot), run_time=1.3)
        self.play(FadeIn(null_equation))

        def sweep_null_input(_mob, alpha: float) -> None:
            scalar = -2.3 + 4.6 * alpha
            point = scalar * null_vector
            moving_input_dot.move_to(input_axes.c2p(*point))

            # Keep the moving vector geometry non-degenerate at the origin.
            # A flat Line has no arrow-tip subpath to collapse, and the tiny
            # hidden segment guarantees a valid Cairo path on every frame.
            if abs(scalar) < 0.04:
                safe_scalar = 0.04 if scalar >= 0 else -0.04
                safe_point = safe_scalar * null_vector
                moving_input_segment.put_start_and_end_on(
                    input_axes.c2p(0, 0, 0),
                    input_axes.c2p(*safe_point),
                )
                moving_input_segment.set_opacity(0.0)
            else:
                moving_input_segment.put_start_and_end_on(
                    input_axes.c2p(0, 0, 0),
                    input_axes.c2p(*point),
                )
                moving_input_segment.set_opacity(1.0)

        self.play(UpdateFromAlphaFunc(moving_input_dot, sweep_null_input), run_time=9.6)
        self.wait(1.6)

        self.play(FadeOut(null_equation))
        key_idea = Text(KEY_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.40)
        self.add_fixed_in_frame_mobjects(key_idea)
        self.play(FadeIn(key_idea))
        self.wait(1.6)

        null_span = MathTex(
            r"\operatorname{null}(A)=\operatorname{span}\{\mathbf n\}",
            font_size=40,
            color=TEXT,
        ).to_edge(DOWN, buff=0.40)
        self.add_fixed_in_frame_mobjects(null_span)
        self.play(FadeOut(key_idea), FadeIn(null_span))
        self.wait(1.8)

        self.play(
            FadeOut(output_plane), FadeOut(output_field), FadeOut(null_line), FadeOut(null_dots),
            FadeOut(moving_input_segment), FadeOut(moving_input_dot), FadeOut(zero_dot),
            FadeOut(input_axes), FadeOut(output_axes), FadeOut(null_span), FadeOut(matrix_tex),
            FadeOut(input_label), FadeOut(output_label),
        )

        summary = VGroup(
            MathTex(r"\operatorname{null}(A)\text{ contains }\mathbf 0", font_size=39, color=ZERO_COLOR),
            MathTex(r"\mathbf u,\mathbf v\in\operatorname{null}(A)\Rightarrow A(\mathbf u+\mathbf v)=\mathbf 0", font_size=39, color=ZERO_COLOR),
            MathTex(r"c\mathbf u\in\operatorname{null}(A)\Rightarrow A(c\mathbf u)=\mathbf 0", font_size=39, color=ZERO_COLOR),
            MathTex(r"\dim(\operatorname{null}(A))+\operatorname{rank}(A)=1+2=3", font_size=39, color=TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(DOWN * 0.15)
        final_idea = Text(FINAL_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.34)
        self.add_fixed_in_frame_mobjects(summary, final_idea)
        self.play(FadeIn(summary), FadeIn(final_idea))
        self.wait(3.2)

    @staticmethod
    def _arrow(vector: np.ndarray, axes: ThreeDAxes, color: str) -> Arrow:
        return Arrow(
            axes.c2p(0, 0, 0),
            axes.c2p(*vector),
            color=color,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.16,
        )

    @staticmethod
    def _line(direction: np.ndarray, axes: ThreeDAxes, color: str):
        point_a = axes.c2p(*(-2.6 * direction))
        point_b = axes.c2p(*(2.6 * direction))
        from manim import Line
        return Line(point_a, point_b, color=color, stroke_width=4)
