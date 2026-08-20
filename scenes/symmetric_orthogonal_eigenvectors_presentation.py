"""Manim presentation: symmetric matrices and orthogonal eigenvectors."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Axes, Create, FadeIn, FadeOut, MathTex, ReplacementTransform,
    Scene, Text, VGroup,
)


class SymmetricOrthogonalEigenvectorsPresentation(Scene):
    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Symmetric Matrices and Orthogonal Eigenvectors"

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.6:
            item.scale_to_fit_width(11.6)
        return item

    def _math_heading(self, tex: str) -> MathTex:
        item = MathTex(tex, font_size=35, color=WHITE)
        if item.width > 11.6:
            item.scale_to_fit_width(11.6)
        return item

    def _chrome(self, heading_text: str):
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD")
        banner.to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=32, color=YELLOW, weight="BOLD")
        title.next_to(banner, DOWN, buff=0.12)
        heading = self._heading(heading_text)
        heading.next_to(title, DOWN, buff=0.17)
        return banner, title, heading

    def _replace_heading(self, old, text: str):
        new = self._heading(text).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.55)
        return new

    def _replace_math_heading(self, old, tex: str):
        new = self._math_heading(tex).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.55)
        return new

    def _fit(self, group: VGroup, heading, gap: float = 0.55) -> VGroup:
        group.next_to(heading, DOWN, buff=gap)
        if group.width > 11.8:
            group.scale_to_fit_width(11.8)
            group.next_to(heading, DOWN, buff=gap)
        bottom_limit = -3.25
        if group.get_bottom()[1] < bottom_limit:
            available = heading.get_bottom()[1] - gap - bottom_limit
            if available > 1.0:
                group.scale_to_fit_height(available)
                group.next_to(heading, DOWN, buff=gap)
        return group

    def construct(self) -> None:
        banner, title, heading = self._chrome("Symmetry gives eigenvectors an additional geometric structure.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.75)

        # Card 1 — symmetric matrix and two eigenpairs.
        matrix = MathTex(r"A=\begin{bmatrix}2&1\\1&2\end{bmatrix}", font_size=54, color=WHITE)
        symmetric = MathTex(r"A^T=A", font_size=48, color=YELLOW)
        pair1 = MathTex(r"A\begin{bmatrix}1\\1\end{bmatrix}=3\begin{bmatrix}1\\1\end{bmatrix}", font_size=43, color=GREEN_C)
        pair2 = MathTex(r"A\begin{bmatrix}1\\-1\end{bmatrix}=1\begin{bmatrix}1\\-1\end{bmatrix}", font_size=43, color=BLUE_C)
        card = self._fit(VGroup(VGroup(matrix, symmetric).arrange(RIGHT, buff=1.0), pair1, pair2).arrange(DOWN, buff=0.48), heading)
        self.play(FadeIn(matrix), FadeIn(symmetric))
        self.play(FadeIn(pair1))
        self.play(FadeIn(pair2))
        self.wait(1.5)

        # Card 2 — geometry: right angle.
        heading = self._replace_heading(heading, "The two eigenvectors point in perpendicular directions.")
        self.play(FadeOut(card))
        axes = Axes(x_range=[-2.5,2.5,1], y_range=[-2.5,2.5,1], x_length=5.0, y_length=5.0, tips=False)
        axes.shift(LEFT * 2.7 + DOWN * 0.25)
        v = Arrow(axes.c2p(0,0), axes.c2p(1,1), buff=0, color=GREEN_C, stroke_width=7)
        w = Arrow(axes.c2p(0,0), axes.c2p(1,-1), buff=0, color=BLUE_C, stroke_width=7)
        vlab = MathTex(r"\mathbf v=\begin{bmatrix}1\\1\end{bmatrix}", font_size=34, color=GREEN_C).next_to(v.get_end(), UP, buff=0.15)
        wlab = MathTex(r"\mathbf w=\begin{bmatrix}1\\-1\end{bmatrix}", font_size=34, color=BLUE_C).next_to(w.get_end(), DOWN, buff=0.15)
        dot = MathTex(r"\mathbf v^T\mathbf w=1(1)+1(-1)=0", font_size=44, color=WHITE)
        right_angle = MathTex(r"\mathbf v\perp\mathbf w", font_size=52, color=YELLOW)
        algebra = VGroup(dot, right_angle).arrange(DOWN, buff=0.55).to_edge(RIGHT, buff=0.7).shift(DOWN * 0.3)
        self.play(Create(axes), FadeIn(v), FadeIn(w), FadeIn(vlab), FadeIn(wlab), run_time=1.1)
        self.play(FadeIn(dot))
        self.play(FadeIn(right_angle))
        self.wait(1.6)

        # Card 3 — general setup.
        heading = self._replace_math_heading(heading, r"A^T=A,\quad A\mathbf v=\lambda\mathbf v,\quad A\mathbf w=\mu\mathbf w,\quad \lambda\ne\mu")
        self.play(FadeOut(axes), FadeOut(v), FadeOut(w), FadeOut(vlab), FadeOut(wlab), FadeOut(algebra))
        setup = MathTex(r"\text{Compare the scalar }\mathbf v^T A\mathbf w\text{ in two ways.}", font_size=45, color=WHITE)
        cue = Text("The symmetry of A lets us move A from one side of the dot product to the other.", font_size=28, color=YELLOW)
        card = self._fit(VGroup(setup, cue).arrange(DOWN, buff=0.65), heading, gap=0.9)
        self.play(FadeIn(setup))
        self.play(FadeIn(cue))
        self.wait(1.4)

        # Card 4 — first evaluation.
        heading = self._replace_heading(heading, "Use Aw = mu w.")
        self.play(FadeOut(card))
        line1 = MathTex(r"\mathbf v^T A\mathbf w=\mathbf v^T(\mu\mathbf w)", font_size=50, color=WHITE)
        line2 = MathTex(r"=\mu\,\mathbf v^T\mathbf w", font_size=54, color=BLUE_C)
        card = self._fit(VGroup(line1, line2).arrange(DOWN, buff=0.55), heading, gap=0.9)
        self.play(FadeIn(line1))
        self.play(FadeIn(line2))
        self.wait(1.3)

        # Card 5 — second evaluation using symmetry.
        heading = self._replace_math_heading(heading, r"A^T=A\text{ lets us rewrite }\mathbf v^T A\mathbf w=(A\mathbf v)^T\mathbf w")
        self.play(FadeOut(card))
        sym = MathTex(r"\mathbf v^T A\mathbf w=\mathbf v^T A^T\mathbf w=(A\mathbf v)^T\mathbf w", font_size=46, color=WHITE)
        use_v = MathTex(r"=(\lambda\mathbf v)^T\mathbf w", font_size=49, color=WHITE)
        result = MathTex(r"=\lambda\,\mathbf v^T\mathbf w", font_size=54, color=GREEN_C)
        card = self._fit(VGroup(sym, use_v, result).arrange(DOWN, buff=0.46), heading, gap=0.65)
        self.play(FadeIn(sym))
        self.play(FadeIn(use_v))
        self.play(FadeIn(result))
        self.wait(1.4)

        # Card 6 — equate the two expressions.
        heading = self._replace_heading(heading, "Both expressions equal the same scalar, so compare them.")
        self.play(FadeOut(card))
        equality = MathTex(r"\mu\,\mathbf v^T\mathbf w=\lambda\,\mathbf v^T\mathbf w", font_size=52, color=WHITE)
        factor = MathTex(r"(\lambda-\mu)\,\mathbf v^T\mathbf w=0", font_size=56, color=YELLOW)
        distinct = MathTex(r"\lambda\ne\mu\quad\Longrightarrow\quad\mathbf v^T\mathbf w=0", font_size=52, color=GREEN_C)
        conclusion = MathTex(r"\boxed{\mathbf v\perp\mathbf w}", font_size=58, color=YELLOW)
        card = self._fit(VGroup(equality, factor, distinct, conclusion).arrange(DOWN, buff=0.42), heading, gap=0.5)
        for item in card:
            self.play(FadeIn(item), run_time=0.48)
        self.wait(1.6)

        # Card 7 — normalize and build Q.
        heading = self._replace_heading(heading, "Normalize the eigenvectors and the eigenvector matrix becomes orthogonal.")
        self.play(FadeOut(card))
        q1 = MathTex(r"\mathbf q_1=\frac1{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}", font_size=46, color=GREEN_C)
        q2 = MathTex(r"\mathbf q_2=\frac1{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}", font_size=46, color=BLUE_C)
        qmat = MathTex(r"Q=[\mathbf q_1\ \mathbf q_2]=\frac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}", font_size=46, color=WHITE)
        orth = MathTex(r"Q^TQ=I\qquad\Longrightarrow\qquad Q^{-1}=Q^T", font_size=49, color=YELLOW)
        card = self._fit(VGroup(VGroup(q1,q2).arrange(RIGHT,buff=0.8), qmat, orth).arrange(DOWN,buff=0.48), heading, gap=0.5)
        self.play(FadeIn(q1), FadeIn(q2))
        self.play(FadeIn(qmat))
        self.play(FadeIn(orth))
        self.wait(1.6)

        # Card 8 — spectral theorem preview.
        heading = self._replace_heading(heading, "For real symmetric matrices, diagonalization can be done with an orthogonal basis.")
        self.play(FadeOut(card))
        d = MathTex(r"D=Q^TAQ=\begin{bmatrix}3&0\\0&1\end{bmatrix}", font_size=52, color=WHITE)
        spectral = MathTex(r"\boxed{A=QDQ^T}", font_size=64, color=YELLOW)
        note1 = Text("Columns of Q: orthonormal eigenvectors", font_size=29, color=GREEN_C)
        note2 = Text("Diagonal of D: corresponding eigenvalues", font_size=29, color=BLUE_C)
        takeaway = Text("This is the spectral theorem in matrix form.", font_size=30, color=WHITE)
        card = self._fit(VGroup(d, spectral, note1, note2, takeaway).arrange(DOWN,buff=0.40), heading, gap=0.45)
        self.play(FadeIn(d))
        self.play(FadeIn(spectral))
        self.play(FadeIn(note1), FadeIn(note2))
        self.play(FadeIn(takeaway))
        self.wait(2.0)
