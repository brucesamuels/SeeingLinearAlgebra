"""CP106 presentation: encode equations as an augmented matrix."""

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
    WHITE,
    Write,
    YELLOW,
)

from engine.augmented_matrix_encoding import AugmentedMatrixEncoding


class AugmentedMatrixEncodingPresentation(Scene):
    """Move equation data into an augmented matrix one row at a time."""

    TITLE = "From Equations to an Augmented Matrix"
    COLUMN_COLORS = (BLUE, GREEN, RED, YELLOW)

    def construct(self) -> None:
        encoding = AugmentedMatrixEncoding()
        snapshot = encoding.snapshot()

        title = Text(self.TITLE, font_size=40).to_edge(UP, buff=0.28)
        subtitle = Text(
            "Keep the numbers. Preserve their positions.",
            font_size=25,
        ).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(subtitle), run_time=1.2)

        natural_heading = Text("The system", font_size=29)
        natural_equations = MathTex(
            r"\begin{aligned}"
            r"x+y+z&=3\\"
            r"2x-y+z&=2\\"
            r"x+2y-z&=2"
            r"\end{aligned}",
            font_size=42,
        )
        natural_group = VGroup(natural_heading, natural_equations).arrange(
            DOWN,
            buff=0.42,
        ).move_to(DOWN * 0.10)
        self.play(FadeIn(natural_heading), Write(natural_equations), run_time=1.5)
        self.wait(2.0)

        instruction = Text(
            "Before suppressing the symbols, write every coefficient.",
            font_size=26,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(instruction), run_time=0.7)
        self.wait(1.8)

        explicit_rows, numeric_sources = self._build_explicit_rows()
        explicit_heading = Text("Make every coefficient visible", font_size=29)
        explicit_group = VGroup(explicit_heading, explicit_rows).arrange(
            DOWN,
            buff=0.38,
        ).move_to(LEFT * 3.45 + DOWN * 0.08)
        self.play(
            FadeOut(instruction),
            ReplacementTransform(natural_heading, explicit_heading),
            ReplacementTransform(natural_equations, explicit_rows),
            run_time=1.2,
        )
        self.wait(2.0)

        matrix, matrix_display, headers, separator = self._build_augmented_matrix()
        matrix_heading = Text("Augmented matrix", font_size=29).move_to(
            RIGHT * 3.30 + UP * 1.75
        )
        divider_caption = Text(
            "The divider separates coefficients from constants.",
            font_size=23,
        ).move_to(RIGHT * 3.15 + DOWN * 2.30)
        self.play(
            FadeIn(matrix_heading),
            FadeIn(headers),
            Create(separator),
            FadeIn(matrix.get_brackets()),
            FadeIn(divider_caption),
            run_time=1.0,
        )

        target_rows = matrix.get_rows()
        for equation_row, sources, target_row in zip(
            explicit_rows,
            numeric_sources,
            target_rows,
            strict=True,
        ):
            row_box = SurroundingRectangle(
                equation_row,
                color=YELLOW,
                buff=0.10,
            )
            self.play(Create(row_box), run_time=0.35)
            self.play(
                *[
                    ReplacementTransform(source.copy(), target)
                    for source, target in zip(sources, target_row, strict=True)
                ],
                run_time=1.2,
            )
            self.play(FadeOut(row_box), run_time=0.3)
            self.wait(0.45)

        self.wait(1.2)
        self.play(
            *[entry.animate.set_color(WHITE) for entry in matrix.get_entries()],
            run_time=0.6,
        )

        self.play(
            FadeOut(explicit_heading),
            FadeOut(explicit_rows),
            FadeOut(subtitle),
            FadeOut(divider_caption),
            matrix_heading.animate.move_to(UP * 1.75),
            matrix_display.animate.move_to(DOWN * 0.08).scale(1.10),
            run_time=1.1,
        )

        a_box, b_box, a_label, b_label = self._build_block_labels(matrix)
        preserved = VGroup(
            Text("The first three columns are the coefficient matrix A.", font_size=25),
            Text("The final column is the right-hand side b.", font_size=25),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.30)
        self.play(
            Create(a_box),
            Create(b_box),
            FadeIn(a_label),
            FadeIn(b_label),
            FadeIn(preserved),
            run_time=1.0,
        )
        self.wait(2.6)

        prompt = VGroup(
            Text("Pause and Predict", font_size=29, color=YELLOW),
            Text("How should x - z = 4 be recorded?", font_size=26),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.30)
        self.play(FadeOut(preserved), FadeIn(prompt), run_time=0.7)
        self.wait(2.2)

        missing_example = self._build_missing_variable_example()
        self.play(
            FadeOut(prompt),
            FadeOut(a_box),
            FadeOut(b_box),
            FadeOut(a_label),
            FadeOut(b_label),
            FadeOut(matrix_heading),
            FadeOut(matrix.get_brackets()),
            FadeOut(matrix.get_entries()),
            FadeOut(separator),
            FadeOut(headers),
            run_time=0.9,
        )
        self.remove(
            matrix_heading,
            matrix.get_brackets(),
            matrix.get_entries(),
            separator,
            headers,
        )
        self.play(FadeIn(missing_example), run_time=0.8)
        self.wait(3.0)

        conclusion = VGroup(
            Text("An augmented matrix preserves the system when:", font_size=28),
            Text("the variable order is fixed,", font_size=26),
            Text("every coefficient—including zero—is recorded,", font_size=26),
            Text("and the final column remains the right-hand side.", font_size=26),
        ).arrange(DOWN, buff=0.20).move_to(DOWN * 0.25)
        conclusion.scale_to_fit_width(11.4)
        outgoing = [mob for mob in self.mobjects if mob is not title]
        self.play(
            *[FadeOut(mob) for mob in outgoing],
            run_time=0.8,
        )
        self.clear()
        self.add(title)
        self.wait(0.15)
        self.play(FadeIn(conclusion), run_time=0.8)
        self.wait(4.0)

    def _build_explicit_rows(self):
        specifications = (
            ("1", "x", "+", "1", "y", "+", "1", "z", "=", "3"),
            ("2", "x", "+", r"(-1)", "y", "+", "1", "z", "=", "2"),
            ("1", "x", "+", "2", "y", "+", r"(-1)", "z", "=", "2"),
        )
        rows = VGroup(
            *[MathTex(*parts, font_size=34) for parts in specifications]
        ).arrange(DOWN, buff=0.40, aligned_edge=LEFT)
        for row in rows:
            row[0].set_color(BLUE)
            row[1].set_color(BLUE)
            row[3].set_color(GREEN)
            row[4].set_color(GREEN)
            row[6].set_color(RED)
            row[7].set_color(RED)
            row[9].set_color(YELLOW)
        numeric_sources = tuple(
            (row[0], row[3], row[6], row[9]) for row in rows
        )
        return rows, numeric_sources

    def _build_augmented_matrix(self):
        matrix = Matrix(
            [[1, 1, 1, 3], [2, -1, 1, 2], [1, 2, -1, 2]],
            h_buff=0.78,
            v_buff=0.62,
        ).scale(0.88).move_to(RIGHT * 3.20 + DOWN * 0.08)
        columns = matrix.get_columns()
        for column, color in zip(columns, self.COLUMN_COLORS, strict=True):
            column.set_color(color)

        separator_x = (
            columns[2].get_right()[0] + columns[3].get_left()[0]
        ) / 2
        separator = Line(
            UP * 1.28,
            DOWN * 1.28,
            stroke_width=2.0,
        ).move_to([separator_x, matrix.get_center()[1], 0])

        header_labels = VGroup(
            MathTex("x", color=BLUE, font_size=31),
            MathTex("y", color=GREEN, font_size=31),
            MathTex("z", color=RED, font_size=31),
            MathTex(r"\mathbf{b}", color=YELLOW, font_size=31),
        )
        for label, column in zip(header_labels, columns, strict=True):
            label.next_to(column, UP, buff=0.25)

        display = VGroup(
            matrix.get_brackets(),
            matrix.get_entries(),
            separator,
            header_labels,
        )
        return matrix, display, header_labels, separator

    def _build_block_labels(self, matrix):
        columns = matrix.get_columns()
        coefficient_entries = VGroup(*columns[:3])
        rhs_entries = columns[3]
        a_box = SurroundingRectangle(
            coefficient_entries,
            color=BLUE,
            buff=0.16,
        )
        b_box = SurroundingRectangle(
            rhs_entries,
            color=YELLOW,
            buff=0.16,
        )
        a_label = MathTex(r"A", color=BLUE, font_size=34).next_to(
            a_box,
            DOWN,
            buff=0.15,
        )
        b_label = MathTex(r"\mathbf{b}", color=YELLOW, font_size=34).next_to(
            b_box,
            DOWN,
            buff=0.15,
        )
        return a_box, b_box, a_label, b_label

    def _build_missing_variable_example(self):
        heading = Text("A missing variable needs a zero placeholder", font_size=28)
        natural = MathTex(r"x-z=4", font_size=37)
        explicit = MathTex(r"1x+0y+(-1)z=4", font_size=34)
        row = Matrix([[1, 0, -1, 4]], h_buff=0.78).scale(0.84)
        columns = row.get_columns()
        separator_x = (
            columns[2].get_right()[0] + columns[3].get_left()[0]
        ) / 2
        separator = Line(UP * 0.45, DOWN * 0.45, stroke_width=2.0).move_to(
            [separator_x, row.get_center()[1], 0]
        )
        zero_box = SurroundingRectangle(columns[1], color=YELLOW, buff=0.10)
        note = Text("The zero keeps y in its column.", font_size=24, color=YELLOW)
        row_group = VGroup(row, separator, zero_box)
        group = VGroup(heading, natural, explicit, row_group, note).arrange(
            DOWN,
            buff=0.24,
        )
        group.scale_to_fit_width(9.8)
        group.move_to(DOWN * 0.70)
        return group
