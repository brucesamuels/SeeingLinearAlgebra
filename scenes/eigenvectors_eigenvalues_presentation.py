"""Manim presentation for Chapter 7 lesson 2: eigenvectors and eigenvalues."""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    MathTex,
    NumberPlane,
    ReplacementTransform,
    Scene,
    Text,
    VGroup,
    WHITE,
    YELLOW,
    BLUE_C,
    GREEN_C,
    GREY_B,
    GREY_D,
    linear,
)

from engine.eigenvectors_eigenvalues import (
    DEFAULT_MATRIX,
    EIGENVECTOR_FAST,
    EIGENVECTOR_SLOW,
    EigenvectorsEigenvaluesLesson,
    LAMBDA_CASES,
)


class EigenvectorsEigenvaluesPresentation(Scene):
    """Formalize the invariant-line phenomenon as ``A v = lambda v``."""

    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Eigenvectors and Eigenvalues"

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=30, color=WHITE)
        if item.width > 12.2:
            item.scale_to_fit_width(12.2)
        return item

    def _base_frame(self, heading_text: str) -> tuple[VGroup, Text, NumberPlane]:
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD")
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.18)

        title = Text(self.LESSON_TITLE, font_size=36, color=YELLOW, weight="BOLD")
        title.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.16)

        heading = self._heading(heading_text)
        heading.next_to(title, np.array([0.0, -1.0, 0.0]), buff=0.24)

        plane = NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            x_length=7.2,
            y_length=4.7,
            background_line_style={"stroke_opacity": 0.32, "stroke_width": 1.1},
            axis_config={"stroke_opacity": 0.7, "stroke_width": 1.5},
        )
        plane.move_to(np.array([-2.75, -0.65, 0.0]))
        return VGroup(banner, title), heading, plane

    def construct(self) -> None:
        lesson = EigenvectorsEigenvaluesLesson(DEFAULT_MATRIX)
        slow = lesson.eigenpair(EIGENVECTOR_SLOW)
        fast = lesson.eigenpair(EIGENVECTOR_FAST)

        chrome, heading, plane = self._base_frame(
            "A surviving direction carries more information than direction alone."
        )
        banner, title = chrome
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))
        self.play(Create(plane), run_time=1.2)

        # Card 1: use the same matrix and invariant direction as CP168.
        origin = plane.c2p(0, 0)
        vector = Arrow(origin, plane.c2p(*EIGENVECTOR_SLOW), buff=0, color=BLUE_C, stroke_width=6)
        ghost = DashedLine(
            origin,
            plane.c2p(*EIGENVECTOR_SLOW),
            dash_length=0.11,
            color=BLUE_C,
            stroke_opacity=0.35,
            stroke_width=3,
        )
        invariant_line = DashedLine(
            plane.c2p(-2.4, 2.4),
            plane.c2p(2.4, -2.4),
            dash_length=0.10,
            color=GREY_D,
            stroke_opacity=0.48,
            stroke_width=1.8,
        )

        matrix_tex = MathTex(r"A=\begin{bmatrix}5&3\\3&5\end{bmatrix}", font_size=38)
        matrix_tex.move_to(np.array([3.75, 1.05, 0.0]))
        vector_tex = MathTex(r"\mathbf v=\begin{bmatrix}1\\-1\end{bmatrix}", font_size=38, color=BLUE_C)
        # Use the rendered bounding boxes to create a genuine vertical gap.
        # Fixed y-coordinates proved unsafe for stacked matrix expressions.
        vector_tex.next_to(matrix_tex, np.array([0.0, -1.0, 0.0]), buff=0.48)
        vector_tex.set_x(matrix_tex.get_center()[0])

        self.play(FadeIn(invariant_line), FadeIn(ghost), FadeIn(vector), FadeIn(matrix_tex), FadeIn(vector_tex))
        self.wait(0.8)
        self.play(
            vector.animate.put_start_and_end_on(origin, plane.c2p(*(0.82 * slow.image))),
            run_time=2.0,
            rate_func=linear,
        )
        self.wait(1.0)

        image_tex = MathTex(
            r"A\mathbf v=\begin{bmatrix}2\\-2\end{bmatrix}=2\mathbf v",
            font_size=38,
            color=WHITE,
        )
        # Place the result below the blue vector equation using the actual
        # occupied bounds, leaving a generous safety margin between them.
        image_tex.next_to(vector_tex, np.array([0.0, -1.0, 0.0]), buff=0.62)
        image_tex.set_x(matrix_tex.get_center()[0])
        self.play(FadeIn(image_tex))
        self.wait(1.5)

        # Card 2: reveal the defining equation only after the numerical example.
        definition_heading = self._heading(
            "An eigenvector stays on its line; the eigenvalue tells how it scales."
        )
        definition_heading.move_to(heading)
        definition = MathTex(
            r"A\mathbf v=\lambda\mathbf v,\qquad \mathbf v\ne\mathbf 0",
            font_size=52,
            color=YELLOW,
        )
        definition.move_to(np.array([3.55, -0.95, 0.0]))
        lambda_note = Text("λ is the scale factor along the eigenvector line.", font_size=25, color=WHITE)
        lambda_note.move_to(np.array([3.5, -2.05, 0.0]))
        lambda_note.scale_to_fit_width(6.0)
        self.play(
            FadeOut(heading),
            FadeIn(definition_heading),
            FadeOut(image_tex),
            FadeOut(matrix_tex),
            FadeOut(vector_tex),
            FadeIn(definition),
            FadeIn(lambda_note),
        )
        self.wait(1.8)

        # Show the second eigendirection from CP168 so lambda is visibly tied to
        # the transformation, not to a single chosen arrow.
        fast_arrow = Arrow(origin, plane.c2p(*(0.34 * EIGENVECTOR_FAST)), buff=0, color=GREEN_C, stroke_width=6)
        fast_line = DashedLine(
            plane.c2p(-2.4, -2.4),
            plane.c2p(2.4, 2.4),
            dash_length=0.10,
            color=GREY_D,
            stroke_opacity=0.48,
            stroke_width=1.8,
        )
        fast_label = MathTex(r"A\mathbf w=8\mathbf w", font_size=38, color=GREEN_C)
        fast_label.move_to(np.array([3.55, 0.15, 0.0]))
        self.play(FadeIn(fast_line), FadeIn(fast_arrow), FadeIn(fast_label))
        self.play(
            fast_arrow.animate.put_start_and_end_on(origin, plane.c2p(*(0.34 * fast.image))),
            run_time=1.8,
            rate_func=linear,
        )
        self.wait(1.2)

        # Card 3: clear the worked example and classify the possible meanings of lambda.
        cases_heading = self._heading("The sign and size of λ describe what happens on that line.")
        cases_heading.move_to(definition_heading)
        self.play(
            FadeOut(definition_heading),
            FadeIn(cases_heading),
            FadeOut(vector),
            FadeOut(ghost),
            FadeOut(invariant_line),
            FadeOut(fast_arrow),
            FadeOut(fast_line),
            FadeOut(fast_label),
            FadeOut(definition),
            FadeOut(lambda_note),
            FadeOut(plane),
        )

        labels = {
            "stretch": r"\lambda>1\quad\text{stretch}",
            "shrink": r"0<\lambda<1\quad\text{shrink}",
            "reverse": r"\lambda<0\quad\text{reverse}",
            "fixed": r"\lambda=1\quad\text{fixed}",
            "collapse": r"\lambda=0\quad\text{collapse to the origin}",
        }
        positions = [
            np.array([-3.6, 1.15, 0.0]),
            np.array([2.7, 1.15, 0.0]),
            np.array([-3.6, -0.25, 0.0]),
            np.array([2.7, -0.25, 0.0]),
            np.array([0.0, -1.65, 0.0]),
        ]
        case_group = VGroup()
        for (name, value), position in zip(LAMBDA_CASES, positions):
            tex = MathTex(labels[name], font_size=36, color=WHITE)
            tex.move_to(position)
            if tex.width > 5.7:
                tex.scale_to_fit_width(5.7)
            case_group.add(tex)
        self.play(FadeIn(case_group), run_time=1.2)
        self.wait(2.2)

        # Final synthesis: direction is encoded by v; scaling is encoded by lambda.
        final_heading = self._heading("Eigenvectors identify invariant directions; eigenvalues describe the scaling.")
        final_heading.move_to(cases_heading)
        final_equation = MathTex(
            r"\boxed{A\mathbf v=\lambda\mathbf v}",
            font_size=64,
            color=YELLOW,
        )
        final_equation.move_to(np.array([0.0, -0.15, 0.0]))
        direction_note = Text("v: the special direction", font_size=28, color=BLUE_C)
        scale_note = Text("λ: the scale factor", font_size=28, color=GREEN_C)
        notes = VGroup(direction_note, scale_note).arrange(np.array([1.0, 0.0, 0.0]), buff=1.25)
        notes.move_to(np.array([0.0, -1.55, 0.0]))
        self.play(
            FadeOut(cases_heading),
            FadeIn(final_heading),
            FadeOut(case_group),
            FadeIn(final_equation),
            FadeIn(notes),
        )
        self.wait(2.2)
