"""CP101 Manim presentation: The Trace of a Matrix."""

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

from engine.matrix_trace import MATRIX_TRACE_LESSON


class MatrixTracePresentation(Scene):
    """Introduce trace and its elementary properties."""

    TITLE = "The Trace of a Matrix"

    @staticmethod
    def _matrix(data, *, scale: float = 0.76) -> Matrix:
        matrix = Matrix(
            [[str(value) for value in row] for row in data],
            h_buff=0.92,
            v_buff=0.64,
        )
        return matrix.scale(scale)

    def construct(self) -> None:
        title = Text(self.TITLE, weight="BOLD").scale(0.67)
        title.to_edge(UP, buff=0.28)
        subtitle = Text(
            "A square matrix produces one number",
        ).scale(0.42)
        subtitle.next_to(title, DOWN, buff=0.16)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.1))
        self.wait(0.8)

        self._introduce_trace(subtitle)
        self._contrast_output_types()
        self._show_square_requirement()
        self._show_linearity()
        self._show_product_property()
        self._show_pause_predict_and_reflection()

    def _introduce_trace(self, subtitle: Text) -> None:
        lesson = MATRIX_TRACE_LESSON
        heading = Text(
            "Add the entries on the main diagonal",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.08)

        matrix = self._matrix(lesson.matrix, scale=0.78)
        matrix.move_to(UP * 0.35)

        entries = matrix.get_entries()
        diagonal_indices = (0, 4, 8)
        colors = (BLUE, ORANGE, GREEN)

        boxes = VGroup()
        for index, color in zip(diagonal_indices, colors):
            entries[index].set_color(color)
            boxes.add(
                SurroundingRectangle(
                    entries[index],
                    color=color,
                    buff=0.1,
                )
            )

        calculation = MathTex(
            r"\operatorname{tr}(A)=3+5+6=14",
            color=YELLOW,
        ).scale(0.88).move_to(DOWN * 1.45)

        definition = MathTex(
            r"\operatorname{tr}(A)=\sum_{i=1}^{n}a_{ii}",
        ).scale(0.82).move_to(DOWN * 2.15)

        self.play(FadeOut(subtitle), Write(heading))
        self.play(FadeIn(matrix))
        self.play(FadeIn(boxes))
        self.play(Write(calculation))
        self.play(Write(definition))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(matrix),
            FadeOut(boxes),
            FadeOut(calculation),
            FadeOut(definition),
        )

    def _contrast_output_types(self) -> None:
        heading = Text(
            "Trace is different from the operations we have used",
            weight="BOLD",
        ).scale(0.45).move_to(UP * 2.08)

        comparisons = VGroup(
            MathTex(r"A+B\longrightarrow\text{matrix}"),
            MathTex(r"cA\longrightarrow\text{matrix}"),
            MathTex(r"AB\longrightarrow\text{matrix}"),
            MathTex(
                r"\operatorname{tr}(A)\longrightarrow\text{number}",
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.34)
        comparisons.scale(0.78).move_to(UP * 0.1)

        note = Text(
            "Trace is a scalar-valued function of a matrix.",
        ).scale(0.42).move_to(DOWN * 1.85)

        self.play(Write(heading))
        for line in comparisons:
            self.play(Write(line), run_time=0.48)
        self.play(FadeIn(note, shift=UP * 0.08))
        self.wait(1.6)

        self.play(
            FadeOut(heading),
            FadeOut(comparisons),
            FadeOut(note),
        )

    def _show_square_requirement(self) -> None:
        lesson = MATRIX_TRACE_LESSON
        heading = Text(
            "Trace requires a square matrix",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.08)

        rectangular = self._matrix(lesson.rectangular_matrix, scale=0.75)
        rectangular.move_to(UP * 0.45)

        shape = MathTex(
            r"2\times3",
            color=RED,
        ).scale(0.85).move_to(DOWN * 0.65)

        explanation = Text(
            "There is no complete main diagonal with one entry from every row and column.",
        ).scale(0.37)
        explanation.scale_to_fit_width(11.2)
        explanation.move_to(DOWN * 1.45)

        undefined = MathTex(
            r"\operatorname{tr}(A)\text{ is not defined}",
            color=RED,
        ).scale(0.82).move_to(DOWN * 2.12)

        self.play(Write(heading))
        self.play(FadeIn(rectangular))
        self.play(Write(shape))
        self.play(FadeIn(explanation, shift=UP * 0.08))
        self.play(Write(undefined))
        self.wait(1.7)

        self.play(
            FadeOut(heading),
            FadeOut(rectangular),
            FadeOut(shape),
            FadeOut(explanation),
            FadeOut(undefined),
        )

    def _show_linearity(self) -> None:
        lesson = MATRIX_TRACE_LESSON
        heading = Text(
            "Trace respects addition and scalar multiplication",
            weight="BOLD",
        ).scale(0.45).move_to(UP * 2.08)

        addition = MathTex(
            r"\operatorname{tr}(A+B)"
            r"=\operatorname{tr}(A)+\operatorname{tr}(B)",
            color=YELLOW,
        ).scale(0.8).move_to(UP * 0.8)

        addition_numbers = MathTex(
            rf"{lesson.sum_trace}={lesson.trace_sum}",
        ).scale(0.78).move_to(UP * 0.05)

        scaling = MathTex(
            r"\operatorname{tr}(cA)=c\,\operatorname{tr}(A)",
            color=YELLOW,
        ).scale(0.82).move_to(DOWN * 0.85)

        scaling_numbers = MathTex(
            rf"{lesson.scaled_trace}={lesson.scalar_trace}",
        ).scale(0.78).move_to(DOWN * 1.58)

        explanation = Text(
            "Both rules follow because trace simply adds diagonal entries.",
        ).scale(0.39).move_to(DOWN * 2.22)

        self.play(Write(heading))
        self.play(Write(addition))
        self.play(Write(addition_numbers))
        self.play(Write(scaling))
        self.play(Write(scaling_numbers))
        self.play(FadeIn(explanation, shift=UP * 0.08))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(addition),
            FadeOut(addition_numbers),
            FadeOut(scaling),
            FadeOut(scaling_numbers),
            FadeOut(explanation),
        )

    def _show_product_property(self) -> None:
        lesson = MATRIX_TRACE_LESSON
        heading = Text(
            "Reversing the factors changes the matrix—but not the trace",
            weight="BOLD",
        ).scale(0.42).move_to(UP * 2.08)

        ab_label = MathTex("AB=").scale(0.75)
        ab_matrix = self._matrix(lesson.ab, scale=0.65)
        ba_label = MathTex(r",\qquad BA=").scale(0.75)
        ba_matrix = self._matrix(lesson.ba, scale=0.65)

        products = VGroup(
            ab_label,
            ab_matrix,
            ba_label,
            ba_matrix,
        ).arrange(RIGHT, buff=0.18)
        products.scale_to_fit_width(10.4)
        products.move_to(UP * 0.55)

        unequal = MathTex(
            r"AB\neq BA",
            color=RED,
        ).scale(0.86).move_to(DOWN * 0.55)

        equal_trace = MathTex(
            r"\operatorname{tr}(AB)=\operatorname{tr}(BA)",
            color=YELLOW,
        ).scale(0.84).move_to(DOWN * 1.35)

        numbers = MathTex(
            rf"{lesson.trace_ab}={lesson.trace_ba}",
            color=GREEN,
        ).scale(0.8).move_to(DOWN * 2.05)

        self.play(Write(heading))
        self.play(FadeIn(products))
        self.play(Write(unequal))
        self.play(Write(equal_trace))
        self.play(Write(numbers))
        self.wait(1.9)

        self.play(
            FadeOut(heading),
            FadeOut(products),
            FadeOut(unequal),
            FadeOut(equal_trace),
            FadeOut(numbers),
        )

    def _show_pause_predict_and_reflection(self) -> None:
        predict = Text(
            "Pause and Predict",
            weight="BOLD",
            color=YELLOW,
        ).scale(0.52).move_to(UP * 1.65)

        prompt = Text(
            "What is the trace of A?",
        ).scale(0.47).move_to(UP * 0.82)

        a_label = MathTex("A=").scale(0.75)
        matrix = self._matrix(((4, -1, 2), (0, 3, 5), (7, 1, -2)), scale=0.67)
        example = VGroup(a_label, matrix).arrange(RIGHT, buff=0.2)
        example.move_to(DOWN * 0.18)

        answer = MathTex(
            r"4+3+(-2)=5",
            color=GREEN,
        ).scale(0.86).move_to(DOWN * 1.5)

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
            "Trace adds the main-diagonal entries of a square matrix.",
            weight="BOLD",
        ).scale(0.46).move_to(UP * 0.72)

        product_note = Text(
            "AB and BA can differ even though their traces agree.",
        ).scale(0.42).move_to(DOWN * 0.02)

        future = Text(
            "Later, trace will reveal information about eigenvalues.",
        ).scale(0.4).move_to(DOWN * 0.78)

        next_lesson = Text(
            "Next: matrix transposition.",
        ).scale(0.4).move_to(DOWN * 1.5)

        self.play(Write(reflection))
        self.play(FadeIn(product_note, shift=UP * 0.08))
        self.play(FadeIn(future, shift=UP * 0.08))
        self.play(FadeIn(next_lesson, shift=UP * 0.08))
        self.wait(2.0)
