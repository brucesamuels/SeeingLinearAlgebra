"""CP73: a geometric introduction to the subspace test."""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Create,
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    MathTex,
    ORIGIN,
    Polygon,
    RED,
    RIGHT,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.subspace_test import SubspaceTest

TITLE = "What Makes a Set a Subspace?"
PASS_HEADING = "A plane through the origin"
FAIL_HEADING = "The same plane, shifted"
KEY_IDEA = "A subspace contains 0 and is closed under addition and scalar multiplication."

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
PLANE_COLOR = "#4FC3F7"
U_COLOR = "#FFB74D"
V_COLOR = "#C792EA"
SUM_COLOR = "#81C995"
SCALE_COLOR = "#F4D35E"


class SubspaceTestPresentation(ThreeDScene):
    """Contrast a genuine subspace with a shifted plane that fails closure."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=66 * DEGREES, theta=-54 * DEGREES, zoom=0.95)

        model = SubspaceTest()
        good = model.through_origin(scale=1.7)
        bad = model.shifted(scale=1.7)

        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-2, 4, 1),
            x_length=8.2,
            y_length=8.2,
            z_length=5.5,
        )
        title = Text(TITLE, font_size=38, color=TEXT).to_edge(UP, buff=0.28)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), FadeIn(axes))

        good_plane = self._plane(model.plane_corners(good.offset), axes, opacity=0.16)
        good_heading = Text(PASS_HEADING, font_size=28, color=TEXT).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(good_heading)
        self.play(FadeIn(good_plane), FadeIn(good_heading))

        origin_dot = self._dot_label(r"\mathbf 0", ORIGIN, axes, GREEN, LEFT + DOWN)
        self.play(FadeIn(origin_dot))
        self.wait(0.8)

        u_arrow = self._arrow(good.offset, good.point_u, axes, U_COLOR)
        v_arrow = self._arrow(good.offset, good.point_v, axes, V_COLOR)
        u_label = self._fixed_label(r"\mathbf u\in W", LEFT, U_COLOR)
        v_label = self._fixed_label(r"\mathbf v\in W", RIGHT, V_COLOR)
        self.play(Create(u_arrow), Create(v_arrow), FadeIn(u_label), FadeIn(v_label))
        self.wait(0.8)

        sum_arrow = self._arrow(good.offset, good.sum_point, axes, SUM_COLOR)
        sum_text = self._fixed_statement(r"\mathbf u+\mathbf v\in W", GREEN)
        self.play(Create(sum_arrow), FadeIn(sum_text))
        self.wait(1.4)
        self.play(FadeOut(sum_arrow), FadeOut(sum_text))

        scaled_arrow = self._arrow(good.offset, good.scaled_point, axes, SCALE_COLOR)
        scale_text = self._fixed_statement(r"c\mathbf u\in W", GREEN)
        self.play(Create(scaled_arrow), FadeIn(scale_text))
        self.wait(1.4)

        pass_badge = Text("PASSES THE SUBSPACE TEST", font_size=28, color=GREEN).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(pass_badge)
        self.play(FadeOut(good_heading), FadeOut(u_label), FadeOut(v_label), FadeOut(scale_text), FadeIn(pass_badge))
        self.wait(1.6)

        self.play(
            FadeOut(origin_dot), FadeOut(u_arrow), FadeOut(v_arrow), FadeOut(scaled_arrow),
            FadeOut(pass_badge), FadeOut(good_plane),
        )

        bad_plane = self._plane(model.plane_corners(bad.offset), axes, opacity=0.16)
        bad_heading = Text(FAIL_HEADING, font_size=28, color=TEXT).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(bad_heading)
        self.play(FadeIn(bad_plane), FadeIn(bad_heading))

        zero_missing = MathTex(r"\mathbf 0\notin S", font_size=38, color=RED).to_corner(LEFT + DOWN, buff=0.48)
        self.add_fixed_in_frame_mobjects(zero_missing)
        self.play(FadeIn(zero_missing))
        self.wait(1.1)

        bad_u = self._arrow(bad.offset, bad.point_u, axes, U_COLOR)
        bad_v = self._arrow(bad.offset, bad.point_v, axes, V_COLOR)
        self.play(Create(bad_u), Create(bad_v))

        bad_sum = self._arrow(np.zeros(3), bad.sum_point, axes, SUM_COLOR)
        bad_sum_text = MathTex(r"\mathbf p+\mathbf q\notin S", font_size=38, color=RED).to_corner(RIGHT + DOWN, buff=0.48)
        self.add_fixed_in_frame_mobjects(bad_sum_text)
        self.play(Create(bad_sum), FadeIn(bad_sum_text))
        self.wait(1.3)
        self.play(FadeOut(bad_sum), FadeOut(bad_sum_text))

        bad_scale = self._arrow(np.zeros(3), bad.scaled_point, axes, SCALE_COLOR)
        bad_scale_text = MathTex(r"2\mathbf p\notin S", font_size=38, color=RED).to_corner(RIGHT + DOWN, buff=0.48)
        self.add_fixed_in_frame_mobjects(bad_scale_text)
        self.play(Create(bad_scale), FadeIn(bad_scale_text))
        self.wait(1.4)

        fail_badge = Text("FAILS THE SUBSPACE TEST", font_size=28, color=RED).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(fail_badge)
        self.play(FadeOut(bad_heading), FadeOut(zero_missing), FadeOut(bad_scale_text), FadeIn(fail_badge))
        self.wait(1.6)

        self.play(FadeOut(bad_u), FadeOut(bad_v), FadeOut(bad_scale), FadeOut(bad_plane), FadeOut(fail_badge))

        test = VGroup(
            MathTex(r"1.\quad \mathbf 0\in W", color=WHITE, font_size=40),
            MathTex(r"2.\quad \mathbf u,\mathbf v\in W\Rightarrow\mathbf u+\mathbf v\in W", color=WHITE, font_size=40),
            MathTex(r"3.\quad \mathbf u\in W,\ c\in\mathbb R\Rightarrow c\mathbf u\in W", color=WHITE, font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(ORIGIN)
        key_idea = Text(KEY_IDEA, font_size=26, color=MUTED).to_edge(DOWN, buff=0.36)
        self.add_fixed_in_frame_mobjects(test, key_idea)
        self.play(FadeOut(axes), FadeIn(test), FadeIn(key_idea))
        self.wait(3.2)

    @staticmethod
    def _plane(corners: np.ndarray, axes: ThreeDAxes, opacity: float) -> Polygon:
        return Polygon(
            *(axes.c2p(*corner) for corner in corners),
            color=PLANE_COLOR,
            fill_color=PLANE_COLOR,
            fill_opacity=opacity,
            stroke_opacity=0.38,
        )

    @staticmethod
    def _arrow(start: np.ndarray, end: np.ndarray, axes: ThreeDAxes, color: str) -> Arrow:
        return Arrow(
            axes.c2p(*start),
            axes.c2p(*end),
            color=color,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.16,
        )

    @staticmethod
    def _dot_label(tex: str, point: np.ndarray, axes: ThreeDAxes, color, direction) -> VGroup:
        from manim import Dot3D
        dot = Dot3D(axes.c2p(*point), radius=0.065, color=color)
        label = MathTex(tex, font_size=32, color=color).next_to(dot, direction, buff=0.12)
        return VGroup(dot, label)

    def _fixed_label(self, tex: str, side, color: str) -> MathTex:
        label = MathTex(tex, font_size=34, color=color)
        label.to_corner(side + UP, buff=0.45)
        self.add_fixed_in_frame_mobjects(label)
        return label

    def _fixed_statement(self, tex: str, color) -> MathTex:
        statement = MathTex(tex, font_size=38, color=color).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(statement)
        return statement
