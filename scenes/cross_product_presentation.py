"""CP89: the cross product as perpendicular direction and oriented area."""

from __future__ import annotations

import numpy as np

from manim import (
    Arrow3D,
    BLUE,
    Create,
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    MathTex,
    ORANGE,
    OUT,
    Polygon,
    RED,
    ReplacementTransform,
    RIGHT,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.cross_product import CrossProduct


class CrossProductPresentation(ThreeDScene):
    TITLE = "What Can Two Vectors Produce in 3D?"

    def construct(self) -> None:
        s = CrossProduct().snapshot()

        title = Text(self.TITLE, font_size=40).to_edge(UP)
        subtitle = Text(
            "A third vector can encode direction, area, and orientation.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.16)

        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle))

        axes = ThreeDAxes(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            z_range=(-3, 3, 1),
            x_length=7.4,
            y_length=5.2,
            z_length=4.8,
        ).shift(DOWN * 0.45)

        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-48 * DEGREES,
            zoom=0.92,
        )

        u_arrow = self._arrow(axes, s.vector_u, BLUE)
        v_arrow = self._arrow(axes, s.vector_v, YELLOW)

        u_label = self._label(r"\mathbf{u}", axes, s.vector_u, BLUE)
        v_label = self._label(r"\mathbf{v}", axes, s.vector_v, YELLOW)

        question = Text(
            "What vector could describe both at once?",
            font_size=27,
            color=YELLOW,
        ).to_edge(DOWN).shift(UP * 0.22)
        self.add_fixed_in_frame_mobjects(question)

        self.play(Create(axes))
        self.play(Create(u_arrow), Create(v_arrow))
        self.play(FadeIn(u_label), FadeIn(v_label), FadeIn(question))
        self.wait(1.0)

        parallelogram = self._parallelogram(axes, s.vector_u, s.vector_v)
        area_label = VGroup(
            Text("Parallelogram area", font_size=26, color=ORANGE),
            MathTex(
                r"\|\mathbf{u}\times\mathbf{v}\|",
                font_size=35,
                color=ORANGE,
            ),
        ).arrange(DOWN, buff=0.10).to_corner(RIGHT + UP).shift(
            LEFT * 0.25 + DOWN * 1.30
        )
        self.add_fixed_in_frame_mobjects(area_label)

        self.play(FadeOut(question))
        self.play(Create(parallelogram), FadeIn(area_label))
        self.wait(1.0)

        cross_arrow = self._arrow(axes, s.cross_uv, GREEN)
        cross_label = self._label(
            r"\mathbf{u}\times\mathbf{v}",
            axes,
            s.cross_uv,
            GREEN,
        )

        perpendicular = Text(
            "Perpendicular to both vectors",
            font_size=27,
            color=GREEN,
        ).to_edge(DOWN).shift(UP * 0.22)
        self.add_fixed_in_frame_mobjects(perpendicular)

        self.play(Create(cross_arrow), FadeIn(cross_label))
        self.play(FadeIn(perpendicular))
        self.wait(0.8)

        self.begin_ambient_camera_rotation(rate=0.18)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)

        self.play(FadeOut(perpendicular), FadeOut(area_label))

        magnitude_card = VGroup(
            Text("Magnitude", font_size=30, color=ORANGE),
            MathTex(
                r"\|\mathbf{u}\times\mathbf{v}\|"
                r"="
                r"\|\mathbf{u}\|\,\|\mathbf{v}\|\sin\theta",
                font_size=36,
            ),
            Text(
                "Its length is the area of the parallelogram.",
                font_size=25,
                color=ORANGE,
            ),
        ).arrange(DOWN, buff=0.22).to_edge(RIGHT).shift(
            LEFT * 0.28 + DOWN * 0.10
        )
        self.add_fixed_in_frame_mobjects(magnitude_card)

        self.play(FadeIn(magnitude_card))
        self.wait(1.3)

        reverse_heading = Text(
            "Order matters",
            font_size=31,
            color=YELLOW,
        ).to_edge(DOWN).shift(UP * 0.72)
        reverse_formula = MathTex(
            r"\mathbf{v}\times\mathbf{u}"
            r"="
            r"-(\mathbf{u}\times\mathbf{v})",
            font_size=37,
        ).next_to(reverse_heading, DOWN, buff=0.14)
        self.add_fixed_in_frame_mobjects(reverse_heading, reverse_formula)

        reverse_arrow = self._arrow(axes, s.cross_vu, RED)
        reverse_label = self._label(
            r"\mathbf{v}\times\mathbf{u}",
            axes,
            s.cross_vu,
            RED,
        )

        self.play(FadeOut(cross_label))
        self.play(
            ReplacementTransform(cross_arrow, reverse_arrow),
            FadeIn(reverse_label),
            FadeIn(reverse_heading),
            FadeIn(reverse_formula),
            run_time=1.8,
        )
        self.wait(1.2)

        self.play(
            FadeOut(axes),
            FadeOut(u_arrow),
            FadeOut(v_arrow),
            FadeOut(u_label),
            FadeOut(v_label),
            FadeOut(parallelogram),
            FadeOut(reverse_arrow),
            FadeOut(reverse_label),
            FadeOut(magnitude_card),
            FadeOut(reverse_heading),
            FadeOut(reverse_formula),
            FadeOut(subtitle),
        )

        self._show_conclusion()
        self.wait(1.5)

    def _show_conclusion(self) -> None:
        heading = Text(
            "The Cross Product",
            font_size=38,
            color=YELLOW,
        )
        direction = Text(
            "Direction: perpendicular to both input vectors",
            font_size=28,
            color=GREEN,
        )
        magnitude = Text(
            "Magnitude: area of the spanned parallelogram",
            font_size=28,
            color=ORANGE,
        )
        orientation = Text(
            "Orientation: reversing the order reverses the vector",
            font_size=28,
            color=RED,
        )
        final = Text(
            "The cross product measures oriented area.",
            font_size=31,
            color=WHITE,
        )

        group = VGroup(
            heading,
            direction,
            magnitude,
            orientation,
            final,
        ).arrange(DOWN, buff=0.34)

        self.add_fixed_in_frame_mobjects(group)
        self.play(FadeIn(group))

    @staticmethod
    def _arrow(axes, vector, color):
        return Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(
                float(vector[0]),
                float(vector[1]),
                float(vector[2]),
            ),
            color=color,
            thickness=0.035,
            height=0.20,
            base_radius=0.09,
        )

    @staticmethod
    def _label(tex, axes, vector, color):
        point = axes.c2p(
            float(vector[0]),
            float(vector[1]),
            float(vector[2]),
        )
        label = MathTex(tex, font_size=28, color=color)
        label.move_to(point + 0.28 * OUT + 0.18 * RIGHT)
        return label

    @staticmethod
    def _parallelogram(axes, vector_u, vector_v):
        origin = axes.c2p(0, 0, 0)
        u_point = axes.c2p(*vector_u)
        v_point = axes.c2p(*vector_v)
        uv_point = axes.c2p(*(vector_u + vector_v))
        return Polygon(
            origin,
            u_point,
            uv_point,
            v_point,
            color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=0.30,
            stroke_width=3,
        )
