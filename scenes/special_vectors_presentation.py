"""Standalone Manim lesson introducing zero and unit vectors."""

from __future__ import annotations

from manim import (
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    NumberPlane,
    ORIGIN,
    ReplacementTransform,
    RIGHT,
    Rotate,
    Scene,
    TAU,
    Text,
    TracedPath,
    Transform,
    UP,
    VGroup,
    Write,
    linear,
)

from engine.manim_instructional_widgets import ThemedText
from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME
from engine.special_vectors_lesson import (
    SPECIAL_VECTORS_SNAPSHOT,
    SpecialVectorSnapshot,
)


class SpecialVectorsPresentation(Scene):
    """Introduce the zero vector and normalization to a unit vector."""

    SNAPSHOT: SpecialVectorSnapshot = SPECIAL_VECTORS_SNAPSHOT
    THEME = SEEING_LINEAR_ALGEBRA_THEME
    LAYOUT = LessonLayout()

    def construct(self) -> None:
        title = ThemedText.lesson_title(
            "Special Vectors",
            theme=self.THEME,
        )
        self.LAYOUT.place_title(title)

        opening = VGroup(
            ThemedText.body(
                "There are two special kinds of vectors.",
                theme=self.THEME,
            ),
            ThemedText.takeaway(
                "The zero vector and unit vectors",
                theme=self.THEME,
            ),
        ).arrange(direction=[0.0, -1.0, 0.0], buff=0.28)
        opening.move_to(ORIGIN)

        self.play(Write(title))
        self.play(FadeIn(opening))
        self.wait(self.THEME.timing.read)
        self.play(FadeOut(opening))

        plane = NumberPlane(
            x_range=[-4, 5, 1],
            y_range=[-3, 4, 1],
            x_length=8.1,
            y_length=5.4,
            background_line_style={
                "stroke_opacity": 0.28,
                "stroke_width": 1.0,
            },
        ).shift([0.0, -0.35, 0.0])
        origin = plane.c2p(0.0, 0.0)

        source_arrow = Arrow(
            origin,
            plane.c2p(*self.SNAPSHOT.source),
            buff=0.0,
        ).set_color(self.THEME.colors.geometry)

        source_label = MathTex(r"\mathbf v=(3,2)").scale(0.72)
        source_label.next_to(source_arrow.get_end(), UP, buff=0.32)
        source_label.shift(RIGHT * 0.22)

        self.play(Create(plane), Create(source_arrow), FadeIn(source_label))
        self.wait(self.THEME.timing.normal)

        zero_heading = ThemedText.guiding_question(
            "What happens when the length becomes zero?",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(zero_heading)

        collapsed_arrow = Arrow(
            origin,
            plane.c2p(1.0e-8, 1.0e-8),
            buff=0.0,
        ).set_color(self.THEME.colors.geometry)
        origin_dot = Dot(origin, radius=0.075).set_color(
            self.THEME.colors.geometry
        )
        zero_formula = MathTex(
            r"\mathbf 0=\begin{bmatrix}0\\0\end{bmatrix}",
        ).scale(0.78)
        self.LAYOUT.place_footer(zero_formula)

        self.play(FadeIn(zero_heading))
        self.play(
            Transform(source_arrow, collapsed_arrow),
            FadeOut(source_label),
            run_time=1.8,
        )
        self.play(FadeIn(origin_dot), Write(zero_formula))
        self.wait(self.THEME.timing.read)

        zero_takeaway = ThemedText.takeaway(
            "The zero vector is the only vector with length zero.",
            theme=self.THEME,
        )
        self.LAYOUT.place_footer(zero_takeaway)
        self.play(
            FadeOut(zero_heading),
            ReplacementTransform(zero_formula, zero_takeaway),
        )
        self.wait(self.THEME.timing.reflection)

        restored_arrow = Arrow(
            origin,
            plane.c2p(*self.SNAPSHOT.source),
            buff=0.0,
        ).set_color(self.THEME.colors.geometry)
        restored_label = MathTex(r"\mathbf v=(3,2)").scale(0.72)
        restored_label.next_to(restored_arrow.get_end(), UP, buff=0.32)
        restored_label.shift(RIGHT * 0.22)

        self.play(
            FadeOut(origin_dot),
            FadeOut(zero_takeaway),
            Transform(source_arrow, restored_arrow),
            FadeIn(restored_label),
            run_time=1.6,
        )

        magnitude_heading = ThemedText.guiding_question(
            "Computing the Magnitude",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(magnitude_heading)

        magnitude_formula = MathTex(
            r"\|\mathbf v\|=\sqrt{3^2+2^2}",
        ).scale(0.75)
        self.LAYOUT.place_footer(magnitude_formula)
        magnitude_exact = MathTex(
            r"\|\mathbf v\|=\sqrt{13}",
        ).scale(0.75)
        magnitude_exact.move_to(magnitude_formula)

        self.play(FadeIn(magnitude_heading), Write(magnitude_formula))
        self.play(
            ReplacementTransform(magnitude_formula, magnitude_exact),
        )
        self.wait(self.THEME.timing.normal)

        question = ThemedText.guiding_question(
            "Can we keep the direction but make the length exactly one?",
            theme=self.THEME,
        )
        self.LAYOUT.place_question(question)
        self.play(
            ReplacementTransform(magnitude_heading, question),
        )
        self.wait(self.THEME.timing.read)

        normalization_general = MathTex(
            r"\widehat{\mathbf v}=\frac{\mathbf v}{\|\mathbf v\|}",
        ).scale(0.78)
        self.LAYOUT.place_footer(normalization_general)
        normalization_substitution = MathTex(
            r"\widehat{\mathbf v}"
            r"=\frac{1}{\sqrt{13}}"
            r"\begin{bmatrix}3\\2\end{bmatrix}",
        ).scale(0.78)
        normalization_substitution.move_to(normalization_general)
        normalization_result = MathTex(
            r"\widehat{\mathbf v}"
            r"=\begin{bmatrix}3/\sqrt{13}\\2/\sqrt{13}\end{bmatrix}",
        ).scale(0.78)
        normalization_result.move_to(normalization_general)

        unit_radius = abs(plane.c2p(1.0, 0.0)[0] - origin[0])
        unit_circle = Circle(radius=unit_radius)
        unit_circle.move_to(origin)
        unit_circle.set_stroke(
            color=self.THEME.colors.geometry,
            width=2.0,
            opacity=0.45,
        )

        unit_arrow = Arrow(
            origin,
            plane.c2p(*self.SNAPSHOT.unit),
            buff=0.0,
        ).set_color(self.THEME.colors.geometry)

        self.play(
            FadeOut(magnitude_exact),
            FadeOut(question),
            Write(normalization_general),
            Create(unit_circle),
        )
        self.play(
            ReplacementTransform(
                normalization_general,
                normalization_substitution,
            ),
        )
        self.play(
            Transform(source_arrow, unit_arrow),
            ReplacementTransform(
                normalization_substitution,
                normalization_result,
            ),
            Transform(
                restored_label,
                MathTex(r"\widehat{\mathbf v}").scale(0.72).next_to(
                    unit_arrow.get_end(),
                    RIGHT,
                    buff=0.12,
                ),
            ),
            run_time=2.2,
        )

        unit_magnitude = MathTex(
            r"\|\widehat{\mathbf v}\|=1",
        ).scale(0.82)
        unit_magnitude.move_to(normalization_result)
        self.play(
            ReplacementTransform(normalization_result, unit_magnitude),
        )
        self.wait(self.THEME.timing.reflection)

        self.play(
            FadeOut(plane),
            FadeOut(unit_magnitude),
            FadeOut(title),
        )

        path = TracedPath(
            source_arrow.get_end,
            stroke_color=self.THEME.colors.geometry,
            stroke_width=2.5,
            dissipating_time=None,
        )
        self.add(path)
        self.play(
            Rotate(
                source_arrow,
                angle=TAU,
                about_point=origin,
                rate_func=linear,
            ),
            Rotate(
                restored_label,
                angle=TAU,
                about_point=origin,
                rate_func=linear,
            ),
            run_time=5.0,
        )

        circle_statement = ThemedText.takeaway(
            "Every point on this circle is a unit vector.",
            theme=self.THEME,
        )
        circle_statement.to_edge(UP, buff=0.5)
        self.play(FadeIn(circle_statement))
        self.wait(self.THEME.timing.reflection)

        closing = VGroup(
            Text("A unit vector keeps the direction...", font_size=34),
            Text("...but standardizes the length.", font_size=34),
        ).arrange(direction=[0.0, -1.0, 0.0], buff=0.24)
        closing.to_edge(UP, buff=0.45)

        self.play(
            FadeOut(circle_statement),
            FadeOut(path),
            FadeIn(closing),
        )
        self.wait(self.THEME.timing.reflection)
