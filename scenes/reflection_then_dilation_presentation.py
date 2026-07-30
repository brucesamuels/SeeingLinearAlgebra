"""CP84: Reflection Before or After Dilation."""
from __future__ import annotations

import numpy as np
from manim import *

from engine.reflection_dilation_commutativity import evaluate_reflection_dilation


class ReflectionThenDilationPresentation(Scene):
    """Compare reflection-then-dilation with dilation-then-reflection."""

    def construct(self) -> None:
        title = Text("Reflection Before or After Dilation?", font_size=40).to_edge(UP)
        subtitle = Text(
            "Two different routes — one final vector.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.15)

        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(1.0)

        plane = NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            x_length=8.4,
            y_length=5.4,
            background_line_style={"stroke_opacity": 0.28},
        ).shift(DOWN * 0.38)

        snapshot = evaluate_reflection_dilation()
        mirror_line = self._mirror_line(plane, snapshot.line_angle)
        mirror_label = MathTex(r"m", font_size=30).next_to(
            mirror_line.get_end(), UP + LEFT, buff=0.10
        )

        origin = Dot(plane.c2p(0, 0), radius=0.07, color=RED)

        self.play(Create(plane), Create(mirror_line), FadeIn(mirror_label), FadeIn(origin))

        original = self._arrow(plane, np.zeros(2), snapshot.vector, BLUE)
        original_label = MathTex(r"\mathbf{v}", font_size=31, color=BLUE).next_to(
            original.get_end(), RIGHT, buff=0.09
        )

        self.play(GrowArrow(original), FadeIn(original_label))
        self.wait(0.8)

        prompt = VGroup(
            Text("Pause and Predict", font_size=30, color=YELLOW),
            Text(
                "Will the order of reflection and dilation matter?",
                font_size=24,
            ),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN).shift(UP * 0.08)

        self.play(FadeIn(prompt))
        self.wait(2.0)
        self.play(FadeOut(prompt))

        # CP84.1: retain a reference to the complete first route so every faded
        # remnant can be removed before the final explanatory card.
        self.route_a = self._show_reflect_then_dilate(
            plane, snapshot, original, original_label
        )
        self._reset_to_original(self.route_a, original, original_label)

        route_b = self._show_dilate_then_reflect(
            plane, snapshot, original, original_label
        )
        self._show_coincidence(plane, snapshot, route_b)
        self._show_homogeneity_statement(
            plane,
            mirror_line,
            mirror_label,
            origin,
            original,
            original_label,
            route_b,
        )

    def _point(self, plane: NumberPlane, vector: np.ndarray) -> np.ndarray:
        return plane.c2p(float(vector[0]), float(vector[1]))

    def _arrow(self, plane, start, end, color, width=5) -> Arrow:
        return Arrow(
            self._point(plane, start),
            self._point(plane, end),
            buff=0,
            color=color,
            stroke_width=width,
            max_tip_length_to_length_ratio=0.16,
        )

    def _mirror_line(self, plane, angle: float) -> Line:
        direction = np.array([np.cos(angle), np.sin(angle)])
        start = -4.5 * direction
        end = 4.5 * direction
        return Line(
            self._point(plane, start),
            self._point(plane, end),
            color=WHITE,
            stroke_width=4,
        )

    def _route_heading(self, tex: str, caption: str) -> VGroup:
        group = VGroup(
            MathTex(tex, font_size=34),
            Text(caption, font_size=23),
        ).arrange(DOWN, buff=0.10)
        return group.to_corner(LEFT + UP).shift(RIGHT * 0.35 + DOWN * 1.28)

    def _show_reflect_then_dilate(self, plane, s, original, original_label):
        heading = self._route_heading(
            r"D_c\!\left(r_m(\mathbf{v})\right)",
            "Path A: reflect first, then dilate.",
        )
        self.play(FadeIn(heading))

        reflected = self._arrow(plane, np.zeros(2), s.reflected, GREEN)
        reflected_label = MathTex(
            r"r_m(\mathbf{v})", font_size=29, color=GREEN
        ).next_to(reflected.get_end(), LEFT, buff=0.10)

        self.play(
            TransformFromCopy(original, reflected),
            FadeIn(reflected_label),
        )
        self.wait(0.9)

        final_a = self._arrow(
            plane, np.zeros(2), s.reflect_then_dilate, YELLOW, width=7
        )
        final_a_label = MathTex(
            r"c\,r_m(\mathbf{v})",
            font_size=30,
            color=YELLOW,
        ).next_to(final_a.get_end(), LEFT + UP, buff=0.10)

        ray = DashedLine(
            self._point(plane, np.zeros(2)),
            self._point(plane, 1.12 * s.reflect_then_dilate),
            color=GREEN,
            stroke_opacity=0.45,
        )

        self.play(Create(ray))
        self.play(
            ReplacementTransform(reflected, final_a),
            Transform(reflected_label, final_a_label),
        )
        self.wait(1.2)

        return VGroup(heading, final_a, reflected_label, ray)

    def _reset_to_original(self, route_a, original, original_label) -> None:
        route_a[1:].set_opacity(0.23)
        reset_note = Text(
            "Reset to the original vector.",
            font_size=24,
            color=GREY_B,
        ).to_edge(DOWN).shift(UP * 0.10)
        self.play(FadeIn(reset_note))
        self.wait(0.7)
        self.play(FadeOut(reset_note), FadeOut(route_a[0]))

    def _show_dilate_then_reflect(self, plane, s, original, original_label):
        heading = self._route_heading(
            r"r_m\!\left(D_c(\mathbf{v})\right)",
            "Path B: dilate first, then reflect.",
        )
        self.play(FadeIn(heading))

        dilated = self._arrow(plane, np.zeros(2), s.dilated, ORANGE)
        dilated_label = MathTex(
            r"c\mathbf{v}", font_size=30, color=ORANGE
        ).next_to(dilated.get_end(), RIGHT, buff=0.10)

        original_ray = DashedLine(
            self._point(plane, np.zeros(2)),
            self._point(plane, 1.10 * s.dilated),
            color=BLUE,
            stroke_opacity=0.42,
        )

        self.play(Create(original_ray))
        self.play(
            TransformFromCopy(original, dilated),
            FadeIn(dilated_label),
        )
        self.wait(0.9)

        final_b = self._arrow(
            plane, np.zeros(2), s.dilate_then_reflect, ORANGE, width=7
        )
        final_b_label = MathTex(
            r"r_m(c\mathbf{v})",
            font_size=30,
            color=ORANGE,
        ).next_to(final_b.get_end(), RIGHT + DOWN, buff=0.10)

        self.play(
            ReplacementTransform(dilated, final_b),
            Transform(dilated_label, final_b_label),
        )
        self.wait(1.2)

        return VGroup(heading, final_b, dilated_label, original_ray)

    def _show_coincidence(self, plane, s, route_b) -> None:
        endpoint = Dot(
            self._point(plane, s.dilate_then_reflect),
            radius=0.09,
            color=WHITE,
        )
        agreement = Text(
            "The two paths land at the same point.",
            font_size=28,
            color=GREEN,
        ).to_edge(DOWN).shift(UP * 0.10)

        self.play(
            Flash(endpoint, color=WHITE, flash_radius=0.28),
            FadeIn(endpoint),
            FadeIn(agreement),
        )
        self.wait(1.5)
        self.play(FadeOut(agreement))
        route_b.add(endpoint)

    def _show_homogeneity_statement(
        self,
        plane,
        mirror_line,
        mirror_label,
        origin,
        original,
        original_label,
        route_b,
    ) -> None:
        geometric_objects = VGroup(
            plane,
            mirror_line,
            mirror_label,
            origin,
            original,
            original_label,
            self.route_a,
            route_b,
        )

        self.play(FadeOut(geometric_objects))

        heading = Text(
            "Reflection across a line through the origin preserves scaling.",
            font_size=30,
        )

        equation = MathTex(
            r"r_m(c\mathbf{v})=c\,r_m(\mathbf{v})",
            font_size=46,
            color=YELLOW,
        )

        explanation = VGroup(
            Text(
                "Reflecting changes direction but preserves distance from the origin.",
                font_size=25,
            ),
            Text(
                "Dilation multiplies that distance by the same scalar.",
                font_size=25,
            ),
        ).arrange(DOWN, buff=0.18)

        conclusion = Text(
            "This is homogeneity — the first condition of linearity.",
            font_size=28,
            color=GREEN,
        )

        group = VGroup(heading, equation, explanation, conclusion).arrange(
            DOWN, buff=0.38
        )
        panel = SurroundingRectangle(group, buff=0.38, color=WHITE)

        self.play(FadeIn(VGroup(panel, group)))
        self.wait(2.8)
