"""Presentation scene for the introductory lesson: What Is a Vector?"""

from __future__ import annotations

from manim import (
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    ReplacementTransform,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    Write,
)

from engine.manim_vector_representation_display import (
    ManimVectorRepresentationDisplay,
)
from engine.vector_representation import VectorRepresentation
from engine.vector_representation_display import (
    VectorRepresentationDisplayProjector,
)
from engine.vector_representation_lesson import (
    VECTOR_REPRESENTATION_LESSON_SEQUENCE,
)


class VectorRepresentationPresentation(Scene):
    """Teach equivalent geometric and coordinate views of one vector."""

    LESSON_SEQUENCE = VECTOR_REPRESENTATION_LESSON_SEQUENCE

    def construct(self) -> None:
        title = Text("What Is a Vector?").scale(0.8).to_edge(UP)

        mathematical_snapshot = VectorRepresentation([3.0, 2.0]).snapshot()
        display_snapshot = VectorRepresentationDisplayProjector(
            display_dimension=2,
            number_format=".1f",
            magnitude_label="magnitude",
        ).project(mathematical_snapshot)

        display = ManimVectorRepresentationDisplay(display_snapshot)
        display.shift(1.2 * LEFT)

        start = display.arrow.get_start()
        end = display.arrow.get_end()
        corner = [end[0], start[1], 0.0]

        horizontal_leg = DashedLine(start, corner)
        vertical_leg = DashedLine(corner, end)

        horizontal_label = MathTex("3").scale(0.7)
        horizontal_label.next_to(horizontal_leg, direction=[0.0, -1.0, 0.0])

        vertical_label = MathTex("2").scale(0.7)
        vertical_label.next_to(vertical_leg, RIGHT)

        component_triangle = VGroup(
            horizontal_leg,
            vertical_leg,
            horizontal_label,
            vertical_label,
        )

        prompt = Text(
            "Which coordinates describe this displacement?"
        ).scale(0.55)
        prompt.next_to(title, direction=[0.0, -1.0, 0.0], buff=0.35)

        equivalence = Text(
            "One vector, several equivalent representations"
        ).scale(0.55)
        equivalence.next_to(title, direction=[0.0, -1.0, 0.0], buff=0.35)

        pythagorean_reference = Text(
            "Use the Pythagorean distance formula"
        ).scale(0.5)
        pythagorean_reference.next_to(
            title,
            direction=[0.0, -1.0, 0.0],
            buff=0.35,
        )

        magnitude_formula = MathTex(
            r"\|\mathbf{v}\|=\sqrt{3^2+2^2}"
        ).scale(0.75)
        magnitude_formula.to_edge([0.0, -1.0, 0.0])

        magnitude_exact = MathTex(
            r"\|\mathbf{v}\|=\sqrt{13}"
        ).scale(0.75)
        magnitude_exact.move_to(magnitude_formula)

        magnitude_decimal = MathTex(
            r"\|\mathbf{v}\|\approx 3.6"
        ).scale(0.75)
        magnitude_decimal.move_to(magnitude_formula)

        # Final label uses the same Text class and scale as dimension_label.
        magnitude_label = Text(display_snapshot.magnitude_text).scale(
            display.style.label_scale
        )
        magnitude_label.next_to(
            display.dimension_label,
            direction=[0.0, 1.0, 0.0],
            buff=display.style.vertical_gap,
            aligned_edge=LEFT,
        )

        reflection = VGroup(
            Text("The arrow shows direction and magnitude.").scale(0.48),
            Text("The coordinates encode the same vector.").scale(0.48),
        ).arrange(direction=[0.0, -1.0, 0.0], buff=0.2)
        reflection.to_edge([0.0, -1.0, 0.0])

        self.play(Write(title))

        # ORIENT
        self.play(Create(display.arrow))
        self.wait(0.5)

        # PREDICT
        self.play(FadeIn(prompt))
        self.wait(1.0)
        self.play(FadeOut(prompt))

        # OBSERVE
        self.play(
            Create(horizontal_leg),
            Create(vertical_leg),
            FadeIn(horizontal_label),
            FadeIn(vertical_label),
        )
        self.play(FadeIn(display.row_coordinates))
        self.play(FadeIn(display.column_coordinates))
        self.play(FadeIn(equivalence))
        self.wait(0.75)

        # STABILIZE
        self.play(FadeOut(equivalence), FadeIn(pythagorean_reference))
        self.play(Write(magnitude_formula))
        self.play(ReplacementTransform(magnitude_formula, magnitude_exact))
        self.play(ReplacementTransform(magnitude_exact, magnitude_decimal))
        self.play(
            ReplacementTransform(magnitude_decimal, magnitude_label),
            FadeIn(display.dimension_label),
            FadeOut(pythagorean_reference),
        )
        self.wait(0.75)

        # REFLECT
        self.play(
            FadeOut(magnitude_label),
            FadeOut(display.dimension_label),
            FadeOut(component_triangle),
            FadeIn(reflection),
        )
        self.wait(1.0)
