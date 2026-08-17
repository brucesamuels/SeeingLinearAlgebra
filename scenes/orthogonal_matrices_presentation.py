"""CP162: Orthogonal matrices preserve geometry."""

from __future__ import annotations

import numpy as np
from manim import (
    Angle,
    Arrow,
    Circle,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    GREY_B,
    GREY_D,
    LEFT,
    Line,
    MathTex,
    NumberPlane,
    ORANGE,
    PI,
    Polygon,
    PURPLE,
    Rectangle,
    RIGHT,
    Scene,
    SurroundingRectangle,
    TEAL,
    Text,
    TransformFromCopy,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    BLUE,
)

from engine.orthogonal_matrices import OrthogonalMatricesLesson


class OrthogonalMatricesPresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Orthogonal Matrices Preserve Geometry"
    SCENE_REVISION = "cp162_r4_balanced_equation_columns"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.05
    HOLD_TIME = 2.25

    def construct(self) -> None:
        self.lesson = OrthogonalMatricesLesson()
        self.snapshot = self.lesson.snapshot()
        self.banner, self.lesson_title_mobject = self._header()
        self.add(self.banner, self.lesson_title_mobject)

        self._orthonormal_columns_card()
        self._length_preservation_card()
        self._angle_preservation_card()
        self._rigid_motion_card()
        self._determinant_card()
        self._closing_card()

    def _header(self) -> tuple[VGroup, Text]:
        banner_box = Rectangle(
            width=13.5,
            height=0.58,
            stroke_width=0,
            fill_color=GREY_D,
            fill_opacity=0.96,
        ).to_edge(UP, buff=0.08)
        banner_text = Text(self.CHAPTER_BANNER, font_size=28, color=WHITE).move_to(banner_box)
        lesson_title = Text(self.LESSON_TITLE, font_size=30, color=YELLOW).next_to(
            banner_box, DOWN, buff=0.18
        )
        if lesson_title.width > 11.8:
            lesson_title.scale_to_fit_width(11.8)
        return VGroup(banner_box, banner_text), lesson_title

    @staticmethod
    def _plane(center, *, x_range=(-2, 3, 1), y_range=(-2, 3, 1), width=4.9, height=4.9) -> NumberPlane:
        return NumberPlane(
            x_range=x_range,
            y_range=y_range,
            x_length=width,
            y_length=height,
            background_line_style={"stroke_opacity": 0.34, "stroke_width": 1.6},
            axis_config={"stroke_opacity": 0.72, "stroke_width": 2.2},
        ).move_to(center)

    @staticmethod
    def _arrow(plane: NumberPlane, vector: np.ndarray, color, *, width: float = 6) -> Arrow:
        return Arrow(
            plane.c2p(0, 0),
            plane.c2p(*vector),
            buff=0,
            color=color,
            stroke_width=width,
        )

    @staticmethod
    def _label(text: str, plane: NumberPlane, point: np.ndarray, color, offset) -> MathTex:
        return MathTex(text, font_size=30, color=color).move_to(plane.c2p(*point) + offset)

    @staticmethod
    def _circle_for_radius(plane: NumberPlane, radius: float, color) -> Circle:
        screen_radius = np.linalg.norm(plane.c2p(radius, 0) - plane.c2p(0, 0))
        return Circle(radius=screen_radius, color=color, stroke_width=3, stroke_opacity=0.8).move_to(
            plane.c2p(0, 0)
        )

    @staticmethod
    def _polygon(plane: NumberPlane, vertices: np.ndarray, color, *, fill_opacity: float = 0.18) -> Polygon:
        return Polygon(
            *(plane.c2p(*vertex) for vertex in vertices),
            color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=fill_opacity,
        )

    def _orthonormal_columns_card(self) -> None:
        heading = Text("Orthonormal columns give an orthogonal matrix", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane(LEFT * 3.15 + DOWN * 0.58, x_range=(-1.4, 1.6, 0.5), y_range=(-1.4, 1.6, 0.5), width=4.9, height=4.9)
        unit_circle = self._circle_for_radius(plane, 1.0, GREEN)
        q1_arrow = self._arrow(plane, self.snapshot.q1, ORANGE)
        q2_arrow = self._arrow(plane, self.snapshot.q2, PURPLE)
        q1_label = self._label(r"\mathbf q_1", plane, self.snapshot.q1, ORANGE, LEFT * 0.38 + UP * 0.22)
        q2_label = self._label(r"\mathbf q_2", plane, self.snapshot.q2, PURPLE, RIGHT * 0.36 + UP * 0.22)
        right_angle = Angle(
            Line(plane.c2p(0, 0), plane.c2p(*self.snapshot.q1)),
            Line(plane.c2p(0, 0), plane.c2p(*self.snapshot.q2)),
            radius=0.36,
            color=WHITE,
        )
        equations = VGroup(
            MathTex(r"Q=\begin{bmatrix}\frac{1}{\sqrt2}&-\frac{1}{\sqrt2}\\[4pt]\frac{1}{\sqrt2}&\frac{1}{\sqrt2}\end{bmatrix}", font_size=38),
            MathTex(self.lesson.ORTHOGONAL_TEST, font_size=40, color=GREEN),
            MathTex(self.lesson.INVERSE_RULE, font_size=40, color=YELLOW),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.05 + UP * 0.08)
        caption = Text(
            "Orthogonal means the columns are orthonormal, so transpose and inverse agree.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), Create(unit_circle), run_time=self.TRANSITION_TIME)
        self.play(Create(q1_arrow), FadeIn(q1_label), Create(q2_arrow), FadeIn(q2_label), Create(right_angle), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, unit_circle, q1_arrow, q2_arrow, q1_label, q2_label, right_angle, equations, caption)), run_time=self.TRANSITION_TIME)

    def _length_preservation_card(self) -> None:
        heading = Text("Lengths are preserved", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left_plane = self._plane(LEFT * 4.05 + DOWN * 0.70, width=3.55, height=3.55)
        right_plane = self._plane(LEFT * 0.55 + DOWN * 0.70, width=3.55, height=3.55)
        left_title = Text("before", font_size=23, color=GREY_B).next_to(left_plane, UP, buff=0.16)
        right_title = Text("after applying Q", font_size=23, color=GREY_B).next_to(right_plane, UP, buff=0.16)
        v_arrow = self._arrow(left_plane, self.snapshot.v, BLUE)
        qv_arrow = self._arrow(right_plane, self.snapshot.Qv, BLUE)
        v_label = self._label(r"\mathbf v", left_plane, self.snapshot.v, BLUE, RIGHT * 0.32 + DOWN * 0.04)
        qv_label = self._label(r"Q\mathbf v", right_plane, self.snapshot.Qv, BLUE, RIGHT * 0.40 + DOWN * 0.02)
        norm_radius = np.linalg.norm(self.snapshot.v)
        left_circle = self._circle_for_radius(left_plane, norm_radius, TEAL)
        right_circle = self._circle_for_radius(right_plane, norm_radius, TEAL)
        equations = VGroup(
            MathTex(r"\|\mathbf v\|=\sqrt5", font_size=37, color=BLUE),
            MathTex(r"\|Q\mathbf v\|=\sqrt5", font_size=37, color=BLUE),
            MathTex(self.lesson.LENGTH_RULE, font_size=40, color=YELLOW),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 4.55 + DOWN * 0.82)
        caption = Text(
            "The image lands on a circle of the same radius — no stretching.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_plane), Create(right_plane), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(Create(v_arrow), FadeIn(v_label), Create(left_circle), run_time=self.EMPHASIS_TIME)
        self.play(TransformFromCopy(v_arrow, qv_arrow), TransformFromCopy(left_circle, right_circle), FadeIn(qv_label), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, left_plane, right_plane, left_title, right_title, v_arrow, qv_arrow, v_label, qv_label, left_circle, right_circle, equations, caption)), run_time=self.TRANSITION_TIME)

    def _angle_preservation_card(self) -> None:
        heading = Text("Dot products and angles are preserved", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left_plane = self._plane(LEFT * 3.35 + DOWN * 0.74)
        right_plane = self._plane(RIGHT * 2.05 + DOWN * 0.74)
        left_title = Text("u and v", font_size=23, color=GREY_B).next_to(left_plane, UP, buff=0.16)
        right_title = Text("Qu and Qv", font_size=23, color=GREY_B).next_to(right_plane, UP, buff=0.16)
        u_arrow = self._arrow(left_plane, self.snapshot.u, ORANGE)
        v_arrow = self._arrow(left_plane, self.snapshot.v, BLUE)
        qu_arrow = self._arrow(right_plane, self.snapshot.Qu, ORANGE)
        qv_arrow = self._arrow(right_plane, self.snapshot.Qv, BLUE)
        u_label = self._label(r"\mathbf u", left_plane, self.snapshot.u, ORANGE, LEFT * 0.42 + DOWN * 0.02)
        v_label = self._label(r"\mathbf v", left_plane, self.snapshot.v, BLUE, RIGHT * 0.42 + DOWN * 0.00)
        qu_label = self._label(r"Q\mathbf u", right_plane, self.snapshot.Qu, ORANGE, RIGHT * 0.60 + DOWN * 0.02)
        qv_label = self._label(r"Q\mathbf v", right_plane, self.snapshot.Qv, BLUE, LEFT * 0.62 + DOWN * 0.02)
        left_angle = Angle(
            Line(left_plane.c2p(0, 0), left_plane.c2p(*self.snapshot.u)),
            Line(left_plane.c2p(0, 0), left_plane.c2p(*self.snapshot.v)),
            radius=0.42,
            color=YELLOW,
        )
        right_angle = Angle(
            Line(right_plane.c2p(0, 0), right_plane.c2p(*self.snapshot.Qu)),
            Line(right_plane.c2p(0, 0), right_plane.c2p(*self.snapshot.Qv)),
            radius=0.42,
            color=YELLOW,
        )
        equations = VGroup(
            MathTex(r"\mathbf u^T\mathbf v=4", font_size=37),
            MathTex(r"(Q\mathbf u)^T(Q\mathbf v)=4", font_size=37),
            MathTex(self.lesson.DOT_RULE, font_size=39, color=GREEN),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 0.10 + DOWN * 2.22)
        caption = Text(
            "Preserving the dot product means preserving the angle between vectors.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_plane), Create(right_plane), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(Create(u_arrow), FadeIn(u_label), Create(v_arrow), FadeIn(v_label), Create(left_angle), run_time=self.EMPHASIS_TIME)
        self.play(TransformFromCopy(u_arrow, qu_arrow), TransformFromCopy(v_arrow, qv_arrow), FadeIn(qu_label), FadeIn(qv_label), Create(right_angle), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, left_plane, right_plane, left_title, right_title, u_arrow, v_arrow, qu_arrow, qv_arrow, u_label, v_label, qu_label, qv_label, left_angle, right_angle, equations, caption)), run_time=self.TRANSITION_TIME)

    def _rigid_motion_card(self) -> None:
        heading = Text("An orthogonal matrix rotates or reflects without shearing", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left_plane = self._plane(LEFT * 3.35 + DOWN * 0.74)
        right_plane = self._plane(RIGHT * 2.05 + DOWN * 0.74)
        left_title = Text("unit square", font_size=23, color=GREY_B).next_to(left_plane, UP, buff=0.16)
        right_title = Text("image under Q", font_size=23, color=GREY_B).next_to(right_plane, UP, buff=0.16)
        square_left = self._polygon(left_plane, self.snapshot.unit_square, TEAL)
        square_right = self._polygon(right_plane, self.snapshot.rotated_square, TEAL)
        e1_left = self._arrow(left_plane, np.array([1.0, 0.0]), ORANGE, width=5)
        e2_left = self._arrow(left_plane, np.array([0.0, 1.0]), PURPLE, width=5)
        q1_right = self._arrow(right_plane, self.snapshot.q1, ORANGE, width=5)
        q2_right = self._arrow(right_plane, self.snapshot.q2, PURPLE, width=5)
        e1_label = self._label(r"\mathbf e_1", left_plane, np.array([1.0, 0.0]), ORANGE, RIGHT * 0.30 + DOWN * 0.24)
        e2_label = self._label(r"\mathbf e_2", left_plane, np.array([0.0, 1.0]), PURPLE, LEFT * 0.26 + DOWN * 0.04)
        q1_label = self._label(r"Q\mathbf e_1", right_plane, self.snapshot.q1, ORANGE, RIGHT * 0.50 + DOWN * 0.16)
        q2_label = self._label(r"Q\mathbf e_2", right_plane, self.snapshot.q2, PURPLE, LEFT * 0.60 + DOWN * 0.00)
        equations = VGroup(
            MathTex(r"Q\text{ sends an orthonormal basis to another orthonormal basis}", font_size=34, color=YELLOW),
            MathTex(r"\text{No stretching, no shearing — only rigid motion.}", font_size=32, color=GREEN),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 0.12 + DOWN * 2.00)
        caption = Text(
            "The square keeps side lengths and right angles, but its orientation changes.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_plane), Create(right_plane), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(square_left), Create(e1_left), Create(e2_left), FadeIn(e1_label), FadeIn(e2_label), run_time=self.EMPHASIS_TIME)
        self.play(TransformFromCopy(square_left, square_right), TransformFromCopy(e1_left, q1_right), TransformFromCopy(e2_left, q2_right), FadeIn(q1_label), FadeIn(q2_label), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, left_plane, right_plane, left_title, right_title, square_left, square_right, e1_left, e2_left, q1_right, q2_right, e1_label, e2_label, q1_label, q2_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _determinant_card(self) -> None:
        heading = Text("The determinant tells rotation from reflection", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left_plane = self._plane(LEFT * 3.65 + DOWN * 0.62, x_range=(-1, 2, 1), y_range=(-1, 2, 1), width=3.75, height=3.75)
        right_plane = self._plane(RIGHT * 0.90 + DOWN * 0.62, x_range=(-1, 2, 1), y_range=(-1, 2, 1), width=3.75, height=3.75)
        rot_square = self._polygon(left_plane, self.snapshot.rotated_square, TEAL)
        ref_square = self._polygon(right_plane, self.snapshot.reflected_square, TEAL)
        rot_label = Text("rotation", font_size=24, color=GREEN).next_to(left_plane, UP, buff=0.16)
        ref_label = Text("reflection", font_size=24, color=YELLOW).next_to(right_plane, UP, buff=0.16)
        left_eqs = VGroup(
            MathTex(r"R=\begin{bmatrix}\frac{1}{\sqrt2}&-\frac{1}{\sqrt2}\\[4pt]\frac{1}{\sqrt2}&\frac{1}{\sqrt2}\end{bmatrix}", font_size=32),
            MathTex(r"\det R=1", font_size=36, color=GREEN),
        ).arrange(DOWN, buff=0.22).move_to(LEFT * 3.65 + DOWN * 2.38)
        right_eqs = VGroup(
            MathTex(r"H=\begin{bmatrix}1&0\\0&-1\end{bmatrix}", font_size=32),
            MathTex(r"\det H=-1", font_size=36, color=YELLOW),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 4.72 + DOWN * 0.78)
        summary = Text(
            "Both are orthogonal.  Determinant +1 keeps orientation; determinant -1 reverses it.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_plane), Create(right_plane), FadeIn(rot_label), FadeIn(ref_label), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(rot_square), FadeIn(ref_square), FadeIn(left_eqs), FadeIn(right_eqs), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(summary), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, left_plane, right_plane, rot_square, ref_square, rot_label, ref_label, left_eqs, right_eqs, summary)), run_time=self.TRANSITION_TIME)

    def _closing_card(self) -> None:
        statement = MathTex(
            r"\boxed{\text{Orthogonal matrices preserve lengths and angles.}}",
            font_size=44,
            color=YELLOW,
        ).move_to(UP * 0.30)
        support = VGroup(
            MathTex(self.lesson.ORTHOGONAL_TEST, font_size=40, color=GREEN),
            MathTex(self.lesson.INVERSE_RULE, font_size=40, color=WHITE),
            MathTex(r"\det Q=\pm 1", font_size=40, color=TEAL),
        ).arrange(DOWN, buff=0.30).next_to(statement, DOWN, buff=0.72)
        frame = SurroundingRectangle(statement, color=GREY_B, buff=0.24)
        caption = Text(
            self.lesson.CLOSING_IDEA,
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.40)

        self.play(FadeIn(statement), Create(frame), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(support), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(statement, frame, support, caption)), run_time=self.TRANSITION_TIME)
