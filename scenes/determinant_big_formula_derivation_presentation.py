"""CP136 presentation: derive the familiar 3x3 determinant formula from permutations."""
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

from engine.determinant_big_formula_derivation import (
    determinant_formula_tex,
    negative_patterns,
    negative_sum_tex,
    positive_patterns,
    positive_sum_tex,
    selection_rule_lines,
)


class DeterminantBigFormulaDerivationPresentation(Scene):
    """Turn the six 3x3 permutations into the familiar six-term determinant formula."""

    def construct(self) -> None:
        banner = Text("Methods of Computation", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = Text("Deriving the 3x3 Formula", font_size=27, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_selection_rule(banner)
        self.show_positive_patterns(banner)
        self.show_negative_patterns(banner)
        self.show_assembled_formula(banner)

    def show_selection_rule(self, banner: Text) -> None:
        title = Text("From a permutation to a product", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.3, 0.0]))

        matrix = self.symbolic_matrix(font_size=30)
        matrix.move_to(np.array([-3.9, -0.25, 0.0]))
        name = MathTex(r"A=", font_size=36, color=WHITE)
        name.next_to(matrix, np.array([-1.0, 0.0, 0.0]), buff=0.25)

        rules = selection_rule_lines()
        rule_group = VGroup(
            Text(rules[0], font_size=24, color=WHITE),
            Text(rules[1], font_size=24, color=WHITE),
            Text(rules[2], font_size=23, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), aligned_edge=np.array([-1.0, 0.0, 0.0]), buff=0.24)
        rule_group.move_to(np.array([2.6, 0.65, 0.0]))

        example = VGroup(
            MathTex(r"\sigma=(2\,3\,1)", font_size=32, color=GREEN),
            MathTex(r"a_{12}a_{23}a_{31}", font_size=34, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.25)
        example.move_to(np.array([2.6, -1.55, 0.0]))

        self.play(FadeIn(title), FadeIn(matrix), FadeIn(name))
        for rule in rule_group:
            self.play(FadeIn(rule))
        self.play(Write(example[0]), Write(example[1]))
        self.wait(1.5)
        self.clear_stage((banner,))

    def show_positive_patterns(self, banner: Text) -> None:
        title = Text("Even permutations give the three positive products", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        cards = []
        x_positions = (-4.1, 0.0, 4.1)
        for pattern, x in zip(positive_patterns(), x_positions):
            card = self.pattern_card(pattern.permutation_tex, pattern.product_tex, GREEN)
            card.move_to(np.array([x, 0.0, 0.0]))
            cards.append(card)

        sum_line = MathTex(positive_sum_tex(), font_size=34, color=GREEN)
        sum_line.scale_to_fit_width(11.4)
        sum_line.move_to(np.array([0.0, -2.75, 0.0]))

        self.play(FadeIn(title))
        for card in cards:
            self.play(FadeIn(card))
        self.play(Write(sum_line))
        self.wait(1.6)
        self.clear_stage((banner,))

    def show_negative_patterns(self, banner: Text) -> None:
        title = Text("Odd permutations give the three negative products", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        cards = []
        x_positions = (-4.1, 0.0, 4.1)
        for pattern, x in zip(negative_patterns(), x_positions):
            card = self.pattern_card(pattern.permutation_tex, pattern.product_tex, RED, prefix="-")
            card.move_to(np.array([x, 0.0, 0.0]))
            cards.append(card)

        sum_line = MathTex(negative_sum_tex(), font_size=34, color=RED)
        sum_line.scale_to_fit_width(11.4)
        sum_line.move_to(np.array([0.0, -2.75, 0.0]))

        self.play(FadeIn(title))
        for card in cards:
            self.play(FadeIn(card))
        self.play(Write(sum_line))
        self.wait(1.6)
        self.clear_stage((banner,))

    def show_assembled_formula(self, banner: Text) -> None:
        title = Text("Assemble the six terms", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        positive = MathTex(positive_sum_tex(), font_size=33, color=GREEN)
        negative = MathTex(negative_sum_tex(), font_size=33, color=RED)
        positive.scale_to_fit_width(11.0)
        negative.scale_to_fit_width(11.0)
        positive.move_to(np.array([0.0, 1.0, 0.0]))
        negative.move_to(np.array([0.0, -0.15, 0.0]))

        blue_positive_terms = positive.copy().set_color(BLUE)
        blue_negative_terms = negative.copy().set_color(BLUE)
        det_prefix = MathTex(r"\det(A)=", font_size=33, color=BLUE)
        det_prefix.scale(blue_positive_terms.height / det_prefix.height)

        first_blue_line = VGroup(det_prefix, blue_positive_terms).arrange(
            np.array([1.0, 0.0, 0.0]),
            buff=0.12,
        )
        second_blue_line = blue_negative_terms
        final = VGroup(first_blue_line, second_blue_line)
        final.arrange(np.array([0.0, -1.0, 0.0]), buff=0.12)
        final.move_to(np.array([0.0, -1.82, 0.0]))

        note = Text(
            "The familiar 3x3 formula is exactly the Big Formula specialized to six permutations.",
            font_size=21,
            color=GREY_B,
        )
        note.scale_to_fit_width(11.4)
        note.move_to(np.array([0.0, -3.15, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(positive))
        self.play(Write(negative))
        self.play(Write(final))
        self.play(FadeIn(note))
        self.wait(2.0)

    def pattern_card(self, permutation_tex: str, product_tex: str, color, prefix: str = "") -> VGroup:
        matrix = self.symbolic_matrix(font_size=22)
        perm = MathTex(permutation_tex, font_size=27, color=color)
        display_tex = rf"{prefix}{product_tex}" if prefix else product_tex
        product = MathTex(display_tex, font_size=29, color=color)
        group = VGroup(perm, matrix, product).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22)
        return group

    @staticmethod
    def symbolic_matrix(font_size: int) -> Matrix:
        return Matrix(
            [
                [r"a_{11}", r"a_{12}", r"a_{13}"],
                [r"a_{21}", r"a_{22}", r"a_{23}"],
                [r"a_{31}", r"a_{32}", r"a_{33}"],
            ],
            element_to_mobject_config={"font_size": font_size},
            h_buff=0.7,
            v_buff=0.55,
        )

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])
