"""CP74: the column space of a matrix is the span of its columns."""
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
    GREEN,
    LEFT,
    MathTex,
    ORIGIN,
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

from engine.column_space import ColumnSpace

TITLE = "The Column Space of a Matrix"
KEY_IDEA = "Every output of A is a linear combination of its columns."
SUBSPACE_IDEA = "Because a column space is a span, it is automatically a subspace."

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
A1_COLOR = "#4FC3F7"
A2_COLOR = "#FFB74D"
A3_COLOR = "#C792EA"
OUTPUT_COLOR = "#81C995"
PLANE_COLOR = "#55D6BE"

MATRIX = np.array([
    [2.0, -0.5, 1.5],
    [0.5, 1.8, 2.3],
    [0.5, 0.8, 1.3],
])

COEFFICIENT_ANCHORS = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 1.0, 0.0],
    [-0.8, 1.2, 0.4],
    [1.3, -0.7, 0.8],
    [-1.1, -0.8, 1.0],
], dtype=float)


class ColumnSpacePresentation(ThreeDScene):
    """Show matrix outputs sweeping through the span of the matrix columns."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=66 * DEGREES, theta=-52 * DEGREES, zoom=0.94)

        model = ColumnSpace(MATRIX)
        columns = model.columns

        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-4, 4, 1),
            x_length=8.2,
            y_length=8.2,
            z_length=5.8,
        )

        title = Text(TITLE, font_size=38, color=TEXT).to_edge(UP, buff=0.28)
        matrix_tex = MathTex(
            r"A=\begin{bmatrix}2&-0.5&1.5\\0.5&1.8&2.3\\0.5&0.8&1.3\end{bmatrix}",
            font_size=34,
            color=WHITE,
        ).to_corner(LEFT + UP, buff=0.42).shift(DOWN * 0.58)
        columns_tex = MathTex(
            r"A=\begin{bmatrix}\vert&\vert&\vert\\"
            r"\mathbf a_1&\mathbf a_2&\mathbf a_3\\"
            r"\vert&\vert&\vert\end{bmatrix}",
            font_size=35,
            color=WHITE,
        ).to_corner(RIGHT + UP, buff=0.45).shift(DOWN * 0.62)
        self.add_fixed_in_frame_mobjects(title, matrix_tex, columns_tex)
        self.play(FadeIn(title), FadeIn(axes), FadeIn(matrix_tex), FadeIn(columns_tex))

        column_arrows = VGroup(
            self._arrow(columns[0], axes, A1_COLOR),
            self._arrow(columns[1], axes, A2_COLOR),
            self._arrow(columns[2], axes, A3_COLOR),
        )
        column_labels = VGroup(
            self._label(r"\mathbf a_1", A1_COLOR, LEFT),
            self._label(r"\mathbf a_2", A2_COLOR, ORIGIN),
            self._label(r"\mathbf a_3", A3_COLOR, RIGHT),
        )
        for label in column_labels:
            self.add_fixed_in_frame_mobjects(label)

        self.play(Create(column_arrows[0]), FadeIn(column_labels[0]))
        self.play(Create(column_arrows[1]), FadeIn(column_labels[1]))
        self.play(Create(column_arrows[2]), FadeIn(column_labels[2]))
        self.wait(1.0)

        dependence = MathTex(
            r"\mathbf a_3=\mathbf a_1+\mathbf a_2",
            font_size=38,
            color=TEXT,
        ).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(dependence)
        self.play(FadeIn(dependence))
        self.wait(1.6)
        self.play(FadeOut(dependence), FadeOut(column_labels))

        equation = MathTex(
            r"A\mathbf x=x_1\mathbf a_1+x_2\mathbf a_2+x_3\mathbf a_3",
            font_size=39,
            color=TEXT,
        ).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(equation)
        self.play(FadeIn(equation))
        self.wait(1.4)

        first_output = model.snapshot(COEFFICIENT_ANCHORS[0]).output
        output_arrow = self._arrow(first_output, axes, OUTPUT_COLOR)
        output_tip = Dot3D(axes.c2p(*first_output), radius=0.055, color=OUTPUT_COLOR)
        output_group = VGroup(output_arrow, output_tip)
        self.play(Create(output_arrow), FadeIn(output_tip))

        def coefficient_at(alpha: float) -> np.ndarray:
            scaled = alpha * (len(COEFFICIENT_ANCHORS) - 1)
            index = min(int(np.floor(scaled)), len(COEFFICIENT_ANCHORS) - 2)
            local = scaled - index
            return (1.0 - local) * COEFFICIENT_ANCHORS[index] + local * COEFFICIENT_ANCHORS[index + 1]

        def sweep_output(_mob, alpha: float) -> None:
            output = model.snapshot(coefficient_at(alpha)).output
            output_arrow.put_start_and_end_on(axes.c2p(*ORIGIN), axes.c2p(*output))
            output_tip.move_to(axes.c2p(*output))

        self.play(UpdateFromAlphaFunc(output_group, sweep_output), run_time=7.5)

        key_idea = Text(KEY_IDEA, font_size=26, color=MUTED).to_edge(DOWN, buff=0.40)
        self.add_fixed_in_frame_mobjects(key_idea)
        self.play(FadeOut(equation), FadeIn(key_idea))

        grid = np.linspace(-1.7, 1.7, 9)
        coefficient_samples = np.array([(a, b, 0.0) for a in grid for b in grid], dtype=float)
        outputs = model.sample_outputs(coefficient_samples)
        field = VGroup(*(
            Dot3D(axes.c2p(*point), radius=0.031, color=PLANE_COLOR, fill_opacity=0.50)
            for point in outputs
        ))

        u = columns[0] / np.linalg.norm(columns[0])
        v = columns[1] - np.dot(columns[1], u) * u
        v = v / np.linalg.norm(v)
        extent = 3.3
        corners = [
            -extent * u - extent * v,
            extent * u - extent * v,
            extent * u + extent * v,
            -extent * u + extent * v,
        ]
        plane = Polygon(
            *(axes.c2p(*point) for point in corners),
            color=PLANE_COLOR,
            fill_color=PLANE_COLOR,
            fill_opacity=0.12,
            stroke_opacity=0.25,
        )
        plane.set_z_index(-1)
        self.play(FadeIn(plane), FadeIn(field), run_time=2.0)
        self.wait(1.8)

        col_equation = MathTex(
            r"\operatorname{col}(A)="
            r"\operatorname{span}\{\mathbf a_1,\mathbf a_2,\mathbf a_3\}",
            font_size=40,
            color=TEXT,
        ).to_edge(DOWN, buff=0.40)
        self.add_fixed_in_frame_mobjects(col_equation)
        self.play(FadeOut(key_idea), FadeIn(col_equation))
        self.wait(2.0)

        self.play(
            FadeOut(matrix_tex), FadeOut(columns_tex), FadeOut(column_arrows),
            FadeOut(output_group), FadeOut(field), FadeOut(plane), FadeOut(axes),
            FadeOut(col_equation),
        )

        closure = VGroup(
            MathTex(r"\mathbf 0=A\mathbf 0\in\operatorname{col}(A)", font_size=39, color=GREEN),
            MathTex(r"A\mathbf x+A\mathbf y=A(\mathbf x+\mathbf y)\in\operatorname{col}(A)", font_size=39, color=GREEN),
            MathTex(r"c(A\mathbf x)=A(c\mathbf x)\in\operatorname{col}(A)", font_size=39, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(ORIGIN)
        subspace_idea = Text(SUBSPACE_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(closure, subspace_idea)
        self.play(FadeIn(closure), FadeIn(subspace_idea))
        self.wait(3.2)

    @staticmethod
    def _arrow(vector: np.ndarray, axes: ThreeDAxes, color: str) -> Arrow:
        return Arrow(
            axes.c2p(*ORIGIN),
            axes.c2p(*vector),
            color=color,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.16,
        )

    def _label(self, tex: str, color: str, horizontal) -> MathTex:
        label = MathTex(tex, font_size=34, color=color).to_edge(UP, buff=0.42)
        if np.array_equal(horizontal, LEFT):
            label.to_corner(LEFT + UP, buff=0.42).shift(DOWN * 1.65)
        elif np.array_equal(horizontal, RIGHT):
            label.to_corner(RIGHT + UP, buff=0.42).shift(DOWN * 1.65)
        else:
            label.shift(DOWN * 1.25)
        return label
