"""CP149: Why Orthogonality? — opening Chapter 6 visually."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    BLUE,
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
    Polygon,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    RightAngle,
    Scene,
    Text,
    Transform,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.why_orthogonality import WhyOrthogonalityLesson


class WhyOrthogonalityPresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Why Orthogonality?"

    def construct(self) -> None:
        self.lesson = WhyOrthogonalityLesson()
        banner, lesson_title = self._header()
        self.lesson_title_mobject = lesson_title
        self.add(banner, lesson_title)

        self._determinant_bridge()
        self._compare_bases()
        self._skew_coordinates()
        self._orthogonal_coordinates()
        self._chapter_question()

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
        return VGroup(banner_box, banner_text), lesson_title

    def _plane(self) -> NumberPlane:
        return NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-2.5, 2.5, 1),
            x_length=7.2,
            y_length=4.2,
            background_line_style={"stroke_opacity": 0.22},
            axis_config={"stroke_opacity": 0.55},
        ).shift(DOWN * 0.20)

    def _determinant_bridge(self) -> None:
        s = self.lesson.determinant_bridge()
        plane = self._plane()

        reference = Polygon(
            *[plane.c2p(*point) for point in s.reference_square],
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.22,
            stroke_width=3,
        )
        transformed = Polygon(
            *[plane.c2p(*point) for point in s.transformed_region],
            color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=0.26,
            stroke_width=3,
        )
        equation = MathTex(
            r"|\det A|=\text{area scale factor}",
            font_size=38,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.20)
        equation.shift(UP * 0.02)
        caption = Text(
            "Determinants told us how linear maps change area and volume.",
            font_size=25,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)

        self.play(FadeIn(equation), Create(plane), FadeIn(reference))
        self.play(Transform(reference, transformed), run_time=2.0)
        self.play(FadeIn(caption))
        self.wait(1.5)

        next_caption = Text(
            "But they do not tell us whether our coordinate directions are easy to use.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        if next_caption.width > 12.4:
            next_caption.scale_to_fit_width(12.4)
        self.play(ReplacementTransform(caption, next_caption))
        self.wait(1.8)
        self.play(FadeOut(VGroup(plane, reference, equation, next_caption)))

    def _compare_bases(self) -> None:
        plane = self._plane()
        skew = self.lesson.skew_basis()
        ortho = self.lesson.orthogonal_basis()

        skew_group = self._basis_group(plane, skew.first, skew.second, "v")
        ortho_group = self._basis_group(plane, ortho.first, ortho.second, "u")

        heading = Text(
            "Two bases for the same plane",
            font_size=30,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.28)
        question = Text(
            "Are some bases better than others?",
            font_size=28,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.38)

        self.play(Create(plane), FadeIn(heading), FadeIn(skew_group))
        self.wait(1.0)
        self.play(Transform(skew_group, ortho_group), run_time=2.0)
        self.play(FadeIn(question))
        self.wait(1.8)
        self.play(FadeOut(VGroup(plane, heading, skew_group, question)))

    def _skew_coordinates(self) -> None:
        plane = self._plane()
        s = self.lesson.skew_basis()
        basis = self._basis_group(plane, s.first, s.second, "v")

        target = Arrow(
            plane.c2p(0, 0),
            plane.c2p(*s.target),
            buff=0,
            color=YELLOW,
            stroke_width=6,
        )
        first_component = Arrow(
            plane.c2p(0, 0),
            plane.c2p(*s.first),
            buff=0,
            color=BLUE,
            stroke_width=5,
        )
        second_start = s.first
        second_end = s.first + s.second
        second_component = Arrow(
            plane.c2p(*second_start),
            plane.c2p(*second_end),
            buff=0,
            color=GREEN,
            stroke_width=5,
        )
        equation = MathTex(
            r"\mathbf{x}=c_1\mathbf{v}_1+c_2\mathbf{v}_2",
            font_size=38,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.28)
        caption = Text(
            "In a skew basis, the coordinate directions are not geometrically separated.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        if caption.width > 12.4:
            caption.scale_to_fit_width(12.4)

        self.play(Create(plane), FadeIn(equation), FadeIn(basis))
        self.play(Create(first_component), Create(second_component), Create(target))
        self.play(FadeIn(caption))
        self.wait(1.8)
        self.play(FadeOut(VGroup(plane, basis, first_component, second_component, target, equation, caption)))

    def _orthogonal_coordinates(self) -> None:
        plane = self._plane()
        s = self.lesson.orthogonal_basis()
        basis = self._basis_group(plane, s.first, s.second, "u")

        target = Arrow(
            plane.c2p(0, 0),
            plane.c2p(*s.target),
            buff=0,
            color=YELLOW,
            stroke_width=6,
        )
        horizontal = Arrow(
            plane.c2p(0, 0),
            plane.c2p(s.target[0], 0),
            buff=0,
            color=BLUE,
            stroke_width=5,
        )
        vertical = Arrow(
            plane.c2p(s.target[0], 0),
            plane.c2p(*s.target),
            buff=0,
            color=GREEN,
            stroke_width=5,
        )

        x_line = Line(plane.c2p(0, 0), plane.c2p(0.65, 0), color=WHITE)
        y_line = Line(plane.c2p(0, 0), plane.c2p(0, 0.65), color=WHITE)
        right_angle = RightAngle(x_line, y_line, length=0.17, quadrant=(1, 1))

        equation = MathTex(
            r"\mathbf{x}=a\mathbf{u}_1+b\mathbf{u}_2",
            font_size=38,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.28)
        caption = Text(
            "Perpendicular directions separate the geometric roles of the coordinates.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        if caption.width > 12.4:
            caption.scale_to_fit_width(12.4)

        self.play(Create(plane), FadeIn(equation), FadeIn(basis), FadeIn(right_angle))
        self.play(Create(horizontal), Create(vertical), Create(target), run_time=1.7)
        self.play(FadeIn(caption))
        self.wait(2.0)
        self.play(FadeOut(VGroup(plane, basis, right_angle, horizontal, vertical, target, equation, caption)))

    def _chapter_question(self) -> None:
        question = VGroup(
            Text(
                "What becomes possible",
                font_size=42,
                color=WHITE,
                weight="SEMIBOLD",
            ),
            Text(
                "when our directions are orthogonal?",
                font_size=42,
                color=YELLOW,
                weight="SEMIBOLD",
            ),
        ).arrange(DOWN, buff=0.16).move_to(UP * 0.75)

        topics = VGroup(
            *[
                Text(topic, font_size=27, color=GREY_B)
                for topic in self.lesson.preview_topics
            ]
        ).arrange(DOWN, buff=0.18).next_to(question, DOWN, buff=0.45)

        self.play(FadeIn(question, shift=UP * 0.10))
        for topic in topics:
            self.play(FadeIn(topic), run_time=0.45)
        self.wait(2.4)

    def _basis_group(
        self,
        plane: NumberPlane,
        first: np.ndarray,
        second: np.ndarray,
        symbol: str,
    ) -> VGroup:
        first_arrow = Arrow(
            plane.c2p(0, 0),
            plane.c2p(*first),
            buff=0,
            color=BLUE,
            stroke_width=6,
        )
        second_arrow = Arrow(
            plane.c2p(0, 0),
            plane.c2p(*second),
            buff=0,
            color=GREEN,
            stroke_width=6,
        )
        first_label = MathTex(
            rf"\mathbf{{{symbol}}}_1",
            font_size=30,
            color=BLUE,
        ).next_to(first_arrow.get_end(), RIGHT, buff=0.10)
        second_label = MathTex(
            rf"\mathbf{{{symbol}}}_2",
            font_size=30,
            color=GREEN,
        ).next_to(second_arrow.get_end(), UP, buff=0.10)
        return VGroup(first_arrow, second_arrow, first_label, second_label)
