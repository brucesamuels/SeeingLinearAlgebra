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
    Text,
    UP,
    VGroup,
    Write,
)

from engine.free_vector_equality import FreeVectorEquality
from engine.free_vector_equality_lesson import (
    FREE_VECTOR_EQUALITY_LESSON_SEQUENCE,
)


class FreeVectorEqualityPresentation(Scene):
    LESSON_SEQUENCE = FREE_VECTOR_EQUALITY_LESSON_SEQUENCE

    def construct(self) -> None:
        title = Text("Free Vectors and Equality").scale(0.8).to_edge(UP)

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
                )
                for copy in equality_snapshot.copies
            ]
        )

        coordinate_label = MathTex(r"\mathbf{v}=\begin{bmatrix}2\\1\end{bmatrix}")
        coordinate_label.scale(0.75)
        coordinate_label.to_edge([0.0, -1.0, 0.0])

        prompt = Text(
            "If we move the arrow, is it still the same vector?"
        ).scale(0.52)
        prompt.next_to(title, [0.0, -1.0, 0.0], buff=0.35)

        invariants = VGroup(
            Text("same coordinates").scale(0.48),
            Text("same direction").scale(0.48),
            Text("same magnitude").scale(0.48),
            Text("different location").scale(0.48),
        ).arrange([0.0, -1.0, 0.0], buff=0.15)
        invariants.to_edge([1.0, 0.0, 0.0])

        definition = VGroup(
            Text("Equal free vectors have the same").scale(0.5),
            Text("direction and magnitude, regardless of location.").scale(0.5),
        ).arrange([0.0, -1.0, 0.0], buff=0.18)
        definition.to_edge([0.0, -1.0, 0.0])

        self.play(Write(title))

        # ORIENT
        self.play(Create(arrows[0]))
        self.play(FadeIn(coordinate_label))
        self.wait(0.5)

        # PREDICT
        self.play(FadeIn(prompt))
        self.wait(1.0)
        self.play(FadeOut(prompt))

        # OBSERVE
        moving_arrow = arrows[0].copy()
        self.add(moving_arrow)
        for target in arrows[1:]:
            next_arrow = target.copy()
            self.play(ReplacementTransform(moving_arrow, next_arrow))
            moving_arrow = next_arrow
            self.wait(0.35)

        self.play(FadeOut(moving_arrow))
        self.play(*[FadeIn(arrow) for arrow in arrows])
        self.wait(0.5)

        # STABILIZE
        self.play(FadeIn(invariants))
        self.wait(0.9)

        # REFLECT
        self.play(
            FadeOut(invariants),
            FadeOut(coordinate_label),
            FadeIn(definition),
        )
        self.wait(1.0)
