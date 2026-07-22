"""Checkpoint 68: the opening Chapter 2 lesson on one-vector span."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    BLUE,
    DOWN,
    FadeIn,
    FadeOut,
    GrowArrow,
    LaggedStart,
    LEFT,
    Line,
    linear,
    MathTex,
    NumberPlane,
    ORIGIN,
    RIGHT,
    Scene,
    Text,
    TracedPath,
    UP,
    ValueTracker,
    VGroup,
    WHITE,
    YELLOW,
    Create,
    DecimalNumber,
    Dot,
)

from engine.manim_one_vector_span import ManimOneVectorSpan
from engine.one_vector_span import OneVectorSpan


CHAPTER_TITLE = "Vector Spaces and Subspaces"
OPENING_QUESTION = "What should we call the collection\nof all vectors we can create?"
LESSON_QUESTION = "What collection can one vector create?"
PREDICTION_PROMPT = "As t takes every real value,\nwhere can the endpoint go?"
SPAN_DEFINITION = (
    r"\operatorname{span}\{\mathbf v\}="
    r"\{t\mathbf v:t\in\mathbb R\}"
)
KEY_IDEA = "One nonzero vector generates a line through the origin."
REFLECTION_PROMPT = "Why must the line pass through the origin?"
GENERATOR = np.array([2.0, 1.0])
COEFFICIENT_EXTENT = 2.75

# The established Chapter 1 palette is retained explicitly here while the
# mathematical model and Manim adapter remain independent of presentation.
BACKGROUND = "#0A0D13"
GRID = "#3A4256"
TEXT = "#E8EAED"
MUTED = "#9AA4B2"
ACCENT = "#4FC3F7"
SPAN_COLOR = "#F6C85F"


class OneVectorSpanPresentation(Scene):
    """Reveal span through continuous scalar-multiple motion."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self._chapter_opening()
        self._one_vector_lesson()

    def _chapter_opening(self) -> None:
        chapter_number = Text("CHAPTER 2", font_size=24, color=ACCENT)
        title = Text(CHAPTER_TITLE, font_size=46, color=TEXT)
        title_group = VGroup(chapter_number, title).arrange(DOWN, buff=0.18)

        cloud = self._living_vector_echo().shift(DOWN * 0.35)
        formula = MathTex(
            r"a\mathbf u+b\mathbf v",
            font_size=46,
            color=SPAN_COLOR,
        ).next_to(cloud, DOWN, buff=0.35)

        self.play(FadeIn(chapter_number, shift=UP * 0.15))
        self.play(FadeIn(title, shift=UP * 0.15))
        self.wait(0.8)
        self.play(FadeOut(title_group, shift=UP * 0.2))

        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=0.5) for dot in cloud],
                lag_ratio=0.025,
            ),
            FadeIn(formula),
        )
        self.wait(0.8)

        opening_question = Text(
            OPENING_QUESTION,
            font_size=36,
            color=TEXT,
            line_spacing=0.9,
        ).to_edge(UP, buff=0.6)
        self.play(FadeIn(opening_question, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(VGroup(cloud, formula, opening_question)))

    def _one_vector_lesson(self) -> None:
        model = OneVectorSpan(GENERATOR)
        coefficient = ValueTracker(1.0)

        title = Text(LESSON_QUESTION, font_size=38, color=TEXT).to_edge(UP, buff=0.35)
        plane = NumberPlane(
            x_range=(-7, 7, 1),
            y_range=(-4, 4, 1),
            x_length=12.5,
            y_length=7.0,
            background_line_style={
                "stroke_color": GRID,
                "stroke_width": 1.0,
                "stroke_opacity": 0.42,
            },
            axis_config={"stroke_color": MUTED, "stroke_width": 1.7},
        ).shift(DOWN * 0.45)

        map_point = lambda coordinates: plane.c2p(*coordinates)
        origin = map_point(np.zeros(2))
        generator_endpoint = map_point(GENERATOR)

        generator_arrow = Arrow(
            origin,
            generator_endpoint,
            buff=0.0,
            color=BLUE,
            stroke_width=7,
            tip_length=0.22,
        )
        generator_label = MathTex(r"\mathbf v", font_size=38, color=BLUE)
        generator_label.next_to(generator_endpoint, UP + LEFT, buff=0.12)

        moving = ManimOneVectorSpan(
            model.snapshot(coefficient.get_value()),
            map_point,
            arrow_kwargs={"color": YELLOW, "stroke_width": 8, "tip_length": 0.24},
            dot_kwargs={"color": WHITE, "radius": 0.065},
        )

        moving.mobject.add_updater(
            lambda _mob: moving.update_from_snapshot(
                model.snapshot(coefficient.get_value())
            )
        )

        coefficient_number = DecimalNumber(
            coefficient.get_value(),
            num_decimal_places=2,
            include_sign=True,
            font_size=34,
            color=YELLOW,
        )
        coefficient_number.add_updater(
            lambda number: number.set_value(coefficient.get_value())
        )
        coefficient_readout = VGroup(
            MathTex(r"t=", font_size=34, color=TEXT),
            coefficient_number,
        ).arrange(RIGHT, buff=0.12).to_corner(UP + RIGHT, buff=0.45)

        multiple_label = MathTex(r"t\mathbf v", font_size=38, color=YELLOW)
        multiple_label.add_updater(
            lambda label: label.next_to(
                moving.endpoint_dot,
                DOWN if coefficient.get_value() >= 0 else UP,
                buff=0.14,
            )
        )

        prediction = VGroup(
            Text("PAUSE AND PREDICT", font_size=20, color=ACCENT),
            Text(PREDICTION_PROMPT, font_size=28, color=TEXT, line_spacing=0.9),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        prediction.to_corner(UP + LEFT, buff=0.55).shift(DOWN * 0.7)

        trace = TracedPath(
            moving.endpoint_dot.get_center,
            stroke_color=SPAN_COLOR,
            stroke_width=6,
        )

        self.play(FadeIn(title), Create(plane))
        self.play(GrowArrow(generator_arrow), FadeIn(generator_label))
        self.wait(0.6)
        self.play(FadeIn(prediction, shift=RIGHT * 0.15))
        self.wait(2.4)
        self.play(FadeOut(prediction))

        self.add(trace)
        self.play(
            FadeIn(moving.mobject),
            FadeIn(multiple_label),
            FadeIn(coefficient_readout),
        )

        # Continuous motion makes the span appear before it is named.
        self.play(coefficient.animate.set_value(COEFFICIENT_EXTENT), run_time=2.4, rate_func=linear)
        self.play(coefficient.animate.set_value(0.0), run_time=1.6, rate_func=linear)
        self.play(coefficient.animate.set_value(-COEFFICIENT_EXTENT), run_time=3.2, rate_func=linear)
        self.play(coefficient.animate.set_value(1.0), run_time=2.2, rate_func=linear)

        moving.mobject.clear_updaters()
        coefficient_number.clear_updaters()
        multiple_label.clear_updaters()
        moving.update_from_snapshot(model.snapshot(1.0))
        coefficient_number.set_value(1.0)
        multiple_label.next_to(moving.endpoint_dot, DOWN, buff=0.14)

        span_line = Line(
            map_point(model.snapshot(-COEFFICIENT_EXTENT).endpoint),
            map_point(model.snapshot(COEFFICIENT_EXTENT).endpoint),
            color=SPAN_COLOR,
            stroke_width=7,
        )
        self.play(FadeOut(trace), Create(span_line), run_time=1.5)

        definition = MathTex(SPAN_DEFINITION, font_size=40, color=TEXT)
        definition.to_edge(DOWN, buff=0.62)
        key_idea = Text(KEY_IDEA, font_size=28, color=MUTED)
        key_idea.next_to(definition, UP, buff=0.22)

        self.play(FadeIn(definition, shift=UP * 0.15))
        self.play(FadeIn(key_idea))
        self.wait(2.4)

        reflection = Text(REFLECTION_PROMPT, font_size=30, color=ACCENT)
        reflection.next_to(key_idea, UP, buff=0.22)
        self.play(FadeIn(reflection))
        self.wait(3.0)

    @staticmethod
    def _living_vector_echo() -> VGroup:
        """A compact visual echo of the Chapter 1 finale, not a reused scene."""

        u = np.array([1.1, 0.25, 0.0])
        v = np.array([-0.25, 0.85, 0.0])
        dots = []
        for a in np.linspace(-2.0, 2.0, 9):
            for b in np.linspace(-1.5, 1.5, 7):
                point = 0.62 * (a * u + b * v)
                dots.append(Dot(point, radius=0.035, color=SPAN_COLOR).set_opacity(0.72))
        return VGroup(*dots)
