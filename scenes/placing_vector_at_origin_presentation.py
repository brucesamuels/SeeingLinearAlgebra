"""Presentation scene: translate a general vector into standard position."""

from __future__ import annotations

from manim import (
    Create,
    FadeIn,
    FadeOut,
    LEFT,
    NumberPlane,
    Scene,
    ValueTracker,
    VGroup,
    Write,
    linear,
)

from engine.manim_instructional_widgets import ThemedText
from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME
from engine.manim_vector_to_origin_display import ManimVectorToOriginDisplay
from engine.vector_to_origin_lesson import VECTOR_TO_ORIGIN_LESSON_SEQUENCE
from engine.vector_to_origin_translation import VectorToOriginTranslation


INITIAL_POINT = (2.0, 1.0)
TERMINAL_POINT = (5.0, 3.0)


def update_vector_to_origin_display(
    display: ManimVectorToOriginDisplay,
    translation_path: VectorToOriginTranslation,
    progress: float,
):
    """Query one snapshot and forward it to the synchronized display."""
    snapshot = translation_path.snapshot(progress)
    display.update_from_snapshot(snapshot)
    return snapshot


class PlacingVectorAtOriginPresentation(Scene):
    """Show why subtracting the initial point places a vector at the origin."""

    LESSON_SEQUENCE = VECTOR_TO_ORIGIN_LESSON_SEQUENCE
    THEME = SEEING_LINEAR_ALGEBRA_THEME
    LAYOUT = LessonLayout()

    def construct(self) -> None:
        title = ThemedText.lesson_title(
            "Placing a Vector at the Origin",
            theme=self.THEME,
        )
        self.LAYOUT.place_title(title)

        translation_path = VectorToOriginTranslation(
            initial_point=INITIAL_POINT,
            terminal_point=TERMINAL_POINT,
        )
        initial_snapshot = translation_path.snapshot(0.0)

        plane = NumberPlane(
            x_range=[-1, 6, 1],
            y_range=[-1, 4, 1],
            x_length=6.5,
            y_length=4.6,
            background_line_style={
                "stroke_color": self.THEME.colors.narration,
                "stroke_opacity": 0.38,
                "stroke_width": 1.0,
            },
            axis_config={
                "color": self.THEME.colors.mathematics,
                "stroke_width": 2.0,
                "include_numbers": True,
                "font_size": 22,
            },
        )
        plane.shift(LEFT * 2.15 + [0.0, -0.35, 0.0])

        display = ManimVectorToOriginDisplay(
            initial_snapshot,
            plane,
            formula_anchor=(3.55, -0.15, 0.0),
            arrow_kwargs={
                "color": self.THEME.colors.geometry,
                "stroke_width": 6.0,
            },
            point_kwargs={
                "color": self.THEME.colors.example,
                "radius": 0.075,
            },
            label_kwargs={
                "font_size": 28,
                "color": self.THEME.colors.mathematics,
            },
            formula_kwargs={
                "font_size": 27,
                "color": self.THEME.colors.mathematics,
            },
        )
        display.tip_dot.set_color(self.THEME.colors.definition)

        prompt = ThemedText.guiding_question(
            "How can we move the tail to the origin without changing the vector?",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(prompt)

        subtraction_caption = ThemedText.body(
            "Subtract the initial point from both endpoints.",
            theme=self.THEME,
        )
        subtraction_caption.move_to([3.55, 1.75, 0.0])

        takeaway = VGroup(
            ThemedText.takeaway(
                "Same vector, now in standard position",
                theme=self.THEME,
            ).set_color(self.THEME.colors.definition),
            ThemedText.body(
                "Its coordinates are terminal minus initial: (5, 3) - (2, 1) = (3, 2).",
                theme=self.THEME,
            ),
        ).arrange([0.0, -1.0, 0.0], buff=0.16)
        self.LAYOUT.place_footer(takeaway)

        self.play(Write(title))

        # ORIENT — first show only a general arrow on an otherwise blank field.
        self.play(Create(display.arrow))
        self.wait(self.THEME.timing.normal)

        # OBSERVE — reveal the coordinate system and the two endpoint coordinates.
        self.play(FadeIn(plane))
        self.bring_to_front(display.arrow)
        self.play(
            FadeIn(display.tail_dot),
            FadeIn(display.tip_dot),
            FadeIn(display.tail_label),
            FadeIn(display.tip_label),
        )
        self.wait(self.THEME.timing.normal)

        # PREDICT
        self.play(FadeIn(prompt))
        self.wait(self.THEME.timing.read)
        self.play(FadeOut(prompt))

        # OBSERVE — the readout, endpoint labels, and geometry use one snapshot.
        self.play(
            FadeIn(subtraction_caption),
            FadeIn(display.formula),
        )
        self.wait(self.THEME.timing.read)

        progress = ValueTracker(0.0)
        display.arrow.add_updater(
            lambda _arrow: update_vector_to_origin_display(
                display,
                translation_path,
                progress.get_value(),
            )
        )
        self.play(
            progress.animate.set_value(1.0),
            run_time=3.0,
            rate_func=linear,
        )
        display.arrow.remove_updater(display.arrow.get_updaters()[0])
        final_snapshot = update_vector_to_origin_display(
            display,
            translation_path,
            1.0,
        )
        assert final_snapshot.is_at_origin
        self.wait(self.THEME.timing.normal)

        # REFLECT
        self.play(
            FadeOut(subtraction_caption),
            FadeIn(takeaway),
        )
        self.wait(self.THEME.timing.reflection)
