"""CP78: use pivot positions from R, but basis columns from A."""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Create,
    CurvedArrow,
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Matrix,
    MathTex,
    Polygon,
    RIGHT,
    SurroundingRectangle,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
)

from engine.pivot_columns import PivotColumns

TITLE = "Pivot Columns: A Basis from the Original Matrix"
QUESTION = "Which columns of A really form a basis for the column space?"
KEY_IDEA = "Pivot positions come from R, but the basis columns come from A."
FINAL_IDEA = "Use the original pivot columns to build a basis for col(A)."

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
A1_COLOR = "#5DADE2"
A2_COLOR = "#AF7AC5"
A3_COLOR = "#F6C85F"
PLANE_COLOR = "#55D6BE"

MATRIX = np.array([
    [1.0, 2.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 3.0, 2.0],
])


class PivotColumnsPresentation(ThreeDScene):
    """Show why basis columns come from the original matrix."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=72 * DEGREES, theta=-58 * DEGREES, zoom=0.92)

        model = PivotColumns(MATRIX)
        snapshot = model.snapshot()
        relation = model.express_nonpivot_column_in_pivot_columns()

        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-4, 4, 1),
            x_length=8.4,
            y_length=8.4,
            z_length=6.0,
        )

        title = Text(TITLE, font_size=38, color=TEXT).to_edge(UP, buff=0.26)
        matrix_a = Matrix([["1", "2", "1"], ["0", "1", "1"], ["1", "3", "2"]], h_buff=0.8)
        matrix_a.scale(0.64)
        label_a = MathTex(r"A=", font_size=34, color=TEXT)
        matrix_a_group = VGroup(label_a, matrix_a).arrange(RIGHT, buff=0.10).to_corner(LEFT + UP, buff=0.38).shift(DOWN * 0.44)

        matrix_r = Matrix([["1", "2", "1"], ["0", "1", "1"], ["0", "0", "0"]], h_buff=0.8)
        matrix_r.scale(0.64)
        label_r = MathTex(r"R=", font_size=34, color=TEXT)
        matrix_r_group = VGroup(label_r, matrix_r).arrange(RIGHT, buff=0.10).to_corner(RIGHT + UP, buff=0.38).shift(DOWN * 0.44)

        matrix_a_columns = matrix_a.get_columns()
        matrix_r_columns = matrix_r.get_columns()
        matrix_a_columns[0].set_color(A1_COLOR)
        matrix_a_columns[1].set_color(A2_COLOR)
        matrix_a_columns[2].set_color(A3_COLOR)
        matrix_r_columns[0].set_color(A1_COLOR)
        matrix_r_columns[1].set_color(A2_COLOR)
        matrix_r_columns[2].set_color(A3_COLOR)

        relation_tex = MathTex(
            rf"\mathbf a_3={relation[0]:.0f}\mathbf a_1+{relation[1]:.0f}\mathbf a_2",
            font_size=38,
            color=TEXT,
        ).to_edge(UP, buff=0.94)
        question = Text(QUESTION, font_size=27, color=TEXT).to_edge(DOWN, buff=0.46)
        pivot_caption = Text("Pivot columns in R", font_size=26, color=MUTED).to_edge(DOWN, buff=0.46)
        nonpivot_caption = Text("The third column is nonpivot, so it is redundant.", font_size=26, color=MUTED).to_edge(DOWN, buff=0.46)
        span_equality = MathTex(
            r"\operatorname{span}\{\mathbf a_1,\mathbf a_2,\mathbf a_3\}="
            r"\operatorname{span}\{\mathbf a_1,\mathbf a_2\}",
            font_size=39,
            color=TEXT,
        ).to_edge(DOWN, buff=0.46)
        basis_text = MathTex(
            r"\{\mathbf a_1,\mathbf a_2\}\text{ is a basis for }\operatorname{col}(A)",
            font_size=38,
            color=TEXT,
        ).move_to(DOWN * 2.08)
        col_space_text = MathTex(
            r"\operatorname{col}(A)=\operatorname{span}\{\mathbf a_1,\mathbf a_2\}",
            font_size=39,
            color=TEXT,
        ).next_to(basis_text, UP, buff=0.28)
        key_idea = Text(KEY_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.26)
        final_idea = Text(FINAL_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.40)

        self.add_fixed_in_frame_mobjects(title, matrix_a_group, matrix_r_group)
        self.play(FadeIn(title), FadeIn(matrix_a_group), FadeIn(matrix_r_group), FadeIn(axes))

        arrows = VGroup(
            self._arrow(MATRIX[:, 0], axes, A1_COLOR),
            self._arrow(MATRIX[:, 1], axes, A2_COLOR),
            self._arrow(MATRIX[:, 2], axes, A3_COLOR),
        )
        labels = VGroup(
            MathTex(r"\mathbf a_1", font_size=38, color=A1_COLOR).move_to(axes.c2p(*(MATRIX[:, 0] * 1.22 + np.array([0.10, 0.00, 0.05])))),
            MathTex(r"\mathbf a_2", font_size=38, color=A2_COLOR).move_to(axes.c2p(*(MATRIX[:, 1] * 1.18 + np.array([0.15, 0.00, 0.10])))),
            MathTex(r"\mathbf a_3", font_size=38, color=A3_COLOR).move_to(axes.c2p(*(MATRIX[:, 2] * 1.20 + np.array([-0.05, 0.15, 0.10])))),
        )
        for label in labels:
            label.set_stroke(color=BACKGROUND, width=8, background=True)
        self.add_fixed_orientation_mobjects(*labels)
        self.play(*(Create(arrow) for arrow in arrows), *(FadeIn(label) for label in labels), run_time=2.0)

        u = MATRIX[:, 0] / np.linalg.norm(MATRIX[:, 0])
        v = MATRIX[:, 1] - np.dot(MATRIX[:, 1], u) * u
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
        self.play(FadeIn(plane), run_time=1.7)

        self.add_fixed_in_frame_mobjects(relation_tex)
        self.play(FadeIn(relation_tex))
        self.wait(1.1)

        self.add_fixed_in_frame_mobjects(question)
        self.play(FadeIn(question))
        self.wait(1.6)
        self.play(FadeOut(question))

        a_pivot_boxes = VGroup(
            SurroundingRectangle(matrix_a_columns[0], color=A1_COLOR, buff=0.10, stroke_width=3),
            SurroundingRectangle(matrix_a_columns[1], color=A2_COLOR, buff=0.10, stroke_width=3),
        )
        r_pivot_boxes = VGroup(
            SurroundingRectangle(matrix_r_columns[0], color=A1_COLOR, buff=0.10, stroke_width=3),
            SurroundingRectangle(matrix_r_columns[1], color=A2_COLOR, buff=0.10, stroke_width=3),
        )
        nonpivot_box = SurroundingRectangle(matrix_a_columns[snapshot.nonpivot_column_indices[0]], color=A3_COLOR, buff=0.10, stroke_width=3)
        guides = VGroup(
            CurvedArrow(
                r_pivot_boxes[0].get_bottom(),
                a_pivot_boxes[0].get_bottom(),
                angle=0.7,
                color=A1_COLOR,
                stroke_width=3,
            ),
            CurvedArrow(
                r_pivot_boxes[1].get_bottom(),
                a_pivot_boxes[1].get_bottom(),
                angle=0.7,
                color=A2_COLOR,
                stroke_width=3,
            ),
        )

        self.add_fixed_in_frame_mobjects(
            a_pivot_boxes, r_pivot_boxes, nonpivot_box, guides, pivot_caption, nonpivot_caption
        )
        self.play(FadeIn(r_pivot_boxes), FadeIn(pivot_caption), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(a_pivot_boxes), Create(guides), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(pivot_caption), FadeIn(nonpivot_caption), FadeIn(nonpivot_box), run_time=0.8)
        self.play(arrows[2].animate.set_opacity(0.18), labels[2].animate.set_opacity(0.18), run_time=1.0)
        self.wait(0.4)
        self.play(FadeOut(arrows[2]), FadeOut(labels[2]), FadeOut(nonpivot_box), FadeOut(nonpivot_caption), run_time=0.9)

        self.add_fixed_in_frame_mobjects(span_equality)
        self.play(FadeOut(relation_tex), FadeIn(span_equality))
        self.wait(2.0)
        self.play(FadeOut(span_equality), FadeOut(guides), FadeOut(r_pivot_boxes), FadeOut(a_pivot_boxes))

        self.add_fixed_in_frame_mobjects(col_space_text, basis_text, key_idea)
        self.play(FadeIn(col_space_text), FadeIn(basis_text), FadeIn(key_idea))
        self.wait(2.8)
        self.play(FadeOut(col_space_text), FadeOut(basis_text), FadeOut(key_idea))

        self.play(
            FadeOut(plane), FadeOut(arrows[0]), FadeOut(arrows[1]),
            FadeOut(labels[0]), FadeOut(labels[1]), FadeOut(axes), FadeOut(matrix_a_group), FadeOut(matrix_r_group)
        )

        summary = VGroup(
            MathTex(r"\text{pivot positions come from }R", font_size=39, color=TEXT),
            MathTex(r"\text{basis columns come from }A", font_size=39, color=TEXT),
            MathTex(r"\operatorname{col}(A)=\operatorname{span}\{\mathbf a_1,\mathbf a_2\}", font_size=39, color=TEXT),
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
