"""Standalone cinematic introduction to families of linear combinations."""

from __future__ import annotations

from math import cos, sin, sqrt

from manim import (
    Arrow,
    Create,
    DecimalNumber,
    DOWN,
    FadeIn,
    FadeOut,
    MathTex,
    NumberPlane,
    ORIGIN,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    Scene,
    TracedPath,
    UP,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
    linear,
)

from engine.coefficient_choreography import (
    CoefficientChoreography,
    selected_story_coefficients,
)
from engine.linear_combination import LinearCombination
from engine.manim_instructional_widgets import ThemedText
from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME


class InfinitePossibilitiesPresentation(Scene):
    """Let one continuously changing linear combination explore the plane."""

    THEME = SEEING_LINEAR_ALGEBRA_THEME
    LAYOUT = LessonLayout()

    U = (2.0, 0.5)
    V = (0.5, 1.5)
    LINEAR_COMBINATION = LinearCombination((U, V))
    STORY = CoefficientChoreography(
        LINEAR_COMBINATION,
        selected_story_coefficients(),
    )

    @staticmethod
    def coefficient_pair(time_value: float) -> tuple[float, float]:
        """Return smooth, nonrepeating-looking coefficients.

        The irrational frequency ratio prevents a short closed orbit, while
        the slowly increasing amplitude lets the resultant explore farther
        and farther from the origin.
        """

        amplitude = 0.85 + 0.045 * time_value
        a_value = amplitude * sin(time_value)
        b_value = amplitude * cos(sqrt(2.0) * time_value)
        return a_value, b_value

    def construct(self) -> None:
        title = ThemedText.lesson_title(
            "Infinite Possibilities",
            theme=self.THEME,
        )
        self.LAYOUT.place_title(title)

        question = ThemedText.guiding_question(
            "What happens when we combine both vector operations?",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(question)

        operations = VGroup(
            MathTex(r"a\mathbf u"),
            MathTex(r"+"),
            MathTex(r"b\mathbf v"),
        ).arrange(RIGHT, buff=0.28)
        operations.move_to(ORIGIN)

        self.play(Write(title))
        self.play(FadeIn(question), FadeIn(operations))
        self.wait(self.THEME.timing.read)

        formula = MathTex(r"a\mathbf u+b\mathbf v").scale(1.05)
        formula.move_to(operations)
        definition = ThemedText.takeaway(
            "This is called a linear combination.",
            theme=self.THEME,
        )
        self.LAYOUT.place_footer(definition)

        self.play(
            ReplacementTransform(operations, formula),
            FadeIn(definition),
        )
        self.wait(self.THEME.timing.reflection)
        self.play(FadeOut(question), FadeOut(definition))

        plane = NumberPlane(
            x_range=[-7, 8, 1],
            y_range=[-5, 6, 1],
            x_length=10.5,
            y_length=6.2,
            background_line_style={
                "stroke_opacity": 0.20,
                "stroke_width": 0.8,
            },
        ).shift(DOWN * 0.35)
        origin = plane.c2p(0.0, 0.0)

        u_arrow = Arrow(origin, plane.c2p(*self.U), buff=0.0)
        u_arrow.set_color(self.THEME.colors.geometry)
        v_arrow = Arrow(origin, plane.c2p(*self.V), buff=0.0)
        v_arrow.set_color(self.THEME.colors.reflection)

        u_label = MathTex(r"\mathbf u").scale(0.65)
        u_label.next_to(u_arrow.get_end(), RIGHT, buff=0.12)
        v_label = MathTex(r"\mathbf v").scale(0.65)
        v_label.next_to(v_arrow.get_end(), UP, buff=0.12)

        self.play(
            Create(plane),
            Create(u_arrow),
            Create(v_arrow),
            FadeIn(u_label),
            FadeIn(v_label),
            formula.animate.scale(0.70).to_edge(UP, buff=1.05),
        )

        sample_heading = ThemedText.guiding_question(
            "Every coefficient pair creates another vector.",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(sample_heading)
        self.play(FadeIn(sample_heading))

        active_arrow = None
        active_readout = None

        for sample in self.STORY:
            a_value, b_value = sample.coefficients
            x_value, y_value = sample.snapshot.result
            next_arrow = Arrow(
                origin,
                plane.c2p(float(x_value), float(y_value)),
                buff=0.0,
            ).set_color(self.THEME.colors.example)
            next_readout = MathTex(
                rf"a={a_value:g},\quad b={b_value:g}",
            ).scale(0.60)
            self.LAYOUT.place_footer(next_readout)

            if active_arrow is None:
                self.play(
                    Create(next_arrow),
                    FadeIn(next_readout),
                    run_time=0.75,
                )
            else:
                self.play(
                    ReplacementTransform(active_arrow, next_arrow),
                    ReplacementTransform(active_readout, next_readout),
                    run_time=0.60,
                )
            active_arrow = next_arrow
            active_readout = next_readout

        living_heading = ThemedText.guiding_question(
            "Now let the coefficients change continuously.",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(living_heading)
        self.play(
            ReplacementTransform(sample_heading, living_heading),
            FadeOut(active_arrow),
            FadeOut(active_readout),
        )

        time_tracker = ValueTracker(0.0)

        def current_coefficients() -> tuple[float, float]:
            return self.coefficient_pair(time_tracker.get_value())

        def current_result() -> tuple[float, float]:
            coefficients = current_coefficients()
            snapshot = self.LINEAR_COMBINATION.snapshot(coefficients)
            return (
                float(snapshot.result[0]),
                float(snapshot.result[1]),
            )

        moving_arrow = always_redraw(
            lambda: Arrow(
                origin,
                plane.c2p(*current_result()),
                buff=0.0,
            ).set_color(self.THEME.colors.example)
        )

        endpoint = always_redraw(
            lambda: MathTex(r"\bullet")
            .scale(0.55)
            .set_color(self.THEME.colors.mathematics)
            .move_to(plane.c2p(*current_result()))
        )

        a_number = DecimalNumber(
            0.0,
            num_decimal_places=2,
            include_sign=True,
        ).scale(0.56)
        b_number = DecimalNumber(
            0.0,
            num_decimal_places=2,
            include_sign=True,
        ).scale(0.56)

        a_number.add_updater(
            lambda number: number.set_value(current_coefficients()[0])
        )
        b_number.add_updater(
            lambda number: number.set_value(current_coefficients()[1])
        )

        live_readout = VGroup(
            MathTex("a=").scale(0.56),
            a_number,
            MathTex(r",\qquad b=").scale(0.56),
            b_number,
        ).arrange(RIGHT, buff=0.08)
        self.LAYOUT.place_footer(live_readout)

        trail = TracedPath(
            endpoint.get_center,
            stroke_color=self.THEME.colors.mathematics,
            stroke_width=2.2,
            stroke_opacity=0.48,
            dissipating_time=None,
        )

        self.add(trail, moving_arrow, endpoint)
        self.play(FadeIn(live_readout))

        self.play(
            time_tracker.animate.set_value(22.0),
            run_time=7.0,
            rate_func=linear,
        )

        farther_heading = ThemedText.guiding_question(
            "As the coefficients grow, the vector explores farther.",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(farther_heading)
        self.play(
            ReplacementTransform(living_heading, farther_heading),
        )

        self.play(
            time_tracker.animate.set_value(52.0),
            run_time=9.0,
            rate_func=linear,
        )

        self.play(
            FadeOut(moving_arrow),
            FadeOut(endpoint),
            FadeOut(live_readout),
            FadeOut(farther_heading),
        )
        self.wait(self.THEME.timing.normal)

        trail_statement = ThemedText.takeaway(
            "Every point on this trail came from one choice of coefficients.",
            theme=self.THEME,
        )
        self.LAYOUT.place_footer(trail_statement)
        self.play(FadeIn(trail_statement))
        self.wait(self.THEME.timing.reflection)

        possibility_question = ThemedText.guiding_question(
            "What if a and b can be any real numbers?",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(possibility_question)
        self.play(
            FadeOut(trail_statement),
            FadeIn(possibility_question),
        )
        self.wait(self.THEME.timing.read)

        plane_wash = Rectangle(
            width=plane.width,
            height=plane.height,
            stroke_width=0.0,
            fill_color=self.THEME.colors.mathematics,
            fill_opacity=0.18,
        ).move_to(plane)

        all_of_it = ThemedText.takeaway(
            "All of it.",
            theme=self.THEME,
        )
        self.LAYOUT.place_footer(all_of_it)

        self.play(
            FadeOut(trail),
            FadeIn(plane_wash),
            FadeOut(possibility_question),
            FadeIn(all_of_it),
            run_time=1.8,
        )
        self.wait(self.THEME.timing.reflection * 1.4)

        closing = VGroup(
            ThemedText.body(
                "Today we learned how to create one vector.",
                theme=self.THEME,
            ),
            ThemedText.takeaway(
                "Next, we study all the vectors we can create.",
                theme=self.THEME,
            ),
        ).arrange(DOWN, buff=0.32)
        closing.move_to(ORIGIN)

        self.play(
            FadeOut(plane),
            FadeOut(plane_wash),
            FadeOut(formula),
            FadeOut(all_of_it),
            FadeOut(title),
            FadeOut(u_arrow),
            FadeOut(v_arrow),
            FadeOut(u_label),
            FadeOut(v_label),
            FadeIn(closing),
        )
        self.wait(self.THEME.timing.reflection * 1.6)
