"""Manim presentation: Positive Definite Matrices — The LDL-Transpose Factorization."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, TEAL_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, MathTex, Matrix, Rectangle,
    ReplacementTransform, Scene, SurroundingRectangle, Text, VGroup,
)

from engine.positive_definite_ldlt import PositiveDefiniteLDLT


class PositiveDefiniteLDLTPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "The LDLᵀ Factorization"

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
    def _matrix(entries, scale=0.70, h_buff=0.82, v_buff=0.72):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _arrow_with_label(label, color=YELLOW):
        arrow = Arrow(LEFT, RIGHT, buff=0, color=color, stroke_width=3.4)
        text = MathTex(label, font_size=29, color=color).next_to(arrow, UP, buff=0.10)
        return VGroup(arrow, text)

    @staticmethod
    def _card(label, formula, color):
        content = VGroup(
            Text(label, font_size=24, color=color, weight="BOLD"),
            MathTex(formula, font_size=39, color=WHITE),
        ).arrange(DOWN, buff=0.20)
        border = Rectangle(
            width=content.width + 0.46,
            height=content.height + 0.38,
            color=color,
            stroke_width=2.4,
        ).move_to(content)
        return VGroup(border, content)

    def construct(self):
        model = PositiveDefiniteLDLT()
        lower = model.lower_factor()
        diagonal = model.diagonal_entries()
        reconstructed = model.reconstruct()
        if not np.allclose(reconstructed, model.matrix):
            raise RuntimeError("LDL-transpose reconstruction failed")

        banner, title, heading = self._chrome(
            "The pivots are known. Now keep the elimination multipliers too."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        source = VGroup(
            MathTex(r"A=", font_size=43),
            self._matrix([["4", "2", "0"], ["2", "3", "1"], ["0", "1", "2"]]),
        ).arrange(RIGHT, buff=0.14)
        pivots = MathTex(
            r"p_1=4,\qquad p_2=2,\qquad p_3=\tfrac{3}{2}",
            font_size=43,
            color=GREEN_C,
        )
        question = Text(
            "Where do the elimination multipliers go?",
            font_size=31,
            color=YELLOW,
        )
        opening = VGroup(source, pivots, question).arrange(DOWN, buff=0.40)
        opening.move_to(DOWN * 0.24)
        self.play(FadeIn(source), FadeIn(pivots))
        self.play(FadeIn(question))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Symmetric elimination leaves a smaller symmetric active block."
        )
        self.play(FadeOut(opening))
        matrix_a = self._matrix(
            [["4", "2", "0"], ["2", "3", "1"], ["0", "1", "2"]],
            scale=0.66,
        )
        first_arrow = self._arrow_with_label(r"p_1=4")
        schur_two = self._matrix([["2", "1"], ["1", "2"]], scale=0.72)
        second_arrow = self._arrow_with_label(r"p_2=2")
        schur_one = self._matrix([[r"\tfrac{3}{2}"]], scale=0.72)
        shrinking = VGroup(
            matrix_a, first_arrow, schur_two, second_arrow, schur_one
        ).arrange(RIGHT, buff=0.50).move_to(UP * 0.18)
        if shrinking.width > 11.2:
            shrinking.scale_to_fit_width(11.2)
        multiplier_one = MathTex(
            r"\ell_{21}=\tfrac{2}{4}=\tfrac{1}{2},\qquad \ell_{31}=0",
            font_size=37,
            color=TEAL_C,
        ).next_to(first_arrow, DOWN, buff=0.38)
        multiplier_two = MathTex(
            r"\ell_{32}=\tfrac{1}{2}",
            font_size=37,
            color=ORANGE,
        ).next_to(second_arrow, DOWN, buff=0.38)
        final_pivot = MathTex(
            r"p_3=\tfrac{3}{2}", font_size=37, color=GREEN_C
        ).next_to(schur_one, DOWN, buff=0.38)
        self.play(FadeIn(matrix_a))
        self.play(FadeIn(first_arrow), FadeIn(schur_two), FadeIn(multiplier_one))
        self.play(FadeIn(second_arrow), FadeIn(schur_one), FadeIn(multiplier_two))
        self.play(FadeIn(final_pivot))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Multipliers fill L below the diagonal; pivots fill D."
        )
        self.play(
            FadeOut(shrinking), FadeOut(multiplier_one),
            FadeOut(multiplier_two), FadeOut(final_pivot),
        )
        l_matrix = self._matrix(
            [["1", "0", "0"], [r"\tfrac{1}{2}", "1", "0"], ["0", r"\tfrac{1}{2}", "1"]],
            scale=0.82,
            v_buff=0.94,
        )
        d_matrix = self._matrix(
            [["4", "0", "0"], ["0", "2", "0"], ["0", "0", r"\tfrac{3}{2}"]],
            scale=0.82,
            v_buff=0.94,
        )
        l_card = VGroup(MathTex("L=", font_size=43), l_matrix).arrange(RIGHT, buff=0.14)
        d_card = VGroup(MathTex("D=", font_size=43), d_matrix).arrange(RIGHT, buff=0.14)
        factors = VGroup(l_card, d_card).arrange(RIGHT, buff=1.00).move_to(DOWN * 0.10)
        l_entries = l_matrix.get_entries()
        d_entries = d_matrix.get_entries()
        multiplier_boxes = VGroup(
            SurroundingRectangle(l_entries[3], color=TEAL_C, buff=0.10),
            SurroundingRectangle(l_entries[6], color=TEAL_C, buff=0.10),
            SurroundingRectangle(l_entries[7], color=ORANGE, buff=0.10),
        )
        pivot_boxes = VGroup(
            *[
                SurroundingRectangle(d_entries[index], color=GREEN_C, buff=0.10)
                for index in (0, 4, 8)
            ]
        )
        factor_note = Text(
            "L stores the row multipliers; D stores the elimination pivots.",
            font_size=27,
            color=WHITE,
        ).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(l_card), Create(multiplier_boxes))
        self.play(FadeIn(d_card), Create(pivot_boxes))
        self.play(FadeIn(factor_note))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "For a symmetric matrix, the matching factor on the right is L-transpose."
        )
        self.play(
            FadeOut(factors), FadeOut(multiplier_boxes),
            FadeOut(pivot_boxes), FadeOut(factor_note),
        )
        product_l = self._matrix(
            [["1", "0", "0"], [r"\tfrac{1}{2}", "1", "0"], ["0", r"\tfrac{1}{2}", "1"]],
            scale=0.68,
            h_buff=1.12,
            v_buff=0.94,
        )
        product_d = self._matrix(
            [["4", "0", "0"], ["0", "2", "0"], ["0", "0", r"\tfrac{3}{2}"]],
            scale=0.68,
            h_buff=1.12,
            v_buff=0.94,
        )
        product_lt = self._matrix(
            [["1", r"\tfrac{1}{2}", "0"], ["0", "1", r"\tfrac{1}{2}"], ["0", "0", "1"]],
            scale=0.68,
            h_buff=1.12,
            v_buff=0.94,
        )
        product_a = self._matrix(
            [["4", "2", "0"], ["2", "3", "1"], ["0", "1", "2"]],
            scale=0.68,
            h_buff=1.12,
            v_buff=0.94,
        )
        factor_l = VGroup(
            MathTex("L", font_size=31, color=TEAL_C), product_l
        ).arrange(DOWN, buff=0.12)
        factor_d = VGroup(
            MathTex("D", font_size=31, color=GREEN_C), product_d
        ).arrange(DOWN, buff=0.12)
        factor_lt = VGroup(
            MathTex(r"L^T", font_size=31, color=ORANGE), product_lt
        ).arrange(DOWN, buff=0.12)
        factor_product = VGroup(
            factor_l,
            MathTex(r"\cdot", font_size=34, color=WHITE),
            factor_d,
            MathTex(r"\cdot", font_size=34, color=WHITE),
            factor_lt,
        ).arrange(RIGHT, buff=0.24)
        result = VGroup(
            MathTex(r"=", font_size=40),
            VGroup(MathTex("A", font_size=31, color=YELLOW), product_a).arrange(
                DOWN, buff=0.12
            ),
        ).arrange(RIGHT, buff=0.24)
        identity = MathTex(r"\boxed{A=LDL^T}", font_size=47, color=YELLOW)
        verification = VGroup(factor_product, result, identity).arrange(DOWN, buff=0.28)
        verification.move_to(DOWN * 0.24)
        if verification.height > 5.0:
            verification.scale_to_fit_height(5.0)
        self.play(FadeIn(factor_l))
        self.play(FadeIn(factor_product[1]), FadeIn(factor_d))
        self.play(FadeIn(factor_product[3]), FadeIn(factor_lt))
        self.play(FadeIn(result))
        self.play(FadeIn(identity))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The factorization changes the quadratic energy into diagonal coordinates."
        )
        self.play(FadeOut(verification))
        energy_chain = VGroup(
            MathTex(r"x^TAx=x^TLDL^Tx", font_size=50, color=WHITE),
            MathTex(r"y=L^Tx", font_size=48, color=TEAL_C),
            MathTex(r"x^TAx=y^TDy", font_size=54, color=YELLOW),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.18)
        self.play(FadeIn(energy_chain[0]))
        self.play(FadeIn(energy_chain[1]))
        self.play(FadeIn(energy_chain[2]))
        self.wait(1.9)

        heading = self._replace_heading(
            heading, "L-transpose supplies the completed-square coordinates."
        )
        self.play(FadeOut(energy_chain))
        y_vector = self._matrix(
            [[r"x_1+\tfrac{1}{2}x_2"], [r"x_2+\tfrac{1}{2}x_3"], [r"x_3"]],
            scale=0.78,
        )
        coordinates = VGroup(
            MathTex(r"y=L^Tx=", font_size=43, color=TEAL_C), y_vector
        ).arrange(RIGHT, buff=0.16)
        squares = MathTex(
            r"x^TAx="
            r"4\left(x_1+\tfrac{1}{2}x_2\right)^2"
            r"+2\left(x_2+\tfrac{1}{2}x_3\right)^2"
            r"+\tfrac{3}{2}x_3^2",
            font_size=44,
            color=YELLOW,
        )
        square_card = VGroup(coordinates, squares).arrange(DOWN, buff=0.58)
        square_card.move_to(DOWN * 0.20)
        if square_card.width > 11.3:
            square_card.scale_to_fit_width(11.3)
        self.play(FadeIn(coordinates))
        self.play(FadeIn(squares))
        self.wait(2.1)

        heading = self._replace_heading(
            heading, "One factor changes coordinates; the other controls their signs."
        )
        self.play(FadeOut(square_card))
        l_role = self._card("L is invertible", r"x\ne0\iff L^Tx\ne0", TEAL_C)
        d_role = self._card("D is diagonal", r"y^TDy=\sum_i d_i y_i^2", GREEN_C)
        roles = VGroup(l_role, d_role).arrange(RIGHT, buff=0.68).move_to(DOWN * 0.12)
        if roles.width > 11.2:
            roles.scale_to_fit_width(11.2)
        self.play(FadeIn(l_role), FadeIn(d_role))
        prediction = Text(
            "Pause: which factor decides whether the energy is always positive?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.24)
        self.play(FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "The signs on D's diagonal decide positive definiteness."
        )
        sign_answer = MathTex(
            r"d_1,d_2,\ldots,d_n>0\quad\Longrightarrow\quad y^TDy>0\ (y\ne0)",
            font_size=43,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.32)
        if sign_answer.width > 11.2:
            sign_answer.scale_to_fit_width(11.2)
        self.play(FadeIn(sign_answer))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "LDL-transpose makes the positive-pivot test visible in matrix form."
        )
        self.play(FadeOut(roles), FadeOut(sign_answer))
        theorem = MathTex(
            r"\boxed{A=A^T\ \text{is positive definite}\quad\Longleftrightarrow\quad A=LDL^T\ \text{with }d_1,d_2,\ldots,d_n>0}",
            font_size=40,
            color=YELLOW,
        )
        application = VGroup(
            MathTex(r"D=\operatorname{diag}\left(4,2,\tfrac{3}{2}\right)", font_size=46, color=GREEN_C),
            Text("Every diagonal entry is positive.", font_size=34, color=GREEN_C),
            Text("So the matrix is positive definite.", font_size=36, color=GREEN_C, weight="BOLD"),
        ).arrange(DOWN, buff=0.28)
        final_card = VGroup(theorem, application).arrange(DOWN, buff=0.58)
        final_card.move_to(DOWN * 0.24)
        if final_card.width > 11.4:
            final_card.scale_to_fit_width(11.4)
        self.play(FadeIn(theorem))
        self.play(FadeIn(application))
        self.wait(2.7)
