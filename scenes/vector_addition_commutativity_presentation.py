"""Presentation scene: show why vector addition is commutative."""

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
    RIGHT,
    Scene,
    Transform,
    VGroup,
    Write,
)

from engine.manim_instructional_widgets import ThemedText
from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME
from engine.vector_addition import VectorAddition
from engine.vector_addition_commutativity_lesson import (
    VECTOR_ADDITION_COMMUTATIVITY_LESSON_SEQUENCE,
)


FIRST_VECTOR = (3.0, 1.0)
SECOND_VECTOR = (1.0, 2.0)


class VectorAdditionCommutativityPresentation(Scene):
    """Compare u + v and v + u as two routes to one endpoint."""

    LESSON_SEQUENCE = VECTOR_ADDITION_COMMUTATIVITY_LESSON_SEQUENCE
    THEME = SEEING_LINEAR_ALGEBRA_THEME
    LAYOUT = LessonLayout()

    def construct(self) -> None:
        title = ThemedText.lesson_title(
            "Commutativity of Vector Addition",
            theme=self.THEME,
        )
        self.LAYOUT.place_title(title)

        uv_snapshot = VectorAddition(
            FIRST_VECTOR,
            SECOND_VECTOR,
        ).snapshot()
        vu_snapshot = VectorAddition(
            SECOND_VECTOR,
            FIRST_VECTOR,
        ).snapshot()

        assert uv_snapshot.result == vu_snapshot.result
        assert uv_snapshot.result == (4.0, 3.0)
        assert uv_snapshot.is_tip_to_tail
        assert vu_snapshot.is_tip_to_tail

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

        origin = plane.c2p(*uv_snapshot.resultant_segment[0])
        u_tip = plane.c2p(*uv_snapshot.first_vector)
        v_tip = plane.c2p(*uv_snapshot.second_vector)
        sum_tip = plane.c2p(*uv_snapshot.result)

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

        v_after_u_target = Arrow(
            u_tip,
            sum_tip,
            buff=0.0,
            color=self.THEME.colors.application,
            stroke_width=6.0,
        )
        u_after_v_target = Arrow(
            v_tip,
            sum_tip,
            buff=0.0,
            color=self.THEME.colors.geometry,
            stroke_width=6.0,
        )
        resultant_arrow = Arrow(
            origin,
            sum_tip,
            buff=0.0,
            color=self.THEME.colors.definition,
            stroke_width=7.0,
        )
        endpoint = Dot(
            sum_tip,
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

        v_after_u_label = MathTex(
            r"\mathbf{v}",
            color=self.THEME.colors.application,
        )
        v_after_u_label.next_to(
            v_after_u_target.get_center(),
            RIGHT,
        )

        u_after_v_label = MathTex(
            r"\mathbf{u}",
            color=self.THEME.colors.geometry,
        )
        u_after_v_label.next_to(
            u_after_v_target.get_center(),
            RIGHT,
        )

        resultant_label = MathTex(
            r"\mathbf{u}+\mathbf{v}",
            color=self.THEME.colors.definition,
        ).scale(0.72)
        resultant_label.next_to(
            resultant_arrow.get_center(),
            RIGHT,
        )

        prompt = ThemedText.guiding_question(
            "What changes if we add the vectors in the opposite order?",
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
        vector_data.move_to([3.45, 1.30, 0.0])

        uv_readout = MathTex(
            r"\mathbf{u}+\mathbf{v}=(4,3)",
            color=self.THEME.colors.mathematics,
        ).scale(0.72)
        uv_readout.move_to([3.45, 0.20, 0.0])

        vu_readout = MathTex(
            r"\mathbf{v}+\mathbf{u}=(4,3)",
            color=self.THEME.colors.mathematics,
        ).scale(0.72)
        vu_readout.move_to([3.45, -0.55, 0.0])

        commutative_equation = MathTex(
            r"\mathbf{u}+\mathbf{v}=\mathbf{v}+\mathbf{u}",
            color=self.THEME.colors.definition,
        ).scale(0.78)
        commutative_equation.move_to([3.45, -1.35, 0.0])

        first_route_caption = ThemedText.body(
            "First route: follow u, then v.",
            theme=self.THEME,
        )
        first_route_caption.move_to([3.45, 2.10, 0.0])

        second_route_caption = ThemedText.body(
            "Second route: follow v, then u.",
            theme=self.THEME,
        )
        second_route_caption.move_to(first_route_caption)

        takeaway = VGroup(
            ThemedText.takeaway(
                "Changing the order changes the path, but not the sum",
                theme=self.THEME,
            ).set_color(self.THEME.colors.definition),
            ThemedText.body(
                "Both routes reach the same opposite corner.",
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
        )
        self.wait(self.THEME.timing.normal)

        # PREDICT
        self.play(FadeIn(prompt))
        self.wait(self.THEME.timing.read)
        self.play(FadeOut(prompt))

        # OBSERVE — construct u + v.
        moving_v = v_arrow.copy()
        self.add(moving_v)
        self.play(
            FadeIn(first_route_caption),
            Transform(moving_v, v_after_u_target),
            FadeIn(v_after_u_label),
            run_time=1.6,
        )
        self.play(
            Create(resultant_arrow),
            FadeIn(resultant_label),
            FadeIn(endpoint),
            FadeIn(uv_readout),
        )
        self.wait(self.THEME.timing.normal)

        # OBSERVE — reverse the order and construct v + u.
        moving_u = u_arrow.copy()
        self.add(moving_u)
        self.play(
            Transform(first_route_caption, second_route_caption),
            Transform(moving_u, u_after_v_target),
            FadeIn(u_after_v_label),
            FadeIn(vu_readout),
            run_time=1.6,
        )
        self.wait(self.THEME.timing.normal)

        # STABILIZE — the four colored edges now form the parallelogram.
        self.play(FadeIn(commutative_equation))
        self.wait(self.THEME.timing.read)

        # REFLECT
        self.play(
            FadeOut(first_route_caption),
            FadeOut(vector_data),
            FadeOut(uv_readout),
            FadeOut(vu_readout),
            FadeOut(commutative_equation),
            FadeIn(takeaway),
        )
        self.wait(self.THEME.timing.reflection)
