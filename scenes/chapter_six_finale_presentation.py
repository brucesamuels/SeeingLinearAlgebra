"""CP165: Chapter 6 finale -- orthogonality and projection."""

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
)

from engine.chapter_six_finale import ChapterSixFinaleLesson


class ChapterSixFinalePresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Orthogonality and Projection: The Big Picture"
    SCENE_REVISION = "cp165_r2_center_matrix_families_heading"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.10
    HOLD_TIME = 2.35

    def construct(self) -> None:
        self.lesson = ChapterSixFinaleLesson()
        self.snapshot = self.lesson.snapshot()
        self.banner, self.lesson_title_mobject = self._header()
        self.add(self.banner, self.lesson_title_mobject)

        self._perpendicularity_card()
        self._projection_decomposition_card()
        self._orthonormal_coordinates_card()
        self._gram_schmidt_qr_card()
        self._least_squares_card()
        self._two_matrix_families_card()
        self._recognition_card()
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
    def _plane(
        center=LEFT * 3.15 + DOWN * 0.50,
        *,
        width: float = 5.20,
        height: float = 5.20,
        x_range=(-2.0, 5.0, 1.0),
        y_range=(-2.5, 4.5, 1.0),
    ) -> NumberPlane:
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
    def _segment(
        plane: NumberPlane,
        start: np.ndarray,
        end: np.ndarray,
        color,
        *,
        width: float = 5,
    ) -> Arrow:
        return Arrow(
            plane.c2p(*start),
            plane.c2p(*end),
            buff=0,
            color=color,
            stroke_width=width,
        )

    @staticmethod
    def _label(text: str, plane: NumberPlane, point: np.ndarray, color, offset) -> MathTex:
        return MathTex(text, font_size=29, color=color).move_to(plane.c2p(*point) + offset)

    @staticmethod
    def _right_math(*mobjects) -> VGroup:
        return VGroup(*mobjects).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.25 + DOWN * 0.10)

    @staticmethod
    def _right_angle_marker(
        plane: NumberPlane,
        vertex: np.ndarray,
        direction_one: np.ndarray,
        direction_two: np.ndarray,
        *,
        size: float = 0.30,
    ) -> VGroup:
        d1 = direction_one / np.linalg.norm(direction_one)
        d2 = direction_two / np.linalg.norm(direction_two)
        p1 = vertex + size * d1
        p2 = vertex + size * (d1 + d2)
        p3 = vertex + size * d2
        return VGroup(
            Line(plane.c2p(*p1), plane.c2p(*p2), color=WHITE, stroke_width=2.6),
            Line(plane.c2p(*p2), plane.c2p(*p3), color=WHITE, stroke_width=2.6),
        )

    def _perpendicularity_card(self) -> None:
        heading = Text("Perpendicular geometry becomes a zero dot product", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane(x_range=(-2.5, 3.5, 1.0), y_range=(-2.5, 3.5, 1.0))
        u_arrow = self._arrow(plane, self.snapshot.u, ORANGE)
        v_arrow = self._arrow(plane, self.snapshot.v, BLUE)
        u_label = self._label(r"\mathbf u", plane, self.snapshot.u, ORANGE, LEFT * 0.34 + UP * 0.12)
        v_label = self._label(r"\mathbf v", plane, self.snapshot.v, BLUE, RIGHT * 0.30 + DOWN * 0.16)
        marker = self._right_angle_marker(
            plane,
            np.zeros(2),
            self.snapshot.u,
            self.snapshot.v,
            size=0.38,
        )
        equations = self._right_math(
            MathTex(r"\mathbf u=\begin{bmatrix}1\\2\end{bmatrix}", font_size=36, color=ORANGE),
            MathTex(r"\mathbf v=\begin{bmatrix}2\\-1\end{bmatrix}", font_size=36, color=BLUE),
            MathTex(r"\mathbf u^T\mathbf v=2-2=0", font_size=38, color=GREEN),
            MathTex(self.lesson.DOT_RULE, font_size=36, color=YELLOW),
        )
        caption = Text(
            "This is the basic translation used throughout the chapter: a geometric right angle becomes an algebraic zero.",
            font_size=20,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(u_arrow), FadeIn(u_label), Create(v_arrow), FadeIn(v_label), Create(marker), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, u_arrow, v_arrow, u_label, v_label, marker, equations, caption)), run_time=self.TRANSITION_TIME)

    def _projection_decomposition_card(self) -> None:
        heading = Text("Projection turns orthogonality into a decomposition", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        q_direction = self.snapshot.q
        line = Line(plane.c2p(*(-2.2 * q_direction)), plane.c2p(*(4.3 * q_direction)), color=TEAL, stroke_width=4)
        sample_arrow = self._arrow(plane, self.snapshot.sample, BLUE)
        projection_arrow = self._arrow(plane, self.snapshot.projection, ORANGE)
        residual_arrow = self._segment(plane, self.snapshot.projection, self.snapshot.sample, PURPLE)
        sample_label = self._label(r"\mathbf v", plane, self.snapshot.sample, BLUE, RIGHT * 0.28 + UP * 0.10)
        projection_label = self._label(r"P\mathbf v", plane, self.snapshot.projection, ORANGE, LEFT * 0.50 + UP * 0.08)
        residual_label = MathTex(r"\mathbf r", font_size=29, color=PURPLE).move_to(
            plane.c2p(*(0.5 * (self.snapshot.projection + self.snapshot.sample))) + RIGHT * 0.38
        )
        marker = self._right_angle_marker(
            plane,
            self.snapshot.projection,
            q_direction,
            self.snapshot.residual,
            size=0.32,
        )
        equations = self._right_math(
            MathTex(self.lesson.DECOMPOSITION_RULE, font_size=36, color=YELLOW),
            MathTex(r"P\mathbf v\in W", font_size=38, color=ORANGE),
            MathTex(r"\mathbf r\in W^\perp", font_size=38, color=PURPLE),
            MathTex(r"P=QQ^T", font_size=42, color=GREEN),
        )
        caption = Text(
            "Every vector separates into a part inside the subspace and a perpendicular residual.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), Create(line), run_time=self.TRANSITION_TIME)
        self.play(Create(sample_arrow), FadeIn(sample_label), run_time=self.EMPHASIS_TIME)
        self.play(TransformFromCopy(sample_arrow, projection_arrow), Create(residual_arrow), FadeIn(projection_label), FadeIn(residual_label), Create(marker), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, line, sample_arrow, projection_arrow, residual_arrow, sample_label, projection_label, residual_label, marker, equations, caption)), run_time=self.TRANSITION_TIME)

    def _orthonormal_coordinates_card(self) -> None:
        heading = Text("Orthonormal coordinates make projection simple", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane(x_range=(-2.5, 3.5, 1.0), y_range=(-2.5, 3.5, 1.0))
        q1 = np.array([1.0, 2.0]) / np.sqrt(5.0)
        q2 = np.array([2.0, -1.0]) / np.sqrt(5.0)
        q1_arrow = self._arrow(plane, 2.0 * q1, ORANGE)
        q2_arrow = self._arrow(plane, 2.0 * q2, PURPLE)
        q1_label = self._label(r"\mathbf q_1", plane, 2.0 * q1, ORANGE, LEFT * 0.40 + UP * 0.08)
        q2_label = self._label(r"\mathbf q_2", plane, 2.0 * q2, PURPLE, RIGHT * 0.36 + DOWN * 0.08)
        marker = self._right_angle_marker(plane, np.zeros(2), q1, q2, size=0.40)
        equations = self._right_math(
            MathTex(r"Q=[\mathbf q_1\ \mathbf q_2]", font_size=38),
            MathTex(r"Q^TQ=I", font_size=42, color=GREEN),
            MathTex(r"\mathbf c=Q^T\mathbf v", font_size=40, color=BLUE),
            MathTex(r"P\mathbf v=Q\mathbf c=QQ^T\mathbf v", font_size=38, color=YELLOW),
        )
        caption = Text(
            "With an orthonormal basis, dot products read off coordinates and reconstruction uses the same basis vectors.",
            font_size=20,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), run_time=self.TRANSITION_TIME)
        self.play(Create(q1_arrow), Create(q2_arrow), FadeIn(q1_label), FadeIn(q2_label), Create(marker), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, q1_arrow, q2_arrow, q1_label, q2_label, marker, equations, caption)), run_time=self.TRANSITION_TIME)

    def _gram_schmidt_qr_card(self) -> None:
        heading = Text("Gram-Schmidt turns independent directions into an orthonormal basis", font_size=26, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left_box = Rectangle(width=3.25, height=2.25, color=GREY_B, stroke_opacity=0.55).move_to(LEFT * 4.25 + DOWN * 0.25)
        middle_box = Rectangle(width=3.25, height=2.25, color=GREY_B, stroke_opacity=0.55).move_to(DOWN * 0.25)
        right_box = Rectangle(width=3.25, height=2.25, color=GREY_B, stroke_opacity=0.55).move_to(RIGHT * 4.25 + DOWN * 0.25)
        left_content = VGroup(
            Text("independent columns", font_size=24, color=WHITE),
            MathTex(r"A=[\mathbf v_1\ \cdots\ \mathbf v_k]", font_size=32, color=BLUE),
        ).arrange(DOWN, buff=0.28).move_to(left_box)
        middle_content = VGroup(
            Text("Gram-Schmidt", font_size=26, color=YELLOW),
            Text("subtract projections", font_size=21, color=GREY_B),
            Text("then normalize", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.22).move_to(middle_box)
        right_content = VGroup(
            Text("orthonormal columns", font_size=24, color=WHITE),
            MathTex(r"Q^TQ=I", font_size=37, color=GREEN),
        ).arrange(DOWN, buff=0.28).move_to(right_box)
        arrow_one = Arrow(left_box.get_right(), middle_box.get_left(), buff=0.18, color=GREY_B)
        arrow_two = Arrow(middle_box.get_right(), right_box.get_left(), buff=0.18, color=GREY_B)
        factorization = MathTex(self.lesson.QR_RULE, font_size=45, color=ORANGE).move_to(DOWN * 2.25)
        caption = Text(
            "QR records the original matrix using orthonormal directions Q and the coefficients collected in R.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_box), Create(middle_box), Create(right_box), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(left_content), Create(arrow_one), FadeIn(middle_content), Create(arrow_two), FadeIn(right_content), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(factorization), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, left_box, middle_box, right_box, left_content, middle_content, right_content, arrow_one, arrow_two, factorization, caption)), run_time=self.TRANSITION_TIME)

    def _least_squares_card(self) -> None:
        heading = Text("Least squares is projection onto the column space", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left_box = Rectangle(width=5.10, height=4.30, color=GREY_B, stroke_opacity=0.55).move_to(LEFT * 3.20 + DOWN * 0.42)
        right_box = Rectangle(width=5.10, height=4.30, color=GREY_B, stroke_opacity=0.55).move_to(RIGHT * 3.20 + DOWN * 0.42)
        left_title = Text("Geometry", font_size=26, color=TEAL).next_to(left_box, UP, buff=0.14)
        right_title = Text("Algebra", font_size=26, color=YELLOW).next_to(right_box, UP, buff=0.14)
        left_content = VGroup(
            MathTex(r"\mathbf b=A\hat{\mathbf x}+\mathbf r", font_size=36),
            MathTex(r"A\hat{\mathbf x}\in\operatorname{Col}(A)", font_size=33, color=ORANGE),
            MathTex(r"\mathbf r\perp\operatorname{Col}(A)", font_size=33, color=PURPLE),
            Text("choose the closest vector", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.24).move_to(left_box)
        right_content = VGroup(
            MathTex(self.lesson.LEAST_SQUARES_RULE, font_size=33, color=GREEN),
            MathTex(self.lesson.NORMAL_EQUATION, font_size=34, color=YELLOW),
            Text("or, after A = QR", font_size=22, color=GREY_B),
            MathTex(self.lesson.QR_LEAST_SQUARES, font_size=36, color=ORANGE),
        ).arrange(DOWN, buff=0.24).move_to(right_box)
        caption = Text(
            "The normal equation and the QR route are two algebraic expressions of the same perpendicular-residual condition.",
            font_size=20,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_box), Create(right_box), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(left_content), FadeIn(right_content), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, left_box, right_box, left_title, right_title, left_content, right_content, caption)), run_time=self.TRANSITION_TIME)

    def _two_matrix_families_card(self) -> None:
        left_box = Rectangle(width=5.25, height=4.55, color=GREY_B, stroke_opacity=0.55).move_to(LEFT * 3.25 + DOWN * 0.45)
        right_box = Rectangle(width=5.25, height=4.55, color=GREY_B, stroke_opacity=0.55).move_to(RIGHT * 3.25 + DOWN * 0.45)
        left_title = Text("Projection matrix P", font_size=27, color=ORANGE).next_to(left_box, UP, buff=0.14)
        right_title = Text("Square orthogonal matrix U", font_size=27, color=GREEN).next_to(right_box, UP, buff=0.14)
        title_band = VGroup(left_title, right_title)
        heading_mid_y = 0.5 * (self.lesson_title_mobject.get_bottom()[1] + title_band.get_top()[1])
        heading = Text(
            "Orthogonality appears in two different matrix families",
            font_size=27,
            color=WHITE,
        ).move_to(np.array([0.0, heading_mid_y, 0.0]))
        left_content = VGroup(
            MathTex(self.lesson.PROJECTION_SIGNATURE, font_size=35, color=YELLOW),
            Text("projects onto a subspace", font_size=23, color=WHITE),
            Text("can shorten vectors", font_size=22, color=GREY_B),
            Text("can collapse dimension", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.30).move_to(left_box)
        right_content = VGroup(
            MathTex(self.lesson.ORTHOGONAL_SIGNATURE, font_size=34, color=YELLOW),
            Text("rotates or reflects", font_size=23, color=WHITE),
            Text("preserves lengths and angles", font_size=22, color=GREY_B),
            Text("does not collapse dimension", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.30).move_to(right_box)
        caption = Text(
            "The word orthogonal links them, but their algebraic signatures tell you which geometry is happening.",
            font_size=20,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_box), Create(right_box), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(left_content), FadeIn(right_content), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, left_box, right_box, left_title, right_title, left_content, right_content, caption)), run_time=self.TRANSITION_TIME)

    def _recognition_card(self) -> None:
        heading = Text("What should you recognize when you see these formulas?", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        cards = VGroup()
        specs = (
            (r"\mathbf u^T\mathbf v=0", "perpendicular vectors", ORANGE),
            (r"Q^TQ=I", "orthonormal columns", GREEN),
            (r"P^T=P,\ P^2=P", "orthogonal projection", YELLOW),
            (r"A^T(\mathbf b-A\hat{\mathbf x})=0", "least-squares residual", PURPLE),
        )
        centers = (LEFT * 3.25 + UP * 0.65, RIGHT * 3.25 + UP * 0.65, LEFT * 3.25 + DOWN * 1.55, RIGHT * 3.25 + DOWN * 1.55)
        for (formula, meaning, color), center in zip(specs, centers):
            box = Rectangle(width=5.35, height=1.70, color=GREY_B, stroke_opacity=0.55).move_to(center)
            formula_mob = MathTex(formula, font_size=33, color=color).move_to(center + UP * 0.28)
            meaning_mob = Text(meaning, font_size=22, color=WHITE).move_to(center + DOWN * 0.40)
            cards.add(VGroup(box, formula_mob, meaning_mob))
        caption = Text(
            "Each equation is a compact signal for a geometric relationship developed in this chapter.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.30)

        self.play(FadeIn(heading), run_time=self.TRANSITION_TIME)
        for card in cards:
            self.play(Create(card[0]), FadeIn(card[1]), FadeIn(card[2]), run_time=0.65)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, cards, caption)), run_time=self.TRANSITION_TIME)

    def _closing_card(self) -> None:
        prompt = Text("The chapter in one sentence", font_size=28, color=GREY_B).move_to(UP * 1.65)
        statement = Text(
            self.lesson.CLOSING_IDEA,
            font_size=42,
            color=YELLOW,
        ).move_to(UP * 0.35)
        frame = SurroundingRectangle(statement, color=GREY_B, buff=0.30)
        chain = VGroup(
            Text("perpendicularity", font_size=24, color=ORANGE),
            MathTex(r"\longrightarrow", font_size=32, color=GREY_B),
            Text("projection", font_size=24, color=TEAL),
            MathTex(r"\longrightarrow", font_size=32, color=GREY_B),
            Text("orthonormal bases", font_size=24, color=GREEN),
            MathTex(r"\longrightarrow", font_size=32, color=GREY_B),
            Text("QR and least squares", font_size=24, color=PURPLE),
        ).arrange(RIGHT, buff=0.24).move_to(DOWN * 1.35)
        if chain.width > 11.8:
            chain.scale_to_fit_width(11.8)
        closing = Text(
            "Geometry tells us what is true; orthogonality gives us an efficient way to compute it.",
            font_size=21,
            color=WHITE,
        ).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(prompt), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(statement), Create(frame), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(chain), FadeIn(closing), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME + 1.0)
        self.play(FadeOut(VGroup(prompt, statement, frame, chain, closing)), run_time=self.TRANSITION_TIME)
