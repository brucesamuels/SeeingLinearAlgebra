"""CP122 presentation: inverse by Gauss-Jordan elimination."""

from __future__ import annotations

from fractions import Fraction

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

from engine.gauss_jordan_inverse import GaussJordanInverse, GaussJordanStep


class GaussJordanInversePresentation(Scene):
    """Interpret [A | I] -> [I | A^{-1}] as a multiple-RHS solve."""

    TRANSITION = 2.20
    HIGHLIGHT = 1.35
    READ = 2.55
    HEADING_Y = 2.24
    EXPLANATION_FONT_SIZE = 21

    def construct(self) -> None:
        snapshot = GaussJordanInverse().snapshot()

        title = Text("Inverse by Gauss-Jordan Elimination", font_size=40).to_edge(UP, buff=0.27)
        subtitle = Text(
            "Solve three unit-vector systems at the same time.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.13)
        subtitle.scale_to_fit_width(11.2)
        self.play(Write(title), FadeIn(subtitle), run_time=2.4)

        heading = self._heading("The inverse solves three systems at once", 29)
        panel = self._multiple_rhs_panel().move_to(DOWN * 0.52)
        self.play(FadeIn(heading), FadeIn(panel), run_time=self.TRANSITION)
        self.wait(2.9)

        next_heading = self._heading("Place the identity matrix beside A", 29)
        next_panel, block_matrix = self._initial_block_panel(snapshot.augmented_start)
        next_panel.move_to(DOWN * 0.56)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(self.READ)

        prompt = VGroup(
            Text("Pause and Predict", font_size=25, color=YELLOW),
            Text("What must happen to the right side while A becomes I?", font_size=21),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(prompt), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(prompt), run_time=0.85)

        first_step = snapshot.steps[0]
        next_heading = self._heading("Apply every row operation across all six columns", 26)
        next_panel, block_matrix = self._step_panel(first_step)
        next_panel.move_to(DOWN * 0.60)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        row_box = SurroundingRectangle(block_matrix.get_rows()[first_step.target_row], color=YELLOW, buff=0.08)
        self.play(Create(row_box), run_time=self.HIGHLIGHT)
        self.wait(1.25)

        for step in snapshot.steps[1:]:
            step_heading = self._heading(f"Gauss-Jordan step {step.index}", 29)
            step_panel, block_matrix = self._step_panel(step)
            step_panel.move_to(DOWN * 0.60)
            self.play(
                FadeOut(row_box),
                ReplacementTransform(heading, step_heading),
                ReplacementTransform(panel, step_panel),
                run_time=self.TRANSITION,
            )
            heading, panel = step_heading, step_panel
            row_box = SurroundingRectangle(block_matrix.get_rows()[step.target_row], color=YELLOW, buff=0.08)
            self.play(Create(row_box), run_time=self.HIGHLIGHT)
            self.wait(1.25)
        self.play(FadeOut(row_box), run_time=0.90)

        next_heading = self._heading("When the left side becomes I, the right side is the inverse", 25)
        next_panel = self._completion_panel(snapshot.reduced_block).move_to(DOWN * 0.58)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = self._heading("Each inverse column solves one unit-vector system", 26)
        next_panel = self._column_panel(snapshot.inverse_columns).move_to(DOWN * 0.58)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = self._heading("Verify the inverse on the right", 29)
        next_panel = self._product_panel(
            snapshot.coefficient_matrix,
            snapshot.inverse_matrix,
            left_label="A",
            right_label=r"A^{-1}",
            equation_tex=r"AA^{-1}=I",
        ).move_to(DOWN * 0.56)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.7)

        next_heading = self._heading("Verify the inverse on the left", 29)
        next_panel = self._product_panel(
            snapshot.inverse_matrix,
            snapshot.coefficient_matrix,
            left_label=r"A^{-1}",
            right_label="A",
            equation_tex=r"A^{-1}A=I",
        ).move_to(DOWN * 0.56)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.7)

        next_heading = self._heading("The right half records the entire row-reduction product", 25)
        next_panel = self._elementary_product_panel().move_to(DOWN * 0.56)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = self._heading("Gauss-Jordan inversion is AX=B with B=I", 28)
        next_panel = self._summary_panel().move_to(DOWN * 0.56)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        self.wait(3.6)

    def _heading(self, text: str, font_size: int) -> Text:
        heading = Text(text, font_size=font_size).move_to(UP * self.HEADING_Y)
        return self._fit_down_only(heading, 11.0)

    def _multiple_rhs_panel(self):
        formula = MathTex(r"AX=I", font_size=44, color=YELLOW)
        columns = MathTex(
            r"X=\begin{bmatrix}\mathbf{x}_1&\mathbf{x}_2&\mathbf{x}_3\end{bmatrix},\qquad "
            r"I=\begin{bmatrix}\mathbf{e}_1&\mathbf{e}_2&\mathbf{e}_3\end{bmatrix}",
            font_size=31,
        )
        systems = MathTex(
            r"A\mathbf{x}_1=\mathbf{e}_1,\qquad "
            r"A\mathbf{x}_2=\mathbf{e}_2,\qquad "
            r"A\mathbf{x}_3=\mathbf{e}_3",
            font_size=31,
            color=GREEN,
        )
        note = Text(
            "The solution matrix X is precisely the inverse of A.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(formula, columns, systems, note).arrange(DOWN, buff=0.38)
        return self._boxed(group)

    def _initial_block_panel(self, block):
        matrix, display = self._augmented_block(block, scale=0.74)
        labels = self._block_labels(matrix, "A", "I")
        formula = MathTex(r"[A\mid I]", font_size=35, color=YELLOW)
        note = Text(
            "Every row operation must act on the coefficient side and the identity side.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(formula, labels, display, note).arrange(DOWN, buff=0.24)
        return self._boxed(group), matrix

    def _step_panel(self, step: GaussJordanStep):
        operation = MathTex(step.operation_tex, font_size=35, color=YELLOW)
        matrix, display = self._augmented_block(step.after_block, scale=0.72)
        labels = self._block_labels(matrix, r"\text{left side}", r"\text{right side}")
        note = Text(step.explanation, font_size=self.EXPLANATION_FONT_SIZE)
        self._fit_down_only(note, 10.7)
        reminder = Text(
            "The highlighted row changes across the complete augmented matrix.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        group = VGroup(operation, labels, display, note, reminder).arrange(DOWN, buff=0.20)
        return self._boxed(group), matrix

    def _completion_panel(self, reduced_block):
        matrix, display = self._augmented_block(reduced_block, scale=0.74)
        labels = self._block_labels(matrix, "I", r"A^{-1}")
        formula = MathTex(r"[A\mid I]\longrightarrow[I\mid A^{-1}]", font_size=37, color=YELLOW)
        inverse = MathTex(
            r"A^{-1}=\begin{bmatrix}"
            r"1&-2&\tfrac52\\"
            r"0&1&-\tfrac32\\"
            r"0&0&\tfrac12"
            r"\end{bmatrix}",
            font_size=34,
            color=GREEN,
        )
        group = VGroup(formula, labels, display, inverse).arrange(DOWN, buff=0.23)
        return self._boxed(group)

    def _column_panel(self, columns):
        colors = (BLUE, GREEN, YELLOW)
        cards = VGroup()
        for index, (column, color) in enumerate(zip(columns, colors, strict=True), start=1):
            vector = self._matrix(column.reshape(3, 1), scale=0.70)
            label = MathTex(rf"\mathbf{{x}}_{index}", font_size=29, color=color)
            equation = MathTex(rf"A\mathbf{{x}}_{index}=\mathbf{{e}}_{index}", font_size=27, color=color)
            content = VGroup(label, vector, equation).arrange(DOWN, buff=0.20)
            cards.add(self._boxed(content, buff=0.14))
        cards.arrange(RIGHT, buff=0.48, aligned_edge=UP)
        note = Text(
            "Reading the inverse by columns solves all three unit-vector systems.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(cards, note).arrange(DOWN, buff=0.36)
        return self._boxed(group)

    def _product_panel(self, left, right, *, left_label: str, right_label: str, equation_tex: str):
        left_matrix = self._matrix(left, scale=0.66)
        right_matrix = self._matrix(right, scale=0.66)
        identity = self._matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]], scale=0.66)
        row = VGroup(
            self._labeled_matrix(left_label, left_matrix, BLUE),
            MathTex(r"\cdot", font_size=34),
            self._labeled_matrix(right_label, right_matrix, GREEN),
            MathTex(r"=", font_size=34),
            self._labeled_matrix("I", identity, YELLOW),
        ).arrange(RIGHT, buff=0.22)
        formula = MathTex(equation_tex, font_size=39, color=YELLOW)
        note = Text(
            "The computed matrix works on both sides of A.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(formula, row, note).arrange(DOWN, buff=0.34)
        return self._boxed(group)

    def _elementary_product_panel(self):
        first = MathTex(
            r"E_4E_3E_2E_1[A\mid I]="
            r"[E_4E_3E_2E_1A\mid E_4E_3E_2E_1]",
            font_size=31,
        )
        second = MathTex(
            r"[I\mid A^{-1}]",
            font_size=38,
            color=GREEN,
        )
        conclusion = MathTex(r"A^{-1}=E_4E_3E_2E_1", font_size=40, color=YELLOW)
        note = Text(
            "The same row operations that turn A into I turn I into the inverse.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(first, second, conclusion, note).arrange(DOWN, buff=0.38)
        return self._boxed(group)

    def _summary_panel(self):
        formula = MathTex(r"[A\mid I]\longrightarrow[I\mid A^{-1}]", font_size=44, color=YELLOW)
        steps = VGroup(
            Text("1. Augment A with the identity matrix.", font_size=23),
            Text("2. Row-reduce the left side all the way to I.", font_size=23),
            Text("3. Read A inverse from the right side.", font_size=23),
        ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        condition = MathTex(
            r"\text{A pivot in every column}\iff A^{-1}\text{ exists}",
            font_size=32,
            color=GREEN,
        )
        preview = Text(
            "If the left side cannot become I, the matrix is not invertible.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        group = VGroup(formula, steps, condition, preview).arrange(DOWN, buff=0.36)
        return self._boxed(group)

    def _augmented_block(self, values, *, scale=0.74):
        matrix = self._matrix(values, scale=scale)
        separator = self._separator(matrix, 3)
        return matrix, VGroup(matrix, separator)

    def _block_labels(self, matrix: Matrix, left_tex: str, right_tex: str):
        columns = matrix.get_columns()
        left_center = (columns[0].get_center()[0] + columns[2].get_center()[0]) / 2
        right_center = (columns[3].get_center()[0] + columns[5].get_center()[0]) / 2
        labels = VGroup(
            MathTex(left_tex, font_size=25, color=BLUE).move_to([left_center, 0, 0]),
            MathTex(right_tex, font_size=25, color=GREEN).move_to([right_center, 0, 0]),
        )
        return labels

    def _labeled_matrix(self, label: str, matrix: Matrix, color):
        name = MathTex(label, font_size=25, color=color)
        return VGroup(name, matrix).arrange(DOWN, buff=0.10)

    def _matrix(self, values, *, scale=0.76):
        formatted = [[self._format_number(value) for value in row] for row in values]
        has_fraction = any("\\tfrac" in entry for row in formatted for entry in row)
        v_buff = 1.02 if has_fraction else 0.68
        return Matrix(formatted, h_buff=0.68, v_buff=v_buff).scale(scale)

    @staticmethod
    def _separator(matrix: Matrix, split_after: int):
        columns = matrix.get_columns()
        x = (columns[split_after - 1].get_right()[0] + columns[split_after].get_left()[0]) / 2
        return Line(UP * matrix.height * 0.48, DOWN * matrix.height * 0.48, stroke_width=2).move_to(
            [x, matrix.get_center()[1], 0]
        )

    @staticmethod
    def _boxed(group, *, buff=0.18):
        return VGroup(SurroundingRectangle(group, color=YELLOW, buff=buff), group)

    @staticmethod
    def _fit_down_only(mobject, max_width: float):
        if mobject.width > max_width:
            mobject.scale_to_fit_width(max_width)
        return mobject

    @staticmethod
    def _format_number(value: float) -> str:
        numeric = float(value)
        rounded = int(round(numeric))
        if abs(numeric - rounded) < 1e-9:
            return str(rounded)
        fraction = Fraction(numeric).limit_denominator(12)
        if abs(float(fraction) - numeric) < 1e-9:
            numerator = fraction.numerator
            denominator = fraction.denominator
            sign = "-" if numerator < 0 else ""
            return rf"{sign}\tfrac{{{abs(numerator)}}}{{{denominator}}}"
        return f"{numeric:g}"
