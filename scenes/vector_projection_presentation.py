"""CP153: Projection onto a Vector."""

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
    Line,
    LEFT,
    MathTex,
    ORANGE,
    Rectangle,
    RIGHT,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    Axes,
    Scene,
)

from engine.vector_projection import ProjectionSnapshot, VectorProjectionLesson


class VectorProjectionPresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Projection onto a Vector"
    SCENE_REVISION = "cp153_r2_left_import_hotfix"
    TRANSITION_TIME = 1.35
    EMPHASIS_TIME = 1.15
    HOLD_TIME = 2.6
    LONG_HOLD_TIME = 3.0

    def construct(self) -> None:
        self.lesson = VectorProjectionLesson()
        self.snapshot = self.lesson.example()
        banner, lesson_title = self._header()
        self.lesson_title_mobject = lesson_title
        self.add(banner, lesson_title)

        self._geometric_question_card()
        self._perpendicular_drop_card()
        self._derive_coefficient_card()
        self._formula_card()
        self._worked_example_card()
        self._orthogonal_residual_card()

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
        return VGroup(banner_box, banner_text), lesson_title

    def _geometry_axes(self, *, shift=DOWN * 0.55) -> Axes:
        return Axes(
            x_range=(-0.5, 5.2, 1),
            y_range=(-0.5, 4.2, 1),
            x_length=6.2,
            y_length=5.1,
            axis_config={"color": GREY_B, "stroke_width": 2.0, "include_ticks": False},
            tips=False,
        ).shift(shift)

    def _arrow(self, axes: Axes, end: np.ndarray, color: str) -> Arrow:
        return Arrow(
            axes.c2p(0, 0),
            axes.c2p(*end),
            buff=0,
            color=color,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.12,
        )

    def _span_line(self, axes: Axes, direction: np.ndarray) -> Line:
        unit = direction / np.linalg.norm(direction)
        return Line(
            axes.c2p(*(-0.45 * unit)),
            axes.c2p(*(5.0 * unit)),
            color=BLUE,
            stroke_opacity=0.55,
            stroke_width=4,
        )

    def _right_angle_marker(self, axes: Axes, snapshot: ProjectionSnapshot) -> VGroup:
        u_hat = snapshot.direction / np.linalg.norm(snapshot.direction)
        r_hat = snapshot.residual / np.linalg.norm(snapshot.residual)
        corner = snapshot.projection
        size = 0.26
        a = corner + size * u_hat
        b = a + size * r_hat
        c = corner + size * r_hat
        return VGroup(
            Line(axes.c2p(*corner), axes.c2p(*a), color=WHITE, stroke_width=3),
            Line(axes.c2p(*a), axes.c2p(*b), color=WHITE, stroke_width=3),
            Line(axes.c2p(*b), axes.c2p(*c), color=WHITE, stroke_width=3),
        )

    def _geometric_question_card(self) -> None:
        heading = Text("A geometric question", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        question = Text(
            "What part of x points in the direction of u?",
            font_size=31,
            color=YELLOW,
        ).move_to(UP * 1.05)
        axes = self._geometry_axes(shift=DOWN * 0.78)
        span = self._span_line(axes, self.snapshot.direction)
        u_arrow = self._arrow(axes, self.snapshot.direction, BLUE)
        x_arrow = self._arrow(axes, self.snapshot.vector, ORANGE)
        u_label = MathTex(r"\mathbf{u}", font_size=36, color=BLUE).next_to(
            axes.c2p(*self.snapshot.direction), RIGHT, buff=0.08
        )
        x_label = MathTex(r"\mathbf{x}", font_size=36, color=ORANGE).next_to(
            axes.c2p(*self.snapshot.vector), UP, buff=0.08
        )
        caption = Text(
            "We want a vector on the blue line that captures x's component in that direction.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.26)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)
        group = VGroup(heading, question, axes, span, u_arrow, x_arrow, u_label, x_label, caption)
        self.play(FadeIn(heading), FadeIn(question), run_time=self.TRANSITION_TIME)
        self.play(Create(axes), Create(span), run_time=self.TRANSITION_TIME)
        self.play(Create(u_arrow), FadeIn(u_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(x_arrow), FadeIn(x_label), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(group), run_time=self.TRANSITION_TIME)

    def _perpendicular_drop_card(self) -> None:
        heading = Text("Drop a perpendicular", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._geometry_axes(shift=DOWN * 0.63 + RIGHT * 0.05)
        span = self._span_line(axes, self.snapshot.direction)
        u_arrow = self._arrow(axes, self.snapshot.direction, BLUE)
        x_arrow = self._arrow(axes, self.snapshot.vector, ORANGE)
        p_arrow = self._arrow(axes, self.snapshot.projection, GREEN)
        drop = DashedLine(
            axes.c2p(*self.snapshot.vector),
            axes.c2p(*self.snapshot.projection),
            color=WHITE,
            dash_length=0.12,
            stroke_width=3,
        )
        right_angle = self._right_angle_marker(axes, self.snapshot)
        p_label = MathTex(
            r"\mathbf{p}=\operatorname{proj}_{\mathbf{u}}\mathbf{x}",
            font_size=34,
            color=GREEN,
        ).next_to(axes.c2p(*self.snapshot.projection), DOWN, buff=0.18)
        statement = VGroup(
            MathTex(r"\mathbf{p}\in\operatorname{span}(\mathbf{u})", font_size=36),
            MathTex(r"(\mathbf{x}-\mathbf{p})\perp\mathbf{u}", font_size=36),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.6 + UP * 0.15)
        caption = Text(
            "The projection is the point on the line reached by a perpendicular drop from x.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.22)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)
        self.play(FadeIn(heading), Create(axes), Create(span), run_time=self.TRANSITION_TIME)
        self.play(Create(u_arrow), Create(x_arrow), run_time=self.EMPHASIS_TIME)
        self.play(Create(drop), run_time=self.TRANSITION_TIME)
        self.play(Create(p_arrow), FadeIn(p_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(right_angle), FadeIn(statement), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, axes, span, u_arrow, x_arrow, p_arrow, drop, right_angle, p_label, statement, caption)),
            run_time=self.TRANSITION_TIME,
        )

    def _derive_coefficient_card(self) -> None:
        heading = Text("Find the scalar amount along u", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        line1 = MathTex(r"\mathbf{p}=c\mathbf{u}", font_size=42)
        line2 = MathTex(r"(\mathbf{x}-c\mathbf{u})\cdot\mathbf{u}=0", font_size=42)
        line3 = MathTex(r"\mathbf{x}\cdot\mathbf{u}-c(\mathbf{u}\cdot\mathbf{u})=0", font_size=39)
        line4 = MathTex(
            r"c=\frac{\mathbf{x}\cdot\mathbf{u}}{\mathbf{u}\cdot\mathbf{u}}",
            font_size=44,
            color=YELLOW,
        )
        derivation = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.34).move_to(DOWN * 0.05)
        caption = Text(
            "The perpendicular residual determines exactly how far to travel along u.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(heading), FadeIn(line1), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(line2), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(line3), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(line4), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(FadeOut(VGroup(heading, derivation, caption)), run_time=self.TRANSITION_TIME)

    def _formula_card(self) -> None:
        heading = Text("Projection formula", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        general = MathTex(self.lesson.GENERAL_FORMULA, font_size=43).move_to(UP * 0.65)
        if general.width > 11.8:
            general.scale_to_fit_width(11.8)
        general_box = SurroundingRectangle(general, buff=0.20, color=WHITE)
        unit_intro = Text(
            "If q is a unit vector, q·q = 1:",
            font_size=24,
            color=GREY_B,
        ).move_to(DOWN * 0.45)
        unit = MathTex(self.lesson.UNIT_FORMULA, font_size=44, color=YELLOW).move_to(DOWN * 1.20)
        unit_box = SurroundingRectangle(unit, buff=0.18, color=WHITE)
        caption = Text(
            "This is why orthonormal directions make projection especially simple.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.18)
        self.play(FadeIn(heading), FadeIn(general), Create(general_box), run_time=self.TRANSITION_TIME)
        self.wait(0.7)
        self.play(FadeIn(unit_intro), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(unit), Create(unit_box), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, general, general_box, unit_intro, unit, unit_box, caption)),
            run_time=self.TRANSITION_TIME,
        )

    def _worked_example_card(self) -> None:
        heading = Text("A numerical projection", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = Axes(
            x_range=(-0.4, 4.8, 1),
            y_range=(-0.4, 3.8, 1),
            x_length=5.0,
            y_length=4.05,
            axis_config={"color": GREY_B, "stroke_width": 2.0, "include_ticks": False},
            tips=False,
        ).shift(LEFT * 3.35 + DOWN * 0.65)
        span = self._span_line(axes, self.snapshot.direction)
        x_arrow = self._arrow(axes, self.snapshot.vector, ORANGE)
        p_arrow = self._arrow(axes, self.snapshot.projection, GREEN)
        drop = DashedLine(
            axes.c2p(*self.snapshot.vector), axes.c2p(*self.snapshot.projection), color=WHITE, dash_length=0.11
        )
        right_angle = self._right_angle_marker(axes, self.snapshot)
        calculations = VGroup(
            MathTex(r"\mathbf{x}=(3,3),\quad \mathbf{u}=(4,1)", font_size=32),
            MathTex(r"\mathbf{x}\cdot\mathbf{u}=15", font_size=34),
            MathTex(r"\mathbf{u}\cdot\mathbf{u}=17", font_size=34),
            MathTex(r"c=\frac{15}{17}", font_size=38, color=YELLOW),
            MathTex(r"\mathbf{p}=\left(\frac{60}{17},\frac{15}{17}\right)", font_size=36, color=GREEN),
        ).arrange(DOWN, buff=0.24, aligned_edge=RIGHT).move_to(RIGHT * 3.55 + DOWN * 0.25)
        caption = Text(
            "The projected vector lies on span(u), and the remaining difference is perpendicular to u.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.18)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)
        self.play(FadeIn(heading), Create(axes), Create(span), run_time=self.TRANSITION_TIME)
        self.play(Create(x_arrow), run_time=self.EMPHASIS_TIME)
        self.play(Create(drop), Create(p_arrow), Create(right_angle), run_time=self.TRANSITION_TIME)
        for line in calculations:
            self.play(FadeIn(line), run_time=0.95)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, axes, span, x_arrow, p_arrow, drop, right_angle, calculations, caption)),
            run_time=self.TRANSITION_TIME,
        )

    def _orthogonal_residual_card(self) -> None:
        heading = Text("Projection creates an orthogonal decomposition", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        decomposition = MathTex(self.lesson.DECOMPOSITION, font_size=39).move_to(UP * 0.65)
        if decomposition.width > 12.0:
            decomposition.scale_to_fit_width(12.0)
        residual = MathTex(self.lesson.ORTHOGONAL_RESIDUAL, font_size=39, color=YELLOW).move_to(DOWN * 0.35)
        residual_box = SurroundingRectangle(residual, buff=0.18, color=WHITE)
        labels = VGroup(
            Text("parallel part", font_size=22, color=GREEN),
            Text("perpendicular part", font_size=22, color=ORANGE),
        ).arrange(RIGHT, buff=2.2).move_to(DOWN * 1.35)
        caption = Text(
            "Every vector is now split into a component along u and a component orthogonal to u.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.20)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)
        self.play(FadeIn(heading), FadeIn(decomposition), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(residual), Create(residual_box), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(labels), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
