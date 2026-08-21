"""Manim presentation: the spectral theorem for real symmetric matrices."""
from __future__ import annotations

from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Axes, Create, FadeIn, FadeOut, MathTex, ReplacementTransform,
    Scene, Text, VGroup,
)


class SpectralTheoremPresentation(Scene):
    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "The Spectral Theorem"

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
        banner, title, heading = self._chrome("Symmetric matrices have an especially simple diagonalization.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.75)

        # Card 1 — recall CP178 structure.
        a = MathTex(r"A=\begin{bmatrix}2&1\\1&2\end{bmatrix}", font_size=54, color=WHITE)
        sym = MathTex(r"A^T=A", font_size=48, color=YELLOW)
        q = MathTex(
            r"Q=\frac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}",
            font_size=52, color=GREEN_C,
        )
        orth = MathTex(r"Q^TQ=I\qquad\Longrightarrow\qquad Q^{-1}=Q^T", font_size=46, color=BLUE_C)
        card = self._fit(VGroup(VGroup(a, sym).arrange(RIGHT, buff=1.0), q, orth).arrange(DOWN, buff=0.5), heading)
        self.play(FadeIn(a), FadeIn(sym))
        self.play(FadeIn(q))
        self.play(FadeIn(orth))
        self.wait(1.5)

        # Card 2 — compute D from A and Q.
        heading = self._replace_math_heading(heading, r"D=Q^{-1}AQ=Q^TAQ")
        self.play(FadeOut(card))
        product = MathTex(
            r"D=\frac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}"
            r"\begin{bmatrix}2&1\\1&2\end{bmatrix}"
            r"\frac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}",
            font_size=40, color=WHITE,
        )
        middle = MathTex(
            r"=\frac12\begin{bmatrix}3&3\\1&-1\end{bmatrix}"
            r"\begin{bmatrix}1&1\\1&-1\end{bmatrix}",
            font_size=48, color=WHITE,
        )
        result = MathTex(r"=\begin{bmatrix}3&0\\0&1\end{bmatrix}", font_size=58, color=YELLOW)
        card = self._fit(VGroup(product, middle, result).arrange(DOWN, buff=0.5), heading, gap=0.65)
        self.play(FadeIn(product))
        self.play(FadeIn(middle))
        self.play(FadeIn(result))
        self.wait(1.5)

        # Card 3 — solve for A.
        heading = self._replace_heading(heading, "Now rearrange the diagonalization formula to reconstruct A.")
        self.play(FadeOut(card))
        line1 = MathTex(r"Q^TAQ=D", font_size=54, color=WHITE)
        line2 = MathTex(r"QQ^TAQQ^T=QDQ^T", font_size=50, color=WHITE)
        line3 = MathTex(r"IAI=QDQ^T", font_size=46, color=GREY_B)
        line4 = MathTex(r"\boxed{A=QDQ^T}", font_size=66, color=YELLOW)
        card = self._fit(VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.42), heading, gap=0.5)
        for item in card:
            self.play(FadeIn(item), run_time=0.48)
        self.wait(1.5)

        # Card 4 — explicit reconstruction.
        heading = self._replace_math_heading(heading, r"A=QDQ^T\text{ reconstructs the original matrix exactly.}")
        self.play(FadeOut(card))
        reconstruction = MathTex(
            r"A="
            r"\frac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}"
            r"\begin{bmatrix}3&0\\0&1\end{bmatrix}"
            r"\frac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}",
            font_size=39, color=WHITE,
        )
        recon2 = MathTex(
            r"=\frac12\begin{bmatrix}3&1\\3&-1\end{bmatrix}"
            r"\begin{bmatrix}1&1\\1&-1\end{bmatrix}",
            font_size=48, color=WHITE,
        )
        recon3 = MathTex(r"=\begin{bmatrix}2&1\\1&2\end{bmatrix}", font_size=58, color=GREEN_C)
        card = self._fit(VGroup(reconstruction, recon2, recon3).arrange(DOWN, buff=0.5), heading, gap=0.65)
        self.play(FadeIn(reconstruction))
        self.play(FadeIn(recon2))
        self.play(FadeIn(recon3))
        self.wait(1.5)

        # Card 5 — geometric interpretation.
        heading = self._replace_heading(heading, "The factorization separates orientation from scaling.")
        self.play(FadeOut(card))
        axes = Axes(x_range=[-3,3,1], y_range=[-3,3,1], x_length=4.8, y_length=4.8, tips=False)
        axes.shift(LEFT * 2.8 + DOWN * 0.25)
        q1 = Arrow(axes.c2p(0,0), axes.c2p(1,1), buff=0, color=GREEN_C, stroke_width=7)
        q2 = Arrow(axes.c2p(0,0), axes.c2p(1,-1), buff=0, color=BLUE_C, stroke_width=7)
        q1lab = MathTex(r"\mathbf q_1", font_size=34, color=GREEN_C).next_to(q1.get_end(), UP, buff=0.12)
        q2lab = MathTex(r"\mathbf q_2", font_size=34, color=BLUE_C).next_to(q2.get_end(), DOWN, buff=0.12)
        flow1 = MathTex(r"Q^T:\ \text{move into eigenvector coordinates}", font_size=38, color=WHITE)
        flow2 = MathTex(r"D:\ \text{scale by }3\text{ and }1", font_size=40, color=YELLOW)
        flow3 = MathTex(r"Q:\ \text{move back to standard coordinates}", font_size=38, color=WHITE)
        flow = VGroup(flow1, flow2, flow3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.25)
        self.play(Create(axes), FadeIn(q1), FadeIn(q2), FadeIn(q1lab), FadeIn(q2lab), run_time=1.0)
        self.play(FadeIn(flow1))
        self.play(FadeIn(flow2))
        self.play(FadeIn(flow3))
        self.wait(1.6)

        # Card 6 — theorem statement.
        heading = self._replace_heading(heading, "Spectral Theorem for real symmetric matrices")
        self.play(FadeOut(axes), FadeOut(q1), FadeOut(q2), FadeOut(q1lab), FadeOut(q2lab), FadeOut(flow))
        theorem1 = MathTex(r"A^T=A", font_size=50, color=WHITE)
        theorem2 = MathTex(r"\Longrightarrow\ \text{there exists an orthogonal }Q\text{ and diagonal }D", font_size=42, color=WHITE)
        theorem3 = MathTex(r"\boxed{A=QDQ^T}", font_size=66, color=YELLOW)
        theorem4 = Text("The columns of Q are an orthonormal basis of eigenvectors.", font_size=29, color=GREEN_C)
        theorem5 = Text("The diagonal entries of D are the corresponding eigenvalues.", font_size=29, color=BLUE_C)
        card = self._fit(VGroup(theorem1, theorem2, theorem3, theorem4, theorem5).arrange(DOWN, buff=0.4), heading, gap=0.45)
        self.play(FadeIn(theorem1))
        self.play(FadeIn(theorem2))
        self.play(FadeIn(theorem3))
        self.play(FadeIn(theorem4), FadeIn(theorem5))
        self.wait(1.8)

        # Card 7 — why this matters.
        heading = self._replace_heading(heading, "Symmetry turns diagonalization into an orthogonal change of coordinates.")
        self.play(FadeOut(card))
        p1 = MathTex(
            r"\text{No arbitrary inverse is needed: }Q^{-1}\text{ becomes }Q^T.",
            font_size=40, color=WHITE,
        )
        p2 = Text("Orthogonal directions are preserved cleanly and numerically stably.", font_size=30, color=WHITE)
        p3 = MathTex(r"A=QDQ^T", font_size=66, color=YELLOW)
        p4 = Text("This structure underlies quadratic forms, principal axes, PCA, and the SVD.", font_size=29, color=GREEN_C)
        card = self._fit(VGroup(p1, p2, p3, p4).arrange(DOWN, buff=0.5), heading, gap=0.6)
        self.play(FadeIn(p1))
        self.play(FadeIn(p2))
        self.play(FadeIn(p3))
        self.play(FadeIn(p4))
        self.wait(2.0)
