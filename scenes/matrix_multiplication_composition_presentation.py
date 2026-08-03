"""CP100 Manim presentation: Matrix Multiplication as Composition."""

from __future__ import annotations

from manim import (
    Axes,
    BLUE,
    Create,
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
    Text,
    Transform,
    UP,
    VGroup,
    Vector,
    Write,
    YELLOW,
)

from engine.matrix_multiplication_composition import (
    MATRIX_COMPOSITION_LESSON,
)


class MatrixMultiplicationCompositionPresentation(Scene):
    """Show that BA applies A first and then B."""

    TITLE = "Matrix Multiplication as Composition"

    @staticmethod
    def _matrix(data, *, scale: float = 0.76) -> Matrix:
        matrix = Matrix(
            [[str(value) for value in row] for row in data],
            h_buff=1.0,
            v_buff=0.66,
        )
        return matrix.scale(scale)

    def construct(self) -> None:
        title = Text(self.TITLE, weight="BOLD").scale(0.64)
        title.to_edge(UP, buff=0.28)
        subtitle = Text(
            "One transformation after another",
        ).scale(0.42)
        subtitle.next_to(title, DOWN, buff=0.16)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.1))
        self.wait(0.8)

        self._introduce_sequence(subtitle)
        self._show_geometric_composition()
        self._show_symbolic_composition()
        self._show_product_matrix()
        self._explain_order()
        self._show_pause_predict_and_reflection()

    def _introduce_sequence(self, subtitle: Text) -> None:
        heading = Text(
            "Apply A first, then apply B",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.05)

        x = MathTex(r"\mathbf{x}").scale(0.95)
        arrow_one = MathTex(r"\xrightarrow{\ A\ }").scale(0.9)
        ax = MathTex(r"A\mathbf{x}").scale(0.95)
        arrow_two = MathTex(r"\xrightarrow{\ B\ }").scale(0.9)
        bax = MathTex(r"B(A\mathbf{x})").scale(0.95)

        sequence = VGroup(
            x,
            arrow_one,
            ax,
            arrow_two,
            bax,
        ).arrange(RIGHT, buff=0.42)
        sequence.scale_to_fit_width(10.8)
        sequence.move_to(UP * 0.45)

        words = Text(
            "The output of A becomes the input to B.",
        ).scale(0.43).move_to(DOWN * 0.65)

        compact = MathTex(
            r"B(A\mathbf{x})=(BA)\mathbf{x}",
            color=YELLOW,
        ).scale(0.92).move_to(DOWN * 1.55)

        self.play(FadeOut(subtitle), Write(heading))
        self.play(FadeIn(sequence))
        self.play(FadeIn(words, shift=UP * 0.08))
        self.play(Write(compact))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(sequence),
            FadeOut(words),
            FadeOut(compact),
        )

    def _show_geometric_composition(self) -> None:
        lesson = MATRIX_COMPOSITION_LESSON
        heading = Text(
            "Watch the vector move through two transformations",
            weight="BOLD",
        ).scale(0.46).move_to(UP * 2.12)

        axes = Axes(
            x_range=[-4, 5, 1],
            y_range=[-1, 4, 1],
            x_length=8.2,
            y_length=4.8,
            tips=False,
        ).scale(0.8).move_to(DOWN * 0.2)

        start = Vector(lesson.vector, color=BLUE)
        start.shift(axes.c2p(0, 0) - start.get_start())

        after_first = Vector(lesson.after_first, color=ORANGE)
        after_first.shift(axes.c2p(0, 0) - after_first.get_start())

        after_second = Vector(lesson.after_second, color=GREEN)
        after_second.shift(axes.c2p(0, 0) - after_second.get_start())

        start_label = MathTex(r"\mathbf{x}=(2,1)", color=BLUE).scale(0.62)
        start_label.move_to(LEFT * 4.6 + UP * 1.45)

        first_label = MathTex(
            r"A\mathbf{x}=(3,1)",
            color=ORANGE,
        ).scale(0.62).move_to(LEFT * 4.5 + UP * 0.78)

        second_label = MathTex(
            r"B(A\mathbf{x})=(-3,1)",
            color=GREEN,
        ).scale(0.62).move_to(LEFT * 4.25 + UP * 0.1)

        operation_one = Text(
            "A: horizontal shear",
        ).scale(0.36).move_to(RIGHT * 4.3 + UP * 1.0)

        operation_two = Text(
            "B: reflect across the y-axis",
        ).scale(0.36).move_to(RIGHT * 4.0 + UP * 0.35)

        self.play(Write(heading), Create(axes))
        self.play(Create(start), FadeIn(start_label))
        self.wait(0.6)
        self.play(FadeIn(operation_one))
        self.play(Transform(start, after_first), FadeIn(first_label))
        self.wait(0.8)
        self.play(FadeIn(operation_two))
        self.play(Transform(start, after_second), FadeIn(second_label))
        self.wait(1.5)

        self.play(
            FadeOut(heading),
            FadeOut(axes),
            FadeOut(start),
            FadeOut(start_label),
            FadeOut(first_label),
            FadeOut(second_label),
            FadeOut(operation_one),
            FadeOut(operation_two),
        )

    def _show_symbolic_composition(self) -> None:
        lesson = MATRIX_COMPOSITION_LESSON
        heading = Text(
            "The same sequence in matrix form",
            weight="BOLD",
        ).scale(0.49).move_to(UP * 2.1)

        b_matrix = self._matrix(lesson.second_matrix, scale=0.7)
        a_matrix = self._matrix(lesson.first_matrix, scale=0.7)
        x_vector = self._matrix(
            ((lesson.vector[0],), (lesson.vector[1],)),
            scale=0.7,
        )

        expression = VGroup(
            b_matrix,
            a_matrix,
            x_vector,
        ).arrange(RIGHT, buff=0.25)
        expression.scale_to_fit_width(6.8)
        expression.move_to(UP * 0.55)

        annotation = Text(
            "Read from right to left: x, then A, then B.",
        ).scale(0.42).move_to(DOWN * 0.62)

        result = MathTex(
            r"B(A\mathbf{x})="
            r"\begin{bmatrix}-3\\1\end{bmatrix}",
            color=YELLOW,
        ).scale(0.84).move_to(DOWN * 1.55)

        self.play(Write(heading))
        self.play(FadeIn(expression))
        self.play(FadeIn(annotation, shift=UP * 0.08))
        self.play(Write(result))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(expression),
            FadeOut(annotation),
            FadeOut(result),
        )

    def _show_product_matrix(self) -> None:
        lesson = MATRIX_COMPOSITION_LESSON
        heading = Text(
            "Combine the two transformations into one matrix",
            weight="BOLD",
        ).scale(0.46).move_to(UP * 2.08)

        b_matrix = self._matrix(lesson.second_matrix, scale=0.68)
        a_matrix = self._matrix(lesson.first_matrix, scale=0.68)
        equals = MathTex("=").scale(0.9)
        product = self._matrix(lesson.product_matrix, scale=0.68)

        equation = VGroup(
            b_matrix,
            a_matrix,
            equals,
            product,
        ).arrange(RIGHT, buff=0.34)
        equation.scale_to_fit_width(9.4)
        equation.move_to(UP * 0.55)

        calculation = MathTex(
            r"BA="
            r"\begin{bmatrix}-1&-1\\0&1\end{bmatrix}",
            color=YELLOW,
        ).scale(0.82).move_to(DOWN * 1.0)

        verification = MathTex(
            r"(BA)\mathbf{x}"
            r"=\begin{bmatrix}-1&-1\\0&1\end{bmatrix}"
            r"\begin{bmatrix}2\\1\end{bmatrix}"
            r"=\begin{bmatrix}-3\\1\end{bmatrix}",
        ).scale(0.68).move_to(DOWN * 2.03)

        self.play(Write(heading))
        self.play(FadeIn(equation))
        self.play(Write(calculation))
        self.play(Write(verification))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(equation),
            FadeOut(calculation),
            FadeOut(verification),
        )

    def _explain_order(self) -> None:
        heading = Text(
            "Why does the rightmost matrix act first?",
            weight="BOLD",
        ).scale(0.48).move_to(UP * 2.08)

        expression = MathTex(
            r"(BA)\mathbf{x}=B(A\mathbf{x})",
            color=YELLOW,
        ).scale(1.0).move_to(UP * 0.7)

        first = Text(
            "A must act on x before B has anything to transform.",
        ).scale(0.42).move_to(DOWN * 0.25)

        caution = Text(
            "The written order records the nesting of the operations.",
        ).scale(0.41).move_to(DOWN * 1.0)

        preview = Text(
            "Changing the order usually changes the result.",
        ).scale(0.43).move_to(DOWN * 1.78)

        self.play(Write(heading))
        self.play(Write(expression))
        self.play(FadeIn(first, shift=UP * 0.08))
        self.play(FadeIn(caution, shift=UP * 0.08))
        self.play(FadeIn(preview, shift=UP * 0.08))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(expression),
            FadeOut(first),
            FadeOut(caution),
            FadeOut(preview),
        )

    def _show_pause_predict_and_reflection(self) -> None:
        predict = Text(
            "Pause and Predict",
            weight="BOLD",
            color=YELLOW,
        ).scale(0.52).move_to(UP * 1.65)

        prompt = Text(
            "In CBx, which matrix acts first?",
        ).scale(0.47).move_to(UP * 0.82)

        expression = MathTex(
            r"CB\mathbf{x}=C(B\mathbf{x})",
        ).scale(0.95).move_to(DOWN * 0.05)

        answer = Text(
            "B acts first.",
            color=GREEN,
            weight="BOLD",
        ).scale(0.5).move_to(DOWN * 1.25)

        self.play(Write(predict), FadeIn(prompt), Write(expression))
        self.wait(2.2)
        self.play(FadeIn(answer, shift=UP * 0.08))
        self.wait(1.2)

        self.play(
            FadeOut(predict),
            FadeOut(prompt),
            FadeOut(expression),
            FadeOut(answer),
        )

        reflection = Text(
            "Matrix multiplication represents composition.",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 0.62)

        order = Text(
            "In BAx, A acts first and B acts second.",
        ).scale(0.43).move_to(DOWN * 0.05)

        next_lesson = Text(
            "Next: why reversing the order usually changes the result.",
        ).scale(0.4).move_to(DOWN * 0.82)

        self.play(Write(reflection))
        self.play(FadeIn(order, shift=UP * 0.08))
        self.play(FadeIn(next_lesson, shift=UP * 0.08))
        self.wait(2.0)
