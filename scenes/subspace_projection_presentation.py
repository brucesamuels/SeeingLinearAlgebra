"""CP155: Projection onto a Subspace."""

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
    LEFT,
    MathTex,
    ORANGE,
    Polygon,
    Rectangle,
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
except ImportError:  # pragma: no cover - Manim compatibility shim
    from manim.opengl import OpenGLArrow as Arrow3D

from engine.subspace_projection import SubspaceProjectionLesson


class SubspaceProjectionPresentation(ThreeDScene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Projection onto a Subspace"
    SCENE_REVISION = "cp155_r4_card3_spacing_and_smoother_labels"
    TRANSITION_TIME = 1.35
    EMPHASIS_TIME = 1.15
    HOLD_TIME = 2.6
    LONG_HOLD_TIME = 3.0

    def construct(self) -> None:
        self.lesson = SubspaceProjectionLesson()
        self.snapshot = self.lesson.example()
        self.general_snapshot = self.lesson.general_basis_example()
        banner, lesson_title = self._header()
        self.lesson_title_mobject = lesson_title
        self.add_fixed_in_frame_mobjects(banner, lesson_title)
        self.add(banner, lesson_title)

        self._from_line_to_subspace_card()
        self._formula_analogy_card()
        self._derive_general_formula_card()
        self._general_basis_example_card()
        self._orthonormal_simplification_card()
        self._same_projection_card()
        self._residual_card()
        self._bridge_to_orthogonal_complement_card()

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

    def _set_camera_default(self) -> None:
        self.set_camera_orientation(phi=60 * DEGREES, theta=-18 * DEGREES, zoom=0.90)

    def _axes(self) -> ThreeDAxes:
        return ThreeDAxes(
            x_range=(-1.0, 4.2, 1),
            y_range=(-1.0, 4.2, 1),
            z_range=(-1.0, 4.2, 1),
            x_length=4.9,
            y_length=4.9,
            z_length=4.9,
        ).shift(RIGHT * 2.15 + DOWN * 1.85)

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

    def _segment3(
        self,
        axes: ThreeDAxes,
        start: np.ndarray,
        end: np.ndarray,
        color: str,
    ) -> Arrow3D:
        return Arrow3D(
            start=axes.c2p(*start),
            end=axes.c2p(*end),
            color=color,
            resolution=8,
            thickness=0.022,
            base_radius=0.036,
            height=0.13,
        )

    def _plane_patch(self, axes: ThreeDAxes) -> Polygon:
        q1, q2 = self.snapshot.basis
        corners = (
            -1.1 * q1 - 0.75 * q2,
            4.45 * q1 - 0.75 * q2,
            4.45 * q1 + 3.35 * q2,
            -1.1 * q1 + 3.35 * q2,
        )
        return Polygon(
            *(axes.c2p(*corner) for corner in corners),
            stroke_color=BLUE,
            stroke_width=2.0,
            fill_color=BLUE,
            fill_opacity=0.16,
        )

    def _world_label(self, tex: str, point: np.ndarray, axes: ThreeDAxes, color: str) -> MathTex:
        # Fixed-orientation labels are registered immediately by Manim.  Keep
        # them invisible until the corresponding geometry is deliberately revealed.
        label = MathTex(tex, font_size=31, color=color).move_to(axes.c2p(*point))
        label.set_opacity(0)
        self.add_fixed_orientation_mobjects(label)
        return label

    @staticmethod
    def _reveal(label: MathTex):
        return FadeIn(label)

    @staticmethod
    def _hide(label: MathTex):
        return FadeOut(label)

    def _remove_world_labels(self, *labels: MathTex) -> None:
        self.remove_fixed_orientation_mobjects(*labels)
        self.remove(*labels)

    def _from_line_to_subspace_card(self) -> None:
        self._set_camera_default()
        axes = self._axes()
        plane = self._plane_patch(axes)
        x_arrow = self._vector3(axes, self.snapshot.vector, ORANGE)
        p_arrow = self._vector3(axes, self.snapshot.projection, GREEN)
        r_arrow = self._segment3(axes, self.snapshot.projection, self.snapshot.vector, WHITE)
        w_label = self._world_label(r"W", np.array([2.4, 2.4, 0.35]), axes, BLUE)
        x_label = self._world_label(
            r"\mathbf{x}", self.snapshot.vector + np.array([0.20, 0.08, 0.18]), axes, ORANGE
        )
        p_label = self._world_label(
            r"\mathbf{p}", self.snapshot.projection + np.array([-0.15, 0.12, 0.18]), axes, GREEN
        )
        r_label = self._world_label(
            r"\mathbf{r}",
            0.5 * (self.snapshot.vector + self.snapshot.projection) + np.array([0.20, -0.10, 0.12]),
            axes,
            WHITE,
        )

        heading = Text("From a line to a whole subspace", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        prompt = Text(
            "Find the point in W reached by dropping x perpendicularly onto the subspace.",
            font_size=25,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.28)
        if prompt.width > 12.2:
            prompt.scale_to_fit_width(12.2)
        self.add_fixed_in_frame_mobjects(heading, prompt)

        self.play(
            FadeIn(heading), Create(axes), FadeIn(plane), self._reveal(w_label),
            run_time=self.TRANSITION_TIME,
        )
        self.play(Create(x_arrow), self._reveal(x_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(p_arrow), self._reveal(p_label), run_time=self.EMPHASIS_TIME)
        self.play(
            Create(r_arrow), self._reveal(r_label), FadeIn(prompt), run_time=self.TRANSITION_TIME
        )
        self.move_camera(phi=63 * DEGREES, theta=20 * DEGREES, zoom=0.92, run_time=3.0)
        self.wait(self.HOLD_TIME)
        self.play(
            FadeOut(VGroup(axes, plane, x_arrow, p_arrow, r_arrow, heading, prompt)),
            self._hide(w_label),
            self._hide(x_label),
            self._hide(p_label),
            self._hide(r_label),
            run_time=self.TRANSITION_TIME,
        )
        self.remove_fixed_in_frame_mobjects(heading, prompt)
        self._remove_world_labels(w_label, x_label, p_label, r_label)

    def _formula_analogy_card(self) -> None:
        heading = Text("The line formula already tells us what to expect", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        line_name = Text("Projection onto a line", font_size=25, color=GREY_B).move_to(UP * 1.35)
        line_formula = MathTex(self.lesson.LINE_FORMULA, font_size=40).move_to(UP * 0.72)
        sub_name = Text("Projection onto a subspace", font_size=25, color=GREY_B).move_to(DOWN * 0.10)
        sub_formula = MathTex(self.lesson.GENERAL_MATRIX_FORMULA, font_size=42, color=GREEN).move_to(DOWN * 0.70)
        analogy = MathTex(
            r"\frac{1}{\mathbf a^T\mathbf a}\quad\longleftrightarrow\quad(A^TA)^{-1}",
            font_size=39,
            color=YELLOW,
        ).move_to(DOWN * 1.52)
        caption = Text(
            "There is no matrix division: multiplying by the inverse plays the analogous role.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.20)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)
        all_items = VGroup(heading, line_name, line_formula, sub_name, sub_formula, analogy, caption)
        self.add_fixed_in_frame_mobjects(*all_items)

        self.play(FadeIn(heading), FadeIn(line_name), FadeIn(line_formula), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(sub_name), FadeIn(sub_formula), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(analogy), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(FadeOut(all_items), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(*all_items)

    def _derive_general_formula_card(self) -> None:
        heading = Text("Why does the inverse appear?", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        premise = MathTex(
            r"A=[\,\mathbf a_1\ \cdots\ \mathbf a_k\,],\qquad "
            r"\mathbf p=A\mathbf c,\qquad\mathbf r=\mathbf x-A\mathbf c",
            font_size=34,
        ).move_to(UP * 1.45)
        steps = VGroup(
            MathTex(r"\mathbf r\perp W\quad\Longrightarrow\quad A^T\mathbf r=\mathbf 0", font_size=35),
            MathTex(r"A^T(\mathbf x-A\mathbf c)=\mathbf 0", font_size=36),
            MathTex(self.lesson.NORMAL_EQUATIONS, font_size=38, color=YELLOW),
            MathTex(r"\mathbf c=(A^TA)^{-1}A^T\mathbf x", font_size=38),
            MathTex(self.lesson.GENERAL_MATRIX_FORMULA, font_size=41, color=GREEN),
        ).arrange(DOWN, buff=0.30).move_to(DOWN * 0.58)
        box = SurroundingRectangle(steps[-1], buff=0.16, color=WHITE)
        self.add_fixed_in_frame_mobjects(heading, premise, steps, box)

        self.play(FadeIn(heading), FadeIn(premise), run_time=self.TRANSITION_TIME)
        for step in steps[:-1]:
            self.play(FadeIn(step), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(steps[-1]), Create(box), run_time=self.TRANSITION_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(FadeOut(VGroup(heading, premise, steps, box)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, premise, steps, box)

    def _general_basis_example_card(self) -> None:
        self._set_camera_default()
        axes = self._axes()
        plane = self._plane_patch(axes)
        a1, a2 = self.general_snapshot.basis
        a1_arrow = self._vector3(axes, a1, BLUE)
        a2_arrow = self._vector3(axes, a2, YELLOW)
        x_arrow = self._vector3(axes, self.general_snapshot.vector, ORANGE)
        p_arrow = self._vector3(axes, self.general_snapshot.projection, GREEN)
        w_label = self._world_label(r"W", np.array([2.4, 2.4, 0.35]), axes, BLUE)
        a1_label = self._world_label(r"\mathbf a_1", a1 + np.array([-0.15, 0.06, 0.15]), axes, BLUE)
        a2_label = self._world_label(r"\mathbf a_2", a2 + np.array([0.10, 0.05, 0.18]), axes, YELLOW)
        x_label = self._world_label(
            r"\mathbf x", self.general_snapshot.vector + np.array([0.20, 0.05, 0.16]), axes, ORANGE
        )
        p_label = self._world_label(
            r"\mathbf p", self.general_snapshot.projection + np.array([-0.18, 0.10, 0.16]), axes, GREEN
        )

        heading = Text("The formula works for a non-orthonormal basis", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        equations = VGroup(
            MathTex(r"A=\begin{bmatrix}1&1\\1&1\\0&2\end{bmatrix},\quad\mathbf x=\begin{bmatrix}3\\1\\2\end{bmatrix}", font_size=29),
            MathTex(r"A^TA=\begin{bmatrix}2&2\\2&6\end{bmatrix},\quad(A^TA)^{-1}=\frac18\begin{bmatrix}6&-2\\-2&2\end{bmatrix}", font_size=27),
            MathTex(r"A^T\mathbf x=\begin{bmatrix}4\\8\end{bmatrix}", font_size=31),
            MathTex(r"\mathbf c=(A^TA)^{-1}A^T\mathbf x=\begin{bmatrix}1\\1\end{bmatrix}", font_size=30),
            MathTex(r"\mathbf p=A\mathbf c=\begin{bmatrix}2\\2\\2\end{bmatrix}", font_size=34, color=GREEN),
        ).arrange(DOWN, buff=0.17, aligned_edge=LEFT).move_to(RIGHT * 3.45 + DOWN * 0.42)
        self.add_fixed_in_frame_mobjects(heading, equations)

        self.play(
            FadeIn(heading), Create(axes), FadeIn(plane), self._reveal(w_label),
            run_time=self.TRANSITION_TIME,
        )
        self.play(
            Create(a1_arrow), Create(a2_arrow), self._reveal(a1_label), self._reveal(a2_label),
            run_time=self.TRANSITION_TIME,
        )
        self.play(Create(x_arrow), self._reveal(x_label), run_time=self.EMPHASIS_TIME)
        for equation in equations[:-1]:
            self.play(FadeIn(equation), run_time=self.EMPHASIS_TIME)
        self.play(
            Create(p_arrow), self._reveal(p_label), FadeIn(equations[-1]), run_time=self.TRANSITION_TIME
        )
        self.move_camera(phi=64 * DEGREES, theta=23 * DEGREES, zoom=0.92, run_time=3.0)
        self.wait(self.LONG_HOLD_TIME)
        self.play(
            FadeOut(VGroup(axes, plane, a1_arrow, a2_arrow, x_arrow, p_arrow, heading, equations)),
            self._hide(w_label),
            self._hide(a1_label),
            self._hide(a2_label),
            self._hide(x_label),
            self._hide(p_label),
            run_time=self.TRANSITION_TIME,
        )
        self.remove_fixed_in_frame_mobjects(heading, equations)
        self._remove_world_labels(w_label, a1_label, a2_label, x_label, p_label)

    def _orthonormal_simplification_card(self) -> None:
        heading = Text("Orthonormal columns make the inverse disappear", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        intro = MathTex(r"Q=[\,\mathbf q_1\ \cdots\ \mathbf q_k\,],\qquad Q^TQ=I", font_size=39).move_to(UP * 1.18)
        general = MathTex(r"\operatorname{proj}_W\mathbf x=Q(Q^TQ)^{-1}Q^T\mathbf x", font_size=40).move_to(UP * 0.34)
        simplify = MathTex(r"=QI Q^T\mathbf x=QQ^T\mathbf x", font_size=43, color=GREEN).move_to(DOWN * 0.42)
        sum_formula = MathTex(self.lesson.ORTHONORMAL_SUM_FORMULA, font_size=36).move_to(DOWN * 1.24)
        caption = Text(
            "Same projection — much simpler computation when the basis is orthonormal.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.22)
        box = SurroundingRectangle(simplify, buff=0.16, color=WHITE)
        items = VGroup(heading, intro, general, simplify, sum_formula, caption, box)
        self.add_fixed_in_frame_mobjects(*items)

        self.play(FadeIn(heading), FadeIn(intro), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(general), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(simplify), Create(box), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(sum_formula), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(FadeOut(items), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(*items)

    def _same_projection_card(self) -> None:
        heading = Text("The projection depends on W, not on the chosen basis", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        arbitrary = VGroup(
            Text("Any independent basis", font_size=25, color=GREY_B),
            MathTex(r"A=[\,\mathbf a_1\ \mathbf a_2\,]", font_size=38),
            MathTex(self.lesson.GENERAL_PROJECTION_MATRIX, font_size=38, color=YELLOW),
        ).arrange(DOWN, buff=0.30).move_to(LEFT * 3.25 + DOWN * 0.15)
        orthonormal = VGroup(
            Text("Orthonormal basis", font_size=25, color=GREY_B),
            MathTex(r"Q=[\,\mathbf q_1\ \mathbf q_2\,]", font_size=38),
            MathTex(self.lesson.PROJECTION_MATRIX, font_size=42, color=GREEN),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.25 + DOWN * 0.15)
        equals = MathTex(r"\Longrightarrow\quad\text{same }P_W\quad\Longrightarrow", font_size=34).move_to(DOWN * 0.18)
        result = MathTex(r"P_W\mathbf x=\mathbf p=(2,2,2)", font_size=40, color=WHITE).to_edge(DOWN, buff=0.34)
        items = VGroup(heading, arbitrary, orthonormal, equals, result)
        self.add_fixed_in_frame_mobjects(*items)

        self.play(FadeIn(heading), FadeIn(arbitrary), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(orthonormal), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(equals), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(result), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
        self.play(FadeOut(items), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(*items)

    def _residual_card(self) -> None:
        self._set_camera_default()
        axes = self._axes()
        plane = self._plane_patch(axes)
        x_arrow = self._vector3(axes, self.snapshot.vector, ORANGE)
        p_arrow = self._vector3(axes, self.snapshot.projection, GREEN)
        r_arrow = self._segment3(axes, self.snapshot.projection, self.snapshot.vector, WHITE)
        w_label = self._world_label(r"W", np.array([2.4, 2.4, 0.35]), axes, BLUE)
        x_label = self._world_label(
            r"\mathbf x", self.snapshot.vector + np.array([0.20, 0.05, 0.16]), axes, ORANGE
        )
        p_label = self._world_label(
            r"\mathbf p", self.snapshot.projection + np.array([-0.18, 0.10, 0.16]), axes, GREEN
        )
        r_label = self._world_label(
            r"\mathbf r",
            0.5 * (self.snapshot.vector + self.snapshot.projection) + np.array([0.18, -0.08, 0.10]),
            axes,
            WHITE,
        )

        heading = Text("The residual is perpendicular to the entire subspace", font_size=29, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        equations = VGroup(
            MathTex(r"\mathbf r=\mathbf x-\mathbf p=(1,-1,0)", font_size=34),
            MathTex(r"A^T\mathbf r=\mathbf 0", font_size=37, color=YELLOW),
            MathTex(r"\mathbf r\perp W", font_size=40),
            MathTex(self.lesson.RESIDUAL_STATEMENT, font_size=37, color=GREEN),
        ).arrange(DOWN, buff=0.24, aligned_edge=LEFT).move_to(RIGHT * 3.35 + DOWN * 0.05)
        self.add_fixed_in_frame_mobjects(heading, equations)

        self.play(
            FadeIn(heading), Create(axes), FadeIn(plane), self._reveal(w_label),
            run_time=self.TRANSITION_TIME,
        )
        self.play(
            Create(x_arrow), Create(p_arrow), self._reveal(x_label), self._reveal(p_label),
            run_time=self.TRANSITION_TIME,
        )
        self.play(Create(r_arrow), self._reveal(r_label), run_time=self.EMPHASIS_TIME)
        for equation in equations:
            self.play(FadeIn(equation), run_time=self.EMPHASIS_TIME)
        self.move_camera(phi=62 * DEGREES, theta=18 * DEGREES, zoom=0.92, run_time=2.8)
        self.wait(self.LONG_HOLD_TIME)
        self.play(
            FadeOut(VGroup(axes, plane, x_arrow, p_arrow, r_arrow, heading, equations)),
            self._hide(w_label),
            self._hide(x_label),
            self._hide(p_label),
            self._hide(r_label),
            run_time=self.TRANSITION_TIME,
        )
        self.remove_fixed_in_frame_mobjects(heading, equations)
        self._remove_world_labels(w_label, x_label, p_label, r_label)

    def _bridge_to_orthogonal_complement_card(self) -> None:
        heading = Text("Next question", font_size=30, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        question = Text(
            "Where do all vectors perpendicular to W live?",
            font_size=32,
            color=YELLOW,
        ).move_to(UP * 0.95)
        name = MathTex(r"W^\perp", font_size=56).move_to(DOWN * 0.05)
        statement = MathTex(
            r"\mathbf{x}=\underbrace{\mathbf{p}}_{\in W}+\underbrace{\mathbf{r}}_{\in W^\perp}",
            font_size=42,
        ).move_to(DOWN * 1.18)
        caption = Text(
            "The next lesson studies the orthogonal complement as a subspace in its own right.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.24)
        if caption.width > 12.2:
            caption.scale_to_fit_width(12.2)
        items = VGroup(heading, question, name, statement, caption)
        self.add_fixed_in_frame_mobjects(*items)

        self.play(FadeIn(heading), FadeIn(question), run_time=self.TRANSITION_TIME)
        self.play(FadeIn(name), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(statement), run_time=self.EMPHASIS_TIME)
        self.play(FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.LONG_HOLD_TIME)
