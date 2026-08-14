"""CP156: Orthogonal Complements."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    BLUE,
    Create,
    DashedLine,
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    GREY_B,
    GREY_D,
    LEFT,
    Line,
    MathTex,
    NumberPlane,
    ORANGE,
    Polygon,
    Rectangle,
    RIGHT,
    Scene,
    SurroundingRectangle,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)
try:
    from manim import Arrow3D
except ImportError:  # pragma: no cover
    from manim.opengl import OpenGLArrow as Arrow3D

from engine.orthogonal_complements import OrthogonalComplementsLesson


class OrthogonalComplementsPresentation(ThreeDScene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Orthogonal Complements"
    SCENE_REVISION = "cp156_r22_card4_caption_left_and_raise"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.05
    HOLD_TIME = 2.4

    def construct(self) -> None:
        self.lesson = OrthogonalComplementsLesson()
        self.snapshot = self.lesson.residual_snapshot()
        self.plane_snapshot = self.lesson.plane_snapshot()
        banner, lesson_title = self._header()
        self.lesson_title_mobject = lesson_title
        self.add_fixed_in_frame_mobjects(banner, lesson_title)
        self.add(banner, lesson_title)

        self._residual_motivation_card()
        self._definition_card()
        self._line_example_card()
        self._plane_example_card()
        self._decomposition_card()
        self._bridge_card()

    def _header(self) -> tuple[VGroup, Text]:
        banner_box = Rectangle(
            width=13.5,
            height=0.58,
            stroke_width=0,
            fill_color=GREY_D,
            fill_opacity=0.96,
        ).to_edge(UP, buff=0.08)
        banner_text = Text(self.CHAPTER_BANNER, font_size=28, color=WHITE).move_to(banner_box)
        lesson_title = Text(self.LESSON_TITLE, font_size=31, color=YELLOW).next_to(
            banner_box, DOWN, buff=0.18
        )
        if lesson_title.width > 11.8:
            lesson_title.scale_to_fit_width(11.8)
        return VGroup(banner_box, banner_text), lesson_title

    @staticmethod
    def _plane2d() -> NumberPlane:
        return NumberPlane(
            x_range=(-1.5, 5.5, 1),
            y_range=(-2.5, 4.5, 1),
            x_length=6.7,
            y_length=5.5,
            background_line_style={"stroke_opacity": 0.20},
            axis_config={"stroke_opacity": 0.55},
        ).shift(LEFT * 2.85 + DOWN * 0.55)

    @staticmethod
    def _square_plane2d() -> NumberPlane:
        return NumberPlane(
            x_range=(-1.5, 5.5, 1),
            y_range=(-2.5, 4.5, 1),
            x_length=5.9,
            y_length=5.9,
            background_line_style={"stroke_opacity": 0.20},
            axis_config={"stroke_opacity": 0.55},
        ).shift(LEFT * 2.10 + DOWN * 0.20)

    @staticmethod
    def _arrow(plane: NumberPlane, vector: np.ndarray, color) -> Arrow:
        return Arrow(plane.c2p(0, 0), plane.c2p(*vector), buff=0, color=color, stroke_width=6)

    @staticmethod
    def _span_line(plane: NumberPlane, direction: np.ndarray, color=WHITE) -> Line:
        unit = direction / np.linalg.norm(direction)
        start = plane.c2p(*(unit * -4.8))
        end = plane.c2p(*(unit * 4.8))
        return Line(start, end, color=color, stroke_width=3)

    @staticmethod
    def _label_for_arrow(text: str, arrow: Arrow, color, offset=UP * 0.2) -> MathTex:
        return MathTex(text, font_size=31, color=color).move_to(arrow.get_end() + offset)

    @staticmethod
    def _right_angle_marker(plane: NumberPlane, point: np.ndarray, along: np.ndarray, perp: np.ndarray) -> VGroup:
        along_u = along / np.linalg.norm(along)
        perp_u = perp / np.linalg.norm(perp)
        a = point + 0.24 * along_u
        c = point + 0.24 * perp_u
        b = a + 0.24 * perp_u
        return VGroup(
            Line(plane.c2p(*a), plane.c2p(*b), color=WHITE, stroke_width=3),
            Line(plane.c2p(*c), plane.c2p(*b), color=WHITE, stroke_width=3),
        )

    def _set_camera_default(self) -> None:
        self.set_camera_orientation(phi=58 * DEGREES, theta=-15 * DEGREES, zoom=0.88)

    def _residual_motivation_card(self) -> None:
        heading = Text(
            "Projection leaves a perpendicular residual",
            font_size=28,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        plane = self._square_plane2d().shift(LEFT * 0.10 + DOWN * 0.05)
        w_line = self._span_line(plane, self.snapshot.w_direction)
        x_arrow = self._arrow(plane, self.snapshot.x, ORANGE)
        p_arrow = self._arrow(plane, self.snapshot.projection, GREEN)
        r_arrow = Arrow(
            plane.c2p(*self.snapshot.projection),
            plane.c2p(*self.snapshot.x),
            buff=0,
            color=BLUE,
            stroke_width=6,
        )
        drop = DashedLine(plane.c2p(*self.snapshot.projection), plane.c2p(*self.snapshot.x), color=BLUE)
        right_angle = self._right_angle_marker(plane, self.snapshot.projection, self.snapshot.w_direction, self.snapshot.residual)
        w_label = MathTex(r"W", font_size=32, color=WHITE).move_to(plane.c2p(1.55, 2.45))
        x_label = self._label_for_arrow(r"\mathbf x", x_arrow, ORANGE, offset=RIGHT * 0.42 + UP * 0.22)
        p_label = self._label_for_arrow(r"\mathbf p", p_arrow, GREEN, offset=LEFT * 0.38 + UP * 0.18)
        r_label = MathTex(r"\mathbf r", font_size=31, color=BLUE).move_to(plane.c2p(3.10, 1.78))
        formula = MathTex(self.lesson.SPLIT, font_size=37).move_to(RIGHT * 3.4 + UP * 0.2)
        caption = Text(
            "The residual points in a direction perpendicular to the subspace.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.36)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), Create(plane), Create(w_line), FadeIn(w_label), run_time=self.TRANSITION_TIME)
        self.play(Create(x_arrow), FadeIn(x_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(p_arrow), FadeIn(p_label), Create(drop), Create(r_arrow), Create(right_angle), FadeIn(r_label), run_time=self.TRANSITION_TIME)
        self.add_fixed_in_frame_mobjects(formula, caption)
        self.play(FadeIn(formula), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(
            FadeOut(VGroup(plane, w_line, x_arrow, p_arrow, r_arrow, drop, right_angle)),
            FadeOut(VGroup(heading, w_label, x_label, p_label, r_label, formula, caption)),
            run_time=self.TRANSITION_TIME,
        )
        self.remove_fixed_in_frame_mobjects(heading, formula, caption)

    def _definition_card(self) -> None:
        heading = Text("Definition", font_size=30, color=WHITE).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        definition = MathTex(self.lesson.DEFINITION, font_size=38).move_to(UP * 0.3)
        box = SurroundingRectangle(definition, buff=0.18, color=WHITE)
        caption = Text(
            "W-perp contains every vector orthogonal to every vector in W.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)
        self.add_fixed_in_frame_mobjects(heading, definition, box)
        self.play(FadeIn(heading), FadeIn(definition), Create(box), run_time=self.TRANSITION_TIME)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, definition, box, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, definition, box, caption)

    def _line_example_card(self) -> None:
        heading = Text("A line and its orthogonal complement", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        plane = self._square_plane2d().shift(RIGHT * 0.78 + UP * 0.36)
        w_line = self._span_line(plane, self.snapshot.w_direction, color=WHITE)
        wp_line = self._span_line(plane, self.snapshot.wp_direction, color=YELLOW)
        w_label = MathTex(r"W=\operatorname{span}(1,1)", font_size=31, color=WHITE).move_to(plane.c2p(2.95, 2.55))
        wp_label = MathTex(r"W^\perp=\operatorname{span}(1,-1)", font_size=31, color=YELLOW).move_to(plane.c2p(4.2, -1.65))
        statement = VGroup(
            MathTex(r"\mathbf w\in W", font_size=35, color=WHITE),
            MathTex(r"\mathbf v\in W^\perp", font_size=35, color=YELLOW),
            MathTex(r"\mathbf v\cdot\mathbf w=0", font_size=39, color=GREEN),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.55 + UP * 0.15)
        caption = Text(
            "In R^2, the orthogonal complement of a line is another perpendicular line.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), Create(plane), Create(w_line), Create(wp_line), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(w_label), FadeIn(wp_label), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(statement, caption)
        self.play(FadeIn(statement), FadeIn(caption), run_time=self.TRANSITION_TIME)
        self.wait(self.HOLD_TIME)
        self.play(
            FadeOut(VGroup(plane, w_line, wp_line)),
            FadeOut(VGroup(heading, w_label, wp_label, statement, caption)),
            run_time=self.TRANSITION_TIME,
        )
        self.remove_fixed_in_frame_mobjects(heading, statement, caption)

    def _plane_example_card(self) -> None:
        self.set_camera_orientation(phi=56 * DEGREES, theta=-10 * DEGREES, zoom=0.66)
        heading = Text("A plane and its orthogonal complement", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = ThreeDAxes(
            x_range=(-0.5, 3.2, 1),
            y_range=(-0.5, 3.2, 1),
            z_range=(-0.5, 3.4, 1),
            x_length=5.05,
            y_length=5.05,
            z_length=5.00,
        ).shift(RIGHT * 4.82 + DOWN * 0.22)
        corners = [axes.c2p(0, 0, 0), axes.c2p(2.6, 0, 0), axes.c2p(2.6, 2.6, 0), axes.c2p(0, 2.6, 0)]
        plane_patch = Polygon(*corners, color=GREY_B, fill_color=GREY_B, fill_opacity=0.28, stroke_width=1.5)
        a1 = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(*self.plane_snapshot.plane_basis_1), color=WHITE, resolution=8, thickness=0.025, base_radius=0.04, height=0.14)
        a2 = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(*self.plane_snapshot.plane_basis_2), color=WHITE, resolution=8, thickness=0.025, base_radius=0.04, height=0.14)
        normal = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(0.0, 0.0, 1.55), color=YELLOW, resolution=8, thickness=0.03, base_radius=0.045, height=0.15)
        w_label = MathTex(r"W", font_size=34, color=WHITE).move_to(axes.c2p(1.78, 1.18, 0.24))
        wp_label = MathTex(r"W^\perp", font_size=34, color=YELLOW).move_to(axes.c2p(-0.92, 0.24, 1.14))
        camera_compensation = RIGHT * 0.44 + UP * 1.33
        wp_label_rotated_position = axes.c2p(-1.05, 0.20, 1.18) + camera_compensation
        statement = VGroup(
            MathTex(r"W=\{(x,y,0)\}", font_size=34, color=WHITE),
            MathTex(r"W^\perp=\operatorname{span}(0,0,1)", font_size=34, color=YELLOW),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 3.42 + UP * 0.55)
        caption = Text(
            "In R^3, the orthogonal complement\nof a plane is a line normal\nto the plane.",
            font_size=20,
            color=GREY_B,
            line_spacing=0.9,
        ).move_to(LEFT * 4.05 + DOWN * 1.76)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), Create(axes), FadeIn(plane_patch), run_time=self.TRANSITION_TIME)
        self.play(Create(a1), Create(a2), Create(normal), run_time=self.TRANSITION_TIME)
        self.add_fixed_orientation_mobjects(w_label, wp_label)
        self.add_fixed_in_frame_mobjects(statement, caption)
        self.play(FadeIn(w_label), FadeIn(wp_label), FadeIn(statement), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        geometry_group = VGroup(axes, plane_patch, a1, a2, normal, w_label)
        self.move_camera(
            phi=56 * DEGREES,
            theta=5 * DEGREES,
            zoom=0.66,
            added_anims=[
                geometry_group.animate.shift(camera_compensation),
                wp_label.animate.move_to(wp_label_rotated_position),
            ],
            run_time=2.6,
        )
        self.wait(1.8)
        self.play(
            FadeOut(VGroup(axes, plane_patch, a1, a2, normal, w_label, wp_label)),
            FadeOut(VGroup(heading, statement, caption)),
            run_time=self.TRANSITION_TIME,
        )
        self.remove_fixed_orientation_mobjects(w_label, wp_label)
        self.remove_fixed_in_frame_mobjects(heading, statement, caption)

    def _decomposition_card(self) -> None:
        heading = Text("Every vector splits uniquely", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        line1 = MathTex(self.lesson.DECOMPOSITION, font_size=43).move_to(UP * 0.65)
        line2 = MathTex(self.lesson.SPLIT, font_size=39).move_to(UP * 0.02)
        line3 = MathTex(r"\text{and this decomposition is unique}", font_size=35, color=YELLOW).move_to(DOWN * 0.62)
        line4 = MathTex(self.lesson.DIMENSION_FACT, font_size=37, color=GREEN).move_to(DOWN * 1.38)
        caption = Text(
            "Orthogonal complements organize the whole space into a direct sum.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.16)
        self.add_fixed_in_frame_mobjects(heading, line1)
        self.play(FadeIn(heading), FadeIn(line1), run_time=self.TRANSITION_TIME)
        self.add_fixed_in_frame_mobjects(line2)
        self.play(FadeIn(line2), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(line3)
        self.play(FadeIn(line3), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(line4, caption)
        self.play(FadeIn(line4), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, line1, line2, line3, line4, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, line1, line2, line3, line4, caption)

    def _bridge_card(self) -> None:
        heading = Text("Next question", font_size=30, color=WHITE).next_to(self.lesson_title_mobject, DOWN, buff=0.24)
        prompt = Text(self.lesson.bridge_prompt, font_size=31, color=YELLOW).move_to(UP * 1.00)
        if prompt.width > 11.4:
            prompt.scale_to_fit_width(11.4)
        equations = VGroup(
            MathTex(r"\text{Given a spanning set }\{\mathbf v_1,\ldots,\mathbf v_k\}", font_size=35),
            MathTex(r"\text{can we turn it into orthogonal directions?}", font_size=35),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 0.18)
        caption = Text(
            "That leads naturally to Gram-Schmidt orthogonalization.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(heading, prompt)
        self.play(FadeIn(heading), FadeIn(prompt), run_time=self.TRANSITION_TIME)
        self.add_fixed_in_frame_mobjects(equations)
        self.play(FadeIn(equations), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
