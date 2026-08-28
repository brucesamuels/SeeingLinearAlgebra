"""Manim presentation: Positive Definite Matrices — The Elimination Test."""
from __future__ import annotations

from manim import (
    BLUE_C, GREEN_C, GREY_B, RED_C, TEAL_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, MathTex, Matrix, Rectangle,
    ReplacementTransform, Scene, SurroundingRectangle, Text, VGroup,
)

from engine.positive_definite_elimination_test import PositiveDefiniteEliminationTest


class PositiveDefiniteEliminationTestPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "The Elimination Test"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Text(
            self.CHAPTER_BANNER, font_size=21, color=GREY_B, weight="BOLD"
        ).to_edge(UP, buff=0.16)
        title = Text(
            self.LESSON_TITLE, font_size=31, color=YELLOW, weight="BOLD"
        ).next_to(banner, DOWN, buff=0.11)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.6)
        return new

    @staticmethod
    def _matrix(entries, scale=0.76):
        return Matrix(entries, h_buff=0.88, v_buff=0.78).scale(scale)

    @staticmethod
    def _criterion_box(label, formula, color):
        content = VGroup(
            Text(label, font_size=24, color=color, weight="BOLD"),
            MathTex(formula, font_size=38, color=WHITE),
        ).arrange(DOWN, buff=0.20)
        border = Rectangle(
            width=content.width + 0.46,
            height=content.height + 0.38,
            color=color,
            stroke_width=2.4,
        ).move_to(content)
        return VGroup(border, content)

    def construct(self):
        model = PositiveDefiniteEliminationTest()
        pivots = model.elimination_pivots()

        banner, title, heading = self._chrome(
            "Positive eigenvalues certify the matrix—but finding them is not always convenient."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        matrix_card = VGroup(
            MathTex("A=", font_size=44),
            self._matrix([["2", "1"], ["1", "2"]]),
        ).arrange(RIGHT, buff=0.14)
        recall = MathTex(
            r"\lambda_1=1>0,\qquad\lambda_2=3>0",
            font_size=43,
            color=GREEN_C,
        )
        question = Text(
            "Can elimination detect the same positivity without finding eigenvalues?",
            font_size=29,
            color=YELLOW,
        )
        opening = VGroup(matrix_card, recall, question).arrange(DOWN, buff=0.40)
        opening.move_to(DOWN * 0.26)
        if opening.width > 11.3:
            opening.scale_to_fit_width(11.3)
        self.play(FadeIn(matrix_card), FadeIn(recall))
        self.play(FadeIn(question))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "One elimination step exposes two pivots."
        )
        self.play(FadeOut(opening))
        source_matrix = self._matrix([["2", "1"], ["1", "2"]], scale=0.86)
        operation = VGroup(
            Arrow(LEFT, RIGHT, buff=0, color=YELLOW, stroke_width=3.5),
            MathTex(r"R_2\leftarrow R_2-\frac12R_1", font_size=32, color=YELLOW),
        )
        operation[1].next_to(operation[0], UP, buff=0.10)
        upper_matrix = self._matrix(
            [["2", "1"], ["0", r"\frac32"]], scale=0.86
        )
        elimination = VGroup(source_matrix, operation, upper_matrix).arrange(
            RIGHT, buff=0.70
        ).move_to(UP * 0.16)
        pivot_one_box = SurroundingRectangle(
            upper_matrix.get_entries()[0], color=GREEN_C, buff=0.10
        )
        pivot_two_box = SurroundingRectangle(
            upper_matrix.get_entries()[3], color=TEAL_C, buff=0.10
        )
        pivot_one = MathTex(
            rf"p_1={pivots[0]:g}", font_size=42, color=GREEN_C
        )
        pivot_two = MathTex(
            r"p_2=\frac32", font_size=42, color=TEAL_C
        )
        pivot_labels = VGroup(pivot_one, pivot_two).arrange(RIGHT, buff=1.12)
        pivot_labels.next_to(elimination, DOWN, buff=0.52)
        self.play(FadeIn(source_matrix))
        self.play(FadeIn(operation), FadeIn(upper_matrix))
        self.play(Create(pivot_one_box), FadeIn(pivot_one))
        self.play(Create(pivot_two_box), FadeIn(pivot_two))

        prediction = Text(
            "Pause: if the next pivot were zero or negative, what would happen to the energy?",
            font_size=27,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.22)
        if prediction.width > 11.3:
            prediction.scale_to_fit_width(11.3)
        self.play(FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "Completing the square reveals what the pivots measure."
        )
        self.play(
            FadeOut(elimination), FadeOut(pivot_one_box), FadeOut(pivot_two_box),
            FadeOut(pivot_labels),
        )
        expanded = MathTex(
            r"x^T A x=2x_1^2+2x_1x_2+2x_2^2",
            font_size=48,
            color=WHITE,
        )
        completed = MathTex(
            r"=2\left(x_1+\frac12x_2\right)^2+\frac32x_2^2",
            font_size=51,
            color=YELLOW,
        )
        coefficients = VGroup(
            VGroup(
                MathTex(r"p_1=2", font_size=38, color=GREEN_C),
                Text("first square coefficient", font_size=22, color=GREEN_C),
            ).arrange(DOWN, buff=0.12),
            VGroup(
                MathTex(r"p_2=\frac32", font_size=38, color=TEAL_C),
                Text("second square coefficient", font_size=22, color=TEAL_C),
            ).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=1.05)
        square_card = VGroup(expanded, completed, coefficients).arrange(DOWN, buff=0.52)
        square_card.move_to(DOWN * 0.30)
        self.play(FadeIn(expanded))
        self.play(FadeIn(completed))
        self.play(FadeIn(coefficients))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Because both square coefficients are positive, every nonzero vector has positive energy."
        )
        conclusion = MathTex(
            r"x\ne0\quad\Longrightarrow\quad"
            r"2\left(x_1+\frac12x_2\right)^2+\frac32x_2^2>0",
            font_size=45,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.36)
        if conclusion.width > 11.3:
            conclusion.scale_to_fit_width(11.3)
        self.play(FadeIn(conclusion))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "The same information is stored in the leading principal minors."
        )
        self.play(FadeOut(square_card), FadeOut(conclusion))
        first_minor = VGroup(
            MathTex(r"\Delta_1=\det", font_size=40, color=GREEN_C),
            self._matrix([["2"]], scale=0.70),
            MathTex(r"=2", font_size=40, color=GREEN_C),
        ).arrange(RIGHT, buff=0.14)
        second_minor = VGroup(
            MathTex(r"\Delta_2=\det", font_size=40, color=TEAL_C),
            self._matrix([["2", "1"], ["1", "2"]], scale=0.70),
            MathTex(r"=3", font_size=40, color=TEAL_C),
        ).arrange(RIGHT, buff=0.14)
        minor_cards = VGroup(first_minor, second_minor).arrange(RIGHT, buff=0.78)
        minor_cards.move_to(UP * 0.20)
        leading_note = Text(
            "Use the upper-left 1×1 block, then the upper-left 2×2 block.",
            font_size=26,
            color=WHITE,
        ).next_to(minor_cards, DOWN, buff=0.52)
        self.play(FadeIn(first_minor))
        self.play(FadeIn(second_minor))
        self.play(FadeIn(leading_note))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "In a 3×3 matrix, the leading blocks grow from the upper-left corner."
        )
        self.play(FadeOut(minor_cards), FadeOut(leading_note))
        three_matrix = self._matrix(
            [["4", "2", "0"], ["2", "3", "1"], ["0", "1", "2"]],
            scale=0.78,
        ).move_to(LEFT * 2.80 + DOWN * 0.18)
        three_label = MathTex(r"B=", font_size=43).next_to(three_matrix, LEFT, buff=0.16)
        entries = three_matrix.get_entries()
        block_one = SurroundingRectangle(entries[0], color=GREEN_C, buff=0.10)
        block_two = SurroundingRectangle(
            VGroup(*[entries[index] for index in (0, 1, 3, 4)]),
            color=TEAL_C,
            buff=0.16,
        )
        block_three = SurroundingRectangle(three_matrix, color=YELLOW, buff=0.10)
        definition = VGroup(
            MathTex(
                r"B_k=\text{the upper-left }k\times k\text{ block}",
                font_size=37,
                color=WHITE,
            ),
            MathTex(r"\Delta_k=\det(B_k)", font_size=42, color=YELLOW),
            Text(
                "These determinants are the leading principal minors.",
                font_size=24,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.28)
        values = VGroup(
            MathTex(r"\Delta_1=4", font_size=37, color=GREEN_C),
            MathTex(r"\Delta_2=8", font_size=37, color=TEAL_C),
            MathTex(r"\Delta_3=12", font_size=37, color=YELLOW),
        ).arrange(RIGHT, buff=0.48)
        explanation = VGroup(definition, values).arrange(DOWN, buff=0.46)
        explanation.move_to(RIGHT * 2.55 + DOWN * 0.18)
        three_example = VGroup(
            three_matrix, three_label, block_one, block_two, block_three, explanation
        )
        self.play(FadeIn(three_label), FadeIn(three_matrix))
        self.play(Create(block_one), FadeIn(values[0]))
        self.play(Create(block_two), FadeIn(values[1]))
        self.play(Create(block_three), FadeIn(values[2]))
        self.play(FadeIn(definition))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Each pivot is a ratio of consecutive leading principal minors."
        )
        self.play(FadeOut(three_example))
        ratio_rule = MathTex(
            r"\Delta_0=1,\qquad p_k=\frac{\Delta_k}{\Delta_{k-1}}",
            font_size=46,
            color=YELLOW,
        ).move_to(UP * 0.55)
        example_ratios = MathTex(
            r"p_1=\frac{4}{1}=4,\qquad p_2=\frac{8}{4}=2,\qquad p_3=\frac{12}{8}=\frac32",
            font_size=40,
            color=GREEN_C,
        ).next_to(ratio_rule, DOWN, buff=0.38)
        self.play(FadeIn(ratio_rule))
        self.play(FadeIn(example_ratios))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "For a symmetric matrix, three positivity statements are equivalent."
        )
        self.play(FadeOut(ratio_rule), FadeOut(example_ratios))
        energy_box = self._criterion_box(
            "quadratic energy", r"x^T A x>0\quad(x\ne0)", GREEN_C
        )
        pivot_box = self._criterion_box(
            "elimination pivots", r"p_1,p_2,\ldots,p_n>0", TEAL_C
        )
        minor_box = self._criterion_box(
            "leading principal minors", r"\Delta_1,\Delta_2,\ldots,\Delta_n>0", YELLOW
        )
        equivalences = VGroup(energy_box, pivot_box, minor_box).arrange(DOWN, buff=0.26)
        equivalences.move_to(DOWN * 0.26)
        if equivalences.height > 5.05:
            equivalences.scale_to_fit_height(5.05)
        self.play(FadeIn(energy_box))
        self.play(FadeIn(pivot_box))
        self.play(FadeIn(minor_box))
        self.wait(1.9)

        heading = self._replace_heading(
            heading, "Sylvester's criterion tests positive definiteness using only leading blocks."
        )
        self.play(FadeOut(equivalences))
        theorem = MathTex(
            r"\boxed{A=A^T\ \text{is positive definite}"
            r"\quad\Longleftrightarrow\quad"
            r"\Delta_1,\Delta_2,\ldots,\Delta_n>0}",
            font_size=43,
            color=YELLOW,
        )
        application = VGroup(
            MathTex(r"\Delta_1=2>0,\qquad\Delta_2=3>0", font_size=47, color=GREEN_C),
            Text("So the matrix is positive definite.", font_size=36, color=GREEN_C, weight="BOLD"),
        ).arrange(DOWN, buff=0.35)
        final_card = VGroup(theorem, application).arrange(DOWN, buff=0.66)
        final_card.move_to(DOWN * 0.28)
        if final_card.width > 11.4:
            final_card.scale_to_fit_width(11.4)
        self.play(FadeIn(theorem))
        self.play(FadeIn(application))
        self.wait(2.7)
