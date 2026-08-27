"""Manim presentation: Positive Definite Matrices — From Directional Energy to a Bowl."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C, DEGREES, GREEN_C, GREY_B, ORANGE, RED_C, TEAL_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Circle, Create, DecimalNumber, Dot3D, FadeIn, FadeOut, Line3D,
    MathTex, Matrix, NumberPlane, ReplacementTransform, Surface, Text, Transform,
    ThreeDAxes, ThreeDScene, ValueTracker, VGroup, always_redraw, smooth,
)

from engine.positive_definite_quadratic_surface import QuadraticSurfaceGeometry


class PositiveDefiniteQuadraticSurfacePresentation(ThreeDScene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "From Directional Energy to a Bowl"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Text(
            self.CHAPTER_BANNER, font_size=21, color=GREY_B, weight="BOLD"
        ).to_edge(UP, buff=0.16)
        title = Text(
            self.LESSON_TITLE, font_size=31, color=YELLOW, weight="BOLD"
        ).next_to(banner, DOWN, buff=0.11)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.16)
        self.add_fixed_in_frame_mobjects(banner, title, heading)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.add_fixed_in_frame_mobjects(new)
        self.play(ReplacementTransform(old, new), run_time=0.6)
        return new

    @staticmethod
    def _matrix(entries, scale=0.78):
        return Matrix(entries, h_buff=0.9, v_buff=0.78).scale(scale)

    def _fixed(self, *items):
        self.add_fixed_in_frame_mobjects(*items)
        return VGroup(*items)

    def construct(self):
        model = QuadraticSurfaceGeometry()
        banner, title, heading = self._chrome(
            "Positive on every unit direction—but what about every nonzero vector?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        matrix_card = VGroup(
            MathTex("A=", font_size=44),
            self._matrix([["2", "1"], ["1", "2"]]),
        ).arrange(RIGHT, buff=0.14)
        recall = VGroup(
            MathTex(r"q(u)=u^T A u>0", font_size=50, color=GREEN_C),
            Text("for every unit direction u", font_size=30, color=WHITE),
        ).arrange(DOWN, buff=0.24)
        opening = self._fixed(matrix_card, recall).arrange(RIGHT, buff=0.90)
        opening.move_to(DOWN * 0.30)
        self.play(FadeIn(matrix_card), FadeIn(recall))
        self.wait(1.5)

        heading = self._replace_heading(
            heading, "Every nonzero vector is a direction multiplied by a distance."
        )
        self.play(FadeOut(opening))

        plane = NumberPlane(
            x_range=[-1.6, 1.6, 0.4],
            y_range=[-1.6, 1.6, 0.4],
            x_length=5.1,
            y_length=5.1,
            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.22},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.4},
        ).move_to(LEFT * 3.0 + DOWN * 0.52)
        origin = plane.c2p(0, 0)
        unit_radius = np.linalg.norm(plane.c2p(1, 0) - origin)
        unit_circle = Circle(
            radius=unit_radius, color=GREY_B, stroke_width=2.3
        ).move_to(origin)
        radius = ValueTracker(0.45)
        theta = np.pi / 6

        radial_arrow = always_redraw(
            lambda: Arrow(
                origin,
                plane.c2p(*model.radial_vector(radius.get_value(), theta)),
                buff=0,
                color=ORANGE,
                stroke_width=8,
                max_tip_length_to_length_ratio=0.16,
            )
        )
        vector_label = always_redraw(
            lambda: MathTex(r"x=ru", font_size=32, color=ORANGE).next_to(
                plane.c2p(*model.radial_vector(radius.get_value(), theta)), UP, buff=0.10
            )
        )
        live_panel = always_redraw(
            lambda: VGroup(
                VGroup(
                    MathTex(r"r=", font_size=43),
                    DecimalNumber(
                        radius.get_value(),
                        num_decimal_places=2,
                        font_size=43,
                        color=ORANGE,
                    ),
                ).arrange(RIGHT, buff=0.12),
                VGroup(
                    MathTex(r"q(ru)=", font_size=43, color=YELLOW),
                    DecimalNumber(
                        model.radial_energy(radius.get_value(), theta),
                        num_decimal_places=2,
                        font_size=43,
                        color=GREEN_C,
                    ),
                ).arrange(RIGHT, buff=0.12),
            ).arrange(DOWN, buff=0.42).move_to(RIGHT * 3.45 + UP * 0.12)
        )
        decomposition = MathTex(
            r"x=ru,\qquad r>0,\qquad \lVert u\rVert=1",
            font_size=39,
            color=WHITE,
        ).move_to(RIGHT * 3.45 + UP * 1.48)
        self._fixed(plane, unit_circle, decomposition)
        self.wait(0.45)
        self._fixed(radial_arrow, vector_label, live_panel)
        self.wait(0.4)
        for target in (0.85, 1.35, 0.60, 1.10):
            self.play(radius.animate.set_value(target), run_time=1.15, rate_func=smooth)
            self.wait(0.22)

        scaling = MathTex(
            r"q(ru)=(ru)^T A(ru)=r^2q(u)",
            font_size=45,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.20)
        consequence = Text(
            "A positive directional energy stays positive at every nonzero distance.",
            font_size=27,
            color=GREEN_C,
        ).next_to(scaling, UP, buff=0.18)
        if consequence.width > 11.2:
            consequence.scale_to_fit_width(11.2)
        self._fixed(scaling, consequence)
        self.play(FadeIn(scaling))
        self.play(FadeIn(consequence))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Now use the quadratic energy as height above the input plane."
        )
        two_d = VGroup(
            plane, unit_circle, radial_arrow, vector_label, live_panel,
            decomposition, scaling, consequence,
        )
        self.play(FadeOut(two_d), FadeOut(banner), FadeOut(title))

        self.set_camera_orientation(phi=68 * DEGREES, theta=-48 * DEGREES, zoom=0.70)
        axes = ThreeDAxes(
            x_range=[-1.4, 1.4, 0.7],
            y_range=[-1.4, 1.4, 0.7],
            z_range=[-4.5, 9, 1.5],
            x_length=5.5,
            y_length=5.5,
            z_length=3.6,
        )
        reference_plane = Surface(
            lambda u, v: axes.c2p(u, v, 0),
            u_range=[-1.2, 1.2],
            v_range=[-1.2, 1.2],
            resolution=(8, 8),
            fill_opacity=0.16,
            checkerboard_colors=[GREY_B, GREY_B],
            stroke_color=GREY_B,
            stroke_width=0.35,
        )
        surface = Surface(
            lambda u, v: axes.c2p(*model.surface_point(u, v)),
            u_range=[-1.2, 1.2],
            v_range=[-1.2, 1.2],
            resolution=(24, 24),
            fill_opacity=0.62,
            checkerboard_colors=[BLUE_C, TEAL_C],
            stroke_color=WHITE,
            stroke_opacity=0.25,
            stroke_width=0.35,
        )
        restored_surface = surface.copy()
        zero_surface = Surface(
            lambda u, v: axes.c2p(u, v, 3 * u * u),
            u_range=[-1.2, 1.2],
            v_range=[-1.2, 1.2],
            resolution=(24, 24),
            fill_opacity=0.62,
            checkerboard_colors=[YELLOW, ORANGE],
            stroke_color=WHITE,
            stroke_opacity=0.25,
            stroke_width=0.35,
        )
        saddle_surface = Surface(
            lambda u, v: axes.c2p(u, v, 3 * u * u - 3 * v * v),
            u_range=[-1.2, 1.2],
            v_range=[-1.2, 1.2],
            resolution=(24, 24),
            fill_opacity=0.62,
            checkerboard_colors=[RED_C, ORANGE],
            stroke_color=WHITE,
            stroke_opacity=0.25,
            stroke_width=0.35,
        )
        sample = model.surface_point(0.75, 0.25)
        base_dot = Dot3D(axes.c2p(sample[0], sample[1], 0), radius=0.075, color=ORANGE)
        height_line = Line3D(
            axes.c2p(sample[0], sample[1], 0),
            axes.c2p(*sample),
            thickness=0.018,
            color=ORANGE,
        )
        lifted_dot = Dot3D(axes.c2p(*sample), radius=0.085, color=YELLOW)
        height_rule = MathTex(
            r"(x,y)\longmapsto \bigl(x,y,q(x,y)\bigr)",
            font_size=38,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.22)
        self._fixed(height_rule)

        self.play(Create(axes), FadeIn(reference_plane), FadeIn(height_rule))
        self.play(FadeIn(base_dot), Create(height_line), FadeIn(lifted_dot))
        self.wait(0.8)
        self.play(FadeIn(surface), run_time=1.5)
        self.begin_ambient_camera_rotation(rate=0.08)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()

        heading = self._replace_heading(
            heading, "What would zero or negative quadratic energy look like here?"
        )
        prediction = Text(
            "Pause and predict.", font_size=34, color=YELLOW, weight="BOLD"
        ).to_edge(DOWN, buff=0.24)
        self._fixed(prediction)
        self.play(FadeOut(height_rule), FadeIn(prediction))
        self.wait(2.7)
        self.play(
            FadeOut(prediction), FadeOut(base_dot),
            FadeOut(height_line), FadeOut(lifted_dot),
        )

        heading = self._replace_heading(
            heading, "Zero away from the origin means touching the plane elsewhere."
        )
        zero_line = Line3D(
            axes.c2p(0, -1.2, 0),
            axes.c2p(0, 1.2, 0),
            thickness=0.026,
            color=YELLOW,
        )
        zero_formula = MathTex(r"z=3x^2", font_size=36, color=YELLOW)
        zero_caption = Text(
            "A whole line of nonzero inputs has zero height.",
            font_size=25,
            color=WHITE,
        )
        zero_panel = VGroup(zero_formula, zero_caption).arrange(RIGHT, buff=0.34)
        zero_panel.to_edge(DOWN, buff=0.20)
        self._fixed(zero_formula, zero_caption)
        self.play(
            Transform(surface, zero_surface),
            FadeIn(zero_line),
            FadeIn(zero_panel),
            run_time=1.6,
        )
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Negative energy means crossing below the input plane."
        )
        negative_depth = Line3D(
            axes.c2p(0, 1, 0),
            axes.c2p(0, 1, -3),
            thickness=0.026,
            color=RED_C,
        )
        negative_formula = MathTex(r"z=3x^2-3y^2", font_size=36, color=RED_C)
        negative_caption = Text(
            "Some nonzero inputs now have negative height.",
            font_size=25,
            color=WHITE,
        )
        negative_panel = VGroup(negative_formula, negative_caption).arrange(RIGHT, buff=0.34)
        negative_panel.to_edge(DOWN, buff=0.20)
        self._fixed(negative_formula, negative_caption)
        self.play(
            FadeOut(zero_panel),
            FadeOut(zero_line),
            Transform(surface, saddle_surface),
            FadeIn(negative_depth),
            FadeIn(negative_panel),
            run_time=1.6,
        )
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "This bowl touches the plane only at the origin and never passes below it."
        )
        self.play(
            FadeOut(negative_panel),
            FadeOut(negative_depth),
            Transform(surface, restored_surface),
            run_time=1.6,
        )
        origin_dot = Dot3D(axes.c2p(0, 0, 0), radius=0.105, color=ORANGE)
        actual_note = Text(
            "q(0)=0; every nonzero input has positive height.",
            font_size=29,
            color=GREEN_C,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.22)
        self._fixed(actual_note)
        self.play(FadeIn(origin_dot), FadeIn(actual_note))
        self.wait(2.8)

        heading = self._replace_heading(
            heading, "Positive definiteness has an exact geometric signature."
        )
        self.play(
            FadeOut(axes), FadeOut(reference_plane), FadeOut(surface),
            FadeOut(origin_dot), FadeOut(actual_note),
        )
        first = MathTex(
            r"\boxed{x^T A x>0\quad\text{for every }x\ne0}",
            font_size=51,
            color=YELLOW,
        )
        equivalence = MathTex(r"\Longleftrightarrow", font_size=53, color=WHITE)
        second = MathTex(
            r"z=x^T A x\ \text{lies above }z=0\ \text{except at the origin}",
            font_size=40,
            color=WHITE,
        )
        term = Text("positive definite", font_size=44, color=GREEN_C, weight="BOLD")
        final_card = VGroup(first, equivalence, second, term).arrange(DOWN, buff=0.32)
        final_card.move_to(DOWN * 0.36)
        self._fixed(first, equivalence, second, term)
        self.add_fixed_in_frame_mobjects(banner, title)
        self.play(FadeIn(banner), FadeIn(title), FadeIn(first))
        self.play(FadeIn(equivalence), FadeIn(second))
        self.play(FadeIn(term))
        self.wait(2.5)
