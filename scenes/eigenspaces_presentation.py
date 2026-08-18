"""Manim presentation for Chapter 7 lesson 3: eigenspaces."""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    NumberPlane,
    Scene,
    Text,
    VGroup,
    WHITE,
    YELLOW,
    BLUE_C,
    GREEN_C,
    RED_C,
    GREY_B,
    GREY_D,
    linear,
)

from engine.eigenspaces import (
    DEFAULT_MATRIX,
    EigenspacesLesson,
    FAST_EIGENVALUE,
    FAST_GENERATOR,
    SCALAR_MULTIPLES,
    SLOW_EIGENVALUE,
    SLOW_GENERATOR,
)


class EigenspacesPresentation(Scene):
    """Show that an eigenvalue belongs to a whole null-space direction."""

    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Eigenspaces"

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=30, color=WHITE)
        if item.width > 12.2:
            item.scale_to_fit_width(12.2)
        return item

    def _chrome(self, heading_text: str) -> tuple[Text, Text, Text]:
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD")
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.18)
        title = Text(self.LESSON_TITLE, font_size=36, color=YELLOW, weight="BOLD")
        title.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.16)
        heading = self._heading(heading_text)
        heading.next_to(title, np.array([0.0, -1.0, 0.0]), buff=0.24)
        return banner, title, heading

    def _plane(self) -> NumberPlane:
        plane = NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            x_length=7.0,
            y_length=4.55,
            background_line_style={"stroke_opacity": 0.32, "stroke_width": 1.1},
            axis_config={"stroke_opacity": 0.7, "stroke_width": 1.5},
        )
        plane.move_to(np.array([-2.9, -0.72, 0.0]))
        return plane

    def construct(self) -> None:
        lesson = EigenspacesLesson(DEFAULT_MATRIX)
        banner, title, heading = self._chrome(
            "One eigenvector reveals an entire family on the same line."
        )
        plane = self._plane()
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), Create(plane), run_time=1.2)

        # Card 1: several nonzero scalar multiples on the same invariant line.
        origin = plane.c2p(0, 0)
        eig_line = DashedLine(
            plane.c2p(-2.35, 2.35),
            plane.c2p(2.35, -2.35),
            dash_length=0.10,
            color=GREY_D,
            stroke_opacity=0.55,
            stroke_width=2.0,
        )
        colors = (BLUE_C, GREEN_C, WHITE)
        arrows = VGroup()
        ghosts = VGroup()
        for scalar, color in zip(SCALAR_MULTIPLES, colors):
            endpoint = 0.72 * scalar * SLOW_GENERATOR
            ghosts.add(
                DashedLine(
                    origin,
                    plane.c2p(*endpoint),
                    dash_length=0.09,
                    color=color,
                    stroke_opacity=0.30,
                    stroke_width=2.6,
                )
            )
            arrows.add(Arrow(origin, plane.c2p(*endpoint), buff=0, color=color, stroke_width=5.5))

        relation = MathTex(
            r"A(c\mathbf v)=cA\mathbf v=c(2\mathbf v)=2(c\mathbf v)",
            font_size=37,
            color=WHITE,
        )
        relation.move_to(np.array([3.55, 0.65, 0.0]))
        relation.scale_to_fit_width(6.1)
        family_note = Text("Every nonzero scalar multiple is also an eigenvector.", font_size=25, color=WHITE)
        family_note.next_to(relation, np.array([0.0, -1.0, 0.0]), buff=0.48)
        family_note.set_x(relation.get_center()[0])
        family_note.scale_to_fit_width(5.9)

        self.play(FadeIn(eig_line), FadeIn(ghosts), FadeIn(arrows), FadeIn(relation))
        self.wait(0.8)
        for arrow, scalar in zip(arrows, SCALAR_MULTIPLES):
            start = 0.72 * scalar * SLOW_GENERATOR
            image = 0.72 * scalar * 2.0 * SLOW_GENERATOR
            # Uniform display compression keeps the family visible without changing direction.
            target = 0.52 * image
            self.play(
                arrow.animate.put_start_and_end_on(origin, plane.c2p(*target)),
                run_time=0.85,
                rate_func=linear,
            )
        self.play(FadeIn(family_note))
        self.wait(1.6)

        # Card 2: name the geometric object and distinguish zero from eigenvectors.
        family_heading = self._heading("The natural object is the whole invariant line, not one arrow.")
        family_heading.move_to(heading)
        zero_dot = Dot(origin, radius=0.07, color=RED_C)
        zero_label = Text("0 is in the subspace, but 0 is not an eigenvector.", font_size=24, color=WHITE)
        zero_label.move_to(np.array([3.55, -1.35, 0.0]))
        zero_label.scale_to_fit_width(6.0)
        eigenspace_label = MathTex(
            r"E_2=\operatorname{span}\!\left\{\begin{bmatrix}1\\-1\end{bmatrix}\right\}",
            font_size=42,
            color=YELLOW,
        )
        eigenspace_label.move_to(np.array([3.55, 0.15, 0.0]))
        self.play(
            FadeOut(heading), FadeIn(family_heading),
            FadeOut(relation), FadeOut(family_note),
            FadeIn(eigenspace_label), FadeIn(zero_dot), FadeIn(zero_label),
        )
        self.wait(1.8)

        # Card 3: derive the null-space equation from A v = lambda v.
        null_heading = self._heading("Move everything to one side: an eigenspace is a null space.")
        null_heading.move_to(family_heading)
        derivation = VGroup(
            MathTex(r"A\mathbf v=\lambda\mathbf v", font_size=43, color=WHITE),
            MathTex(r"A\mathbf v-\lambda\mathbf v=\mathbf 0", font_size=43, color=WHITE),
            MathTex(r"(A-\lambda I)\mathbf v=\mathbf 0", font_size=47, color=YELLOW),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.42)
        derivation.move_to(np.array([3.55, 0.15, 0.0]))
        self.play(
            FadeOut(family_heading), FadeIn(null_heading),
            FadeOut(eigenspace_label), FadeOut(zero_label),
            FadeOut(arrows), FadeOut(ghosts), FadeOut(zero_dot),
            FadeIn(derivation[0]),
        )
        self.wait(0.6)
        self.play(FadeIn(derivation[1]))
        self.wait(0.6)
        self.play(FadeIn(derivation[2]))
        self.wait(1.5)

        # Card 4: compute the null space for lambda=2 and reconnect it to the line.
        example_heading = self._heading("For λ = 2, the null space is exactly the line we have been seeing.")
        example_heading.move_to(null_heading)
        shifted = MathTex(
            r"A-2I=\begin{bmatrix}3&3\\3&3\end{bmatrix}",
            font_size=40,
            color=WHITE,
        )
        equation = MathTex(r"x+y=0", font_size=42, color=WHITE)
        conclusion = MathTex(
            r"E_2=\operatorname{Null}(A-2I)=\operatorname{span}\!\left\{\begin{bmatrix}1\\-1\end{bmatrix}\right\}",
            font_size=38,
            color=YELLOW,
        )
        shifted.move_to(np.array([3.55, 0.85, 0.0]))
        equation.next_to(shifted, np.array([0.0, -1.0, 0.0]), buff=0.48)
        equation.set_x(shifted.get_center()[0])
        conclusion.next_to(equation, np.array([0.0, -1.0, 0.0]), buff=0.52)
        conclusion.set_x(shifted.get_center()[0])
        conclusion.scale_to_fit_width(6.2)
        self.play(
            FadeOut(null_heading), FadeIn(example_heading), FadeOut(derivation),
            FadeIn(shifted), FadeIn(equation), FadeIn(conclusion),
        )
        self.wait(2.0)

        # Final synthesis: show both eigenspaces for the same matrix.
        final_heading = self._heading("Each eigenvalue has its own eigenspace.")
        final_heading.move_to(example_heading)
        fast_line = DashedLine(
            plane.c2p(-2.35, -2.35),
            plane.c2p(2.35, 2.35),
            dash_length=0.10,
            color=GREEN_C,
            stroke_opacity=0.8,
            stroke_width=3.0,
        )
        slow_line = DashedLine(
            plane.c2p(-2.35, 2.35),
            plane.c2p(2.35, -2.35),
            dash_length=0.10,
            color=BLUE_C,
            stroke_opacity=0.8,
            stroke_width=3.0,
        )
        fast_label = MathTex(
            r"E_8=\operatorname{Null}(A-8I)=\operatorname{span}\!\left\{\begin{bmatrix}1\\1\end{bmatrix}\right\}",
            font_size=36,
            color=GREEN_C,
        )
        slow_label = MathTex(
            r"E_2=\operatorname{Null}(A-2I)=\operatorname{span}\!\left\{\begin{bmatrix}1\\-1\end{bmatrix}\right\}",
            font_size=36,
            color=BLUE_C,
        )
        fast_label.move_to(np.array([3.55, 0.70, 0.0]))
        slow_label.next_to(fast_label, np.array([0.0, -1.0, 0.0]), buff=0.64)
        slow_label.set_x(fast_label.get_center()[0])
        fast_label.scale_to_fit_width(6.2)
        slow_label.scale_to_fit_width(6.2)
        footer = Text("Eigenvectors are the nonzero vectors in an eigenspace.", font_size=25, color=WHITE)
        footer.to_edge(np.array([0.0, -1.0, 0.0]), buff=0.30)
        footer.scale_to_fit_width(9.5)
        self.play(
            FadeOut(example_heading), FadeIn(final_heading),
            FadeOut(shifted), FadeOut(equation), FadeOut(conclusion), FadeOut(eig_line),
            FadeIn(fast_line), FadeIn(slow_line), FadeIn(fast_label), FadeIn(slow_label), FadeIn(footer),
        )
        self.wait(2.4)
