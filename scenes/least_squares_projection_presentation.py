"""CP161: Least Squares as Orthogonal Projection."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow3D,
    Create,
    DashedLine,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    GREY_B,
    GREY_D,
    IN,
    LEFT,
    Line,
    MathTex,
    ORANGE,
    Polygon,
    PURPLE,
    Rectangle,
    RIGHT,
    SurroundingRectangle,
    TEAL,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    BLUE,
)

from engine.least_squares_projection import LeastSquaresProjectionLesson


class LeastSquaresProjectionPresentation(ThreeDScene):
    CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"
    LESSON_TITLE = "Least Squares: Projection and the Normal Equation"
    SCENE_REVISION = "cp161_r14_lower_penultimate_math_blocks"
    TRANSITION_TIME = 1.25
    EMPHASIS_TIME = 1.05
    HOLD_TIME = 2.35

    def construct(self) -> None:
        self.lesson = LeastSquaresProjectionLesson()
        self.snapshot = self.lesson.snapshot()
        self._set_projection_geometry_view()
        self.banner, self.lesson_title_mobject = self._header()
        self.add_fixed_in_frame_mobjects(self.banner, self.lesson_title_mobject)
        self.add(self.banner, self.lesson_title_mobject)

        self._no_exact_solution_card()
        self._closest_point_card()
        self._residual_orthogonality_card()
        self._set_default_view()
        self._matrix_orthogonality_card()
        self._normal_equation_card()
        self._solve_normal_equation_card()
        self._qr_route_card()


    def _set_projection_geometry_view(self) -> None:
        # One consistent view for Cards 1-3.  The camera direction is chosen
        # perpendicular to the projection vector p=(1,1,2); with equal axis
        # scale this makes p horizontal on screen and the residual vertical.
        self.set_camera_orientation(
            phi=111.42 * np.pi / 180,
            theta=101.31 * np.pi / 180,
            gamma=-118.71 * np.pi / 180,
            zoom=0.88,
        )

    def _set_default_view(self) -> None:
        self.set_camera_orientation(phi=67 * np.pi / 180, theta=-48 * np.pi / 180, zoom=0.86)

    def _header(self) -> tuple[VGroup, Text]:
        banner_box = Rectangle(
            width=13.5,
            height=0.58,
            stroke_width=0,
            fill_color=GREY_D,
            fill_opacity=0.96,
        ).to_edge(UP, buff=0.08)
        banner_text = Text(self.CHAPTER_BANNER, font_size=28, color=WHITE).move_to(banner_box)
        lesson_title = Text(self.LESSON_TITLE, font_size=30, color=YELLOW).next_to(
            banner_box, DOWN, buff=0.18
        )
        if lesson_title.width > 11.8:
            lesson_title.scale_to_fit_width(11.8)
        return VGroup(banner_box, banner_text), lesson_title

    @staticmethod
    def _axes3d() -> ThreeDAxes:
        return ThreeDAxes(
            x_range=(-1.5, 3.0, 1),
            y_range=(-1.5, 3.0, 1),
            z_range=(-2.0, 4.5, 1),
            x_length=4.5,
            y_length=4.5,
            z_length=6.5,
            axis_config={"stroke_opacity": 0.28, "stroke_width": 1.5, "include_tip": False},
        ).shift(LEFT * 0.907 + DOWN * 1.041 + IN * 2.149)

    def _column_space_patch(self, axes: ThreeDAxes) -> Polygon:
        a1 = self.snapshot.a1
        a2 = self.snapshot.a2
        corners = (
            -0.95 * a1 - 0.95 * a2,
            2.10 * a1 - 0.95 * a2,
            2.10 * a1 + 2.10 * a2,
            -0.95 * a1 + 2.10 * a2,
        )
        return Polygon(
            *(axes.c2p(*corner) for corner in corners),
            fill_color=TEAL,
            fill_opacity=0.24,
            stroke_color=TEAL,
            stroke_opacity=0.72,
            stroke_width=2.5,
        )

    @staticmethod
    def _origin_arrow(axes: ThreeDAxes, vector: np.ndarray, color, thickness: float = 0.022) -> Arrow3D:
        return Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(*vector),
            color=color,
            thickness=thickness,
            base_radius=0.05,
        )

    @staticmethod
    def _segment_arrow(
        axes: ThreeDAxes,
        start: np.ndarray,
        end: np.ndarray,
        color,
        thickness: float = 0.022,
    ) -> Arrow3D:
        return Arrow3D(
            start=axes.c2p(*start),
            end=axes.c2p(*end),
            color=color,
            thickness=thickness,
            base_radius=0.05,
        )

    @staticmethod
    def _label(text: str, axes: ThreeDAxes, point: np.ndarray, color, offset: np.ndarray) -> MathTex:
        return MathTex(text, font_size=30, color=color).move_to(axes.c2p(*point) + offset)

    @staticmethod
    def _right_angle_marker(
        axes: ThreeDAxes,
        point: np.ndarray,
        along: np.ndarray,
        perp: np.ndarray,
        size: float = 0.30,
    ) -> VGroup:
        along_u = along / np.linalg.norm(along)
        perp_u = perp / np.linalg.norm(perp)
        a = point + size * along_u
        c = point + size * perp_u
        b = a + size * perp_u
        return VGroup(
            Line(axes.c2p(*a), axes.c2p(*b), color=WHITE, stroke_width=3.5),
            Line(axes.c2p(*c), axes.c2p(*b), color=WHITE, stroke_width=3.5),
        )

    def _no_exact_solution_card(self) -> None:
        heading = Text("When Ax = b has no exact solution", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._axes3d()
        plane = self._column_space_patch(axes)
        a1_arrow = self._origin_arrow(axes, self.snapshot.a1, ORANGE, thickness=0.017)
        a2_arrow = self._origin_arrow(axes, self.snapshot.a2, PURPLE, thickness=0.017)
        b_arrow = self._origin_arrow(axes, self.snapshot.b, BLUE)
        a1_label = self._label(r"\mathbf a_1", axes, self.snapshot.a1, ORANGE, np.array([-0.42, 0.38, 0.0]))
        a2_label = self._label(r"\mathbf a_2", axes, self.snapshot.a2, PURPLE, np.array([0.42, 0.38, 0.0]))
        b_label = self._label(r"\mathbf b", axes, self.snapshot.b, BLUE, np.array([0.48, 0.42, 0.0]))
        plane_label = MathTex(r"\operatorname{Col}(A)", font_size=31, color=TEAL).move_to(
            axes.c2p(0.65, 1.20, 1.85) + np.array([-0.20, 0.28, 0.0])
        )
        equations = VGroup(
            MathTex(r"A=\begin{bmatrix}1&0\\0&1\\1&1\end{bmatrix}", font_size=39),
            MathTex(r"\mathbf b=\begin{bmatrix}2\\2\\1\end{bmatrix}", font_size=39, color=BLUE),
            MathTex(r"\mathbf b\notin\operatorname{Col}(A)", font_size=38, color=YELLOW),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.45 + UP * 0.05)
        caption = Text(
            "No choice of x makes Ax land exactly on b.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), FadeIn(axes), FadeIn(plane), run_time=self.TRANSITION_TIME)
        self.add_fixed_orientation_mobjects(a1_label, a2_label, b_label, plane_label)
        self.play(
            Create(a1_arrow), FadeIn(a1_label),
            Create(a2_arrow), FadeIn(a2_label),
            Create(b_arrow), FadeIn(b_label), FadeIn(plane_label),
            run_time=self.EMPHASIS_TIME,
        )
        self.add_fixed_in_frame_mobjects(equations, caption)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, axes, plane, a1_arrow, a2_arrow, b_arrow, a1_label, a2_label, b_label, plane_label, equations, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_orientation_mobjects(a1_label, a2_label, b_label, plane_label)
        self.remove_fixed_in_frame_mobjects(heading, equations, caption)

    def _closest_point_card(self) -> None:
        heading = Text("Least squares chooses the closest vector in Col(A)", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._axes3d()
        plane = self._column_space_patch(axes)
        b_arrow = self._origin_arrow(axes, self.snapshot.b, BLUE, thickness=0.018)
        p_arrow = self._origin_arrow(axes, self.snapshot.projection, GREEN)
        residual = DashedLine(
            axes.c2p(*self.snapshot.projection),
            axes.c2p(*self.snapshot.b),
            color=YELLOW,
            dash_length=0.14,
            dashed_ratio=0.58,
        ).set_stroke(width=4.5)
        marker = self._right_angle_marker(
            axes,
            self.snapshot.projection,
            -self.snapshot.projection,
            self.snapshot.residual,
            size=0.42,
        )
        b_label = self._label(r"\mathbf b", axes, self.snapshot.b, BLUE, np.array([0.48, 0.42, 0.0]))
        p_label = self._label(r"A\widehat{\mathbf x}", axes, self.snapshot.projection, GREEN, np.array([-0.55, -0.34, 0.0]))
        r_label = MathTex(r"\mathbf r", font_size=30, color=YELLOW).move_to(
            0.5 * (axes.c2p(*self.snapshot.projection) + axes.c2p(*self.snapshot.b)) + RIGHT * 0.34 + UP * 0.08
        )
        equations = VGroup(
            MathTex(r"\widehat{\mathbf x}=\arg\min_{\mathbf x}\|\mathbf b-A\mathbf x\|", font_size=36, color=YELLOW),
            MathTex(r"A\widehat{\mathbf x}=\operatorname{proj}_{\operatorname{Col}(A)}\mathbf b", font_size=34, color=GREEN),
            MathTex(r"A\widehat{\mathbf x}=(1,1,2)", font_size=34),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.45 + UP * 0.06)
        caption = Text(
            "The closest point is where the perpendicular from b meets the column space.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), FadeIn(axes), FadeIn(plane), run_time=self.TRANSITION_TIME)
        self.add_fixed_orientation_mobjects(b_label, p_label, r_label)
        self.play(Create(b_arrow), FadeIn(b_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(p_arrow), FadeIn(p_label), run_time=self.EMPHASIS_TIME)
        self.play(Create(residual), FadeIn(r_label), Create(marker), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(equations, caption)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, axes, plane, b_arrow, p_arrow, residual, marker, b_label, p_label, r_label, equations, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_orientation_mobjects(b_label, p_label, r_label)
        self.remove_fixed_in_frame_mobjects(heading, equations, caption)

    def _residual_orthogonality_card(self) -> None:
        heading = Text("The residual is perpendicular to the column space", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        axes = self._axes3d()
        plane = self._column_space_patch(axes)
        a1_arrow = self._origin_arrow(axes, self.snapshot.a1, ORANGE, thickness=0.017)
        a2_arrow = self._origin_arrow(axes, self.snapshot.a2, PURPLE, thickness=0.017)
        p_arrow = self._origin_arrow(axes, self.snapshot.projection, GREEN, thickness=0.019)
        residual = DashedLine(
            axes.c2p(*self.snapshot.projection),
            axes.c2p(*self.snapshot.b),
            color=YELLOW,
            dash_length=0.14,
            dashed_ratio=0.58,
        ).set_stroke(width=4.5)
        marker = self._right_angle_marker(
            axes,
            self.snapshot.projection,
            -self.snapshot.projection,
            self.snapshot.residual,
            size=0.40,
        )
        r_label = MathTex(r"\mathbf r=\mathbf b-A\widehat{\mathbf x}", font_size=30, color=YELLOW).move_to(
            0.5 * (axes.c2p(*self.snapshot.projection) + axes.c2p(*self.snapshot.b)) + RIGHT * 0.38 + UP * 0.08
        )
        p_label = self._label(
            r"A\widehat{\mathbf x}",
            axes,
            self.snapshot.projection,
            GREEN,
            np.array([-0.55, -0.34, 0.0]),
        )
        equations = VGroup(
            MathTex(r"\mathbf r=(1,1,-1)", font_size=36, color=YELLOW),
            MathTex(r"\mathbf a_1\cdot\mathbf r=0", font_size=35, color=ORANGE),
            MathTex(r"\mathbf a_2\cdot\mathbf r=0", font_size=35, color=PURPLE),
            MathTex(r"\mathbf r\perp\operatorname{Col}(A)", font_size=39, color=GREEN),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 3.42 + UP * 0.02)
        caption = Text(
            "At the nearest point, the error cannot have any component inside Col(A).",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.32)

        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), FadeIn(axes), FadeIn(plane), run_time=self.TRANSITION_TIME)
        self.add_fixed_orientation_mobjects(p_label, r_label)
        self.play(
            Create(a1_arrow), Create(a2_arrow), Create(p_arrow), FadeIn(p_label),
            run_time=self.EMPHASIS_TIME,
        )
        self.play(Create(residual), FadeIn(r_label), Create(marker), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(equations, caption)
        self.play(FadeIn(equations), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, axes, plane, a1_arrow, a2_arrow, p_arrow, residual, marker, p_label, r_label, equations, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_orientation_mobjects(p_label, r_label)
        self.remove_fixed_in_frame_mobjects(heading, equations, caption)

    def _matrix_orthogonality_card(self) -> None:
        heading = Text("Package those perpendicularity conditions into one equation", font_size=27, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        stack = VGroup(
            MathTex(r"\mathbf a_1^T\mathbf r=0,\qquad \mathbf a_2^T\mathbf r=0", font_size=40),
            MathTex(r"\begin{bmatrix}\mathbf a_1^T\\\mathbf a_2^T\end{bmatrix}\mathbf r=\mathbf 0", font_size=40),
            MathTex(self.lesson.RESIDUAL_ORTHOGONALITY, font_size=50, color=GREEN),
            MathTex(r"\mathbf r=\mathbf b-A\widehat{\mathbf x}", font_size=42, color=YELLOW),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.02)
        caption = Text(
            "The transpose collects all dot products with the columns of A at once.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.34)
        self.add_fixed_in_frame_mobjects(heading, stack[0])
        self.play(FadeIn(heading), FadeIn(stack[0]), run_time=self.TRANSITION_TIME)
        self.add_fixed_in_frame_mobjects(stack[1])
        self.play(FadeIn(stack[1]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(stack[2])
        self.play(FadeIn(stack[2]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(stack[3], caption)
        self.play(FadeIn(stack[3]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, stack, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, stack[0], stack[1], stack[2], stack[3], caption)

    def _normal_equation_card(self) -> None:
        heading = Text("THE NORMAL EQUATION", font_size=31, color=YELLOW).next_to(
            self.lesson_title_mobject, DOWN, buff=0.26
        )
        derivation = VGroup(
            MathTex(r"A^T\mathbf r=\mathbf 0", font_size=42),
            MathTex(r"A^T(\mathbf b-A\widehat{\mathbf x})=\mathbf 0", font_size=42),
            MathTex(r"A^T\mathbf b-A^TA\widehat{\mathbf x}=\mathbf 0", font_size=42),
        ).arrange(DOWN, buff=0.34).move_to(UP * 0.55)
        normal_equation = MathTex(self.lesson.NORMAL_EQUATION, font_size=57, color=YELLOW).move_to(DOWN * 1.25)
        normal_box = SurroundingRectangle(
            normal_equation,
            color=YELLOW,
            buff=0.24,
            stroke_width=3.2,
        )
        caption = Text(
            "This equation characterizes the least-squares solution.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.28)

        self.add_fixed_in_frame_mobjects(heading, derivation[0])
        self.play(FadeIn(heading), FadeIn(derivation[0]), run_time=self.TRANSITION_TIME)
        self.add_fixed_in_frame_mobjects(derivation[1])
        self.play(FadeIn(derivation[1]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(derivation[2])
        self.play(FadeIn(derivation[2]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(normal_equation, normal_box, caption)
        self.play(FadeIn(normal_equation), Create(normal_box), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME + 0.8)
        self.play(FadeOut(VGroup(heading, derivation, normal_equation, normal_box, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, derivation[0], derivation[1], derivation[2], normal_equation, normal_box, caption)

    def _solve_normal_equation_card(self) -> None:
        heading = Text("Solve the normal equation for this example", font_size=28, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        computation = VGroup(
            MathTex(r"A^TA=\begin{bmatrix}2&1\\1&2\end{bmatrix}", font_size=40),
            MathTex(r"A^T\mathbf b=\begin{bmatrix}3\\3\end{bmatrix}", font_size=40),
            MathTex(r"\begin{bmatrix}2&1\\1&2\end{bmatrix}\widehat{\mathbf x}=\begin{bmatrix}3\\3\end{bmatrix}", font_size=42, color=YELLOW),
            MathTex(r"\widehat{\mathbf x}=\begin{bmatrix}1\\1\end{bmatrix}", font_size=46, color=GREEN),
        ).arrange(DOWN, buff=0.28).move_to(LEFT * 1.8 + DOWN * 0.34)
        check = VGroup(
            MathTex(r"A\widehat{\mathbf x}=\begin{bmatrix}1\\1\\2\end{bmatrix}", font_size=37, color=GREEN),
            MathTex(r"\mathbf r=\mathbf b-A\widehat{\mathbf x}=\begin{bmatrix}1\\1\\-1\end{bmatrix}", font_size=34, color=YELLOW),
            MathTex(r"A^T\mathbf r=\mathbf 0", font_size=39),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.20 + DOWN * 0.38)
        divider = Line(UP * 1.22, DOWN * 2.33, color=GREY_B, stroke_opacity=0.45)
        caption = Text(
            "The algebra returns exactly the projection and perpendicular residual from the geometry.",
            font_size=21,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.30)

        self.add_fixed_in_frame_mobjects(heading, computation[0], computation[1])
        self.play(FadeIn(heading), FadeIn(computation[0]), FadeIn(computation[1]), run_time=self.TRANSITION_TIME)
        self.add_fixed_in_frame_mobjects(computation[2])
        self.play(FadeIn(computation[2]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(computation[3], divider, check[0])
        self.play(FadeIn(computation[3]), FadeIn(divider), FadeIn(check[0]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(check[1], check[2], caption)
        self.play(FadeIn(check[1]), FadeIn(check[2]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME)
        self.play(FadeOut(VGroup(heading, computation, divider, check, caption)), run_time=self.TRANSITION_TIME)
        self.remove_fixed_in_frame_mobjects(heading, computation[0], computation[1], computation[2], computation[3], divider, check[0], check[1], check[2], caption)

    def _qr_route_card(self) -> None:
        heading = Text("QR solves the same least-squares problem without forming A^T A", font_size=26, color=WHITE).next_to(
            self.lesson_title_mobject, DOWN, buff=0.24
        )
        left = VGroup(
            Text("Normal equation", font_size=24, color=YELLOW),
            MathTex(self.lesson.NORMAL_EQUATION, font_size=40),
            MathTex(r"\begin{bmatrix}2&1\\1&2\end{bmatrix}\widehat{\mathbf x}=\begin{bmatrix}3\\3\end{bmatrix}", font_size=36),
        ).arrange(DOWN, buff=0.34).move_to(LEFT * 3.25 + DOWN * 0.10)
        right = VGroup(
            Text("QR route", font_size=24, color=GREEN),
            MathTex(r"A=QR", font_size=40),
            MathTex(self.lesson.QR_LEAST_SQUARES, font_size=43, color=GREEN),
            MathTex(r"\widehat{\mathbf x}=\begin{bmatrix}1\\1\end{bmatrix}", font_size=40),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.20 + DOWN * 0.10)
        divider = Line(UP * 1.50, DOWN * 1.95, color=GREY_B, stroke_opacity=0.45)
        caption = Text(
            self.lesson.CLOSING_IDEA,
            font_size=24,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.32)

        self.add_fixed_in_frame_mobjects(heading, left[0], left[1])
        self.play(FadeIn(heading), FadeIn(left[0]), FadeIn(left[1]), run_time=self.TRANSITION_TIME)
        self.add_fixed_in_frame_mobjects(left[2], divider, right[0], right[1])
        self.play(FadeIn(left[2]), FadeIn(divider), FadeIn(right[0]), FadeIn(right[1]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(right[2])
        self.play(FadeIn(right[2]), run_time=self.EMPHASIS_TIME)
        self.add_fixed_in_frame_mobjects(right[3], caption)
        self.play(FadeIn(right[3]), FadeIn(caption), run_time=self.EMPHASIS_TIME)
        self.wait(self.HOLD_TIME + 0.5)
