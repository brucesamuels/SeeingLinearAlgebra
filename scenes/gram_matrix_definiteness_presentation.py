"""Manim presentation: Positive Definite Matrices — Why A-transpose A Is Positive Semidefinite."""
from __future__ import annotations

import numpy as np
from manim import (
    GREEN_C, GREY_B, ORANGE, RED_C, TEAL_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Create, FadeIn, FadeOut, MathTex, Matrix, Rectangle,
    Scene, SurroundingRectangle, Text, VGroup,
)

from engine.gram_matrix_definiteness import GramMatrixDefiniteness


class GramMatrixDefinitenessPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "Why AᵀA Is Positive Semidefinite"

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
        self.play(FadeOut(old), run_time=0.18)
        self.play(FadeIn(new), run_time=0.22)
        return new

    @staticmethod
    def _matrix(entries, scale=0.72, h_buff=0.90, v_buff=0.80):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _card(label, formula, color):
        content = VGroup(
            Text(label, font_size=25, color=color, weight="BOLD"),
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
        model = GramMatrixDefiniteness()
        dependent_model = GramMatrixDefiniteness([[1, 2], [1, 2], [0, 0]])
        if not np.allclose(model.gram_matrix(), [[2, 1], [1, 2]]):
            raise RuntimeError("unexpected Gram matrix")
        if not np.allclose(dependent_model.image([-2, 1]), [0, 0, 0]):
            raise RuntimeError("dependent-column null vector failed")

        banner, title, heading = self._chrome(
            "Cholesky turned positive quadratic energy into a squared norm."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        opening = VGroup(
            MathTex(r"x^TAx=\lVert Rx\rVert^2", font_size=53, color=GREEN_C),
            Text(
                "Does the same squared-norm pattern appear for every matrix?",
                font_size=30,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.55).move_to(DOWN * 0.18)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "A rectangular matrix still produces a symmetric square matrix A-transpose A."
        )
        self.play(FadeOut(opening))
        a_matrix = self._matrix(
            [["1", "0"], ["1", "1"], ["0", "1"]], scale=0.78
        )
        gram_matrix = self._matrix([["2", "1"], ["1", "2"]], scale=0.82)
        construction = VGroup(
            VGroup(MathTex("A=", font_size=43), a_matrix).arrange(RIGHT, buff=0.14),
            MathTex(r"\Longrightarrow", font_size=46, color=YELLOW),
            VGroup(MathTex(r"A^TA=", font_size=43), gram_matrix).arrange(RIGHT, buff=0.14),
        ).arrange(RIGHT, buff=0.60).move_to(DOWN * 0.12)
        if construction.width > 11.2:
            construction.scale_to_fit_width(11.2)
        callback = Text(
            "This is the same matrix that opened the chapter.",
            font_size=28,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(construction[0]))
        self.play(FadeIn(construction[1]), FadeIn(construction[2]))
        self.play(FadeIn(callback))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Its quadratic energy is always a squared length."
        )
        self.play(FadeOut(construction), FadeOut(callback))
        identity = MathTex(
            r"x^T(A^TA)x=(Ax)^T(Ax)=\lVert Ax\rVert^2\ge0",
            font_size=50,
            color=YELLOW,
        ).move_to(UP * 0.30)
        consequence = VGroup(
            Text("Negative Gram energy is impossible.", font_size=31, color=GREEN_C, weight="BOLD"),
            MathTex(r"x^T(A^TA)x<0\quad\text{cannot happen}", font_size=39, color=RED_C),
        ).arrange(DOWN, buff=0.34).next_to(identity, DOWN, buff=0.58)
        self.play(FadeIn(identity))
        self.play(FadeIn(consequence))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Nonnegative energy defines positive semidefiniteness."
        )
        self.play(FadeOut(identity), FadeOut(consequence))
        definition = VGroup(
            Text("positive semidefinite", font_size=38, color=YELLOW, weight="BOLD"),
            MathTex(
                r"M=M^T,\qquad x^TMx\ge0\quad\text{for every }x",
                font_size=48,
                color=WHITE,
            ),
            MathTex(
                r"\boxed{A^TA\ \text{is positive semidefinite}}",
                font_size=49,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.20)
        self.play(FadeIn(definition[0]))
        self.play(FadeIn(definition[1]))
        self.play(FadeIn(definition[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Independent columns rule out every nonzero zero-energy direction."
        )
        self.play(FadeOut(definition))
        independent_a = self._matrix(
            [["1", "0"], ["1", "1"], ["0", "1"]], scale=0.82
        ).move_to(LEFT * 2.65 + DOWN * 0.10)
        columns = independent_a.get_columns()
        column_boxes = VGroup(
            SurroundingRectangle(columns[0], color=TEAL_C, buff=0.13),
            SurroundingRectangle(columns[1], color=ORANGE, buff=0.13),
        )
        independent_logic = VGroup(
            Text("independent columns", font_size=29, color=GREEN_C, weight="BOLD"),
            MathTex(r"\operatorname{null}(A)=\{0\}", font_size=43, color=TEAL_C),
            MathTex(r"x\ne0\Longrightarrow Ax\ne0", font_size=41, color=WHITE),
            MathTex(r"\lVert Ax\rVert^2>0", font_size=46, color=GREEN_C),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 2.45 + DOWN * 0.12)
        self.play(FadeIn(independent_a), Create(column_boxes))
        self.play(FadeIn(independent_logic[0]), FadeIn(independent_logic[1]))
        self.play(FadeIn(independent_logic[2]), FadeIn(independent_logic[3]))
        self.wait(2.0)

        prediction = Text(
            "Pause: when can a nonzero vector still have zero Gram energy?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "Zero energy occurs exactly when A sends a nonzero vector to zero."
        )
        zero_equivalence = MathTex(
            r"x^TA^TAx=0\quad\Longleftrightarrow\quad\lVert Ax\rVert^2=0"
            r"\quad\Longleftrightarrow\quad Ax=0",
            font_size=44,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.50)
        if zero_equivalence.width > 11.2:
            zero_equivalence.scale_to_fit_width(11.2)
        self.play(FadeIn(zero_equivalence))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Dependent columns create an explicit nonzero null-space direction."
        )
        self.play(
            FadeOut(independent_a), FadeOut(column_boxes),
            FadeOut(independent_logic), FadeOut(zero_equivalence),
        )
        b_matrix = self._matrix(
            [["1", "2"], ["1", "2"], ["0", "0"]], scale=0.76
        )
        x_vector = self._matrix([["-2"], ["1"]], scale=0.70)
        zero_vector = self._matrix([["0"], ["0"], ["0"]], scale=0.66)
        null_product = VGroup(
            VGroup(MathTex("B=", font_size=40), b_matrix).arrange(RIGHT, buff=0.12),
            MathTex(r"\cdot", font_size=36),
            x_vector,
            MathTex("=", font_size=40),
            zero_vector,
        ).arrange(RIGHT, buff=0.34).move_to(UP * 0.20)
        vector_label = MathTex(
            r"x=(-2,1)^T\ne0,\qquad Bx=0",
            font_size=41,
            color=TEAL_C,
        ).next_to(null_product, DOWN, buff=0.38)
        zero_energy = MathTex(
            r"x^TB^TBx=\lVert Bx\rVert^2=0",
            font_size=46,
            color=YELLOW,
        ).next_to(vector_label, DOWN, buff=0.34)
        self.play(FadeIn(null_product))
        self.play(FadeIn(vector_label))
        self.play(FadeIn(zero_energy))
        self.wait(2.1)

        heading = self._replace_heading(
            heading, "The dependent-column Gram matrix is semidefinite, but not definite."
        )
        self.play(FadeOut(null_product), FadeOut(vector_label), FadeOut(zero_energy))
        b_gram = self._matrix([["2", "4"], ["4", "8"]], scale=0.84)
        gram_card = VGroup(
            MathTex(r"B^TB=", font_size=43), b_gram
        ).arrange(RIGHT, buff=0.14).move_to(UP * 0.32)
        comparison = VGroup(
            self._card("never negative", r"x^TB^TBx\ge0", GREEN_C),
            self._card("zero is possible", r"x=(-2,1)^T\ne0", YELLOW),
        ).arrange(RIGHT, buff=0.55).next_to(gram_card, DOWN, buff=0.56)
        conclusion = Text(
            "positive semidefinite — not positive definite",
            font_size=31,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.50)
        self.play(FadeIn(gram_card))
        self.play(FadeIn(comparison))
        self.play(FadeIn(conclusion))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Column independence is exactly what upgrades semidefinite to definite."
        )
        self.play(FadeOut(gram_card), FadeOut(comparison), FadeOut(conclusion))
        universal = MathTex(
            r"\boxed{A^TA\ \text{is always positive semidefinite}}",
            font_size=46,
            color=GREEN_C,
        )
        criterion = MathTex(
            r"\boxed{A^TA\ \text{is positive definite}"
            r"\quad\Longleftrightarrow\quad A\ \text{has independent columns}}",
            font_size=43,
            color=YELLOW,
        )
        final_card = VGroup(universal, criterion).arrange(DOWN, buff=0.62)
        final_card.move_to(DOWN * 0.20)
        if final_card.width > 11.4:
            final_card.scale_to_fit_width(11.4)
        self.play(FadeIn(universal))
        self.play(FadeIn(criterion))
        self.wait(2.8)
