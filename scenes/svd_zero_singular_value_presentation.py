"""Manim presentation: What Does a Zero Singular Value Mean?"""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Circle,
    Create,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    LEFT,
    MathTex,
    Matrix,
    NumberPlane,
    ORANGE,
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

from engine.svd_zero_singular_value import ZeroSingularValueModel


class ZeroSingularValuePresentation(Scene):
    CHAPTER_BANNER = "SINGULAR VALUES, RANK, AND APPROXIMATION"
    LESSON_TITLE = "What Does a Zero Singular Value Mean?"

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
            r"\textbf{What Does a Zero Singular Value Mean?}",
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
        body = VGroup(
            Text(label, font_size=25, color=color, weight="BOLD"),
            MathTex(formula, font_size=35, color=WHITE),
        ).arrange(DOWN, buff=0.20)
        border = SurroundingRectangle(body, color=color, buff=0.18, stroke_width=2.1)
        return VGroup(border, body)

    @staticmethod
    def _plane():
        return NumberPlane(
            x_range=[-2.4, 2.4, 1],
            y_range=[-2.4, 2.4, 1],
            x_length=4.25,
            y_length=3.45,
            background_line_style={"stroke_opacity": 0.26, "stroke_width": 1.1},
            axis_config={"stroke_opacity": 0.75},
        )

    def construct(self):
        model = ZeroSingularValueModel()
        root_two = np.sqrt(2.0)
        if not np.allclose(model.singular_values(), [2, 0]):
            raise RuntimeError("unexpected singular values")
        if not np.allclose(model.apply([1 / root_two, -1 / root_two]), [0, 0]):
            raise RuntimeError("expected null direction was not lost")
        if not np.allclose(model.reduced_reconstruction(), model.matrix):
            raise RuntimeError("reduced SVD reconstruction failed")

        banner, title, heading = self._chrome(
            "What changes when a matrix completely erases one input direction?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        a_matrix = self._matrix([["1", "1"], ["1", "1"]], scale=0.82)
        opening = VGroup(
            VGroup(MathTex("A=", font_size=43), a_matrix).arrange(RIGHT, buff=0.14),
            Text("maps the plane into a line", font_size=31, color=TEAL_C),
        ).arrange(RIGHT, buff=1.15).move_to(DOWN * 0.05)
        question = Text(
            "Which input direction disappears?",
            font_size=30,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(opening))
        self.play(FadeIn(question))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Watch the unit circle collapse onto a line segment."
        )
        self.play(FadeOut(opening), FadeOut(question))
        input_plane = self._plane().shift(LEFT * 3.15 + DOWN * 0.12)
        output_plane = self._plane().shift(RIGHT * 3.15 + DOWN * 0.12)
        input_label = Text("INPUT", font_size=23, color=TEAL_C, weight="BOLD").next_to(
            input_plane, UP, buff=0.10
        )
        output_label = Text("OUTPUT", font_size=23, color=GREEN_C, weight="BOLD").next_to(
            output_plane, UP, buff=0.10
        )
        circle = Circle(radius=input_plane.x_axis.get_unit_size(), color=TEAL_C, stroke_width=2.4)
        circle.move_to(input_plane.c2p(0, 0))
        source = model.circle_samples(32)
        mapped = model.mapped_circle_samples(32)
        source_dots = VGroup(
            *[Dot(input_plane.c2p(*point), radius=0.035, color=TEAL_C) for point in source]
        )
        moving_dots = source_dots.copy().set_color(GREEN_C)
        transform_arrow = MathTex(r"\xrightarrow{\ A\ }", font_size=40, color=YELLOW)
        transform_arrow.move_to(DOWN * 0.12)
        self.play(FadeIn(input_plane), FadeIn(output_plane), FadeIn(input_label), FadeIn(output_label))
        self.play(Create(circle), FadeIn(source_dots), FadeIn(moving_dots))
        self.play(FadeIn(transform_arrow))
        self.play(
            *[
                dot.animate.move_to(output_plane.c2p(*point))
                for dot, point in zip(moving_dots, mapped, strict=True)
            ],
            source_dots.animate.set_opacity(0.28),
            run_time=2.4,
        )
        self.wait(1.6)

        heading = self._replace_heading(
            heading, "One direction survives; an orthogonal nonzero direction becomes zero."
        )
        v_one = np.array([1 / root_two, 1 / root_two])
        v_two = np.array([1 / root_two, -1 / root_two])
        u_one = np.array([1 / root_two, 1 / root_two])
        active_input = Arrow(
            input_plane.c2p(0, 0), input_plane.c2p(*v_one), buff=0, color=TEAL_C
        )
        null_input = Arrow(
            input_plane.c2p(0, 0), input_plane.c2p(*v_two), buff=0, color=ORANGE
        )
        active_output = Arrow(
            output_plane.c2p(0, 0), output_plane.c2p(*(2 * u_one)), buff=0, color=GREEN_C
        )
        lost_output = Dot(output_plane.c2p(0, 0), radius=0.11, color=RED_C)
        active_label = MathTex(r"Av_1=2u_1", font_size=31, color=GREEN_C).next_to(
            output_plane, DOWN, buff=0.15
        )
        null_label = MathTex(r"Av_2=0", font_size=34, color=ORANGE).next_to(
            active_label, DOWN, buff=0.12
        )
        self.play(Create(active_input), Create(active_output), FadeIn(active_label))
        self.play(Create(null_input), FadeIn(lost_output), FadeIn(null_label))
        self.wait(2.0)

        prediction = Text(
            "Pause: where is the lost direction recorded in the SVD?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.28)
        self.play(FadeOut(active_label), FadeOut(null_label), FadeIn(prediction))
        self.wait(2.8)

        heading = self._replace_heading(
            heading, "The Gram matrix records one positive direction and one zero direction."
        )
        geometry = VGroup(
            input_plane, output_plane, input_label, output_label, circle, source_dots,
            moving_dots, transform_arrow, active_input, null_input, active_output, lost_output,
        )
        self.play(FadeOut(geometry), FadeOut(prediction))
        gram = self._matrix([["2", "2"], ["2", "2"]], scale=0.84)
        gram_line = VGroup(
            VGroup(MathTex(r"A^TA=", font_size=43), gram).arrange(RIGHT, buff=0.14),
            MathTex(r"\Longrightarrow", font_size=44, color=YELLOW),
            VGroup(
                MathTex(r"\lambda_1=4", font_size=40, color=TEAL_C),
                MathTex(r"\lambda_2=0", font_size=40, color=ORANGE),
            ).arrange(DOWN, buff=0.28),
        ).arrange(RIGHT, buff=0.72).move_to(DOWN * 0.02)
        self.play(FadeIn(gram_line[0]))
        self.play(FadeIn(gram_line[1]), FadeIn(gram_line[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Singular values are the nonnegative square roots of those eigenvalues."
        )
        self.play(FadeOut(gram_line))
        sigma = self._matrix([["2", "0"], ["0", "0"]], scale=0.88)
        singular_values = VGroup(
            MathTex(r"\sigma_i=\sqrt{\lambda_i(A^TA)}", font_size=45, color=WHITE),
            VGroup(
                MathTex(r"\sigma_1=2", font_size=42, color=TEAL_C),
                MathTex(r"\sigma_2=0", font_size=42, color=ORANGE),
            ).arrange(RIGHT, buff=1.20),
            VGroup(MathTex(r"\Sigma=", font_size=43), sigma).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.08)
        self.play(FadeIn(singular_values[0]))
        self.play(FadeIn(singular_values[1]))
        self.play(FadeIn(singular_values[2]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "A zero singular value identifies a nonzero vector in the null space."
        )
        self.play(FadeOut(singular_values))
        null_connection = VGroup(
            MathTex(r"\sigma_2=0", font_size=45, color=ORANGE),
            MathTex(r"\Longleftrightarrow", font_size=44, color=YELLOW),
            MathTex(r"Av_2=0", font_size=45, color=ORANGE),
            MathTex(r"\Longleftrightarrow", font_size=44, color=YELLOW),
            MathTex(r"v_2\in\mathcal N(A)", font_size=45, color=WHITE),
        ).arrange(RIGHT, buff=0.30).move_to(DOWN * 0.02)
        null_basis = MathTex(
            r"\mathcal N(A)=\operatorname{span}\{v_2\}",
            font_size=41,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(null_connection))
        self.play(FadeIn(null_basis))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Positive singular values count the independent output directions."
        )
        self.play(FadeOut(null_connection), FadeOut(null_basis))
        rank_cards = VGroup(
            self._card("SURVIVING DIRECTION", r"Av_1=2u_1", TEAL_C),
            self._card("LOST DIRECTION", r"Av_2=0", ORANGE),
            self._card("RANK", r"\operatorname{rank}(A)=1", GREEN_C),
        ).arrange(RIGHT, buff=0.42).move_to(DOWN * 0.02)
        rank_count = MathTex(
            r"\operatorname{rank}(A)=\#\{\sigma_i>0\}",
            font_size=43,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(rank_cards[0]), FadeIn(rank_cards[1]))
        self.play(FadeIn(rank_cards[2]), FadeIn(rank_count))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Only the surviving singular direction contributes to the matrix."
        )
        self.play(FadeOut(rank_cards), FadeOut(rank_count))
        reduced = VGroup(
            Text("reduced rank-one SVD", font_size=29, color=GREY_B),
            MathTex(r"A=2u_1v_1^T", font_size=55, color=YELLOW),
            Text(
                "The zero singular component contributes nothing.",
                font_size=30,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.04)
        self.play(FadeIn(reduced[0]))
        self.play(FadeIn(reduced[1]))
        self.play(FadeIn(reduced[2]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "A zero singular value means that the matrix loses a direction."
        )
        self.play(FadeOut(reduced))
        conclusion = VGroup(
            MathTex(r"\boxed{\sigma_i=0\ \Longleftrightarrow\ Av_i=0}", font_size=50, color=YELLOW),
            MathTex(
                r"\boxed{\operatorname{rank}(A)=\#\{\text{positive singular values}\}}",
                font_size=46,
                color=WHITE,
            ),
            Text(
                "Positive directions carry information; zero directions are lost.",
                font_size=29,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.06)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.wait(3.0)
