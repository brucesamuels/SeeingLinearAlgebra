"""Manim presentation: repeated eigenvalues and diagonalizability."""
from __future__ import annotations

from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, RED_C, WHITE, YELLOW,
    DOWN, RIGHT, UP,
    FadeIn, FadeOut, MathTex, ReplacementTransform, Scene, Text, VGroup,
)


class RepeatedEigenvaluesPresentation(Scene):
    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Repeated Eigenvalues and Diagonalizability"

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

    def _fit(self, group: VGroup, heading, gap: float = 0.56) -> VGroup:
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
        banner, title, heading = self._chrome("A repeated eigenvalue does not by itself tell us whether a matrix is diagonalizable.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.75)

        # Card 1 — same characteristic polynomial, two different matrices.
        good = MathTex(r"A_1=\begin{bmatrix}2&0\\0&2\end{bmatrix}", font_size=52, color=GREEN_C)
        bad = MathTex(r"A_2=\begin{bmatrix}2&1\\0&2\end{bmatrix}", font_size=52, color=ORANGE)
        pair = VGroup(good, bad).arrange(RIGHT, buff=1.35)
        charpoly = MathTex(r"\det(A_i-\lambda I)=(2-\lambda)^2", font_size=46, color=WHITE)
        repeated = MathTex(r"\lambda=2\quad\text{with multiplicity }2", font_size=42, color=YELLOW)
        card = self._fit(VGroup(pair, charpoly, repeated).arrange(DOWN, buff=0.54), heading)
        self.play(FadeIn(pair))
        self.play(FadeIn(charpoly))
        self.play(FadeIn(repeated))
        self.wait(1.5)

        # Card 2 — first matrix has a two-dimensional eigenspace.
        heading = self._replace_math_heading(heading, r"\text{For }A_1,\text{ find }E_2=\operatorname{Null}(A_1-2I)\text{.}")
        self.play(FadeOut(card))
        subtract = MathTex(
            r"A_1-2I=\begin{bmatrix}2&0\\0&2\end{bmatrix}-\begin{bmatrix}2&0\\0&2\end{bmatrix}",
            font_size=43,
            color=WHITE,
        )
        zero = MathTex(r"=\begin{bmatrix}0&0\\0&0\end{bmatrix}", font_size=48, color=GREEN_C)
        nullspace = MathTex(r"E_2=\operatorname{Null}(0)=\mathbb R^2", font_size=50, color=YELLOW)
        basis = MathTex(r"\text{Two independent eigenvectors: }\begin{bmatrix}1\\0\end{bmatrix},\ \begin{bmatrix}0\\1\end{bmatrix}", font_size=39, color=WHITE)
        conclusion = Text("Enough eigenvectors for a basis: A1 is diagonalizable.", font_size=28, color=GREEN_C)
        card = self._fit(VGroup(subtract, zero, nullspace, basis, conclusion).arrange(DOWN, buff=0.33), heading, gap=0.43)
        for item in card:
            self.play(FadeIn(item), run_time=0.45)
        self.wait(1.5)

        # Card 3 — second matrix has only a one-dimensional eigenspace.
        heading = self._replace_math_heading(heading, r"\text{For }A_2,\text{ again find }E_2=\operatorname{Null}(A_2-2I)\text{.}")
        self.play(FadeOut(card))
        subtract2 = MathTex(
            r"A_2-2I=\begin{bmatrix}2&1\\0&2\end{bmatrix}-\begin{bmatrix}2&0\\0&2\end{bmatrix}",
            font_size=43,
            color=WHITE,
        )
        shifted = MathTex(r"=\begin{bmatrix}0&1\\0&0\end{bmatrix}", font_size=48, color=ORANGE)
        system = MathTex(r"\begin{bmatrix}0&1\\0&0\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix}=0\quad\Longrightarrow\quad y=0", font_size=43, color=WHITE)
        eigenspace = MathTex(r"E_2=\operatorname{span}\left\{\begin{bmatrix}1\\0\end{bmatrix}\right\}", font_size=50, color=YELLOW)
        conclusion2 = Text("Only one independent eigenvector: A2 is not diagonalizable.", font_size=28, color=RED_C)
        card = self._fit(VGroup(subtract2, shifted, system, eigenspace, conclusion2).arrange(DOWN, buff=0.31), heading, gap=0.42)
        for item in card:
            self.play(FadeIn(item), run_time=0.45)
        self.wait(1.5)

        # Card 4 — compare the two eigenspaces directly.
        heading = self._replace_heading(heading, "The characteristic polynomial is the same; the eigenspace dimension is not.")
        self.play(FadeOut(card))
        left_title = Text("A1", font_size=30, color=GREEN_C, weight="BOLD")
        left_poly = MathTex(r"(2-\lambda)^2", font_size=43, color=WHITE)
        left_space = MathTex(r"\dim E_2=2", font_size=49, color=GREEN_C)
        left_result = Text("diagonalizable", font_size=27, color=GREEN_C)
        left = VGroup(left_title, left_poly, left_space, left_result).arrange(DOWN, buff=0.35)
        right_title = Text("A2", font_size=30, color=ORANGE, weight="BOLD")
        right_poly = MathTex(r"(2-\lambda)^2", font_size=43, color=WHITE)
        right_space = MathTex(r"\dim E_2=1", font_size=49, color=ORANGE)
        right_result = Text("not diagonalizable", font_size=27, color=RED_C)
        right = VGroup(right_title, right_poly, right_space, right_result).arrange(DOWN, buff=0.35)
        comparison = VGroup(left, right).arrange(RIGHT, buff=2.2)
        card = self._fit(comparison, heading, gap=0.75)
        self.play(FadeIn(left))
        self.play(FadeIn(right))
        self.wait(1.6)

        # Card 5 — name the two multiplicities.
        heading = self._replace_heading(heading, "Two different multiplicities are measuring two different things.")
        self.play(FadeOut(card))
        algebraic = MathTex(
            r"\text{Algebraic multiplicity}=\text{multiplicity as a root of }\det(A-\lambda I)",
            font_size=38,
            color=WHITE,
        )
        geometric = MathTex(
            r"\text{Geometric multiplicity}=\dim E_\lambda=\dim\operatorname{Null}(A-\lambda I)",
            font_size=39,
            color=WHITE,
        )
        inequality = MathTex(r"1\leq \text{geometric multiplicity}\leq \text{algebraic multiplicity}", font_size=41, color=YELLOW)
        examples = MathTex(
            r"A_1:\ 2=2\qquad\qquad A_2:\ 1<2",
            font_size=48,
            color=GREEN_C,
        )
        card = self._fit(VGroup(algebraic, geometric, inequality, examples).arrange(DOWN, buff=0.48), heading, gap=0.58)
        for item in card:
            self.play(FadeIn(item), run_time=0.5)
        self.wait(1.6)

        # Card 6 — diagonalizability criterion.
        heading = self._replace_heading(heading, "A matrix is diagonalizable exactly when its eigenspaces supply enough independent eigenvectors.")
        self.play(FadeOut(card))
        criterion1 = MathTex(r"\sum_{\lambda}\dim E_\lambda=n", font_size=58, color=YELLOW)
        or_text = Text("equivalently, for each eigenvalue", font_size=27, color=GREY_B)
        criterion2 = MathTex(
            r"\text{geometric multiplicity}=\text{algebraic multiplicity}",
            font_size=43,
            color=GREEN_C,
        )
        p_good = MathTex(r"P=[\mathbf v_1\ \mathbf v_2]\quad\text{invertible}", font_size=42, color=WHITE)
        p_bad = MathTex(r"\text{too few eigenvectors}\quad\Longrightarrow\quad\text{no invertible eigenvector matrix }P", font_size=37, color=RED_C)
        card = self._fit(VGroup(criterion1, or_text, criterion2, p_good, p_bad).arrange(DOWN, buff=0.39), heading, gap=0.47)
        for item in card:
            self.play(FadeIn(item), run_time=0.48)
        self.wait(1.7)

        # Card 7 — takeaway.
        heading = self._replace_heading(heading, "Repeated eigenvalues are not the problem; missing eigenvectors are.")
        self.play(FadeOut(card))
        root = MathTex(r"\text{Repeated root}\ \lambda", font_size=46, color=WHITE)
        arrow = MathTex(r"\Downarrow", font_size=45, color=GREY_B)
        question = MathTex(r"\text{How large is }E_\lambda\text{?}", font_size=50, color=YELLOW)
        good_end = MathTex(r"\dim E_\lambda=\text{algebraic multiplicity}\ \Longrightarrow\ \text{enough eigenvectors}", font_size=39, color=GREEN_C)
        bad_end = MathTex(r"\dim E_\lambda<\text{algebraic multiplicity}\ \Longrightarrow\ \text{not diagonalizable}", font_size=39, color=RED_C)
        card = self._fit(VGroup(root, arrow, question, good_end, bad_end).arrange(DOWN, buff=0.38), heading, gap=0.5)
        self.play(FadeIn(root), FadeIn(arrow), FadeIn(question))
        self.play(FadeIn(good_end))
        self.play(FadeIn(bad_end))
        self.wait(2.0)
