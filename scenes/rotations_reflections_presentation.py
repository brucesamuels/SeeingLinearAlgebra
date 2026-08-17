"""CP163: rotations and reflections as orthogonal transformations."""

from __future__ import annotations

import numpy as np
from manim import (
    Angle,
    Arrow,
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
    Rotate,
    Scene,
    TEAL,
    Text,
    Transform,
    TransformFromCopy,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    BLUE,
)

from engine.rotations_reflections import RotationsReflectionsLesson


class RotationsReflectionsPresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Rotations and Reflections: Orthogonal Transformations"
    SCENE_REVISION = "cp163_r6_final_spacing_cleanup"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.10
    HOLD_TIME = 2.30

    def construct(self) -> None:
        self.lesson = RotationsReflectionsLesson()
        self.snapshot = self.lesson.snapshot()
        self.banner, self.lesson_title_mobject = self._header()
        self.add(self.banner, self.lesson_title_mobject)

        self._rotation_from_basis_card()
        self._rotation_in_motion_card()
        self._inverse_rotation_card()
        self._reflection_geometry_card()
        self._reflection_inverse_card()
        self._why_orthogonal_card()
        self._specific_examples_orthogonal_card()
        self._compare_orientation_card()

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
    def _plane(center=LEFT * 2.95 + DOWN * 0.52, *, width: float = 5.55, height: float = 5.55) -> NumberPlane:
        return NumberPlane(
            x_range=(-3.0, 3.0, 1.0),
            y_range=(-3.0, 3.0, 1.0),
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
    def _triangle(plane: NumberPlane, vertices: np.ndarray, color=TEAL, *, opacity: float = 0.22) -> Polygon:
        return Polygon(
            *(plane.c2p(*vertex) for vertex in vertices),
            stroke_color=color,
            stroke_width=3.2,
            fill_color=color,
            fill_opacity=opacity,
        )

    @staticmethod
    def _right_math(*mobjects) -> VGroup:
        return VGroup(*mobjects).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.25 + DOWN * 0.20)

    def _rotation_from_basis_card(self) -> None:
        heading = Text("A rotation matrix is determined by where it sends the basis", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        e1 = self._arrow(plane, self.snapshot.e1, GREY_B, width=4)
        e2 = self._arrow(plane, self.snapshot.e2, GREY_B, width=4)
        re1 = self._arrow(plane, self.snapshot.Re1, ORANGE)
        re2 = self._arrow(plane, self.snapshot.Re2, PURPLE)
        e1_label = self._label(r"\mathbf e_1", plane, self.snapshot.e1, GREY_B, RIGHT * 0.30 + DOWN * 0.18)
        e2_label = self._label(r"\mathbf e_2", plane, self.snapshot.e2, GREY_B, LEFT * 0.26 + UP * 0.22)
        re1_label = self._label(r"R_\theta\mathbf e_1", plane, self.snapshot.Re1, ORANGE, RIGHT * 0.48 + UP * 0.10)
        re2_label = self._label(r"R_\theta\mathbf e_2", plane, self.snapshot.Re2, PURPLE, LEFT * 0.58 + UP * 0.06)
        theta_arc = Angle(
            Line(plane.c2p(0, 0), plane.c2p(*self.snapshot.e1)),
            Line(plane.c2p(0, 0), plane.c2p(*self.snapshot.Re1)),
            radius=0.55,
            color=YELLOW,
        )
        theta_label = MathTex(r"\theta", font_size=30, color=YELLOW).move_to(plane.c2p(0.72, 0.38))
        equations = self._right_math(
            MathTex(r"R_\theta\mathbf e_1=(\cos\theta,\sin\theta)", font_size=36, color=ORANGE),
            MathTex(r"R_\theta\mathbf e_2=(-\sin\theta,\cos\theta)", font_size=36, color=PURPLE),
            MathTex(self.lesson.ROTATION_MATRIX, font_size=39, color=YELLOW),
        )
        caption = Text(
            "The columns of a transformation matrix are the images of the basis vectors.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(e1), Create(e2), FadeIn(e1_label), FadeIn(e2_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(re1), Create(re2), FadeIn(re1_label), FadeIn(re2_label), Create(theta_arc), FadeIn(theta_label), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, e1, e2, re1, re2, e1_label, e2_label, re1_label, re2_label, theta_arc, theta_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _rotation_in_motion_card(self) -> None:
        heading = Text("The whole figure rotates rigidly through the same angle", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        original = self._triangle(plane, self.snapshot.triangle, GREY_B, opacity=0.10)
        moving = self._triangle(plane, self.snapshot.triangle, TEAL, opacity=0.26)
        v_arrow = self._arrow(plane, self.snapshot.v, BLUE)
        moving_v = v_arrow.copy()
        v_label = self._label(r"\mathbf v", plane, self.snapshot.v, BLUE, RIGHT * 0.34 + UP * 0.16)
        target_label = self._label(r"R_{60^\circ}\mathbf v", plane, self.snapshot.Rv, BLUE, LEFT * 0.55 + UP * 0.16)
        equations = self._right_math(
            MathTex(r"\theta=60^\circ", font_size=38, color=YELLOW),
            MathTex(r"R_{60^\circ}=\begin{bmatrix}\frac12&-\frac{\sqrt3}{2}\\[4pt]\frac{\sqrt3}{2}&\frac12\end{bmatrix}", font_size=37),
            MathTex(r"R_{60^\circ}\begin{bmatrix}2\\1\end{bmatrix}=\begin{bmatrix}1-\frac{\sqrt3}{2}\\[2pt]\sqrt3+\frac12\end{bmatrix}", font_size=34, color=BLUE),
        )
        caption = Text(
            "Every point turns by the same angle about the origin; distances within the figure stay fixed.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), FadeIn(original), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(moving), Create(v_arrow), FadeIn(v_label), run_time=self.EMPHASIS_TIME)
        self.play(
            Rotate(moving, angle=self.snapshot.theta, about_point=plane.c2p(0, 0)),
            Rotate(moving_v, angle=self.snapshot.theta, about_point=plane.c2p(0, 0)),
            FadeOut(v_label),
            run_time=1.8,
        )
        self.add(moving_v)
        self.play(FadeIn(target_label), FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, original, moving, v_arrow, moving_v, target_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _inverse_rotation_card(self) -> None:
        heading = Text("Undoing a rotation means rotating by the opposite angle", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        rv_arrow = self._arrow(plane, self.snapshot.Rv, BLUE)
        restored = rv_arrow.copy()
        rv_label = self._label(r"R_\theta\mathbf v", plane, self.snapshot.Rv, BLUE, LEFT * 0.54 + UP * 0.16)
        v_label = self._label(r"\mathbf v", plane, self.snapshot.v, GREEN, RIGHT * 0.34 + UP * 0.16)
        equations = self._right_math(
            MathTex(r"R_{-\theta}R_\theta=I", font_size=41, color=GREEN),
            MathTex(self.lesson.ROTATION_INVERSE, font_size=40, color=YELLOW),
            MathTex(r"R_\theta^TR_\theta=I", font_size=40),
        )
        caption = Text(
            "For rotations, transpose means reverse the direction of the turn.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), Create(rv_arrow), FadeIn(rv_label), run_time=self.TRANSITION_TIME)
        self.play(
            Rotate(restored, angle=-self.snapshot.theta, about_point=plane.c2p(0, 0)),
            FadeOut(rv_label),
            run_time=1.8,
        )
        self.add(restored)
        restored.set_color(GREEN)
        self.play(FadeIn(v_label), FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, rv_arrow, restored, v_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _reflection_geometry_card(self) -> None:
        heading = Text("A reflection fixes one direction and reverses the perpendicular one", font_size=26, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        mirror = Line(plane.c2p(-2.8, 0), plane.c2p(2.8, 0), color=YELLOW, stroke_width=4)
        mirror_label = Text("mirror line", font_size=22, color=YELLOW).next_to(mirror, DOWN, buff=0.12).shift(LEFT * 1.35)
        v_arrow = self._arrow(plane, self.snapshot.v, BLUE)
        hv_arrow = self._arrow(plane, self.snapshot.reflected_v, PURPLE)
        v_label = self._label(r"\mathbf v", plane, self.snapshot.v, BLUE, RIGHT * 0.34 + UP * 0.16)
        hv_label = self._label(r"H\mathbf v", plane, self.snapshot.reflected_v, PURPLE, RIGHT * 0.48 + DOWN * 0.16)
        dashed = Line(plane.c2p(*self.snapshot.v), plane.c2p(*self.snapshot.reflected_v), color=GREY_B, stroke_width=2.2)
        equations = self._right_math(
            MathTex(r"H\mathbf e_1=\mathbf e_1", font_size=39, color=ORANGE),
            MathTex(r"H\mathbf e_2=-\mathbf e_2", font_size=39, color=PURPLE),
            MathTex(self.lesson.REFLECTION_MATRIX, font_size=40, color=YELLOW),
        )
        caption = Text(
            "The x-axis stays fixed while the perpendicular direction changes sign.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), Create(mirror), FadeIn(mirror_label), run_time=self.TRANSITION_TIME)
        self.play(Create(v_arrow), FadeIn(v_label), run_time=self.EMPHASIS_TIME)
        self.play(TransformFromCopy(v_arrow, hv_arrow), FadeIn(hv_label), Create(dashed), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, mirror, mirror_label, v_arrow, hv_arrow, v_label, hv_label, dashed, equations, caption)), run_time=self.TRANSITION_TIME)

    def _reflection_inverse_card(self) -> None:
        heading = Text("A reflection is its own inverse", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        mirror = Line(plane.c2p(-2.8, 0), plane.c2p(2.8, 0), color=YELLOW, stroke_width=4)
        original = self._triangle(plane, self.snapshot.triangle, GREY_B, opacity=0.10)
        reflected = self._triangle(plane, self.snapshot.reflected_triangle, TEAL, opacity=0.28)
        restored = reflected.copy()
        equations = self._right_math(
            MathTex(r"H(H\mathbf v)=\mathbf v", font_size=41, color=GREEN),
            MathTex(r"H^2=I", font_size=43, color=GREEN),
            MathTex(self.lesson.REFLECTION_INVERSE, font_size=40, color=YELLOW),
        )
        caption = Text(
            "Reflect twice across the same line and every point returns to where it started.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), Create(mirror), FadeIn(original), FadeIn(reflected), run_time=self.TRANSITION_TIME)
        self.play(Transform(restored, self._triangle(plane, self.snapshot.triangle, GREEN, opacity=0.22)), run_time=1.6)
        self.add(restored)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, mirror, original, reflected, restored, equations, caption)), run_time=self.TRANSITION_TIME)

    def _why_orthogonal_card(self) -> None:
        heading = Text("Why are these transformations orthogonal?", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        criterion = MathTex(self.lesson.ORTHOGONAL_CRITERION, font_size=34, color=YELLOW).move_to(UP * 1.90)

        left_box = Rectangle(width=5.55, height=3.55, color=GREY_B, stroke_opacity=0.55).move_to(LEFT * 3.10 + DOWN * 0.40)
        right_box = Rectangle(width=5.55, height=3.55, color=GREY_B, stroke_opacity=0.55).move_to(RIGHT * 3.10 + DOWN * 0.40)
        left_title = Text("Rotation", font_size=26, color=GREEN).next_to(left_box, UP, buff=0.14)
        right_title = Text("Reflection", font_size=26, color=YELLOW).next_to(right_box, UP, buff=0.14)

        left_math = VGroup(
            MathTex(r"R_\theta=[R_\theta\mathbf e_1\;R_\theta\mathbf e_2]", font_size=30),
            Text("Its two columns are perpendicular", font_size=22, color=WHITE),
            Text("and each column has length 1.", font_size=22, color=WHITE),
            MathTex(r"\Rightarrow R_\theta^TR_\theta=I", font_size=33, color=GREEN),
        ).arrange(DOWN, buff=0.18).move_to(left_box)

        right_math = VGroup(
            MathTex(r"H=[H\mathbf e_1\;H\mathbf e_2]", font_size=30),
            Text("Its two columns are perpendicular", font_size=22, color=WHITE),
            Text("and each column has length 1.", font_size=22, color=WHITE),
            MathTex(r"\Rightarrow H^TH=I", font_size=33, color=YELLOW),
        ).arrange(DOWN, buff=0.18).move_to(right_box)

        caption = Text(
            "So both transformations send the standard basis to another orthonormal set.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), FadeIn(criterion), Create(left_box), Create(right_box), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(left_math), FadeIn(right_math), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, criterion, left_box, right_box, left_title, right_title, left_math, right_math, caption)), run_time=self.TRANSITION_TIME)

    def _specific_examples_orthogonal_card(self) -> None:
        heading = Text("Check the columns in the specific examples", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left_box = Rectangle(width=5.65, height=4.60, color=GREY_B, stroke_opacity=0.55).move_to(LEFT * 3.08 + DOWN * 0.58)
        right_box = Rectangle(width=5.65, height=4.60, color=GREY_B, stroke_opacity=0.55).move_to(RIGHT * 3.08 + DOWN * 0.58)
        left_title = Text("Rotation example", font_size=25, color=GREEN).next_to(left_box, UP, buff=0.14)
        right_title = Text("Reflection example", font_size=25, color=YELLOW).next_to(right_box, UP, buff=0.14)

        pythagorean_note = Text(
            "The Pythagorean identity gives unit-length columns.",
            font_size=19,
            color=GREY_B,
        )
        max_note_width = left_box.width - 0.50
        if pythagorean_note.width > max_note_width:
            pythagorean_note.scale_to_fit_width(max_note_width)

        left_math = VGroup(
            MathTex(r"R_{60^\circ}=\begin{bmatrix}\frac12&-\frac{\sqrt3}{2}\\[4pt]\frac{\sqrt3}{2}&\frac12\end{bmatrix}", font_size=28),
            MathTex(r"\mathbf q_1=\begin{bmatrix}\frac12\\[2pt]\frac{\sqrt3}{2}\end{bmatrix},\quad \mathbf q_2=\begin{bmatrix}-\frac{\sqrt3}{2}\\[2pt]\frac12\end{bmatrix}", font_size=26),
            MathTex(r"\mathbf q_1^T\mathbf q_2=-\frac{\sqrt3}{4}+\frac{\sqrt3}{4}=0", font_size=27),
            MathTex(r"\|\mathbf q_1\|^2=\frac14+\frac34=1,\quad \|\mathbf q_2\|^2=\frac34+\frac14=1", font_size=25),
            pythagorean_note,
        ).arrange(DOWN, buff=0.15).move_to(left_box)

        right_math = VGroup(
            MathTex(r"H=\begin{bmatrix}1&0\\0&-1\end{bmatrix}", font_size=28),
            MathTex(r"\mathbf h_1=\begin{bmatrix}1\\0\end{bmatrix},\quad \mathbf h_2=\begin{bmatrix}0\\-1\end{bmatrix}", font_size=27),
            MathTex(r"\mathbf h_1^T\mathbf h_2=(1)(0)+(0)(-1)=0", font_size=27),
            MathTex(r"\|\mathbf h_1\|=1,\quad \|\mathbf h_2\|=1", font_size=27),
            Text("Here the arithmetic is immediate.", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.15).move_to(right_box)

        caption = Text(
            "In each concrete matrix, the columns are orthogonal and each has magnitude 1.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_box), Create(right_box), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(left_math), FadeIn(right_math), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, left_box, right_box, left_title, right_title, left_math, right_math, caption)), run_time=self.TRANSITION_TIME)

    def _compare_orientation_card(self) -> None:
        heading = Text("Orientation distinguishes them", font_size=26, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.12
        )
        left_box = Rectangle(width=5.3, height=4.45, color=GREY_B, stroke_opacity=0.55).move_to(LEFT * 3.25 + DOWN * 0.62)
        right_box = Rectangle(width=5.3, height=4.45, color=GREY_B, stroke_opacity=0.55).move_to(RIGHT * 3.25 + DOWN * 0.62)
        left_title = Text("Rotation", font_size=27, color=GREEN).next_to(left_box, UP, buff=0.16)
        right_title = Text("Reflection", font_size=27, color=YELLOW).next_to(right_box, UP, buff=0.16)
        left_math = VGroup(
            MathTex(r"R_\theta^TR_\theta=I", font_size=39),
            MathTex(r"\det R_\theta=+1", font_size=41, color=GREEN),
            Text("orientation preserved", font_size=24, color=GREEN),
        ).arrange(DOWN, buff=0.34).move_to(left_box)
        right_math = VGroup(
            MathTex(r"H^TH=I", font_size=39),
            MathTex(r"\det H=-1", font_size=41, color=YELLOW),
            Text("orientation reversed", font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.34).move_to(right_box)
        title_band = VGroup(left_title, right_title)
        gap_mid_y = 0.5 * (heading.get_bottom()[1] + title_band.get_top()[1])
        orthogonal_text = Text(
            "Rotation and reflection are both orthogonal",
            font_size=24,
            color=WHITE,
        ).move_to(np.array([0.0, gap_mid_y, 0.0]))

        self.play(FadeIn(heading), Create(left_box), Create(right_box), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(orthogonal_text), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(left_math), FadeIn(right_math), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME + 0.5)
        self.play(FadeOut(VGroup(heading, left_box, right_box, left_title, right_title, orthogonal_text, left_math, right_math)), run_time=self.TRANSITION_TIME)
