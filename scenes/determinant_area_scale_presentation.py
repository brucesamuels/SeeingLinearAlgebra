"""CP129 presentation: Determinant as Area Scale Factor in R^2."""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    GREEN,
    GREY_B,
    WHITE,
    YELLOW,
    Arrow,
    Axes,
    BraceBetweenPoints,
    Create,
    DashedLine,
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

from engine.determinant_area_scale import (
    UNIT_SQUARE,
    area_scale_statement,
    build_area_scale_example,
)


class DeterminantAreaScalePresentation(Scene):
    """Show that absolute determinant measures planar area scaling."""

    TITLE_SIZE = 42
    BODY_SIZE = 28
    CAPTION_SIZE = 29

    def construct(self) -> None:
        example = build_area_scale_example()

        title = Text("Determinant as Area Scale Factor", font_size=self.TITLE_SIZE)
        title.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.28)
        subtitle = Text(
            "Start with one square unit and watch what the transformation does.",
            font_size=24,
            color=GREY_B,
        ).next_to(title, np.array([0.0, -1.0, 0.0]), buff=0.14)
        self.play(Write(title), FadeIn(subtitle))

        axes = Axes(
            x_range=[-0.5, 4.2, 1],
            y_range=[-0.5, 3.3, 1],
            x_length=6.2,
            y_length=4.7,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-2.65, -0.55, 0.0]))

        square = self.region_polygon(axes, UNIT_SQUARE, BLUE, 0.42)
        square_label = MathTex(r"\text{area}=1", font_size=30, color=BLUE)
        square_label.next_to(square, np.array([0.0, -1.0, 0.0]), buff=0.18)

        e1 = Arrow(axes.c2p(0, 0), axes.c2p(1, 0), buff=0, color=GREEN)
        e2 = Arrow(axes.c2p(0, 0), axes.c2p(0, 1), buff=0, color=YELLOW)
        e1_label = MathTex(r"\mathbf e_1", color=GREEN, font_size=28).next_to(
            e1, np.array([0.0, -1.0, 0.0]), buff=0.08
        )
        e2_label = MathTex(r"\mathbf e_2", color=YELLOW, font_size=28).next_to(
            e2, np.array([-1.0, 0.0, 0.0]), buff=0.08
        )

        matrix_heading = Text("Apply", font_size=24, color=GREY_B)
        matrix = Matrix([[2, 1], [0, 2]], element_to_mobject_config={"font_size": 35})
        matrix_group = VGroup(matrix_heading, matrix).arrange(
            np.array([0.0, -1.0, 0.0]), buff=0.2
        ).move_to(np.array([3.45, 0.85, 0.0]))

        self.play(Create(axes), FadeIn(square), FadeIn(square_label))
        self.play(Create(e1), Create(e2), FadeIn(e1_label), FadeIn(e2_label))
        self.wait(1.0)
        self.play(FadeIn(matrix_group))

        col1, col2 = example.columns
        a1 = Arrow(axes.c2p(0, 0), axes.c2p(*col1), buff=0, color=GREEN)
        a2 = Arrow(axes.c2p(0, 0), axes.c2p(*col2), buff=0, color=YELLOW)
        a1_label = MathTex(r"\mathbf a_1", color=GREEN, font_size=28).next_to(
            a1, np.array([0.0, -1.0, 0.0]), buff=0.08
        )
        a2_label = MathTex(r"\mathbf a_2", color=YELLOW, font_size=28).next_to(
            a2, np.array([1.0, 0.0, 0.0]), buff=0.08
        )
        column_note = Text(
            "The columns are the images of the basis vectors.",
            font_size=25,
            color=WHITE,
        ).move_to(np.array([3.35, -0.7, 0.0]))

        self.play(
            ReplacementTransform(e1, a1),
            ReplacementTransform(e2, a2),
            ReplacementTransform(e1_label, a1_label),
            ReplacementTransform(e2_label, a2_label),
        )
        self.play(FadeIn(column_note))
        self.wait(1.25)

        parallelogram = self.region_polygon(axes, example.image_vertices, GREEN, 0.42)
        transformed_label = MathTex(r"\text{image of the unit square}", font_size=28, color=GREEN)
        transformed_label.next_to(parallelogram, np.array([0.0, 1.0, 0.0]), buff=0.16)

        self.play(
            Transform(square, parallelogram),
            FadeOut(square_label),
            FadeIn(transformed_label),
            run_time=1.7,
        )
        self.wait(1.0)

        base_guide = DashedLine(axes.c2p(0, 0), axes.c2p(2, 0), color=WHITE)
        height_guide = DashedLine(axes.c2p(1, 0), axes.c2p(1, 2), color=WHITE)
        base_brace = BraceBetweenPoints(axes.c2p(0, -0.08), axes.c2p(2, -0.08), direction=np.array([0.0, -1.0, 0.0]))
        height_brace = BraceBetweenPoints(axes.c2p(1.08, 0), axes.c2p(1.08, 2), direction=np.array([1.0, 0.0, 0.0]))
        base_label = MathTex(r"2", font_size=27).next_to(base_brace, np.array([0.0, -1.0, 0.0]), buff=0.08)
        height_label = MathTex(r"2", font_size=27).next_to(height_brace, np.array([1.0, 0.0, 0.0]), buff=0.08)

        area_work = VGroup(
            MathTex(r"\text{area}=\text{base}\cdot\text{height}", font_size=30),
            MathTex(r"=2\cdot2=4", font_size=34, color=YELLOW),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.18)
        area_work.move_to(np.array([3.35, -1.25, 0.0]))

        self.play(
            FadeOut(column_note),
            Create(base_guide),
            Create(height_guide),
            FadeIn(base_brace),
            FadeIn(height_brace),
            FadeIn(base_label),
            FadeIn(height_label),
        )
        self.play(FadeIn(area_work))
        self.wait(1.5)

        comparison = VGroup(
            MathTex(r"\text{original area}=1", font_size=30, color=BLUE),
            MathTex(r"\text{image area}=4", font_size=30, color=GREEN),
            MathTex(r"\text{area scale factor}=\frac{4}{1}=4", font_size=32, color=YELLOW),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.23, aligned_edge=np.array([-1.0, 0.0, 0.0]))
        comparison.move_to(np.array([3.25, -0.95, 0.0]))

        self.play(FadeOut(area_work), FadeOut(matrix_group), FadeIn(comparison))
        self.play(Indicate(comparison[2], color=YELLOW, scale_factor=1.04))
        self.wait(1.4)

        conclusion = MathTex(r"|\det(A)|=\text{area scale factor}", font_size=42, color=YELLOW)
        conclusion.move_to(np.array([0.0, -2.8, 0.0]))
        self.play(FadeIn(conclusion))
        self.wait(1.6)

        sign_preview = Text(
            "The magnitude tells the area change. The sign comes next.",
            font_size=24,
            color=GREY_B,
        ).next_to(conclusion, np.array([0.0, -1.0, 0.0]), buff=0.18)
        self.play(FadeIn(sign_preview))
        self.wait(1.5)

        self.play(
            *[FadeOut(mob) for mob in list(self.mobjects)]
        )
        final_line = Text(area_scale_statement(), font_size=31, color=YELLOW)
        final_line.scale_to_fit_width(11.8)
        self.play(Write(final_line))
        self.wait(2.5)

    @staticmethod
    def region_polygon(axes: Axes, vertices: np.ndarray, color, fill_opacity: float) -> Polygon:
        return Polygon(
            *[axes.c2p(float(x), float(y)) for x, y in vertices],
            color=color,
            stroke_width=4,
            fill_color=color,
            fill_opacity=fill_opacity,
        )
