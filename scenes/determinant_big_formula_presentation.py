"""CP135 presentation: the Big Formula for determinants."""
from __future__ import annotations

import numpy as np
from manim import FadeIn, FadeOut, MathTex, Matrix, Scene, Text, VGroup, WHITE, YELLOW, BLUE, GREEN, RED, GREY_B, Write

from engine.determinant_big_formula import (
    big_formula_explanation_lines,
    big_formula_tex,
    familiar_formula_3x3_tex,
    grouped_formula_3x3_lines,
    n_factorial_terms_statement,
    negative_terms_3x3,
    permutation_terms_3x3,
    positive_terms_3x3,
)


class DeterminantBigFormulaPresentation(Scene):
    """Introduce the permutation formula and derive the 3x3 determinant expression."""

    def construct(self) -> None:
        banner = Text("Methods of Computation", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = Text("The Big Formula", font_size=27, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_overview(banner)
        self.show_general_formula(banner)
        self.show_three_by_three_terms(banner)
        self.show_familiar_formula(banner)

    def show_overview(self, banner: Text) -> None:
        title = Text("What does the determinant add up?", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.25, 0.0]))
        lines = VGroup(
            Text("The determinant sums signed products.", font_size=25, color=WHITE),
            Text("Each product chooses one entry from each row and each column.", font_size=24, color=WHITE),
            Text(n_factorial_terms_statement(3), font_size=24, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.24)
        lines.move_to(np.array([0.0, 0.3, 0.0]))
        self.play(FadeIn(title))
        for line in lines:
            self.play(FadeIn(line))
        self.wait(1.4)
        self.clear_stage((banner,))

    def show_general_formula(self, banner: Text) -> None:
        title = Text("The general permutation formula", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))
        formula = MathTex(big_formula_tex(), font_size=34, color=BLUE)
        formula.move_to(np.array([0.0, 1.15, 0.0]))

        matrix = Matrix(
            [[r"a_{11}", r"a_{12}", r"a_{13}"], [r"a_{21}", r"a_{22}", r"a_{23}"], [r"a_{31}", r"a_{32}", r"a_{33}"]],
            element_to_mobject_config={"font_size": 28},
        )
        matrix.move_to(np.array([-4.55, -0.7, 0.0]))
        matrix_label = MathTex(r"A=", font_size=34, color=WHITE).next_to(matrix, np.array([-1.0, 0.0, 0.0]), buff=0.25)

        explanations = big_formula_explanation_lines()
        bullets = VGroup(
            Text(explanations[0], font_size=22, color=WHITE),
            Text(explanations[1], font_size=22, color=WHITE),
            Text(explanations[2], font_size=21, color=WHITE),
            Text(explanations[3], font_size=21, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), aligned_edge=np.array([-1.0, 0.0, 0.0]), buff=0.18)
        bullets.move_to(np.array([2.85, -0.8, 0.0]))
        self.play(FadeIn(title), Write(formula))
        self.play(FadeIn(matrix), FadeIn(matrix_label))
        for bullet in bullets:
            self.play(FadeIn(bullet))
        self.wait(1.6)
        self.clear_stage((banner,))

    def show_three_by_three_terms(self, banner: Text) -> None:
        title = Text("For 3x3 there are six permutation terms", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.45, 0.0]))

        positive_title = Text("Even permutations: positive", font_size=24, color=GREEN)
        positive_title.move_to(np.array([-3.0, 1.8, 0.0]))
        negative_title = Text("Odd permutations: negative", font_size=24, color=RED)
        negative_title.move_to(np.array([3.0, 1.8, 0.0]))

        pos_lines = []
        for term in positive_terms_3x3():
            pos_lines.append(MathTex(rf"{term.permutation_tex}:\;{term.product_tex}", font_size=30, color=GREEN))
        neg_lines = []
        for term in negative_terms_3x3():
            neg_lines.append(MathTex(rf"{term.permutation_tex}:\;{term.product_tex}", font_size=30, color=RED))

        positive_group = VGroup(*pos_lines).arrange(np.array([0.0, -1.0, 0.0]), aligned_edge=np.array([-1.0, 0.0, 0.0]), buff=0.20)
        positive_group.move_to(np.array([-3.15, 0.0, 0.0]))
        negative_group = VGroup(*neg_lines).arrange(np.array([0.0, -1.0, 0.0]), aligned_edge=np.array([-1.0, 0.0, 0.0]), buff=0.20)
        negative_group.move_to(np.array([3.15, 0.0, 0.0]))

        note = Text(
            "Every term uses one entry from each row and each column. The sign comes from the parity of the permutation.",
            font_size=20,
            color=GREY_B,
        )
        note.scale_to_fit_width(11.6)
        note.move_to(np.array([0.0, -3.05, 0.0]))

        self.play(FadeIn(title), FadeIn(positive_title), FadeIn(negative_title))
        for line in positive_group:
            self.play(FadeIn(line))
        for line in negative_group:
            self.play(FadeIn(line))
        self.play(FadeIn(note))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_familiar_formula(self, banner: Text) -> None:
        title = Text("The familiar 3x3 determinant formula", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.3, 0.0]))
        grouped = grouped_formula_3x3_lines()
        pos = MathTex(grouped[0], font_size=28, color=GREEN)
        neg = MathTex(grouped[1], font_size=28, color=RED)
        pos.scale_to_fit_width(11.4)
        neg.scale_to_fit_width(11.4)
        pos.move_to(np.array([0.0, 0.9, 0.0]))
        neg.move_to(np.array([0.0, -0.15, 0.0]))
        final_line_1 = MathTex(
            r"\det(A)=a_{11}a_{22}a_{33}+a_{12}a_{23}a_{31}+a_{13}a_{21}a_{32}",
            font_size=28,
            color=BLUE,
        )
        final_line_2 = MathTex(
            r"-a_{11}a_{23}a_{32}-a_{12}a_{21}a_{33}-a_{13}a_{22}a_{31}",
            font_size=28,
            color=BLUE,
        )
        final_line_1.scale_to_fit_width(11.4)
        final_line_2.scale_to_fit_width(11.4)
        final_formula = VGroup(final_line_1, final_line_2).arrange(
            np.array([0.0, -1.0, 0.0]), buff=0.10
        )
        final_formula.move_to(np.array([0.0, -1.72, 0.0]))
        summary = Text(
            "The Big Formula explains where the six-term 3x3 rule comes from.",
            font_size=22,
            color=GREY_B,
        )
        summary.move_to(np.array([0.0, -3.05, 0.0]))
        self.play(FadeIn(title))
        self.play(Write(pos), Write(neg))
        self.play(Write(final_formula))
        self.play(FadeIn(summary))
        self.wait(2.0)

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])
