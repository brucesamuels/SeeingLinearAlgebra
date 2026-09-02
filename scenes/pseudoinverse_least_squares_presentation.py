"""Manim presentation: Least Squares and Minimum-Norm Solutions."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    MathTex,
    Matrix,
    ORANGE,
    PURPLE,
    RED_C,
    RIGHT,
    Scene,
    SurroundingRectangle,
    TEAL_C,
    Tex,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.pseudoinverse_least_squares import PseudoinverseLeastSquares


class PseudoinverseLeastSquaresPresentation(Scene):
    CHAPTER_BANNER = "SINGULAR VALUES, RANK, AND APPROXIMATION"
    LESSON_TITLE = "Least Squares and Minimum-Norm Solutions"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Tex(
            r"\textbf{SINGULAR VALUES, RANK, AND APPROXIMATION}",
            font_size=23,
            color=GREY_B,
        ).to_edge(UP, buff=0.16)
        title = Tex(
            r"\textbf{Least Squares and Minimum-Norm Solutions}",
            font_size=33,
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
    def _column(entries, scale=0.72, v_buff=0.80):
        return Matrix([[entry] for entry in entries], h_buff=0.75, v_buff=v_buff).scale(scale)

    @staticmethod
    def _align_entries_with_fraction_bars(matrix, indices, offset=0.15):
        entries = list(matrix.get_entries())
        for index in indices:
            entries[index].shift(UP * offset)

    @staticmethod
    def _card(label, formula, note, color):
        body = VGroup(
            Text(label, font_size=24, color=color, weight="BOLD"),
            MathTex(formula, font_size=37, color=WHITE),
            Text(note, font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.18)
        border = SurroundingRectangle(body, color=color, buff=0.18, stroke_width=2.1)
        return VGroup(border, body)

    def construct(self):
        model = PseudoinverseLeastSquares()
        if not np.allclose(model.closest_output(), [2, 2, 0]):
            raise RuntimeError("unexpected closest output")
        if not np.allclose(model.solution(), [1, 1]):
            raise RuntimeError("unexpected pseudoinverse solution")
        if not np.allclose(model.normal_equation_residual(), [0, 0]):
            raise RuntimeError("residual is not orthogonal to the image")

        banner, title, heading = self._chrome(
            "The target lies outside the image, so it has no pre-image."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        a_matrix = self._matrix([["1", "1"], ["1", "1"], ["0", "0"]], scale=0.68)
        b_column = self._column(["3", "1", "2"], scale=0.68)
        opening = VGroup(
            VGroup(MathTex(r"A=", font_size=41), a_matrix).arrange(RIGHT, buff=0.14),
            VGroup(
                MathTex(r"A(x_1,x_2)=(s,s,0),\quad s=x_1+x_2", font_size=37, color=TEAL_C),
                VGroup(MathTex(r"\mathbf b=", font_size=40), b_column).arrange(RIGHT, buff=0.12),
                MathTex(r"\mathbf b\notin\mathcal R(A)", font_size=38, color=RED_C),
            ).arrange(DOWN, buff=0.28),
        ).arrange(RIGHT, buff=0.92).move_to(DOWN * 0.03)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The component equations make the inconsistency explicit."
        )
        self.play(FadeOut(opening))
        contradiction = VGroup(
            MathTex(r"x_1+x_2=3", font_size=45, color=TEAL_C),
            MathTex(r"x_1+x_2=1", font_size=45, color=ORANGE),
            MathTex(r"0=2", font_size=45, color=RED_C),
            Text("No input maps exactly to b.", font_size=29, color=RED_C, weight="BOLD"),
        ).arrange(DOWN, buff=0.34).move_to(DOWN * 0.02)
        self.play(FadeIn(contradiction[:3]))
        self.play(FadeIn(contradiction[3]))
        self.wait(2.1)

        heading = self._replace_heading(
            heading, "The pseudoinverse answers two different questions in sequence."
        )
        self.play(FadeOut(contradiction))
        questions = VGroup(
            self._card(
                "1  CLOSEST REACHABLE OUTPUT",
                r"\widehat{\mathbf b}=AA^+\mathbf b",
                "project b onto the image",
                TEAL_C,
            ),
            self._card(
                "2  SELECTED PRE-IMAGE",
                r"\widehat{\mathbf x}=A^+\mathbf b",
                "return to the row space",
                GREEN_C,
            ),
        ).arrange(RIGHT, buff=0.68).move_to(DOWN * 0.04)
        pipeline = MathTex(
            r"\mathbf b\ \longmapsto\ \widehat{\mathbf b}\ \longmapsto\ \widehat{\mathbf x}",
            font_size=40,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.58)
        self.play(FadeIn(questions[0]))
        self.play(FadeIn(questions[1]), FadeIn(pipeline))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "First project the target onto the image of A."
        )
        self.play(FadeOut(questions), FadeOut(pipeline))
        image_projector = self._matrix(
            [
                [r"\frac12", r"\frac12", "0"],
                [r"\frac12", r"\frac12", "0"],
                ["0", "0", "0"],
            ],
            scale=0.63,
            h_buff=1.10,
            v_buff=1.23,
        )
        self._align_entries_with_fraction_bars(image_projector, (2, 5), offset=0.14)
        target_column = self._column(["3", "1", "2"], scale=0.63)
        projected_column = self._column(["2", "2", "0"], scale=0.63)
        projection_calculation = VGroup(
            MathTex(r"\widehat{\mathbf b}=AA^+\mathbf b=", font_size=38, color=TEAL_C),
            image_projector,
            target_column,
            MathTex(r"=", font_size=39),
            projected_column,
        ).arrange(RIGHT, buff=0.16).move_to(DOWN * 0.01)
        projection_note = MathTex(
            r"\widehat{\mathbf b}=(2,2,0)\in\mathcal R(A)",
            font_size=37,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.58)
        self.play(FadeIn(projection_calculation))
        self.play(FadeIn(projection_note))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The remaining residual is orthogonal to every reachable output."
        )
        self.play(FadeOut(projection_calculation), FadeOut(projection_note))
        residual_card = VGroup(
            MathTex(
                r"\mathbf r=\mathbf b-\widehat{\mathbf b}=(1,-1,2)",
                font_size=43,
                color=ORANGE,
            ),
            MathTex(
                r"(1,-1,2)\cdot(1,1,0)=0",
                font_size=41,
                color=WHITE,
            ),
            MathTex(r"A^T\mathbf r=0", font_size=43, color=GREEN_C),
            Text("No reachable output is closer to b.", font_size=28, color=YELLOW, weight="BOLD"),
        ).arrange(DOWN, buff=0.34).move_to(DOWN * 0.02)
        self.play(FadeIn(residual_card[0]))
        self.play(FadeIn(residual_card[1]), FadeIn(residual_card[2]))
        self.play(FadeIn(residual_card[3]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Then A-plus returns the row-space pre-image of that projection."
        )
        self.play(FadeOut(residual_card))
        a_plus = self._matrix(
            [[r"\frac14", r"\frac14", "0"], [r"\frac14", r"\frac14", "0"]],
            scale=0.69,
            h_buff=1.18,
            v_buff=1.38,
        )
        self._align_entries_with_fraction_bars(a_plus, (2, 5), offset=0.14)
        target_column = self._column(["3", "1", "2"], scale=0.63)
        solution_column = self._column(["1", "1"], scale=0.68, v_buff=0.88)
        solution_calculation = VGroup(
            MathTex(r"\widehat{\mathbf x}=A^+\mathbf b=", font_size=39, color=GREEN_C),
            a_plus,
            target_column,
            MathTex(r"=", font_size=39),
            solution_column,
        ).arrange(RIGHT, buff=0.16).move_to(DOWN * 0.01)
        verification = MathTex(
            r"A\widehat{\mathbf x}=(2,2,0)=\widehat{\mathbf b}",
            font_size=38,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.58)
        self.play(FadeIn(solution_calculation))
        self.play(FadeIn(verification))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The projected output still has infinitely many pre-images."
        )
        self.play(FadeOut(solution_calculation), FadeOut(verification))
        family = VGroup(
            MathTex(
                r"\mathbf x_t=(1,1)+t(1,-1)=(1+t,1-t)",
                font_size=43,
                color=TEAL_C,
            ),
            MathTex(
                r"A\mathbf x_t=(2,2,0)=\widehat{\mathbf b}\qquad\text{for every }t",
                font_size=41,
                color=GREEN_C,
            ),
            Text(
                "Null-space motion changes the pre-image but not its image.",
                font_size=28,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.03)
        self.play(FadeIn(family[0]))
        self.play(FadeIn(family[1]))
        self.play(FadeIn(family[2]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Among those pre-images, the row-space choice has minimum norm."
        )
        self.play(FadeOut(family))
        norm_argument = VGroup(
            MathTex(
                r"\|\mathbf x_t\|^2=(1+t)^2+(1-t)^2",
                font_size=43,
                color=WHITE,
            ),
            MathTex(r"=2+2t^2\ge 2", font_size=47, color=YELLOW),
            MathTex(
                r"t=0\quad\Longrightarrow\quad\widehat{\mathbf x}=(1,1)",
                font_size=42,
                color=GREEN_C,
            ),
            Text("Equality occurs only at the pseudoinverse solution.", font_size=28, color=TEAL_C),
        ).arrange(DOWN, buff=0.36).move_to(DOWN * 0.02)
        self.play(FadeIn(norm_argument[0]))
        self.play(FadeIn(norm_argument[1]))
        self.play(FadeIn(norm_argument[2]), FadeIn(norm_argument[3]))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "On the row space and image, A is one-to-one and onto."
        )
        self.play(FadeOut(norm_argument))
        restricted_inverse = VGroup(
            MathTex(
                r"A:\mathcal R(A^T)\ \xrightarrow[\text{onto}]{\text{one-to-one}}\ \mathcal R(A)",
                font_size=43,
                color=TEAL_C,
            ),
            MathTex(
                r"A^+:\mathcal R(A)\longrightarrow\mathcal R(A^T)",
                font_size=43,
                color=GREEN_C,
            ),
            Text("Between these subspaces, the two functions are genuine inverses.", font_size=28),
            MathTex(
                r"\mathbf b\ \xrightarrow{\ AA^+\ }\ \widehat{\mathbf b}\ \xrightarrow{\ A^+\ }\ \widehat{\mathbf x}",
                font_size=39,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.02)
        self.play(FadeIn(restricted_inverse[0]))
        self.play(FadeIn(restricted_inverse[1]), FadeIn(restricted_inverse[2]))
        self.play(FadeIn(restricted_inverse[3]))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "A-plus chooses the best achievable fit and the shortest pre-image."
        )
        self.play(FadeOut(restricted_inverse))
        conclusion = VGroup(
            MathTex(r"\boxed{\widehat{\mathbf x}=A^+\mathbf b}", font_size=54, color=YELLOW),
            VGroup(
                self._card(
                    "LEAST SQUARES",
                    r"A\widehat{\mathbf x}=P_{\mathcal R(A)}\mathbf b",
                    "closest reachable output",
                    TEAL_C,
                ),
                self._card(
                    "MINIMUM NORM",
                    r"\widehat{\mathbf x}\perp\mathcal N(A)",
                    "shortest pre-image",
                    GREEN_C,
                ),
            ).arrange(RIGHT, buff=0.64),
            Text(
                "Project to the image. Return through the row space.",
                font_size=29,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.40).move_to(DOWN * 0.04)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.wait(3.0)
