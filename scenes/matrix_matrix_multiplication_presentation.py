"""CP99 Manim presentation: Matrix-Matrix Multiplication."""

from __future__ import annotations

from manim import (
    BLUE,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    MathTex,
    Matrix,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from engine.matrix_matrix_multiplication import (
    MATRIX_MATRIX_MULTIPLICATION_LESSON,
    entry_computations,
)


class MatrixMatrixMultiplicationPresentation(Scene):
    """Compute a matrix product entry by entry using rows and columns."""

    TITLE = "Matrix–Matrix Multiplication"

    @staticmethod
    def _matrix(data, *, scale: float = 0.78) -> Matrix:
        matrix = Matrix(
            [[str(value) for value in row] for row in data],
            h_buff=0.82,
            v_buff=0.6,
        )
        return matrix.scale(scale)

    def construct(self) -> None:
        title = Text(self.TITLE, weight="BOLD").scale(0.66)
        title.to_edge(UP, buff=0.28)
        subtitle = Text(
            "Every entry is a row–column dot product",
        ).scale(0.42)
        subtitle.next_to(title, DOWN, buff=0.16)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.1))
        self.wait(0.8)

        self._show_dimension_rule(subtitle)
        self._show_first_entry()
        self._show_remaining_entries()
        self._state_general_rule()
        self._show_incompatible_product()
        self._show_pause_predict_and_reflection()

    def _show_dimension_rule(self, subtitle: Text) -> None:
        heading = Text(
            "First check the dimensions",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.05)

        valid = MathTex(
            r"A_{m\times n}B_{n\times p}=C_{m\times p}",
            color=YELLOW,
        ).scale(0.92).move_to(UP * 0.65)

        inner = Text(
            "The inner dimensions must match.",
        ).scale(0.44).move_to(DOWN * 0.25)

        outer = Text(
            "The outer dimensions determine the product.",
        ).scale(0.42).move_to(DOWN * 0.95)

        example = MathTex(
            r"(2\times3)(3\times2)\longrightarrow2\times2",
        ).scale(0.85).move_to(DOWN * 1.75)

        self.play(FadeOut(subtitle), Write(heading))
        self.play(Write(valid))
        self.play(FadeIn(inner, shift=UP * 0.08))
        self.play(FadeIn(outer, shift=UP * 0.08))
        self.play(Write(example))
        self.wait(1.7)

        self.play(
            FadeOut(heading),
            FadeOut(valid),
            FadeOut(inner),
            FadeOut(outer),
            FadeOut(example),
        )

    def _base_product(self) -> tuple[VGroup, Matrix, Matrix, Matrix]:
        lesson = MATRIX_MATRIX_MULTIPLICATION_LESSON
        left = self._matrix(lesson.left, scale=0.73)
        right = self._matrix(lesson.right, scale=0.73)
        equals = MathTex("=").scale(0.9)
        result = self._matrix(lesson.result, scale=0.73)

        product = VGroup(left, right, equals, result).arrange(
            RIGHT,
            buff=0.36,
        )
        product.scale_to_fit_width(11.6)
        product.move_to(UP * 0.48)
        return product, left, right, result

    def _show_first_entry(self) -> None:
        heading = Text(
            "Row 1 with Column 1",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.1)

        product, left, right, result = self._base_product()

        row = left.get_rows()[0]
        column = right.get_columns()[0]
        result_entry = result.get_entries()[0]

        row_box = SurroundingRectangle(row, color=BLUE, buff=0.12)
        column_box = SurroundingRectangle(column, color=ORANGE, buff=0.12)

        calculation = MathTex(
            r"(1)(2)+(2)(-1)+(-1)(5)=-5",
            color=YELLOW,
        ).scale(0.7).move_to(DOWN * 1.28)

        location = MathTex(
            r"c_{11}=-5",
            color=GREEN,
        ).scale(0.78).move_to(DOWN * 2.0)

        self.play(Write(heading), FadeIn(product))
        self.play(FadeIn(row_box), FadeIn(column_box))
        self.play(Write(calculation))
        self.play(result_entry.animate.set_color(GREEN), Write(location))
        self.wait(1.5)

        self.play(
            FadeOut(heading),
            FadeOut(product),
            FadeOut(row_box),
            FadeOut(column_box),
            FadeOut(calculation),
            FadeOut(location),
        )

    def _show_remaining_entries(self) -> None:
        heading = Text(
            "Repeat for every row–column pair",
            weight="BOLD",
        ).scale(0.48).move_to(UP * 2.1)

        product, left, right, result = self._base_product()
        calculations = [
            (0, 1, r"(1)(1)+(2)(3)+(-1)(2)=5", BLUE),
            (1, 0, r"(3)(2)+(0)(-1)+(4)(5)=26", ORANGE),
            (1, 1, r"(3)(1)+(0)(3)+(4)(2)=11", RED),
        ]

        self.play(Write(heading), FadeIn(product))

        for row_index, column_index, expression, color in calculations:
            row_box = SurroundingRectangle(
                left.get_rows()[row_index],
                color=color,
                buff=0.12,
            )
            column_box = SurroundingRectangle(
                right.get_columns()[column_index],
                color=color,
                buff=0.12,
            )
            calculation = MathTex(
                expression,
                color=color,
            ).scale(0.68).move_to(DOWN * 1.35)

            result_entry = result.get_entries()[
                row_index * len(right.get_columns()) + column_index
            ]

            self.play(FadeIn(row_box), FadeIn(column_box))
            self.play(Write(calculation))
            self.play(result_entry.animate.set_color(color))
            self.wait(0.65)
            self.play(
                FadeOut(row_box),
                FadeOut(column_box),
                FadeOut(calculation),
            )

        final_label = MathTex(
            r"AB=\begin{bmatrix}-5&5\\26&11\end{bmatrix}",
            color=YELLOW,
        ).scale(0.82).move_to(DOWN * 1.7)

        self.play(Write(final_label))
        self.wait(1.5)

        self.play(
            FadeOut(heading),
            FadeOut(product),
            FadeOut(final_label),
        )

    def _state_general_rule(self) -> None:
        heading = Text(
            "General entry rule",
            weight="BOLD",
        ).scale(0.51).move_to(UP * 2.08)

        rule = MathTex(
            r"c_{ij}=\sum_{k=1}^{n}a_{ik}b_{kj}",
            color=YELLOW,
        ).scale(1.0).move_to(UP * 0.72)

        words = Text(
            "Entry (i, j) comes from row i of A and column j of B.",
        ).scale(0.43).move_to(DOWN * 0.35)

        order = Text(
            "Rows come from the left matrix; columns come from the right.",
        ).scale(0.4).move_to(DOWN * 1.15)

        warning = Text(
            "Matrix multiplication is not entrywise multiplication.",
        ).scale(0.41).move_to(DOWN * 1.92)

        self.play(Write(heading))
        self.play(Write(rule))
        self.play(FadeIn(words, shift=UP * 0.08))
        self.play(FadeIn(order, shift=UP * 0.08))
        self.play(FadeIn(warning, shift=UP * 0.08))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(rule),
            FadeOut(words),
            FadeOut(order),
            FadeOut(warning),
        )

    def _show_incompatible_product(self) -> None:
        heading = Text(
            "When multiplication is undefined",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.08)

        mismatch = MathTex(
            r"A_{2\times3}B_{2\times2}",
            color=RED,
        ).scale(0.95).move_to(UP * 0.7)

        explanation = Text(
            "A row of A has 3 entries, but a column of B has only 2.",
        ).scale(0.42).move_to(DOWN * 0.25)

        undefined = MathTex(
            r"AB\text{ is not defined}",
            color=RED,
        ).scale(0.9).move_to(DOWN * 1.15)

        contrast = Text(
            "Notice: equal matrix sizes are not required.",
        ).scale(0.41).move_to(DOWN * 1.95)

        self.play(Write(heading))
        self.play(Write(mismatch))
        self.play(FadeIn(explanation, shift=UP * 0.08))
        self.play(Write(undefined))
        self.play(FadeIn(contrast, shift=UP * 0.08))
        self.wait(1.7)

        self.play(
            FadeOut(heading),
            FadeOut(mismatch),
            FadeOut(explanation),
            FadeOut(undefined),
            FadeOut(contrast),
        )

    def _show_pause_predict_and_reflection(self) -> None:
        predict = Text(
            "Pause and Predict",
            weight="BOLD",
            color=YELLOW,
        ).scale(0.52).move_to(UP * 1.65)

        prompt = Text(
            "What is the upper-right entry of AB?",
        ).scale(0.47).move_to(UP * 0.82)

        a_label = MathTex("A=").scale(0.74)
        a_matrix = self._matrix(((1, 2), (0, -1)), scale=0.66)
        b_label = MathTex(r",\quad B=").scale(0.74)
        b_matrix = self._matrix(((3, 4), (5, -2)), scale=0.66)

        example = VGroup(
            a_label,
            a_matrix,
            b_label,
            b_matrix,
        ).arrange(RIGHT, buff=0.18)
        example.scale_to_fit_width(8.0)
        example.move_to(DOWN * 0.12)

        answer = MathTex(
            r"(1)(4)+(2)(-2)=0",
            color=GREEN,
        ).scale(0.84).move_to(DOWN * 1.5)

        self.play(Write(predict), FadeIn(prompt), FadeIn(example))
        self.wait(2.2)
        self.play(Write(answer))
        self.wait(1.2)

        self.play(
            FadeOut(predict),
            FadeOut(prompt),
            FadeOut(example),
            FadeOut(answer),
        )

        reflection = Text(
            "Each entry of AB is a row–column dot product.",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 0.62)

        dimension_summary = Text(
            "Inner dimensions must match; outer dimensions survive.",
        ).scale(0.42).move_to(DOWN * 0.05)

        next_lesson = Text(
            "Next: matrix multiplication as composition of transformations.",
        ).scale(0.4).move_to(DOWN * 0.82)

        self.play(Write(reflection))
        self.play(FadeIn(dimension_summary, shift=UP * 0.08))
        self.play(FadeIn(next_lesson, shift=UP * 0.08))
        self.wait(2.0)
