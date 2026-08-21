"""Manim presentation for Dynamics and the Dominant Eigenvector."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    Arrow, Axes, FadeIn, FadeOut, MathTex, ReplacementTransform,
    Text, VGroup, Scene,
)

from engine.dominant_eigenvector import DominantEigenvectorLesson

DOWN = np.array([0.0, -1.0, 0.0])
UP = np.array([0.0, 1.0, 0.0])
LEFT = np.array([-1.0, 0.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])


class DominantEigenvectorPresentation(Scene):
    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Dynamics and the Dominant Eigenvector"

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.7:
            item.scale_to_fit_width(11.7)
        return item

    def _chrome(self, heading_text: str):
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD").to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=32, color=YELLOW, weight="BOLD").next_to(banner, DOWN, buff=0.12)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.17)
        return banner, title, heading

    def _replace_heading(self, old: Text, text: str) -> Text:
        new = self._heading(text).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.5)
        return new

    def construct(self) -> None:
        lesson = DominantEigenvectorLesson()
        banner, title, heading = self._chrome("Repeated transformations reveal which eigendirection grows fastest.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.8)

        # Card 1: recall diagonal dynamics.
        formula1 = MathTex(r"A=QDQ^T", font_size=48, color=WHITE)
        formula2 = MathTex(r"A^k=QD^kQ^T", font_size=50, color=YELLOW)
        formula3 = MathTex(r"D^k=\begin{bmatrix}\lambda_1^k&0\\0&\lambda_2^k\end{bmatrix}", font_size=44, color=GREEN_C)
        g = VGroup(formula1, formula2, formula3).arrange(DOWN, buff=0.5).shift(DOWN*0.25)
        self.play(FadeIn(formula1)); self.play(FadeIn(formula2)); self.play(FadeIn(formula3)); self.wait(1.4)

        # Card 2: concrete matrix and eigendirections.
        heading = self._replace_heading(heading, "Use a matrix with two different growth rates.")
        self.play(FadeOut(g))
        matrix = MathTex(r"A=\begin{bmatrix}3&1\\1&3\end{bmatrix}", font_size=44)
        q1 = MathTex(r"\mathbf q_1=\frac1{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\quad \lambda_1=4", font_size=39, color=GREEN_C)
        q2 = MathTex(r"\mathbf q_2=\frac1{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix},\quad \lambda_2=2", font_size=39, color=BLUE_C)
        block = VGroup(matrix, q1, q2).arrange(DOWN, buff=0.48).shift(DOWN*0.2)
        self.play(FadeIn(matrix)); self.play(FadeIn(q1), FadeIn(q2)); self.wait(1.4)

        # Card 3: decompose x and apply powers.
        heading = self._replace_heading(heading, "Track each eigenvector component separately.")
        self.play(FadeOut(block))
        xeq = MathTex(r"\mathbf x=\mathbf q_1+\mathbf q_2", font_size=46, color=ORANGE)
        p1 = MathTex(r"A^k\mathbf x=4^k\mathbf q_1+2^k\mathbf q_2", font_size=46, color=WHITE)
        p2 = MathTex(r"=4^k\left(\mathbf q_1+\left(\frac12\right)^k\mathbf q_2\right)", font_size=46, color=YELLOW)
        stack = VGroup(xeq, p1, p2).arrange(DOWN, buff=0.55).shift(DOWN*0.1)
        self.play(FadeIn(xeq)); self.play(FadeIn(p1)); self.play(FadeIn(p2)); self.wait(1.6)

        # Card 4: numerical ratios.
        heading = self._replace_heading(heading, "The slower component becomes negligible relative to the faster one.")
        self.play(FadeOut(stack))
        ratios = VGroup(
            MathTex(r"k=1:\quad 4\mathbf q_1+2\mathbf q_2", font_size=40),
            MathTex(r"k=2:\quad 16\mathbf q_1+4\mathbf q_2", font_size=40),
            MathTex(r"k=4:\quad 256\mathbf q_1+16\mathbf q_2", font_size=40),
            MathTex(r"\frac{2^k}{4^k}=\left(\frac12\right)^k\longrightarrow 0", font_size=46, color=YELLOW),
        ).arrange(DOWN, buff=0.42).shift(DOWN*0.15)
        for item in ratios:
            self.play(FadeIn(item), run_time=0.45)
        self.wait(1.5)

        # Card 5: geometry of convergence in direction.
        heading = self._replace_heading(heading, "After normalization, the iterates point toward the dominant eigenvector.")
        self.play(FadeOut(ratios))
        axes = Axes(x_range=[-0.2, 1.4, 0.5], y_range=[-0.2, 1.4, 0.5], x_length=5.2, y_length=5.2, tips=False)
        axes.shift(LEFT*2.6 + DOWN*0.5)
        origin = axes.c2p(0,0)
        q1dir = np.array([1,1], dtype=float) / np.sqrt(2)
        q1_arrow = Arrow(origin, axes.c2p(*(0.95*q1dir)), buff=0, color=GREEN_C, stroke_width=6)
        q1_label = MathTex(r"\mathbf q_1", color=GREEN_C, font_size=34).next_to(q1_arrow.get_end(), UP, buff=0.12)
        arrows = []
        for k, color in [(0, ORANGE), (1, BLUE_C), (2, WHITE), (4, YELLOW)]:
            d = lesson.normalized_power_direction(k)
            a = Arrow(origin, axes.c2p(*(0.95*d)), buff=0, color=color, stroke_width=5)
            arrows.append(a)
        labels = VGroup(
            MathTex(r"k=0", font_size=30, color=ORANGE),
            MathTex(r"k=1", font_size=30, color=BLUE_C),
            MathTex(r"k=2", font_size=30, color=WHITE),
            MathTex(r"k=4", font_size=30, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=1.1).shift(DOWN*0.25)
        self.play(FadeIn(axes), FadeIn(q1_arrow), FadeIn(q1_label))
        for a, lab in zip(arrows, labels):
            self.play(FadeIn(a), FadeIn(lab), run_time=0.45)
        self.wait(1.6)

        # Card 6: general dominant-eigenvalue statement.
        heading = self._replace_heading(heading, "The largest eigenvalue magnitude controls the long-term direction.")
        self.play(FadeOut(axes), FadeOut(q1_arrow), FadeOut(q1_label), *(FadeOut(a) for a in arrows), FadeOut(labels))
        general = MathTex(
            r"\mathbf x=\sum_i c_i\mathbf v_i"
            r"\quad\Longrightarrow\quad "
            r"A^k\mathbf x=\sum_i c_i\lambda_i^k\mathbf v_i",
            font_size=41,
            color=WHITE,
        )
        condition = MathTex(r"|\lambda_1|>|\lambda_2|\ge\cdots", font_size=44, color=YELLOW)
        conclusion = MathTex(r"\frac{A^k\mathbf x}{\|A^k\mathbf x\|}\longrightarrow \pm\frac{\mathbf v_1}{\|\mathbf v_1\|}", font_size=43, color=GREEN_C)
        caveat = Text("provided the starting vector has a nonzero component in the dominant eigendirection", font_size=25, color=GREY_B)
        final = VGroup(general, condition, conclusion, caveat).arrange(DOWN, buff=0.5).shift(DOWN*0.1)
        self.play(FadeIn(general)); self.play(FadeIn(condition)); self.play(FadeIn(conclusion)); self.play(FadeIn(caveat)); self.wait(2.0)
