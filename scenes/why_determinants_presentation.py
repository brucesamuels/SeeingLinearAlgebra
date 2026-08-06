"""CP128 presentation: Why Do We Need Determinants?

Student-facing design principles:
- meaning before formulas;
- one stable coordinate system and reference square;
- four geometric behaviors in a deliberate sequence;
- no entrywise determinant formula appears.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    GREEN,
    GREY_B,
    ORANGE,
    RED,
    WHITE,
    YELLOW,
    AnimationGroup,
    Arrow,
    Axes,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    MathTex,
    Matrix,
    Polygon,
    ReplacementTransform,
    Scene,
    Text,
    Transform,
    VGroup,
    Write,
)

from engine.determinant_need import UNIT_SQUARE, build_examples, central_question


class WhyDeterminantsPresentation(Scene):
    """Open Chapter 5 by motivating the determinant geometrically."""

    TITLE_SIZE = 42
    BODY_SIZE = 28
    CAPTION_SIZE = 30
    QUESTION_SIZE = 34
    FRAME_SCALE = 1.55

    def construct(self) -> None:
        title = Text("Why Do We Need Determinants?", font_size=self.TITLE_SIZE)
        title.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.28)
        subtitle = Text(
            "One number can summarize what a linear transformation does to space.",
            font_size=24,
            color=GREY_B,
        ).next_to(title, np.array([0.0, -1.0, 0.0]), buff=0.14)
        self.play(Write(title), FadeIn(subtitle, shift=np.array([0.0, 0.12, 0.0])))
        self.wait(1.2)

        axes = Axes(
            x_range=[-2.5, 3.5, 1],
            y_range=[-1.5, 2.8, 1],
            x_length=6.2,
            y_length=4.4,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-2.7, -0.55, 0.0]))

        original = self.region_polygon(axes, UNIT_SQUARE, color=BLUE, fill_opacity=0.42)
        original_label = MathTex(r"\text{reference region}", font_size=28, color=BLUE)
        original_label.next_to(original, np.array([0.0, -1.0, 0.0]), buff=0.18)

        matrix_panel = VGroup(
            Text("Linear map", font_size=24, color=GREY_B),
            Matrix([[2, 1], [0, 1]], element_to_mobject_config={"font_size": 34}),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.2)
        matrix_panel.move_to(np.array([3.5, 0.65, 0.0]))

        arrow = Arrow(
            start=np.array([0.55, 0.1, 0.0]),
            end=np.array([1.65, 0.1, 0.0]),
            buff=0.0,
            color=YELLOW,
        )
        arrow_text = MathTex(r"A", font_size=34, color=YELLOW).next_to(
            arrow, np.array([0.0, 1.0, 0.0]), buff=0.08
        )

        self.play(Create(axes), FadeIn(original), FadeIn(original_label))
        self.play(FadeIn(matrix_panel), Create(arrow), FadeIn(arrow_text))
        self.wait(0.8)

        examples = build_examples()
        current_polygon = original
        current_matrix = matrix_panel[1]
        current_caption = None
        current_scale = None

        colors = {"expand": GREEN, "contract": ORANGE, "reverse": RED, "collapse": YELLOW}
        display_matrices = {
            "expand": [[2, 1], [0, 1]],
            "contract": [[1, 0], [0, r"\frac12"]],
            "reverse": [[-1, 0], [0, 1]],
            "collapse": [[1, 2], [0, 0]],
        }
        scale_language = {
            "expand": r"\text{signed scale: }+2",
            "contract": r"\text{signed scale: }+\frac12",
            "reverse": r"\text{signed scale: }-1",
            "collapse": r"\text{signed scale: }0",
        }

        for index, example in enumerate(examples):
            transformed_vertices = UNIT_SQUARE @ example.matrix.T
            target_polygon = self.region_polygon(
                axes,
                transformed_vertices,
                color=colors[example.key],
                fill_opacity=0.48 if example.key != "collapse" else 0.18,
            )
            target_matrix = Matrix(
                display_matrices[example.key],
                element_to_mobject_config={"font_size": 34},
            ).move_to(current_matrix)
            caption = Text(
                example.caption,
                font_size=self.CAPTION_SIZE,
                color=colors[example.key],
            ).move_to(np.array([3.5, -0.7, 0.0]))
            scale = MathTex(
                scale_language[example.key],
                font_size=30,
                color=WHITE,
            ).next_to(caption, np.array([0.0, -1.0, 0.0]), buff=0.22)

            animations = [
                Transform(current_polygon, target_polygon),
                ReplacementTransform(current_matrix, target_matrix),
            ]
            if current_caption is not None:
                animations.extend([FadeOut(current_caption), FadeOut(current_scale)])
            self.play(*animations, run_time=1.5)
            current_matrix = target_matrix
            self.play(FadeIn(caption), FadeIn(scale))
            current_caption = caption
            current_scale = scale
            if index == 2:
                self.play(Indicate(current_polygon, color=RED, scale_factor=1.04))
            self.wait(1.15)

        self.play(
            FadeOut(matrix_panel[0]),
            FadeOut(current_matrix),
            FadeOut(arrow),
            FadeOut(arrow_text),
            FadeOut(current_caption),
            FadeOut(current_scale),
            FadeOut(original_label),
            FadeOut(current_polygon),
            FadeOut(axes),
            FadeOut(subtitle),
        )

        behaviors = VGroup(
            Text("expand or contract", font_size=29, color=GREEN),
            Text("preserve or reverse orientation", font_size=29, color=RED),
            Text("collapse a dimension", font_size=29, color=YELLOW),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.32, aligned_edge=np.array([-1.0, 0.0, 0.0]))
        behaviors.move_to(np.array([0.0, 0.55, 0.0]))

        lead = Text("A linear transformation can", font_size=30).next_to(
            behaviors, np.array([0.0, 1.0, 0.0]), buff=0.4
        )
        self.play(FadeIn(lead), AnimationGroup(*[FadeIn(item) for item in behaviors], lag_ratio=0.25))
        self.wait(1.5)

        determinant_line = VGroup(
            Text("The determinant records all three with", font_size=30),
            Text("one signed scale factor.", font_size=34, color=YELLOW),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.16)
        determinant_line.move_to(np.array([0.0, -1.3, 0.0]))
        self.play(FadeIn(determinant_line))
        self.wait(1.6)

        self.play(FadeOut(lead), FadeOut(behaviors), FadeOut(determinant_line), FadeOut(title))
        question = Text(
            central_question(),
            font_size=self.QUESTION_SIZE,
            color=YELLOW,
        )
        question.scale_to_fit_width(12.2)
        question.move_to(np.array([0.0, 0.25, 0.0]))
        chapter = Text("Chapter 5: Determinants", font_size=28, color=GREY_B)
        chapter.next_to(question, np.array([0.0, -1.0, 0.0]), buff=0.55)
        self.play(Write(question), FadeIn(chapter))
        self.wait(2.8)

    @staticmethod
    def region_polygon(axes: Axes, vertices: np.ndarray, *, color, fill_opacity: float) -> Polygon:
        points = [axes.c2p(float(x), float(y)) for x, y in vertices]
        return Polygon(
            *points,
            color=color,
            stroke_width=4,
            fill_color=color,
            fill_opacity=fill_opacity,
        )
