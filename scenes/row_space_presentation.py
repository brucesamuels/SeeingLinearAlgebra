"""CP77: row reduction changes the rows, but not the row space."""
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
    MathTex,
    Polygon,
    RIGHT,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
)

from engine.row_space import RowSpace

TITLE = "Row Space: What Row Reduction Preserves"
QUESTION = "Do row operations change the row space?"
KEY_IDEA = "Row reduction changes the rows, but not the row space."
FINAL_IDEA = "The pivot rows of echelon form give a basis for the row space."

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
R1_COLOR = "#5DADE2"
R2_COLOR = "#AF7AC5"
R3_COLOR = "#F6C85F"
PLANE_COLOR = "#55D6BE"

MATRIX = np.array([
    [1.0, 2.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 3.0, 2.0],
])


class RowSpacePresentation(ThreeDScene):
    """Show a redundant row collapsing while the row space stays fixed."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=66 * DEGREES, theta=-48 * DEGREES, zoom=0.90)

        model = RowSpace(MATRIX)
        snapshot = model.snapshot()
        step_after_first_elimination = snapshot.steps[1]

        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-4, 4, 1),
            x_length=8.4,
            y_length=8.4,
            z_length=6.0,
        )

        title = Text(TITLE, font_size=38, color=TEXT).to_edge(UP, buff=0.30)
        matrix_tex = MathTex(
            r"A=\begin{bmatrix}1&2&1\\0&1&1\\1&3&2\end{bmatrix}",
            font_size=35,
            color=TEXT,
        ).to_corner(LEFT + UP, buff=0.44).shift(DOWN * 0.55)
        question = Text(QUESTION, font_size=27, color=TEXT).to_edge(DOWN, buff=0.44)
        op_one = MathTex(r"R_3\leftarrow R_3-R_1", font_size=38, color=TEXT).to_edge(DOWN, buff=0.44)
        op_two = MathTex(r"R_3\leftarrow R_3-R_2", font_size=38, color=TEXT).to_edge(DOWN, buff=0.44)
        echelon_tex = MathTex(
            r"R=\begin{bmatrix}1&2&1\\0&1&1\\0&0&0\end{bmatrix}",
            font_size=35,
            color=TEXT,
        ).to_corner(RIGHT + UP, buff=0.44).shift(DOWN * 0.55)
        equality = MathTex(
            r"\operatorname{row}(A)=\operatorname{row}(R)",
            font_size=40,
            color=TEXT,
        ).to_edge(DOWN, buff=0.44)
        pivot_basis = MathTex(
            r"\text{pivot rows of }R\text{ form a basis}",
            font_size=40,
            color=TEXT,
        ).move_to(DOWN * 2.15)
        dimension = MathTex(
            r"\dim(\operatorname{row}(A))=\operatorname{rank}(A)=2",
            font_size=40,
            color=TEXT,
        ).next_to(pivot_basis, UP, buff=0.26)
        key_idea = Text(KEY_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.28)
        final_idea = Text(FINAL_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.46)

        self.add_fixed_in_frame_mobjects(title, matrix_tex)
        self.play(FadeIn(title), FadeIn(matrix_tex), FadeIn(axes))

        arrows = VGroup(
            self._arrow(MATRIX[0], axes, R1_COLOR),
            self._arrow(MATRIX[1], axes, R2_COLOR),
            self._arrow(MATRIX[2], axes, R3_COLOR),
        )
        labels = VGroup(
            MathTex(r"r_1", font_size=34, color=R1_COLOR).move_to(axes.c2p(*(MATRIX[0] * 1.10))),
            MathTex(r"r_2", font_size=34, color=R2_COLOR).move_to(axes.c2p(*(MATRIX[1] * 1.16 + np.array([0.0, 0.1, 0.0])))),
            MathTex(r"r_3", font_size=34, color=R3_COLOR).move_to(axes.c2p(*(MATRIX[2] * 1.08 + np.array([0.1, 0.0, 0.1])))),
        )
        self.play(*(Create(arrow) for arrow in arrows), *(FadeIn(label) for label in labels), run_time=2.0)

        grid = np.linspace(-2.0, 2.0, 5)
        coefficients = np.array([(a, b) for a in grid for b in grid], dtype=float)
        row_space_points = model.sample_initial_row_space(coefficients)
        dots = VGroup(*(
            Dot3D(axes.c2p(*point), radius=0.032, color=PLANE_COLOR, fill_opacity=0.48)
            for point in row_space_points
        ))
        u = MATRIX[0] / np.linalg.norm(MATRIX[0])
        v = MATRIX[1] - np.dot(MATRIX[1], u) * u
        v = v / np.linalg.norm(v)
        extent = 3.2
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
            stroke_opacity=0.24,
        )
        plane.set_z_index(-1)
        self.play(FadeIn(plane), FadeIn(dots), run_time=1.7)

        self.add_fixed_in_frame_mobjects(question)
        self.play(FadeIn(question))
        self.wait(1.8)
        self.play(FadeOut(question))

        self.add_fixed_in_frame_mobjects(op_one)
        self.play(FadeIn(op_one))
        self.play(
            arrows[2].animate.put_start_and_end_on(axes.c2p(0, 0, 0), axes.c2p(*step_after_first_elimination[2])),
            labels[2].animate.move_to(axes.c2p(*(step_after_first_elimination[2] * 1.18 + np.array([0.0, 0.08, 0.0])))),
            run_time=1.4,
        )
        self.play(FadeOut(op_one))
        self.wait(0.8)

        self.add_fixed_in_frame_mobjects(op_two)
        self.play(FadeIn(op_two))
        self.play(arrows[2].animate.set_opacity(0.18), labels[2].animate.set_opacity(0.18), run_time=0.8)
        self.play(FadeOut(arrows[2]), FadeOut(labels[2]), run_time=0.9)
        self.add_fixed_in_frame_mobjects(echelon_tex)
        self.play(FadeOut(op_two), FadeIn(echelon_tex), run_time=0.8)

        self.add_fixed_in_frame_mobjects(equality)
        self.play(FadeIn(equality))
        self.wait(2.0)
        self.play(FadeOut(equality))

        self.add_fixed_in_frame_mobjects(dimension, pivot_basis, key_idea)
        self.play(FadeIn(dimension), FadeIn(pivot_basis), FadeIn(key_idea))
        self.wait(2.8)
        self.play(FadeOut(key_idea), FadeOut(pivot_basis), FadeOut(dimension))

        self.play(FadeOut(plane), FadeOut(dots), FadeOut(arrows[0]), FadeOut(arrows[1]), FadeOut(labels[0]), FadeOut(labels[1]), FadeOut(axes), FadeOut(echelon_tex), FadeOut(matrix_tex))

        summary = VGroup(
            MathTex(r"\text{same row space before and after row reduction}", font_size=39, color=TEXT),
            MathTex(r"\text{nonzero pivot rows form a basis}", font_size=39, color=TEXT),
            MathTex(r"\dim(\operatorname{row}(A))=\operatorname{rank}(A)", font_size=39, color=TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(UP * 0.18)
        self.add_fixed_in_frame_mobjects(summary, final_idea)
        self.play(FadeIn(summary), FadeIn(final_idea))
        self.wait(3.0)

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
