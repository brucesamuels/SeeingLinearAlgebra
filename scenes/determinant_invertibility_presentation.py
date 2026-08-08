"""CP140 presentation: determinant as a test for invertibility."""
from __future__ import annotations

import numpy as np
from manim import BLUE, FadeIn, FadeOut, GREEN, GREY_B, MathTex, Matrix, RED, Scene, Text, VGroup, WHITE, YELLOW, Write

from engine.determinant_invertibility import (
    closing_lines,
    geometric_lines,
    invertible_chain_tex,
    invertible_determinant,
    invertible_example,
    homogeneous_system_statement_tex,
    null_vector_equation_tex,
    nullspace_invertibility_theorem_tex,
    singular_chain_tex,
    singular_determinant,
    singular_example,
    singular_null_vector,
)


class DeterminantInvertibilityPresentation(Scene):
    """Connect determinant, pivots, rank, null space, and invertibility."""

    def construct(self) -> None:
        banner = Text("What the Determinant Tells Us", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = Text("Determinant and Invertibility", font_size=28, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_invertible_example(banner)
        self.show_singular_example(banner)
        self.show_geometric_meaning(banner)
        self.show_nullspace_theorem(banner)
        self.show_equivalence_chains(banner)
        self.show_closing_test(banner)

    def show_invertible_example(self, banner: Text) -> None:
        title = Text("A nonzero determinant signals invertibility", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        matrix = Matrix(
            [[str(x) for x in row] for row in invertible_example()],
            element_to_mobject_config={"font_size": 31}, h_buff=0.82, v_buff=0.62,
        )
        matrix.move_to(np.array([-3.4, 0.45, 0.0]))
        diagonal = VGroup(*[matrix.get_entries()[4 * i] for i in range(3)])
        diagonal.set_color(BLUE)

        determinant = MathTex(rf"\det(A)=2\cdot3\cdot4={invertible_determinant()}", font_size=38, color=GREEN)
        determinant.move_to(np.array([2.6, 1.05, 0.0]))

        consequences = VGroup(
            Text("three pivots", font_size=27, color=WHITE),
            Text("rank = 3", font_size=27, color=WHITE),
            MathTex(r"\mathcal N(A)=\{\mathbf 0\}", font_size=34, color=BLUE),
            Text("A is invertible", font_size=29, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.28)
        consequences.move_to(np.array([2.6, -0.65, 0.0]))

        self.play(FadeIn(title), FadeIn(matrix))
        self.play(FadeIn(diagonal))
        self.play(Write(determinant))
        for line in consequences:
            self.play(FadeIn(line))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_singular_example(self, banner: Text) -> None:
        title = Text("A zero determinant signals singularity", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        matrix = Matrix(
            [[str(x) for x in row] for row in singular_example()],
            element_to_mobject_config={"font_size": 30}, h_buff=0.82, v_buff=0.62,
        )
        matrix.move_to(np.array([-3.6, 0.65, 0.0]))
        row_relation = MathTex(r"R_2=2R_1", font_size=34, color=RED)
        row_relation.next_to(matrix, np.array([0.0, -1.0, 0.0]), buff=0.35)

        determinant = MathTex(rf"\det(B)={singular_determinant()}", font_size=40, color=RED)
        determinant.move_to(np.array([2.65, 1.25, 0.0]))

        null_eq = MathTex(null_vector_equation_tex(), font_size=30, color=BLUE)
        null_eq.scale_to_fit_width(6.8)
        null_eq.move_to(np.array([2.55, -0.25, 0.0]))

        vector = singular_null_vector()
        cue = Text(f"The nonzero vector ({vector[0]}, {vector[1]}, {vector[2]}) is sent to zero.", font_size=22, color=WHITE)
        cue.scale_to_fit_width(6.8)
        cue.move_to(np.array([2.55, -1.75, 0.0]))
        conclusion = Text("B cannot be inverted.", font_size=28, color=RED)
        conclusion.move_to(np.array([2.55, -2.45, 0.0]))

        self.play(FadeIn(title), FadeIn(matrix))
        self.play(FadeIn(row_relation))
        self.play(Write(determinant))
        self.play(Write(null_eq))
        self.play(FadeIn(cue), FadeIn(conclusion))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_geometric_meaning(self, banner: Text) -> None:
        title = Text("Invertibility is also a geometric question", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        nonzero = MathTex(r"\det(A)\neq0", font_size=42, color=GREEN)
        zero = MathTex(r"\det(A)=0", font_size=42, color=RED)
        nonzero.move_to(np.array([-3.2, 0.95, 0.0]))
        zero.move_to(np.array([3.2, 0.95, 0.0]))

        left = VGroup(
            Text("No dimension is lost", font_size=27, color=WHITE),
            Text("volume stays nonzero", font_size=24, color=GREY_B),
            Text("the map can be undone", font_size=26, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.32)
        left.move_to(np.array([-3.2, -0.65, 0.0]))

        right = VGroup(
            Text("Dimension collapses", font_size=27, color=WHITE),
            Text("volume becomes zero", font_size=24, color=GREY_B),
            Text("information is lost", font_size=26, color=RED),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.32)
        right.move_to(np.array([3.2, -0.65, 0.0]))

        footer = Text(geometric_lines()[1], font_size=23, color=BLUE)
        footer.scale_to_fit_width(11.2)
        footer.move_to(np.array([0.0, -2.65, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(nonzero), Write(zero))
        self.play(FadeIn(left), FadeIn(right))
        self.play(FadeIn(footer))
        self.wait(2.0)
        self.clear_stage((banner,))


    def show_nullspace_theorem(self, banner: Text) -> None:
        title = Text("Invertibility Theorem", font_size=31, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        condition = Text(
            "For a square matrix A:",
            font_size=26,
            color=WHITE,
        )
        condition.move_to(np.array([0.0, 1.35, 0.0]))

        theorem = MathTex(
            nullspace_invertibility_theorem_tex(),
            font_size=42,
            color=BLUE,
        )
        theorem.scale_to_fit_width(11.0)
        theorem.move_to(np.array([0.0, 0.35, 0.0]))

        equivalent = MathTex(
            homogeneous_system_statement_tex(),
            font_size=31,
            color=WHITE,
        )
        equivalent.scale_to_fit_width(11.0)
        equivalent.move_to(np.array([0.0, -1.05, 0.0]))

        cue = Text(
            "So no nonzero vector can be sent to zero by an invertible matrix.",
            font_size=24,
            color=GREEN,
        )
        cue.scale_to_fit_width(10.8)
        cue.move_to(np.array([0.0, -2.25, 0.0]))

        self.play(FadeIn(title), FadeIn(condition))
        self.play(Write(theorem))
        self.play(Write(equivalent))
        self.play(FadeIn(cue))
        self.wait(2.2)
        self.clear_stage((banner,))

    def show_equivalence_chains(self, banner: Text) -> None:
        title = Text("For an n x n matrix, these statements are equivalent", font_size=28, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        left = VGroup(*[
            MathTex(line, font_size=28, color=GREEN if i == 0 else WHITE)
            for i, line in enumerate(invertible_chain_tex())
        ]).arrange(np.array([0.0, -1.0, 0.0]), buff=0.18)
        right = VGroup(*[
            MathTex(line, font_size=28, color=RED if i == 0 else WHITE)
            for i, line in enumerate(singular_chain_tex())
        ]).arrange(np.array([0.0, -1.0, 0.0]), buff=0.18)

        left.scale_to_fit_width(5.7)
        right.scale_to_fit_width(5.7)
        left.move_to(np.array([-3.2, -0.15, 0.0]))
        right.move_to(np.array([3.2, -0.15, 0.0]))

        self.play(FadeIn(title))
        for l_line, r_line in zip(left, right):
            self.play(FadeIn(l_line), FadeIn(r_line))
        self.wait(2.2)
        self.clear_stage((banner,))

    def show_closing_test(self, banner: Text) -> None:
        title = Text("The determinant is an invertibility test", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        lines = closing_lines()
        summary = VGroup(
            Text(lines[0], font_size=26, color=WHITE),
            MathTex(r"\det(A)\neq0\quad\Longrightarrow\quad A\text{ invertible}", font_size=38, color=GREEN),
            MathTex(r"\det(A)=0\quad\Longrightarrow\quad A\text{ singular}", font_size=38, color=RED),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.52)
        summary.move_to(np.array([0.0, 0.0, 0.0]))
        summary.scale_to_fit_width(11.2)

        reminder = Text("This test applies to square matrices.", font_size=23, color=GREY_B)
        reminder.move_to(np.array([0.0, -2.55, 0.0]))

        self.play(FadeIn(title))
        for line in summary:
            self.play(FadeIn(line))
        self.play(FadeIn(reminder))
        self.wait(2.0)

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])
