"""CP107 presentation: the three elementary row operations."""

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
    ReplacementTransform,
    RIGHT,
    Scene,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
)

from engine.elementary_row_operations import ElementaryRowOperations


class ElementaryRowOperationsPresentation(Scene):
    """Show each legal row operation on equations and an augmented matrix."""

    TITLE = "Elementary Row Operations"

    def construct(self) -> None:
        operations = ElementaryRowOperations()
        snapshot = operations.snapshot()

        title = Text(self.TITLE, font_size=40).to_edge(UP, buff=0.28)
        subtitle = Text(
            "Change the equations without changing their common solution.",
            font_size=25,
        ).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(subtitle), run_time=1.2)

        left_heading = Text("Equations", font_size=28).move_to(LEFT * 3.45 + UP * 1.60)
        right_heading = Text("Augmented matrix", font_size=28).move_to(
            RIGHT * 3.30 + UP * 1.60
        )
        divider = Line(UP * 1.30, DOWN * 2.15, stroke_width=1.2)

        equations = self._equation_group((r"x+y=2", r"2x-y=1"))
        matrix, matrix_display = self._augmented_matrix(snapshot.base_augmented)
        headers = self._matrix_headers(matrix)
        self.play(
            FadeIn(left_heading),
            FadeIn(right_heading),
            Create(divider),
            Write(equations),
            FadeIn(matrix_display),
            FadeIn(headers),
            run_time=1.6,
        )

        solution_badge = VGroup(
            Text("Common solution", font_size=23),
            MathTex(r"(x,y)=(1,1)", color=GREEN, font_size=34),
        ).arrange(DOWN, buff=0.10).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(solution_badge), run_time=0.7)
        self.wait(2.0)

        operation_heading = Text("1. Swap two rows", font_size=29, color=YELLOW)
        operation_heading.next_to(subtitle, DOWN, buff=0.30)
        operation_symbol = MathTex(
            r"R_1\leftrightarrow R_2",
            font_size=38,
            color=YELLOW,
        ).next_to(solution_badge, UP, buff=0.24)
        equation_boxes = VGroup(
            SurroundingRectangle(equations[0], color=BLUE, buff=0.10),
            SurroundingRectangle(equations[1], color=YELLOW, buff=0.10),
        )
        matrix_rows = matrix.get_rows()
        matrix_boxes = VGroup(
            SurroundingRectangle(matrix_rows[0], color=BLUE, buff=0.10),
            SurroundingRectangle(matrix_rows[1], color=YELLOW, buff=0.10),
        )
        self.play(FadeIn(operation_heading), Write(operation_symbol), run_time=0.8)
        self.play(Create(equation_boxes), Create(matrix_boxes), run_time=0.7)

        swapped_equations = self._equation_group((r"2x-y=1", r"x+y=2"))
        swapped_matrix, swapped_display = self._augmented_matrix(
            snapshot.swapped_augmented
        )
        self.play(
            ReplacementTransform(equations, swapped_equations),
            ReplacementTransform(matrix_display, swapped_display),
            FadeOut(equation_boxes),
            FadeOut(matrix_boxes),
            run_time=1.2,
        )
        equations = swapped_equations
        matrix = swapped_matrix
        matrix_display = swapped_display
        swap_note = Text(
            "Reordering the equations changes no solution.",
            font_size=24,
        ).next_to(operation_symbol, UP, buff=0.20)
        self.play(FadeIn(swap_note), run_time=0.6)
        self.wait(1.8)

        base_equations = self._equation_group((r"x+y=2", r"2x-y=1"))
        base_matrix, base_display = self._augmented_matrix(snapshot.base_augmented)
        self.play(
            FadeOut(swap_note),
            FadeOut(operation_symbol),
            FadeOut(operation_heading),
            ReplacementTransform(equations, base_equations),
            ReplacementTransform(matrix_display, base_display),
            run_time=1.0,
        )
        equations = base_equations
        matrix = base_matrix
        matrix_display = base_display

        operation_heading = Text("2. Scale one row", font_size=29, color=YELLOW)
        operation_heading.next_to(subtitle, DOWN, buff=0.30)
        operation_symbol = MathTex(
            r"R_1\leftarrow 2R_1",
            font_size=38,
            color=YELLOW,
        ).next_to(solution_badge, UP, buff=0.24)
        equation_box = SurroundingRectangle(equations[0], color=BLUE, buff=0.10)
        matrix_box = SurroundingRectangle(matrix.get_rows()[0], color=BLUE, buff=0.10)
        self.play(FadeIn(operation_heading), Write(operation_symbol), run_time=0.8)
        self.play(Create(equation_box), Create(matrix_box), run_time=0.6)

        scaled_equations = self._equation_group((r"2x+2y=4", r"2x-y=1"))
        scaled_matrix, scaled_display = self._augmented_matrix(snapshot.scaled_augmented)
        self.play(
            ReplacementTransform(equations, scaled_equations),
            ReplacementTransform(matrix_display, scaled_display),
            FadeOut(equation_box),
            FadeOut(matrix_box),
            run_time=1.2,
        )
        equations = scaled_equations
        matrix = scaled_matrix
        matrix_display = scaled_display
        scale_note = Text(
            "Multiply the entire equation by the same nonzero number.",
            font_size=23,
        ).next_to(operation_symbol, UP, buff=0.20)
        self.play(FadeIn(scale_note), run_time=0.6)
        self.wait(2.0)

        base_equations = self._equation_group((r"x+y=2", r"2x-y=1"))
        base_matrix, base_display = self._augmented_matrix(snapshot.base_augmented)
        self.play(
            FadeOut(scale_note),
            FadeOut(operation_symbol),
            FadeOut(operation_heading),
            ReplacementTransform(equations, base_equations),
            ReplacementTransform(matrix_display, base_display),
            run_time=1.0,
        )
        equations = base_equations
        matrix = base_matrix
        matrix_display = base_display

        prompt = VGroup(
            Text("Pause and Predict", font_size=29, color=YELLOW),
            Text(
                "Which multiple of row 1 should be added to row 2 to eliminate x?",
                font_size=24,
            ),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.25)
        prompt.scale_to_fit_width(11.4)
        self.play(FadeOut(solution_badge), FadeIn(prompt), run_time=0.7)
        self.wait(2.4)
        self.play(FadeOut(prompt), run_time=0.5)

        operation_heading = Text("3. Replace one row", font_size=29, color=YELLOW)
        operation_heading.next_to(subtitle, DOWN, buff=0.30)
        operation_symbol = MathTex(
            r"R_2\leftarrow R_2-2R_1",
            font_size=38,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.35)
        equation_boxes = VGroup(
            SurroundingRectangle(equations[0], color=BLUE, buff=0.10),
            SurroundingRectangle(equations[1], color=YELLOW, buff=0.10),
        )
        matrix_boxes = VGroup(
            SurroundingRectangle(matrix.get_rows()[0], color=BLUE, buff=0.10),
            SurroundingRectangle(matrix.get_rows()[1], color=YELLOW, buff=0.10),
        )
        self.play(FadeIn(operation_heading), Write(operation_symbol), run_time=0.8)
        self.play(Create(equation_boxes), Create(matrix_boxes), run_time=0.7)

        replaced_equations = self._equation_group((r"x+y=2", r"-3y=-3"))
        replaced_matrix, replaced_display = self._augmented_matrix(
            snapshot.replaced_augmented
        )
        self.play(
            ReplacementTransform(equations, replaced_equations),
            ReplacementTransform(matrix_display, replaced_display),
            FadeOut(equation_boxes),
            FadeOut(matrix_boxes),
            run_time=1.2,
        )
        equations = replaced_equations
        matrix_display = replaced_display
        arithmetic = VGroup(
            MathTex(
                r"(2x-y)-2(x+y)",
                font_size=28,
            ),
            MathTex(
                r"=1-2(2)\quad\Longrightarrow\quad -3y=-3",
                font_size=28,
            ),
        ).arrange(DOWN, buff=0.12)
        arithmetic.scale_to_fit_width(5.6)
        arithmetic.move_to(LEFT * 3.45 + DOWN * 1.55)
        self.play(Write(arithmetic), run_time=1.1)
        self.wait(2.1)

        solution_badge = VGroup(
            Text("The common solution is still", font_size=23),
            MathTex(r"(x,y)=(1,1)", color=GREEN, font_size=34),
        ).arrange(DOWN, buff=0.10).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(operation_symbol), FadeIn(solution_badge), run_time=0.7)
        self.wait(2.0)

        outgoing = VGroup(
            subtitle,
            left_heading,
            right_heading,
            divider,
            equations,
            matrix_display,
            headers,
            operation_heading,
            arithmetic,
            solution_badge,
        )
        self.play(FadeOut(outgoing), run_time=1.0)

        summary_heading = Text("Three legal moves", font_size=31, color=YELLOW)
        summary = VGroup(
            MathTex(r"R_i\leftrightarrow R_j", font_size=38),
            MathTex(r"R_i\leftarrow cR_i\qquad(c\ne 0)", font_size=38),
            MathTex(r"R_i\leftarrow R_i+cR_j\qquad(i\ne j)", font_size=38),
        ).arrange(DOWN, buff=0.34)
        conclusion = Text(
            "Each operation changes the description—but preserves the solution set.",
            font_size=27,
        )
        final_group = VGroup(summary_heading, summary, conclusion).arrange(
            DOWN,
            buff=0.42,
        ).move_to(DOWN * 0.15)
        final_group.scale_to_fit_width(11.4)
        self.play(FadeIn(final_group), run_time=1.0)
        self.wait(4.0)

    def _equation_group(self, equation_tex: tuple[str, str]) -> VGroup:
        return VGroup(
            *[MathTex(tex, font_size=38) for tex in equation_tex]
        ).arrange(DOWN, buff=0.48, aligned_edge=LEFT).move_to(
            LEFT * 3.45 + DOWN * 0.05
        )

    def _augmented_matrix(self, values) -> tuple[Matrix, VGroup]:
        display_values = [
            [
                str(int(round(float(value))))
                if abs(float(value) - round(float(value))) < 1e-9
                else f"{float(value):g}"
                for value in row
            ]
            for row in values
        ]
        matrix = Matrix(display_values, h_buff=0.90, v_buff=0.70).scale(0.92)
        matrix.move_to(RIGHT * 3.25 + DOWN * 0.05)
        columns = matrix.get_columns()
        separator_x = (columns[1].get_right()[0] + columns[2].get_left()[0]) / 2
        separator = Line(UP * 0.95, DOWN * 0.95, stroke_width=2.0).move_to(
            [separator_x, matrix.get_center()[1], 0]
        )
        return matrix, VGroup(matrix, separator)

    def _matrix_headers(self, matrix: Matrix) -> VGroup:
        columns = matrix.get_columns()
        headers = VGroup(
            MathTex("x", color=BLUE, font_size=30),
            MathTex("y", color=YELLOW, font_size=30),
            MathTex(r"\mathbf{b}", color=GREEN, font_size=30),
        )
        for header, column in zip(headers, columns, strict=True):
            header.next_to(column, UP, buff=0.25)
        return headers
