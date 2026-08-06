"""CP130 presentation: determinant sign and orientation in R^2."""
from __future__ import annotations
import numpy as np
from manim import (
    BLUE, GREEN, GREY_B, RED, WHITE, YELLOW,
    Arrow, Axes, Create, CurvedArrow, FadeIn, FadeOut, Indicate,
    MathTex, Matrix, Polygon, ReplacementTransform, Scene, Text,
    Transform, VGroup, Write,
)
from engine.determinant_orientation import (
    UNIT_SQUARE, build_orientation_examples, sign_statement,
)

class DeterminantOrientationPresentation(Scene):
    """Compare equal-area maps with opposite determinant signs."""

    def construct(self) -> None:
        positive, negative = build_orientation_examples()
        title = Text("Determinant Sign and Orientation", font_size=42)
        title.to_edge(np.array([0.,1.,0.]), buff=0.28)
        subtitle = Text(
            "Equal area changes can still differ in orientation.",
            font_size=25, color=GREY_B,
        ).next_to(title, np.array([0.,-1.,0.]), buff=0.14)
        self.play(Write(title), FadeIn(subtitle))

        axes = Axes(
            x_range=[-1.5,4.0,1], y_range=[-2.4,2.6,1],
            x_length=7.0, y_length=5.3, tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-2.6,-0.45,0.]))
        square = self.region_polygon(axes, UNIT_SQUARE, BLUE, 0.42)
        self.play(Create(axes), FadeIn(square))

        e1 = Arrow(axes.c2p(0,0), axes.c2p(1,0), buff=0, color=GREEN)
        e2 = Arrow(axes.c2p(0,0), axes.c2p(0,1), buff=0, color=YELLOW)
        order_arrow = CurvedArrow(
            axes.c2p(0.72,0.08), axes.c2p(0.08,0.72),
            angle=0.7, color=WHITE,
        )
        order_label = Text("first e1, then e2", font_size=23, color=WHITE)
        order_label.move_to(np.array([3.35,1.5,0.]))
        self.play(Create(e1), Create(e2), Create(order_arrow), FadeIn(order_label))
        self.wait(1.0)

        matrix_pos = Matrix([[2,1],[0,1]], element_to_mobject_config={"font_size":34})
        pos_caption = Text("orientation preserved", font_size=27, color=GREEN)
        pos_group = VGroup(matrix_pos, pos_caption).arrange(np.array([0.,-1.,0.]), buff=0.24)
        pos_group.move_to(np.array([3.35,0.2,0.]))
        pos_poly = self.region_polygon(axes, positive.image_vertices, GREEN, 0.42)
        pos_result = MathTex(r"\det(A)=+2", font_size=38, color=GREEN)
        pos_result.move_to(np.array([3.35,-1.25,0.]))
        self.play(FadeIn(pos_group), Transform(square, pos_poly))
        self.play(FadeIn(pos_result))
        self.play(Indicate(pos_caption, color=GREEN, scale_factor=1.05))
        self.wait(1.3)

        matrix_neg = Matrix([[2,1],[0,-1]], element_to_mobject_config={"font_size":34})
        neg_caption = Text("orientation reversed", font_size=27, color=RED)
        neg_group = VGroup(matrix_neg, neg_caption).arrange(np.array([0.,-1.,0.]), buff=0.24)
        neg_group.move_to(np.array([3.35,0.2,0.]))
        neg_poly = self.region_polygon(axes, negative.image_vertices, RED, 0.42)
        neg_result = MathTex(r"\det(B)=-2", font_size=38, color=RED)
        neg_result.move_to(np.array([3.35,-1.25,0.]))
        reverse_arrow = CurvedArrow(
            axes.c2p(0.72,-0.08), axes.c2p(0.08,-0.72),
            angle=-0.7, color=RED,
        )
        self.play(
            ReplacementTransform(pos_group, neg_group),
            ReplacementTransform(pos_result, neg_result),
            Transform(square, neg_poly),
            ReplacementTransform(order_arrow, reverse_arrow),
        )
        self.play(Indicate(neg_caption, color=RED, scale_factor=1.05))
        self.wait(1.4)

        comparison = VGroup(
            MathTex(r"|\det(A)|=|\det(B)|=2", font_size=34, color=YELLOW),
            Text("same area scale", font_size=27, color=YELLOW),
            MathTex(r"\det(A)>0:\ \text{orientation preserved}", font_size=30, color=GREEN),
            MathTex(r"\det(B)<0:\ \text{orientation reversed}", font_size=30, color=RED),
        ).arrange(np.array([0.,-1.,0.]), buff=0.22)
        comparison.move_to(np.array([2.9,-0.25,0.]))
        self.play(FadeOut(neg_group), FadeOut(neg_result), FadeOut(order_label), FadeIn(comparison))
        self.wait(1.8)

        conclusion = MathTex(
            r"\operatorname{sign}(\det A)\ \text{records orientation}",
            font_size=39, color=YELLOW,
        ).move_to(np.array([0.,-3.05,0.]))
        self.play(FadeIn(conclusion))
        self.wait(1.8)

        self.play(*[FadeOut(mob) for mob in list(self.mobjects)])
        final_line = Text(sign_statement(), font_size=34, color=YELLOW)
        final_line.scale_to_fit_width(11.6)
        self.play(Write(final_line))
        self.wait(2.5)

    @staticmethod
    def region_polygon(axes: Axes, vertices: np.ndarray, color, fill_opacity: float) -> Polygon:
        return Polygon(
            *[axes.c2p(float(x), float(y)) for x,y in vertices],
            color=color, stroke_width=4, fill_color=color, fill_opacity=fill_opacity,
        )
