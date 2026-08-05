"""CP120 presentation: elimination as matrix multiplication and A = LU."""

from __future__ import annotations

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

from engine.elimination_matrix_multiplication import (
    EliminationMatrixMultiplication,
    EliminationStep,
)


class EliminationMatrixMultiplicationPresentation(Scene):
    """Show elimination products and reverse them to produce A = LU."""

    TRANSITION = 1.65
    HIGHLIGHT = 1.10
    READ = 2.35
    HEADING_Y = 2.20
    EXPLANATION_FONT_SIZE = 21

    def construct(self) -> None:
        snapshot = EliminationMatrixMultiplication().snapshot()

        title = Text("Elimination as Matrix Multiplication", font_size=39).to_edge(UP, buff=0.27)
        subtitle = Text(
            "From individual elimination matrices to the factorization A = LU.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.13)
        subtitle.scale_to_fit_width(11.4)
        self.play(Write(title), FadeIn(subtitle), run_time=1.9)

        heading = Text("Previously, we built the elementary building blocks", font_size=28).move_to(UP * self.HEADING_Y)
        heading.scale_to_fit_width(11.0)
        panel = self._bridge_panel().move_to(DOWN * 0.48)
        self.play(FadeIn(heading), FadeIn(panel), run_time=self.TRANSITION)
        self.wait(2.7)

        next_heading = Text("Our goal is elimination from A to U", font_size=30).move_to(UP * self.HEADING_Y)
        next_panel = self._goal_panel(snapshot.original_matrix, snapshot.upper_triangular_matrix).move_to(DOWN * 0.50)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.8)

        for step in snapshot.elimination_steps:
            next_heading = self._step_heading(step)
            next_panel, result_matrix = self._step_panel(step)
            next_panel.move_to(DOWN * 0.48)
            self.play(
                ReplacementTransform(heading, next_heading),
                ReplacementTransform(panel, next_panel),
                run_time=self.TRANSITION,
            )
            changed_row = result_matrix.get_rows()[step.target_row]
            row_box = SurroundingRectangle(changed_row, color=GREEN, buff=0.10)
            self.play(Create(row_box), run_time=self.HIGHLIGHT)
            self.wait(self.READ)
            self.play(FadeOut(row_box), run_time=0.65)
            heading, panel = next_heading, next_panel

        next_heading = Text("Compose the three elimination matrices", font_size=30).move_to(UP * self.HEADING_Y)
        next_panel = self._composition_panel(snapshot).move_to(DOWN * 0.52)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = Text("Multiply them into one elimination operator", font_size=29).move_to(UP * self.HEADING_Y)
        next_panel = self._combined_operator_panel(snapshot).move_to(DOWN * 0.50)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.1)

        next_heading = Text("Reverse the product to recover A from U", font_size=29).move_to(UP * self.HEADING_Y)
        next_panel = self._inverse_product_panel(snapshot).move_to(DOWN * 0.52)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = Text("The inverse product is lower triangular", font_size=29).move_to(UP * self.HEADING_Y)
        next_panel = self._lower_factor_panel(snapshot).move_to(DOWN * 0.50)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = Text("The multipliers move into L", font_size=30).move_to(UP * self.HEADING_Y)
        next_panel = self._multiplier_panel(snapshot).move_to(DOWN * 0.48)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        next_heading = Text("Verify the factorization by multiplying L and U", font_size=28).move_to(UP * self.HEADING_Y)
        next_heading.scale_to_fit_width(11.0)
        next_panel = self._verification_panel(snapshot).move_to(DOWN * 0.50)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.2)

        next_heading = Text("Elimination and factorization are the same process", font_size=28).move_to(UP * self.HEADING_Y)
        next_heading.scale_to_fit_width(11.0)
        next_panel = self._summary_panel().move_to(DOWN * 0.48)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        self.wait(3.6)

    def _step_heading(self, step: EliminationStep):
        prose = Text(f"Step {step.index}: use the multiplier", font_size=28)
        symbol = MathTex(
            rf"m_{{{step.target_row + 1}{step.pivot_row + 1}}}={self._tex_number(step.multiplier)}",
            font_size=36,
            color=YELLOW,
        )
        heading = VGroup(prose, symbol).arrange(RIGHT, buff=0.22)
        heading.move_to(UP * self.HEADING_Y)
        return heading

    def _step_panel(self, step: EliminationStep):
        operation = MathTex(step.operation_tex, font_size=34, color=YELLOW)
        e_matrix = self._matrix(step.elementary_matrix, scale=0.70)
        before_matrix = self._matrix(step.before_matrix, scale=0.70)
        result_matrix = self._matrix(step.after_matrix, scale=0.70)
        product = VGroup(
            self._labeled_matrix(rf"E_{step.index}", e_matrix),
            MathTex(r"\cdot", font_size=38),
            self._labeled_matrix(rf"A_{step.index - 1}", before_matrix),
            MathTex(r"=", font_size=38),
            self._labeled_matrix(rf"A_{step.index}", result_matrix),
        ).arrange(RIGHT, buff=0.28)
        explanation = Text(
            "Left multiplication replaces one row while leaving the other rows unchanged.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(explanation, 10.8)
        group = VGroup(operation, product, explanation).arrange(DOWN, buff=0.38)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group), result_matrix

    def _bridge_panel(self):
        line1 = MathTex(r"E_1A=A_1,\qquad E_2A_1=A_2,\qquad E_3A_2=U", font_size=37)
        line2 = MathTex(r"E_3E_2E_1A=U", font_size=43, color=YELLOW)
        note = Text(
            "CP120 studies the product of those elementary matrices rather than each operation in isolation.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(line1, line2, note).arrange(DOWN, buff=0.46)
        return self._boxed(group)

    def _goal_panel(self, original, upper):
        left = self._labeled_matrix("A", self._matrix(original, scale=0.86))
        right = self._labeled_matrix("U", self._matrix(upper, scale=0.86))
        arrow = MathTex(r"\xrightarrow{\text{elimination}}", font_size=37, color=YELLOW)
        matrices = VGroup(left, arrow, right).arrange(RIGHT, buff=0.60)
        note = Text(
            "Only entries below the pivots are eliminated; pivot rows are not scaled and no back elimination is used.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(matrices, note).arrange(DOWN, buff=0.50)
        return self._boxed(group)

    def _composition_panel(self, snapshot):
        factors = VGroup()
        for step in reversed(snapshot.elimination_steps):
            factors.add(self._labeled_matrix(rf"E_{step.index}", self._matrix(step.elementary_matrix, scale=0.57)))
        factors.add(self._labeled_matrix("A", self._matrix(snapshot.original_matrix, scale=0.57)))
        expression = VGroup()
        for index, item in enumerate(factors):
            expression.add(item)
            if index < len(factors) - 1:
                expression.add(MathTex(r"\cdot", font_size=32))
        expression.add(MathTex(r"=", font_size=34))
        expression.add(self._labeled_matrix("U", self._matrix(snapshot.upper_triangular_matrix, scale=0.57)))
        expression.arrange(RIGHT, buff=0.16)
        formula = MathTex(snapshot.elimination_product_tex, font_size=42, color=YELLOW)
        note = Text(
            "The rightmost matrix acts first, so the elimination matrices appear in reverse chronological order.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(expression, formula, note).arrange(DOWN, buff=0.38)
        return self._boxed(group)

    def _combined_operator_panel(self, snapshot):
        factor_product = MathTex(r"E=E_3E_2E_1", font_size=39, color=YELLOW)
        matrix = self._labeled_matrix("E", self._matrix(snapshot.elimination_product, scale=0.84))
        identity = MathTex(r"EA=U", font_size=44, color=GREEN)
        note = Text(
            "One lower-triangular matrix now performs all three elimination steps at once.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(factor_product, matrix, identity, note).arrange(DOWN, buff=0.34)
        return self._boxed(group)

    def _inverse_product_panel(self, snapshot):
        first = MathTex(r"EA=U", font_size=40)
        second = MathTex(r"A=E^{-1}U", font_size=42, color=YELLOW)
        third = MathTex(snapshot.inverse_product_tex, font_size=40, color=GREEN)
        note = Text(
            "The order reverses when a product is inverted.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(first, second, third, note).arrange(DOWN, buff=0.42)
        return self._boxed(group)

    def _lower_factor_panel(self, snapshot):
        inverse_factors = VGroup()
        for step in snapshot.elimination_steps:
            inverse_factors.add(
                self._labeled_matrix(
                    rf"E_{step.index}^{{-1}}",
                    self._matrix(step.inverse_elementary_matrix, scale=0.60),
                )
            )
        product = VGroup()
        for index, item in enumerate(inverse_factors):
            product.add(item)
            if index < len(inverse_factors) - 1:
                product.add(MathTex(r"\cdot", font_size=32))
        product.add(MathTex(r"=", font_size=34))
        product.add(self._labeled_matrix("L", self._matrix(snapshot.lower_triangular_matrix, scale=0.67)))
        product.arrange(RIGHT, buff=0.18)
        formula = MathTex(r"L=E_1^{-1}E_2^{-1}E_3^{-1}", font_size=39, color=YELLOW)
        note = Text(
            "The inverse elimination matrices multiply to a unit lower-triangular matrix.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(product, formula, note).arrange(DOWN, buff=0.38)
        return self._boxed(group)

    def _multiplier_panel(self, snapshot):
        equations = VGroup()
        colors = (BLUE, GREEN, YELLOW)
        for step, color in zip(snapshot.elimination_steps, colors, strict=True):
            i, j = step.target_row + 1, step.pivot_row + 1
            equations.add(
                MathTex(
                    rf"m_{{{i}{j}}}={self._tex_number(step.multiplier)}"
                    rf"\quad\Longrightarrow\quad"
                    rf"(E_{step.index})_{{{i}{j}}}=-m_{{{i}{j}}},"
                    rf"\quad L_{{{i}{j}}}=m_{{{i}{j}}}",
                    font_size=32,
                    color=color,
                )
            )
        equations.arrange(DOWN, buff=0.28)
        conclusion = MathTex(
            r"L=\begin{bmatrix}1&0&0\\2&1&0\\-1&-1&1\end{bmatrix}",
            font_size=40,
            color=YELLOW,
        )
        note = Text(
            "Elimination matrices store negative multipliers; L stores the multipliers themselves.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(equations, conclusion, note).arrange(DOWN, buff=0.34)
        return self._boxed(group)

    def _verification_panel(self, snapshot):
        l_matrix = self._matrix(snapshot.lower_triangular_matrix, scale=0.76)
        u_matrix = self._matrix(snapshot.upper_triangular_matrix, scale=0.76)
        a_matrix = self._matrix(snapshot.original_matrix, scale=0.76)
        product = VGroup(
            self._labeled_matrix("L", l_matrix),
            MathTex(r"\cdot", font_size=38),
            self._labeled_matrix("U", u_matrix),
            MathTex(r"=", font_size=38),
            self._labeled_matrix("A", a_matrix),
        ).arrange(RIGHT, buff=0.34)
        formula = MathTex(snapshot.lu_factorization_tex, font_size=48, color=YELLOW)
        note = Text(
            "Multiplying L by U exactly reconstructs the original matrix.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(product, formula, note).arrange(DOWN, buff=0.44)
        return self._boxed(group)

    def _summary_panel(self):
        chain = VGroup(
            MathTex(r"E_3E_2E_1A=U", font_size=40, color=BLUE),
            MathTex(r"A=E_1^{-1}E_2^{-1}E_3^{-1}U", font_size=39, color=GREEN),
            MathTex(r"A=LU", font_size=48, color=YELLOW),
        ).arrange(DOWN, buff=0.34)
        ideas = VGroup(
            Text("E records the operations that eliminate A.", font_size=self.EXPLANATION_FONT_SIZE),
            Text("L records the multipliers that rebuild A from U.", font_size=self.EXPLANATION_FONT_SIZE),
            Text("LU factorization is Gaussian elimination written as a matrix identity.", font_size=self.EXPLANATION_FONT_SIZE),
        ).arrange(DOWN, buff=0.20)
        group = VGroup(chain, ideas).arrange(DOWN, buff=0.48)
        return self._boxed(group)

    @staticmethod
    def _boxed(group):
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    def _labeled_matrix(self, label_tex: str, matrix: Matrix):
        label = MathTex(label_tex, font_size=28, color=YELLOW)
        return VGroup(label, matrix).arrange(DOWN, buff=0.12)

    def _matrix(self, values, *, scale: float):
        formatted = [[self._format_number(value) for value in row] for row in values]
        return Matrix(formatted, h_buff=0.72, v_buff=0.72).scale(scale)

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

    @staticmethod
    def _tex_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
