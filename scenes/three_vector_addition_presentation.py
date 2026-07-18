"""Presentation scene: add three vectors in 3-space with a parallelepiped."""

from __future__ import annotations

from manim import (
    Arrow3D,
    Create,
    DEGREES,
    FadeOut,
    Line3D,
    MathTex,
    ReplacementTransform,
    ThreeDAxes,
    ThreeDScene,
    VGroup,
)

from engine.manim_instructional_widgets import ThemedText
from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME
from engine.three_vector_addition import ThreeVectorAddition
from engine.three_vector_addition_lesson import (
    THREE_VECTOR_ADDITION_LESSON_SEQUENCE,
)


FIRST_VECTOR_3D = (3.0, 0.0, 1.0)
SECOND_VECTOR_3D = (0.0, 3.0, 1.0)
THIRD_VECTOR_3D = (1.0, 1.0, 3.0)


class ThreeVectorAdditionPresentation(ThreeDScene):
    """Teach three-vector addition in 3-space via a parallelepiped."""

    LESSON_SEQUENCE = THREE_VECTOR_ADDITION_LESSON_SEQUENCE
    THEME = SEEING_LINEAR_ALGEBRA_THEME
    LAYOUT = LessonLayout()

    def _register_fixed_frame_hidden(self, *mobjects) -> None:
        for mobject in mobjects:
            mobject.set_opacity(0.0)
        self.add_fixed_in_frame_mobjects(*mobjects)

    def _register_fixed_orientation_hidden(self, *mobjects) -> None:
        for mobject in mobjects:
            mobject.set_opacity(0.0)
        self.add_fixed_orientation_mobjects(*mobjects)

    def construct(self) -> None:
        title = ThemedText.lesson_title(
            'Three Vectors in 3-Space',
            theme=self.THEME,
        )
        self.LAYOUT.place_title(title)

        snapshot = ThreeVectorAddition(
            FIRST_VECTOR_3D,
            SECOND_VECTOR_3D,
            THIRD_VECTOR_3D,
        ).snapshot()
        assert snapshot.dimension == 3
        assert snapshot.coefficients == (1.0, 1.0, 1.0)
        assert snapshot.is_successive_path
        assert snapshot.result == (4.0, 4.0, 5.0)

        prompt = ThemedText.guiding_question(
            'After u, where should the tails of v and w go?',
            theme=self.THEME,
        )
        self.LAYOUT.place_question(prompt)

        narrative = ThemedText.body(
            'Follow u, then v, then w.',
            theme=self.THEME,
        )
        narrative.move_to([3.95, 1.70, 0.0])

        vector_data = VGroup(
            MathTex(r'\mathbf{u}=(3,0,1)', color=self.THEME.colors.geometry),
            MathTex(r'\mathbf{v}=(0,3,1)', color=self.THEME.colors.application),
            MathTex(r'\mathbf{w}=(1,1,3)', color=self.THEME.colors.definition),
        ).arrange([0.0, -1.0, 0.0], buff=0.16)
        vector_data.move_to([4.2, 0.65, 0.0])

        symbolic_sum = MathTex(
            r'\mathbf{u}+\mathbf{v}+\mathbf{w}',
            color=self.THEME.colors.mathematics,
        ).scale(0.76)
        symbolic_sum.move_to([4.2, -0.35, 0.0])

        substituted_sum = MathTex(
            r'\mathbf{u}+\mathbf{v}+\mathbf{w}=(3,0,1)+(0,3,1)+(1,1,3)',
            color=self.THEME.colors.mathematics,
        ).scale(0.56)
        substituted_sum.move_to(symbolic_sum)

        exact_sum = MathTex(
            r'\mathbf{u}+\mathbf{v}+\mathbf{w}=(4,4,5)',
            color=self.THEME.colors.definition,
        ).scale(0.74)
        exact_sum.move_to(symbolic_sum)

        parallelepiped_caption = ThemedText.body(
            'The sum is the body diagonal to the opposite corner.',
            theme=self.THEME,
        )
        parallelepiped_caption.move_to([4.2, -1.35, 0.0])

        takeaway = VGroup(
            ThemedText.takeaway(
                'The sum is the body diagonal of the parallelepiped',
                theme=self.THEME,
            ).set_color(self.THEME.colors.definition),
            ThemedText.body(
                'Following u, then v, then w reaches the opposite corner.',
                theme=self.THEME,
            ),
        ).arrange([0.0, -1.0, 0.0], buff=0.16)
        self.LAYOUT.place_footer(takeaway)

        self._register_fixed_frame_hidden(
            title,
            prompt,
            narrative,
            vector_data,
            symbolic_sum,
            parallelepiped_caption,
            takeaway,
        )

        axes = ThreeDAxes(
            x_range=[-1, 6, 1],
            y_range=[-1, 6, 1],
            z_range=[-1, 7, 1],
            x_length=5.4,
            y_length=5.4,
            z_length=5.8,
        )
        axes.shift([-2.20, -1.85, -1.20])

        origin = axes.c2p(*snapshot.resultant_segment[0])
        first_tip = axes.c2p(*snapshot.first_segment[1])
        second_standard_tip = axes.c2p(*snapshot.second_vector)
        second_tip = axes.c2p(*snapshot.second_segment[1])
        third_standard_tip = axes.c2p(*snapshot.third_vector)
        result_tip = axes.c2p(*snapshot.result)

        first_arrow = Arrow3D(
            start=origin,
            end=first_tip,
            color=self.THEME.colors.geometry,
            thickness=0.02,
        )
        second_arrow = Arrow3D(
            start=origin,
            end=second_standard_tip,
            color=self.THEME.colors.application,
            thickness=0.02,
        )
        third_arrow = Arrow3D(
            start=origin,
            end=third_standard_tip,
            color=self.THEME.colors.definition,
            thickness=0.02,
        )

        translated_second_arrow = Arrow3D(
            start=first_tip,
            end=second_tip,
            color=self.THEME.colors.application,
            thickness=0.02,
        )
        translated_third_arrow = Arrow3D(
            start=second_tip,
            end=result_tip,
            color=self.THEME.colors.definition,
            thickness=0.02,
        )
        resultant_arrow = Arrow3D(
            start=origin,
            end=result_tip,
            color=self.THEME.colors.definition,
            thickness=0.024,
        )

        first_label = MathTex(r'\mathbf{u}', color=self.THEME.colors.geometry)
        first_label.move_to(axes.c2p(1.5, -0.1, 0.55))
        second_label = MathTex(r'\mathbf{v}', color=self.THEME.colors.application)
        second_label.move_to(axes.c2p(0.10, 1.5, 0.65))
        third_label = MathTex(r'\mathbf{w}', color=self.THEME.colors.definition)
        third_label.move_to(axes.c2p(0.75, 0.75, 1.70))
        translated_second_label = MathTex(
            r'\mathbf{v}', color=self.THEME.colors.application
        )
        translated_second_label.move_to(axes.c2p(3.0, 1.45, 1.55))
        translated_third_label = MathTex(
            r'\mathbf{w}', color=self.THEME.colors.definition
        )
        translated_third_label.move_to(axes.c2p(3.45, 3.20, 3.30))
        resultant_label = MathTex(
            r'\mathbf{u}+\mathbf{v}+\mathbf{w}',
            color=self.THEME.colors.definition,
        ).scale(0.70)
        resultant_label.move_to(axes.c2p(2.15, 2.05, 2.50))

        self._register_fixed_orientation_hidden(
            first_label,
            second_label,
            third_label,
            resultant_label,
        )

        parallelepiped_edges = VGroup(
            *[
                Line3D(
                    start=axes.c2p(*start),
                    end=axes.c2p(*end),
                    color=self.THEME.colors.narration,
                    thickness=0.01,
                )
                for start, end in snapshot.parallelepiped_edges
            ]
        )

        self.set_camera_orientation(phi=74 * DEGREES, theta=-58 * DEGREES)

        self.play(title.animate.set_opacity(1.0))
        self.play(Create(axes))

        # ORIENT — all three vectors begin in standard position.
        self.play(
            Create(first_arrow),
            first_label.animate.set_opacity(1.0),
            Create(second_arrow),
            second_label.animate.set_opacity(1.0),
            Create(third_arrow),
            third_label.animate.set_opacity(1.0),
            vector_data.animate.set_opacity(1.0),
        )
        self.wait(self.THEME.timing.normal)

        # PREDICT
        self.play(prompt.animate.set_opacity(1.0))
        self.wait(self.THEME.timing.read)
        self.play(prompt.animate.set_opacity(0.0))

        # OBSERVE — translate v, then w, preserving each vector.
        self.play(
            narrative.animate.set_opacity(1.0),
            symbolic_sum.animate.set_opacity(1.0),
        )
        self.play(
            ReplacementTransform(second_arrow, translated_second_arrow),
            ReplacementTransform(second_label, translated_second_label),
            run_time=1.5,
        )
        self.play(
            ReplacementTransform(third_arrow, translated_third_arrow),
            ReplacementTransform(third_label, translated_third_label),
            ReplacementTransform(symbolic_sum, substituted_sum),
            run_time=1.6,
        )
        self.wait(self.THEME.timing.normal)

        # STABILIZE
        self.play(
            Create(resultant_arrow),
            resultant_label.animate.set_opacity(1.0),
            ReplacementTransform(substituted_sum, exact_sum),
        )
        self.wait(self.THEME.timing.read)

        # OBSERVE — reveal the parallelepiped and keep it visible with the diagonal.
        self.play(
            Create(parallelepiped_edges),
            parallelepiped_caption.animate.set_opacity(1.0),
        )
        self.begin_ambient_camera_rotation(rate=0.18)
        self.wait(1.8)
        self.stop_ambient_camera_rotation()

        # REFLECT — keep the diagonal and parallelepiped visible.
        self.play(
            FadeOut(narrative),
            FadeOut(vector_data),
            FadeOut(parallelepiped_caption),
            takeaway.animate.set_opacity(1.0),
        )
        self.wait(self.THEME.timing.reflection)
