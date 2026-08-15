"""CP160: QR Factorization - Gram-Schmidt in matrix form."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Circle,
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
    Rectangle,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    BLUE,
    TEAL,
)

from engine.qr_factorization import QRFactorizationLesson


class QRFactorizationPresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "QR Factorization: Gram-Schmidt in Matrix Form"
    SCENE_REVISION = "cp160_r4_right_title_clearance"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.05
    HOLD_TIME = 2.3

    def construct(self) -> None:
        self.lesson = QRFactorizationLesson()
        self.snapshot = self.lesson.snapshot()
        self.banner, self.lesson_title_mobject = self._header()
        self.add(self.banner, self.lesson_title_mobject)

        self._original_columns_card()
        self._orthonormal_columns_card()
        self._first_column_coefficients_card()
        self._second_column_coefficients_card()
        self._assemble_qr_card()
        self._inverse_trick_for_r_card()
        self._why_qr_helps_card()

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
    def _plane(*, closeup: bool = False) -> NumberPlane:
        if closeup:
            return NumberPlane(
                x_range=(-1.6, 1.6, 0.5),
                y_range=(-1.6, 1.6, 0.5),
                x_length=5.35,
                y_length=5.35,
                background_line_style={"stroke_opacity": 0.34, "stroke_width": 1.6},
                axis_config={"stroke_opacity": 0.72, "stroke_width": 2.2},
            ).shift(LEFT * 2.75 + DOWN * 0.45)
        return NumberPlane(
            x_range=(-1.0, 5.0, 1),
            y_range=(-2.0, 5.0, 1),
            x_length=5.75,
            y_length=5.55,
            background_line_style={"stroke_opacity": 0.34, "stroke_width": 1.6},
            axis_config={"stroke_opacity": 0.72, "stroke_width": 2.2},
        ).shift(LEFT * 2.70 + DOWN * 0.50)

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
    def _right_angle_marker(
        plane: NumberPlane,
        point: np.ndarray,
        along: np.ndarray,
        perp: np.ndarray,
        size: float = 0.15,
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

    def _original_columns_card(self) -> None:
        heading = Text("Begin with the columns of A", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        a1_arrow = self._arrow(plane, self.snapshot.a1, ORANGE)
        a2_arrow = self._arrow(plane, self.snapshot.a2, BLUE)
        a1_label = self._label(r"\mathbf a_1", plane, self.snapshot.a1, ORANGE, LEFT * 0.38 + UP * 0.32)
        a2_label = self._label(r"\mathbf a_2", plane, self.snapshot.a2, BLUE, RIGHT * 0.42 + UP * 0.22)
        equations = VGroup(
            MathTex(r"A=\begin{bmatrix}1&4\\2&3\end{bmatrix}", font_size=42),
            MathTex(r"A=[\,\mathbf a_1\ \mathbf a_2\,]", font_size=38, color=YELLOW),
            MathTex(r"\mathbf a_1=(1,2),\quad \mathbf a_2=(4,3)", font_size=34),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.35 + UP * 0.10)
        caption = Text(
            "QR begins by orthonormalizing the columns of A.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)
        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(a1_arrow), Create(a2_arrow), FadeIn(a1_label), FadeIn(a2_label), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, a1_arrow, a2_arrow, a1_label, a2_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _orthonormal_columns_card(self) -> None:
        heading = Text("Gram-Schmidt produces the columns of Q", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane(closeup=True)
        radius = np.linalg.norm(plane.c2p(1, 0) - plane.c2p(0, 0))
        unit_circle = Circle(radius=radius, color=GREEN, stroke_width=3).move_to(plane.c2p(0, 0))
        q1_arrow = self._arrow(plane, self.snapshot.q1, ORANGE)
        q2_arrow = self._arrow(plane, self.snapshot.q2, PURPLE)
        q1_label = self._label(r"\mathbf q_1", plane, self.snapshot.q1, ORANGE, LEFT * 0.42 + UP * 0.28)
        q2_label = self._label(r"\mathbf q_2", plane, self.snapshot.q2, PURPLE, RIGHT * 0.44 + DOWN * 0.18)
        right_angle = self._right_angle_marker(plane, np.zeros(2), self.snapshot.q1, self.snapshot.q2)
        equations = VGroup(
            MathTex(r"\mathbf q_1=\frac1{\sqrt5}(1,2)", font_size=37, color=ORANGE),
            MathTex(r"\mathbf q_2=\frac1{\sqrt5}(2,-1)", font_size=37, color=PURPLE),
            MathTex(r"Q=\begin{bmatrix}\vert&\vert\\\mathbf q_1&\mathbf q_2\\\vert&\vert\end{bmatrix}", font_size=39),
            MathTex(self.lesson.Q_ORTHONORMAL, font_size=38, color=GREEN),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 3.35 + UP * 0.08)
        caption = Text(
            "The columns of Q are orthonormal and span the same column space as A.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)
        self.play(FadeIn(heading), Create(plane), Create(unit_circle), run_time=self.TRANSITION_TIME)
        self.play(Create(q1_arrow), Create(q2_arrow), FadeIn(q1_label), FadeIn(q2_label), Create(right_angle), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, unit_circle, q1_arrow, q2_arrow, q1_label, q2_label, right_angle, equations, caption)), run_time=self.TRANSITION_TIME)

    def _first_column_coefficients_card(self) -> None:
        heading = Text("Describe the first column using q1 and q2", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        q1_arrow = self._arrow(plane, self.snapshot.q1, ORANGE, width=4)
        a1_arrow = self._arrow(plane, self.snapshot.a1, BLUE)
        q1_label = self._label(r"\mathbf q_1", plane, self.snapshot.q1, ORANGE, LEFT * 0.44 + UP * 0.28)
        a1_label = self._label(r"\mathbf a_1", plane, self.snapshot.a1, BLUE, LEFT * 0.40 + UP * 0.30)
        equations = VGroup(
            MathTex(r"\mathbf a_1=\sqrt5\,\mathbf q_1+0\,\mathbf q_2", font_size=39, color=YELLOW),
            MathTex(r"[\mathbf a_1]_{\{\mathbf q_1,\mathbf q_2\}}=\begin{bmatrix}\sqrt5\\0\end{bmatrix}", font_size=38),
        ).arrange(DOWN, buff=0.34).move_to(RIGHT * 3.35 + UP * 0.10)
        caption = Text(
            "The first coordinate column of R is already visible.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)
        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(q1_arrow), FadeIn(q1_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(a1_arrow), FadeIn(a1_label), FadeIn(equations[0]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations[1]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, q1_arrow, a1_arrow, q1_label, a1_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _second_column_coefficients_card(self) -> None:
        heading = Text("Describe the second column in the orthonormal basis", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        a2_arrow = self._arrow(plane, self.snapshot.a2, BLUE)
        first_end = self.snapshot.a2_q1_component
        a2_q1 = Arrow(
            plane.c2p(0, 0),
            plane.c2p(*first_end),
            buff=0,
            color=ORANGE,
            stroke_width=6,
        )
        a2_q2 = Arrow(
            plane.c2p(*first_end),
            plane.c2p(*self.snapshot.a2),
            buff=0,
            color=PURPLE,
            stroke_width=6,
        )
        endpoint_guide = DashedLine(
            plane.c2p(*first_end),
            plane.c2p(*self.snapshot.a2),
            color=PURPLE,
            stroke_opacity=0.45,
        )
        a2_label = self._label(r"\mathbf a_2", plane, self.snapshot.a2, BLUE, RIGHT * 0.45 + UP * 0.20)
        comp1_label = MathTex(r"2\sqrt5\,\mathbf q_1", font_size=29, color=ORANGE).move_to(
            plane.c2p(*(0.55 * first_end)) + LEFT * 0.58 + UP * 0.18
        )
        comp2_label = MathTex(r"\sqrt5\,\mathbf q_2", font_size=29, color=PURPLE).move_to(
            0.5 * (plane.c2p(*first_end) + plane.c2p(*self.snapshot.a2)) + RIGHT * 0.70
        )
        equations = VGroup(
            MathTex(r"\mathbf a_2=2\sqrt5\,\mathbf q_1+\sqrt5\,\mathbf q_2", font_size=37, color=YELLOW),
            MathTex(r"[\mathbf a_2]_{\{\mathbf q_1,\mathbf q_2\}}=\begin{bmatrix}2\sqrt5\\\sqrt5\end{bmatrix}", font_size=37),
        ).arrange(DOWN, buff=0.34).move_to(RIGHT * 3.43 + UP * 0.10)
        caption = Text(
            "The second column of R records exactly these two orthonormal coordinates.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)
        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(a2_arrow), FadeIn(a2_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(a2_q1), FadeIn(comp1_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(endpoint_guide), Create(a2_q2), FadeIn(comp2_label), FadeIn(equations[0]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations[1]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, a2_arrow, a2_q1, a2_q2, endpoint_guide, a2_label, comp1_label, comp2_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _assemble_qr_card(self) -> None:
        heading = Text("Put the coordinate columns together", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        matrices = VGroup(
            MathTex(r"A=\begin{bmatrix}1&4\\2&3\end{bmatrix}", font_size=42),
            MathTex(r"Q=\frac1{\sqrt5}\begin{bmatrix}1&2\\2&-1\end{bmatrix}", font_size=42),
            MathTex(r"R=\begin{bmatrix}\sqrt5&2\sqrt5\\0&\sqrt5\end{bmatrix}", font_size=42),
        ).arrange(RIGHT, buff=0.58).move_to(UP * 0.35)
        factorization = MathTex(self.lesson.QR_FACTORIZATION, font_size=54, color=YELLOW).move_to(DOWN * 1.15)
        explanation = Text(
            "R is upper triangular because Gram-Schmidt removes components along earlier directions.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.40)
        self.play(FadeIn(heading), FadeIn(matrices[0]), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(matrices[1]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(matrices[2]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(factorization), FadeIn(explanation), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, matrices, factorization, explanation)), run_time=self.TRANSITION_TIME)

    def _inverse_trick_for_r_card(self) -> None:
        heading = Text("A computational shortcut for R", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left_title = Text("Multiply by the inverse", font_size=24, color=YELLOW).move_to(
            LEFT * 3.15 + UP * 1.55
        )
        derivation = VGroup(
            MathTex(r"A=QR", font_size=38),
            MathTex(r"Q^{-1}A=Q^{-1}QR", font_size=36),
            MathTex(r"Q^{-1}A=R", font_size=38, color=YELLOW),
            MathTex(self.lesson.Q_INVERSE_TRANSPOSE, font_size=38, color=GREEN),
            MathTex(self.lesson.R_FROM_QA, font_size=40, color=YELLOW),
        ).arrange(DOWN, buff=0.24).move_to(LEFT * 3.05 + DOWN * 0.20)

        right_title = Text("For our Q", font_size=24, color=YELLOW).move_to(
            RIGHT * 3.10 + UP * 1.78
        )
        computation = VGroup(
            MathTex(
                r"R=Q^TA",
                font_size=37,
            ),
            MathTex(
                r"=\frac1{\sqrt5}"
                r"\begin{bmatrix}1&2\\2&-1\end{bmatrix}"
                r"\begin{bmatrix}1&4\\2&3\end{bmatrix}",
                font_size=32,
            ),
            MathTex(
                r"=\frac1{\sqrt5}"
                r"\begin{bmatrix}5&10\\0&5\end{bmatrix}",
                font_size=35,
            ),
            MathTex(
                r"=\begin{bmatrix}\sqrt5&2\sqrt5\\0&\sqrt5\end{bmatrix}",
                font_size=38,
                color=GREEN,
            ),
        ).arrange(DOWN, buff=0.27).move_to(RIGHT * 3.05 + DOWN * 0.42)
        divider = Line(UP * 1.55, DOWN * 2.15, color=GREY_B, stroke_opacity=0.45)
        caption = Text(
            "Because this Q is square and orthogonal, its inverse is its transpose.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), FadeIn(left_title), FadeIn(derivation[0]), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(derivation[1]), FadeIn(derivation[2]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(derivation[3]), FadeIn(derivation[4]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(divider), FadeIn(right_title), FadeIn(computation[0]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(computation[1]), FadeIn(computation[2]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(computation[3]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, left_title, derivation, divider, right_title, computation, caption)),
            run_time=self.TRANSITION_TIME,
        )

    def _why_qr_helps_card(self) -> None:
        heading = Text("Why QR is useful", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        properties = VGroup(
            MathTex(self.lesson.Q_ORTHONORMAL, font_size=40, color=GREEN),
            MathTex(self.lesson.R_FROM_QA, font_size=40),
            MathTex(r"A\mathbf x=\mathbf b", font_size=39),
            MathTex(r"QR\mathbf x=\mathbf b", font_size=39),
            MathTex(r"R\mathbf x=Q^T\mathbf b", font_size=43, color=YELLOW),
        ).arrange(DOWN, buff=0.27).move_to(DOWN * 0.02)
        bridge = Text(self.lesson.bridge_prompt, font_size=27, color=YELLOW).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(heading), FadeIn(properties[0]), FadeIn(properties[1]), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(properties[2]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(properties[3]), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(properties[4]), FadeIn(bridge), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
