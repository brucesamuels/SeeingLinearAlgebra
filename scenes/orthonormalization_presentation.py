"""CP158: From Orthogonal to Orthonormal."""

from __future__ import annotations

import numpy as np
from manim import (
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
    PURPLE,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    Scene,
    Text,
    Transform,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.orthonormalization import OrthonormalizationLesson


class OrthonormalizationPresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "From Orthogonal to Orthonormal"
    SCENE_REVISION = "cp158_r3_grid_on_all_graphic_cards"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.05
    HOLD_TIME = 2.3

    def construct(self) -> None:
        self.lesson = OrthonormalizationLesson()
        self.snapshot = self.lesson.snapshot()
        self.banner, self.lesson_title_mobject = self._header()
        self.add(self.banner, self.lesson_title_mobject)

        self._recall_orthogonal_pair_card()
        self._normalize_first_card()
        self._normalize_second_card()
        self._unit_circle_card()
        self._orthonormal_summary_card()
        self._bridge_to_qr_card()

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
    def _plane(*, wide: bool = True, emphasized_grid: bool = False) -> NumberPlane:
        if emphasized_grid:
            background_line_style = {"stroke_opacity": 0.34, "stroke_width": 1.6}
            axis_config = {"stroke_opacity": 0.72, "stroke_width": 2.2}
        else:
            background_line_style = {"stroke_opacity": 0.20}
            axis_config = {"stroke_opacity": 0.55}
        if wide:
            return NumberPlane(
                x_range=(-1.5, 4.5, 1),
                y_range=(-2.5, 4.0, 1),
                x_length=5.7,
                y_length=6.175,
                background_line_style=background_line_style,
                axis_config=axis_config,
            ).shift(LEFT * 2.65 + DOWN * 0.30)
        return NumberPlane(
            x_range=(-1.6, 1.6, 0.5),
            y_range=(-1.6, 1.6, 0.5),
            x_length=5.25,
            y_length=5.25,
            background_line_style=background_line_style,
            axis_config=axis_config,
        ).shift(LEFT * 2.65 + DOWN * 0.32)

    @staticmethod
    def _arrow(plane: NumberPlane, vector: np.ndarray, color) -> Arrow:
        return Arrow(plane.c2p(0, 0), plane.c2p(*vector), buff=0, color=color, stroke_width=6)

    @staticmethod
    def _label(text: str, plane: NumberPlane, point: np.ndarray, color, offset=UP * 0.18) -> MathTex:
        return MathTex(text, font_size=31, color=color).move_to(plane.c2p(*point) + offset)

    @staticmethod
    def _right_angle_marker(
        plane: NumberPlane,
        point: np.ndarray,
        along: np.ndarray,
        perp: np.ndarray,
        size: float = 0.18,
    ) -> VGroup:
        along_u = along / np.linalg.norm(along)
        perp_u = perp / np.linalg.norm(perp)
        a = point + size * along_u
        c = point + size * perp_u
        b = a + size * perp_u
        return VGroup(
            Line(plane.c2p(*a), plane.c2p(*b), color=WHITE, stroke_width=3),
            Line(plane.c2p(*c), plane.c2p(*b), color=WHITE, stroke_width=3),
        )

    def _recall_orthogonal_pair_card(self) -> None:
        heading = Text("Start with the orthogonal pair from Gram-Schmidt", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane(emphasized_grid=True)
        u1_arrow = self._arrow(plane, self.snapshot.u1, ORANGE)
        u2_arrow = self._arrow(plane, self.snapshot.u2, PURPLE)
        u1_label = self._label(r"\mathbf u_1=(1,2)", plane, self.snapshot.u1, ORANGE, LEFT * 0.18 + UP * 0.36)
        u2_label = self._label(r"\mathbf u_2=(2,-1)", plane, self.snapshot.u2, PURPLE, RIGHT * 0.48 + DOWN * 0.20)
        right_angle = self._right_angle_marker(plane, np.zeros(2), self.snapshot.u1, self.snapshot.u2)
        facts = VGroup(
            MathTex(r"\mathbf u_1\cdot\mathbf u_2=0", font_size=39, color=YELLOW),
            MathTex(r"\|\mathbf u_1\|=\|\mathbf u_2\|=\sqrt5", font_size=37),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.35 + UP * 0.28)
        caption = Text(
            "They are perpendicular, but neither vector has unit length.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(u1_arrow), Create(u2_arrow), FadeIn(u1_label), FadeIn(u2_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(right_angle), FadeIn(facts), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, u1_arrow, u2_arrow, u1_label, u2_label, right_angle, facts, caption)), run_time=self.TRANSITION_TIME)

    def _normalize_first_card(self) -> None:
        heading = Text("Normalize the first direction", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane(emphasized_grid=True)
        u1_arrow = self._arrow(plane, self.snapshot.u1, ORANGE)
        u2_arrow = self._arrow(plane, self.snapshot.u2, PURPLE)
        e1_arrow = self._arrow(plane, self.snapshot.e1, ORANGE)
        u1_label = self._label(r"\mathbf u_1", plane, self.snapshot.u1, ORANGE, LEFT * 0.05 + UP * 0.34)
        e1_label = self._label(r"\mathbf e_1", plane, self.snapshot.e1, ORANGE, LEFT * 0.35 + UP * 0.26)
        u2_label = self._label(r"\mathbf u_2", plane, self.snapshot.u2, PURPLE, RIGHT * 0.34 + DOWN * 0.18)
        formulas = VGroup(
            MathTex(self.lesson.NORMALIZE_1, font_size=37),
            MathTex(r"=\frac{1}{\sqrt5}(1,2)", font_size=37),
            MathTex(r"\|\mathbf e_1\|=1", font_size=37, color=YELLOW),
        ).arrange(DOWN, buff=0.26).move_to(RIGHT * 3.35 + UP * 0.18)
        caption = Text(
            "Normalization changes length, not direction.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), Create(plane), Create(u1_arrow), Create(u2_arrow), FadeIn(u1_label), FadeIn(u2_label), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(formulas[0]), run_time=self.EMPHASIS_TIME)
        self.play(ReplacementTransform(u1_arrow, e1_arrow), FadeOut(u1_label), FadeIn(e1_label), FadeIn(formulas[1]), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(formulas[2]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, e1_arrow, u2_arrow, e1_label, u2_label, formulas, caption)), run_time=self.TRANSITION_TIME)

    def _normalize_second_card(self) -> None:
        heading = Text("Normalize the second direction", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane(emphasized_grid=True)
        e1_arrow = self._arrow(plane, self.snapshot.e1, ORANGE)
        u2_arrow = self._arrow(plane, self.snapshot.u2, PURPLE)
        e2_arrow = self._arrow(plane, self.snapshot.e2, PURPLE)
        e1_label = self._label(r"\mathbf e_1", plane, self.snapshot.e1, ORANGE, LEFT * 0.35 + UP * 0.26)
        u2_label = self._label(r"\mathbf u_2", plane, self.snapshot.u2, PURPLE, RIGHT * 0.34 + DOWN * 0.18)
        e2_label = self._label(r"\mathbf e_2", plane, self.snapshot.e2, PURPLE, RIGHT * 0.40 + DOWN * 0.20)
        formulas = VGroup(
            MathTex(self.lesson.NORMALIZE_2, font_size=37),
            MathTex(r"=\frac{1}{\sqrt5}(2,-1)", font_size=37),
            MathTex(r"\|\mathbf e_2\|=1", font_size=37, color=YELLOW),
        ).arrange(DOWN, buff=0.26).move_to(RIGHT * 3.35 + UP * 0.18)
        caption = Text(
            "Both directions now have length one, and their angle has not changed.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), Create(plane), Create(e1_arrow), Create(u2_arrow), FadeIn(e1_label), FadeIn(u2_label), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(formulas[0]), run_time=self.EMPHASIS_TIME)
        self.play(ReplacementTransform(u2_arrow, e2_arrow), FadeOut(u2_label), FadeIn(e2_label), FadeIn(formulas[1]), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(formulas[2]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, e1_arrow, e2_arrow, e1_label, e2_label, formulas, caption)), run_time=self.TRANSITION_TIME)

    def _unit_circle_card(self) -> None:
        heading = Text("Unit length and perpendicularity together", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane(wide=False, emphasized_grid=True)
        radius = np.linalg.norm(plane.c2p(1, 0) - plane.c2p(0, 0))
        unit_circle = Circle(radius=radius, color=GREEN, stroke_width=3).move_to(plane.c2p(0, 0))
        e1_arrow = self._arrow(plane, self.snapshot.e1, ORANGE)
        e2_arrow = self._arrow(plane, self.snapshot.e2, PURPLE)
        e1_label = self._label(r"\mathbf e_1", plane, self.snapshot.e1, ORANGE, LEFT * 0.28 + UP * 0.25)
        e2_label = self._label(r"\mathbf e_2", plane, self.snapshot.e2, PURPLE, RIGHT * 0.34 + DOWN * 0.16)
        right_angle = self._right_angle_marker(plane, np.zeros(2), self.snapshot.e1, self.snapshot.e2, size=0.13)
        facts = VGroup(
            MathTex(self.lesson.UNIT_FACTS, font_size=38, color=GREEN),
            MathTex(self.lesson.ORTHOGONALITY, font_size=38, color=YELLOW),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.30 + UP * 0.30)
        caption = Text(
            "An orthonormal set consists of mutually perpendicular unit vectors.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), Create(plane), Create(unit_circle), run_time=self.TRANSITION_TIME)
        self.play(Create(e1_arrow), Create(e2_arrow), FadeIn(e1_label), FadeIn(e2_label), Create(right_angle), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(facts), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, unit_circle, e1_arrow, e2_arrow, e1_label, e2_label, right_angle, facts, caption)), run_time=self.TRANSITION_TIME)

    def _orthonormal_summary_card(self) -> None:
        heading = Text("What normalization preserves", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        statements = VGroup(
            MathTex(r"\mathbf e_i=\frac{\mathbf u_i}{\|\mathbf u_i\|}", font_size=40),
            MathTex(self.lesson.UNIT_FACTS, font_size=37, color=GREEN),
            MathTex(self.lesson.ORTHOGONALITY, font_size=37, color=YELLOW),
            MathTex(self.lesson.SPAN_FACT, font_size=34),
        ).arrange(DOWN, buff=0.34).move_to(DOWN * 0.02)
        caption = Text(
            "Lengths change; directions, perpendicularity, and the spanned subspace do not.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(heading), FadeIn(statements[0]), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(statements[1]), FadeIn(statements[2]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(statements[3]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, statements, caption)), run_time=self.TRANSITION_TIME)

    def _bridge_to_qr_card(self) -> None:
        heading = Text("Next question", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        prompt = Text(self.lesson.bridge_prompt, font_size=30, color=YELLOW).move_to(UP * 0.92)
        if prompt.width > 11.4:
            prompt.scale_to_fit_width(11.4)
        q_matrix = MathTex(
            r"Q=\begin{bmatrix}\vert&\vert\\ \mathbf e_1&\mathbf e_2\\ \vert&\vert\end{bmatrix}",
            font_size=42,
        ).move_to(LEFT * 2.15 + DOWN * 0.48)
        property_math = VGroup(
            MathTex(r"Q^TQ=I", font_size=42, color=GREEN),
            MathTex(r"A=QR", font_size=43, color=YELLOW),
        ).arrange(DOWN, buff=0.38).move_to(RIGHT * 2.45 + DOWN * 0.48)
        caption = Text(
            "Orthonormal columns are the geometric heart of QR factorization.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), FadeIn(prompt), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(q_matrix), FadeIn(property_math[0]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(property_math[1]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
