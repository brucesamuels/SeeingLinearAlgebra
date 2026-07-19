"""Presentation scene: visualize scalar multiplication of one vector."""

from __future__ import annotations

from manim import (
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    NumberPlane,
    ReplacementTransform,
    Scene,
    Transform,
    VGroup,
    Write,
)

from engine.manim_instructional_widgets import ThemedText
from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME
from engine.scalar_multiplication_lesson import (
    BASE_VECTOR,
    SCALAR_MULTIPLICATION_STAGES,
    scaled_vector,
)


class ScalarMultiplicationPresentation(Scene):
    """Show how the scalar controls length and direction."""

    LESSON_STAGES = SCALAR_MULTIPLICATION_STAGES
    THEME = SEEING_LINEAR_ALGEBRA_THEME
    LAYOUT = LessonLayout()

    def construct(self) -> None:
        title = ThemedText.lesson_title("Scalar Multiplication", theme=self.THEME)
        self.LAYOUT.place_title(title)

        question = ThemedText.guiding_question(
            "What does multiplying a vector by a number do?",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(question)

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=8.0,
            y_length=4.8,
            background_line_style={
                "stroke_color": self.THEME.colors.narration,
                "stroke_opacity": 0.34,
                "stroke_width": 1.0,
            },
            axis_config={
                "color": self.THEME.colors.mathematics,
                "stroke_width": 2.0,
                "include_numbers": True,
                "font_size": 22,
            },
        )
        plane.shift(LEFT * 1.55 + [0.0, -0.35, 0.0])
        origin = plane.c2p(0.0, 0.0)

        vector_arrow = Arrow(
            origin,
            plane.c2p(*BASE_VECTOR),
            buff=0.0,
            color=self.THEME.colors.geometry,
            stroke_width=7.0,
        )
        vector_label = MathTex(
            r"\mathbf{v}=(2,1)",
            color=self.THEME.colors.geometry,
        ).scale(0.72)
        vector_label.move_to([3.85, 1.30, 0.0])

        scalar_readout = MathTex(
            r"1\mathbf{v}=(2,1)",
            color=self.THEME.colors.mathematics,
        ).scale(0.78)
        scalar_readout.move_to([3.85, 0.45, 0.0])

        interpretation = ThemedText.body(
            "The scalar controls the vector's length and direction.",
            theme=self.THEME,
        )
        interpretation.move_to([3.85, -0.55, 0.0])

        endpoint = Dot(
            plane.c2p(*BASE_VECTOR),
            color=self.THEME.colors.definition,
            radius=0.08,
        )

        takeaway = VGroup(
            ThemedText.takeaway(
                "Scalar multiplication changes magnitude and may reverse direction",
                theme=self.THEME,
            ).set_color(self.THEME.colors.definition),
            MathTex(
                r"(-1)\mathbf{v}=-\mathbf{v}",
                color=self.THEME.colors.application,
            ).scale(0.70),
        ).arrange([0.0, -1.0, 0.0], buff=0.14)
        self.LAYOUT.place_footer(takeaway)

        self.play(Write(title))
        self.play(FadeIn(plane), Create(vector_arrow), FadeIn(endpoint))
        self.play(FadeIn(vector_label), FadeIn(question))
        self.wait(self.THEME.timing.read)
        self.play(FadeOut(question), FadeIn(scalar_readout), FadeIn(interpretation))

        for stage in self.LESSON_STAGES:
            result = scaled_vector(stage.scalar)
            render_tip = result if result != (0.0, 0.0) else (1.0e-8, 0.0)
            target_arrow = Arrow(
                origin,
                plane.c2p(*render_tip),
                buff=0.0,
                color=(
                    self.THEME.colors.application
                    if stage.scalar < 0
                    else self.THEME.colors.geometry
                ),
                stroke_width=7.0,
            )
            target_endpoint = Dot(
                plane.c2p(*result),
                color=self.THEME.colors.definition,
                radius=0.08,
            )
            result_tex = _scalar_equation(stage.scalar, result)
            target_readout = MathTex(
                result_tex,
                color=self.THEME.colors.mathematics,
            ).scale(0.78)
            target_readout.move_to(scalar_readout)
            target_interpretation = ThemedText.body(
                stage.interpretation,
                theme=self.THEME,
            )
            target_interpretation.move_to(interpretation)

            self.play(
                Transform(vector_arrow, target_arrow),
                Transform(endpoint, target_endpoint),
                ReplacementTransform(scalar_readout, target_readout),
                ReplacementTransform(interpretation, target_interpretation),
            )
            scalar_readout = target_readout
            interpretation = target_interpretation
            self.wait(self.THEME.timing.read)

        self.play(FadeIn(takeaway))
        self.wait(self.THEME.timing.reflection)


def _scalar_equation(
    scalar: float,
    result: tuple[float, float],
) -> str:
    scalar_tex = {
        2.0: "2",
        0.5: r"\tfrac12",
        0.0: "0",
        -1.0: "-1",
    }[scalar]
    x, y = (_display_number(value) for value in result)
    return rf"({scalar_tex})\mathbf{{v}}=({x},{y})"


def _display_number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)
