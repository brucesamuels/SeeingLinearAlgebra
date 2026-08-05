"""CP121 presentation: multiple right-hand sides and reusable elimination."""

from __future__ import annotations

import numpy as np

from manim import (
    BLUE,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    Line,
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

from engine.multiple_right_hand_sides import BlockEliminationStep, MultipleRightHandSides


class MultipleRightHandSidesPresentation(Scene):
    """Solve AX=B and compare repeated elimination with reusable LU."""

    TRANSITION = 2.25
    HIGHLIGHT = 1.45
    READ = 2.45
    HEADING_Y = 2.22
    EXPLANATION_FONT_SIZE = 21

    def construct(self) -> None:
        snapshot = MultipleRightHandSides().snapshot()
        counts = snapshot.operation_counts

        title = Text("Multiple Right-Hand Sides", font_size=41).to_edge(UP, buff=0.27)
        subtitle = Text(
            "Factor the coefficient matrix once, then reuse the work.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.13)
        subtitle.scale_to_fit_width(11.3)
        self.play(Write(title), FadeIn(subtitle), run_time=2.4)

        heading = self._heading("Several systems share the same coefficient matrix", 28)
        panel = self._separate_systems_panel(snapshot.coefficient_matrix, snapshot.right_hand_sides).move_to(DOWN * 0.50)
        self.play(FadeIn(heading), FadeIn(panel), run_time=self.TRANSITION)
        self.wait(2.8)

        next_heading = self._heading("Place all right-hand sides into one matrix", 29)
        next_panel = self._block_system_panel(
            snapshot.coefficient_matrix,
            snapshot.right_hand_sides,
            snapshot.solution_matrix,
        ).move_to(DOWN * 0.52)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(self.READ)

        next_heading = self._heading("Repeated reduction recomputes the same elimination", 27)
        next_panel = self._repeated_reduction_panel(counts.right_hand_sides).move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.8)

        next_heading = self._heading("One block reduction updates every right-hand side", 27)
        first_step = snapshot.block_elimination_steps[0]
        next_panel, block_matrix = self._block_step_panel(first_step, initial=True)
        next_panel.move_to(DOWN * 0.58)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        target_box = SurroundingRectangle(block_matrix.get_rows()[first_step.target_row], color=YELLOW, buff=0.08)
        self.play(Create(target_box), run_time=self.HIGHLIGHT)
        self.wait(1.2)

        for step in snapshot.block_elimination_steps[1:]:
            step_heading = self._heading(f"Apply elimination step {step.index} across the entire block", 27)
            step_panel, block_matrix = self._block_step_panel(step, initial=False)
            step_panel.move_to(DOWN * 0.58)
            self.play(
                FadeOut(target_box),
                ReplacementTransform(heading, step_heading),
                ReplacementTransform(panel, step_panel),
                run_time=self.TRANSITION,
            )
            heading, panel = step_heading, step_panel
            target_box = SurroundingRectangle(block_matrix.get_rows()[step.target_row], color=YELLOW, buff=0.08)
            self.play(Create(target_box), run_time=self.HIGHLIGHT)
            self.wait(1.25)
        self.play(FadeOut(target_box), run_time=0.90)

        next_heading = self._heading("The reduced block contains U and two transformed columns", 26)
        next_panel = self._reduced_block_panel(snapshot.upper_triangular_matrix, snapshot.intermediate_matrix).move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.7)

        next_heading = self._heading("Back substitution solves both columns together", 28)
        next_panel = self._back_substitution_panel(
            snapshot.upper_triangular_matrix,
            snapshot.solution_matrix,
            snapshot.intermediate_matrix,
        ).move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.8)

        next_heading = self._heading("LU stores the elimination for reuse", 29)
        next_panel = self._lu_reuse_panel(
            snapshot.lower_triangular_matrix,
            snapshot.upper_triangular_matrix,
            snapshot.right_hand_sides,
            snapshot.intermediate_matrix,
            snapshot.solution_matrix,
        ).move_to(DOWN * 0.58)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = self._heading("Exact count for this 3 by 3 example", 29)
        next_panel = self._exact_count_panel(counts).move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = self._heading("For m right-hand sides, the cubic work should occur once", 25)
        next_panel = self._asymptotic_count_panel().move_to(DOWN * 0.56)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.1)

        next_heading = self._heading("Block reduction and LU reuse perform the same arithmetic", 25)
        next_panel = self._block_vs_lu_panel().move_to(DOWN * 0.56)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = self._heading("Verify every solution column at once", 29)
        next_panel = self._verification_panel(
            snapshot.coefficient_matrix,
            snapshot.solution_matrix,
            snapshot.right_hand_sides,
        ).move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.8)

        next_heading = self._heading("One factorization, many solutions", 30)
        next_panel = self._summary_panel().move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        self.wait(3.5)

    def _heading(self, text: str, font_size: int) -> Text:
        heading = Text(text, font_size=font_size).move_to(UP * self.HEADING_Y)
        return self._fit_down_only(heading, 11.0)

    def _separate_systems_panel(self, a, b):
        cards = VGroup()
        for column in range(b.shape[1]):
            equation = MathTex(rf"A\mathbf{{x}}_{column + 1}=\mathbf{{b}}_{column + 1}", font_size=34, color=YELLOW)
            augmented, _ = self._augmented_matrix(a, b[:, column])
            card_group = VGroup(equation, augmented).arrange(DOWN, buff=0.28)
            card = VGroup(SurroundingRectangle(card_group, color=YELLOW, buff=0.16), card_group)
            cards.add(card)
        cards.arrange(RIGHT, buff=0.70)
        note = Text(
            "The matrix A is identical, but independent reduction repeats its elimination.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(cards, note).arrange(DOWN, buff=0.42)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _block_system_panel(self, a, b, x):
        a_m = self._matrix(a, scale=0.78)
        x_m = self._matrix(x, scale=0.78)
        b_m = self._matrix(b, scale=0.78)
        equation = VGroup(
            self._labeled_matrix("A", a_m, YELLOW),
            MathTex(r"\cdot", font_size=38),
            self._labeled_matrix("X", x_m, BLUE),
            MathTex(r"=", font_size=38),
            self._labeled_matrix("B", b_m, GREEN),
        ).arrange(RIGHT, buff=0.28)
        columns = MathTex(
            r"X=\begin{bmatrix}\mathbf{x}_1&\mathbf{x}_2\end{bmatrix},\qquad "
            r"B=\begin{bmatrix}\mathbf{b}_1&\mathbf{b}_2\end{bmatrix}",
            font_size=31,
            color=YELLOW,
        )
        note = Text(
            "One matrix equation represents both systems simultaneously.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(equation, columns, note).arrange(DOWN, buff=0.34)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _repeated_reduction_panel(self, m: int):
        left = VGroup(
            Text("System 1", font_size=23, color=BLUE),
            MathTex(r"[A\mid\mathbf b_1]\longrightarrow[U\mid\mathbf y_1]", font_size=32),
            MathTex(r"3\text{ elimination steps}", font_size=27, color=YELLOW),
        ).arrange(DOWN, buff=0.26)
        right = VGroup(
            Text("System 2", font_size=23, color=GREEN),
            MathTex(r"[A\mid\mathbf b_2]\longrightarrow[U\mid\mathbf y_2]", font_size=32),
            MathTex(r"3\text{ elimination steps}", font_size=27, color=YELLOW),
        ).arrange(DOWN, buff=0.26)
        cards = VGroup(
            VGroup(SurroundingRectangle(left, color=BLUE, buff=0.16), left),
            VGroup(SurroundingRectangle(right, color=GREEN, buff=0.16), right),
        ).arrange(RIGHT, buff=0.70)
        total = MathTex(r"3+3=6\text{ coefficient-matrix elimination steps}", font_size=31, color=RED)
        note = Text(
            "The pivots and multipliers are recomputed even though A has not changed.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(cards, total, note).arrange(DOWN, buff=0.38)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _block_step_panel(self, step: BlockEliminationStep, *, initial: bool):
        before_matrix, before_display = self._block_matrix(step.before_block)
        after_matrix, after_display = self._block_matrix(step.after_block)
        operation = MathTex(step.operation_tex, font_size=34, color=YELLOW)
        arrow = MathTex(r"\longrightarrow", font_size=42, color=YELLOW)
        matrices = VGroup(before_display, arrow, after_display).arrange(RIGHT, buff=0.34)
        labels = VGroup(
            Text("before", font_size=20, color=BLUE).next_to(before_display, UP, buff=0.10),
            Text("after", font_size=20, color=GREEN).next_to(after_display, UP, buff=0.10),
        )
        note = Text(
            "The same row operation updates A and every column of B.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(operation, VGroup(matrices, labels), note).arrange(DOWN, buff=0.34)
        panel = VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)
        return panel, after_matrix

    def _reduced_block_panel(self, u, y):
        block = np.hstack([u, y])
        matrix, display = self._block_matrix(block, scale=0.90)
        labels = VGroup(
            MathTex(r"U", font_size=29, color=BLUE),
            MathTex(r"Y", font_size=29, color=GREEN),
        )
        labels[0].move_to([matrix.get_columns()[1].get_center()[0], matrix.get_top()[1] + 0.26, 0])
        labels[1].move_to([matrix.get_columns()[3].get_center()[0], matrix.get_top()[1] + 0.26, 0])
        formula = MathTex(r"[A\mid B]\longrightarrow[U\mid Y]", font_size=38, color=YELLOW)
        note = Text(
            "Elimination is complete once; only triangular solution work remains.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(formula, VGroup(display, labels), note).arrange(DOWN, buff=0.35)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _back_substitution_panel(self, u, x, y):
        equation = self._matrix_equation("U", u, "X", x, "Y", y)
        rows = VGroup(
            MathTex(r"x_{31}=1,\qquad x_{32}=-1", font_size=31, color=GREEN),
            MathTex(r"x_{21}=0,\qquad x_{22}=1", font_size=31, color=BLUE),
            MathTex(r"x_{11}=1,\qquad x_{12}=0", font_size=31, color=YELLOW),
        ).arrange(DOWN, buff=0.22)
        note = Text(
            "Each triangular row solves all right-hand-side columns before moving upward.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(equation, rows, note).arrange(DOWN, buff=0.34)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _lu_reuse_panel(self, l, u, b, y, x):
        top = MathTex(r"A=LU", font_size=40, color=YELLOW)
        first = self._compact_equation("L", l, "Y", y, "B", b)
        second = self._compact_equation("U", u, "X", x, "Y", y)
        labels = VGroup(
            Text("forward substitution", font_size=20, color=GREEN),
            Text("back substitution", font_size=20, color=BLUE),
        ).arrange(RIGHT, buff=2.2)
        note = Text(
            "A future right-hand side reuses L and U; no new factorization is required.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(top, first, second, labels, note).arrange(DOWN, buff=0.27)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _exact_count_panel(self, counts):
        convention = Text(
            "Count each scalar addition, subtraction, multiplication, or division as one operation.",
            font_size=20,
            color=YELLOW,
        )
        self._fit_down_only(convention, 10.9)
        components = VGroup(
            MathTex(r"\text{factor }A:\ 13", font_size=31),
            MathTex(r"\text{forward solve per column}:\ 6", font_size=31),
            MathTex(r"\text{back solve per column}:\ 9", font_size=31),
            MathTex(r"\text{total triangular work per column}:\ 15", font_size=31, color=YELLOW),
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        comparison = VGroup(
            MathTex(r"\text{two independent reductions}:\ 2(13+15)=56", font_size=32, color=RED),
            MathTex(r"\text{factor once, solve twice}:\ 13+2(15)=43", font_size=32, color=GREEN),
            MathTex(r"\text{savings}:\ 56-43=13", font_size=34, color=YELLOW),
        ).arrange(DOWN, buff=0.24)
        group = VGroup(convention, components, comparison).arrange(DOWN, buff=0.34)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _asymptotic_count_panel(self):
        repeated = VGroup(
            Text("Repeat elimination m times", font_size=22, color=RED),
            MathTex(r"m\left(\frac{2}{3}n^3+2n^2\right)", font_size=40, color=RED),
        ).arrange(DOWN, buff=0.22)
        reused = VGroup(
            Text("Factor once, solve m times", font_size=22, color=GREEN),
            MathTex(r"\frac{2}{3}n^3+2mn^2", font_size=40, color=GREEN),
        ).arrange(DOWN, buff=0.22)
        cards = VGroup(
            VGroup(SurroundingRectangle(repeated, color=RED, buff=0.18), repeated),
            VGroup(SurroundingRectangle(reused, color=GREEN, buff=0.18), reused),
        ).arrange(RIGHT, buff=0.75)
        saving = MathTex(r"\text{savings}\approx(m-1)\frac{2}{3}n^3", font_size=38, color=YELLOW)
        note = Text(
            "The work on the right-hand sides grows with m; the cubic elimination work does not.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(cards, saving, note).arrange(DOWN, buff=0.38)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _block_vs_lu_panel(self):
        block = VGroup(
            Text("All columns known now", font_size=22, color=BLUE),
            MathTex(r"[A\mid B]\longrightarrow[U\mid Y]", font_size=34),
            Text("one block elimination", font_size=20),
        ).arrange(DOWN, buff=0.24)
        lu = VGroup(
            Text("Columns may arrive later", font_size=22, color=GREEN),
            MathTex(r"A=LU,\quad LY=B,\quad UX=Y", font_size=34),
            Text("stored reusable factors", font_size=20),
        ).arrange(DOWN, buff=0.24)
        cards = VGroup(
            VGroup(SurroundingRectangle(block, color=BLUE, buff=0.17), block),
            VGroup(SurroundingRectangle(lu, color=GREEN, buff=0.17), lu),
        ).arrange(RIGHT, buff=0.70)
        same = MathTex(r"\text{same arithmetic count when all right-hand sides are known}", font_size=31, color=YELLOW)
        distinction = Text(
            "LU is reusable: each future column needs only forward and back substitution.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(distinction, 10.8)
        group = VGroup(cards, same, distinction).arrange(DOWN, buff=0.38)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _verification_panel(self, a, x, b):
        equation = self._matrix_equation("A", a, "X", x, "B", b)
        columns = VGroup(
            MathTex(r"A\mathbf{x}_1=\mathbf{b}_1", font_size=34, color=BLUE),
            MathTex(r"A\mathbf{x}_2=\mathbf{b}_2", font_size=34, color=GREEN),
        ).arrange(RIGHT, buff=1.3)
        conclusion = Text(
            "Matrix multiplication verifies both systems in one calculation.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        group = VGroup(equation, columns, conclusion).arrange(DOWN, buff=0.38)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _summary_panel(self):
        formula = MathTex(r"AX=B,\qquad A=LU,\qquad LY=B,\qquad UX=Y", font_size=39, color=YELLOW)
        steps = VGroup(
            Text("1. Factor A once.", font_size=24),
            Text("2. Apply forward substitution to every column of B.", font_size=24),
            Text("3. Apply back substitution to every column of Y.", font_size=24),
            Text("4. Reuse L and U whenever a new right-hand side arrives.", font_size=24),
        ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        conclusion = Text(
            "The number of solves grows with the number of columns; the factorization does not.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(conclusion, 10.8)
        group = VGroup(formula, steps, conclusion).arrange(DOWN, buff=0.38)
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=0.18), group)

    def _matrix_equation(self, left_name, left, middle_name, middle, right_name, right):
        return VGroup(
            self._labeled_matrix(left_name, self._matrix(left, scale=0.68), YELLOW),
            MathTex(r"\cdot", font_size=35),
            self._labeled_matrix(middle_name, self._matrix(middle, scale=0.68), BLUE),
            MathTex(r"=", font_size=35),
            self._labeled_matrix(right_name, self._matrix(right, scale=0.68), GREEN),
        ).arrange(RIGHT, buff=0.24)

    def _compact_equation(self, left_name, left, middle_name, middle, right_name, right):
        return VGroup(
            self._labeled_matrix(left_name, self._matrix(left, scale=0.48), YELLOW, label_size=21),
            MathTex(r"\cdot", font_size=28),
            self._labeled_matrix(middle_name, self._matrix(middle, scale=0.48), BLUE, label_size=21),
            MathTex(r"=", font_size=28),
            self._labeled_matrix(right_name, self._matrix(right, scale=0.48), GREEN, label_size=21),
        ).arrange(RIGHT, buff=0.20)

    def _labeled_matrix(self, label, matrix, color, *, label_size=25):
        name = MathTex(label, font_size=label_size, color=color)
        return VGroup(name, matrix).arrange(DOWN, buff=0.10)

    def _augmented_matrix(self, a, b):
        values = np.column_stack([a, b])
        matrix = self._matrix(values, scale=0.68)
        separator = self._separator(matrix, 3)
        return VGroup(matrix, separator), matrix

    def _block_matrix(self, values, *, scale=0.76):
        matrix = self._matrix(values, scale=scale)
        separator = self._separator(matrix, 3)
        return matrix, VGroup(matrix, separator)

    @staticmethod
    def _separator(matrix: Matrix, split_after: int):
        columns = matrix.get_columns()
        x = (columns[split_after - 1].get_right()[0] + columns[split_after].get_left()[0]) / 2
        return Line(UP * matrix.height * 0.48, DOWN * matrix.height * 0.48, stroke_width=2).move_to(
            [x, matrix.get_center()[1], 0]
        )

    def _matrix(self, values, *, scale=0.78):
        formatted = [[self._format_number(value) for value in row] for row in values]
        return Matrix(formatted, h_buff=0.72, v_buff=0.68).scale(scale)

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
