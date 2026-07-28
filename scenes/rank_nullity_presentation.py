"""CP79.3: text-led synthesis of dependence, pivots, rank, and nullity."""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Create,
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    Matrix,
    MathTex,
    ORIGIN,
    Polygon,
    RIGHT,
    SurroundingRectangle,
    Text,
    ThreeDAxes,
    ThreeDScene,
    Transform,
    UP,
    VGroup,
)

TITLE = "Rank and Nullity: What the Matrix Keeps and Loses"
BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
V1_COLOR = "#5DADE2"
V2_COLOR = "#AF7AC5"
V3_COLOR = "#F6C85F"
PLANE_COLOR = "#55D6BE"
ZERO_COLOR = "#F28B82"

V1 = np.array([2.0, 0.2, 0.4])
V2 = np.array([-0.4, 1.7, 0.9])
V3_INDEPENDENT = np.array([0.4, -0.2, 2.1])
V3_DEPENDENT = V1 + V2


class RankNullityPresentation(ThreeDScene):
    """Use slow text and brief visual callbacks to synthesize rank-nullity."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=69 * DEGREES, theta=-52 * DEGREES, zoom=0.94)

        title = Text(TITLE, font_size=38, color=TEXT).to_edge(UP, buff=0.28)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title))

        opening = Text(
            "When one vector is a linear combination of the others,\n"
            "it adds no new direction to the space.\n\n"
            "The collection may contain more vectors,\n"
            "but its dimension does not increase.",
            font_size=34,
            color=TEXT,
            line_spacing=1.15,
        ).move_to(DOWN * 2.7)
        self.add_fixed_in_frame_mobjects(opening)
        self.play(FadeIn(opening), opening.animate.shift(UP * 2.7), run_time=7.0)
        self.wait(1.2)
        self.play(FadeOut(opening))

        axes = ThreeDAxes(
            x_range=(-4, 4, 1),
            y_range=(-4, 4, 1),
            z_range=(-4, 4, 1),
            x_length=7.6,
            y_length=7.6,
            z_length=5.8,
        )
        self.play(FadeIn(axes))

        v1_arrow = self._arrow(V1, axes, V1_COLOR)
        v2_arrow = self._arrow(V2, axes, V2_COLOR)
        v3_arrow = self._arrow(V3_INDEPENDENT, axes, V3_COLOR)
        v3_target = self._arrow(V3_DEPENDENT, axes, V3_COLOR)

        labels = VGroup(
            MathTex(r"\mathbf v_1", font_size=36, color=V1_COLOR).move_to(axes.c2p(*(1.20 * V1 + np.array([0.18, -0.08, 0.06])))),
            MathTex(r"\mathbf v_2", font_size=36, color=V2_COLOR).move_to(axes.c2p(*(1.20 * V2 + np.array([0.18, -0.08, 0.08])))),
            MathTex(r"\mathbf v_3", font_size=36, color=V3_COLOR).move_to(axes.c2p(*(1.12 * V3_INDEPENDENT + np.array([0.12, -0.08, 0.10])))),
        )
        for label in labels:
            label.set_stroke(color=BACKGROUND, width=8, background=True)
        self.add_fixed_orientation_mobjects(labels[0], labels[1])

        u = V1 / np.linalg.norm(V1)
        v = V2 - np.dot(V2, u) * u
        v = v / np.linalg.norm(v)
        extent = 3.0
        plane = Polygon(
            *(axes.c2p(*point) for point in [
                -extent * u - extent * v,
                extent * u - extent * v,
                extent * u + extent * v,
                -extent * u + extent * v,
            ]),
            color=PLANE_COLOR,
            fill_color=PLANE_COLOR,
            fill_opacity=0.12,
            stroke_opacity=0.24,
        )
        plane.set_z_index(-1)

        self.play(Create(v1_arrow), Create(v2_arrow), FadeIn(labels[0]), FadeIn(labels[1]), run_time=1.8)
        self.play(FadeIn(plane), run_time=1.2)
        self.add_fixed_orientation_mobjects(labels[2])
        self.play(Create(v3_arrow), FadeIn(labels[2]), run_time=1.2)

        collapse_caption = Text(
            "Now make the third vector dependent.",
            font_size=28,
            color=MUTED,
        ).to_edge(DOWN, buff=0.42)
        relation = MathTex(
            r"\mathbf v_3=\mathbf v_1+\mathbf v_2",
            font_size=40,
            color=TEXT,
        ).next_to(collapse_caption, UP, buff=0.25)
        no_volume = MathTex(
            r"\text{new volume}=0",
            font_size=38,
            color=ZERO_COLOR,
        ).next_to(relation, UP, buff=0.25)
        self.add_fixed_in_frame_mobjects(collapse_caption, relation, no_volume)
        self.play(FadeIn(collapse_caption))
        self.play(
            Transform(v3_arrow, v3_target),
            labels[2].animate.move_to(axes.c2p(*(1.14 * V3_DEPENDENT + np.array([0.14, -0.06, 0.08])))),
            run_time=3.2,
        )
        self.play(FadeIn(relation), FadeIn(no_volume))
        self.wait(1.8)
        self.play(FadeOut(collapse_caption), FadeOut(relation), FadeOut(no_volume))
        self.play(FadeOut(axes), FadeOut(v1_arrow), FadeOut(v2_arrow), FadeOut(v3_arrow), FadeOut(labels), FadeOut(plane))

        bridge = Text(
            "Row reduction tells us\n"
            "which columns introduce\n"
            "genuinely new directions.\n\n"
            "Those locations are\n"
            "the pivot positions.",
            font_size=33,
            color=TEXT,
            line_spacing=1.15,
        ).move_to(DOWN * 2.7)
        self.add_fixed_in_frame_mobjects(bridge)
        self.play(FadeIn(bridge), bridge.animate.shift(UP * 2.7), run_time=6.0)
        self.wait(1.0)
        self.play(FadeOut(bridge))

        matrix_a = Matrix([["1", "2", "1"], ["0", "1", "1"], ["1", "3", "2"]], h_buff=0.9).scale(0.85)
        matrix_r = Matrix([["1", "2", "1"], ["0", "1", "1"], ["0", "0", "0"]], h_buff=0.9).scale(0.85)
        label_a = MathTex(r"A=", font_size=38, color=TEXT)
        label_r = MathTex(r"R=", font_size=38, color=TEXT)
        a_group = VGroup(label_a, matrix_a).arrange(RIGHT, buff=0.12).shift(LEFT * 3.0)
        r_group = VGroup(label_r, matrix_r).arrange(RIGHT, buff=0.12).shift(RIGHT * 3.0)

        a_columns = matrix_a.get_columns()
        r_columns = matrix_r.get_columns()
        for columns in (a_columns, r_columns):
            columns[0].set_color(V1_COLOR)
            columns[1].set_color(V2_COLOR)
            columns[2].set_color(V3_COLOR)

        pivot_boxes_r = VGroup(
            SurroundingRectangle(r_columns[0], color=V1_COLOR, buff=0.10, stroke_width=3),
            SurroundingRectangle(r_columns[1], color=V2_COLOR, buff=0.10, stroke_width=3),
        )
        pivot_boxes_a = VGroup(
            SurroundingRectangle(a_columns[0], color=V1_COLOR, buff=0.10, stroke_width=3),
            SurroundingRectangle(a_columns[1], color=V2_COLOR, buff=0.10, stroke_width=3),
        )
        pivot_text = Text(
            "Pivot positions are found in R.\n"
            "The corresponding original columns of A form a basis for col(A).",
            font_size=30,
            color=TEXT,
            line_spacing=1.15,
        ).to_edge(DOWN, buff=0.45)
        self.add_fixed_in_frame_mobjects(a_group, r_group, pivot_boxes_r, pivot_boxes_a, pivot_text)
        self.play(FadeIn(a_group), FadeIn(r_group))
        self.play(FadeIn(pivot_boxes_r), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(pivot_boxes_a), FadeIn(pivot_text), run_time=1.2)
        self.wait(2.4)
        self.play(FadeOut(a_group), FadeOut(r_group), FadeOut(pivot_boxes_r), FadeOut(pivot_boxes_a), FadeOut(pivot_text))

        nullity_text = Text(
            "The remaining input directions do not add new dimension.\n\n"
            "Instead, they appear as directions in the null space —\n"
            "directions that collapse to the zero vector.",
            font_size=33,
            color=TEXT,
            line_spacing=1.15,
        ).move_to(DOWN * 2.8)
        self.add_fixed_in_frame_mobjects(nullity_text)
        self.play(FadeIn(nullity_text), nullity_text.animate.shift(UP * 2.8), run_time=7.0)
        self.wait(1.1)
        self.play(FadeOut(nullity_text))

        theorem_intro = Text(
            "So the input dimensions split in two ways:",
            font_size=34,
            color=TEXT,
        ).shift(UP * 2.0)
        theorem = MathTex(
            r"\operatorname{rank}(A)+\operatorname{nullity}(A)=n",
            font_size=48,
            color=TEXT,
        ).shift(UP * 0.85)
        interpretation = VGroup(
            Text("Rank counts the independent directions that survive.", font_size=30, color=V1_COLOR),
            Text("Nullity counts the directions that collapse to zero.", font_size=30, color=V3_COLOR),
            Text("Together, they account for the entire input space.", font_size=30, color=TEXT),
        ).arrange(DOWN, buff=0.30).shift(DOWN * 1.60)
        example = MathTex(r"2+1=3", font_size=46, color=TEXT).next_to(theorem, DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(theorem_intro, theorem, example)
        self.play(FadeIn(theorem_intro), FadeIn(theorem), FadeIn(example), run_time=1.4)
        self.wait(0.8)
        self.add_fixed_in_frame_mobjects(interpretation)
        self.play(FadeIn(interpretation), run_time=1.4)
        self.wait(4.0)

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
