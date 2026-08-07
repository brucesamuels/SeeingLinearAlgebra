"""CP138 presentation: use cofactor expansion efficiently and recursively."""
from __future__ import annotations

import numpy as np
from manim import BLUE, FadeIn, FadeOut, GREEN, GREY_B, MathTex, Matrix, RED, Scene, Text, VGroup, WHITE, YELLOW, Write

from engine.determinant_cofactor_efficiency import (
    arithmetic_lines,
    comparison_counts,
    determinant_value,
    example_matrix,
    first_expansion_step,
    first_expansion_tex,
    matrix_tex,
    minor_3x3_value,
    recursive_expansion_tex,
    strategy_lines,
)


class DeterminantCofactorEfficiencyPresentation(Scene):
    """Show how zeros make recursive cofactor expansion practical."""

    def construct(self) -> None:
        banner = Text("Methods of Computation", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = Text("Using Cofactor Expansion Efficiently", font_size=27, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_choice(banner)
        self.show_first_expansion(banner)
        self.show_recursive_expansion(banner)
        self.show_arithmetic(banner)
        self.show_strategy(banner)

    def show_choice(self, banner: Text) -> None:
        title = Text("Which row or column should we use?", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        matrix = self.numeric_matrix(example_matrix(), font_size=30)
        matrix.move_to(np.array([0.0, 0.45, 0.0]))
        row2 = VGroup(*matrix.get_rows()[1])
        row2.set_color(GREEN)

        prompt = Text("Row 2 has three zeros - only one cofactor term survives.", font_size=24, color=WHITE)
        prompt.move_to(np.array([0.0, -2.25, 0.0]))

        self.play(FadeIn(title), FadeIn(matrix))
        self.play(FadeIn(row2))
        self.play(FadeIn(prompt))
        self.wait(1.7)
        self.clear_stage((banner,))

    def show_first_expansion(self, banner: Text) -> None:
        title = Text("Expand along the row with the most zeros", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        matrix = self.numeric_matrix(example_matrix(), font_size=27)
        matrix.move_to(np.array([-3.7, 0.35, 0.0]))
        VGroup(*matrix.get_rows()[1]).set_color(GREEN)

        step = first_expansion_step()
        sign = MathTex(r"(-1)^{2+2}=+1", font_size=30, color=BLUE)
        sign.move_to(np.array([2.6, 1.15, 0.0]))

        expansion = MathTex(first_expansion_tex(), font_size=30, color=WHITE)
        if expansion.width > 7.4:
            expansion.scale(7.4 / expansion.width)
        expansion.move_to(np.array([2.4, -0.25, 0.0]))

        cue = Text("Delete row 2 and column 2.", font_size=23, color=GREY_B)
        cue.move_to(np.array([2.4, -2.0, 0.0]))

        self.play(FadeIn(title), FadeIn(matrix))
        self.play(Write(sign))
        self.play(Write(expansion))
        self.play(FadeIn(cue))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_recursive_expansion(self, banner: Text) -> None:
        title = Text("Cofactor expansion is recursive", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        b = first_expansion_step().minor
        b_matrix = self.numeric_matrix(b, font_size=31)
        b_matrix.move_to(np.array([-3.7, 0.4, 0.0]))
        VGroup(*b_matrix.get_rows()[0]).set_color(BLUE)

        note = Text("The new 3x3 determinant can be expanded again.", font_size=23, color=WHITE)
        note.move_to(np.array([2.45, 1.25, 0.0]))

        expansion = MathTex(recursive_expansion_tex(), font_size=31, color=WHITE)
        if expansion.width > 7.4:
            expansion.scale(7.4 / expansion.width)
        expansion.move_to(np.array([2.45, -0.1, 0.0]))

        zero_note = Text("The zero entry contributes nothing.", font_size=23, color=GREEN)
        zero_note.move_to(np.array([2.45, -1.75, 0.0]))

        self.play(FadeIn(title), FadeIn(b_matrix))
        self.play(FadeIn(note))
        self.play(Write(expansion))
        self.play(FadeIn(zero_note))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_arithmetic(self, banner: Text) -> None:
        title = Text("Now the arithmetic is small", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        lines = arithmetic_lines()
        displays = VGroup(
            MathTex(lines[0], font_size=37, color=BLUE),
            MathTex(lines[1], font_size=37, color=WHITE),
            MathTex(lines[2], font_size=43, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.55)
        displays.move_to(np.array([0.0, -0.05, 0.0]))

        self.play(FadeIn(title))
        for display in displays:
            self.play(Write(display))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_strategy(self, banner: Text) -> None:
        title = Text("Choose the expansion that creates the least work", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        good, poor = comparison_counts()
        comparison = VGroup(
            Text(f"Row 2: {good} surviving term", font_size=27, color=GREEN),
            Text(f"Row 3: {poor} surviving terms", font_size=27, color=RED),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.3)
        comparison.move_to(np.array([0.0, 1.0, 0.0]))

        lines = strategy_lines()
        strategy = VGroup(
            Text(lines[0], font_size=24, color=WHITE),
            Text(lines[1], font_size=25, color=BLUE),
            Text(lines[2], font_size=27, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.30)
        strategy.move_to(np.array([0.0, -1.25, 0.0]))
        if strategy.width > 11.4:
            strategy.scale(11.4 / strategy.width)

        self.play(FadeIn(title))
        self.play(FadeIn(comparison))
        for line in strategy:
            self.play(FadeIn(line))
        self.wait(2.0)

    @staticmethod
    def numeric_matrix(values: tuple[tuple[int, ...], ...], font_size: int) -> Matrix:
        return Matrix(
            [[str(value) for value in row] for row in values],
            element_to_mobject_config={"font_size": font_size},
            h_buff=0.8,
            v_buff=0.6,
        )

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])
