"""CP157: Gram-Schmidt with Two Vectors."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    BLUE,
    Create,
    DashedLine,
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
    PURPLE,
    Polygon,
    Rectangle,
    RIGHT,
    Scene,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.gram_schmidt_two_vectors import GramSchmidtTwoVectorsLesson


class GramSchmidtTwoVectorsPresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Gram-Schmidt with Two Vectors"
    SCENE_REVISION = "cp157_r6_card2_marker_natural_quadrant"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.0
    HOLD_TIME = 2.2

    def construct(self) -> None:
        self.lesson = GramSchmidtTwoVectorsLesson()
        self.snapshot = self.lesson.pair_snapshot()
        self.banner, self.lesson_title_mobject = self._header()
        self.add(self.banner, self.lesson_title_mobject)

        self._starting_pair_card()
        self._projection_card()
        self._subtract_projection_card()
        self._orthogonality_card()
        self._summary_card()
        self._bridge_card()

    def _header(self) -> tuple[VGroup, Text]:
        banner_box = Rectangle(
            width=13.5,
            height=0.58,
            stroke_width=0,
            fill_color=GREY_D,
            fill_opacity=0.96,
        ).to_edge(UP, buff=0.08)
        banner_text = Text(self.CHAPTER_BANNER, font_size=28, color=WHITE).move_to(banner_box)
        lesson_title = Text(self.LESSON_TITLE, font_size=31, color=YELLOW).next_to(
            banner_box, DOWN, buff=0.18
        )
        if lesson_title.width > 11.8:
            lesson_title.scale_to_fit_width(11.8)
        return VGroup(banner_box, banner_text), lesson_title

    @staticmethod
    def _plane() -> NumberPlane:
        return NumberPlane(
            x_range=(-1.0, 5.5, 1),
            y_range=(-1.5, 5.5, 1),
            x_length=5.9,
            y_length=5.9,
            background_line_style={"stroke_opacity": 0.20},
            axis_config={"stroke_opacity": 0.55},
        ).shift(LEFT * 2.55 + DOWN * 0.25)

    @staticmethod
    def _arrow(plane: NumberPlane, vector: np.ndarray, color) -> Arrow:
        return Arrow(plane.c2p(0, 0), plane.c2p(*vector), buff=0, color=color, stroke_width=6)

    @staticmethod
    def _label(text: str, point: np.ndarray, plane: NumberPlane, color, shift_vec=UP * 0.18) -> MathTex:
        return MathTex(text, font_size=31, color=color).move_to(plane.c2p(*point) + shift_vec)

    @staticmethod
    def _right_angle_marker(plane: NumberPlane, point: np.ndarray, along: np.ndarray, perp: np.ndarray) -> VGroup:
        along_u = along / np.linalg.norm(along)
        perp_u = perp / np.linalg.norm(perp)
        a = point + 0.24 * along_u
        c = point + 0.24 * perp_u
        b = a + 0.24 * perp_u
        return VGroup(
            Line(plane.c2p(*a), plane.c2p(*b), color=WHITE, stroke_width=3),
            Line(plane.c2p(*c), plane.c2p(*b), color=WHITE, stroke_width=3),
        )

    def _starting_pair_card(self) -> None:
        heading = Text("Start with a spanning pair", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        v1_arrow = self._arrow(plane, self.snapshot.v1, ORANGE)
        v2_arrow = self._arrow(plane, self.snapshot.v2, BLUE)
        span_fill = Polygon(
            plane.c2p(0, 0),
            plane.c2p(*self.snapshot.v1),
            plane.c2p(*(self.snapshot.v1 + self.snapshot.v2)),
            plane.c2p(*self.snapshot.v2),
            fill_color=GREEN,
            fill_opacity=0.12,
            stroke_opacity=0,
        )
        v1_label = self._label(r"\mathbf v_1", self.snapshot.v1, plane, ORANGE, RIGHT * 0.28 + UP * 0.12)
        v2_label = self._label(r"\mathbf v_2", self.snapshot.v2, plane, BLUE, RIGHT * 0.28 + UP * 0.14)
        equation = MathTex(
            r"\operatorname{span}\{\mathbf v_1,\mathbf v_2\}",
            font_size=41,
        ).move_to(RIGHT * 3.35 + UP * 0.35)
        caption = Text(
            "The directions span the plane, but they are not yet orthogonal.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(v1_arrow), FadeIn(v1_label), Create(v2_arrow), FadeIn(v2_label), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(span_fill), FadeIn(equation), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, plane, v1_arrow, v2_arrow, span_fill, v1_label, v2_label, equation, caption)),
            run_time=self.TRANSITION_TIME,
        )

    def _projection_card(self) -> None:
        heading = Text("Project the second vector onto the first", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        u1_arrow = self._arrow(plane, self.snapshot.u1, ORANGE)
        v2_arrow = self._arrow(plane, self.snapshot.v2, BLUE)
        proj_arrow = self._arrow(plane, self.snapshot.projection, GREEN)
        residual_segment = DashedLine(
            plane.c2p(*self.snapshot.projection),
            plane.c2p(*self.snapshot.v2),
            color=GREEN,
        )
        u1_label = self._label(r"\mathbf u_1=\mathbf v_1", self.snapshot.u1, plane, ORANGE, LEFT * 0.58 + UP * 0.62)
        v2_label = self._label(r"\mathbf v_2", self.snapshot.v2, plane, BLUE, RIGHT * 0.26 + UP * 0.16)
        proj_label = self._label(r"\operatorname{proj}_{\mathbf u_1}\mathbf v_2", self.snapshot.projection, plane, GREEN, LEFT * 0.62 + UP * 0.34)
        equations = VGroup(
            MathTex(r"\operatorname{proj}_{\mathbf u_1}\mathbf v_2", font_size=36),
            MathTex(r"=\frac{\mathbf v_2\cdot\mathbf u_1}{\mathbf u_1\cdot\mathbf u_1}\mathbf u_1", font_size=36),
            MathTex(r"=2\mathbf u_1=(2,4)", font_size=36, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.45 + UP * 0.55)
        right_angle = self._right_angle_marker(
            plane,
            self.snapshot.projection,
            -self.snapshot.u1,
            self.snapshot.v2 - self.snapshot.projection,
        )
        caption = Text(
            "The small square marks that the leftover direction is perpendicular to u1.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(u1_arrow), FadeIn(u1_label), Create(v2_arrow), FadeIn(v2_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(proj_arrow), Create(residual_segment), Create(right_angle), FadeIn(proj_label), FadeIn(equations), FadeIn(caption), run_time=self.TRANSITION_TIME)
        self.wait(self.HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, plane, u1_arrow, v2_arrow, proj_arrow, residual_segment, right_angle, u1_label, v2_label, proj_label, equations, caption)),
            run_time=self.TRANSITION_TIME,
        )

    def _subtract_projection_card(self) -> None:
        heading = Text("Subtract the parallel part", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        u1_arrow = self._arrow(plane, self.snapshot.u1, ORANGE)
        v2_arrow = self._arrow(plane, self.snapshot.v2, BLUE)
        proj_arrow = self._arrow(plane, self.snapshot.projection, GREEN)
        residual_segment = Arrow(
            plane.c2p(*self.snapshot.projection),
            plane.c2p(*self.snapshot.v2),
            buff=0,
            color=PURPLE,
            stroke_width=6,
        )
        u2_arrow = self._arrow(plane, self.snapshot.u2, PURPLE)
        u1_label = self._label(r"\mathbf u_1", self.snapshot.u1, plane, ORANGE, LEFT * 0.05 + UP * 0.34)
        v2_label = self._label(r"\mathbf v_2", self.snapshot.v2, plane, BLUE, RIGHT * 0.26 + UP * 0.16)
        u2_label = self._label(r"\mathbf u_2", self.snapshot.u2, plane, PURPLE, RIGHT * 0.34 + DOWN * 0.18)
        equations = VGroup(
            MathTex(self.lesson.STEP_FORMULA, font_size=35),
            MathTex(r"=(4,3)-(2,4)", font_size=35),
            MathTex(r"=(2,-1)", font_size=35, color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.35 + UP * 0.25)
        caption = Text(
            "What remains is a new direction with the parallel piece removed.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(u1_arrow), FadeIn(u1_label), Create(v2_arrow), FadeIn(v2_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(proj_arrow), Create(residual_segment), run_time=self.EMPHASIS_TIME)
        self.play(
            residual_segment.animate.put_start_and_end_on(plane.c2p(0, 0), plane.c2p(*self.snapshot.u2)),
            FadeIn(u2_label),
            FadeIn(equations),
            FadeIn(caption),
            run_time=self.TRANSITION_TIME,
        )
        self.wait(self.HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, plane, u1_arrow, v2_arrow, proj_arrow, residual_segment, u1_label, v2_label, u2_label, equations, caption)),
            run_time=self.TRANSITION_TIME,
        )

    def _orthogonality_card(self) -> None:
        heading = Text("Now the directions are orthogonal", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        u1_arrow = self._arrow(plane, self.snapshot.u1, ORANGE)
        u2_arrow = self._arrow(plane, self.snapshot.u2, PURPLE)
        right_angle = self._right_angle_marker(plane, np.array([0.0, 0.0]), self.snapshot.u1, self.snapshot.u2)
        u1_label = self._label(r"\mathbf u_1", self.snapshot.u1, plane, ORANGE, LEFT * 0.05 + UP * 0.34)
        u2_label = self._label(r"\mathbf u_2", self.snapshot.u2, plane, PURPLE, RIGHT * 0.34 + DOWN * 0.18)
        equations = VGroup(
            MathTex(r"\mathbf u_1\cdot\mathbf u_2", font_size=38),
            MathTex(r"=(1,2)\cdot(2,-1)", font_size=38),
            MathTex(r"=2-2=0", font_size=38, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(RIGHT * 3.35 + UP * 0.25)
        caption = Text(
            "The subtraction step forces the new direction to be perpendicular.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), Create(plane), Create(u1_arrow), Create(u2_arrow), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(u1_label), FadeIn(u2_label), Create(right_angle), FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, plane, u1_arrow, u2_arrow, right_angle, u1_label, u2_label, equations, caption)),
            run_time=self.TRANSITION_TIME,
        )

    def _summary_card(self) -> None:
        heading = Text("Gram-Schmidt step", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        box_math = VGroup(
            MathTex(r"\mathbf u_1=\mathbf v_1", font_size=39),
            MathTex(self.lesson.GENERAL_FORMULA, font_size=37),
            MathTex(self.lesson.SPAN_FACT, font_size=35, color=YELLOW),
        ).arrange(DOWN, buff=0.34).move_to(DOWN * 0.05)
        box = SurroundingRectangle(box_math, buff=0.28, color=WHITE)
        caption = Text(
            "Projection is the engine: subtract each earlier component to create an orthogonal direction.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(heading), FadeIn(box_math[0]), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(box_math[1]), run_time=self.EMPHASIS_TIME)
        self.play(Create(box), FadeIn(box_math[2]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, box_math, box, caption)), run_time=self.TRANSITION_TIME)

    def _bridge_card(self) -> None:
        heading = Text("Next question", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        prompt = Text(self.lesson.bridge_prompt, font_size=31, color=YELLOW).move_to(UP * 0.9)
        if prompt.width > 11.4:
            prompt.scale_to_fit_width(11.4)
        equations = VGroup(
            MathTex(r"\mathbf e_1=\frac{\mathbf u_1}{\|\mathbf u_1\|}", font_size=38),
            MathTex(r"\mathbf e_2=\frac{\mathbf u_2}{\|\mathbf u_2\|}", font_size=38),
        ).arrange(DOWN, buff=0.28).move_to(DOWN * 0.42)
        caption = Text(
            "That normalization step turns an orthogonal basis into an orthonormal one.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), FadeIn(prompt), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
