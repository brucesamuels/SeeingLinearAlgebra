"""Manim presentation: Positive Definite Matrices — The Eigenvalue Test."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, RED_C, TEAL_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Circle, Create, DecimalNumber, FadeIn, FadeOut, MathTex, Matrix,
    NumberPlane, Rectangle, ReplacementTransform, Scene, Text, ValueTracker,
    VGroup, always_redraw, smooth,
)

from engine.positive_definite_eigenvalue_test import PositiveDefiniteEigenvalueTest


class PositiveDefiniteEigenvalueTestPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "The Eigenvalue Test"

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
    def _box(label, formula, color):
        content = VGroup(
            Text(label, font_size=25, color=color, weight="BOLD"),
            MathTex(formula, font_size=37, color=WHITE),
        ).arrange(DOWN, buff=0.20)
        border = Rectangle(
            width=content.width + 0.42,
            height=content.height + 0.36,
            color=color,
            stroke_width=2.4,
        ).move_to(content)
        return VGroup(border, content)

    def construct(self):
        model = PositiveDefiniteEigenvalueTest()
        banner, title, heading = self._chrome(
            "The unit circle contains two directions where the energy stops changing."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        matrix_card = VGroup(
            MathTex("A=", font_size=44),
            self._matrix([["2", "1"], ["1", "2"]]),
        ).arrange(RIGHT, buff=0.14)
        question = VGroup(
            MathTex(r"q(x)=x^T A x", font_size=52, color=YELLOW),
            Text(
                "Which unit directions give the smallest and largest values?",
                font_size=30,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.32)
        opening = VGroup(matrix_card, question).arrange(RIGHT, buff=0.86)
        opening.move_to(DOWN * 0.28)
        if opening.width > 11.3:
            opening.scale_to_fit_width(11.3)
        self.play(FadeIn(matrix_card), FadeIn(question))
        self.wait(1.5)

        heading = self._replace_heading(
            heading, "Sweep the unit vector and watch for the extreme energies."
        )
        self.play(FadeOut(opening))
        plane = NumberPlane(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5.0,
            y_length=5.0,
            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.24},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.4},
        ).move_to(LEFT * 3.0 + DOWN * 0.53)
        origin = plane.c2p(0, 0)
        unit_radius = np.linalg.norm(plane.c2p(1, 0) - origin)
        unit_circle = Circle(
            radius=unit_radius, color=GREY_B, stroke_width=2.4
        ).move_to(origin)
        theta = ValueTracker(0.0)
        direction_arrow = always_redraw(
            lambda: Arrow(
                origin,
                plane.c2p(*model.direction(theta.get_value())),
                buff=0,
                color=ORANGE,
                stroke_width=8,
                max_tip_length_to_length_ratio=0.16,
            )
        )
        x_label = always_redraw(
            lambda: MathTex(r"x(\theta)", font_size=32, color=ORANGE).next_to(
                plane.c2p(*model.direction(theta.get_value())), UP, buff=0.10
            )
        )
        energy_panel = always_redraw(
            lambda: VGroup(
                MathTex(r"x^T A x=", font_size=47, color=YELLOW),
                DecimalNumber(
                    model.directional_energy(theta.get_value()),
                    num_decimal_places=2,
                    font_size=47,
                    color=GREEN_C,
                ),
            ).arrange(RIGHT, buff=0.16).move_to(RIGHT * 3.42 + UP * 0.24)
        )
        range_hint = MathTex(
            r"\text{smallest?}\qquad\text{largest?}",
            font_size=35,
            color=WHITE,
        ).move_to(RIGHT * 3.42 + DOWN * 0.70)
        self.play(Create(plane), Create(unit_circle))
        self.add(direction_arrow, x_label, energy_panel)
        self.play(FadeIn(range_hint))
        for target in (np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi, 7 * np.pi / 4):
            self.play(theta.animate.set_value(target), run_time=1.15, rate_func=smooth)
            self.wait(0.20)

        prediction = Text(
            "Pause: which two lines through the origin are special?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.22)
        self.play(FadeIn(prediction))
        self.wait(2.5)
        self.play(FadeOut(prediction), FadeOut(range_hint))

        heading = self._replace_heading(
            heading, "The two diagonal directions give the extreme unit energies."
        )
        self.remove(direction_arrow, x_label, energy_panel)
        up_direction = model.direction(np.pi / 4)
        down_direction = model.direction(-np.pi / 4)
        up_arrow = Arrow(
            origin, plane.c2p(*up_direction), buff=0, color=GREEN_C, stroke_width=8
        )
        down_arrow = Arrow(
            origin, plane.c2p(*down_direction), buff=0, color=TEAL_C, stroke_width=8
        )
        up_label = MathTex(r"u_+", font_size=35, color=GREEN_C).next_to(
            up_arrow.get_end(), UP, buff=0.10
        )
        down_label = MathTex(r"u_-", font_size=35, color=TEAL_C).next_to(
            down_arrow.get_end(), DOWN, buff=0.10
        )
        extreme_values = VGroup(
            MathTex(r"q(u_+)=3", font_size=48, color=GREEN_C),
            MathTex(r"q(u_-)=1", font_size=48, color=TEAL_C),
            MathTex(
                r"\boxed{1\le x^T A x\le3\quad\text{when }\lVert x\rVert=1}",
                font_size=38,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.38).move_to(RIGHT * 3.38 + DOWN * 0.20)
        self.play(FadeIn(up_arrow), FadeIn(up_label), FadeIn(extreme_values[0]))
        self.play(FadeIn(down_arrow), FadeIn(down_label), FadeIn(extreme_values[1]))
        self.play(FadeIn(extreme_values[2]))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "These special directions are eigenvector directions."
        )
        self.play(
            FadeOut(plane), FadeOut(unit_circle), FadeOut(up_arrow), FadeOut(down_arrow),
            FadeOut(up_label), FadeOut(down_label), FadeOut(extreme_values),
        )
        plus_vector = VGroup(
            MathTex(r"u_+=\frac1{\sqrt2}", font_size=39, color=GREEN_C),
            self._matrix([["1"], ["1"]], scale=0.67),
            MathTex(r",\qquad Au_+=3u_+", font_size=42, color=GREEN_C),
        ).arrange(RIGHT, buff=0.12)
        minus_vector = VGroup(
            MathTex(r"u_-=\frac1{\sqrt2}", font_size=39, color=TEAL_C),
            self._matrix([["1"], ["-1"]], scale=0.67),
            MathTex(r",\qquad Au_-=1u_-", font_size=42, color=TEAL_C),
        ).arrange(RIGHT, buff=0.12)
        eigenpairs = VGroup(plus_vector, minus_vector).arrange(DOWN, buff=0.56)
        eigenpairs.move_to(DOWN * 0.25)
        self.play(FadeIn(plus_vector))
        self.play(FadeIn(minus_vector))
        self.wait(1.5)

        heading = self._replace_heading(
            heading, "For a unit eigenvector, its eigenvalue is its quadratic energy."
        )
        self.play(FadeOut(eigenpairs))
        unit_rule = VGroup(
            MathTex(r"Au=\lambda u,\qquad \lVert u\rVert=1", font_size=49),
            MathTex(
                r"u^T A u=u^T(\lambda u)=\lambda\,u^Tu=\boxed{\lambda}",
                font_size=52,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.58).move_to(DOWN * 0.26)
        self.play(FadeIn(unit_rule[0]))
        self.play(FadeIn(unit_rule[1]))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "In an eigenvector basis, every quadratic energy separates into squares."
        )
        self.play(FadeOut(unit_rule))
        decomposition = MathTex(
            r"x=c_+u_++c_-u_-", font_size=48, color=WHITE
        )
        example_energy = MathTex(
            r"x^T A x=3c_+^2+c_-^2", font_size=55, color=GREEN_C
        )
        general_energy = MathTex(
            r"x=\sum_i c_i u_i\quad\Longrightarrow\quad x^T A x=\sum_i\lambda_i c_i^2",
            font_size=46,
            color=YELLOW,
        )
        energy_card = VGroup(decomposition, example_energy, general_energy).arrange(
            DOWN, buff=0.55
        ).move_to(DOWN * 0.28)
        self.play(FadeIn(decomposition))
        self.play(FadeIn(example_energy))
        self.play(FadeIn(general_energy))
        self.wait(1.9)

        heading = self._replace_heading(
            heading, "The coefficient signs reproduce the three geometries from the last lesson."
        )
        self.play(FadeOut(energy_card))
        positive_box = self._box("both positive", r"3c_+^2+c_-^2", GREEN_C)
        zero_box = self._box("one zero", r"3c_+^2+0c_-^2", YELLOW)
        negative_box = self._box("one negative", r"3c_+^2-3c_-^2", RED_C)
        comparison = VGroup(positive_box, zero_box, negative_box).arrange(RIGHT, buff=0.38)
        if comparison.width > 11.3:
            comparison.scale_to_fit_width(11.3)
        comparison.move_to(DOWN * 0.26)
        self.play(FadeIn(positive_box))
        self.play(FadeIn(zero_box))
        self.play(FadeIn(negative_box))
        self.wait(1.9)

        heading = self._replace_heading(
            heading, "For a symmetric matrix, positivity is decided by its eigenvalues."
        )
        self.play(FadeOut(comparison))
        theorem = MathTex(
            r"\boxed{"
            r"A=A^T\ \text{is positive definite}"
            r"\quad\Longleftrightarrow\quad"
            r"\lambda_i>0\ \text{for every eigenvalue}"
            r"}",
            font_size=44,
            color=YELLOW,
        )
        application = VGroup(
            MathTex(r"\lambda_1=1>0,\qquad\lambda_2=3>0", font_size=48, color=GREEN_C),
            Text("So the matrix is positive definite.", font_size=36, color=GREEN_C, weight="BOLD"),
        ).arrange(DOWN, buff=0.36)
        final_card = VGroup(theorem, application).arrange(DOWN, buff=0.68)
        final_card.move_to(DOWN * 0.30)
        if final_card.width > 11.4:
            final_card.scale_to_fit_width(11.4)
        self.play(FadeIn(theorem))
        self.play(FadeIn(application))
        self.wait(2.6)
