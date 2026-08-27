"""Manim presentation: Positive Definite Matrices — Why Positive Definiteness?"""
from __future__ import annotations

import numpy as np

from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Circle, Create, DecimalNumber, FadeIn, FadeOut, MathTex, Matrix,
    NumberPlane, ReplacementTransform, Scene, Text, ValueTracker, VGroup,
    always_redraw, linear,
)

from engine.positive_definite_directional_energy import DirectionalQuadraticEnergy


class PositiveDefiniteWhyPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "Why Positive Definiteness?"

    def _chrome(self, heading_text):
        banner = Text(
            self.CHAPTER_BANNER, font_size=21, color=GREY_B, weight="BOLD"
        ).to_edge(UP, buff=0.16)
        title = Text(
            self.LESSON_TITLE, font_size=31, color=YELLOW, weight="BOLD"
        ).next_to(banner, DOWN, buff=0.11)
        heading = Text(heading_text, font_size=27, color=WHITE)
        if heading.width > 11.4:
            heading.scale_to_fit_width(11.4)
        heading.next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = Text(text, font_size=27, color=WHITE)
        if new.width > 11.4:
            new.scale_to_fit_width(11.4)
        new.move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.6)
        return new

    @staticmethod
    def _matrix(entries, scale=0.78):
        return Matrix(entries, h_buff=0.9, v_buff=0.78).scale(scale)

    def construct(self):
        model = DirectionalQuadraticEnergy()
        banner, title, heading = self._chrome(
            "A matrix can assign a scalar energy to every direction."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        matrix_card = VGroup(
            MathTex("A=", font_size=44),
            self._matrix([["2", "1"], ["1", "2"]]),
        ).arrange(RIGHT, buff=0.14)
        vector_card = VGroup(
            MathTex(r"x(\theta)=", font_size=42),
            self._matrix([[r"\cos\theta"], [r"\sin\theta"]], scale=0.70),
        ).arrange(RIGHT, buff=0.12)
        definition = MathTex(r"q(x)=x^T A x", font_size=52, color=YELLOW)
        opening = VGroup(matrix_card, vector_card, definition).arrange(RIGHT, buff=0.72)
        opening.move_to(DOWN * 0.25)
        if opening.width > 11.3:
            opening.scale_to_fit_width(11.3)
        self.play(FadeIn(matrix_card), FadeIn(vector_card))
        self.play(FadeIn(definition))
        self.wait(1.4)

        heading = self._replace_heading(
            heading, "Turn the unit vector and watch its quadratic energy."
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
        unit_circle = Circle(radius=unit_radius, color=GREY_B, stroke_width=2.5).move_to(origin)
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
            lambda: MathTex(r"x(\theta)", font_size=33, color=ORANGE).next_to(
                plane.c2p(*model.direction(theta.get_value())), UP, buff=0.10
            )
        )

        matrix_readout = VGroup(
            MathTex("A=", font_size=37),
            self._matrix([["2", "1"], ["1", "2"]], scale=0.68),
        ).arrange(RIGHT, buff=0.10).move_to(RIGHT * 3.45 + UP * 0.42)
        energy_readout = always_redraw(
            lambda: VGroup(
                MathTex(r"x^T A x=", font_size=48, color=YELLOW),
                DecimalNumber(
                    model.directional_energy(theta.get_value()),
                    num_decimal_places=2,
                    font_size=49,
                    color=GREEN_C,
                ),
            ).arrange(RIGHT, buff=0.18).move_to(RIGHT * 3.45 + DOWN * 0.48)
        )
        positive_note = Text(
            "positive", font_size=31, color=GREEN_C, weight="BOLD"
        ).move_to(RIGHT * 3.45 + DOWN * 1.35)
        readout = VGroup(matrix_readout, energy_readout, positive_note)

        self.play(Create(plane), Create(unit_circle))
        self.play(FadeIn(direction_arrow), FadeIn(x_label), FadeIn(readout))
        self.wait(0.8)
        for target in (np.pi / 3, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi):
            self.play(theta.animate.set_value(target), run_time=1.25, rate_func=linear)
            self.wait(0.25)

        heading = self._replace_heading(
            heading, "Can any nonzero direction make this value zero or negative?"
        )
        question = Text(
            "Pause and predict.", font_size=34, color=YELLOW, weight="BOLD"
        ).to_edge(DOWN, buff=0.24)
        self.play(FadeIn(question))
        self.wait(2.6)

        self.play(FadeOut(question))
        for target in (7 * np.pi / 3, 5 * np.pi / 2, 3 * np.pi):
            self.play(theta.animate.set_value(target), run_time=1.15, rate_func=linear)
        self.wait(0.7)

        heading = self._replace_heading(
            heading, "Every nonzero direction has strictly positive quadratic energy."
        )
        self.play(
            FadeOut(plane), FadeOut(unit_circle), FadeOut(direction_arrow),
            FadeOut(x_label), FadeOut(readout)
        )
        final_definition = MathTex(
            r"\boxed{x^T A x>0\quad\text{for every }x\ne 0}",
            font_size=58,
            color=YELLOW,
        )
        term = Text("positive definite", font_size=46, color=GREEN_C, weight="BOLD")
        final_card = VGroup(final_definition, term).arrange(DOWN, buff=0.62).move_to(DOWN * 0.35)
        self.play(FadeIn(final_definition))
        self.play(FadeIn(term))
        self.wait(2.4)
