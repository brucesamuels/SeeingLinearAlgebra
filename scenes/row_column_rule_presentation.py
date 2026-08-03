"""CP98 Manim presentation: The Row-Column Rule."""

from __future__ import annotations

from manim import (
    BLUE,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
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

from engine.row_column_rule import (
    ROW_COLUMN_RULE_LESSON,
    row_computations,
)


class RowColumnRulePresentation(Scene):
    """Connect column combinations to row-dot-vector computations."""

    TITLE = "The Row–Column Rule"

    @staticmethod
    def _matrix(data, *, scale: float = 0.82) -> Matrix:
        matrix = Matrix(
            [[str(value) for value in row] for row in data],
            h_buff=0.86,
            v_buff=0.62,
        )
        return matrix.scale(scale)

    @staticmethod
    def _column_vector(data, *, scale: float = 0.82) -> Matrix:
        matrix = Matrix(
            [[str(value)] for value in data],
            h_buff=0.72,
            v_buff=0.62,
        )
        return matrix.scale(scale)

    def construct(self) -> None:
        title = Text(self.TITLE, weight="BOLD").scale(0.68)
        title.to_edge(UP, buff=0.28)
        subtitle = Text(
            "Each output entry comes from one row",
        ).scale(0.42)
        subtitle.next_to(title, DOWN, buff=0.16)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.1))
        self.wait(0.8)

        self._connect_to_column_combination(subtitle)
        self._show_first_row_computation()
        self._show_second_row_computation()
        self._state_general_rule()
        self._show_dimension_logic()
        self._show_pause_predict_and_reflection()

    def _connect_to_column_combination(self, subtitle: Text) -> None:
        heading = Text(
            "The same product, viewed two ways",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.05)

        column_view = MathTex(
            r"A\mathbf{x}"
            r"=x_1\mathbf{a}_1+x_2\mathbf{a}_2+x_3\mathbf{a}_3",
            color=YELLOW,
        ).scale(0.8).move_to(UP * 0.62)

        row_view = MathTex(
            r"A\mathbf{x}"
            r"=\begin{bmatrix}"
            r"\text{row}_1(A)\cdot\mathbf{x}\\"
            r"\text{row}_2(A)\cdot\mathbf{x}"
            r"\end{bmatrix}",
        ).scale(0.78).move_to(DOWN * 0.8)

        bridge = Text(
            "Column combinations build the vector; rows compute its entries.",
        ).scale(0.4).move_to(DOWN * 2.05)

        self.play(FadeOut(subtitle), Write(heading))
        self.play(Write(column_view))
        self.play(Write(row_view))
        self.play(FadeIn(bridge, shift=UP * 0.08))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(column_view),
            FadeOut(row_view),
            FadeOut(bridge),
        )

    def _base_product(self) -> tuple[VGroup, Matrix, Matrix, Matrix]:
        lesson = ROW_COLUMN_RULE_LESSON
        matrix = self._matrix(lesson.matrix, scale=0.82)
        vector = self._column_vector(lesson.vector, scale=0.82)
        equals = MathTex("=").scale(0.9)
        result = self._column_vector(lesson.result, scale=0.82)

        product = VGroup(
            matrix,
            vector,
            equals,
            result,
        ).arrange(RIGHT, buff=0.42)
        product.scale_to_fit_width(10.2)
        product.move_to(UP * 0.52)
        return product, matrix, vector, result

    def _show_first_row_computation(self) -> None:
        heading = Text(
            "First row gives the first output entry",
            weight="BOLD",
        ).scale(0.48).move_to(UP * 2.12)

        product, matrix, vector, result = self._base_product()
        first = row_computations(
            ROW_COLUMN_RULE_LESSON.matrix,
            ROW_COLUMN_RULE_LESSON.vector,
        )[0]

        row_entries = matrix.get_rows()[0]
        vector_entries = vector.get_entries()
        result_entry = result.get_entries()[0]

        row_box = SurroundingRectangle(
            row_entries,
            color=BLUE,
            buff=0.12,
        )
        vector_box = SurroundingRectangle(
            vector_entries,
            color=ORANGE,
            buff=0.12,
        )

        calculation = MathTex(
            r"(2)(3)+(-1)(2)+(3)(-1)=1",
            color=YELLOW,
        ).scale(0.72).move_to(DOWN * 1.25)

        label = MathTex(
            r"\text{row}_1(A)\cdot\mathbf{x}=1",
            color=GREEN,
        ).scale(0.72).move_to(DOWN * 2.0)

        self.play(Write(heading), FadeIn(product))
        self.play(FadeIn(row_box), FadeIn(vector_box))
        self.play(Write(calculation))
        self.play(result_entry.animate.set_color(GREEN), Write(label))
        self.wait(1.5)

        self.play(
            FadeOut(heading),
            FadeOut(product),
            FadeOut(row_box),
            FadeOut(vector_box),
            FadeOut(calculation),
            FadeOut(label),
        )

    def _show_second_row_computation(self) -> None:
        heading = Text(
            "Second row gives the second output entry",
            weight="BOLD",
        ).scale(0.48).move_to(UP * 2.12)

        product, matrix, vector, result = self._base_product()
        second = row_computations(
            ROW_COLUMN_RULE_LESSON.matrix,
            ROW_COLUMN_RULE_LESSON.vector,
        )[1]

        row_entries = matrix.get_rows()[1]
        vector_entries = vector.get_entries()
        result_entry = result.get_entries()[1]

        row_box = SurroundingRectangle(
            row_entries,
            color=RED,
            buff=0.12,
        )
        vector_box = SurroundingRectangle(
            vector_entries,
            color=ORANGE,
            buff=0.12,
        )

        calculation = MathTex(
            r"(1)(3)+(4)(2)+(-2)(-1)=13",
            color=YELLOW,
        ).scale(0.72).move_to(DOWN * 1.25)

        label = MathTex(
            r"\text{row}_2(A)\cdot\mathbf{x}=13",
            color=GREEN,
        ).scale(0.72).move_to(DOWN * 2.0)

        self.play(Write(heading), FadeIn(product))
        self.play(FadeIn(row_box), FadeIn(vector_box))
        self.play(Write(calculation))
        self.play(result_entry.animate.set_color(GREEN), Write(label))
        self.wait(1.5)

        self.play(
            FadeOut(heading),
            FadeOut(product),
            FadeOut(row_box),
            FadeOut(vector_box),
            FadeOut(calculation),
            FadeOut(label),
        )

    def _state_general_rule(self) -> None:
        heading = Text(
            "General row–column rule",
            weight="BOLD",
        ).scale(0.51).move_to(UP * 2.1)

        rule = MathTex(
            r"(A\mathbf{x})_i"
            r"=\sum_{j=1}^{n}a_{ij}x_j",
            color=YELLOW,
        ).scale(0.96).move_to(UP * 0.65)

        words = Text(
            "Output entry i is row i of A dotted with x.",
        ).scale(0.44).move_to(DOWN * 0.4)

        warning = Text(
            "Do not multiply entries merely because they are adjacent.",
        ).scale(0.4).move_to(DOWN * 1.2)

        sequence = Text(
            "Pair corresponding positions, multiply, then add.",
        ).scale(0.41).move_to(DOWN * 1.9)

        self.play(Write(heading))
        self.play(Write(rule))
        self.play(FadeIn(words, shift=UP * 0.08))
        self.play(FadeIn(warning, shift=UP * 0.08))
        self.play(FadeIn(sequence, shift=UP * 0.08))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(rule),
            FadeOut(words),
            FadeOut(warning),
            FadeOut(sequence),
        )

    def _show_dimension_logic(self) -> None:
        heading = Text(
            "Why must the inner dimensions match?",
            weight="BOLD",
        ).scale(0.49).move_to(UP * 2.1)

        valid = MathTex(
            r"A_{m\times n}\mathbf{x}_{n\times1}"
            r"=(A\mathbf{x})_{m\times1}",
            color=YELLOW,
        ).scale(0.9).move_to(UP * 0.72)

        explanation = Text(
            "Each row has n entries, so x must also have n entries.",
        ).scale(0.42).move_to(DOWN * 0.3)

        invalid = MathTex(
            r"A_{2\times3}\mathbf{x}_{2\times1}",
            color=RED,
        ).scale(0.9).move_to(DOWN * 1.15)

        invalid_note = Text(
            "A three-entry row cannot be dotted with a two-entry vector.",
        ).scale(0.39).move_to(DOWN * 1.9)

        self.play(Write(heading))
        self.play(Write(valid))
        self.play(FadeIn(explanation, shift=UP * 0.08))
        self.play(Write(invalid))
        self.play(FadeIn(invalid_note, shift=UP * 0.08))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(valid),
            FadeOut(explanation),
            FadeOut(invalid),
            FadeOut(invalid_note),
        )

    def _show_pause_predict_and_reflection(self) -> None:
        predict = Text(
            "Pause and Predict",
            weight="BOLD",
            color=YELLOW,
        ).scale(0.52).move_to(UP * 1.65)

        prompt = Text(
            "What is the second entry of A x?",
        ).scale(0.47).move_to(UP * 0.82)

        a_label = MathTex("A=").scale(0.75)
        a_matrix = self._matrix(((1, 2), (-3, 4)), scale=0.68)
        x_label = MathTex(r",\quad\mathbf{x}=").scale(0.75)
        x_vector = self._column_vector((5, -1), scale=0.68)

        example = VGroup(
            a_label,
            a_matrix,
            x_label,
            x_vector,
        ).arrange(RIGHT, buff=0.18)
        example.scale_to_fit_width(7.6)
        example.move_to(DOWN * 0.18)

        answer = MathTex(
            r"(-3)(5)+(4)(-1)=-19",
            color=GREEN,
        ).scale(0.82).move_to(DOWN * 1.5)

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
            "Each row of A computes one entry of A x.",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 0.62)

        connection = Text(
            "This is the same product we already built from the columns.",
        ).scale(0.42).move_to(DOWN * 0.05)

        next_lesson = Text(
            "Next: use the row–column rule to multiply two matrices.",
        ).scale(0.41).move_to(DOWN * 0.8)

        self.play(Write(reflection))
        self.play(FadeIn(connection, shift=UP * 0.08))
        self.play(FadeIn(next_lesson, shift=UP * 0.08))
        self.wait(2.0)
