"""Manim presentation for Chapter 7 lesson 5: computing eigenvalues in a 3x3 example."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C,
    GREEN_C,
    GREY_B,
    RED_C,
    WHITE,
    YELLOW,
    Circumscribe,
    FadeIn,
    FadeOut,
    MathTex,
    ReplacementTransform,
    Scene,
    Text,
    TransformMatchingTex,
    VGroup,
)

from engine.computing_eigenvalues import DEFAULT_MATRIX, EigenvalueComputationLesson


DOWN = np.array([0.0, -1.0, 0.0])
UP = np.array([0.0, 1.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])


class ComputingEigenvaluesPresentation(Scene):
    """Work a complete 3x3 eigenvalue computation from start to finish."""

    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Computing Eigenvalues in a 3×3 Example"

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=29, color=WHITE)
        if item.width > 12.0:
            item.scale_to_fit_width(12.0)
        return item

    def _chrome(self, heading_text: str) -> tuple[Text, Text, Text]:
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD")
        banner.to_edge(UP, buff=0.18)
        title = Text(self.LESSON_TITLE, font_size=34, color=YELLOW, weight="BOLD")
        title.next_to(banner, DOWN, buff=0.16)
        heading = self._heading(heading_text)
        heading.next_to(title, DOWN, buff=0.28)
        return banner, title, heading

    def _replace_heading(self, old: Text, text: str) -> Text:
        new = self._heading(text)
        new.move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.55)
        return new

    def construct(self) -> None:
        EigenvalueComputationLesson(DEFAULT_MATRIX)
        banner, title, heading = self._chrome("Now carry the characteristic-equation method into 3×3.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.9)

        # Card 1 — present the 3x3 example.
        matrix = MathTex(
            r"A=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}",
            font_size=58,
            color=WHITE,
        )
        matrix.move_to(np.array([0.0, 0.15, 0.0]))
        note = Text("The zeros will let us compute the 3×3 determinant efficiently.", font_size=28, color=WHITE)
        note.next_to(matrix, DOWN, buff=0.72)
        self.play(FadeIn(matrix), FadeIn(note))
        self.wait(1.5)

        # Card 2 — build A-lambda I explicitly.
        heading = self._replace_heading(heading, "Subtract λ from all three diagonal entries.")
        a_matrix = MathTex(
            r"A=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}",
            font_size=38,
            color=WHITE,
        )
        lambda_i = MathTex(
            r"\lambda I=\begin{bmatrix}\lambda&0&0\\0&\lambda&0\\0&0&\lambda\end{bmatrix}",
            font_size=38,
            color=YELLOW,
        )
        top = VGroup(a_matrix, lambda_i).arrange(RIGHT, buff=1.0)
        top.move_to(np.array([0.0, 0.68, 0.0]))
        shifted = MathTex(
            r"A-\lambda I="
            r"\begin{bmatrix}4-\lambda&1&0\\2&3-\lambda&0\\0&0&1-\lambda\end{bmatrix}",
            font_size=47,
            color=GREEN_C,
        )
        shifted.next_to(top, DOWN, buff=0.70)
        diag_note = Text("Only the diagonal entries change.", font_size=27, color=WHITE)
        diag_note.to_edge(DOWN, buff=0.34)
        self.play(FadeOut(matrix), FadeOut(note), FadeIn(top))
        self.play(FadeIn(shifted), FadeIn(diag_note))
        self.play(Circumscribe(shifted, color=GREEN_C, fade_out=True), run_time=0.9)
        self.wait(1.4)

        # Card 3 — set up the 3x3 determinant.
        heading = self._replace_heading(heading, "Set det(A − λI)=0.")
        determinant = MathTex(
            r"\begin{vmatrix}"
            r"4-\lambda&1&0\\"
            r"2&3-\lambda&0\\"
            r"0&0&1-\lambda"
            r"\end{vmatrix}=0",
            font_size=54,
            color=WHITE,
        )
        determinant.move_to(np.array([0.0, 0.05, 0.0]))
        zero_note = Text("The third column has two zeros — expand there.", font_size=28, color=WHITE)
        zero_note.next_to(determinant, DOWN, buff=0.72)
        self.play(FadeOut(top), FadeOut(shifted), FadeOut(diag_note), FadeIn(determinant), FadeIn(zero_note))
        self.wait(1.4)

        # Card 4 — animate cofactor reduction to a 2x2 determinant.
        heading = self._replace_heading(heading, "Use the zero structure to reduce the 3×3 determinant.")
        cofactor = MathTex(
            r"(1-\lambda)"
            r"\begin{vmatrix}4-\lambda&1\\2&3-\lambda\end{vmatrix}=0",
            font_size=55,
            color=WHITE,
        )
        cofactor.move_to(np.array([0.0, 0.25, 0.0]))
        explanation = Text(
            "Only the (3,3) entry contributes in this cofactor expansion.",
            font_size=27,
            color=WHITE,
        )
        explanation.next_to(cofactor, DOWN, buff=0.70)
        self.play(FadeOut(zero_note))
        self.play(TransformMatchingTex(determinant, cofactor), run_time=1.1)
        self.play(FadeIn(explanation))
        self.wait(1.5)

        # Card 5 — compute the remaining 2x2 determinant with ad-bc.
        heading = self._replace_heading(heading, "Now compute the remaining 2×2 determinant with ad − bc.")
        rule = MathTex(r"\begin{vmatrix}a&b\\c&d\end{vmatrix}=ad-bc", font_size=39, color=GREY_B)
        rule.move_to(np.array([0.0, 0.85, 0.0]))
        first_product = MathTex(r"(4-\lambda)(3-\lambda)", font_size=46, color=GREEN_C)
        minus = MathTex(r"-", font_size=46, color=WHITE)
        second_product = MathTex(r"1\cdot2", font_size=46, color=RED_C)
        products = VGroup(first_product, minus, second_product).arrange(RIGHT, buff=0.30)
        products.next_to(rule, DOWN, buff=0.66)
        reduced = MathTex(
            r"(1-\lambda)\big((4-\lambda)(3-\lambda)-2\big)=0",
            font_size=47,
            color=YELLOW,
        )
        reduced.next_to(products, DOWN, buff=0.68)
        self.play(FadeOut(cofactor), FadeOut(explanation), FadeIn(rule))
        self.play(FadeIn(first_product), run_time=0.65)
        self.wait(0.25)
        self.play(FadeIn(minus), FadeIn(second_product), run_time=0.65)
        self.wait(0.35)
        self.play(FadeIn(reduced))
        self.wait(1.5)

        # Card 6 — simplify the quadratic factor.
        heading = self._replace_heading(heading, "Simplify the quadratic factor.")
        line1 = MathTex(
            r"(1-\lambda)\big((4-\lambda)(3-\lambda)-2\big)=0",
            font_size=45,
            color=WHITE,
        )
        line2 = MathTex(
            r"(1-\lambda)(12-7\lambda+\lambda^2-2)=0",
            font_size=44,
            color=WHITE,
        )
        line3 = MathTex(
            r"(1-\lambda)(\lambda^2-7\lambda+10)=0",
            font_size=49,
            color=YELLOW,
        )
        stack = VGroup(line1, line2, line3).arrange(DOWN, buff=0.62)
        stack.move_to(np.array([0.0, -0.05, 0.0]))
        self.play(FadeOut(rule), FadeOut(products), FadeOut(reduced), FadeIn(line1))
        self.play(TransformMatchingTex(line1.copy(), line2), run_time=0.85)
        self.wait(0.3)
        self.play(TransformMatchingTex(line2.copy(), line3), run_time=0.85)
        self.wait(1.5)

        # Card 7 — factor and solve all three roots.
        heading = self._replace_heading(heading, "Factor and read off all three eigenvalues.")
        start = MathTex(r"(1-\lambda)(\lambda^2-7\lambda+10)=0", font_size=48, color=WHITE)
        factored = MathTex(r"(1-\lambda)(\lambda-5)(\lambda-2)=0", font_size=53, color=YELLOW)
        roots = MathTex(
            r"\boxed{\lambda=1,\qquad \lambda=2,\qquad \lambda=5}",
            font_size=52,
            color=GREEN_C,
        )
        group = VGroup(start, factored, roots).arrange(DOWN, buff=0.72)
        group.move_to(np.array([0.0, -0.05, 0.0]))
        self.play(FadeOut(stack), FadeIn(start))
        self.play(TransformMatchingTex(start.copy(), factored), run_time=0.9)
        self.wait(0.4)
        self.play(FadeIn(roots))
        self.wait(1.7)

        # Card 8 — synthesis.
        heading = self._replace_heading(heading, "A 3×3 computation uses the same method — with more determinant structure.")
        step1 = Text("1. Form  A − λI", font_size=31, color=WHITE)
        step2 = Text("2. Compute  det(A − λI)", font_size=31, color=WHITE)
        step3 = Text("3. Use zeros or cofactors strategically", font_size=31, color=WHITE)
        step4 = Text("4. Factor and solve for λ", font_size=31, color=WHITE)
        steps = VGroup(step1, step2, step3, step4).arrange(DOWN, buff=0.48)
        steps.move_to(np.array([0.0, -0.05, 0.0]))
        final = MathTex(r"\boxed{\lambda=1,\ 2,\ 5}", font_size=52, color=YELLOW)
        final.next_to(steps, DOWN, buff=0.62)
        self.play(FadeOut(group), FadeIn(step1))
        self.play(FadeIn(step2))
        self.play(FadeIn(step3))
        self.play(FadeIn(step4))
        self.play(FadeIn(final))
        self.wait(2.0)
