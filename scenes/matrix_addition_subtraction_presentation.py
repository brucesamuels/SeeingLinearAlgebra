"""CP96 Manim presentation: Matrix Addition and Subtraction."""

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
    Text,
    TransformMatchingTex,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
)

from engine.matrix_addition_subtraction import (
    MATRIX_ADDITION_SUBTRACTION_LESSON,
    entrywise_steps,
    negate_matrix,
)

# Use the project's theme when its current public API is available.  The
# fallback keeps the checkpoint renderable while remaining visually consistent.
try:
    from engine.lesson_theme import SEEING_LINEAR_ALGEBRA_THEME
except ImportError:  # pragma: no cover - depends on the host repository
    SEEING_LINEAR_ALGEBRA_THEME = None


class MatrixAdditionSubtractionPresentation(Scene):
    """Introduce equal-size, entrywise matrix addition and subtraction."""

    TITLE = "Matrix Addition and Subtraction"

    def construct(self) -> None:
        title = Text(self.TITLE, weight="BOLD").scale(0.68)
        title.to_edge(UP, buff=0.28)
        subtitle = Text(
            "Combine corresponding entries",
        ).scale(0.42)
        subtitle.next_to(title, DOWN, buff=0.16)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.12))
        self.wait(0.8)

        self._show_shape_requirement(subtitle)
        self._show_addition_example()
        self._show_subtraction_example()
        self._show_incompatible_shapes()
        self._show_properties_and_reflection()

    @staticmethod
    def _matrix(data, *, scale: float = 0.82) -> Matrix:
        matrix = Matrix(
            [[str(value) for value in row] for row in data],
            h_buff=0.85,
            v_buff=0.62,
        )
        return matrix.scale(scale)

    def _clear_below_title(self) -> None:
        removable = [
            mob
            for mob in self.mobjects
            if mob.get_center()[1] < 2.45
        ]
        if removable:
            self.play(*[FadeOut(mob) for mob in removable], run_time=0.55)

    def _show_shape_requirement(self, subtitle: Text) -> None:
        question = Text(
            "When can two matrices be added?",
        ).scale(0.53).move_to(UP * 1.1)

        same_size = MathTex(
            r"A_{m\times n}+B_{m\times n}",
            color=YELLOW,
        ).scale(0.95)
        same_size.next_to(question, DOWN, buff=0.48)

        rule = Text(
            "They must have the same number of rows and columns.",
        ).scale(0.43)
        rule.next_to(same_size, DOWN, buff=0.48)

        self.play(FadeOut(subtitle), Write(question))
        self.play(Write(same_size))
        self.play(FadeIn(rule, shift=UP * 0.12))
        self.wait(1.7)
        self.play(FadeOut(question), FadeOut(same_size), FadeOut(rule))

    def _show_addition_example(self) -> None:
        lesson = MATRIX_ADDITION_SUBTRACTION_LESSON
        heading = Text("Addition is entrywise", weight="BOLD").scale(0.52)
        heading.move_to(UP * 2.15)

        left = self._matrix(lesson.addition_left)
        plus = MathTex("+").scale(0.9)
        right = self._matrix(lesson.addition_right)
        equals = MathTex("=").scale(0.9)
        result = self._matrix(lesson.addition_result)

        equation = VGroup(left, plus, right, equals, result).arrange(
            RIGHT, buff=0.38
        )
        equation.scale_to_fit_width(12.4)
        equation.move_to(UP * 0.55)

        self.play(Write(heading))
        self.play(FadeIn(left), Write(plus), FadeIn(right))
        self.wait(0.5)

        left_entries = left.get_entries()
        right_entries = right.get_entries()
        result_entries = result.get_entries()
        colors = (BLUE, GREEN, ORANGE, RED)

        for index, step in enumerate(
            entrywise_steps(
                lesson.addition_left,
                lesson.addition_right,
                operation="add",
            )
        ):
            left_entries[index].set_color(colors[index])
            right_entries[index].set_color(colors[index])
            result_entries[index].set_color(colors[index])

            calculation = MathTex(
                rf"{step.left_value}+({step.right_value})={step.result}"
                if step.right_value < 0
                else rf"{step.left_value}+{step.right_value}={step.result}",
                color=colors[index],
            ).scale(0.66)
            calculation.move_to(DOWN * 1.45)

            self.play(
                FadeIn(calculation, shift=UP * 0.1),
                run_time=0.35,
            )
            self.wait(0.42)
            self.play(FadeOut(calculation), run_time=0.22)

        self.play(Write(equals), FadeIn(result))
        general_rule = MathTex(
            r"(A+B)_{ij}=a_{ij}+b_{ij}",
            color=YELLOW,
        ).scale(0.82).move_to(DOWN * 1.55)
        self.play(Write(general_rule))
        self.wait(1.7)
        self.play(
            FadeOut(heading),
            FadeOut(equation),
            FadeOut(general_rule),
        )

    def _show_subtraction_example(self) -> None:
        lesson = MATRIX_ADDITION_SUBTRACTION_LESSON
        heading = Text(
            "Subtraction means adding the negative",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.15)

        direct = MathTex(r"A-B").scale(1.05)
        rewrite = MathTex(r"A+(-B)").scale(1.05)
        rewrite.move_to(direct)

        self.play(Write(heading), Write(direct))
        self.play(TransformMatchingTex(direct, rewrite))
        self.wait(0.7)

        left = self._matrix(lesson.subtraction_left, scale=0.72)
        minus = MathTex("-")
        right = self._matrix(lesson.subtraction_right, scale=0.72)
        equals = MathTex("=")
        result = self._matrix(lesson.subtraction_result, scale=0.72)
        direct_equation = VGroup(
            left, minus, right, equals, result
        ).arrange(RIGHT, buff=0.32)
        direct_equation.scale_to_fit_width(11.8)
        direct_equation.move_to(UP * 0.35)

        negative = self._matrix(
            negate_matrix(lesson.subtraction_right),
            scale=0.72,
        )
        plus = MathTex("+")
        rewritten_equation = VGroup(
            self._matrix(lesson.subtraction_left, scale=0.72),
            plus,
            negative,
            MathTex("="),
            self._matrix(lesson.subtraction_as_addition_result, scale=0.72),
        ).arrange(RIGHT, buff=0.32)
        rewritten_equation.scale_to_fit_width(11.8)
        rewritten_equation.move_to(DOWN * 1.9)

        self.play(FadeOut(rewrite), FadeIn(direct_equation))
        self.play(FadeIn(rewritten_equation, shift=UP * 0.12))
        self.wait(1.8)

        takeaway = Text(
            "Negate every entry of B, then add corresponding entries.",
        ).scale(0.37)
        takeaway.next_to(rewritten_equation, DOWN, buff=0.42)
        self.play(FadeIn(takeaway))
        self.wait(1.6)
        self.play(
            FadeOut(heading),
            FadeOut(direct_equation),
            FadeOut(rewritten_equation),
            FadeOut(takeaway),
        )

    def _show_incompatible_shapes(self) -> None:
        heading = Text(
            "Different dimensions? The operation is undefined.",
            weight="BOLD",
        ).scale(0.48).move_to(UP * 2.05)

        mismatch = MathTex(
            r"A_{2\times 3}+B_{3\times 2}",
        ).scale(1.0).move_to(UP * 0.65)

        explanation = Text(
            "There is no one-to-one pairing of corresponding positions.",
        ).scale(0.42).move_to(DOWN * 0.4)

        not_defined = MathTex(
            r"\text{not defined}",
            color=RED,
        ).scale(0.9).move_to(DOWN * 1.35)

        self.play(Write(heading))
        self.play(Write(mismatch))
        self.play(FadeIn(explanation), Write(not_defined))
        self.wait(1.8)
        self.play(
            FadeOut(heading),
            FadeOut(mismatch),
            FadeOut(explanation),
            FadeOut(not_defined),
        )

    def _show_properties_and_reflection(self) -> None:
        heading = Text(
            "The familiar algebra survives entrywise",
            weight="BOLD",
        ).scale(0.5).move_to(UP * 2.12)

        properties = VGroup(
            MathTex(r"A+B=B+A"),
            MathTex(r"(A+B)+C=A+(B+C)"),
            MathTex(r"A+0=A"),
            MathTex(r"A+(-A)=0"),
        ).arrange(DOWN, buff=0.32)
        properties.scale(0.78).move_to(UP * 0.15)

        self.play(Write(heading))
        for property_line in properties:
            self.play(Write(property_line), run_time=0.48)
        self.wait(1.4)

        self.play(FadeOut(properties), FadeOut(heading))

        predict = Text(
            "Pause and Predict",
            weight="BOLD",
            color=YELLOW,
        ).scale(0.52).move_to(UP * 1.55)
        prompt = Text(
            "What is the first entry of A − B?",
        ).scale(0.48).move_to(UP * 0.62)
        a_label = MathTex("A=").scale(0.78)
        a_matrix = self._matrix(((3, -1), (2, 5)), scale=0.68)
        comma = MathTex(r",\qquad").scale(0.78)
        b_label = MathTex("B=").scale(0.78)
        b_matrix = self._matrix(((7, 4), (-2, 1)), scale=0.68)
        example = VGroup(
            a_label,
            a_matrix,
            comma,
            b_label,
            b_matrix,
        ).arrange(RIGHT, buff=0.18)
        example.scale_to_fit_width(9.8)
        example.move_to(DOWN * 0.35)
        answer = MathTex(
            r"3-7=-4",
            color=GREEN,
        ).scale(0.9).move_to(DOWN * 1.55)

        self.play(Write(predict), FadeIn(prompt), Write(example))
        self.wait(2.3)
        self.play(Write(answer))
        self.wait(1.25)

        self.play(
            FadeOut(predict),
            FadeOut(prompt),
            FadeOut(example),
            FadeOut(answer),
        )

        reflection = Text(
            "Matrix addition and subtraction are entrywise operations.",
            weight="BOLD",
        ).scale(0.5)
        reflection.move_to(UP * 0.42)
        condition = Text(
            "The matrices must have exactly the same dimensions.",
        ).scale(0.43).next_to(reflection, DOWN, buff=0.42)
        bridge = Text(
            "Next: multiplying every entry by a scalar.",
        ).scale(0.42).next_to(condition, DOWN, buff=0.55)

        self.play(Write(reflection))
        self.play(FadeIn(condition, shift=UP * 0.1))
        self.play(FadeIn(bridge, shift=UP * 0.1))
        self.wait(2.0)
