"""Manim presentation: Positive Definite Matrices — Why Least Squares Has a Unique Solution."""
from __future__ import annotations

import numpy as np
from manim import (
    GREEN_C, GREY_B, ORANGE, RED_C, TEAL_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    FadeIn, FadeOut, MathTex, Matrix, Rectangle, Scene, Tex, Text, VGroup,
)

from engine.least_squares_uniqueness import LeastSquaresUniqueness


class LeastSquaresUniquenessPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "Why Least Squares Has a Unique Solution"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Tex(
            r"\textbf{POSITIVE DEFINITE MATRICES}", font_size=24, color=GREY_B
        ).to_edge(UP, buff=0.16)
        title = Tex(
            r"\textbf{Why Least Squares Has a Unique Solution}",
            font_size=34,
            color=YELLOW,
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
        model = LeastSquaresUniqueness()
        dependent = LeastSquaresUniqueness(
            [[1, 2], [1, 2], [0, 0]], [3, 3, 1]
        )
        solution = model.unique_solution()
        if not np.allclose(solution, [1, 1]):
            raise RuntimeError("unexpected least-squares solution")
        if not np.allclose(model.normal_residual(solution), [0, 0]):
            raise RuntimeError("least-squares residual is not orthogonal")
        first = np.array([3.0, 0.0])
        second = dependent.shifted_coefficient(first, [-2, 1], 1.0)
        if not np.allclose(dependent.fitted_vector(first), dependent.fitted_vector(second)):
            raise RuntimeError("dependent-column fits should agree")

        banner, title, heading = self._chrome(
            "CP205 showed when a Gram matrix is positive definite."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        opening = VGroup(
            MathTex(
                r"A\ \text{has independent columns}"
                r"\quad\Longleftrightarrow\quad A^TA\ \text{is positive definite}",
                font_size=42,
                color=GREEN_C,
            ),
            Text(
                "What does that guarantee in least squares?",
                font_size=32,
                color=YELLOW,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.60).move_to(DOWN * 0.12)
        if opening.width > 11.3:
            opening.scale_to_fit_width(11.3)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Least squares chooses coefficients that make Ax as close as possible to b."
        )
        self.play(FadeOut(opening))
        a_matrix = self._matrix(
            [["1", "0"], ["1", "1"], ["0", "1"]], scale=0.74
        )
        b_vector = self._matrix([["2"], ["1"], ["2"]], scale=0.68)
        data = VGroup(
            VGroup(MathTex("A=", font_size=40), a_matrix).arrange(RIGHT, buff=0.14),
            VGroup(MathTex("b=", font_size=40), b_vector).arrange(RIGHT, buff=0.14),
        ).arrange(RIGHT, buff=1.25).move_to(UP * 0.10)
        objective = MathTex(
            r"\widehat x\ \text{minimizes}\quad\lVert Ax-b\rVert^2",
            font_size=48,
            color=YELLOW,
        ).next_to(data, DOWN, buff=0.52)
        self.play(FadeIn(data))
        self.play(FadeIn(objective))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Residual orthogonality produces the normal equations."
        )
        self.play(FadeOut(data), FadeOut(objective))
        residual_logic = VGroup(
            MathTex(r"r=b-A\widehat x", font_size=44, color=WHITE),
            MathTex(r"A^Tr=0", font_size=48, color=TEAL_C),
            MathTex(
                r"\boxed{A^TA\widehat x=A^Tb}",
                font_size=53,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.12)
        self.play(FadeIn(residual_logic[0]))
        self.play(FadeIn(residual_logic[1]))
        self.play(FadeIn(residual_logic[2]))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "For this example, the normal equations are a two-by-two system."
        )
        self.play(FadeOut(residual_logic))
        gram = self._matrix([["2", "1"], ["1", "2"]], scale=0.82)
        unknown = self._matrix([[r"\widehat x_1"], [r"\widehat x_2"]], scale=0.66)
        rhs = self._matrix([["3"], ["3"]], scale=0.72)
        normal_system = VGroup(
            gram,
            unknown,
            MathTex("=", font_size=42),
            rhs,
        ).arrange(RIGHT, buff=0.38).move_to(DOWN * 0.02)
        labels = VGroup(
            MathTex(r"A^TA", font_size=34, color=GREEN_C).next_to(gram, DOWN, buff=0.22),
            MathTex(r"\widehat x", font_size=34, color=TEAL_C).next_to(unknown, DOWN, buff=0.22),
            MathTex(r"A^Tb", font_size=34, color=ORANGE).next_to(rhs, DOWN, buff=0.22),
        )
        self.play(FadeIn(normal_system), FadeIn(labels))
        self.wait(1.5)
        prediction = Text(
            "Pause: why must this system have exactly one solution?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "Positive definiteness makes the normal-equation matrix invertible."
        )
        self.play(FadeOut(normal_system), FadeOut(labels))
        implication = VGroup(
            self._card("independent columns", r"\operatorname{null}(A)=\{0\}", TEAL_C),
            MathTex(r"\Longrightarrow", font_size=43, color=YELLOW),
            self._card("positive definite", r"x^TA^TAx>0", GREEN_C),
            MathTex(r"\Longrightarrow", font_size=43, color=YELLOW),
            self._card("invertible", r"\operatorname{null}(A^TA)=\{0\}", ORANGE),
        ).arrange(RIGHT, buff=0.28).move_to(DOWN * 0.08)
        if implication.width > 11.4:
            implication.scale_to_fit_width(11.4)
        self.play(FadeIn(implication[0]))
        self.play(FadeIn(implication[1]), FadeIn(implication[2]))
        self.play(FadeIn(implication[3]), FadeIn(implication[4]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Solving gives one coefficient vector and one closest fitted vector."
        )
        self.play(FadeOut(implication))
        solved_gram = self._matrix([["2", "1"], ["1", "2"]], scale=0.76)
        solved_x = self._matrix([["1"], ["1"]], scale=0.70)
        solved_rhs = self._matrix([["3"], ["3"]], scale=0.70)
        solved_system = VGroup(
            solved_gram, solved_x, MathTex("=", font_size=40), solved_rhs
        ).arrange(RIGHT, buff=0.34).move_to(UP * 0.32)
        answer = MathTex(
            r"\widehat x=(1,1)^T",
            font_size=44,
            color=GREEN_C,
        ).next_to(solved_system, DOWN, buff=0.36)
        fitted = MathTex(
            r"A\widehat x=(1,2,1)^T",
            font_size=42,
            color=TEAL_C,
        ).next_to(answer, DOWN, buff=0.30)
        self.play(FadeIn(solved_system))
        self.play(FadeIn(answer), FadeIn(fitted))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "The residual confirms the least-squares orthogonality condition."
        )
        self.play(FadeOut(solved_system), FadeOut(answer), FadeOut(fitted))
        residual_vector = self._matrix([["1"], ["-1"], ["1"]], scale=0.72)
        zero_vector = self._matrix([["0"], ["0"]], scale=0.72)
        residual_check = VGroup(
            VGroup(MathTex(r"r=b-A\widehat x=", font_size=40), residual_vector).arrange(RIGHT, buff=0.16),
            VGroup(MathTex(r"A^Tr=", font_size=42), zero_vector).arrange(RIGHT, buff=0.16),
        ).arrange(RIGHT, buff=1.15).move_to(DOWN * 0.02)
        callback = Text(
            "The unique coefficients produce the orthogonal projection.",
            font_size=29,
            color=GREEN_C,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(residual_check))
        self.play(FadeIn(callback))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Dependent columns can describe the same fitted vector in different ways."
        )
        self.play(FadeOut(residual_check), FadeOut(callback))
        b_matrix = self._matrix(
            [["1", "2"], ["1", "2"], ["0", "0"]], scale=0.72
        )
        x_one = self._matrix([["3"], ["0"]], scale=0.64)
        x_two = self._matrix([["1"], ["1"]], scale=0.64)
        dependent_data = VGroup(
            VGroup(MathTex("B=", font_size=38), b_matrix).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"x_1=", font_size=36), x_one).arrange(RIGHT, buff=0.10),
            VGroup(MathTex(r"x_2=", font_size=36), x_two).arrange(RIGHT, buff=0.10),
        ).arrange(RIGHT, buff=0.70).move_to(UP * 0.18)
        same_fit = MathTex(
            r"Bx_1=Bx_2=(3,3,0)^T",
            font_size=46,
            color=YELLOW,
        ).next_to(dependent_data, DOWN, buff=0.44)
        distinct = Text(
            "Different coefficients — exactly the same fit",
            font_size=30,
            color=RED_C,
            weight="BOLD",
        ).next_to(same_fit, DOWN, buff=0.34)
        self.play(FadeIn(dependent_data))
        self.play(FadeIn(same_fit))
        self.play(FadeIn(distinct))
        self.wait(2.1)

        heading = self._replace_heading(
            heading, "A null-space direction creates an entire family of equivalent coefficients."
        )
        self.play(FadeOut(dependent_data), FadeOut(same_fit), FadeOut(distinct))
        null_family = VGroup(
            MathTex(r"z=(-2,1)^T,\qquad Bz=0", font_size=45, color=TEAL_C),
            MathTex(r"B(x+tz)=Bx+tBz=Bx", font_size=47, color=YELLOW),
            Text(
                "No unique coefficient vector",
                font_size=32,
                color=RED_C,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.46).move_to(DOWN * 0.10)
        self.play(FadeIn(null_family[0]))
        self.play(FadeIn(null_family[1]))
        self.play(FadeIn(null_family[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Full column rank is the condition that guarantees unique least-squares coefficients."
        )
        self.play(FadeOut(null_family))
        final = VGroup(
            MathTex(
                r"\boxed{A\ \text{has full column rank}}",
                font_size=46,
                color=GREEN_C,
            ),
            MathTex(r"\Downarrow", font_size=40, color=YELLOW),
            MathTex(
                r"\boxed{A^TA\ \text{is positive definite and invertible}}",
                font_size=45,
                color=GREEN_C,
            ),
            MathTex(r"\Downarrow", font_size=40, color=YELLOW),
            MathTex(
                r"\boxed{\widehat x\ \text{is the unique least-squares coefficient vector}}",
                font_size=43,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.23).move_to(DOWN * 0.14)
        if final.width > 11.4:
            final.scale_to_fit_width(11.4)
        self.play(FadeIn(final[0]))
        self.play(FadeIn(final[1]), FadeIn(final[2]))
        self.play(FadeIn(final[3]), FadeIn(final[4]))
        self.wait(2.8)
