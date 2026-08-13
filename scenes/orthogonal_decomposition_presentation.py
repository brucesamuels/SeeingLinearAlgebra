"""CP154: Orthogonal Decomposition."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Axes,
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
    ORANGE,
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

from engine.orthogonal_decomposition import (
    OrthogonalDecompositionLesson,
    OrthogonalDecompositionSnapshot,
)


class OrthogonalDecompositionPresentation(Scene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Orthogonal Decomposition"
    SCENE_REVISION = "cp154_r2_labeled_geometry"
    TRANSITION_TIME = 1.35
    EMPHASIS_TIME = 1.15
    HOLD_TIME = 2.6
    LONG_HOLD_TIME = 3.0

    def construct(self) -> None:
        self.lesson = OrthogonalDecompositionLesson()
        self.snapshot = self.lesson.example()
        banner, lesson_title = self._header()
        self.lesson_title_mobject = lesson_title
        self.add(banner, lesson_title)

        self._projection_becomes_split_card()
        self._where_parts_live_card()
        self._uniqueness_card()
        self._worked_example_card()
        self._pythagorean_card()
        self._bridge_to_subspaces_card()

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

    def _axes(self, *, shift=DOWN * 0.55) -> Axes:
        return Axes(
            x_range=(-0.7, 5.0, 1),
            y_range=(-1.4, 4.4, 1),
            x_length=6.25,
            y_length=5.35,
            axis_config={"color": GREY_B, "stroke_width": 2.0, "include_ticks": False},
            tips=False,
        ).shift(shift)

    def _span_line(self, axes: Axes, direction: np.ndarray) -> Line:
        unit = direction / np.linalg.norm(direction)
        return Line(
            axes.c2p(*(-0.65 * unit)),
            axes.c2p(*(5.8 * unit)),
            color=BLUE,
            stroke_width=4,
            stroke_opacity=0.55,
        )

    def _origin_arrow(self, axes: Axes, end: np.ndarray, color: str) -> Arrow:
        return Arrow(
            axes.c2p(0, 0),
            axes.c2p(*end),
            buff=0,
            color=color,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.12,
        )

    def _residual_arrow(self, axes: Axes, snapshot: OrthogonalDecompositionSnapshot) -> Arrow:
        return Arrow(
            axes.c2p(*snapshot.parallel),
            axes.c2p(*(snapshot.parallel + snapshot.perpendicular)),
            buff=0,
            color=WHITE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.16,
        )

    def _right_angle_marker(self, axes: Axes, snapshot: OrthogonalDecompositionSnapshot) -> VGroup:
        p_hat = snapshot.parallel / np.linalg.norm(snapshot.parallel)
        r_hat = snapshot.perpendicular / np.linalg.norm(snapshot.perpendicular)
        corner = snapshot.parallel
        size = 0.26
        a = corner - size * p_hat
        b = a + size * r_hat
        c = corner + size * r_hat
        return VGroup(
            Line(axes.c2p(*corner), axes.c2p(*a), color=YELLOW, stroke_width=3),
            Line(axes.c2p(*a), axes.c2p(*b), color=YELLOW, stroke_width=3),
            Line(axes.c2p(*b), axes.c2p(*c), color=YELLOW, stroke_width=3),
        )

    def _projection_becomes_split_card(self) -> None:
        heading = Text("Projection gives more than one vector", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        prompt = Text(
            "It splits x into a part along W and a perpendicular remainder.",
            font_size=27,
            color=YELLOW,
        ).move_to(UP * 1.12)
        axes = self._axes(shift=LEFT * 0.25 + DOWN * 0.78)
        span = self._span_line(axes, self.snapshot.direction)
        x_arrow = self._origin_arrow(axes, self.snapshot.vector, ORANGE)
        p_arrow = self._origin_arrow(axes, self.snapshot.parallel, GREEN)
        r_arrow = self._residual_arrow(axes, self.snapshot)
        right_angle = self._right_angle_marker(axes, self.snapshot)
        x_label = MathTex(r"\mathbf{x}", font_size=34, color=ORANGE).next_to(
            axes.c2p(*self.snapshot.vector), RIGHT, buff=0.08
        )
        p_label = MathTex(r"\mathbf{p}", font_size=34, color=GREEN).next_to(
            axes.c2p(*self.snapshot.parallel), UP, buff=0.08
        )
        r_label = MathTex(r"\mathbf{r}", font_size=34, color=WHITE).next_to(
            axes.c2p(*(0.5 * (self.snapshot.parallel + self.snapshot.vector))), RIGHT, buff=0.10
        )
        w_diagram_label = MathTex(r"W", font_size=32, color=BLUE).move_to(
            axes.c2p(1.65, 1.65) + LEFT * 0.42 + UP * 0.28
        )
        equation = MathTex(r"\mathbf{x}=\mathbf{p}+\mathbf{r}", font_size=40).to_edge(DOWN, buff=0.24)

        self.play(FadeIn(heading), FadeIn(prompt), run_time=self.TRANSITION_TIME)
        self.play(Create(axes), Create(span), FadeIn(w_diagram_label), run_time=self.TRANSITION_TIME)
        self.play(Create(x_arrow), FadeIn(x_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(p_arrow), FadeIn(p_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(r_arrow), FadeIn(r_label), Create(right_angle), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(equation), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, prompt, axes, span, x_arrow, p_arrow, r_arrow, right_angle,
                           x_label, p_label, r_label, w_diagram_label, equation)),
            run_time=self.TRANSITION_TIME,
        )

    def _where_parts_live_card(self) -> None:
        heading = Text("Where do the two pieces live?", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._axes(shift=LEFT * 3.25 + DOWN * 0.72)
        span = self._span_line(axes, self.snapshot.direction)
        p_arrow = self._origin_arrow(axes, self.snapshot.parallel, GREEN)
        r_arrow = self._residual_arrow(axes, self.snapshot)
        right_angle = self._right_angle_marker(axes, self.snapshot)
        w_diagram_label = MathTex(r"W", font_size=32, color=BLUE).move_to(
            axes.c2p(1.65, 1.65) + LEFT * 0.42 + UP * 0.28
        )
        p_diagram_label = MathTex(r"\mathbf{p}", font_size=32, color=GREEN).next_to(
            axes.c2p(*self.snapshot.parallel), UP, buff=0.08
        )
        r_diagram_label = MathTex(r"\mathbf{r}", font_size=32, color=WHITE).move_to(
            axes.c2p(*(0.5 * (self.snapshot.parallel + self.snapshot.vector))) + DOWN * 0.28
        )
        statements = VGroup(
            MathTex(r"W=\operatorname{span}(\mathbf{u})", font_size=36, color=BLUE),
            MathTex(r"\mathbf{p}\in W", font_size=38, color=GREEN),
            MathTex(r"\mathbf{r}=\mathbf{x}-\mathbf{p}\in W^\perp", font_size=36),
            MathTex(r"\mathbf{p}\cdot\mathbf{r}=0", font_size=38, color=YELLOW),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(RIGHT * 3.2 + DOWN * 0.15)
        caption = Text(
            "The parallel component belongs to W; the remainder belongs to its orthogonal complement.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.20)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)

        self.play(
            FadeIn(heading), Create(axes), Create(span), FadeIn(w_diagram_label),
            run_time=self.TRANSITION_TIME,
        )
        self.play(
            Create(p_arrow), Create(r_arrow), Create(right_angle),
            FadeIn(p_diagram_label), FadeIn(r_diagram_label),
            run_time=self.TRANSITION_TIME,
        )
        for statement in statements:
            self.play(FadeIn(statement), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(
            FadeOut(VGroup(
                heading, axes, span, p_arrow, r_arrow, right_angle,
                w_diagram_label, p_diagram_label, r_diagram_label, statements, caption,
            )),
            run_time=self.TRANSITION_TIME,
        )

    def _uniqueness_card(self) -> None:
        heading = Text("Why is the orthogonal split unique?", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        line1 = MathTex(
            r"\mathbf{x}=\mathbf{p}+\mathbf{r}=\mathbf{p}'+\mathbf{r}'",
            font_size=40,
        )
        line2 = MathTex(
            r"\mathbf{p}-\mathbf{p}'=\mathbf{r}'-\mathbf{r}",
            font_size=40,
        )
        line3 = VGroup(
            MathTex(r"\mathbf{p}-\mathbf{p}'\in W", font_size=34, color=GREEN),
            MathTex(r"\mathbf{r}'-\mathbf{r}\in W^\perp", font_size=34, color=WHITE),
        ).arrange(RIGHT, buff=1.0)
        line4 = MathTex(r"W\cap W^\perp=\{\mathbf{0}\}", font_size=40, color=YELLOW)
        line5 = MathTex(
            r"\mathbf{p}=\mathbf{p}',\qquad \mathbf{r}=\mathbf{r}'",
            font_size=40,
        )
        proof = VGroup(line1, line2, line3, line4, line5).arrange(DOWN, buff=0.34).move_to(DOWN * 0.10)
        caption = Text(
            "A vector cannot be both in W and perpendicular to W unless it is the zero vector.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.22)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)

        self.play(FadeIn(heading), FadeIn(line1), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(line2), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(line3), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(line4), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(line5), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(FadeOut(VGroup(heading, proof, caption)), run_time=self.TRANSITION_TIME)

    def _worked_example_card(self) -> None:
        heading = Text("A clean numerical decomposition", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = Axes(
            x_range=(-0.5, 4.8, 1),
            y_range=(-1.3, 4.2, 1),
            x_length=5.3,
            y_length=4.75,
            axis_config={"color": GREY_B, "stroke_width": 2.0, "include_ticks": False},
            tips=False,
        ).shift(LEFT * 3.35 + DOWN * 0.72)
        span = self._span_line(axes, self.snapshot.direction)
        x_arrow = self._origin_arrow(axes, self.snapshot.vector, ORANGE)
        p_arrow = self._origin_arrow(axes, self.snapshot.parallel, GREEN)
        r_arrow = self._residual_arrow(axes, self.snapshot)
        right_angle = self._right_angle_marker(axes, self.snapshot)
        w_diagram_label = MathTex(
            r"W=\operatorname{span}(1,1)", font_size=26, color=BLUE
        ).move_to(axes.c2p(1.55, 1.55) + LEFT * 0.58 + UP * 0.30)
        x_diagram_label = MathTex(r"\mathbf{x}", font_size=32, color=ORANGE).next_to(
            axes.c2p(*self.snapshot.vector), RIGHT, buff=0.08
        )
        p_diagram_label = MathTex(r"\mathbf{p}", font_size=32, color=GREEN).next_to(
            axes.c2p(*self.snapshot.parallel), UP, buff=0.08
        )
        r_diagram_label = MathTex(r"\mathbf{r}", font_size=32, color=WHITE).move_to(
            axes.c2p(*(0.5 * (self.snapshot.parallel + self.snapshot.vector))) + DOWN * 0.28
        )
        calculations = VGroup(
            MathTex(r"\mathbf{x}=(4,2),\quad W=\operatorname{span}(1,1)", font_size=31),
            MathTex(r"\mathbf{p}=(3,3)", font_size=36, color=GREEN),
            MathTex(r"\mathbf{r}=\mathbf{x}-\mathbf{p}=(1,-1)", font_size=34),
            MathTex(r"(3,3)\cdot(1,-1)=0", font_size=35, color=YELLOW),
            MathTex(r"(4,2)=(3,3)+(1,-1)", font_size=35),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 3.25 + DOWN * 0.15)
        caption = Text(
            "The two components reconstruct x exactly, and they meet at a right angle.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.18)

        self.play(
            FadeIn(heading), Create(axes), Create(span), FadeIn(w_diagram_label),
            run_time=self.TRANSITION_TIME,
        )
        self.play(Create(x_arrow), FadeIn(x_diagram_label), run_time=self.EMPHASIS_TIME)
        self.play(
            Create(p_arrow), Create(r_arrow), Create(right_angle),
            FadeIn(p_diagram_label), FadeIn(r_diagram_label),
            run_time=self.TRANSITION_TIME,
        )
        for line in calculations:
            self.play(FadeIn(line), run_time=0.98)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(
            FadeOut(VGroup(
                heading, axes, span, x_arrow, p_arrow, r_arrow, right_angle,
                w_diagram_label, x_diagram_label, p_diagram_label, r_diagram_label,
                calculations, caption,
            )),
            run_time=self.TRANSITION_TIME,
        )

    def _pythagorean_card(self) -> None:
        heading = Text("Perpendicular pieces preserve length information", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        general = MathTex(self.lesson.PYTHAGOREAN, font_size=44).move_to(UP * 0.85)
        general_box = SurroundingRectangle(general, buff=0.18, color=WHITE)
        explanation = Text(
            "Because p is perpendicular to r, the decomposition forms a right triangle.",
            font_size=25,
            color=GREY_B,
        ).move_to(UP * 0.05)
        numeric = VGroup(
            MathTex(r"\|\mathbf{x}\|^2=4^2+2^2=20", font_size=36, color=ORANGE),
            MathTex(r"\|\mathbf{p}\|^2=3^2+3^2=18", font_size=36, color=GREEN),
            MathTex(r"\|\mathbf{r}\|^2=1^2+(-1)^2=2", font_size=36),
            MathTex(r"20=18+2", font_size=42, color=YELLOW),
        ).arrange(DOWN, buff=0.24).move_to(DOWN * 1.25)

        self.play(FadeIn(heading), FadeIn(general), Create(general_box), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(explanation), run_time=self.EMPHASIS_TIME)
        for line in numeric:
            self.play(FadeIn(line), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(
            FadeOut(VGroup(heading, general, general_box, explanation, numeric)),
            run_time=self.TRANSITION_TIME,
        )

    def _bridge_to_subspaces_card(self) -> None:
        heading = Text("The line was only the first case", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        decomposition = MathTex(self.lesson.LINE_DECOMPOSITION, font_size=39).move_to(UP * 0.82)
        if decomposition.width > 12.0:
            decomposition.scale_to_fit_width(12.0)
        identities = MathTex(self.lesson.PROJECTION_IDENTITIES, font_size=37).move_to(DOWN * 0.05)
        if identities.width > 11.8:
            identities.scale_to_fit_width(11.8)
        question = Text(
            "How do we find p when W has several basis vectors?",
            font_size=29,
            color=YELLOW,
        ).move_to(DOWN * 1.18)
        caption = Text(
            "That question leads from projection onto a vector to projection onto a subspace.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.22)

        self.play(FadeIn(heading), FadeIn(decomposition), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(identities), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(question), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
