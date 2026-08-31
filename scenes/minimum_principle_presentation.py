"""Manim presentation: Positive Definite Matrices — The Minimum Principle."""
from __future__ import annotations

import numpy as np
from manim import (
    DOWN, FadeIn, FadeOut, GREEN_C, GREY_B, LEFT, MathTex, Matrix, ORANGE,
    RIGHT, Scene, SurroundingRectangle, TEAL_C, Tex, Text, UP, VGroup,
    WHITE, YELLOW,
)

from engine.minimum_principle import MinimumPrinciple


class MinimumPrinciplePresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "The Minimum Principle"

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
            r"\textbf{The Minimum Principle}", font_size=34, color=YELLOW
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
    def _compact_entries(matrix, factor=0.78):
        entries = list(matrix.get_entries())
        centers = [entry.get_center().copy() for entry in entries]
        for entry, center in zip(entries, centers):
            entry.scale(factor).move_to(center)
        return entries

    @staticmethod
    def _minimum_card(label, constraint, value, color):
        content = VGroup(
            Text(label, font_size=26, color=color, weight="BOLD"),
            MathTex(constraint, font_size=33, color=WHITE),
            MathTex(value, font_size=38, color=color),
        ).arrange(DOWN, buff=0.18)
        border = SurroundingRectangle(content, color=color, buff=0.24, stroke_width=2.2)
        return VGroup(border, content)

    def construct(self):
        model = MinimumPrinciple()
        eigenvalues, eigenvectors = model.ordered_eigenpairs()
        if not np.allclose(eigenvalues, [1, 3, 4]):
            raise RuntimeError("unexpected eigenvalues for the minimum-principle example")
        if not np.allclose(model.eigenvalue_bounds(), [1, 4]):
            raise RuntimeError("unexpected Rayleigh-quotient bounds")
        for index, expected in enumerate(eigenvalues):
            minimum, direction = model.constrained_minimum(index)
            if not np.isclose(minimum, expected):
                raise RuntimeError("successive constrained minimum failed")
            if not np.allclose(direction, eigenvectors[:, index]):
                raise RuntimeError("unexpected minimizing direction")

        banner, title, heading = self._chrome(
            "Can minimization recover the eigenvalues of a symmetric matrix?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        a_matrix = self._matrix(
            [["2", "1", "0"], ["1", "2", "0"], ["0", "0", "4"]],
            scale=0.78,
        )
        opening = VGroup(
            VGroup(MathTex("A=", font_size=42), a_matrix).arrange(RIGHT, buff=0.16),
            VGroup(
                Text("Goal", font_size=29, color=YELLOW, weight="BOLD"),
                MathTex(r"\lambda_1,\lambda_2,\lambda_3", font_size=47),
                Text("from minimum energy", font_size=28, color=GREEN_C),
            ).arrange(DOWN, buff=0.30),
        ).arrange(RIGHT, buff=1.30).move_to(DOWN * 0.04)
        opening_note = Text(
            "A is symmetric and positive definite.", font_size=29, color=TEAL_C
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]), FadeIn(opening_note))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Normalize quadratic energy by the squared length of the vector."
        )
        self.play(FadeOut(opening), FadeOut(opening_note))
        quotient = VGroup(
            Text("Rayleigh quotient", font_size=31, color=YELLOW, weight="BOLD"),
            MathTex(
                r"R_A(x)=\frac{x^TAx}{x^Tx},\qquad x\ne0",
                font_size=52,
                color=WHITE,
            ),
            VGroup(
                MathTex(r"x^TAx", font_size=37, color=ORANGE),
                Text("quadratic energy", font_size=26, color=ORANGE),
                MathTex(r"x^Tx=\lVert x\rVert^2", font_size=37, color=TEAL_C),
                Text("squared length", font_size=26, color=TEAL_C),
            ).arrange(RIGHT, buff=0.42),
        ).arrange(DOWN, buff=0.44).move_to(DOWN * 0.05)
        self.play(FadeIn(quotient[0]), FadeIn(quotient[1]))
        self.play(FadeIn(quotient[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Scaling changes energy and length by the same factor."
        )
        self.play(FadeOut(quotient))
        scaling = VGroup(
            MathTex(
                r"R_A(cx)=\frac{(cx)^TA(cx)}{(cx)^T(cx)}",
                font_size=48,
                color=WHITE,
            ),
            MathTex(
                r"=\frac{c^2x^TAx}{c^2x^Tx}=R_A(x)",
                font_size=48,
                color=YELLOW,
            ),
            Text(
                "The Rayleigh quotient measures a direction, not its length.",
                font_size=30,
                color=GREEN_C,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.06)
        self.play(FadeIn(scaling[0]))
        self.play(FadeIn(scaling[1]))
        self.play(FadeIn(scaling[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "This matrix has three orthonormal eigen-directions."
        )
        self.play(FadeOut(scaling))
        v_one = self._matrix([["1"], ["-1"], ["0"]], scale=0.56)
        v_two = self._matrix([["1"], ["1"], ["0"]], scale=0.56)
        v_three = self._matrix([["0"], ["0"], ["1"]], scale=0.56)
        eigenpairs = VGroup(
            VGroup(
                MathTex(r"\lambda_1=1", font_size=34, color=TEAL_C),
                VGroup(MathTex(r"v_1=\frac1{\sqrt2}", font_size=31), v_one).arrange(RIGHT, buff=0.10),
            ).arrange(DOWN, buff=0.18),
            VGroup(
                MathTex(r"\lambda_2=3", font_size=34, color=ORANGE),
                VGroup(MathTex(r"v_2=\frac1{\sqrt2}", font_size=31), v_two).arrange(RIGHT, buff=0.10),
            ).arrange(DOWN, buff=0.18),
            VGroup(
                MathTex(r"\lambda_3=4", font_size=34, color=YELLOW),
                VGroup(MathTex(r"v_3=", font_size=31), v_three).arrange(RIGHT, buff=0.10),
            ).arrange(DOWN, buff=0.18),
        ).arrange(RIGHT, buff=0.52).move_to(DOWN * 0.08)
        eigen_note = MathTex(
            r"v_i^Tv_j=0\ (i\ne j),\qquad \lVert v_i\rVert=1",
            font_size=34,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(eigenpairs[0]), FadeIn(eigenpairs[1]))
        self.play(FadeIn(eigenpairs[2]), FadeIn(eigen_note))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Express an arbitrary direction in the eigenvector basis."
        )
        self.play(FadeOut(eigenpairs), FadeOut(eigen_note))
        coordinates = VGroup(
            MathTex(
                r"x=c_1v_1+c_2v_2+c_3v_3",
                font_size=50,
                color=WHITE,
            ),
            MathTex(
                r"x^Tx=c_1^2+c_2^2+c_3^2",
                font_size=45,
                color=TEAL_C,
            ),
            MathTex(
                r"x^TAx=c_1^2+3c_2^2+4c_3^2",
                font_size=45,
                color=ORANGE,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.06)
        self.play(FadeIn(coordinates[0]))
        self.play(FadeIn(coordinates[1]))
        self.play(FadeIn(coordinates[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The quotient is a weighted average of the eigenvalues."
        )
        self.play(FadeOut(coordinates))
        spectral_formula = VGroup(
            MathTex(
                r"R_A(x)=\frac{c_1^2+3c_2^2+4c_3^2}"
                r"{c_1^2+c_2^2+c_3^2}",
                font_size=49,
                color=WHITE,
            ),
            MathTex(
                r"=1w_1+3w_2+4w_3,\qquad "
                r"w_i=\frac{c_i^2}{c_1^2+c_2^2+c_3^2}",
                font_size=41,
                color=YELLOW,
            ),
            MathTex(
                r"w_i\ge0,\qquad w_1+w_2+w_3=1",
                font_size=39,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.46).move_to(DOWN * 0.06)
        self.play(FadeIn(spectral_formula[0]))
        self.play(FadeIn(spectral_formula[1]))
        self.play(FadeIn(spectral_formula[2]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "A weighted average cannot fall below 1 or rise above 4."
        )
        self.play(FadeOut(spectral_formula))
        bounds = VGroup(
            MathTex(r"\boxed{1\le R_A(x)\le4}", font_size=56, color=YELLOW),
            VGroup(
                MathTex(r"R_A(v_1)=1", font_size=40, color=TEAL_C),
                MathTex(r"R_A(v_2)=3", font_size=40, color=ORANGE),
                MathTex(r"R_A(v_3)=4", font_size=40, color=YELLOW),
            ).arrange(RIGHT, buff=0.66),
            Text(
                "The smallest possible directional energy occurs along v₁.",
                font_size=29,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.06)
        self.play(FadeIn(bounds[0]))
        self.play(FadeIn(bounds[1]))
        self.play(FadeIn(bounds[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The first eigenvalue is the unrestricted minimum."
        )
        self.play(FadeOut(bounds))
        first_minimum = VGroup(
            MathTex(
                r"\boxed{\lambda_1=\min_{x\ne0}R_A(x)=1}",
                font_size=54,
                color=TEAL_C,
            ),
            MathTex(r"\text{minimum attained when }x\parallel v_1", font_size=40),
        ).arrange(DOWN, buff=0.62).move_to(DOWN * 0.02)
        self.play(FadeIn(first_minimum[0]))
        self.play(FadeIn(first_minimum[1]))
        self.wait(1.8)

        prediction = Text(
            "Pause: what happens if the lowest-energy direction is excluded?",
            font_size=30,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "Require x to be perpendicular to the first eigenvector."
        )
        self.play(FadeOut(first_minimum))
        second_minimum = VGroup(
            MathTex(r"x\perp v_1\quad\Longrightarrow\quad c_1=0", font_size=46, color=YELLOW),
            MathTex(
                r"R_A(x)=\frac{3c_2^2+4c_3^2}{c_2^2+c_3^2}\ge3",
                font_size=48,
                color=WHITE,
            ),
            MathTex(
                r"\boxed{\lambda_2=\min_{\substack{x\ne0\\x\perp v_1}}R_A(x)=3}",
                font_size=47,
                color=ORANGE,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.06)
        self.play(FadeIn(second_minimum[0]))
        self.play(FadeIn(second_minimum[1]))
        self.play(FadeIn(second_minimum[2]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Exclude the first two eigen-directions to reveal the third."
        )
        self.play(FadeOut(second_minimum))
        third_minimum = VGroup(
            MathTex(
                r"x\perp v_1,v_2\quad\Longrightarrow\quad x=c_3v_3",
                font_size=46,
                color=YELLOW,
            ),
            MathTex(r"R_A(x)=4", font_size=50, color=WHITE),
            MathTex(
                r"\boxed{\lambda_3="
                r"\min_{\substack{x\ne0\\x\perp v_1,v_2}}R_A(x)=4}",
                font_size=47,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.05)
        self.play(FadeIn(third_minimum[0]))
        self.play(FadeIn(third_minimum[1]))
        self.play(FadeIn(third_minimum[2]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Minimize, exclude the directions already found, and repeat."
        )
        self.play(FadeOut(third_minimum))
        cards = VGroup(
            self._minimum_card("FIRST", r"x\ne0", r"\min R_A=\lambda_1", TEAL_C),
            self._minimum_card("SECOND", r"x\perp v_1", r"\min R_A=\lambda_2", ORANGE),
            self._minimum_card("THIRD", r"x\perp v_1,v_2", r"\min R_A=\lambda_3", YELLOW),
        ).arrange(RIGHT, buff=0.34).move_to(DOWN * 0.04)
        if cards.width > 11.3:
            cards.scale_to_fit_width(11.3)
        self.play(FadeIn(cards[0]))
        self.play(FadeIn(cards[1]))
        self.play(FadeIn(cards[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The successive minimum principle recovers every eigenvalue."
        )
        self.play(FadeOut(cards))
        principle = VGroup(
            Text("SUCCESSIVE MINIMUM PRINCIPLE", font_size=28, color=YELLOW, weight="BOLD"),
            MathTex(
                r"\boxed{\lambda_k="
                r"\min_{\substack{x\ne0\\x\perp v_1,\ldots,v_{k-1}}}"
                r"\frac{x^TAx}{x^Tx}}",
                font_size=48,
                color=WHITE,
            ),
            Text(
                "Each constraint removes the lower-energy directions.",
                font_size=30,
                color=GREEN_C,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.05)
        if principle.width > 11.2:
            principle.scale_to_fit_width(11.2)
        self.play(FadeIn(principle[0]))
        self.play(FadeIn(principle[1]))
        self.play(FadeIn(principle[2]))
        self.wait(2.8)
