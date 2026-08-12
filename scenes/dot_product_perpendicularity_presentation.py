"""CP150: Dot Product and Perpendicularity."""

from __future__ import annotations

import numpy as np
from manim import (
    Arc,
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
    Rectangle,
    ReplacementTransform,
    RIGHT,
    RightAngle,
    Scene,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.dot_product_perpendicularity import DotProductPerpendicularityLesson


class DotProductPerpendicularityPresentation(Scene):
    CP150_REVISION = "r6_verified_split_layout_test_fix"
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Dot Product and Perpendicularity"

    def construct(self) -> None:
        self.lesson = DotProductPerpendicularityLesson()
        banner, lesson_title = self._header()
        self.lesson_title_mobject = lesson_title
        self.add(banner, lesson_title)

        self._transitional_question()
        self._coordinate_formula()
        self._geometric_formula()
        self._perpendicularity_test()
        self._sign_interpretation()
        self._takeaway()

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

    def _plane(self) -> NumberPlane:
        return NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-2.5, 3.5, 1),
            x_length=7.2,
            y_length=4.5,
            background_line_style={"stroke_opacity": 0.22},
            axis_config={"stroke_opacity": 0.55},
        ).shift(DOWN * 0.18)

    def _vector_pair_group(
        self,
        plane: NumberPlane,
        first: np.ndarray,
        second: np.ndarray,
        *,
        show_angle: bool = True,
        right_angle: bool = False,
    ) -> VGroup:
        u_arrow = Arrow(
            plane.c2p(0, 0),
            plane.c2p(*first),
            buff=0,
            color=BLUE,
            stroke_width=6,
        )
        v_arrow = Arrow(
            plane.c2p(0, 0),
            plane.c2p(*second),
            buff=0,
            color=GREEN,
            stroke_width=6,
        )
        u_label = MathTex(r"\mathbf{u}", font_size=30, color=BLUE).next_to(
            u_arrow.get_end(), RIGHT, buff=0.10
        )
        v_label = MathTex(r"\mathbf{v}", font_size=30, color=GREEN).next_to(
            v_arrow.get_end(), UP, buff=0.10
        )
        group = VGroup(u_arrow, v_arrow, u_label, v_label)
        if show_angle:
            start = np.arctan2(first[1], first[0])
            end = np.arctan2(second[1], second[0])
            if end < start:
                start, end = end, start
            angle_arc = Arc(
                radius=0.65,
                start_angle=start,
                angle=end - start,
                arc_center=plane.c2p(0, 0),
                color=ORANGE,
            )
            theta = MathTex(r"\theta", font_size=28, color=ORANGE).move_to(
                plane.c2p(0.65 * np.cos((start + end) / 2), 0.65 * np.sin((start + end) / 2))
            )
            group.add(angle_arc, theta)
        if right_angle:
            x_line = Line(plane.c2p(0, 0), plane.c2p(0.75, 0), color=WHITE)
            y_line = Line(plane.c2p(0, 0), plane.c2p(0, 0.75), color=WHITE)
            marker = RightAngle(x_line, y_line, length=0.17, quadrant=(1, 1))
            group.add(marker)
        return group

    def _transitional_question(self) -> None:
        plane = self._plane()
        s = self.lesson.bridge_example()
        pair = self._vector_pair_group(plane, s.first, s.second)
        prompt = Text(
            "How can we recognize perpendicularity algebraically?",
            font_size=29,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.26)
        if prompt.width > 12.2:
            prompt.scale_to_fit_width(12.2)
        caption = Text(
            "The dot product turns geometric alignment into a single number.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.play(Create(plane), FadeIn(prompt), FadeIn(pair))
        self.play(FadeIn(caption))
        self.wait(1.8)
        self.play(FadeOut(VGroup(plane, prompt, pair, caption)))

    def _coordinate_formula(self) -> None:
        vectors = MathTex(
            r"\mathbf{u}=\begin{bmatrix}u_1\\u_2\end{bmatrix},\qquad",
            r"\mathbf{v}=\begin{bmatrix}v_1\\v_2\end{bmatrix}",
            font_size=36,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        formula = MathTex(
            r"\mathbf{u}\cdot\mathbf{v}=u_1v_1+u_2v_2",
            font_size=42,
        ).move_to(DOWN * 0.05)
        caption = Text(
            "The dot product multiplies matching components and adds the results.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        if caption.width > 12.4:
            caption.scale_to_fit_width(12.4)
        self.play(FadeIn(vectors))
        self.play(FadeIn(formula))
        self.play(FadeIn(caption))
        self.wait(1.8)
        self.play(FadeOut(VGroup(vectors, formula, caption)))

    def _geometric_formula(self) -> None:
        plane = self._plane()
        s = self.lesson.bridge_example()
        pair = self._vector_pair_group(plane, s.first, s.second)
        formula = MathTex(
            r"\mathbf{u}\cdot\mathbf{v}=\|\mathbf{u}\|\,\|\mathbf{v}\|\cos\theta",
            font_size=40,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        caption = Text(
            "The dot product depends on both length and alignment.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.play(Create(plane), FadeIn(formula), FadeIn(pair))
        self.play(FadeIn(caption))
        self.wait(2.0)
        self.play(FadeOut(VGroup(plane, formula, pair, caption)))

    def _perpendicularity_test(self) -> None:
        # Card 4 uses a dedicated split layout: geometry entirely on the left,
        # derivation entirely on the right.  Do not reuse the full-width plane.
        plane = NumberPlane(
            x_range=(-1.0, 3.5, 1),
            y_range=(-1.0, 3.5, 1),
            x_length=4.7,
            y_length=4.0,
            background_line_style={"stroke_opacity": 0.22},
            axis_config={"stroke_opacity": 0.55},
        ).move_to(LEFT * 3.05 + DOWN * 0.25)

        s = self.lesson.right_example()
        pair = self._vector_pair_group(
            plane, s.first, s.second, show_angle=False, right_angle=True
        )

        line1 = MathTex(r"\theta=90^\circ", font_size=40)
        line2 = MathTex(r"\cos\theta=0", font_size=40)
        line3 = MathTex(r"\mathbf{u}\cdot\mathbf{v}=0", font_size=42)
        derivation = VGroup(line1, line2, line3).arrange(DOWN, buff=0.28)
        derivation.move_to(RIGHT * 3.05 + UP * 0.35)

        caption = Text(
            "Perpendicular vectors have no directional overlap.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)

        self.play(Create(plane), FadeIn(pair), FadeIn(line1))
        self.play(FadeIn(line2))
        self.play(FadeIn(line3))
        self.play(FadeIn(caption))
        self.wait(2.0)
        self.play(FadeOut(VGroup(plane, pair, derivation, caption)))

    def _sign_interpretation(self) -> None:
        plane = self._plane()
        acute = self.lesson.acute_example()
        right = self.lesson.right_example()
        obtuse = self.lesson.obtuse_example()
        examples = VGroup(
            self._mini_pair(acute.first, acute.second, "acute", r"\mathbf{u}\cdot\mathbf{v}>0"),
            self._mini_pair(right.first, right.second, "right", r"\mathbf{u}\cdot\mathbf{v}=0", right_angle=True),
            self._mini_pair(obtuse.first, obtuse.second, "obtuse", r"\mathbf{u}\cdot\mathbf{v}<0"),
        ).arrange(RIGHT, buff=0.38)
        examples.scale(0.93).move_to(DOWN * 0.18)
        heading = Text(
            "The sign records how the vectors align.",
            font_size=28,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        caption = Text(
            "Positive for acute, zero for right, negative for obtuse.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(heading), FadeIn(examples))
        self.play(FadeIn(caption))
        self.wait(2.3)
        self.play(FadeOut(VGroup(heading, examples, caption)))

    def _mini_pair(
        self,
        first: np.ndarray,
        second: np.ndarray,
        label: str,
        relation: str,
        *,
        right_angle: bool = False,
    ) -> VGroup:
        plane = NumberPlane(
            x_range=(-1.5, 3, 1),
            y_range=(-1.0, 3.0, 1),
            x_length=2.6,
            y_length=2.3,
            background_line_style={"stroke_opacity": 0.18},
            axis_config={"stroke_opacity": 0.45},
        )
        pair = self._vector_pair_group(
            plane, first, second, show_angle=not right_angle, right_angle=right_angle
        )
        name = Text(label, font_size=22, color=WHITE)
        inequality = MathTex(relation, font_size=29)
        stack = VGroup(name, plane, pair, inequality).arrange(DOWN, buff=0.14)
        panel = SurroundingRectangle(stack, buff=0.16, color=GREY_D, stroke_width=1.5)
        return VGroup(panel, stack)

    def _takeaway(self) -> None:
        theorem = MathTex(
            self.lesson.FINAL_STATEMENT,
            font_size=46,
        ).move_to(UP * 0.10)
        box = SurroundingRectangle(theorem, buff=0.22, color=WHITE)
        caption = Text(
            "The dot product gives an algebraic test for orthogonality.",
            font_size=24,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.42)
        bridge = Text(
            "Next: projection will isolate the component in a chosen direction.",
            font_size=22,
            color=YELLOW,
        ).next_to(theorem, DOWN, buff=0.55)
        if bridge.width > 11.6:
            bridge.scale_to_fit_width(11.6)
        self.play(FadeIn(theorem), Create(box))
        self.play(FadeIn(bridge), FadeIn(caption))
        self.wait(2.5)
