"""CP86: Linearity Preserves Linear Combinations."""
from __future__ import annotations

import numpy as np
from manim import *

from engine.linear_combination_preservation import (
    evaluate_linear_combination_preservation,
)


class LinearityPreservesLinearCombinationsPresentation(Scene):
    """Compare transform-after-combine with combine-after-transform."""

    def construct(self) -> None:
        title = Text(
            "Linearity Preserves Linear Combinations",
            font_size=40,
        ).to_edge(UP)

        subtitle = MathTex(
            r"T(a\mathbf{u}+b\mathbf{v})",
            r"\quad\text{versus}\quad",
            r"aT(\mathbf{u})+bT(\mathbf{v})",
            font_size=29,
        ).next_to(title, DOWN, buff=0.16)

        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(1.0)

        plane = NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            x_length=8.1,
            y_length=5.1,
            background_line_style={"stroke_opacity": 0.28},
        ).shift(LEFT * 0.42 + DOWN * 0.62)

        origin = Dot(plane.c2p(0, 0), radius=0.07, color=RED)
        snapshot = evaluate_linear_combination_preservation()

        self.play(Create(plane), FadeIn(origin))

        matrix_card = self._matrix_card(snapshot.matrix)
        self.play(FadeIn(matrix_card))

        prompt = VGroup(
            Text("Pause and Predict", font_size=30, color=YELLOW),
            Text(
                "Will both routes produce the same transformed vector?",
                font_size=24,
            ),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN).shift(UP * 0.08)

        self.play(FadeIn(prompt))
        self.wait(2.0)
        self.play(FadeOut(prompt))

        original_group = self._show_original_vectors(
            plane,
            snapshot,
        )

        combination_group = self._build_linear_combination(
            plane,
            snapshot,
            original_group,
        )

        retained_result = self._transform_combination(
            plane,
            snapshot,
            combination_group,
        )

        self._clear_first_construction(
            original_group,
            combination_group,
            retained_result,
        )

        transformed_components = self._transform_components_separately(
            plane,
            snapshot,
        )

        comparison_group = self._scale_and_add_transformed_components(
            plane,
            snapshot,
            transformed_components,
            retained_result,
        )

        self._show_linearity_statement(
            plane,
            origin,
            matrix_card,
            retained_result,
            transformed_components,
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

    def _matrix_card(self, matrix):
        input_vector = Matrix(
            [[r"x_1"], [r"x_2"]],
            element_to_mobject_config={"font_size": 24},
        )

        matrix_tex = Matrix(
            [
                [f"{matrix[0, 0]:.2f}", f"{matrix[0, 1]:.2f}"],
                [f"{matrix[1, 0]:.2f}", f"{matrix[1, 1]:.2f}"],
            ],
            element_to_mobject_config={"font_size": 24},
        )

        transformation_label = MathTex(
            r"T\!\left(",
            font_size=27,
        )
        close_and_equals = MathTex(
            r"\right)=",
            font_size=27,
        )
        symbolic = MathTex(
            r"A\mathbf{x}",
            font_size=27,
        )

        product = VGroup(
            transformation_label,
            input_vector.copy(),
            close_and_equals,
            matrix_tex,
            input_vector.copy(),
            symbolic,
        ).arrange(RIGHT, buff=0.10)

        caption = Text(
            "A matrix acts on a vector by matrix-vector multiplication.",
            font_size=19,
        ).next_to(product, DOWN, buff=0.10)

        content = VGroup(product, caption)
        background = BackgroundRectangle(
            content,
            buff=0.16,
            fill_opacity=0.84,
            stroke_opacity=0.5,
        )

        return VGroup(background, content).to_corner(RIGHT + UP).shift(
            LEFT * 0.18 + DOWN * 1.12
        )

    def _route_heading(self, tex, caption):
        return VGroup(
            MathTex(tex, font_size=33),
            Text(caption, font_size=22),
        ).arrange(DOWN, buff=0.10).to_corner(LEFT + UP).shift(
            RIGHT * 0.35 + DOWN * 1.28
        )

    def _show_original_vectors(self, plane, s):
        zero = np.zeros(2)

        u_arrow = self._arrow(plane, zero, s.u, BLUE)
        v_arrow = self._arrow(plane, zero, s.v, GREEN)

        u_label = MathTex(
            r"\mathbf{u}",
            font_size=30,
            color=BLUE,
        ).next_to(u_arrow.get_end(), RIGHT, buff=0.08)

        v_label = MathTex(
            r"\mathbf{v}",
            font_size=30,
            color=GREEN,
        ).next_to(v_arrow.get_end(), LEFT, buff=0.08)

        self.play(
            GrowArrow(u_arrow),
            GrowArrow(v_arrow),
            FadeIn(u_label),
            FadeIn(v_label),
        )
        self.wait(1.0)

        return VGroup(u_arrow, v_arrow, u_label, v_label)

    def _build_linear_combination(self, plane, s, original_group):
        heading = self._route_heading(
            r"a\mathbf{u}+b\mathbf{v}",
            "First scale the vectors, then add.",
        )
        self.play(FadeIn(heading))

        zero = np.zeros(2)

        au_arrow = self._arrow(
            plane,
            zero,
            s.au,
            BLUE,
            width=6,
        )
        au_label = MathTex(
            r"a\mathbf{u}",
            font_size=29,
            color=BLUE,
        ).next_to(au_arrow.get_end(), RIGHT, buff=0.08)

        self.play(
            TransformFromCopy(original_group[0], au_arrow),
            FadeIn(au_label),
        )
        self.wait(0.7)

        bv_arrow = self._arrow(
            plane,
            s.au,
            s.combination,
            GREEN,
            width=6,
        )
        bv_label = MathTex(
            r"b\mathbf{v}",
            font_size=29,
            color=GREEN,
        ).next_to(bv_arrow.get_center(), LEFT, buff=0.08)

        self.play(
            TransformFromCopy(original_group[1], bv_arrow),
            FadeIn(bv_label),
        )
        self.wait(0.7)

        combination_arrow = self._arrow(
            plane,
            zero,
            s.combination,
            YELLOW,
            width=8,
        )
        combination_label = MathTex(
            r"a\mathbf{u}+b\mathbf{v}",
            font_size=30,
            color=YELLOW,
        ).next_to(combination_arrow.get_end(), RIGHT + DOWN, buff=0.10)

        self.play(
            GrowArrow(combination_arrow),
            FadeIn(combination_label),
        )
        self.wait(1.2)

        return VGroup(
            heading,
            au_arrow,
            au_label,
            bv_arrow,
            bv_label,
            combination_arrow,
            combination_label,
        )

    def _transform_combination(self, plane, s, combination_group):
        transformed_arrow = self._arrow(
            plane,
            np.zeros(2),
            s.transformed_combination,
            ORANGE,
            width=8,
        )
        transformed_label = MathTex(
            r"T(a\mathbf{u}+b\mathbf{v})",
            font_size=30,
            color=ORANGE,
        ).next_to(transformed_arrow.get_end(), LEFT + DOWN, buff=0.10)

        self.play(
            TransformFromCopy(combination_group[5], transformed_arrow),
            FadeIn(transformed_label),
        )
        self.wait(2.0)

        return VGroup(transformed_arrow, transformed_label)

    def _clear_first_construction(
        self,
        original_group,
        combination_group,
        retained_result,
    ):
        note = Text(
            "Retain the transformed result. Clear the first construction.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN).shift(UP * 0.10)

        self.play(FadeIn(note))
        self.wait(0.8)
        self.play(
            FadeOut(original_group),
            FadeOut(combination_group),
            FadeOut(note),
        )
        self.wait(0.5)

    def _transform_components_separately(self, plane, s):
        heading = self._route_heading(
            r"T(\mathbf{u}),\quad T(\mathbf{v})",
            "Now transform the component vectors separately.",
        )
        self.play(FadeIn(heading))

        zero = np.zeros(2)

        u_arrow = self._arrow(plane, zero, s.u, BLUE)
        u_label = MathTex(
            r"\mathbf{u}",
            font_size=29,
            color=BLUE,
        ).next_to(u_arrow.get_end(), RIGHT, buff=0.08)

        self.play(GrowArrow(u_arrow), FadeIn(u_label))
        self.wait(0.6)

        transformed_u = self._arrow(
            plane,
            zero,
            s.transformed_u,
            BLUE,
            width=6,
        )
        transformed_u_label = MathTex(
            r"T(\mathbf{u})",
            font_size=28,
            color=BLUE,
        ).next_to(transformed_u.get_end(), RIGHT, buff=0.08)

        self.play(
            TransformFromCopy(u_arrow, transformed_u),
            FadeIn(transformed_u_label),
        )
        self.wait(0.7)
        self.play(FadeOut(u_arrow), FadeOut(u_label))

        v_arrow = self._arrow(plane, zero, s.v, GREEN)
        v_label = MathTex(
            r"\mathbf{v}",
            font_size=29,
            color=GREEN,
        ).next_to(v_arrow.get_end(), LEFT, buff=0.08)

        self.play(GrowArrow(v_arrow), FadeIn(v_label))
        self.wait(0.6)

        transformed_v = self._arrow(
            plane,
            zero,
            s.transformed_v,
            GREEN,
            width=6,
        )
        transformed_v_label = MathTex(
            r"T(\mathbf{v})",
            font_size=28,
            color=GREEN,
        ).next_to(transformed_v.get_end(), LEFT, buff=0.08)

        self.play(
            TransformFromCopy(v_arrow, transformed_v),
            FadeIn(transformed_v_label),
        )
        self.wait(0.7)
        self.play(FadeOut(v_arrow), FadeOut(v_label))

        return VGroup(
            heading,
            transformed_u,
            transformed_u_label,
            transformed_v,
            transformed_v_label,
        )

    def _scale_and_add_transformed_components(
        self,
        plane,
        s,
        transformed_components,
        retained_result,
    ):
        zero = np.zeros(2)

        scaled_u = self._arrow(
            plane,
            zero,
            s.scaled_transformed_u,
            BLUE,
            width=6,
        )
        scaled_u_label = MathTex(
            r"aT(\mathbf{u})",
            font_size=28,
            color=BLUE,
        ).next_to(scaled_u.get_end(), RIGHT, buff=0.08)

        self.play(
            TransformFromCopy(transformed_components[1], scaled_u),
            TransformFromCopy(transformed_components[2], scaled_u_label),
        )
        self.wait(0.8)

        scaled_v = self._arrow(
            plane,
            s.scaled_transformed_u,
            s.combination_of_transforms,
            GREEN,
            width=6,
        )
        scaled_v_label = MathTex(
            r"bT(\mathbf{v})",
            font_size=28,
            color=GREEN,
        ).next_to(scaled_v.get_center(), LEFT, buff=0.08)

        self.play(
            TransformFromCopy(transformed_components[3], scaled_v),
            TransformFromCopy(transformed_components[4], scaled_v_label),
        )
        self.wait(0.8)

        resultant = self._arrow(
            plane,
            zero,
            s.combination_of_transforms,
            YELLOW,
            width=7,
        )
        resultant_label = MathTex(
            r"aT(\mathbf{u})+bT(\mathbf{v})",
            font_size=29,
            color=YELLOW,
        ).next_to(resultant.get_end(), RIGHT + UP, buff=0.10)

        self.play(
            GrowArrow(resultant),
            FadeIn(resultant_label),
        )
        self.wait(1.2)

        endpoint = Dot(
            self._point(plane, s.combination_of_transforms),
            radius=0.09,
            color=WHITE,
        )
        agreement = Text(
            "The two routes produce the same endpoint.",
            font_size=27,
            color=GREEN,
        ).to_edge(DOWN).shift(UP * 0.10)

        self.play(
            Flash(endpoint, color=WHITE, flash_radius=0.28),
            FadeIn(endpoint),
            FadeIn(agreement),
        )
        self.wait(1.7)
        self.play(FadeOut(agreement))

        return VGroup(
            scaled_u,
            scaled_u_label,
            scaled_v,
            scaled_v_label,
            resultant,
            resultant_label,
            endpoint,
        )

    def _show_linearity_statement(
        self,
        plane,
        origin,
        matrix_card,
        retained_result,
        transformed_components,
        comparison_group,
    ):
        geometric_objects = VGroup(
            plane,
            origin,
            matrix_card,
            retained_result,
            transformed_components,
            comparison_group,
        )
        self.play(FadeOut(geometric_objects))

        heading = Text(
            "Linearity combines homogeneity and additivity.",
            font_size=31,
        )

        equation = MathTex(
            r"T(a\mathbf{u}+b\mathbf{v})"
            r"="
            r"aT(\mathbf{u})+bT(\mathbf{v})",
            font_size=46,
            color=YELLOW,
        )

        explanation = VGroup(
            MathTex(
                r"A(c\mathbf{v})=c(A\mathbf{v})",
                font_size=30,
            ),
            MathTex(
                r"A(\mathbf{u}+\mathbf{v})"
                r"="
                r"A\mathbf{u}+A\mathbf{v}",
                font_size=30,
            ),
        ).arrange(DOWN, buff=0.20)

        matrix_message = Text(
            "Matrix multiplication preserves both scaling and addition.",
            font_size=25,
        )

        conclusion = Text(
            "Therefore every matrix transformation is linear.",
            font_size=28,
            color=GREEN,
        )

        group = VGroup(
            heading,
            equation,
            explanation,
            matrix_message,
            conclusion,
        ).arrange(DOWN, buff=0.32)

        panel = SurroundingRectangle(group, buff=0.38, color=WHITE)

        self.play(FadeIn(VGroup(panel, group)))
        self.wait(3.0)
