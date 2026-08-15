"""CP159: Gram-Schmidt in R^3."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow3D,
    Create,
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    GREY_B,
    GREY_D,
    LEFT,
    MathTex,
    ORANGE,
    PURPLE,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    Scene,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    BLUE,
    TEAL,
)

from engine.gram_schmidt_three_vectors import GramSchmidtThreeVectorsLesson


class GramSchmidtThreeVectorsPresentation(ThreeDScene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Gram-Schmidt in R^3"
    SCENE_REVISION = "cp159_r6_card5_pairwise_views"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.05
    HOLD_TIME = 2.2

    def construct(self) -> None:
        self.lesson = GramSchmidtThreeVectorsLesson()
        self.snapshot = self.lesson.snapshot()
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES, zoom=0.84)
        self.banner, self.lesson_title_mobject = self._header()
        self.add_fixed_in_frame_mobjects(self.banner, self.lesson_title_mobject)
        self.add(self.banner, self.lesson_title_mobject)

        self._starting_triple_card()
        self._build_u1_u2_card()
        self._remove_u1_component_from_v3_card()
        self._remove_u2_component_from_v3_card()
        self._orthogonal_frame_card()
        self._synthesis_card()


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
    def _axes3d() -> ThreeDAxes:
        return ThreeDAxes(
            x_range=(-0.5, 4.5, 1),
            y_range=(-2.5, 3.5, 1),
            z_range=(-2.0, 3.5, 1),
            x_length=5.35,
            y_length=6.15,
            z_length=5.35,
            axis_config={"stroke_opacity": 0.72, "stroke_width": 2.0},
        ).shift(LEFT * 2.2 + DOWN * 2.45)

    @staticmethod
    def _arrow(axes: ThreeDAxes, vector: np.ndarray, color) -> Arrow3D:
        return Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(*vector),
            color=color,
            thickness=0.02,
            base_radius=0.05,
        )

    @staticmethod
    def _label(text: str, axes: ThreeDAxes, point: np.ndarray, color, offset: np.ndarray) -> MathTex:
        return MathTex(text, font_size=30, color=color).move_to(axes.c2p(*point) + offset)

    def _starting_triple_card(self) -> None:
        heading = Text("Start with three independent vectors", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._axes3d()
        v1_arrow = self._arrow(axes, self.snapshot.v1, ORANGE)
        v2_arrow = self._arrow(axes, self.snapshot.v2, PURPLE)
        v3_arrow = self._arrow(axes, self.snapshot.v3, BLUE)
        v1_label = self._label(r"\mathbf v_1", axes, self.snapshot.v1, ORANGE, np.array([-0.62, 0.48, 0.0]))
        v2_label = self._label(r"\mathbf v_2", axes, self.snapshot.v2, PURPLE, np.array([0.52, -0.40, 0.0]))
        v3_label = self._label(r"\mathbf v_3", axes, self.snapshot.v3, BLUE, np.array([0.66, 0.38, 0.0]))
        equations = VGroup(
            MathTex(r"\mathbf v_1=(2,2,0)", font_size=34, color=ORANGE),
            MathTex(r"\mathbf v_2=(2,0,2)", font_size=34, color=PURPLE),
            MathTex(r"\mathbf v_3=(3,-1,1)", font_size=34, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.35 + UP * 0.18)
        caption = Text(
            "Gram-Schmidt will keep the span but replace these with orthogonal directions.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), Create(axes), run_time=self.TRANSITION_TIME)
        self.add_fixed_orientation_mobjects(v1_label, v2_label, v3_label)
        self.play(
            Create(v1_arrow), FadeIn(v1_label),
            Create(v2_arrow), FadeIn(v2_label),
            Create(v3_arrow), FadeIn(v3_label),
            run_time=self.EMPHASIS_TIME,
        )
        self.add_fixed_in_frame_mobjects(equations, caption)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(axes, v1_arrow, v2_arrow, v3_arrow, v1_label, v2_label, v3_label, heading, equations, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_orientation_mobjects(v1_label, v2_label, v3_label)
        self.remove_fixed_in_frame_mobjects(heading, equations, caption)

    def _build_u1_u2_card(self) -> None:
        heading = Text("First make u1 and u2", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._axes3d()
        u1_arrow = self._arrow(axes, self.snapshot.u1, ORANGE)
        proj_arrow = self._arrow(axes, self.snapshot.proj_v2_on_u1, GREEN)
        u2_arrow = self._arrow(axes, self.snapshot.u2, PURPLE)
        u1_label = self._label(r"\mathbf u_1", axes, self.snapshot.u1, ORANGE, np.array([-0.62, 0.48, 0.0]))
        proj_label = self._label(r"\operatorname{proj}_{\mathbf u_1}\mathbf v_2", axes, self.snapshot.proj_v2_on_u1, GREEN, np.array([-0.40, 0.52, 0.0]))
        u2_label = self._label(r"\mathbf u_2", axes, self.snapshot.u2, PURPLE, np.array([0.52, -0.38, 0.0]))
        equations = VGroup(
            MathTex(r"\mathbf u_1=\mathbf v_1=(2,2,0)", font_size=33, color=ORANGE),
            MathTex(r"\operatorname{proj}_{\mathbf u_1}\mathbf v_2=(1,1,0)", font_size=33, color=GREEN),
            MathTex(r"\mathbf u_2=\mathbf v_2-\operatorname{proj}_{\mathbf u_1}\mathbf v_2=(1,-1,2)", font_size=31, color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.45 + UP * 0.15)
        caption = Text(
            "The two-vector step is the same as before; now it prepares us for the third vector.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), Create(axes), run_time=self.TRANSITION_TIME)
        self.add_fixed_orientation_mobjects(u1_label)
        self.play(Create(u1_arrow), FadeIn(u1_label), run_time=self.EMPHASIS_TIME)
        self.add_fixed_orientation_mobjects(proj_label)
        self.add_fixed_in_frame_mobjects(equations[0], equations[1])
        self.play(Create(proj_arrow), FadeIn(proj_label), FadeIn(equations[0]), FadeIn(equations[1]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_orientation_mobjects(u2_label)
        self.add_fixed_in_frame_mobjects(equations[2], caption)
        self.play(Create(u2_arrow), FadeIn(u2_label), FadeIn(equations[2]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(axes, u1_arrow, proj_arrow, u2_arrow, u1_label, proj_label, u2_label, heading, equations, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_orientation_mobjects(u1_label, proj_label, u2_label)
        self.remove_fixed_in_frame_mobjects(heading, equations[0], equations[1], equations[2], caption)

    def _remove_u1_component_from_v3_card(self) -> None:
        heading = Text("Start with v3 and remove its u1 component", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._axes3d()
        u1_arrow = self._arrow(axes, self.snapshot.u1, ORANGE)
        u2_arrow = self._arrow(axes, self.snapshot.u2, PURPLE)
        v3_arrow = self._arrow(axes, self.snapshot.v3, BLUE)
        proj31_arrow = self._arrow(axes, self.snapshot.proj_v3_on_u1, GREEN)
        w3_arrow = self._arrow(axes, self.snapshot.w3, TEAL)
        u1_label = self._label(r"\mathbf u_1", axes, self.snapshot.u1, ORANGE, np.array([-0.62, 0.48, 0.0]))
        u2_label = self._label(r"\mathbf u_2", axes, self.snapshot.u2, PURPLE, np.array([0.52, -0.38, 0.0]))
        v3_label = self._label(r"\mathbf v_3", axes, self.snapshot.v3, BLUE, np.array([0.66, 0.38, 0.0]))
        w3_label = self._label(r"\mathbf w_3", axes, self.snapshot.w3, TEAL, np.array([0.56, 0.40, 0.0]))
        equations = VGroup(
            MathTex(r"\operatorname{proj}_{\mathbf u_1}\mathbf v_3=(1,1,0)", font_size=33, color=GREEN),
            MathTex(r"\mathbf w_3=\mathbf v_3-\operatorname{proj}_{\mathbf u_1}\mathbf v_3", font_size=31),
            MathTex(r"=(2,-2,1)", font_size=33, color=TEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.35 + UP * 0.15)
        caption = Text(
            "After the first subtraction, one earlier component is gone, but w3 may still lean along u2.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), Create(axes), run_time=self.TRANSITION_TIME)
        self.add_fixed_orientation_mobjects(u1_label, u2_label)
        self.play(Create(u1_arrow), FadeIn(u1_label), Create(u2_arrow), FadeIn(u2_label), run_time=self.EMPHASIS_TIME)
        self.add_fixed_orientation_mobjects(v3_label)
        self.play(Create(v3_arrow), FadeIn(v3_label), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(equations[0])
        self.play(Create(proj31_arrow), FadeIn(equations[0]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_orientation_mobjects(w3_label)
        self.add_fixed_in_frame_mobjects(equations[1], equations[2], caption)
        self.play(ReplacementTransform(v3_arrow, w3_arrow), FadeOut(v3_label), FadeIn(w3_label), FadeIn(equations[1]), FadeIn(equations[2]), FadeIn(caption), run_time=self.TRANSITION_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(axes, u1_arrow, u2_arrow, proj31_arrow, w3_arrow, u1_label, u2_label, w3_label, heading, equations, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_orientation_mobjects(u1_label, u2_label, v3_label, w3_label)
        self.remove_fixed_in_frame_mobjects(heading, equations[0], equations[1], equations[2], caption)

    def _remove_u2_component_from_v3_card(self) -> None:
        heading = Text("Now remove the u2 component", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._axes3d()
        u1_arrow = self._arrow(axes, self.snapshot.u1, ORANGE)
        u2_arrow = self._arrow(axes, self.snapshot.u2, PURPLE)
        w3_arrow = self._arrow(axes, self.snapshot.w3, TEAL)
        proj32_arrow = self._arrow(axes, self.snapshot.proj_v3_on_u2, GREEN)
        u3_arrow = self._arrow(axes, self.snapshot.u3, YELLOW)
        u1_label = self._label(r"\mathbf u_1", axes, self.snapshot.u1, ORANGE, np.array([-0.62, 0.48, 0.0]))
        u2_label = self._label(r"\mathbf u_2", axes, self.snapshot.u2, PURPLE, np.array([0.52, -0.38, 0.0]))
        w3_label = self._label(r"\mathbf w_3", axes, self.snapshot.w3, TEAL, np.array([0.56, 0.40, 0.0]))
        u3_label = self._label(r"\mathbf u_3", axes, self.snapshot.u3, YELLOW, np.array([0.48, -0.42, 0.0]))
        equations = VGroup(
            MathTex(r"\operatorname{proj}_{\mathbf u_2}\mathbf v_3=(1,-1,2)", font_size=33, color=GREEN),
            MathTex(r"\mathbf u_3=\mathbf v_3-\operatorname{proj}_{\mathbf u_1}\mathbf v_3-\operatorname{proj}_{\mathbf u_2}\mathbf v_3", font_size=29),
            MathTex(r"=(1,-1,-1)", font_size=33, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20).move_to(RIGHT * 3.45 + UP * 0.12)
        caption = Text(
            "The third vector is the first one that must lose two earlier projection components.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), Create(axes), run_time=self.TRANSITION_TIME)
        self.add_fixed_orientation_mobjects(u1_label, u2_label)
        self.play(Create(u1_arrow), FadeIn(u1_label), Create(u2_arrow), FadeIn(u2_label), run_time=self.EMPHASIS_TIME)
        self.add_fixed_orientation_mobjects(w3_label)
        self.play(Create(w3_arrow), FadeIn(w3_label), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(equations[0])
        self.play(Create(proj32_arrow), FadeIn(equations[0]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_orientation_mobjects(u3_label)
        self.add_fixed_in_frame_mobjects(equations[1], equations[2], caption)
        self.play(ReplacementTransform(w3_arrow, u3_arrow), FadeOut(w3_label), FadeIn(u3_label), FadeIn(equations[1]), FadeIn(equations[2]), FadeIn(caption), run_time=self.TRANSITION_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(axes, u1_arrow, u2_arrow, proj32_arrow, u3_arrow, u1_label, u2_label, u3_label, heading, equations, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_orientation_mobjects(u1_label, u2_label, w3_label, u3_label)
        self.remove_fixed_in_frame_mobjects(heading, equations[0], equations[1], equations[2], caption)

    def _orthogonal_frame_card(self) -> None:
        heading = Text("Now the frame is orthogonal", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._axes3d()
        u1_arrow = self._arrow(axes, self.snapshot.u1, ORANGE)
        u2_arrow = self._arrow(axes, self.snapshot.u2, PURPLE)
        u3_arrow = self._arrow(axes, self.snapshot.u3, YELLOW)
        u1_label = self._label(r"\mathbf u_1", axes, self.snapshot.u1, ORANGE, np.array([-0.62, 0.48, 0.0]))
        u2_label = self._label(r"\mathbf u_2", axes, self.snapshot.u2, PURPLE, np.array([0.52, -0.38, 0.0]))
        u3_label = self._label(r"\mathbf u_3", axes, self.snapshot.u3, YELLOW, np.array([0.48, -0.42, 0.0]))
        equations = VGroup(
            MathTex(r"\mathbf u_1\cdot\mathbf u_2=0", font_size=34, color=GREEN),
            MathTex(r"\mathbf u_1\cdot\mathbf u_3=0", font_size=34, color=GREEN),
            MathTex(r"\mathbf u_2\cdot\mathbf u_3=0", font_size=34, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.40 + UP * 0.12)
        caption = Text(
            "Looking nearly along one vector makes the other two reveal a right angle.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), Create(axes), run_time=self.TRANSITION_TIME)
        self.add_fixed_orientation_mobjects(u1_label, u2_label, u3_label)
        self.play(
            Create(u1_arrow), FadeIn(u1_label),
            Create(u2_arrow), FadeIn(u2_label),
            Create(u3_arrow), FadeIn(u3_label),
            run_time=self.EMPHASIS_TIME,
        )
        self.add_fixed_in_frame_mobjects(equations[0], caption)
        self.play(FadeIn(equations[0]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.move_camera(phi=55 * DEGREES, theta=135 * DEGREES, zoom=0.88, run_time=1.8)
        self.wait(0.8)
        self.add_fixed_in_frame_mobjects(equations[1])
        self.play(FadeIn(equations[1]), run_time=0.8)
        self.move_camera(phi=37 * DEGREES, theta=-45 * DEGREES, zoom=0.88, run_time=1.8)
        self.wait(0.8)
        self.add_fixed_in_frame_mobjects(equations[2])
        self.play(FadeIn(equations[2]), run_time=0.8)
        self.move_camera(phi=88 * DEGREES, theta=45 * DEGREES, zoom=0.88, run_time=1.8)
        self.wait(self.HOLD_TIME)
        self.move_camera(phi=65 * DEGREES, theta=-40 * DEGREES, zoom=0.84, run_time=1.2)
        self.play(FadeOut(VGroup(axes, u1_arrow, u2_arrow, u3_arrow, u1_label, u2_label, u3_label, heading, equations, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_orientation_mobjects(u1_label, u2_label, u3_label)
        self.remove_fixed_in_frame_mobjects(heading, equations[0], equations[1], equations[2], caption)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES, zoom=0.84)

    def _synthesis_card(self) -> None:
        heading = Text("The reusable Gram-Schmidt pattern", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        formulas = VGroup(
            MathTex(r"\mathbf u_1=\mathbf v_1", font_size=37),
            MathTex(r"\mathbf u_2=\mathbf v_2-\operatorname{proj}_{\mathbf u_1}\mathbf v_2", font_size=35),
            MathTex(r"\mathbf u_3=\mathbf v_3-\operatorname{proj}_{\mathbf u_1}\mathbf v_3-\operatorname{proj}_{\mathbf u_2}\mathbf v_3", font_size=31),
            MathTex(self.lesson.GENERAL_STEP, font_size=31, color=YELLOW),
            MathTex(self.lesson.NORMALIZE_NOTE, font_size=30, color=GREEN),
        ).arrange(DOWN, buff=0.30).move_to(DOWN * 0.06)
        caption = Text(
            self.lesson.closing_prompt,
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.30)
        self.add_fixed_in_frame_mobjects(heading, formulas[0], formulas[1])
        self.play(FadeIn(heading), FadeIn(formulas[0]), FadeIn(formulas[1]), run_time=self.TRANSITION_TIME)
        self.add_fixed_in_frame_mobjects(formulas[2])
        self.play(FadeIn(formulas[2]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(formulas[3], formulas[4], caption)
        self.play(FadeIn(formulas[3]), FadeIn(formulas[4]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
