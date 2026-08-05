"""CP124 presentation: pivoting and the factorization PA = LU."""

from __future__ import annotations

from math import log10

import numpy as np

from manim import (
    BLUE,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    MathTex,
    Matrix,
    RED,
    ReplacementTransform,
    RIGHT,
    Scene,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from engine.pivoting_pa_lu import PivotingPALU, PivotingStep


class PivotingPALUPresentation(Scene):
    """Show why pivoting changes A = LU into PA = LU."""

    TRANSITION = 2.20
    HIGHLIGHT = 1.35
    READ = 2.60
    HEADING_Y = 2.24
    EXPLANATION_FONT_SIZE = 21

    def construct(self) -> None:
        snapshot = PivotingPALU().snapshot()

        title = Text("Pivoting and PA = LU", font_size=42).to_edge(UP, buff=0.27)
        subtitle = Text(
            "Row exchanges rescue zero pivots and improve numerical stability.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.13)
        self._fit_down_only(subtitle, 11.2)
        self.play(Write(title), FadeIn(subtitle), run_time=2.4)

        heading = self._heading("A zero pivot stops ordinary elimination", 30)
        panel, coefficient_matrix = self._zero_pivot_panel(
            snapshot.coefficient_matrix,
            snapshot.determinant,
        )
        panel.move_to(DOWN * 0.56)
        self.play(FadeIn(heading), FadeIn(panel), run_time=self.TRANSITION)
        pivot_box = SurroundingRectangle(
            coefficient_matrix.get_entries()[0],
            color=RED,
            buff=0.12,
        )
        self.play(Create(pivot_box), run_time=self.HIGHLIGHT)
        self.wait(self.READ)

        prompt = VGroup(
            Text("Pause and Predict", font_size=25, color=YELLOW),
            Text("Which row should move to the top?", font_size=21),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.10)
        self.play(FadeIn(prompt), run_time=1.0)
        self.wait(1.9)
        self.play(FadeOut(prompt), FadeOut(pivot_box), run_time=0.90)

        swap_heading = self._heading("Swap rows before eliminating", 30)
        swap_panel = self._permutation_panel(
            snapshot.permutation_matrix,
            snapshot.coefficient_matrix,
            snapshot.permuted_matrix,
        ).move_to(DOWN * 0.55)
        self.play(
            ReplacementTransform(heading, swap_heading),
            ReplacementTransform(panel, swap_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = swap_heading, swap_panel
        self.wait(3.0)

        for step in snapshot.steps:
            step_heading = self._heading(
                "Now eliminate beneath the first pivot"
                if step.index == 1
                else "Eliminate beneath the second pivot",
                29,
            )
            step_panel, result_matrix = self._elimination_step_panel(step)
            step_panel.move_to(DOWN * 0.56)
            self.play(
                ReplacementTransform(heading, step_heading),
                ReplacementTransform(panel, step_panel),
                run_time=self.TRANSITION,
            )
            heading, panel = step_heading, step_panel
            row_box = SurroundingRectangle(
                result_matrix.get_rows()[step.target_row],
                color=BLUE,
                buff=0.10,
            )
            self.play(Create(row_box), run_time=self.HIGHLIGHT)
            self.wait(2.0)
            self.play(FadeOut(row_box), run_time=0.80)

        factor_heading = self._heading("Collect the elimination multipliers in L", 29)
        factor_panel = self._factorization_panel(
            snapshot.permuted_matrix,
            snapshot.lower_triangular,
            snapshot.upper_triangular,
            snapshot.factorization_tex,
        ).move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, factor_heading),
            ReplacementTransform(panel, factor_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = factor_heading, factor_panel
        self.wait(3.2)

        verify_heading = self._heading("Verify PA = LU and recover A", 30)
        verify_panel = self._verification_panel(
            snapshot.coefficient_matrix,
            snapshot.lower_triangular,
            snapshot.upper_triangular,
            snapshot.reconstruction_tex,
        ).move_to(DOWN * 0.53)
        self.play(
            ReplacementTransform(heading, verify_heading),
            ReplacementTransform(panel, verify_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = verify_heading, verify_panel
        self.wait(3.2)

        tiny_heading = self._heading("A tiny pivot is legal—but risky", 30)
        tiny_panel = self._tiny_pivot_panel(
            snapshot.tiny_epsilon,
            snapshot.multiplier_without_pivoting,
            snapshot.multiplier_with_pivoting,
            snapshot.no_swap_second_entry,
            snapshot.pivoted_second_entry,
        ).move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, tiny_heading),
            ReplacementTransform(panel, tiny_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = tiny_heading, tiny_panel
        self.wait(3.5)

        algorithm_heading = self._heading("Partial pivoting chooses the largest available magnitude", 27)
        algorithm_panel = self._partial_pivoting_panel(snapshot.partial_pivot_rule_tex)
        algorithm_panel.next_to(algorithm_heading, DOWN, buff=0.30)
        self.play(
            ReplacementTransform(heading, algorithm_heading),
            ReplacementTransform(panel, algorithm_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = algorithm_heading, algorithm_panel
        self.wait(3.3)

        summary_heading = self._heading("What pivoting changes—and what it preserves", 29)
        summary_panel = self._summary_panel().move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, summary_heading),
            ReplacementTransform(panel, summary_panel),
            run_time=self.TRANSITION,
        )
        self.wait(4.0)

    def _heading(self, text: str, font_size: int):
        heading = Text(text, font_size=font_size).move_to(UP * self.HEADING_Y)
        return self._fit_down_only(heading, 11.1)

    def _zero_pivot_panel(self, values, determinant: float):
        coefficient_matrix = self._matrix(values, scale=0.86)
        label = MathTex(r"A=", font_size=38, color=BLUE)
        matrix_row = VGroup(label, coefficient_matrix).arrange(RIGHT, buff=0.24)
        determinant_formula = MathTex(
            rf"\det(A)={self._format_number(determinant)}\ne0",
            font_size=35,
            color=GREEN,
        )
        obstruction = MathTex(
            r"m_{21}=\frac{a_{21}}{a_{11}}=\frac{2}{0}\quad\text{is undefined}",
            font_size=35,
            color=RED,
        )
        formula_row = VGroup(determinant_formula, obstruction).arrange(RIGHT, buff=0.62)
        self._fit_down_only(formula_row, 10.7)
        note = Text(
            "The matrix is invertible, but this row order gives no usable first pivot.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(matrix_row, formula_row, note).arrange(DOWN, buff=0.40)
        return self._boxed(group, color=RED), coefficient_matrix

    def _permutation_panel(self, p_values, a_values, pa_values):
        p_card = self._labeled_matrix(p_values, r"P", GREEN, scale=0.68)
        a_card = self._labeled_matrix(a_values, r"A", BLUE, scale=0.68)
        pa_card = self._labeled_matrix(pa_values, r"PA", YELLOW, scale=0.68)
        equation = VGroup(
            p_card,
            MathTex(r"\cdot", font_size=40),
            a_card,
            MathTex(r"=", font_size=40),
            pa_card,
        ).arrange(RIGHT, buff=0.22)
        operation = MathTex(r"R_1\leftrightarrow R_2", font_size=37, color=GREEN)
        note = Text(
            "Applied to the full augmented system, P performs the row exchange without changing its solutions.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        return self._boxed(VGroup(operation, equation, note).arrange(DOWN, buff=0.36))

    def _elimination_step_panel(self, step: PivotingStep):
        operation = MathTex(step.operation_tex, font_size=34, color=YELLOW)
        before = self._matrix(step.before_matrix, scale=0.72)
        after = self._matrix(step.after_matrix, scale=0.72)
        matrix_row = VGroup(
            before,
            MathTex(r"\longrightarrow", font_size=38),
            after,
        ).arrange(RIGHT, buff=0.40)
        explanation = Text(
            step.explanation,
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(explanation, 10.8)
        group = VGroup(operation, matrix_row, explanation).arrange(DOWN, buff=0.42)
        return self._boxed(group), after

    def _factorization_panel(self, pa_values, l_values, u_values, factorization_tex: str):
        formula = MathTex(factorization_tex, font_size=46, color=YELLOW)
        pa_card = self._labeled_matrix(pa_values, r"PA", BLUE, scale=0.66)
        l_card = self._labeled_matrix(l_values, r"L", GREEN, scale=0.66)
        u_card = self._labeled_matrix(u_values, r"U", YELLOW, scale=0.66)
        equality = VGroup(
            pa_card,
            MathTex(r"=", font_size=39),
            l_card,
            MathTex(r"\cdot", font_size=39),
            u_card,
        ).arrange(RIGHT, buff=0.20)
        multipliers = MathTex(
            r"L_{31}=m_{31}=2,\qquad L_{32}=m_{32}=-3",
            font_size=32,
            color=GREEN,
        )
        note = Text(
            "P records row exchanges, L records multipliers, and U records the echelon form.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(formula, equality, multipliers, note).arrange(DOWN, buff=0.33)
        return self._boxed(group)

    def _verification_panel(self, a_values, l_values, u_values, reconstruction_tex: str):
        left = VGroup(
            MathTex(r"LU=PA", font_size=41, color=GREEN),
            self._matrix(np.matmul(l_values, u_values), scale=0.74),
        ).arrange(DOWN, buff=0.20)
        right = VGroup(
            MathTex(reconstruction_tex, font_size=41, color=YELLOW),
            self._matrix(a_values, scale=0.74),
        ).arrange(DOWN, buff=0.20)
        cards = VGroup(self._boxed(left, color=GREEN), self._boxed(right)).arrange(
            RIGHT,
            buff=0.62,
            aligned_edge=UP,
        )
        permutation = MathTex(
            r"P^{-1}=P^T=P",
            font_size=35,
            color=BLUE,
        )
        note_line_1 = VGroup(
            Text(
                "Undo the row exchange with",
                font_size=self.EXPLANATION_FONT_SIZE,
                color=YELLOW,
            ),
            MathTex(r"P^T", font_size=30, color=YELLOW),
        ).arrange(RIGHT, buff=0.16)
        note_line_2 = VGroup(
            Text(
                "The original matrix is",
                font_size=self.EXPLANATION_FONT_SIZE,
                color=YELLOW,
            ),
            MathTex(r"A=P^TLU", font_size=31, color=YELLOW),
        ).arrange(RIGHT, buff=0.16)
        note = VGroup(note_line_1, note_line_2).arrange(DOWN, buff=0.12)
        self._fit_down_only(note, 10.8)
        return self._boxed(VGroup(cards, permutation, note).arrange(DOWN, buff=0.38))

    def _tiny_pivot_panel(
        self,
        epsilon: float,
        multiplier_without_pivoting: float,
        multiplier_with_pivoting: float,
        no_swap_second_entry: float,
        pivoted_second_entry: float,
    ):
        epsilon_power = int(round(-log10(epsilon)))
        large_power = int(round(log10(multiplier_without_pivoting)))
        matrix = MathTex(
            rf"\widetilde A=\begin{{bmatrix}}10^{{-{epsilon_power}}}&1\\1&1\end{{bmatrix}}",
            font_size=38,
            color=BLUE,
        )
        no_swap = VGroup(
            Text("Keep the tiny pivot", font_size=23, color=RED),
            MathTex(rf"m=10^{{{large_power}}}", font_size=34, color=RED),
            MathTex(
                rf"1-10^{{{large_power}}}={self._format_number(no_swap_second_entry)}",
                font_size=31,
            ),
            Text("large intermediate value", font_size=20, color=RED),
        ).arrange(DOWN, buff=0.22)
        with_swap = VGroup(
            Text("Use partial pivoting", font_size=23, color=GREEN),
            MathTex(rf"m=10^{{-{epsilon_power}}}", font_size=34, color=GREEN),
            MathTex(
                rf"1-10^{{-{epsilon_power}}}={pivoted_second_entry:.4f}",
                font_size=31,
            ),
            Text("moderate intermediate value", font_size=20, color=GREEN),
        ).arrange(DOWN, buff=0.22)
        cards = VGroup(
            self._boxed(no_swap, color=RED),
            self._boxed(with_swap, color=GREEN),
        ).arrange(RIGHT, buff=0.70, aligned_edge=UP)
        note = Text(
            "Large multipliers can magnify roundoff, even when the pivot is not exactly zero.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        return self._boxed(VGroup(matrix, cards, note).arrange(DOWN, buff=0.40))

    def _partial_pivoting_panel(self, rule_tex: str):
        rule = MathTex(rule_tex, font_size=37, color=YELLOW)
        steps = VGroup(
            self._algorithm_row("1", "In column k, find the largest magnitude at or below the pivot."),
            self._algorithm_row("2", "Swap that row into position k and record the exchange in P."),
            self._algorithm_row("3", "Eliminate below the pivot and store the multipliers in L."),
        ).arrange(DOWN, buff=0.27, aligned_edge=LEFT)
        caution = Text(
            "If later swaps occur, software also reorders the multipliers already stored in L.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(caution, 10.6)
        return self._boxed(VGroup(rule, steps, caution).arrange(DOWN, buff=0.38))

    def _summary_panel(self):
        cases = VGroup(
            VGroup(
                MathTex(r"a_{kk}=0", font_size=35, color=RED),
                Text("row swap required", font_size=22),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                MathTex(r"|a_{kk}|\ \text{very small}", font_size=34, color=YELLOW),
                Text("row swap usually safer", font_size=22),
            ).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=1.25)
        factorization = VGroup(
            MathTex(r"PA=LU", font_size=45, color=GREEN),
            MathTex(r"A=P^TLU", font_size=42, color=BLUE),
        ).arrange(RIGHT, buff=1.20)
        preserved = Text(
            "Pivoting reorders equations; it does not change the solutions of the system.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(preserved, 10.8)
        group = VGroup(cases, factorization, preserved).arrange(DOWN, buff=0.50)
        return self._boxed(group)

    def _algorithm_row(self, number: str, text: str):
        badge = MathTex(number, font_size=29, color=YELLOW)
        sentence = Text(text, font_size=self.EXPLANATION_FONT_SIZE)
        self._fit_down_only(sentence, 9.8)
        return VGroup(badge, sentence).arrange(RIGHT, buff=0.28)

    def _labeled_matrix(self, values, label: str, color, *, scale: float):
        matrix = self._matrix(values, scale=scale)
        label_mobject = MathTex(label, font_size=29, color=color)
        return VGroup(label_mobject, matrix).arrange(DOWN, buff=0.10)

    def _matrix(self, values, *, scale: float = 1.0):
        formatted = [[self._format_number(value) for value in row] for row in values]
        return Matrix(formatted, h_buff=0.80, v_buff=0.72).scale(scale)

    @staticmethod
    def _boxed(group, *, color=YELLOW, buff=0.20):
        return VGroup(SurroundingRectangle(group, color=color, buff=buff), group)

    @staticmethod
    def _fit_down_only(mobject, max_width: float):
        if mobject.width > max_width:
            mobject.scale_to_fit_width(max_width)
        return mobject

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"

