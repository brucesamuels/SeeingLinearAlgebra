"""Presentation scene: equal free vectors may appear at different locations."""

from __future__ import annotations

from manim import (
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    MathTex,
    ReplacementTransform,
    Scene,
    VGroup,
    Write,
)

from engine.free_vector_equality import FreeVectorEquality
from engine.free_vector_equality_lesson import (
    FREE_VECTOR_EQUALITY_LESSON_SEQUENCE,
)
from engine.manim_instructional_widgets import ThemedText
from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME


class FreeVectorEqualityPresentation(Scene):
    LESSON_SEQUENCE = FREE_VECTOR_EQUALITY_LESSON_SEQUENCE
    THEME = SEEING_LINEAR_ALGEBRA_THEME
    LAYOUT = LessonLayout()

    def construct(self) -> None:
        title = ThemedText.lesson_title(
            "Free Vectors and Equality",
            theme=self.THEME,
        )
        self.LAYOUT.place_title(title)

        equality_snapshot = FreeVectorEquality(
            coordinates=[2.0, 1.0],
            origins=(
                [-4.0, -2.0],
                [-1.5, 1.2],
                [1.0, -1.5],
                [3.0, 1.0],
            ),
        ).snapshot()

        arrows = VGroup(
            *[
                Arrow(
                    start=[copy.origin[0], copy.origin[1], 0.0],
                    end=[copy.endpoint[0], copy.endpoint[1], 0.0],
                    buff=0.0,
                    color=self.THEME.colors.geometry,
                )
                for copy in equality_snapshot.copies
            ]
        )

        coordinate_label = MathTex(
            r"\mathbf{v}=\begin{bmatrix}2\\1\end{bmatrix}"
        )
        coordinate_label.scale(0.75)
        coordinate_label.set_color(self.THEME.colors.mathematics)
        self.LAYOUT.place_footer(coordinate_label)

        prompt = ThemedText.guiding_question(
            "If we move the arrow, is it still the same vector?",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(prompt)

        invariants = VGroup(
            ThemedText.body(
                "same coordinates",
                theme=self.THEME,
            ).set_color(self.THEME.colors.mathematics),
            ThemedText.body(
                "same direction",
                theme=self.THEME,
            ).set_color(self.THEME.colors.geometry),
            ThemedText.body(
                "same magnitude",
                theme=self.THEME,
            ).set_color(self.THEME.colors.geometry),
            ThemedText.body(
                "different location",
                theme=self.THEME,
            ).set_color(self.THEME.colors.example),
        ).arrange([0.0, -1.0, 0.0], buff=0.15)
        invariants.to_edge([1.0, 0.0, 0.0])

        definition = VGroup(
            ThemedText.takeaway(
                "Equal free vectors have the same",
                theme=self.THEME,
            ).set_color(self.THEME.colors.definition),
            ThemedText.body(
                "direction and magnitude, regardless of location.",
                theme=self.THEME,
            ),
        ).arrange([0.0, -1.0, 0.0], buff=0.18)
        self.LAYOUT.place_footer(definition)

        self.play(Write(title))

        # ORIENT
        self.play(Create(arrows[0]))
        self.play(FadeIn(coordinate_label))
        self.wait(self.THEME.timing.normal)

        # PREDICT
        self.play(FadeIn(prompt))
        self.wait(self.THEME.timing.read)
        self.play(FadeOut(prompt))

        # OBSERVE
        moving_arrow = arrows[0].copy()
        self.add(moving_arrow)
        for target in arrows[1:]:
            next_arrow = target.copy()
            self.play(ReplacementTransform(moving_arrow, next_arrow))
            moving_arrow = next_arrow
            self.wait(self.THEME.timing.quick)

        self.play(FadeOut(moving_arrow))
        self.play(*[FadeIn(arrow) for arrow in arrows])
        self.wait(self.THEME.timing.normal)

        # STABILIZE
        self.play(FadeIn(invariants))
        self.wait(self.THEME.timing.read)

        # REFLECT
        self.play(
            FadeOut(invariants),
            FadeOut(coordinate_label),
            FadeIn(definition),
        )
        self.wait(self.THEME.timing.reflection)
