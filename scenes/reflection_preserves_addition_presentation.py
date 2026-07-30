"""CP85: Reflection Preserves Vector Addition."""
from __future__ import annotations

import numpy as np
from manim import *

from engine.reflection_additivity import evaluate_reflection_additivity


class ReflectionPreservesAdditionPresentation(Scene):
    """Compare reflect-after-add with add-after-reflect."""

    def construct(self) -> None:
        title = Text("Does Reflection Preserve Addition?", font_size=40).to_edge(UP)
        subtitle = Text(
            "Two routes through the same geometry.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.15)

        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(1.0)

        plane = NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            x_length=8.6,
            y_length=5.4,
            background_line_style={"stroke_opacity": 0.28},
        ).shift(DOWN * 0.38)

        snapshot = evaluate_reflection_additivity()
        mirror_line = self._mirror_line(plane, snapshot.line_angle)
        mirror_label = MathTex(r"m", font_size=30).next_to(
            mirror_line.get_end(), UP + LEFT, buff=0.08
        )
        origin = Dot(plane.c2p(0, 0), radius=0.07, color=RED)

        self.play(
            Create(plane),
            Create(mirror_line),
            FadeIn(mirror_label),
            FadeIn(origin),
        )

        original_group = self._show_original_sum(plane, snapshot)

        prompt = VGroup(
            Text("Pause and Predict", font_size=30, color=YELLOW),
            Text(
                "Will reflecting the sum match adding the reflected vectors?",
                font_size=24,
            ),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN).shift(UP * 0.08)

        self.play(FadeIn(prompt))
        self.wait(2.0)
        self.play(FadeOut(prompt))

        retained_result = self._reflect_and_retain_sum(
            plane,
            snapshot,
            original_group,
        )

        self._erase_everything_except_result(
            original_group,
            retained_result,
        )

        reflected_components = self._redraw_and_reflect_components(
            plane,
            snapshot,
        )

        comparison_group = self._show_sum_of_reflections(
            plane,
            snapshot,
            retained_result,
            reflected_components,
        )

        self._show_additivity_statement(
            plane,
            mirror_line,
            mirror_label,
            origin,
            retained_result,
            reflected_components,
            comparison_group,
        )

    def _point(self, plane, vector):
        return plane.c2p(float(vector[0]), float(vector[1]))

    def _arrow(self, plane, start, end, color, width=5):
        return Arrow(
            self._point(plane, start),
            self._point(plane, end),
            buff=0,
            color=color,
            stroke_width=width,
            max_tip_length_to_length_ratio=0.16,
        )

    def _mirror_line(self, plane, angle):
        direction = np.array([np.cos(angle), np.sin(angle)])
        return Line(
            self._point(plane, -4.5 * direction),
            self._point(plane, 4.5 * direction),
            color=WHITE,
            stroke_width=4,
        )

    def _route_heading(self, tex, caption):
        return VGroup(
            MathTex(tex, font_size=34),
            Text(caption, font_size=23),
        ).arrange(DOWN, buff=0.10).to_corner(LEFT + UP).shift(
            RIGHT * 0.35 + DOWN * 1.28
        )

    def _show_original_sum(self, plane, s):
        zero = np.zeros(2)

        u_arrow = self._arrow(plane, zero, s.u, BLUE)
        v_arrow = self._arrow(plane, s.u, s.sum_vector, GREEN)
        sum_arrow = self._arrow(plane, zero, s.sum_vector, YELLOW, width=7)

        u_label = MathTex(r"\mathbf{u}", font_size=30, color=BLUE).next_to(
            u_arrow.get_center(), DOWN, buff=0.08
        )
        v_label = MathTex(r"\mathbf{v}", font_size=30, color=GREEN).next_to(
            v_arrow.get_center(), RIGHT, buff=0.08
        )
        sum_label = MathTex(
            r"\mathbf{u}+\mathbf{v}",
            font_size=30,
            color=YELLOW,
        ).next_to(sum_arrow.get_end(), RIGHT, buff=0.10)

        self.play(GrowArrow(u_arrow), GrowArrow(v_arrow))
        self.play(
            GrowArrow(sum_arrow),
            FadeIn(u_label),
            FadeIn(v_label),
            FadeIn(sum_label),
        )
        self.wait(1.2)

        return VGroup(
            u_arrow,
            v_arrow,
            sum_arrow,
            u_label,
            v_label,
            sum_label,
        )

    def _reflect_and_retain_sum(self, plane, s, original_group):
        heading = self._route_heading(
            r"r_m(\mathbf{u}+\mathbf{v})",
            "First add, then reflect the resultant.",
        )
        self.play(FadeIn(heading))

        reflected_sum = self._arrow(
            plane,
            np.zeros(2),
            s.reflected_sum,
            ORANGE,
            width=8,
        )
        reflected_sum_label = MathTex(
            r"r_m(\mathbf{u}+\mathbf{v})",
            font_size=29,
            color=ORANGE,
        ).next_to(reflected_sum.get_end(), LEFT + DOWN, buff=0.10)

        self.play(
            TransformFromCopy(original_group[2], reflected_sum),
            FadeIn(reflected_sum_label),
        )
        self.wait(2.2)

        return VGroup(heading, reflected_sum, reflected_sum_label)

    def _erase_everything_except_result(
        self,
        original_group,
        retained_result,
    ):
        note = Text(
            "Keep the reflected result. Clear the original construction.",
            font_size=24,
            color=GREY_B,
        ).to_edge(DOWN).shift(UP * 0.10)

        self.play(FadeIn(note))
        self.wait(0.9)

        self.play(
            FadeOut(original_group),
            FadeOut(retained_result[0]),
            FadeOut(note),
        )
        self.wait(0.5)

    def _redraw_and_reflect_components(self, plane, s):
        heading = self._route_heading(
            r"r_m(\mathbf{u}),\quad r_m(\mathbf{v})",
            "Now redraw and reflect each vector separately.",
        )
        self.play(FadeIn(heading))

        zero = np.zeros(2)

        u_arrow = self._arrow(plane, zero, s.u, BLUE)
        u_label = MathTex(r"\mathbf{u}", font_size=30, color=BLUE).next_to(
            u_arrow.get_center(), DOWN, buff=0.08
        )

        self.play(GrowArrow(u_arrow), FadeIn(u_label))
        self.wait(0.7)

        reflected_u = self._arrow(
            plane,
            zero,
            s.reflected_u,
            BLUE,
            width=6,
        )
        reflected_u_label = MathTex(
            r"r_m(\mathbf{u})",
            font_size=28,
            color=BLUE,
        ).next_to(reflected_u.get_end(), LEFT, buff=0.10)

        self.play(
            TransformFromCopy(u_arrow, reflected_u),
            FadeIn(reflected_u_label),
        )
        self.wait(0.8)
        self.play(FadeOut(u_arrow), FadeOut(u_label))

        v_arrow = self._arrow(plane, zero, s.v, GREEN)
        v_label = MathTex(r"\mathbf{v}", font_size=30, color=GREEN).next_to(
            v_arrow.get_center(), LEFT, buff=0.08
        )

        self.play(GrowArrow(v_arrow), FadeIn(v_label))
        self.wait(0.7)

        reflected_v_origin = self._arrow(
            plane,
            zero,
            s.reflected_v,
            GREEN,
            width=6,
        )
        reflected_v_origin_label = MathTex(
            r"r_m(\mathbf{v})",
            font_size=28,
            color=GREEN,
        ).next_to(reflected_v_origin.get_end(), DOWN, buff=0.10)

        self.play(
            TransformFromCopy(v_arrow, reflected_v_origin),
            FadeIn(reflected_v_origin_label),
        )
        self.wait(0.9)
        self.play(FadeOut(v_arrow), FadeOut(v_label))

        return VGroup(
            heading,
            reflected_u,
            reflected_u_label,
            reflected_v_origin,
            reflected_v_origin_label,
        )

    def _show_sum_of_reflections(
        self,
        plane,
        s,
        retained_result,
        reflected_components,
    ):
        zero = np.zeros(2)

        translated_reflected_v = self._arrow(
            plane,
            s.reflected_u,
            s.sum_of_reflections,
            GREEN,
            width=6,
        )
        translated_v_label = MathTex(
            r"r_m(\mathbf{v})",
            font_size=28,
            color=GREEN,
        ).next_to(translated_reflected_v.get_center(), DOWN, buff=0.08)

        self.play(
            TransformFromCopy(
                reflected_components[3],
                translated_reflected_v,
            ),
            TransformFromCopy(
                reflected_components[4],
                translated_v_label,
            ),
        )
        self.wait(0.8)

        sum_of_reflections = self._arrow(
            plane,
            zero,
            s.sum_of_reflections,
            YELLOW,
            width=7,
        )
        sum_label = MathTex(
            r"r_m(\mathbf{u})+r_m(\mathbf{v})",
            font_size=29,
            color=YELLOW,
        ).next_to(sum_of_reflections.get_end(), RIGHT + UP, buff=0.10)

        self.play(
            GrowArrow(sum_of_reflections),
            FadeIn(sum_label),
        )
        self.wait(1.2)

        endpoint = Dot(
            self._point(plane, s.sum_of_reflections),
            radius=0.09,
            color=WHITE,
        )
        agreement = Text(
            "The new resultant coincides with the retained reflected sum.",
            font_size=26,
            color=GREEN,
        ).to_edge(DOWN).shift(UP * 0.10)

        self.play(
            Flash(endpoint, color=WHITE, flash_radius=0.28),
            FadeIn(endpoint),
            FadeIn(agreement),
        )
        self.wait(1.8)
        self.play(FadeOut(agreement))

        return VGroup(
            translated_reflected_v,
            translated_v_label,
            sum_of_reflections,
            sum_label,
            endpoint,
        )

    def _show_additivity_statement(
        self,
        plane,
        mirror_line,
        mirror_label,
        origin,
        retained_result,
        reflected_components,
        comparison_group,
    ):
        geometric_objects = VGroup(
            plane,
            mirror_line,
            mirror_label,
            origin,
            retained_result,
            reflected_components,
            comparison_group,
        )
        self.play(FadeOut(geometric_objects))

        heading = Text(
            "Reflection across a line through the origin preserves addition.",
            font_size=30,
        )

        equation = MathTex(
            r"r_m(\mathbf{u}+\mathbf{v})"
            r"="
            r"r_m(\mathbf{u})+r_m(\mathbf{v})",
            font_size=43,
            color=YELLOW,
        )

        explanation = VGroup(
            Text(
                "Reflect the sum, or reflect the vectors and then add.",
                font_size=25,
            ),
            Text(
                "Both constructions produce the same resultant.",
                font_size=25,
            ),
        ).arrange(DOWN, buff=0.18)

        conclusion = Text(
            "This is additivity — the second condition of linearity.",
            font_size=28,
            color=GREEN,
        )

        group = VGroup(
            heading,
            equation,
            explanation,
            conclusion,
        ).arrange(DOWN, buff=0.38)

        panel = SurroundingRectangle(group, buff=0.38, color=WHITE)

        self.play(FadeIn(VGroup(panel, group)))
        self.wait(2.8)
