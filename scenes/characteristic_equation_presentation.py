"""Manim presentation for Chapter 7 lesson 4: why the characteristic equation appears."""
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
    Indicate,
    MathTex,
    ReplacementTransform,
    Scene,
    Text,
    TransformMatchingTex,
    VGroup,
)

from engine.characteristic_equation import CharacteristicEquationLesson, DEFAULT_MATRIX


DOWN = np.array([0.0, -1.0, 0.0])
UP = np.array([0.0, 1.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])
LEFT = np.array([-1.0, 0.0, 0.0])


class CharacteristicEquationPresentation(Scene):
    """Derive det(A-lambda I)=0 algebraically, then compute a 2x2 example."""

    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Why the Characteristic Equation Appears"

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
        lesson = CharacteristicEquationLesson(DEFAULT_MATRIX)
        banner, title, heading = self._chrome("Start with the definition of an eigenvalue and eigenvector.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.9)

        # Card 1 — definition.
        definition = MathTex(
            r"A\mathbf v=\lambda\mathbf v,\qquad \mathbf v\neq\mathbf 0",
            font_size=58,
            color=WHITE,
        )
        definition.move_to(np.array([0.0, -0.25, 0.0]))
        definition.set_color_by_tex(r"\lambda", YELLOW)
        definition.set_color_by_tex(r"\mathbf v", BLUE_C)
        definition_note = Text(
            "We want to solve for the values of λ that allow a nonzero vector v.",
            font_size=27,
            color=WHITE,
        )
        definition_note.next_to(definition, DOWN, buff=0.72)
        definition_note.scale_to_fit_width(10.4)
        self.play(FadeIn(definition), FadeIn(definition_note))
        self.wait(1.5)

        # Card 2 — identity matrix makes matrix subtraction legitimate.
        heading = self._replace_heading(heading, "Use the identity matrix so both sides contain a matrix acting on v.")
        identity_fact = MathTex(r"I\mathbf v=\mathbf v", font_size=45, color=GREEN_C)
        identity_fact.move_to(np.array([0.0, 0.65, 0.0]))
        identity_matrix = MathTex(r"I=\begin{bmatrix}1&0\\0&1\end{bmatrix}", font_size=42, color=GREEN_C)
        identity_matrix.next_to(identity_fact, DOWN, buff=0.42)
        identity_matrix.set_x(identity_fact.get_center()[0])
        with_identity = MathTex(r"A\mathbf v=\lambda I\mathbf v", font_size=58, color=WHITE)
        with_identity.next_to(identity_matrix, DOWN, buff=0.62)
        with_identity.set_x(identity_fact.get_center()[0])
        with_identity.set_color_by_tex(r"\lambda I", YELLOW)
        with_identity.set_color_by_tex(r"\mathbf v", BLUE_C)
        identity_note = Text(
            "Because Iv = v, inserting I changes nothing — but now A and λI can be subtracted.",
            font_size=26,
            color=WHITE,
        )
        identity_note.to_edge(DOWN, buff=0.34)
        identity_note.scale_to_fit_width(11.1)
        self.play(FadeOut(definition_note), ReplacementTransform(definition, with_identity), FadeIn(identity_fact), FadeIn(identity_matrix))
        self.play(FadeIn(identity_note))
        self.wait(1.7)

        # Card 3 — move to one side and factor v.
        heading = self._replace_heading(heading, "Bring the matrix terms to one side, then factor out v.")
        subtract_line = MathTex(r"A\mathbf v-\lambda I\mathbf v=\mathbf 0", font_size=54, color=WHITE)
        subtract_line.move_to(np.array([0.0, 0.42, 0.0]))
        subtract_line.set_color_by_tex(r"\mathbf v", BLUE_C)
        subtract_line.set_color_by_tex(r"\lambda I", YELLOW)
        factored_line = MathTex(r"(A-\lambda I)\mathbf v=\mathbf 0", font_size=59, color=WHITE)
        factored_line.next_to(subtract_line, DOWN, buff=0.78)
        factored_line.set_color_by_tex(r"A-\lambda I", YELLOW)
        factored_line.set_color_by_tex(r"\mathbf v", BLUE_C)
        factor_note = Text("The common factor is the vector v.", font_size=27, color=WHITE)
        factor_note.next_to(factored_line, DOWN, buff=0.60)
        self.play(FadeOut(identity_fact), FadeOut(identity_matrix), FadeOut(identity_note), ReplacementTransform(with_identity, subtract_line))
        self.wait(0.7)
        self.play(FadeIn(factored_line), FadeIn(factor_note))
        self.play(Indicate(subtract_line, color=BLUE_C), Indicate(factored_line, color=BLUE_C), run_time=0.9)
        self.wait(1.6)

        # Card 4 — nonzero solution -> singular -> determinant zero.
        heading = self._replace_heading(heading, "A nonzero solution exists only if A − λI is singular.")
        nonzero = MathTex(r"(A-\lambda I)\mathbf v=\mathbf 0,\qquad \mathbf v\neq\mathbf 0", font_size=46, color=WHITE)
        singular = MathTex(r"A-\lambda I\ \text{is singular}", font_size=49, color=WHITE)
        determinant_condition = MathTex(r"\boxed{\det(A-\lambda I)=0}", font_size=56, color=YELLOW)
        logic = VGroup(nonzero, singular, determinant_condition).arrange(DOWN, buff=0.58)
        logic.move_to(np.array([0.0, -0.20, 0.0]))
        arrow1 = MathTex(r"\Downarrow", font_size=38, color=GREY_B)
        arrow2 = MathTex(r"\Downarrow", font_size=38, color=GREY_B)
        arrow1.move_to(0.5 * (nonzero.get_bottom() + singular.get_top()))
        arrow2.move_to(0.5 * (singular.get_bottom() + determinant_condition.get_top()))
        characteristic_note = Text("This is the characteristic equation.", font_size=29, color=WHITE)
        characteristic_note.to_edge(DOWN, buff=0.34)
        self.play(FadeOut(subtract_line), FadeOut(factored_line), FadeOut(factor_note), FadeIn(nonzero))
        self.wait(0.55)
        self.play(FadeIn(arrow1), FadeIn(singular))
        self.wait(0.55)
        self.play(FadeIn(arrow2), FadeIn(determinant_condition))
        self.play(FadeIn(characteristic_note))
        self.wait(1.8)

        # Card 5 — build A-lambda I entry by entry.
        heading = self._replace_heading(heading, "Now build A − λI for our familiar 2×2 matrix.")
        matrix_a = MathTex(r"A=\begin{bmatrix}5&3\\3&5\end{bmatrix}", font_size=44, color=WHITE)
        lambda_i = MathTex(r"\lambda I=\begin{bmatrix}\lambda&0\\0&\lambda\end{bmatrix}", font_size=44, color=YELLOW)
        pair = VGroup(matrix_a, lambda_i).arrange(RIGHT, buff=1.35)
        pair.move_to(np.array([0.0, 0.52, 0.0]))
        subtraction = MathTex(
            r"A-\lambda I="
            r"\begin{bmatrix}5&3\\3&5\end{bmatrix}"
            r"-\begin{bmatrix}\lambda&0\\0&\lambda\end{bmatrix}",
            font_size=40,
            color=WHITE,
        )
        subtraction.next_to(pair, DOWN, buff=0.62)
        shifted = MathTex(
            r"A-\lambda I=\begin{bmatrix}5-\lambda&3\\3&5-\lambda\end{bmatrix}",
            font_size=45,
            color=GREEN_C,
        )
        shifted.next_to(subtraction, DOWN, buff=0.62)
        subtraction_note = Text("Only the diagonal entries change, because λI has zeros off the diagonal.", font_size=26, color=WHITE)
        subtraction_note.to_edge(DOWN, buff=0.32)
        subtraction_note.scale_to_fit_width(10.8)
        self.play(FadeOut(nonzero), FadeOut(singular), FadeOut(determinant_condition), FadeOut(arrow1), FadeOut(arrow2), FadeOut(characteristic_note), FadeIn(pair))
        self.wait(0.6)
        self.play(FadeIn(subtraction))
        self.wait(0.7)
        self.play(FadeIn(shifted), FadeIn(subtraction_note))
        self.play(Circumscribe(shifted, color=GREEN_C, fade_out=True), run_time=0.9)
        self.wait(1.6)

        # Card 6 — explicitly animate the 2x2 determinant rule ad-bc.
        heading = self._replace_heading(heading, "Compute the 2×2 determinant with the familiar rule ad − bc.")
        determinant_matrix = MathTex(
            r"\det(A-\lambda I)="
            r"\begin{vmatrix}5-\lambda&3\\3&5-\lambda\end{vmatrix}",
            font_size=47,
            color=WHITE,
        )
        determinant_matrix.move_to(np.array([0.0, 0.72, 0.0]))
        rule = MathTex(r"\begin{vmatrix}a&b\\c&d\end{vmatrix}=ad-bc", font_size=39, color=GREY_B)
        rule.next_to(determinant_matrix, DOWN, buff=0.54)
        first_product = MathTex(r"(5-\lambda)(5-\lambda)", font_size=45, color=GREEN_C)
        minus = MathTex(r"-", font_size=45, color=WHITE)
        second_product = MathTex(r"3\cdot3", font_size=45, color=RED_C)
        products = VGroup(first_product, minus, second_product).arrange(RIGHT, buff=0.32)
        products.next_to(rule, DOWN, buff=0.66)
        compact = MathTex(r"(5-\lambda)^2-9", font_size=50, color=YELLOW)
        compact.next_to(products, DOWN, buff=0.56)
        determinant_note = Text("Multiply the main diagonal, then subtract the other diagonal product.", font_size=26, color=WHITE)
        determinant_note.to_edge(DOWN, buff=0.30)
        determinant_note.scale_to_fit_width(10.8)
        self.play(FadeOut(pair), FadeOut(subtraction), FadeOut(shifted), FadeOut(subtraction_note), FadeIn(determinant_matrix), FadeIn(rule))
        self.wait(0.55)
        self.play(FadeIn(first_product), Indicate(determinant_matrix, color=GREEN_C), run_time=0.85)
        self.wait(0.35)
        self.play(FadeIn(minus), FadeIn(second_product), Indicate(determinant_matrix, color=RED_C), run_time=0.85)
        self.play(FadeIn(determinant_note))
        self.wait(0.6)
        self.play(ReplacementTransform(products, compact))
        self.wait(1.5)

        # Card 7 — expand, factor, solve.
        heading = self._replace_heading(heading, "Set the determinant equal to zero and solve for λ.")
        start = MathTex(r"(5-\lambda)^2-9=0", font_size=49, color=WHITE)
        expanded = MathTex(r"25-10\lambda+\lambda^2-9=0", font_size=47, color=WHITE)
        simplified = MathTex(r"\lambda^2-10\lambda+16=0", font_size=49, color=WHITE)
        factored = MathTex(r"(\lambda-2)(\lambda-8)=0", font_size=51, color=YELLOW)
        roots = MathTex(r"\boxed{\lambda=2\qquad\text{or}\qquad\lambda=8}", font_size=53, color=GREEN_C)
        solve_stack = VGroup(start, expanded, simplified, factored, roots).arrange(DOWN, buff=0.39)
        solve_stack.move_to(np.array([0.0, -0.18, 0.0]))
        self.play(FadeOut(determinant_matrix), FadeOut(rule), FadeOut(compact), FadeOut(determinant_note), FadeIn(start))
        self.play(TransformMatchingTex(start.copy(), expanded), run_time=0.8)
        self.wait(0.3)
        self.play(TransformMatchingTex(expanded.copy(), simplified), run_time=0.8)
        self.wait(0.3)
        self.play(TransformMatchingTex(simplified.copy(), factored), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(roots))
        self.wait(1.8)

        # Card 8 — synthesis.
        heading = self._replace_heading(heading, "The characteristic equation is the bridge from the definition to computation.")
        summary1 = MathTex(r"A\mathbf v=\lambda\mathbf v", font_size=48, color=WHITE)
        summary2 = MathTex(r"(A-\lambda I)\mathbf v=\mathbf 0", font_size=48, color=WHITE)
        summary3 = MathTex(r"\det(A-\lambda I)=0", font_size=52, color=YELLOW)
        summary4 = Text("Solve this equation to find the eigenvalues.", font_size=29, color=WHITE)
        summary = VGroup(summary1, summary2, summary3, summary4).arrange(DOWN, buff=0.55)
        summary.move_to(np.array([0.0, -0.18, 0.0]))
        self.play(FadeOut(solve_stack), FadeIn(summary1))
        self.play(FadeIn(summary2))
        self.play(FadeIn(summary3))
        self.play(FadeIn(summary4))
        self.wait(2.3)
