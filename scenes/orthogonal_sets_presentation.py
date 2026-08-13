"""CP151: Orthogonal Sets."""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    Create,
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    GREY_B,
    GREY_D,
    LEFT,
    MathTex,
    ORANGE,
    Rectangle,
    RIGHT,
    Scene,
    SurroundingRectangle,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)
try:
    from manim import Arrow3D
except ImportError:  # pragma: no cover - compatibility shim
    from manim.opengl import OpenGLArrow as Arrow3D

from engine.orthogonal_sets import OrthogonalSetsLesson


class OrthogonalSetsPresentation(ThreeDScene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Orthogonal Sets"
    SCENE_REVISION = "cp151_r14_expanded_3d_rotation"

    def construct(self) -> None:
        self.lesson = OrthogonalSetsLesson()
        banner, lesson_title = self._header()
        self.lesson_title_mobject = lesson_title
        self.add_fixed_in_frame_mobjects(banner, lesson_title)
        self.add(banner, lesson_title)

        self._transition_to_collections()
        self._definition_card()
        self._orthogonal_example_card()
        self._nonexample_card()
        self._independence_card()
        self._bridge_card()

    def _header(self) -> tuple[VGroup, Text]:
        banner_box = Rectangle(
            width=13.5,
            height=0.58,
            stroke_width=0,
            fill_color=GREY_D,
            fill_opacity=0.96,
        ).to_edge(UP, buff=0.08)
        banner_text = Text(
            self.CHAPTER_BANNER,
            font_size=28,
            color=WHITE,
        ).move_to(banner_box)
        lesson_title = Text(
            self.LESSON_TITLE,
            font_size=31,
            color=YELLOW,
        ).next_to(banner_box, DOWN, buff=0.18)
        if lesson_title.width > 11.8:
            lesson_title.scale_to_fit_width(11.8)
        return VGroup(banner_box, banner_text), lesson_title

    def _vector3(self, axes: ThreeDAxes, end: np.ndarray, color: str) -> Arrow3D:
        return Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(*end),
            color=color,
            resolution=8,
            thickness=0.025,
            base_radius=0.04,
            height=0.14,
        )

    def _set_camera_default(self) -> None:
        self.set_camera_orientation(phi=58 * DEGREES, theta=-15 * DEGREES, zoom=0.90)

    def _transition_to_collections(self) -> None:
        question = Text(
            "Two vectors are perpendicular when their dot product is zero.",
            font_size=28,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.26)
        if question.width > 12.0:
            question.scale_to_fit_width(12.0)
        next_question = Text(
            "What if we have a whole collection of vectors?",
            font_size=31,
            color=YELLOW,
        ).move_to(UP * 0.35)
        caption = Text(
            "Now orthogonality becomes a pairwise condition across the set.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(question, next_question, caption)
        self.play(FadeIn(question))
        self.play(FadeIn(next_question))
        self.play(FadeIn(caption))
        self.wait(1.8)
        self.play(FadeOut(VGroup(question, next_question, caption)))
        self.remove_fixed_in_frame_mobjects(question, next_question, caption)

    def _definition_card(self) -> None:
        heading = Text(
            "Definition",
            font_size=30,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        formula = MathTex(self.lesson.DEFINITION, font_size=37).move_to(UP * 0.25)
        caption = Text(
            "Every distinct pair must have dot product zero.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)
        self.add_fixed_in_frame_mobjects(heading, formula, caption)
        self.play(FadeIn(heading), FadeIn(formula))
        self.play(FadeIn(caption))
        self.wait(2.0)
        self.play(FadeOut(VGroup(heading, formula, caption)))
        self.remove_fixed_in_frame_mobjects(heading, formula, caption)

    def _orthogonal_example_card(self) -> None:
        self._set_camera_default()
        axes = ThreeDAxes(
            x_range=(-0.5, 2.8, 1),
            y_range=(-0.5, 2.8, 1),
            z_range=(-0.5, 2.8, 1),
            x_length=3.9,
            y_length=3.9,
            z_length=3.9,
        ).shift(RIGHT * 2.60 + DOWN * 2.45)
        s = self.lesson.orthogonal_example()
        arrows = VGroup(
            self._vector3(axes, s.vectors[0], BLUE),
            self._vector3(axes, s.vectors[1], GREEN),
            self._vector3(axes, s.vectors[2], ORANGE),
        )
        heading = Text(
            "An orthogonal set in R^3",
            font_size=30,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        dots = VGroup(
            MathTex(r"\mathbf{v}_1\cdot\mathbf{v}_2=0", font_size=35),
            MathTex(r"\mathbf{v}_1\cdot\mathbf{v}_3=0", font_size=35),
            MathTex(r"\mathbf{v}_2\cdot\mathbf{v}_3=0", font_size=35),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.0 + UP * 0.15)
        caption = Text(
            "Three nonzero directions can all be perpendicular in 3-space.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(heading, dots, caption)
        self.play(FadeIn(heading), Create(axes))
        for arrow in arrows:
            self.play(Create(arrow), run_time=0.45)
        self.move_camera(phi=62 * DEGREES, theta=28 * DEGREES, zoom=0.92, run_time=2.6)
        self.play(FadeIn(dots), FadeIn(caption))
        self.wait(1.6)
        self.play(FadeOut(VGroup(axes, arrows, heading, dots, caption)))
        self.remove_fixed_in_frame_mobjects(heading, dots, caption)

    def _nonexample_card(self) -> None:
        self._set_camera_default()
        axes = ThreeDAxes(
            x_range=(-0.5, 2.8, 1),
            y_range=(-0.5, 2.8, 1),
            z_range=(-0.5, 2.8, 1),
            x_length=3.9,
            y_length=3.9,
            z_length=3.9,
        ).shift(RIGHT * 2.60 + DOWN * 2.45)
        s = self.lesson.nonexample()
        arrows = VGroup(
            self._vector3(axes, s.vectors[0], BLUE),
            self._vector3(axes, s.vectors[1], GREEN),
            self._vector3(axes, s.vectors[2], ORANGE),
        )
        heading = Text(
            "One good pair is not enough",
            font_size=30,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        dots = VGroup(
            MathTex(r"\mathbf{w}_1\cdot\mathbf{w}_2=0", font_size=35),
            MathTex(r"\mathbf{w}_2\cdot\mathbf{w}_3=0", font_size=35),
            MathTex(r"\mathbf{w}_1\cdot\mathbf{w}_3\neq 0", font_size=35, color=YELLOW),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.05 + UP * 0.15)
        caption = Text(
            "An orthogonal set requires every distinct pair to be perpendicular.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(heading, dots, caption)
        self.play(FadeIn(heading), Create(axes))
        for arrow in arrows:
            self.play(Create(arrow), run_time=0.45)
        self.move_camera(phi=62 * DEGREES, theta=25 * DEGREES, zoom=0.92, run_time=2.6)
        self.play(FadeIn(dots), FadeIn(caption))
        self.wait(1.8)
        self.play(FadeOut(VGroup(axes, arrows, heading, dots, caption)))
        self.remove_fixed_in_frame_mobjects(heading, dots, caption)

    def _independence_card(self) -> None:
        heading = Text(
            "Why orthogonal sets matter",
            font_size=30,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        line1 = MathTex(r"c_1\mathbf{v}_1+\cdots+c_k\mathbf{v}_k=\mathbf{0}", font_size=38)
        line2 = MathTex(r"\text{Dot with }\mathbf{v}_j", font_size=36)
        line3 = MathTex(r"c_j\,\mathbf{v}_j\cdot\mathbf{v}_j=0", font_size=38)
        line4 = MathTex(r"c_j\,\|\mathbf{v}_j\|^2=0\quad\Rightarrow\quad c_j=0", font_size=38)
        derivation = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.18).move_to(UP * 0.15)
        theorem = MathTex(self.lesson.THEOREM, font_size=38).move_to(DOWN * 1.55)
        theorem_box = SurroundingRectangle(theorem, buff=0.18, color=WHITE)
        caption = Text(
            "Because each nonzero vector is orthogonal to the others, every coefficient must vanish.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.16)
        if caption.width > 12.1:
            caption.scale_to_fit_width(12.1)
        self.add_fixed_in_frame_mobjects(heading, derivation, theorem, theorem_box, caption)
        self.play(FadeIn(heading), FadeIn(line1))
        self.play(FadeIn(line2))
        self.play(FadeIn(line3))
        self.play(FadeIn(line4))
        self.play(FadeIn(theorem), Create(theorem_box), FadeIn(caption))
        self.wait(2.2)
        self.play(FadeOut(VGroup(heading, derivation, theorem, theorem_box, caption)))
        self.remove_fixed_in_frame_mobjects(heading, derivation, theorem, theorem_box, caption)

    def _bridge_card(self) -> None:
        heading = Text(
            "Next question",
            font_size=30,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        title = Text(
            "What if the vectors are also unit length?",
            font_size=32,
            color=YELLOW,
        ).move_to(UP * 0.88)
        first, second = self.lesson.bridge_to_orthonormal
        conditions = VGroup(
            MathTex(first, font_size=38),
            MathTex(second, font_size=38),
        ).arrange(DOWN, buff=0.28).move_to(DOWN * 0.15)
        caption = Text(
            "That stronger condition leads naturally to orthonormal sets.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(heading, title, conditions, caption)
        self.play(FadeIn(heading), FadeIn(title))
        self.play(FadeIn(conditions))
        self.play(FadeIn(caption))
        self.wait(2.0)
