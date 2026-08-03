"""CP103 Manim presentation: Order, Identity, and Undoing."""

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

from engine.matrix_order_identity_undoing import (
    MATRIX_ORDER_IDENTITY_UNDOING_LESSON,
)


class MatrixOrderIdentityUndoingPresentation(Scene):
    """Conceptual capstone for the Matrix Operations chapter."""

    TITLE = "Order, Identity, and Undoing"

    @staticmethod
    def _matrix(data, *, scale: float = 0.72) -> Matrix:
        matrix = Matrix(
            [[str(value) for value in row] for row in data],
            h_buff=0.94,
            v_buff=0.64,
        )
        return matrix.scale(scale)

    @staticmethod
    def _vector_from_origin(axes: Axes, coordinates, color):
        vector = Vector(coordinates, color=color)
        vector.shift(axes.c2p(0, 0) - vector.get_start())
        return vector

    def construct(self) -> None:
        title = Text(self.TITLE, weight="BOLD").scale(0.66)
        title.to_edge(UP, buff=0.28)
        subtitle = Text(
            "Does order matter? What does nothing? What can be undone?",
        ).scale(0.38)
        subtitle.next_to(title, DOWN, buff=0.16)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.1))
        self.wait(0.8)

        self._show_noncommutativity(subtitle)
        self._show_identity_matrix()
        self._show_undoing()
        self._show_pause_predict_and_reflection()

    def _show_noncommutativity(self, subtitle: Text) -> None:
        lesson = MATRIX_ORDER_IDENTITY_UNDOING_LESSON

        heading = Text(
            "Same two transformations, different order",
            weight="BOLD",
        ).scale(0.48).move_to(UP * 2.08)

        axes = Axes(
            x_range=[-4, 5, 1],
            y_range=[-1, 4, 1],
            x_length=8.0,
            y_length=4.8,
            tips=False,
        ).scale(0.78).move_to(DOWN * 0.15)

        start = self._vector_from_origin(axes, lesson.vector, BLUE)
        ba_final = self._vector_from_origin(
            axes,
            lesson.shear_then_reflection_vector,
            GREEN,
        )
        ab_final = self._vector_from_origin(
            axes,
            lesson.reflection_then_shear_vector,
            ORANGE,
        )

        start_label = MathTex(r"\mathbf{x}=(2,1)", color=BLUE).scale(0.6)
        start_label.move_to(LEFT * 4.5 + UP * 1.45)

        ba_label = MathTex(
            r"BA\mathbf{x}=(-3,1)",
            color=GREEN,
        ).scale(0.6).move_to(LEFT * 4.15 + UP * 0.8)

        ab_label = MathTex(
            r"AB\mathbf{x}=(-1,1)",
            color=ORANGE,
        ).scale(0.6).move_to(LEFT * 4.15 + UP * 0.15)

        actions = Text(
            "A = shear,  B = reflect across the y-axis",
        ).scale(0.36).move_to(RIGHT * 4.1 + UP * 1.0)

        formulas = VGroup(
            MathTex(r"BA\neq AB", color=YELLOW).scale(0.88),
            MathTex(r"BA\mathbf{x}\neq AB\mathbf{x}").scale(0.78),
        ).arrange(DOWN, buff=0.25)
        formulas.move_to(RIGHT * 3.95 + DOWN * 1.02)

        self.play(FadeOut(subtitle), Write(heading))
        self.play(Create(axes))
        self.play(Create(start), FadeIn(start_label))
        self.play(FadeIn(actions))
        self.wait(0.5)

        ba_transition = Text(
            "First A, then B",
            color=GREEN,
            weight="BOLD",
        ).scale(0.38).move_to(RIGHT * 4.05 + UP * 0.25)

        self.play(FadeIn(ba_transition, shift=UP * 0.05))
        self.play(Transform(start, ba_final), FadeIn(ba_label))
        self.wait(0.8)

        start_reset = self._vector_from_origin(axes, lesson.vector, BLUE)
        self.play(
            Transform(start, start_reset),
            FadeOut(ba_transition),
        )

        ab_transition = Text(
            "First B, then A",
            color=ORANGE,
            weight="BOLD",
        ).scale(0.38).move_to(RIGHT * 4.05 + UP * 0.25)

        self.play(FadeIn(ab_transition, shift=UP * 0.05))
        self.play(Transform(start, ab_final), FadeIn(ab_label))
        self.play(FadeIn(formulas, shift=UP * 0.08))
        self.wait(1.6)

        self.play(
            FadeOut(heading),
            FadeOut(axes),
            FadeOut(start),
            FadeOut(start_label),
            FadeOut(ba_label),
            FadeOut(ab_label),
            FadeOut(actions),
            FadeOut(formulas),
            FadeOut(ab_transition),
        )

    def _show_identity_matrix(self) -> None:
        lesson = MATRIX_ORDER_IDENTITY_UNDOING_LESSON

        heading = Text(
            "The identity matrix changes nothing",
            weight="BOLD",
        ).scale(0.49).move_to(UP * 2.08)

        identity = self._matrix(lesson.identity, scale=0.7)
        vector = self._matrix(
            ((lesson.vector[0],), (lesson.vector[1],)),
            scale=0.7,
        )
        equals = MathTex("=").scale(0.9)
        result = self._matrix(
            ((lesson.identity_result[0],), (lesson.identity_result[1],)),
            scale=0.7,
        )

        equation = VGroup(
            identity,
            vector,
            equals,
            result,
        ).arrange(RIGHT, buff=0.32)
        equation.scale_to_fit_width(8.8)
        equation.move_to(UP * 0.55)

        statement = MathTex(
            r"I\mathbf{x}=\mathbf{x}",
            color=YELLOW,
        ).scale(0.94).move_to(DOWN * 0.82)

        meaning = Text(
            "I is the do-nothing transformation.",
        ).scale(0.42).move_to(DOWN * 1.55)

        extension = MathTex(
            r"IA=A,\qquad AI=A",
        ).scale(0.82).move_to(DOWN * 2.22)

        self.play(Write(heading))
        self.play(FadeIn(equation))
        self.play(Write(statement))
        self.play(FadeIn(meaning, shift=UP * 0.08))
        self.play(Write(extension))
        self.wait(1.7)

        self.play(
            FadeOut(heading),
            FadeOut(equation),
            FadeOut(statement),
            FadeOut(meaning),
            FadeOut(extension),
        )

    def _show_undoing(self) -> None:
        lesson = MATRIX_ORDER_IDENTITY_UNDOING_LESSON

        heading = Text(
            "Some transformations can be undone",
            weight="BOLD",
        ).scale(0.49).move_to(UP * 2.08)

        inverse = self._matrix(lesson.shear_inverse, scale=0.64)
        shear = self._matrix(lesson.shear, scale=0.64)
        equals = MathTex("=").scale(0.86)
        identity = self._matrix(lesson.identity, scale=0.64)

        top_line = VGroup(
            inverse,
            shear,
            equals,
            identity,
        ).arrange(RIGHT, buff=0.28)
        top_line.scale_to_fit_width(7.7)
        top_line.move_to(UP * 0.96)

        invertible_text = Text(
            "A shear can be undone by another shear.",
        ).scale(0.35).move_to(DOWN * 0.02)

        inverse_name = MathTex(
            r"A^{-1}A=I,\qquad AA^{-1}=I",
            color=YELLOW,
        ).scale(0.72).move_to(DOWN * 0.76)

        projection = self._matrix(lesson.projection, scale=0.62)
        x_vector = self._matrix(
            ((lesson.vector[0],), (lesson.vector[1],)),
            scale=0.62,
        )
        projected = self._matrix(
            ((lesson.projected_vector[0],), (lesson.projected_vector[1],)),
            scale=0.62,
        )

        projection_line = VGroup(
            projection,
            x_vector,
            MathTex("=").scale(0.82),
            projected,
        ).arrange(RIGHT, buff=0.24)
        projection_line.scale_to_fit_width(6.5)
        projection_line.move_to(DOWN * 1.98)

        noninvertible_text = Text(
            "A projection collapses information, so it cannot be undone.",
        ).scale(0.32).move_to(DOWN * 3.04)

        self.play(Write(heading))
        self.play(FadeIn(top_line))
        self.play(FadeIn(invertible_text, shift=UP * 0.08))
        self.play(Write(inverse_name))
        self.play(FadeIn(projection_line))
        self.play(FadeIn(noninvertible_text, shift=UP * 0.08))
        self.wait(1.8)

        self.play(
            FadeOut(heading),
            FadeOut(top_line),
            FadeOut(invertible_text),
            FadeOut(inverse_name),
            FadeOut(projection_line),
            FadeOut(noninvertible_text),
        )

    def _show_pause_predict_and_reflection(self) -> None:
        predict = Text(
            "Pause and Predict",
            weight="BOLD",
            color=YELLOW,
        ).scale(0.52).move_to(UP * 1.65)

        prompt = Text(
            "Which matrix acts first in ACBx?",
        ).scale(0.47).move_to(UP * 0.82)

        expression = MathTex(
            r"ACB\mathbf{x}=A(C(B\mathbf{x}))",
        ).scale(0.92).move_to(DOWN * 0.05)

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
            "Order matters in matrix multiplication.",
            weight="BOLD",
        ).scale(0.49).move_to(UP * 0.72)

        identity = Text(
            "I does nothing, and some matrices have inverses that undo them.",
        ).scale(0.4).move_to(DOWN * 0.02)

        future = Text(
            "We will study inverses more fully with linear systems.",
        ).scale(0.39).move_to(DOWN * 0.76)

        assembly = Text(
            "Next: assemble the Matrix Operations chapter.",
        ).scale(0.4).move_to(DOWN * 1.48)

        self.play(Write(reflection))
        self.play(FadeIn(identity, shift=UP * 0.08))
        self.play(FadeIn(future, shift=UP * 0.08))
        self.play(FadeIn(assembly, shift=UP * 0.08))
        self.wait(2.0)
