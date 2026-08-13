"""CP152: Orthonormal Sets."""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    Create,
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    GREY_B,
    GREY_D,
    MathTex,
    Matrix,
    ORANGE,
    Rectangle,
    ReplacementTransform,
    RIGHT,
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
except ImportError:  # pragma: no cover - compatibility shim
    from manim.opengl import OpenGLArrow as Arrow3D

from engine.orthonormal_sets import OrthonormalSetsLesson


class OrthonormalSetsPresentation(ThreeDScene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Orthonormal Sets"
    SCENE_REVISION = "cp152_r2_slower_transitions"
    TRANSITION_TIME = 1.35
    EMPHASIS_TIME = 1.15
    HOLD_TIME = 2.6
    LONG_HOLD_TIME = 3.0


    def construct(self) -> None:
        self.lesson = OrthonormalSetsLesson()
        banner, lesson_title = self._header()
        self.lesson_title_mobject = lesson_title
        self.add_fixed_in_frame_mobjects(banner, lesson_title)
        self.add(banner, lesson_title)

        self._from_orthogonal_to_orthonormal()
        self._definition_card()
        self._normalization_card()
        self._gram_matrix_card()
        self._coordinates_card()
        self._projection_bridge_card()

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
        return VGroup(banner_box, banner_text), lesson_title

    def _vector3(self, axes: ThreeDAxes, end: np.ndarray, color: str) -> Arrow3D:
        return Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(*end),
            color=color,
            resolution=8,
            thickness=0.025,
            base_radius=0.04,
            height=0.14,
        )

    def _set_camera_default(self) -> None:
        self.set_camera_orientation(phi=58 * DEGREES, theta=-15 * DEGREES, zoom=0.90)

    def _from_orthogonal_to_orthonormal(self) -> None:
        heading = Text(
            "Orthogonality separates directions.",
            font_size=30,
            color=WHITE,
        ).next_to(self.lesson_title_mobject, DOWN, buff=0.26)
        question = Text(
            "What changes if every vector also has length 1?",
            font_size=32,
            color=YELLOW,
        ).move_to(UP * 0.35)
        caption = Text(
            "We keep the directions and standardize the lengths.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(heading, question, caption)
        self.play(FadeIn(heading), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(question), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, question, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, question, caption)

    def _definition_card(self) -> None:
        heading = Text("Definition", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        formula = MathTex(self.lesson.DEFINITION, font_size=34).move_to(UP * 0.30)
        if formula.width > 12.2:
            formula.scale_to_fit_width(12.2)
        compact = MathTex(self.lesson.KRONECKER, font_size=42, color=YELLOW).move_to(DOWN * 0.72)
        caption = Text(
            "Different vectors are perpendicular; each vector has unit length.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(heading, formula, compact, caption)
        self.play(FadeIn(heading), FadeIn(formula), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(compact), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, formula, compact, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, formula, compact, caption)

    def _normalization_card(self) -> None:
        self._set_camera_default()
        axes = ThreeDAxes(
            x_range=(-0.5, 2.8, 1),
            y_range=(-0.5, 2.8, 1),
            z_range=(-0.5, 2.8, 1),
            x_length=3.9,
            y_length=3.9,
            z_length=3.9,
        ).shift(RIGHT * 2.60 + DOWN * 2.45)
        scaled = self.lesson.scaled_orthogonal_example()
        unit = self.lesson.normalized_example()
        old_arrows = VGroup(
            self._vector3(axes, scaled.vectors[0], BLUE),
            self._vector3(axes, scaled.vectors[1], GREEN),
            self._vector3(axes, scaled.vectors[2], ORANGE),
        )
        unit_arrows = VGroup(
            self._vector3(axes, unit.vectors[0], BLUE),
            self._vector3(axes, unit.vectors[1], GREEN),
            self._vector3(axes, unit.vectors[2], ORANGE),
        )
        heading = Text("Normalize without changing direction", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        rules = VGroup(
            MathTex(r"\mathbf{q}_1=\frac{\mathbf{v}_1}{\|\mathbf{v}_1\|}", font_size=35),
            MathTex(r"\mathbf{q}_2=\frac{\mathbf{v}_2}{\|\mathbf{v}_2\|}", font_size=35),
            MathTex(r"\mathbf{q}_3=\frac{\mathbf{v}_3}{\|\mathbf{v}_3\|}", font_size=35),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.05 + UP * 0.10)
        caption = Text(
            "Scaling changes length, not direction, so the right angles remain.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(heading, rules, caption)
        self.play(FadeIn(heading), Create(axes), run_time=self.TRANSITION_TIME)
        for arrow in old_arrows:
            self.play(Create(arrow), run_time=0.95)
        self.move_camera(phi=62 * DEGREES, theta=28 * DEGREES, zoom=0.92, run_time=3.4)
        self.play(FadeIn(rules), run_time=self.TRANSITION_TIME)
        for old, new in zip(old_arrows, unit_arrows):
            self.play(ReplacementTransform(old, new), run_time=0.95)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(axes, unit_arrows, heading, rules, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, rules, caption)

    def _gram_matrix_card(self) -> None:
        heading = Text("All pairwise dot products at once", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        qdef = MathTex(r"Q=[\,\mathbf{q}_1\ \mathbf{q}_2\ \mathbf{q}_3\,]", font_size=38).move_to(
            UP * 1.05
        )
        gram = MathTex(
            r"Q^TQ="
            r"\begin{bmatrix}"
            r"\mathbf{q}_1\!\cdot\!\mathbf{q}_1&\mathbf{q}_1\!\cdot\!\mathbf{q}_2&\mathbf{q}_1\!\cdot\!\mathbf{q}_3\\"
            r"\mathbf{q}_2\!\cdot\!\mathbf{q}_1&\mathbf{q}_2\!\cdot\!\mathbf{q}_2&\mathbf{q}_2\!\cdot\!\mathbf{q}_3\\"
            r"\mathbf{q}_3\!\cdot\!\mathbf{q}_1&\mathbf{q}_3\!\cdot\!\mathbf{q}_2&\mathbf{q}_3\!\cdot\!\mathbf{q}_3"
            r"\end{bmatrix}"
            r"=I",
            font_size=31,
        ).move_to(DOWN * 0.15)
        if gram.width > 11.7:
            gram.scale_to_fit_width(11.7)
        identity = MathTex(self.lesson.MATRIX_IDENTITY, font_size=44, color=YELLOW).move_to(DOWN * 1.55)
        box = SurroundingRectangle(identity, buff=0.16, color=WHITE)
        caption = Text(
            "Orthonormal columns have identity as their Gram matrix.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.18)
        self.add_fixed_in_frame_mobjects(heading, qdef, gram, identity, box, caption)
        self.play(FadeIn(heading), FadeIn(qdef), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(gram), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(identity), Create(box), FadeIn(caption), run_time=self.TRANSITION_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, qdef, gram, identity, box, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, qdef, gram, identity, box, caption)

    def _coordinates_card(self) -> None:
        heading = Text("Why unit length is so useful", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        line1 = MathTex(
            r"\mathbf{x}=c_1\mathbf{q}_1+\cdots+c_k\mathbf{q}_k",
            font_size=39,
        )
        line2 = MathTex(r"\mathbf{q}_j\cdot\mathbf{x}", font_size=39)
        line3 = MathTex(
            r"=c_1(\mathbf{q}_j\cdot\mathbf{q}_1)+\cdots+c_k(\mathbf{q}_j\cdot\mathbf{q}_k)",
            font_size=34,
        )
        line4 = MathTex(r"=c_j", font_size=42, color=YELLOW)
        derivation = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.20).move_to(UP * 0.05)
        result = MathTex(self.lesson.COORDINATE_RULE, font_size=42).move_to(DOWN * 1.45)
        result_box = SurroundingRectangle(result, buff=0.18, color=WHITE)
        caption = Text(
            "With an orthonormal set, dot products read off the coordinates directly.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.18)
        self.add_fixed_in_frame_mobjects(heading, derivation, result, result_box, caption)
        self.play(FadeIn(heading), FadeIn(line1), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(line2), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(line3), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(line4), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(result), Create(result_box), FadeIn(caption), run_time=self.TRANSITION_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(FadeOut(VGroup(heading, derivation, result, result_box, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, derivation, result, result_box, caption)

    def _projection_bridge_card(self) -> None:
        heading = Text("Next question", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        question = Text(
            "How much of a vector points in one chosen direction?",
            font_size=32,
            color=YELLOW,
        ).move_to(UP * 0.78)
        scalar = MathTex(r"\mathbf{q}\cdot\mathbf{x}", font_size=48).move_to(DOWN * 0.15)
        note = Text(
            "For a unit vector q, this dot product gives the signed scalar amount along q.",
            font_size=23,
            color=GREY_B,
        ).move_to(DOWN * 1.15)
        if note.width > 12.0:
            note.scale_to_fit_width(12.0)
        caption = Text(
            "Turning that scalar amount into a vector leads to projection.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.30)
        self.add_fixed_in_frame_mobjects(heading, question, scalar, note, caption)
        self.play(FadeIn(heading), FadeIn(question), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(scalar), FadeIn(note), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
