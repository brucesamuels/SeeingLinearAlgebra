"""Presentation scene: introduce vector addition through head-to-tail motion."""

from __future__ import annotations

from manim import (
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    NumberPlane,
    ReplacementTransform,
    RIGHT,
    Scene,
    VGroup,
    Write,
)

from engine.manim_instructional_widgets import ThemedText
from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME
from engine.vector_addition import VectorAddition
from engine.vector_addition_lesson import VECTOR_ADDITION_LESSON_SEQUENCE


FIRST_VECTOR = (3.0, 1.0)
SECOND_VECTOR = (1.0, 2.0)


class VectorAdditionPresentation(Scene):
    """Teach that vector addition follows successive displacements."""

    LESSON_SEQUENCE = VECTOR_ADDITION_LESSON_SEQUENCE
    THEME = SEEING_LINEAR_ALGEBRA_THEME
    LAYOUT = LessonLayout()

    def construct(self) -> None:
        title = ThemedText.lesson_title(
            "Vector Addition",
            theme=self.THEME,
        )
        self.LAYOUT.place_title(title)

        snapshot = VectorAddition(
            FIRST_VECTOR,
            SECOND_VECTOR,
        ).snapshot()
        assert snapshot.coefficients == (1.0, 1.0)
        assert snapshot.is_tip_to_tail

        plane = NumberPlane(
            x_range=[-1, 6, 1],
            y_range=[-1, 5, 1],
            x_length=6.4,
            y_length=5.0,
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
        plane.shift(LEFT * 2.15 + [0.0, -0.35, 0.0])

        origin = plane.c2p(*snapshot.resultant_segment[0])
        first_tip = plane.c2p(*snapshot.first_segment[1])
        second_tip = plane.c2p(*snapshot.second_vector)
        result_tip = plane.c2p(*snapshot.result)

        first_arrow = Arrow(
            origin,
            first_tip,
            buff=0.0,
            color=self.THEME.colors.geometry,
            stroke_width=6.0,
        )
        second_arrow = Arrow(
            origin,
            second_tip,
            buff=0.0,
            color=self.THEME.colors.application,
            stroke_width=6.0,
        )
        translated_second_arrow = Arrow(
            first_tip,
            result_tip,
            buff=0.0,
            color=self.THEME.colors.application,
            stroke_width=6.0,
        )
        resultant_arrow = Arrow(
            origin,
            result_tip,
            buff=0.0,
            color=self.THEME.colors.definition,
            stroke_width=7.0,
        )

        first_label = MathTex(r"\mathbf{u}", color=self.THEME.colors.geometry)
        first_label.next_to(first_arrow.get_center(), direction=[0.0, -1.0, 0.0])
        first_label.shift([0.0, 0.18, 0.0])

        second_label = MathTex(
            r"\mathbf{v}",
            color=self.THEME.colors.application,
        )
        second_label.next_to(second_arrow.get_center(), LEFT)

        translated_second_label = MathTex(
            r"\mathbf{v}",
            color=self.THEME.colors.application,
        )
        translated_second_label.next_to(
            translated_second_arrow.get_center(),
            RIGHT,
        )

        resultant_label = MathTex(
            r"\mathbf{u}+\mathbf{v}",
            color=self.THEME.colors.definition,
        ).scale(0.72)
        resultant_label.next_to(resultant_arrow.get_center(), RIGHT)

        prompt = ThemedText.guiding_question(
            "Where should the tail of the second vector begin?",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(prompt)

        successive_displacements = ThemedText.body(
            "Follow u first, then follow v.",
            theme=self.THEME,
        )
        successive_displacements.move_to([3.45, 1.65, 0.0])

        vector_data = VGroup(
            MathTex(
                r"\mathbf{u}=(3,1)",
                color=self.THEME.colors.geometry,
            ),
            MathTex(
                r"\mathbf{v}=(1,2)",
                color=self.THEME.colors.application,
            ),
        ).arrange([0.0, -1.0, 0.0], buff=0.20)
        vector_data.move_to([3.45, 0.65, 0.0])

        symbolic_sum = MathTex(
            r"\mathbf{u}+\mathbf{v}",
            color=self.THEME.colors.mathematics,
        ).scale(0.78)
        symbolic_sum.move_to([3.45, -0.45, 0.0])

        substituted_sum = MathTex(
            r"\mathbf{u}+\mathbf{v}=(3,1)+(1,2)",
            color=self.THEME.colors.mathematics,
        ).scale(0.70)
        substituted_sum.move_to(symbolic_sum)

        exact_sum = MathTex(
            r"\mathbf{u}+\mathbf{v}=(4,3)",
            color=self.THEME.colors.definition,
        ).scale(0.78)
        exact_sum.move_to(symbolic_sum)

        alternate_second = DashedLine(
            origin,
            second_tip,
            color=self.THEME.colors.narration,
            stroke_opacity=0.75,
        )
        alternate_first = DashedLine(
            second_tip,
            result_tip,
            color=self.THEME.colors.narration,
            stroke_opacity=0.75,
        )
        parallelogram = VGroup(alternate_second, alternate_first)

        parallelogram_caption = ThemedText.body(
            "The parallelogram gives the same endpoint.",
            theme=self.THEME,
        )
        parallelogram_caption.move_to([3.45, -1.55, 0.0])

        takeaway = VGroup(
            ThemedText.takeaway(
                "Vector addition combines successive displacements",
                theme=self.THEME,
            ).set_color(self.THEME.colors.definition),
            ThemedText.body(
                "The sum points from the starting point to the final endpoint.",
                theme=self.THEME,
            ),
        ).arrange([0.0, -1.0, 0.0], buff=0.16)
        self.LAYOUT.place_footer(takeaway)

        self.play(Write(title))
        self.play(FadeIn(plane))

        # ORIENT — both vectors begin in standard position.
        self.play(
            Create(first_arrow),
            FadeIn(first_label),
            Create(second_arrow),
            FadeIn(second_label),
            FadeIn(vector_data),
        )
        self.wait(self.THEME.timing.normal)

        # PREDICT
        self.play(FadeIn(prompt))
        self.wait(self.THEME.timing.read)
        self.play(FadeOut(prompt))

        # OBSERVE — move v without changing its magnitude or direction.
        self.play(
            FadeIn(successive_displacements),
            FadeIn(symbolic_sum),
        )
        self.play(
            ReplacementTransform(
                second_arrow,
                translated_second_arrow,
            ),
            ReplacementTransform(
                second_label,
                translated_second_label,
            ),
            ReplacementTransform(
                symbolic_sum,
                substituted_sum,
            ),
            run_time=1.8,
        )
        self.wait(self.THEME.timing.normal)

        # STABILIZE — the resultant and coordinate computation agree.
        self.play(
            Create(resultant_arrow),
            FadeIn(resultant_label),
            ReplacementTransform(
                substituted_sum,
                exact_sum,
            ),
        )
        self.wait(self.THEME.timing.read)

        # OBSERVE — reveal the parallelogram only after head-to-tail is clear.
        self.play(
            Create(alternate_second),
            Create(alternate_first),
            FadeIn(parallelogram_caption),
        )
        self.wait(self.THEME.timing.normal)

        # REFLECT
        self.play(
            FadeOut(successive_displacements),
            FadeOut(vector_data),
            FadeOut(exact_sum),
            FadeOut(parallelogram_caption),
            FadeOut(parallelogram),
            FadeIn(takeaway),
        )
        self.wait(self.THEME.timing.reflection)
