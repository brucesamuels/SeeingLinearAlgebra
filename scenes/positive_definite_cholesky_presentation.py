"""Manim presentation: Positive Definite Matrices — Cholesky: A Matrix Square Root."""
from __future__ import annotations

import numpy as np
from manim import (
    GREEN_C, GREY_B, ORANGE, RED_C, TEAL_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Create, FadeIn, FadeOut, MathTex, Matrix, Rectangle,
    ReplacementTransform, Scene, SurroundingRectangle, Text, VGroup,
)

from engine.positive_definite_cholesky import PositiveDefiniteCholesky


class PositiveDefiniteCholeskyPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "Cholesky: A Matrix Square Root"

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
    def _matrix(entries, scale=0.70, h_buff=0.90, v_buff=0.80):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _card(label, formulas, color):
        formula_group = VGroup(
            *[MathTex(formula, font_size=34, color=WHITE) for formula in formulas]
        ).arrange(DOWN, buff=0.18)
        content = VGroup(
            Text(label, font_size=24, color=color, weight="BOLD"), formula_group
        ).arrange(DOWN, buff=0.22)
        border = Rectangle(
            width=content.width + 0.44,
            height=content.height + 0.36,
            color=color,
            stroke_width=2.4,
        ).move_to(content)
        return VGroup(border, content)

    def construct(self):
        model = PositiveDefiniteCholesky()
        upper = model.upper_factor()
        steps = model.construction_steps()
        if len(steps) != 6 or not np.allclose(model.reconstruct(), model.matrix):
            raise RuntimeError("Cholesky construction verification failed")

        banner, title, heading = self._chrome(
            "The LDL-transpose factorization has one more simplification when D is positive."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        source = VGroup(
            MathTex(r"A=LDL^T", font_size=48, color=WHITE),
            MathTex(
                r"D=\operatorname{diag}\left(4,2,\tfrac{3}{2}\right)>0",
                font_size=46,
                color=GREEN_C,
            ),
            Text(
                "What does positivity let us do to the diagonal factor?",
                font_size=30,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.46).move_to(DOWN * 0.22)
        self.play(FadeIn(source[0]), FadeIn(source[1]))
        self.play(FadeIn(source[2]))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Every positive pivot has a positive square root."
        )
        self.play(FadeOut(source))
        d_matrix = self._matrix(
            [["4", "0", "0"], ["0", "2", "0"], ["0", "0", r"\tfrac{3}{2}"]],
            scale=0.76,
            h_buff=1.04,
            v_buff=0.92,
        )
        root_matrix = self._matrix(
            [
                ["2", "0", "0"],
                ["0", r"\sqrt2", "0"],
                ["0", "0", r"\sqrt{\tfrac32}"],
            ],
            scale=0.76,
            h_buff=1.08,
            v_buff=0.92,
        )
        d_card = VGroup(MathTex("D=", font_size=42), d_matrix).arrange(RIGHT, buff=0.14)
        root_card = VGroup(
            MathTex(r"D^{1/2}=", font_size=42, color=YELLOW), root_matrix
        ).arrange(RIGHT, buff=0.14)
        square_roots = VGroup(d_card, root_card).arrange(RIGHT, buff=0.92)
        square_roots.move_to(DOWN * 0.06)
        diagonal_boxes = VGroup(
            *[
                SurroundingRectangle(root_matrix.get_entries()[index], color=GREEN_C, buff=0.10)
                for index in (0, 4, 8)
            ]
        )
        relation = MathTex(
            r"D=D^{1/2}D^{1/2}", font_size=45, color=YELLOW
        ).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(d_card))
        self.play(FadeIn(root_card), Create(diagonal_boxes))
        self.play(FadeIn(relation))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Absorb the square roots into the two triangular factors."
        )
        self.play(FadeOut(square_roots), FadeOut(diagonal_boxes), FadeOut(relation))
        absorption = VGroup(
            MathTex(
                r"A=L\,D^{1/2}D^{1/2}L^T",
                font_size=49,
                color=WHITE,
            ),
            MathTex(r"R=D^{1/2}L^T", font_size=50, color=TEAL_C),
            MathTex(r"\boxed{A=R^TR}", font_size=54, color=YELLOW),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.18)
        self.play(FadeIn(absorption[0]))
        self.play(FadeIn(absorption[1]))
        self.play(FadeIn(absorption[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The positive square roots form an upper-triangular factor R."
        )
        self.play(FadeOut(absorption))
        r_matrix = self._matrix(
            [
                ["2", "1", "0"],
                ["0", r"\sqrt2", r"\tfrac1{\sqrt2}"],
                ["0", "0", r"\sqrt{\tfrac32}"],
            ],
            scale=0.84,
            h_buff=1.20,
            v_buff=1.00,
        )
        r_card = VGroup(MathTex("R=", font_size=46), r_matrix).arrange(RIGHT, buff=0.16)
        positive_diagonal = VGroup(
            *[
                SurroundingRectangle(r_matrix.get_entries()[index], color=GREEN_C, buff=0.11)
                for index in (0, 4, 8)
            ]
        )
        r_note = Text(
            "Upper triangular, with a positive diagonal.",
            font_size=29,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.32)
        self.play(FadeIn(r_card), Create(positive_diagonal))
        self.play(FadeIn(r_note))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Multiplying R-transpose by R reconstructs the original matrix."
        )
        self.play(FadeOut(r_card), FadeOut(positive_diagonal), FadeOut(r_note))
        rt_matrix = self._matrix(
            [
                ["2", "0", "0"],
                ["1", r"\sqrt2", "0"],
                ["0", r"\tfrac1{\sqrt2}", r"\sqrt{\tfrac32}"],
            ],
            scale=0.66,
            h_buff=1.16,
            v_buff=0.98,
        )
        verify_r = self._matrix(
            [
                ["2", "1", "0"],
                ["0", r"\sqrt2", r"\tfrac1{\sqrt2}"],
                ["0", "0", r"\sqrt{\tfrac32}"],
            ],
            scale=0.66,
            h_buff=1.16,
            v_buff=0.98,
        )
        verify_a = self._matrix(
            [["4", "2", "0"], ["2", "3", "1"], ["0", "1", "2"]],
            scale=0.70,
            h_buff=1.02,
            v_buff=0.90,
        )
        factor_line = VGroup(
            VGroup(MathTex(r"R^T", font_size=30, color=ORANGE), rt_matrix).arrange(DOWN, buff=0.12),
            MathTex(r"\cdot", font_size=36),
            VGroup(MathTex(r"R", font_size=30, color=TEAL_C), verify_r).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=0.28)
        result_line = VGroup(
            MathTex(r"=", font_size=40),
            VGroup(MathTex("A", font_size=30, color=YELLOW), verify_a).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=0.24)
        verification = VGroup(factor_line, result_line).arrange(DOWN, buff=0.28)
        verification.move_to(DOWN * 0.22)
        if verification.height > 5.0:
            verification.scale_to_fit_height(5.0)
        self.play(FadeIn(factor_line[0]))
        self.play(FadeIn(factor_line[1]), FadeIn(factor_line[2]))
        self.play(FadeIn(result_line))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Cholesky builds R from left to right, one row at a time."
        )
        self.play(FadeOut(verification))
        row_one = self._card(
            "first row",
            (r"r_{11}=\sqrt4=2", r"r_{12}=2/r_{11}=1", r"r_{13}=0"),
            TEAL_C,
        )
        row_two = self._card(
            "second row",
            (
                r"r_{22}=\sqrt{3-r_{12}^2}=\sqrt2",
                r"r_{23}=\tfrac{1-r_{12}r_{13}}{r_{22}}=\tfrac1{\sqrt2}",
            ),
            ORANGE,
        )
        row_three = self._card(
            "final diagonal",
            (r"r_{33}=\sqrt{2-r_{13}^2-r_{23}^2}=\sqrt{\tfrac32}",),
            GREEN_C,
        )
        construction = VGroup(row_one, row_two, row_three).arrange(DOWN, buff=0.22)
        construction.move_to(DOWN * 0.22)
        if construction.height > 5.05:
            construction.scale_to_fit_height(5.05)
        self.play(FadeIn(row_one))
        self.play(FadeIn(row_two))
        self.play(FadeIn(row_three))
        self.wait(2.1)

        heading = self._replace_heading(
            heading, "Every diagonal step requires one more positive radicand."
        )
        self.play(FadeOut(construction))
        diagonal_rule = MathTex(
            r"r_{kk}=\sqrt{a_{kk}-\sum_{i<k}r_{ik}^2}",
            font_size=52,
            color=YELLOW,
        ).move_to(UP * 0.36)
        pivot_note = Text(
            "The expression under the radical is the next elimination pivot.",
            font_size=28,
            color=WHITE,
        ).next_to(diagonal_rule, DOWN, buff=0.45)
        self.play(FadeIn(diagonal_rule), FadeIn(pivot_note))
        prediction = Text(
            "Pause: what would prevent the next positive square root from existing?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.24)
        self.play(FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "A zero or negative pivot stops the positive-diagonal construction."
        )
        failure = VGroup(
            MathTex(r"\text{pivot}=0", font_size=42, color=ORANGE),
            MathTex(r"\text{pivot}<0", font_size=42, color=RED_C),
        ).arrange(RIGHT, buff=1.10).to_edge(DOWN, buff=0.36)
        self.play(FadeIn(failure))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Cholesky turns quadratic energy into an ordinary squared length."
        )
        self.play(FadeOut(diagonal_rule), FadeOut(pivot_note), FadeOut(failure))
        norm_chain = VGroup(
            MathTex(r"x^TAx=x^TR^TRx", font_size=50, color=WHITE),
            MathTex(r"x^TAx=(Rx)^T(Rx)", font_size=50, color=TEAL_C),
            MathTex(r"\boxed{x^TAx=\lVert Rx\rVert^2}", font_size=55, color=YELLOW),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.20)
        self.play(FadeIn(norm_chain[0]))
        self.play(FadeIn(norm_chain[1]))
        self.play(FadeIn(norm_chain[2]))
        self.wait(2.1)

        heading = self._replace_heading(
            heading, "Positive definite matrices are exactly the matrices with this triangular square root."
        )
        self.play(FadeOut(norm_chain))
        theorem = MathTex(
            r"\boxed{A=A^T\ \text{is positive definite}\quad\Longleftrightarrow\quad A=R^TR}",
            font_size=43,
            color=YELLOW,
        )
        uniqueness = VGroup(
            Text("R is the unique upper-triangular factor", font_size=34, color=GREEN_C),
            Text("with positive diagonal entries.", font_size=30, color=GREEN_C),
        ).arrange(DOWN, buff=0.24)
        application = MathTex(
            r"\operatorname{diag}(R)=\left(2,\sqrt2,\sqrt{\tfrac32}\right)>0",
            font_size=43,
            color=GREEN_C,
        )
        final_card = VGroup(theorem, uniqueness, application).arrange(DOWN, buff=0.54)
        final_card.move_to(DOWN * 0.24)
        if final_card.width > 11.4:
            final_card.scale_to_fit_width(11.4)
        self.play(FadeIn(theorem))
        self.play(FadeIn(uniqueness), FadeIn(application))
        self.wait(2.8)
