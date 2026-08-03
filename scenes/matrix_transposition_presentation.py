"""CP102 Manim presentation: Matrix Transposition."""

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
    Transform,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from engine.matrix_transposition import MATRIX_TRANSPOSITION_LESSON


class MatrixTranspositionPresentation(Scene):
    """Introduce transpose as exchanging rows and columns."""

    TITLE = "Matrix Transposition"

    @staticmethod
    def _matrix(data, *, scale: float = 0.74) -> Matrix:
        matrix = Matrix(
            [[str(value) for value in row] for row in data],
            h_buff=0.94,
            v_buff=0.64,
        )
        return matrix.scale(scale)

    def construct(self) -> None:
        title = Text(self.TITLE, weight="BOLD").scale(0.67)
        title.to_edge(UP, buff=0.28)
        subtitle = Text(
            "Rows become columns",
        ).scale(0.42)
        subtitle.next_to(title, DOWN, buff=0.16)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.1))
        self.wait(0.8)

        self._introduce_transpose(subtitle)
        self._show_entry_rule()
        self._show_dimension_reversal()
        self._show_basic_properties()
        self._show_product_reversal()
        self._show_symmetric_matrices()
        self._show_pause_predict_and_reflection()

    def _introduce_transpose(self, subtitle: Text) -> None:
        lesson = MATRIX_TRANSPOSITION_LESSON
        heading = Text(
            "Turn each row into a column",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.08)

        original = self._matrix(lesson.matrix, scale=0.76)
        arrow = MathTex(r"\longrightarrow").scale(0.9)
        transposed = self._matrix(lesson.transposed, scale=0.76)

        display = VGroup(original, arrow, transposed).arrange(
            RIGHT, buff=0.5
        )
        display.scale_to_fit_width(10.8)
        display.move_to(UP * 0.35)

        first_row_box = SurroundingRectangle(
            original.get_rows()[0],
            color=BLUE,
            buff=0.12,
        )
        first_column_box = SurroundingRectangle(
            transposed.get_columns()[0],
            color=BLUE,
            buff=0.12,
        )

        second_row_box = SurroundingRectangle(
            original.get_rows()[1],
            color=ORANGE,
            buff=0.12,
        )
        second_column_box = SurroundingRectangle(
            transposed.get_columns()[1],
            color=ORANGE,
            buff=0.12,
        )

        notation = MathTex(
            r"A\longrightarrow A^T",
            color=YELLOW,
        ).scale(0.9).move_to(DOWN * 1.65)

        self.play(FadeOut(subtitle), Write(heading))
        self.play(FadeIn(display))
        self.play(FadeIn(first_row_box), FadeIn(first_column_box))
        self.wait(0.8)
        self.play(FadeIn(second_row_box), FadeIn(second_column_box))
        self.play(Write(notation))
        self.wait(1.6)

        self.play(
            FadeOut(heading),
            FadeOut(display),
            FadeOut(first_row_box),
            FadeOut(first_column_box),
            FadeOut(second_row_box),
            FadeOut(second_column_box),
            FadeOut(notation),
        )

    def _show_entry_rule(self) -> None:
        heading = Text(
            "Entry (i, j) moves to position (j, i)",
            weight="BOLD",
        ).scale(0.47).move_to(UP * 2.08)

        rule = MathTex(
            r"(A^T)_{ij}=a_{ji}",
            color=YELLOW,
        ).scale(1.0).move_to(UP * 0.65)

        example = MathTex(
            r"a_{23}=4\quad\Longrightarrow\quad (A^T)_{32}=4",
        ).scale(0.84).move_to(DOWN * 0.35)

        diagonal = Text(
            "Entries on the main diagonal stay in place.",
        ).scale(0.42).move_to(DOWN * 1.25)

        self.play(Write(heading))
        self.play(Write(rule))
        self.play(Write(example))
        self.play(FadeIn(diagonal, shift=UP * 0.08))
        self.wait(1.7)

        self.play(
            FadeOut(heading),
            FadeOut(rule),
            FadeOut(example),
            FadeOut(diagonal),
        )

    def _show_dimension_reversal(self) -> None:
        heading = Text(
            "Transposition reverses the dimensions",
            weight="BOLD",
        ).scale(0.49).move_to(UP * 2.08)

        dimensions = MathTex(
            r"A_{m\times n}\longrightarrow A^T_{n\times m}",
            color=YELLOW,
        ).scale(0.95).move_to(UP * 0.65)

        example = MathTex(
            r"2\times3\longrightarrow3\times2",
        ).scale(0.9).move_to(DOWN * 0.35)

        double = MathTex(
            r"(A^T)^T=A",
        ).scale(0.9).move_to(DOWN * 1.35)

        words = Text(
            "Transposing twice returns the original matrix.",
        ).scale(0.41).move_to(DOWN * 2.02)

        self.play(Write(heading))
        self.play(Write(dimensions))
        self.play(Write(example))
        self.play(Write(double))
        self.play(FadeIn(words, shift=UP * 0.08))
        self.wait(1.7)

        self.play(
            FadeOut(heading),
            FadeOut(dimensions),
            FadeOut(example),
            FadeOut(double),
            FadeOut(words),
        )

    def _show_basic_properties(self) -> None:
        heading = Text(
            "Transpose respects addition and scalar multiplication",
            weight="BOLD",
        ).scale(0.44).move_to(UP * 2.08)

        addition = MathTex(
            r"(A+B)^T=A^T+B^T",
            color=YELLOW,
        ).scale(0.9).move_to(UP * 0.72)

        scaling = MathTex(
            r"(cA)^T=cA^T",
            color=YELLOW,
        ).scale(0.9).move_to(DOWN * 0.2)

        explanation = Text(
            "Each rule works because entries simply change positions.",
        ).scale(0.41).move_to(DOWN * 1.2)

        self.play(Write(heading))
        self.play(Write(addition))
        self.play(Write(scaling))
        self.play(FadeIn(explanation, shift=UP * 0.08))
        self.wait(1.7)

        self.play(
            FadeOut(heading),
            FadeOut(addition),
            FadeOut(scaling),
            FadeOut(explanation),
        )

    def _show_product_reversal(self) -> None:
        lesson = MATRIX_TRANSPOSITION_LESSON
        heading = Text(
            "The transpose of a product reverses the order",
            weight="BOLD",
        ).scale(0.46).move_to(UP * 2.08)

        law = MathTex(
            r"(AB)^T=B^TA^T",
            color=YELLOW,
        ).scale(0.95).move_to(UP * 1.18)

        proof_heading = Text(
            "Proof by comparing the (i, j) entries",
            weight="BOLD",
        ).scale(0.38).move_to(UP * 0.48)

        proof_line_one = MathTex(
            r"\bigl((AB)^T\bigr)_{ij}"
            r"=(AB)_{ji}"
            r"=\sum_k a_{jk}b_{ki}",
        ).scale(0.68).move_to(DOWN * 0.12)

        proof_line_two = MathTex(
            r"\sum_k a_{jk}b_{ki}"
            r"=\sum_k (B^T)_{ik}(A^T)_{kj}"
            r"=(B^TA^T)_{ij}",
            color=YELLOW,
        ).scale(0.65).move_to(DOWN * 0.82)

        conclusion = Text(
            "Every corresponding entry is equal, so the matrices are equal.",
        ).scale(0.36).move_to(DOWN * 1.48)

        self.play(Write(heading))
        self.play(Write(law))
        self.play(FadeIn(proof_heading, shift=UP * 0.06))
        self.play(Write(proof_line_one))
        self.play(Write(proof_line_two))
        self.play(FadeIn(conclusion, shift=UP * 0.06))
        self.wait(2.0)

        self.play(
            FadeOut(proof_heading),
            FadeOut(proof_line_one),
            FadeOut(proof_line_two),
            FadeOut(conclusion),
        )

        left_label = MathTex(r"(AB)^T=").scale(0.72)
        left_matrix = self._matrix(lesson.transpose_product, scale=0.62)
        right_label = MathTex(r",\qquad B^TA^T=").scale(0.72)
        right_matrix = self._matrix(
            lesson.reversed_transpose_product,
            scale=0.62,
        )

        comparison = VGroup(
            left_label,
            left_matrix,
            right_label,
            right_matrix,
        ).arrange(RIGHT, buff=0.16)
        comparison.scale_to_fit_width(10.6)
        comparison.move_to(DOWN * 0.2)

        reason = Text(
            "The numerical example confirms the entry-by-entry proof.",
        ).scale(0.39).move_to(DOWN * 1.62)

        self.play(FadeIn(comparison))
        self.play(FadeIn(reason, shift=UP * 0.08))
        self.wait(1.7)

        self.play(
            FadeOut(heading),
            FadeOut(law),
            FadeOut(comparison),
            FadeOut(reason),
        )

    def _show_symmetric_matrices(self) -> None:
        lesson = MATRIX_TRANSPOSITION_LESSON
        heading = Text(
            "Some matrices are unchanged by transposition",
            weight="BOLD",
        ).scale(0.45).move_to(UP * 2.08)

        matrix = self._matrix(lesson.symmetric_matrix, scale=0.7)
        matrix.move_to(UP * 0.35)

        property_line = MathTex(
            r"A^T=A",
            color=YELLOW,
        ).scale(0.95).move_to(DOWN * 1.15)

        name = Text(
            "Such a matrix is called symmetric.",
        ).scale(0.43).move_to(DOWN * 1.9)

        self.play(Write(heading))
        self.play(FadeIn(matrix))
        self.play(Write(property_line))
        self.play(FadeIn(name, shift=UP * 0.08))
        self.wait(1.7)

        self.play(
            FadeOut(heading),
            FadeOut(matrix),
            FadeOut(property_line),
            FadeOut(name),
        )

    def _show_pause_predict_and_reflection(self) -> None:
        predict = Text(
            "Pause and Predict",
            weight="BOLD",
            color=YELLOW,
        ).scale(0.52).move_to(UP * 1.65)

        prompt = Text(
            "What is the size of A transpose?",
        ).scale(0.47).move_to(UP * 0.82)

        given = MathTex(
            r"A\text{ is }4\times7",
        ).scale(0.9).move_to(DOWN * 0.05)

        answer = MathTex(
            r"A^T\text{ is }7\times4",
            color=GREEN,
        ).scale(0.9).move_to(DOWN * 1.22)

        self.play(Write(predict), FadeIn(prompt), Write(given))
        self.wait(2.2)
        self.play(Write(answer))
        self.wait(1.2)

        self.play(
            FadeOut(predict),
            FadeOut(prompt),
            FadeOut(given),
            FadeOut(answer),
        )

        reflection = Text(
            "Transposition exchanges rows and columns.",
            weight="BOLD",
        ).scale(0.49).move_to(UP * 0.72)

        product = Text(
            "For products, it also reverses the order of the factors.",
        ).scale(0.41).move_to(DOWN * 0.02)

        next_lesson = Text(
            "Next: order, identity, and undoing.",
        ).scale(0.4).move_to(DOWN * 0.8)

        self.play(Write(reflection))
        self.play(FadeIn(product, shift=UP * 0.08))
        self.play(FadeIn(next_lesson, shift=UP * 0.08))
        self.wait(2.0)
