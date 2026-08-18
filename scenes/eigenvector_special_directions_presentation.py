"""Manim presentation for Chapter 7 lesson 1: special directions."""
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
    TEAL_C,
    PURPLE_C,
    GREY_B,
    GREY_D,
    linear,
)

from engine.eigenvector_special_directions import (
    DEFAULT_MATRIX,
    ROTATION_MATRIX,
    SAMPLE_VECTORS,
    SpecialDirectionsLesson,
)


class EigenvectorSpecialDirectionsPresentation(Scene):
    """Discover invariant directions by contrasting two transformations."""

    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Why Eigenvectors? — Special Directions of a Transformation"
    OPENING_HEADING = "Do any directions stay on their original lines?"
    ROTATION_HEADING = "A 90° rotation moves every nonzero vector to a different line."
    CONTRAST_HEADING = "Now compare a transformation with two special directions."
    SPECIAL_HEADING = "This time, two directions stay on the same line."
    FINAL_STATEMENT = "These special directions are eigenvector directions."

    VECTOR_COLORS = (BLUE_C, GREEN_C, TEAL_C, PURPLE_C, YELLOW, YELLOW)
    SPECIAL_INDICES = (4, 5)

    @staticmethod
    def _fit_heading(text: str) -> Text:
        heading = Text(text, font_size=30, color=WHITE)
        if heading.width > 12.3:
            heading.scale_to_fit_width(12.3)
        return heading

    def construct(self) -> None:
        rotation_lesson = SpecialDirectionsLesson(ROTATION_MATRIX)
        special_lesson = SpecialDirectionsLesson(DEFAULT_MATRIX)

        banner = Text(
            self.CHAPTER_BANNER,
            font_size=22,
            color=GREY_B,
            weight="BOLD",
        ).to_edge(np.array([0.0, 1.0, 0.0]), buff=0.18)

        title = Text(
            self.LESSON_TITLE,
            font_size=34,
            color=YELLOW,
            weight="BOLD",
        )
        title.scale_to_fit_width(12.7)
        title.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.16)

        heading = self._fit_heading(self.OPENING_HEADING)
        heading.next_to(title, np.array([0.0, -1.0, 0.0]), buff=0.24)

        plane = NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            x_length=9.5,
            y_length=5.0,
            background_line_style={"stroke_opacity": 0.34, "stroke_width": 1.2},
            axis_config={"stroke_opacity": 0.7, "stroke_width": 1.5},
        )
        plane.shift(np.array([0.0, -0.72, 0.0]))

        rotation_tex = MathTex(
            r"R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}",
            font_size=34,
            color=WHITE,
        )
        rotation_tex.move_to(np.array([5.05, 1.0, 0.0]))

        special_tex = MathTex(
            r"A=\begin{bmatrix}5&3\\3&5\end{bmatrix}",
            font_size=34,
            color=WHITE,
        )
        special_tex.move_to(rotation_tex)

        caption = Text(
            "Compare each image with its original dashed line.",
            font_size=24,
            color=GREY_B,
        ).to_edge(np.array([0.0, -1.0, 0.0]), buff=0.28)

        origin = plane.c2p(0, 0)
        rotation_observations = [rotation_lesson.observe(v) for v in SAMPLE_VECTORS]
        special_observations = [special_lesson.observe(v) for v in SAMPLE_VECTORS]

        rays = VGroup()
        ghost_arrows = VGroup()
        arrows = VGroup()
        for index, vector in enumerate(SAMPLE_VECTORS):
            direction = vector / np.linalg.norm(vector)
            ray_start = plane.c2p(*(direction * -3.7))
            ray_end = plane.c2p(*(direction * 3.7))
            ray = DashedLine(
                ray_start,
                ray_end,
                dash_length=0.10,
                color=GREY_D,
                stroke_opacity=0.34,
                stroke_width=1.4,
            )
            rays.add(ray)

            ghost_arrow = DashedLine(
                origin,
                plane.c2p(*vector),
                dash_length=0.11,
                color=self.VECTOR_COLORS[index],
                stroke_opacity=0.34,
                stroke_width=3.0,
            )
            ghost_arrows.add(ghost_arrow)

            arrow = Arrow(
                origin,
                plane.c2p(*vector),
                buff=0,
                color=self.VECTOR_COLORS[index],
                stroke_width=5.0,
                max_tip_length_to_length_ratio=0.16,
            )
            arrows.add(arrow)

        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))
        self.play(Create(plane), run_time=1.4)
        self.play(FadeIn(rays), FadeIn(ghost_arrows), FadeIn(arrows), FadeIn(rotation_tex), FadeIn(caption))
        self.wait(1.0)

        # Act I: rotate every vector by 90 degrees. No nonzero real direction
        # remains on its original dashed line.
        rotation_heading = self._fit_heading(self.ROTATION_HEADING)
        rotation_heading.move_to(heading)
        self.play(FadeOut(heading), FadeIn(rotation_heading))
        self.play(
            *[
                arrow.animate.put_start_and_end_on(
                    origin, plane.c2p(*observation.image)
                )
                for arrow, observation in zip(arrows, rotation_observations)
            ],
            run_time=2.4,
            rate_func=linear,
        )
        self.wait(1.6)

        no_same_line = Text(
            "No image stays on its original line.",
            font_size=25,
            color=WHITE,
        ).to_edge(np.array([0.0, -1.0, 0.0]), buff=0.28)
        self.play(FadeOut(caption), FadeIn(no_same_line))
        self.wait(1.4)

        # Reset the same arrows before applying the contrasting transformation.
        contrast_heading = self._fit_heading(self.CONTRAST_HEADING)
        contrast_heading.move_to(rotation_heading)
        self.play(
            FadeOut(rotation_heading),
            FadeIn(contrast_heading),
            FadeOut(no_same_line),
            ReplacementTransform(rotation_tex, special_tex),
            *[
                arrow.animate.put_start_and_end_on(origin, plane.c2p(*vector))
                for arrow, vector in zip(arrows, SAMPLE_VECTORS)
            ],
            run_time=1.5,
        )
        self.wait(0.8)

        compare_caption = Text(
            "Watch the original dashed lines again.",
            font_size=24,
            color=GREY_B,
        ).to_edge(np.array([0.0, -1.0, 0.0]), buff=0.28)
        self.play(FadeIn(compare_caption))
        special_display_scale = 0.48
        self.play(
            *[
                arrow.animate.put_start_and_end_on(
                    origin, plane.c2p(*(special_display_scale * observation.image))
                )
                for arrow, observation in zip(arrows, special_observations)
            ],
            run_time=2.8,
            rate_func=linear,
        )
        # Hold the full comparison: live transformed vectors in front, frozen
        # dashed originals behind them.  This is the key visual evidence.
        self.wait(2.0)

        special_heading = self._fit_heading(self.SPECIAL_HEADING)
        special_heading.move_to(contrast_heading)
        generic_indices = tuple(i for i in range(len(arrows)) if i not in self.SPECIAL_INDICES)
        self.play(
            FadeOut(contrast_heading),
            FadeIn(special_heading),
            *[FadeOut(arrows[i]) for i in generic_indices],
            *[FadeOut(ghost_arrows[i]) for i in generic_indices],
            *[FadeOut(rays[i]) for i in generic_indices],
            *[
                rays[i].animate.set_color(YELLOW).set_opacity(0.90).set_stroke(width=2.8)
                for i in self.SPECIAL_INDICES
            ],
            run_time=1.2,
        )

        same_line_labels = VGroup(
            Text("same line", font_size=22, color=YELLOW),
            Text("same line", font_size=22, color=YELLOW),
        )
        same_line_labels[0].move_to(plane.c2p(-2.25, -2.45))
        same_line_labels[1].move_to(plane.c2p(2.25, -2.45))
        self.play(FadeIn(same_line_labels))
        self.wait(1.8)

        final_statement = Text(self.FINAL_STATEMENT, font_size=26, color=YELLOW)
        final_statement.scale_to_fit_width(9.8)
        final_statement.to_edge(np.array([0.0, -1.0, 0.0]), buff=0.28)
        self.play(FadeOut(compare_caption), FadeIn(final_statement))
        self.wait(2.0)
