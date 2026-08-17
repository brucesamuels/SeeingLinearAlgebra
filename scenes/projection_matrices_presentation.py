"""CP164: projection matrices -- symmetric and idempotent."""

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
    PURPLE,
    Rectangle,
    RIGHT,
    Scene,
    TEAL,
    Text,
    TransformFromCopy,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.projection_matrices import ProjectionMatricesLesson


class ProjectionMatricesPresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Projection Matrices: Symmetric and Idempotent"
    SCENE_REVISION = "cp164_r2_general_to_orthonormal_projection"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.10
    HOLD_TIME = 2.35

    def construct(self) -> None:
        self.lesson = ProjectionMatricesLesson()
        self.snapshot = self.lesson.snapshot()
        self.banner, self.lesson_title_mobject = self._header()
        self.add(self.banner, self.lesson_title_mobject)

        self._from_basis_to_matrix_card()
        self._general_to_orthonormal_card()
        self._geometry_of_projection_card()
        self._idempotent_card()
        self._symmetric_card()
        self._concrete_example_card()
        self._subspace_complement_card()
        self._projection_vs_orthogonal_card()

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
        center=LEFT * 3.15 + DOWN * 0.52,
        *,
        width: float = 5.35,
        height: float = 5.35,
        x_range=(-1.5, 5.0, 1.0),
        y_range=(-2.0, 4.5, 1.0),
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
    def _segment(plane: NumberPlane, start: np.ndarray, end: np.ndarray, color, *, width: float = 5) -> Arrow:
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
        return VGroup(*mobjects).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.30 + DOWN * 0.10)

    @staticmethod
    def _right_angle_marker(
        plane: NumberPlane,
        vertex: np.ndarray,
        direction_one: np.ndarray,
        direction_two: np.ndarray,
        *,
        size: float = 0.28,
    ) -> VGroup:
        d1 = direction_one / np.linalg.norm(direction_one)
        d2 = direction_two / np.linalg.norm(direction_two)
        p0 = vertex
        p1 = vertex + size * d1
        p2 = vertex + size * (d1 + d2)
        p3 = vertex + size * d2
        return VGroup(
            Line(plane.c2p(*p1), plane.c2p(*p2), color=WHITE, stroke_width=2.6),
            Line(plane.c2p(*p2), plane.c2p(*p3), color=WHITE, stroke_width=2.6),
        )

    def _from_basis_to_matrix_card(self) -> None:
        heading = Text("An orthonormal basis gives the projection matrix", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        q_line = Line(plane.c2p(-0.75, -1.5), plane.c2p(2.1, 4.2), color=TEAL, stroke_width=4)
        q_arrow = self._arrow(plane, self.snapshot.q * 2.0, ORANGE)
        q_label = self._label(r"\mathbf q", plane, self.snapshot.q * 2.0, ORANGE, RIGHT * 0.28 + UP * 0.10)
        line_label = Text("W = span(q)", font_size=22, color=TEAL).move_to(plane.c2p(1.65, 2.55) + RIGHT * 0.45)
        equations = self._right_math(
            MathTex(r"Q=[\mathbf q_1\ \cdots\ \mathbf q_k]", font_size=36),
            MathTex(r"Q^TQ=I", font_size=39, color=GREEN),
            MathTex(self.lesson.GENERAL_PROJECTION, font_size=44, color=YELLOW),
            MathTex(self.lesson.GENERAL_ACTION, font_size=39, color=WHITE),
        )
        caption = Text(
            "Q^T measures the coordinates in the orthonormal basis; Q rebuilds the vector inside the subspace.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), Create(q_line), run_time=self.TRANSITION_TIME)
        self.play(Create(q_arrow), FadeIn(q_label), FadeIn(line_label), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, q_line, q_arrow, q_label, line_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _general_to_orthonormal_card(self) -> None:
        heading = Text("From the general projection formula to QQ^T", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        general_label = Text("General full-rank basis", font_size=24, color=GREY_B).move_to(UP * 1.55)
        general_formula = MathTex(
            self.lesson.FULL_COLUMN_PROJECTION,
            font_size=45,
            color=WHITE,
        ).next_to(general_label, DOWN, buff=0.24)

        orthonormal_label = Text("Choose an orthonormal basis Q", font_size=24, color=YELLOW).next_to(
            general_formula, DOWN, buff=0.48
        )
        derivation = VGroup(
            MathTex(r"P=Q(Q^TQ)^{-1}Q^T", font_size=43),
            MathTex(r"Q^TQ=I", font_size=41, color=GREEN),
            MathTex(r"P=QI^{-1}Q^T", font_size=43),
            MathTex(r"P=QQ^T", font_size=48, color=YELLOW),
        ).arrange(DOWN, buff=0.24).next_to(orthonormal_label, DOWN, buff=0.25)

        caption = Text(
            "Orthonormal columns make the Gram matrix Q^TQ equal to the identity, so the inverse disappears.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), FadeIn(general_label), FadeIn(general_formula), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(orthonormal_label), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(derivation), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, general_label, general_formula, orthonormal_label, derivation, caption)),
            run_time=self.TRANSITION_TIME,
        )

    def _geometry_of_projection_card(self) -> None:
        heading = Text("Projection chooses the closest vector in the subspace", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        q_line = Line(plane.c2p(-0.75, -1.5), plane.c2p(2.1, 4.2), color=TEAL, stroke_width=4)
        v_arrow = self._arrow(plane, self.snapshot.v, BLUE)
        p_arrow = self._arrow(plane, self.snapshot.Pv, ORANGE)
        residual = self._segment(plane, self.snapshot.Pv, self.snapshot.v, PURPLE, width=5)
        v_label = self._label(r"\mathbf v", plane, self.snapshot.v, BLUE, RIGHT * 0.28 + UP * 0.16)
        p_label = self._label(r"P\mathbf v", plane, self.snapshot.Pv, ORANGE, LEFT * 0.42 + UP * 0.18)
        r_label = self._label(r"\mathbf r", plane, (self.snapshot.v + self.snapshot.Pv) / 2, PURPLE, RIGHT * 0.34)
        marker = self._right_angle_marker(
            plane,
            self.snapshot.Pv,
            self.snapshot.q,
            self.snapshot.residual,
        )
        equations = self._right_math(
            MathTex(r"\mathbf v=P\mathbf v+\mathbf r", font_size=39),
            MathTex(r"P\mathbf v\in W", font_size=38, color=ORANGE),
            MathTex(r"\mathbf r\perp W", font_size=38, color=PURPLE),
        )
        caption = Text(
            "The residual points in the perpendicular direction, so Pv is the closest point in W.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), Create(q_line), run_time=self.TRANSITION_TIME)
        self.play(Create(v_arrow), FadeIn(v_label), run_time=self.EMPHASIS_TIME)
        self.play(TransformFromCopy(v_arrow, p_arrow), Create(residual), FadeIn(p_label), FadeIn(r_label), Create(marker), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, q_line, v_arrow, p_arrow, residual, v_label, p_label, r_label, marker, equations, caption)), run_time=self.TRANSITION_TIME)

    def _idempotent_card(self) -> None:
        heading = Text("Project twice and nothing changes", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane()
        q_line = Line(plane.c2p(-0.75, -1.5), plane.c2p(2.1, 4.2), color=TEAL, stroke_width=4)
        v_arrow = self._arrow(plane, self.snapshot.v, BLUE)
        p_arrow = self._arrow(plane, self.snapshot.Pv, ORANGE)
        second_arrow = self._arrow(plane, self.snapshot.repeated_projection, GREEN, width=4)
        p_label = self._label(r"P\mathbf v", plane, self.snapshot.Pv, ORANGE, LEFT * 0.42 + UP * 0.18)
        equations = self._right_math(
            MathTex(r"P(P\mathbf v)=P\mathbf v", font_size=41, color=GREEN),
            MathTex(self.lesson.IDEMPOTENT_RULE, font_size=48, color=YELLOW),
            Text("Once a vector is in W, projecting again leaves it fixed.", font_size=22, color=GREY_B),
        )
        caption = Text(
            "Idempotent means repeated application has the same effect as applying the map once.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), Create(q_line), Create(v_arrow), run_time=self.TRANSITION_TIME)
        self.play(TransformFromCopy(v_arrow, p_arrow), FadeIn(p_label), run_time=self.EMPHASIS_TIME)
        self.play(TransformFromCopy(p_arrow, second_arrow), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, q_line, v_arrow, p_arrow, second_arrow, p_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _symmetric_card(self) -> None:
        heading = Text("Projection matrices onto subspaces are symmetric", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        derivation = VGroup(
            MathTex(r"P=QQ^T", font_size=50, color=YELLOW),
            MathTex(r"P^T=(QQ^T)^T", font_size=43),
            MathTex(r"\phantom{P^T}=QQ^T", font_size=43),
            MathTex(self.lesson.SYMMETRY_RULE, font_size=50, color=GREEN),
        ).arrange(DOWN, buff=0.30).move_to(LEFT * 2.65 + DOWN * 0.15)
        meaning_box = Rectangle(width=5.35, height=3.25, color=GREY_B, stroke_opacity=0.55).move_to(RIGHT * 3.20 + DOWN * 0.10)
        meaning = VGroup(
            Text("Symmetry is built into", font_size=24, color=WHITE),
            MathTex(r"QQ^T", font_size=45, color=YELLOW),
            Text("because transposing reverses", font_size=22, color=GREY_B),
            Text("the factors and returns the same product.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.20).move_to(meaning_box)
        caption = Text(
            "For an orthogonal projection, symmetry and idempotence are the two defining algebraic signatures.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), FadeIn(derivation), Create(meaning_box), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(meaning), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, derivation, meaning_box, meaning, caption)), run_time=self.TRANSITION_TIME)

    def _concrete_example_card(self) -> None:
        heading = Text("A concrete projection matrix", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left_box = Rectangle(width=5.75, height=4.55, color=GREY_B, stroke_opacity=0.55).move_to(LEFT * 3.10 + DOWN * 0.45)
        right_box = Rectangle(width=5.75, height=4.55, color=GREY_B, stroke_opacity=0.55).move_to(RIGHT * 3.10 + DOWN * 0.45)
        left_title = Text("Build P", font_size=26, color=GREEN).next_to(left_box, UP, buff=0.14)
        right_title = Text("Apply P", font_size=26, color=YELLOW).next_to(right_box, UP, buff=0.14)
        left_math = VGroup(
            MathTex(r"\mathbf q=\frac1{\sqrt5}\begin{bmatrix}1\\2\end{bmatrix}", font_size=34, color=ORANGE),
            MathTex(r"P=\mathbf q\mathbf q^T", font_size=34),
            MathTex(r"P=\frac15\begin{bmatrix}1&2\\2&4\end{bmatrix}", font_size=38, color=YELLOW),
        ).arrange(DOWN, buff=0.28).move_to(left_box)
        right_math = VGroup(
            MathTex(r"\mathbf v=\begin{bmatrix}4\\1\end{bmatrix}", font_size=34, color=BLUE),
            MathTex(r"P\mathbf v=\frac15\begin{bmatrix}6\\12\end{bmatrix}", font_size=34),
            MathTex(r"P\mathbf v=\begin{bmatrix}6/5\\12/5\end{bmatrix}", font_size=36, color=ORANGE),
            MathTex(r"\mathbf r=\begin{bmatrix}14/5\\-7/5\end{bmatrix}", font_size=32, color=PURPLE),
        ).arrange(DOWN, buff=0.22).move_to(right_box)
        caption = Text(
            "The projected vector lies on span(1,2), and the residual is perpendicular to that line.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_box), Create(right_box), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(left_math), FadeIn(right_math), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, left_box, right_box, left_title, right_title, left_math, right_math, caption)), run_time=self.TRANSITION_TIME)

    def _subspace_complement_card(self) -> None:
        heading = Text("P keeps the subspace and kills its orthogonal complement", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._plane(center=LEFT * 3.10 + DOWN * 0.56, x_range=(-3.0, 3.0, 1.0), y_range=(-3.0, 3.0, 1.0))
        q_line = Line(plane.c2p(-1.3, -2.6), plane.c2p(1.3, 2.6), color=TEAL, stroke_width=4)
        perp_line = Line(plane.c2p(-2.6, 1.3), plane.c2p(2.6, -1.3), color=PURPLE, stroke_width=3)
        q_arrow = self._arrow(plane, self.snapshot.q * 2.0, ORANGE)
        n_arrow = self._arrow(plane, self.snapshot.orthogonal_direction * 2.0, PURPLE)
        q_label = self._label(r"\mathbf q", plane, self.snapshot.q * 2.0, ORANGE, RIGHT * 0.24)
        n_label = self._label(r"\mathbf n", plane, self.snapshot.orthogonal_direction * 2.0, PURPLE, RIGHT * 0.26 + DOWN * 0.10)
        equations = self._right_math(
            MathTex(r"P\mathbf q=\mathbf q", font_size=42, color=ORANGE),
            MathTex(r"P\mathbf n=\mathbf 0", font_size=42, color=PURPLE),
            MathTex(r"\operatorname{range}(P)=W", font_size=37),
            MathTex(r"\operatorname{null}(P)=W^\perp", font_size=37),
        )
        caption = Text(
            "Along W, P acts like the identity; along W-perp, P collapses everything to zero.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(plane), Create(q_line), Create(perp_line), run_time=self.TRANSITION_TIME)
        self.play(Create(q_arrow), Create(n_arrow), FadeIn(q_label), FadeIn(n_label), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, plane, q_line, perp_line, q_arrow, n_arrow, q_label, n_label, equations, caption)), run_time=self.TRANSITION_TIME)

    def _projection_vs_orthogonal_card(self) -> None:
        left_box = Rectangle(width=5.6, height=4.65, color=GREY_B, stroke_opacity=0.55).move_to(LEFT * 3.10 + DOWN * 0.48)
        right_box = Rectangle(width=5.6, height=4.65, color=GREY_B, stroke_opacity=0.55).move_to(RIGHT * 3.10 + DOWN * 0.48)
        left_title = Text("Projection P", font_size=26, color=YELLOW).next_to(left_box, UP, buff=0.14)
        right_title = Text("Orthogonal Q", font_size=26, color=GREEN).next_to(right_box, UP, buff=0.14)
        title_band = VGroup(left_title, right_title)
        comparison_mid_y = 0.5 * (self.lesson_title_mobject.get_bottom()[1] + title_band.get_top()[1])
        heading = Text(
            "Projection matrix versus orthogonal matrix",
            font_size=27,
            color=WHITE,
        ).move_to(np.array([0.0, comparison_mid_y, 0.0]))
        left_math = VGroup(
            MathTex(self.lesson.IDEMPOTENT_RULE, font_size=44, color=YELLOW),
            MathTex(self.lesson.SYMMETRY_RULE, font_size=39),
            Text("moves vectors toward a subspace", font_size=22, color=WHITE),
            Text("may shorten vectors", font_size=22, color=GREY_B),
            Text("usually loses a dimension", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.24).move_to(left_box)
        right_math = VGroup(
            MathTex(self.lesson.ORTHOGONAL_MATRIX_RULE, font_size=44, color=GREEN),
            MathTex(r"Q^{-1}=Q^T", font_size=39),
            Text("rotates or reflects", font_size=22, color=WHITE),
            Text("preserves lengths and angles", font_size=22, color=GREY_B),
            Text("does not collapse dimension", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.24).move_to(right_box)
        conclusion = Text(
            self.lesson.CLOSING_IDEA,
            font_size=22,
            color=WHITE,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading), Create(left_box), Create(right_box), FadeIn(left_title), FadeIn(right_title), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(left_math), FadeIn(right_math), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(conclusion), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME + 0.4)
        self.play(FadeOut(VGroup(heading, left_box, right_box, left_title, right_title, left_math, right_math, conclusion)), run_time=self.TRANSITION_TIME)
