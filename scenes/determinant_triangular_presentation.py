"""CP139 presentation: determinants of triangular and block-triangular matrices."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    FadeIn,
    FadeOut,
    GREEN,
    GREY_B,
    MathTex,
    Matrix,
    RED,
    Scene,
    Text,
    VGroup,
    WHITE,
    YELLOW,
    Write,
)

from engine.determinant_triangular import (
    block_example_factorization_tex,
    block_example_tex,
    block_triangular_rule_tex,
    block_triangular_symbolic_tex,
    diagonal_product_tex,
    lower_triangular_determinant,
    lower_triangular_example,
    strategy_lines,
    triangular_explanation_lines,
    triangular_rule_tex,
    upper_triangular_determinant,
    upper_triangular_example,
)


class DeterminantTriangularPresentation(Scene):
    """Recognize triangular structure before computing a determinant."""

    def construct(self) -> None:
        banner = Text("Methods of Computation", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = Text("Triangular Structure", font_size=28, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_upper_triangular(banner)
        self.show_why_diagonal_product(banner)
        self.show_lower_triangular(banner)
        self.show_block_triangular(banner)
        self.show_strategy(banner)

    def show_upper_triangular(self, banner: Text) -> None:
        title = Text("A triangular matrix gives us a shortcut", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        matrix = Matrix(
            [[str(x) for x in row] for row in upper_triangular_example()],
            element_to_mobject_config={"font_size": 30},
            h_buff=0.72,
            v_buff=0.54,
        )
        matrix.move_to(np.array([0.0, 0.65, 0.0]))

        diagonal = VGroup(*[matrix.get_entries()[5 * i] for i in range(4)])
        diagonal.set_color(BLUE)

        observation = Text(
            "Everything below the diagonal is zero.",
            font_size=24,
            color=GREY_B,
        )
        observation.move_to(np.array([0.0, -1.45, 0.0]))

        product = MathTex(diagonal_product_tex(), font_size=38, color=GREEN)
        product.move_to(np.array([0.0, -2.35, 0.0]))

        self.play(FadeIn(title), FadeIn(matrix))
        self.play(FadeIn(diagonal), FadeIn(observation))
        self.play(Write(product))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_why_diagonal_product(self, banner: Text) -> None:
        title = Text("Why does the diagonal product work?", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        small = Matrix(
            [[r"a", r"b", r"c"], [r"0", r"d", r"e"], [r"0", r"0", r"f"]],
            element_to_mobject_config={"font_size": 31},
            h_buff=0.8,
            v_buff=0.6,
        )
        small.move_to(np.array([-3.7, 0.45, 0.0]))

        first_expansion = MathTex(
            r"\det(T)=a\begin{vmatrix}d&e\\0&f\end{vmatrix}",
            font_size=34,
            color=BLUE,
        )
        second_expansion = MathTex(r"=a(df)=adf", font_size=36, color=GREEN)
        derivation = VGroup(first_expansion, second_expansion).arrange(
            np.array([0.0, -1.0, 0.0]), buff=0.4
        )
        derivation.move_to(np.array([2.0, 0.45, 0.0]))

        explanation = VGroup(
            *[
                Text(line, font_size=22, color=WHITE if i < 2 else GREY_B)
                for i, line in enumerate(triangular_explanation_lines())
            ]
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22)
        explanation.move_to(np.array([0.0, -2.1, 0.0]))

        self.play(FadeIn(title), FadeIn(small))
        self.play(Write(first_expansion))
        self.play(Write(second_expansion))
        for line in explanation:
            self.play(FadeIn(line))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_lower_triangular(self, banner: Text) -> None:
        title = Text("The same rule holds below the diagonal", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        matrix = Matrix(
            [[str(x) for x in row] for row in lower_triangular_example()],
            element_to_mobject_config={"font_size": 31},
            h_buff=0.8,
            v_buff=0.6,
        )
        matrix.move_to(np.array([-2.8, 0.35, 0.0]))

        rule = MathTex(triangular_rule_tex(), font_size=38, color=BLUE)
        rule.move_to(np.array([2.6, 1.05, 0.0]))
        example = MathTex(
            rf"\det(L)=5(-1)(6)={lower_triangular_determinant()}",
            font_size=36,
            color=GREEN,
        )
        example.move_to(np.array([2.6, -0.2, 0.0]))

        cue = Text(
            "Upper or lower triangular: the determinant is the product of the diagonal entries.",
            font_size=23,
            color=WHITE,
        )
        cue.scale_to_fit_width(11.5)
        cue.move_to(np.array([0.0, -2.4, 0.0]))

        self.play(FadeIn(title), FadeIn(matrix))
        self.play(Write(rule), Write(example))
        self.play(FadeIn(cue))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_block_triangular(self, banner: Text) -> None:
        title = Text("The idea extends to blocks", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        symbolic = MathTex(block_triangular_symbolic_tex(), font_size=38, color=WHITE)
        symbolic.move_to(np.array([-3.2, 0.75, 0.0]))
        rule = MathTex(block_triangular_rule_tex(), font_size=38, color=BLUE)
        rule.move_to(np.array([2.65, 0.75, 0.0]))

        cue = Text(
            "If the lower-left block is zero, only the diagonal blocks control the determinant.",
            font_size=22,
            color=GREY_B,
        )
        cue.scale_to_fit_width(11.4)
        cue.move_to(np.array([0.0, -0.45, 0.0]))

        example = MathTex(block_example_tex(), font_size=27, color=WHITE)
        example.move_to(np.array([-3.0, -1.8, 0.0]))
        factorization = MathTex(block_example_factorization_tex(), font_size=29, color=GREEN)
        factorization.scale_to_fit_width(6.5)
        factorization.move_to(np.array([3.0, -1.8, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(symbolic), Write(rule))
        self.play(FadeIn(cue))
        self.play(FadeIn(example), Write(factorization))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_strategy(self, banner: Text) -> None:
        title = Text("Recognize structure before you compute", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        lines = strategy_lines()
        summary = VGroup(
            Text(lines[0], font_size=26, color=WHITE),
            Text(lines[1], font_size=27, color=GREEN),
            Text(lines[2], font_size=27, color=BLUE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.48)
        summary.move_to(np.array([0.0, 0.1, 0.0]))
        summary.scale_to_fit_width(11.3)

        closing = Text(
            "Zeros and triangular structure can turn a long determinant computation into a glance.",
            font_size=23,
            color=GREY_B,
        )
        closing.scale_to_fit_width(11.3)
        closing.move_to(np.array([0.0, -2.55, 0.0]))

        self.play(FadeIn(title))
        for line in summary:
            self.play(FadeIn(line))
        self.play(FadeIn(closing))
        self.wait(2.0)

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])
