"""Smoke scene for the introductory vector-representation display."""

from __future__ import annotations

from manim import Create, FadeIn, Scene

from engine.manim_vector_representation_display import (
    ManimVectorRepresentationDisplay,
)
from engine.vector_representation import VectorRepresentation
from engine.vector_representation_display import (
    VectorRepresentationDisplayProjector,
)


class VectorRepresentationDisplaySmoke(Scene):
    def construct(self) -> None:
        snapshot = VectorRepresentation([3.0, 2.0]).snapshot()
        display_snapshot = VectorRepresentationDisplayProjector(
            display_dimension=2,
            number_format=".1f",
        ).project(snapshot)

        display = ManimVectorRepresentationDisplay(display_snapshot)
        display.move_to([0.0, 0.0, 0.0])

        self.play(Create(display.arrow))
        self.play(FadeIn(display.information_group))
        self.wait(1)
