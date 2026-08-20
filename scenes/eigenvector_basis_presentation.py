"""Manim presentation for Chapter 7 lesson 7: an eigenvector basis."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C,
    GREEN_C,
    GREY_B,
    ORANGE,
    PURPLE_C,
    WHITE,
    YELLOW,
    Arrow3D,
    FadeIn,
    FadeOut,
    MathTex,
    ReplacementTransform,
    Text,
    ThreeDAxes,
    ThreeDScene,
    VGroup,
)

from engine.eigenvector_basis import EigenvectorBasisLesson


DOWN = np.array([0.0, -1.0, 0.0])
UP = np.array([0.0, 1.0, 0.0])
LEFT = np.array([-1.0, 0.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])


class EigenvectorBasisPresentation(ThreeDScene):
    """Show why an eigenvector basis makes a transformation act coordinate by coordinate."""

    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "An Eigenvector Basis"
    CAMERA_PHI = 68 * np.pi / 180
    CAMERA_THETA = -48 * np.pi / 180

    def _screen_plane_shift(self, *, left: float, down: float) -> np.ndarray:
        """Return a world-space translation parallel to the camera's screen plane."""
        theta = self.CAMERA_THETA
        phi = self.CAMERA_PHI
        screen_right = np.array([-np.sin(theta), np.cos(theta), 0.0])
        screen_up = np.array([
            np.cos(phi) * np.cos(theta),
            np.cos(phi) * np.sin(theta),
            -np.sin(phi),
        ])
        return -left * screen_right - down * screen_up

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.7:
            item.scale_to_fit_width(11.7)
        return item

    def _chrome(self, heading_text: str) -> tuple[Text, Text, Text]:
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD")
        banner.to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=32, color=YELLOW, weight="BOLD")
        title.next_to(banner, DOWN, buff=0.12)
        heading = self._heading(heading_text)
        heading.next_to(title, DOWN, buff=0.17)
        self.add_fixed_in_frame_mobjects(banner, title, heading)
        return banner, title, heading

    def _replace_heading(self, old: Text, text: str) -> Text:
        new = self._heading(text)
        new.move_to(old)
        self.add_fixed_in_frame_mobjects(new)
        self.play(ReplacementTransform(old, new), run_time=0.55)
        return new

    def _fixed_group(self, *items) -> VGroup:
        group = VGroup(*items)
        self.add_fixed_in_frame_mobjects(*items)
        return group

    def construct(self) -> None:
        lesson = EigenvectorBasisLesson()
        example = lesson.example()
        self.set_camera_orientation(phi=self.CAMERA_PHI, theta=self.CAMERA_THETA, zoom=0.82)

        banner, title, heading = self._chrome("Three independent eigenvectors give us a new coordinate system.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.8)

        # Card 1 — recall the basis from CP173.
        basis_line = MathTex(
            r"\mathcal B=\left\{"
            r"\mathbf v_1=\begin{bmatrix}0\\0\\1\end{bmatrix},\ "
            r"\mathbf v_2=\begin{bmatrix}1\\-2\\0\end{bmatrix},\ "
            r"\mathbf v_3=\begin{bmatrix}1\\1\\0\end{bmatrix}"
            r"\right\}",
            font_size=38,
            color=WHITE,
        )
        basis_note = Text("Because these three vectors are independent, they form a basis for R^3.", font_size=27, color=YELLOW)
        recall = self._fixed_group(basis_line, basis_note).arrange(DOWN, buff=0.58)
        recall.move_to(np.array([0.0, -0.25, 0.0]))
        self.play(FadeIn(basis_line))
        self.play(FadeIn(basis_note))
        self.wait(1.4)

        # Card 2 — visualize the three eigenvector directions in 3D.
        heading = self._replace_heading(heading, "Use the eigenvectors themselves as coordinate directions.")
        self.play(FadeOut(recall))
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-2, 2, 1], x_length=5.0, y_length=5.0, z_length=3.6)
        v1 = Arrow3D(start=axes.c2p(0,0,0), end=axes.c2p(0,0,1), color=PURPLE_C, thickness=0.025)
        v2 = Arrow3D(start=axes.c2p(0,0,0), end=axes.c2p(1,-2,0), color=BLUE_C, thickness=0.025)
        v3 = Arrow3D(start=axes.c2p(0,0,0), end=axes.c2p(1,1,0), color=GREEN_C, thickness=0.025)
        labels = [
            MathTex(r"\mathbf v_1", font_size=30, color=PURPLE_C).move_to(axes.c2p(0.12, 0.05, 1.28)),
            MathTex(r"\mathbf v_2", font_size=30, color=BLUE_C).move_to(axes.c2p(1.25, -2.2, 0.12)),
            MathTex(r"\mathbf v_3", font_size=30, color=GREEN_C).move_to(axes.c2p(1.18, 1.18, 0.10)),
        ]
        self.play(FadeIn(axes), FadeIn(v1), FadeIn(v2), FadeIn(v3), *(FadeIn(label) for label in labels), run_time=1.2)
        self.wait(1.5)

        # Card 3 — decompose a generic vector in the eigenbasis.
        heading = self._replace_heading(heading, "A vector is described by how much of each eigenvector it contains.")
        geometry_group = VGroup(axes, v1, v2, v3, *labels)
        layout_shift = self._screen_plane_shift(left=2.6, down=0.45)
        self.play(
            geometry_group.animate.shift(layout_shift),
            run_time=0.85,
        )
        x_arrow = Arrow3D(start=axes.c2p(0,0,0), end=axes.c2p(*example.standard_vector), color=ORANGE, thickness=0.055)
        decomposition = MathTex(
            r"\mathbf x=\mathbf v_1+\mathbf v_2+\mathbf v_3=\begin{bmatrix}2\\-1\\1\end{bmatrix}",
            font_size=38,
            color=WHITE,
        )
        coords = MathTex(r"[\mathbf x]_{\mathcal B}=\begin{bmatrix}1\\1\\1\end{bmatrix}", font_size=42, color=ORANGE)
        algebra = self._fixed_group(decomposition, coords).arrange(DOWN, buff=0.50)
        algebra.to_edge(RIGHT, buff=0.55).shift(DOWN * 0.35)
        x_label = MathTex(r"\mathbf x", font_size=34, color=ORANGE).move_to(axes.c2p(2.25, -1.0, 1.2))
        self.play(FadeIn(x_arrow), FadeIn(x_label), FadeIn(decomposition))
        self.play(FadeIn(coords))
        self.wait(1.5)

        # Card 4 — apply A to each basis component.
        self.play(FadeOut(decomposition), FadeOut(coords), FadeOut(x_label), run_time=0.5)
        self.remove(decomposition, coords, x_label)
        heading = self._replace_heading(heading, "Each eigenvector component scales independently under A.")
        action = MathTex(
            r"A\mathbf v_1=1\mathbf v_1,\qquad "
            r"A\mathbf v_2=2\mathbf v_2,\qquad "
            r"A\mathbf v_3=5\mathbf v_3",
            font_size=36,
            color=WHITE,
        )
        action.set_color_by_tex(r"1\mathbf v_1", PURPLE_C)
        action.set_color_by_tex(r"2\mathbf v_2", BLUE_C)
        action.set_color_by_tex(r"5\mathbf v_3", GREEN_C)
        transformed_combo = MathTex(
            r"A\mathbf x=1\mathbf v_1+2\mathbf v_2+5\mathbf v_3",
            font_size=40,
            color=YELLOW,
        )
        transformed_coords = MathTex(
            r"[A\mathbf x]_{\mathcal B}=\begin{bmatrix}1\\2\\5\end{bmatrix}",
            font_size=42,
            color=ORANGE,
        )
        action_group = self._fixed_group(action, transformed_combo, transformed_coords).arrange(DOWN, buff=0.42)
        action_group.to_edge(RIGHT, buff=0.45).shift(DOWN * 0.25)
        self.play(FadeIn(action))
        self.play(FadeIn(transformed_combo))
        ax_arrow = Arrow3D(start=axes.c2p(0,0,0), end=axes.c2p(*example.transformed_vector), color=YELLOW, thickness=0.035)
        self.play(FadeOut(x_arrow), run_time=0.4)
        self.play(FadeIn(ax_arrow), run_time=0.55)
        self.play(FadeIn(transformed_coords))
        self.wait(1.7)

        # Card 5 — coordinate-to-coordinate view.
        heading = self._replace_heading(heading, "In eigenvector coordinates, A does not mix the coordinates.")
        self.play(FadeOut(axes), FadeOut(v1), FadeOut(v2), FadeOut(v3), FadeOut(ax_arrow), *(FadeOut(label) for label in labels), FadeOut(action_group))
        before = MathTex(r"[\mathbf x]_{\mathcal B}=\begin{bmatrix}1\\1\\1\end{bmatrix}", font_size=48, color=WHITE)
        scale = MathTex(
            r"\begin{bmatrix}1&0&0\\0&2&0\\0&0&5\end{bmatrix}",
            font_size=52,
            color=YELLOW,
        )
        after = MathTex(r"[A\mathbf x]_{\mathcal B}=\begin{bmatrix}1\\2\\5\end{bmatrix}", font_size=48, color=GREEN_C)
        arrow1 = MathTex(r"\longrightarrow", font_size=44, color=GREY_B)
        arrow2 = MathTex(r"\longrightarrow", font_size=44, color=GREY_B)
        coordinate_flow = self._fixed_group(before, arrow1, scale, arrow2, after).arrange(RIGHT, buff=0.38)
        if coordinate_flow.width > 12.0:
            coordinate_flow.scale_to_fit_width(12.0)
        coordinate_flow.move_to(np.array([0.0, -0.20, 0.0]))
        note = Text("The transformation becomes independent scaling along the three eigenvector directions.", font_size=27, color=WHITE)
        self.add_fixed_in_frame_mobjects(note)
        note.next_to(coordinate_flow, DOWN, buff=0.66)
        self.play(FadeIn(before))
        self.play(FadeIn(arrow1), FadeIn(scale), FadeIn(arrow2))
        self.play(FadeIn(after))
        self.play(FadeIn(note))
        self.wait(1.7)

        # Card 6 — synthesis, deliberately stopping before formal diagonalization.
        heading = self._replace_heading(heading, "An eigenvector basis turns one complicated transformation into simple scaling.")
        conclusion1 = MathTex(
            r"\mathbf x=c_1\mathbf v_1+c_2\mathbf v_2+c_3\mathbf v_3",
            font_size=42,
            color=WHITE,
        )
        conclusion2 = MathTex(
            r"A\mathbf x=c_1\mathbf v_1+2c_2\mathbf v_2+5c_3\mathbf v_3",
            font_size=42,
            color=GREEN_C,
        )
        takeaway = Text("Next: encode this change of coordinates with matrices.", font_size=28, color=YELLOW)
        synthesis = self._fixed_group(conclusion1, conclusion2, takeaway).arrange(DOWN, buff=0.58)
        synthesis.move_to(np.array([0.0, -0.20, 0.0]))
        self.play(FadeOut(coordinate_flow), FadeOut(note), FadeIn(conclusion1))
        self.play(FadeIn(conclusion2))
        self.play(FadeIn(takeaway))
        self.wait(2.0)
