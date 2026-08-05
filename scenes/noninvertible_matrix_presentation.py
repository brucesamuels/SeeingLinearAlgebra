"""CP123 presentation: why some matrices are not invertible."""

from __future__ import annotations

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

from engine.noninvertible_matrix import NoninvertibilityStep, NoninvertibleMatrix


class NoninvertibleMatrixPresentation(Scene):
    """Connect failed Gauss-Jordan inversion with rank and null space."""

    TRANSITION = 2.20
    HIGHLIGHT = 1.35
    READ = 2.55
    HEADING_Y = 2.24
    EXPLANATION_FONT_SIZE = 21

    def construct(self) -> None:
        snapshot = NoninvertibleMatrix().snapshot()

        title = Text("Why Some Matrices Are Not Invertible", font_size=40).to_edge(UP, buff=0.27)
        subtitle = Text(
            "A missing pivot appears in several equivalent ways.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.13)
        subtitle.scale_to_fit_width(11.2)
        self.play(Write(title), FadeIn(subtitle), run_time=2.4)

        heading = self._heading("Try the same Gauss-Jordan inversion process", 29)
        panel, block_matrix = self._initial_panel(snapshot.augmented_start)
        panel.move_to(DOWN * 0.54)
        self.play(FadeIn(heading), FadeIn(panel), run_time=self.TRANSITION)
        self.wait(2.8)

        first_step = snapshot.steps[0]
        next_heading = self._heading("A dependent row creates the warning", 29)
        next_panel, block_matrix = self._step_panel(first_step)
        next_panel.move_to(DOWN * 0.56)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        warning_box = SurroundingRectangle(
            block_matrix.get_rows()[first_step.target_row],
            color=RED,
            buff=0.10,
        )
        self.play(Create(warning_box), run_time=self.HIGHLIGHT)
        self.wait(self.READ)

        prompt = VGroup(
            Text("Pause and Predict", font_size=25, color=YELLOW),
            Text("Can later row operations create a third pivot?", font_size=21),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.10)
        self.play(FadeIn(prompt), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(prompt), FadeOut(warning_box), run_time=0.90)

        for step in snapshot.steps[1:]:
            next_heading = self._heading(f"Continue reducing the left block: step {step.index}", 28)
            next_panel, block_matrix = self._step_panel(step)
            next_panel.move_to(DOWN * 0.56)
            self.play(
                ReplacementTransform(heading, next_heading),
                ReplacementTransform(panel, next_panel),
                run_time=self.TRANSITION,
            )
            heading, panel = next_heading, next_panel
            row_box = SurroundingRectangle(
                block_matrix.get_rows()[step.target_row],
                color=BLUE,
                buff=0.10,
            )
            self.play(Create(row_box), run_time=self.HIGHLIGHT)
            self.wait(1.65)
            self.play(FadeOut(row_box), run_time=0.75)

        failure_heading = self._heading("The left block cannot become the identity", 29)
        failure_panel, failure_matrix = self._failure_panel(
            snapshot.reduced_block,
            snapshot.failure_tex,
        )
        failure_panel.move_to(DOWN * 0.55)
        self.play(
            ReplacementTransform(heading, failure_heading),
            ReplacementTransform(panel, failure_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = failure_heading, failure_panel
        missing_column_box = SurroundingRectangle(
            failure_matrix.get_columns()[2],
            color=RED,
            buff=0.11,
        )
        self.play(Create(missing_column_box), run_time=self.HIGHLIGHT)
        self.wait(2.9)

        systems_heading = self._heading("AX = I requires three unit-vector systems", 29)
        systems_panel = self._unit_systems_panel(
            snapshot.unit_system_statuses,
            snapshot.unit_system_contradictions,
        ).move_to(DOWN * 0.54)
        self.play(
            ReplacementTransform(heading, systems_heading),
            FadeOut(missing_column_box),
            ReplacementTransform(panel, systems_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = systems_heading, systems_panel
        self.wait(3.1)

        null_heading = self._heading("The missing pivot creates a nonzero null-space vector", 28)
        null_panel = self._null_space_panel(snapshot.left_rref, snapshot.null_space_tex)
        null_panel.next_to(null_heading, DOWN, buff=0.32)
        self.play(
            ReplacementTransform(heading, null_heading),
            ReplacementTransform(panel, null_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = null_heading, null_panel
        self.wait(3.0)

        columns_heading = self._heading("The same vector reveals dependent columns", 29)
        columns_panel = self._column_dependence_panel(snapshot.coefficient_matrix).move_to(DOWN * 0.52)
        self.play(
            ReplacementTransform(heading, columns_heading),
            ReplacementTransform(panel, columns_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = columns_heading, columns_panel
        self.wait(3.0)

        proof_heading = self._heading("A nonzero null vector rules out an inverse", 29)
        proof_panel = self._inverse_contradiction_panel().move_to(DOWN * 0.52)
        self.play(
            ReplacementTransform(heading, proof_heading),
            ReplacementTransform(panel, proof_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = proof_heading, proof_panel
        self.wait(3.0)

        summary_heading = self._heading("Equivalent tests for invertibility", 30)
        summary_panel = self._equivalence_panel(snapshot.equivalence_tex).move_to(DOWN * 0.56)
        self.play(
            ReplacementTransform(heading, summary_heading),
            ReplacementTransform(panel, summary_panel),
            run_time=self.TRANSITION,
        )
        self.wait(3.8)

    def _heading(self, text: str, font_size: int):
        heading = Text(text, font_size=font_size).move_to(UP * self.HEADING_Y)
        return self._fit_down_only(heading, 11.1)

    def _initial_panel(self, values):
        formula = MathTex(r"AX=I", font_size=43, color=YELLOW)
        matrix, display = self._block_matrix(values)
        labels = self._block_labels(matrix, left=r"A", right=r"I")
        note = Text(
            "An inverse would require row operations to turn the left block into I.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(formula, VGroup(display, labels), note).arrange(DOWN, buff=0.38)
        return self._boxed(group), matrix

    def _step_panel(self, step: NoninvertibilityStep):
        operation = MathTex(step.operation_tex, font_size=36, color=YELLOW)
        matrix, display = self._block_matrix(step.after_block)
        explanation = Text(
            step.explanation,
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(explanation, 10.8)
        group = VGroup(operation, display, explanation).arrange(DOWN, buff=0.38)
        return self._boxed(group), matrix

    def _failure_panel(self, values, failure_tex: str):
        matrix, display = self._block_matrix(values)
        labels = self._block_labels(matrix, left=r"R", right=r"C")
        rank = MathTex(r"\operatorname{rank}(A)=2<3", font_size=36, color=RED)
        failure = MathTex(failure_tex, font_size=35, color=RED)
        note = Text(
            "The third variable column has no pivot, so the left block cannot be I.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(VGroup(display, labels), VGroup(rank, failure).arrange(RIGHT, buff=0.80), note).arrange(
            DOWN,
            buff=0.38,
        )
        return self._boxed(group, color=RED), matrix

    def _unit_systems_panel(self, statuses: tuple[str, ...], contradictions: tuple[float, ...]):
        cards = VGroup()
        colors = (RED, RED, YELLOW)
        for index, (status, contradiction, color) in enumerate(
            zip(statuses, contradictions, colors, strict=True),
            start=1,
        ):
            equation = MathTex(
                rf"A\mathbf{{x}}_{index}=\mathbf{{e}}_{index}",
                font_size=30,
                color=color,
            )
            if status == "none":
                row = MathTex(rf"0={int(contradiction)}", font_size=34, color=RED)
                verdict = Text("no solution", font_size=22, color=RED)
            else:
                row = MathTex(r"0=0", font_size=34, color=GREEN)
                verdict = Text("infinitely many solutions", font_size=21, color=YELLOW)
            content = VGroup(equation, row, verdict).arrange(DOWN, buff=0.25)
            cards.add(self._boxed(content, color=color, buff=0.17))
        cards.arrange(RIGHT, buff=0.38, aligned_edge=UP)
        conclusion = Text(
            "No single matrix X can solve all three columns, so AX = I has no solution.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(conclusion, 10.8)
        group = VGroup(cards, conclusion).arrange(DOWN, buff=0.48)
        return self._boxed(group)

    def _null_space_panel(self, values, null_space_tex: str):
        matrix = self._matrix(values).scale(0.88)
        equations = VGroup(
            MathTex(r"x-z=0", font_size=31),
            MathTex(r"y+z=0", font_size=31),
            MathTex(r"z=t", font_size=31, color=YELLOW),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        left_card = self._boxed(VGroup(matrix, equations).arrange(DOWN, buff=0.35), color=BLUE)
        solution = MathTex(
            r"\mathbf{x}=t\begin{bmatrix}1\\-1\\1\end{bmatrix}",
            font_size=39,
            color=YELLOW,
        )
        null_space = MathTex(null_space_tex, font_size=34, color=GREEN)
        check = MathTex(
            r"A\begin{bmatrix}1\\-1\\1\end{bmatrix}=\mathbf0",
            font_size=34,
            color=GREEN,
        )
        right_card = self._boxed(VGroup(solution, null_space, check).arrange(DOWN, buff=0.34), color=GREEN)
        cards = VGroup(left_card, right_card).arrange(RIGHT, buff=0.50, aligned_edge=UP)
        note = Text(
            "A nonzero vector in N(A) means the transformation is not one-to-one.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(note, 10.8)
        return self._boxed(VGroup(cards, note).arrange(DOWN, buff=0.45))

    def _column_dependence_panel(self, values):
        columns = [values[:, index] for index in range(3)]
        column_mobjects = VGroup()
        colors = (BLUE, YELLOW, GREEN)
        for index, (column, color) in enumerate(zip(columns, colors, strict=True), start=1):
            vector = MathTex(
                rf"\mathbf{{c}}_{index}=" + self._column_vector_tex(column),
                font_size=33,
                color=color,
            )
            column_mobjects.add(vector)
        column_mobjects.arrange(RIGHT, buff=0.55)
        relation = MathTex(
            r"\mathbf{c}_1-\mathbf{c}_2+\mathbf{c}_3=\mathbf0",
            font_size=42,
            color=RED,
        )
        explanation = Text(
            "A nontrivial combination of the columns equals zero, so the columns are dependent.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        self._fit_down_only(explanation, 10.8)
        group = VGroup(column_mobjects, relation, explanation).arrange(DOWN, buff=0.44)
        return self._boxed(group)

    def _inverse_contradiction_panel(self):
        assumption = VGroup(
            MathTex(r"A\mathbf{v}=\mathbf0", font_size=37, color=GREEN),
            MathTex(r"\mathbf{v}\ne\mathbf0", font_size=37, color=YELLOW),
        ).arrange(RIGHT, buff=1.10)
        chain = MathTex(
            r"\mathbf{v}=I\mathbf{v}=A^{-1}A\mathbf{v}=A^{-1}\mathbf0=\mathbf0",
            font_size=38,
        )
        contradiction = Text(
            "Contradiction: an inverse cannot coexist with a nonzero null vector.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=RED,
        )
        self._fit_down_only(contradiction, 10.8)
        group = VGroup(assumption, chain, contradiction).arrange(DOWN, buff=0.48)
        return self._boxed(group, color=RED)

    def _equivalence_panel(self, lines: tuple[str, ...]):
        formulae = VGroup(
            MathTex(lines[0], font_size=34, color=BLUE),
            MathTex(lines[1], font_size=34, color=GREEN),
            MathTex(lines[2], font_size=30, color=YELLOW),
        ).arrange(DOWN, buff=0.35)
        failures = VGroup(
            Text("missing pivot", font_size=22, color=RED),
            Text("rank 2 < 3", font_size=22, color=RED),
            Text("nonzero null vector", font_size=22, color=RED),
            Text("dependent columns", font_size=22, color=RED),
        ).arrange(RIGHT, buff=0.50)
        verdict = Text(
            "This matrix fails every equivalent invertibility test.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=RED,
        )
        group = VGroup(formulae, failures, verdict).arrange(DOWN, buff=0.44)
        return self._boxed(group, color=RED)

    def _block_matrix(self, values):
        formatted = [[self._format_number(value) for value in row] for row in values]
        matrix = Matrix(formatted, h_buff=0.70, v_buff=0.72).scale(0.82)
        columns = matrix.get_columns()
        separator_x = (columns[2].get_right()[0] + columns[3].get_left()[0]) / 2
        separator = Line(UP * 1.18, DOWN * 1.18, stroke_width=2.0).move_to(
            [separator_x, matrix.get_center()[1], 0]
        )
        return matrix, VGroup(matrix, separator)

    def _matrix(self, values):
        formatted = [[self._format_number(value) for value in row] for row in values]
        return Matrix(formatted, h_buff=0.82, v_buff=0.70)

    @staticmethod
    def _block_labels(matrix: Matrix, *, left: str, right: str):
        left_center = (matrix.get_columns()[0].get_center() + matrix.get_columns()[2].get_center()) / 2
        right_center = (matrix.get_columns()[3].get_center() + matrix.get_columns()[5].get_center()) / 2
        labels = VGroup(
            MathTex(left, font_size=28, color=BLUE),
            MathTex(right, font_size=28, color=GREEN),
        )
        labels[0].move_to([left_center[0], matrix.get_top()[1] + 0.28, 0])
        labels[1].move_to([right_center[0], matrix.get_top()[1] + 0.28, 0])
        return labels

    @staticmethod
    def _boxed(group, *, color=YELLOW, buff=0.20):
        return VGroup(SurroundingRectangle(group, color=color, buff=buff), group)

    @staticmethod
    def _fit_down_only(mobject, max_width: float):
        if mobject.width > max_width:
            mobject.scale_to_fit_width(max_width)
        return mobject

    @staticmethod
    def _column_vector_tex(values) -> str:
        entries = [str(int(round(float(value)))) for value in values]
        return r"\begin{bmatrix}" + r"\\".join(entries) + r"\end{bmatrix}"

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
