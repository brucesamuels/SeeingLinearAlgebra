"""Presentation scene: interpret vector subtraction as adding a negative."""

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
    PI,
    ReplacementTransform,
    RIGHT,
    Rotate,
    Scene,
    Transform,
    VGroup,
    Write,
)

from engine.manim_instructional_widgets import ThemedText
from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME
from engine.vector_subtraction import VectorSubtraction
from engine.vector_subtraction_lesson import VECTOR_SUBTRACTION_LESSON_SEQUENCE


MINUEND_VECTOR = (3.0, 1.0)
SUBTRAHEND_VECTOR = (1.0, 2.0)


class VectorSubtractionPresentation(Scene):
    """Show ``u - v`` by reversing and then adding ``v``."""

    LESSON_SEQUENCE = VECTOR_SUBTRACTION_LESSON_SEQUENCE
    THEME = SEEING_LINEAR_ALGEBRA_THEME
    LAYOUT = LessonLayout()

    def construct(self) -> None:
        title = ThemedText.lesson_title(
            "Vector Subtraction",
            theme=self.THEME,
        )
        self.LAYOUT.place_title(title)

        snapshot = VectorSubtraction(
            MINUEND_VECTOR,
            SUBTRAHEND_VECTOR,
        ).snapshot()

        assert snapshot.result == (2.0, -1.0)
        assert snapshot.negative_subtrahend == (-1.0, -2.0)
        assert snapshot.coefficients == (1.0, -1.0)
        assert snapshot.is_tip_to_tail
        assert snapshot.is_opposite_vector
        assert snapshot.preserves_magnitude

        plane = NumberPlane(
            x_range=[-2, 5, 1],
            y_range=[-3, 4, 1],
            x_length=6.2,
            y_length=5.2,
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
        u_tip = plane.c2p(*snapshot.minuend_vector)
        v_tip = plane.c2p(*snapshot.subtrahend_vector)
        negative_v_tip = plane.c2p(*snapshot.negative_subtrahend)
        result_tip = plane.c2p(*snapshot.result)

        u_arrow = Arrow(
            origin,
            u_tip,
            buff=0.0,
            color=self.THEME.colors.geometry,
            stroke_width=6.0,
        )
        v_arrow = Arrow(
            origin,
            v_tip,
            buff=0.0,
            color=self.THEME.colors.application,
            stroke_width=6.0,
        )
        negative_v_target = Arrow(
            origin,
            negative_v_tip,
            buff=0.0,
            color=self.THEME.colors.application,
            stroke_width=6.0,
        )
        translated_negative_target = Arrow(
            u_tip,
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
        endpoint = Dot(
            result_tip,
            color=self.THEME.colors.definition,
            radius=0.08,
        )

        u_label = MathTex(
            r"\mathbf{u}",
            color=self.THEME.colors.geometry,
        )
        u_label.next_to(u_arrow.get_center(), [0.0, -1.0, 0.0])
        u_label.shift([0.0, 0.18, 0.0])

        v_label = MathTex(
            r"\mathbf{v}",
            color=self.THEME.colors.application,
        )
        v_label.next_to(v_arrow.get_center(), LEFT)

        negative_v_label = MathTex(
            r"-\mathbf{v}",
            color=self.THEME.colors.application,
        )
        negative_v_label.next_to(negative_v_target.get_center(), LEFT)

        translated_negative_label = MathTex(
            r"-\mathbf{v}",
            color=self.THEME.colors.application,
        )
        translated_negative_label.next_to(
            translated_negative_target.get_center(),
            RIGHT,
        )

        resultant_label = MathTex(
            r"\mathbf{u}-\mathbf{v}",
            color=self.THEME.colors.definition,
        ).scale(0.72)
        resultant_label.next_to(
            resultant_arrow.get_center(),
            [0.0, -1.0, 0.0],
        )

        prompt = ThemedText.guiding_question(
            "How can subtraction be drawn using only vector addition?",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(prompt)

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
        vector_data.move_to([3.45, 1.45, 0.0])

        reverse_caption = ThemedText.body(
            "Reverse v without changing its length.",
            theme=self.THEME,
        )
        reverse_caption.move_to([3.45, 2.18, 0.0])

        translate_caption = ThemedText.body(
            "Now add -v at the tip of u.",
            theme=self.THEME,
        )
        translate_caption.move_to(reverse_caption)

        opposite_readout = VGroup(
            MathTex(
                r"-\mathbf{v}=(-1,-2)",
                color=self.THEME.colors.application,
            ),
            MathTex(
                r"\|-\mathbf{v}\|=\|\mathbf{v}\|",
                color=self.THEME.colors.mathematics,
            ).scale(0.78),
        ).arrange([0.0, -1.0, 0.0], buff=0.18)
        opposite_readout.move_to([3.45, 0.55, 0.0])

        symbolic_subtraction = MathTex(
            r"\mathbf{u}-\mathbf{v}",
            color=self.THEME.colors.mathematics,
        ).scale(0.80)
        symbolic_subtraction.move_to([3.45, -0.55, 0.0])

        addition_form = MathTex(
            r"\mathbf{u}+(-\mathbf{v})",
            color=self.THEME.colors.mathematics,
        ).scale(0.78)
        addition_form.move_to(symbolic_subtraction)

        substituted_form = MathTex(
            r"(3,1)+(-1,-2)",
            color=self.THEME.colors.mathematics,
        ).scale(0.72)
        substituted_form.move_to(symbolic_subtraction)

        exact_result = MathTex(
            r"\mathbf{u}-\mathbf{v}=(2,-1)",
            color=self.THEME.colors.definition,
        ).scale(0.74)
        exact_result.move_to(symbolic_subtraction)

        takeaway = VGroup(
            ThemedText.takeaway(
                "To subtract a vector, add its opposite",
                theme=self.THEME,
            ).set_color(self.THEME.colors.definition),
            ThemedText.body(
                "The opposite has the same magnitude and reverse direction.",
                theme=self.THEME,
            ),
        ).arrange([0.0, -1.0, 0.0], buff=0.16)
        self.LAYOUT.place_footer(takeaway)

        self.play(Write(title))
        self.play(FadeIn(plane))

        # ORIENT — u and v begin in standard position.
        self.play(
            Create(u_arrow),
            FadeIn(u_label),
            Create(v_arrow),
            FadeIn(v_label),
            FadeIn(vector_data),
            FadeIn(symbolic_subtraction),
        )
        self.wait(self.THEME.timing.normal)

        # PREDICT
        self.play(FadeIn(prompt))
        self.wait(self.THEME.timing.read)
        self.play(FadeOut(prompt))

        # OBSERVE — reverse v through the origin to create -v.
        self.play(FadeIn(reverse_caption))
        self.play(
            Rotate(v_arrow, angle=PI, about_point=origin),
            Transform(v_label, negative_v_label),
            ReplacementTransform(symbolic_subtraction, addition_form),
            run_time=1.6,
        )
        self.play(FadeIn(opposite_readout))
        self.wait(self.THEME.timing.normal)

        # OBSERVE — translate -v to the tip of u.
        moving_negative_v = v_arrow.copy()
        self.add(moving_negative_v)
        self.play(
            Transform(reverse_caption, translate_caption),
            v_arrow.animate.set_opacity(0.35),
            v_label.animate.set_opacity(0.35),
            Transform(moving_negative_v, translated_negative_target),
            FadeIn(translated_negative_label),
            ReplacementTransform(addition_form, substituted_form),
            run_time=1.6,
        )
        self.wait(self.THEME.timing.normal)

        # STABILIZE — draw the difference and finish the computation.
        self.play(
            Create(resultant_arrow),
            FadeIn(resultant_label),
            FadeIn(endpoint),
            ReplacementTransform(substituted_form, exact_result),
        )
        self.wait(self.THEME.timing.read)

        # REFLECT
        self.play(
            FadeOut(reverse_caption),
            FadeOut(vector_data),
            FadeOut(opposite_readout),
            FadeOut(exact_result),
            FadeIn(takeaway),
        )
        self.wait(self.THEME.timing.reflection)
