"""CP132 presentation: foundational properties of the determinant."""
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
    Axes,
    DashedLine,
    Create,
    FadeIn,
    FadeOut,
    MathTex,
    Matrix,
    Polygon,
    Scene,
    Text,
    VGroup,
    Write,
)

from engine.determinant_properties import (
    UNIT_SQUARE,
    build_additivity_example,
    build_identity_example,
    build_row_scaling_examples,
    build_row_swap_examples,
    property_summary_lines,
)


class DeterminantPropertiesPresentation(Scene):
    """Enumerate foundational determinant properties in a continuing sequence."""

    def construct(self) -> None:
        banner = Text("Properties of the Determinant", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        self.play(Write(banner))

        subtitle = Text(
            "We are building a list of determinant properties.",
            font_size=24,
            color=GREY_B,
        ).next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_property_one(banner)
        self.show_property_two(banner)
        self.show_property_three_scaling(banner)
        self.show_property_three_additivity(banner)
        self.show_summary(banner)

    def show_property_one(self, banner: Text) -> None:
        label = Text("Property 1: det(I) = 1", font_size=28, color=YELLOW)
        label.move_to(np.array([0.0, 2.15, 0.0]))
        identity = build_identity_example()

        axes = Axes(
            x_range=[-0.3, 1.6, 1],
            y_range=[-0.3, 1.6, 1],
            x_length=4.2,
            y_length=4.2,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-3.2, -0.25, 0.0]))
        square = self.region_polygon(axes, identity.image_vertices, BLUE, 0.38)
        matrix = Matrix([[1, 0], [0, 1]], element_to_mobject_config={"font_size": 36})
        matrix.move_to(np.array([3.2, 0.9, 0.0]))
        lines = VGroup(
            Text("Identity leaves the unit square unchanged.", font_size=24, color=WHITE),
            MathTex(r"\det(I)=1", font_size=36, color=YELLOW),
            Text("Area and orientation are both preserved.", font_size=24, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22).move_to(np.array([3.25, -1.25, 0.0]))

        self.play(FadeIn(label), Create(axes), FadeIn(square), FadeIn(matrix))
        self.play(FadeIn(lines[0]))
        self.play(Write(lines[1]))
        self.play(FadeIn(lines[2]))
        self.wait(1.0)
        self.clear_stage(preserve=(banner,))

    def show_property_two(self, banner: Text) -> None:
        label = Text("Property 2: Swapping two rows changes the sign", font_size=28, color=YELLOW)
        label.move_to(np.array([0.0, 2.15, 0.0]))
        base, swapped = build_row_swap_examples()
        reflected_vertices = base.image_vertices[:, ::-1]

        left_axes = Axes(
            x_range=[-0.4, 3.4, 1],
            y_range=[-0.4, 3.4, 1],
            x_length=4.4,
            y_length=4.4,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-3.4, -0.72, 0.0]))
        right_axes = Axes(
            x_range=[-0.4, 3.4, 1],
            y_range=[-0.4, 3.4, 1],
            x_length=4.4,
            y_length=4.4,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([1.6, -0.72, 0.0]))
        left_poly = self.region_polygon(left_axes, base.image_vertices, ORANGE, 0.38)
        right_poly = self.region_polygon(right_axes, reflected_vertices, RED, 0.38)
        left_matrix = Matrix([[2, 1], [1, 2]], element_to_mobject_config={"font_size": 32})
        right_matrix = Matrix([[1, 2], [2, 1]], element_to_mobject_config={"font_size": 32})
        left_matrix.move_to(np.array([-3.4, 1.2, 0.0]))
        right_matrix.move_to(np.array([1.6, 1.2, 0.0]))
        reflection_line = DashedLine(right_axes.c2p(0, 0), right_axes.c2p(3.1, 3.1), color=GREY_B)
        reflection_caption = Text("reflection across y = x", font_size=20, color=GREY_B)
        reflection_caption.move_to(np.array([1.6, -2.0, 0.0]))
        left_det = MathTex(r"\det\!\begin{bmatrix}2&1\\1&2\end{bmatrix}=3", font_size=29, color=ORANGE)
        right_det_matrix = MathTex(r"\det\!\begin{bmatrix}1&2\\2&1\end{bmatrix}", font_size=27, color=RED)
        right_det_value = MathTex(r"=-3", font_size=31, color=RED)
        right_det = VGroup(right_det_matrix, right_det_value).arrange(np.array([1.0, 0.0, 0.0]), buff=0.16)
        left_det.move_to(np.array([-3.4, -2.95, 0.0]))
        right_det.move_to(np.array([1.6, -2.95, 0.0]))
        bottom_caption = Text("The area magnitude stays the same, but orientation reverses.", font_size=22, color=WHITE)
        bottom_caption.move_to(np.array([0.0, -3.35, 0.0]))

        self.play(FadeIn(label))
        self.play(Create(left_axes), Create(right_axes), FadeIn(left_poly), FadeIn(right_poly), Create(reflection_line))
        self.play(FadeIn(left_matrix), FadeIn(right_matrix), FadeIn(reflection_caption))
        self.play(Write(left_det), FadeIn(right_det))
        self.play(FadeIn(bottom_caption))
        self.wait(1.1)
        self.clear_stage(preserve=(banner,))

    def show_property_three_scaling(self, banner: Text) -> None:
        label = Text("Property 3a: Scaling one row scales the determinant", font_size=28, color=YELLOW)
        label.move_to(np.array([0.0, 2.3, 0.0]))
        base, scaled, factor = build_row_scaling_examples()

        left_axes = Axes(
            x_range=[-0.4, 4.6, 1],
            y_range=[-0.4, 3.6, 1],
            x_length=4.6,
            y_length=4.2,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-3.3, -0.78, 0.0]))
        right_axes = Axes(
            x_range=[-0.4, 5.4, 1],
            y_range=[-0.4, 3.6, 1],
            x_length=4.8,
            y_length=4.2,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([1.7, -0.78, 0.0]))
        left_poly = self.region_polygon(left_axes, base.image_vertices, ORANGE, 0.38)
        right_poly = self.region_polygon(right_axes, scaled.image_vertices, GREEN, 0.38)
        left_matrix = Matrix([[2, 1], [1, 2]], element_to_mobject_config={"font_size": 32})
        right_matrix = Matrix([[4, 2], [1, 2]], element_to_mobject_config={"font_size": 32})
        left_matrix.move_to(np.array([-3.3, 1.35, 0.0]))
        right_matrix.move_to(np.array([1.7, 1.35, 0.0]))
        left_det = MathTex(r"\det(A)=3", font_size=34, color=ORANGE)
        right_det = MathTex(r"\det(2r_1,r_2)=2\det(A)=6", font_size=34, color=GREEN)
        left_det.move_to(np.array([-3.3, -2.75, 0.0]))
        right_det.move_to(np.array([1.7, -2.75, 0.0]))
        bottom_caption = Text(
            f"Multiplying one row by {int(factor)} multiplies the determinant by {int(factor)}.",
            font_size=21,
            color=WHITE,
        )
        bottom_caption.move_to(np.array([0.0, -3.38, 0.0]))

        self.play(FadeIn(label))
        self.play(Create(left_axes), Create(right_axes), FadeIn(left_poly), FadeIn(right_poly))
        self.play(FadeIn(left_matrix), FadeIn(right_matrix))
        self.play(Write(left_det), Write(right_det))
        self.play(FadeIn(bottom_caption))
        self.wait(1.1)
        self.clear_stage(preserve=(banner,))

    def show_property_three_additivity(self, banner: Text) -> None:
        label = Text("Property 3b: The determinant is additive in one row", font_size=28, color=YELLOW)
        label.move_to(np.array([0.0, 2.15, 0.0]))
        additivity = build_additivity_example()

        axes = Axes(
            x_range=[-0.4, 3.4, 1],
            y_range=[-0.4, 3.4, 1],
            x_length=4.6,
            y_length=4.6,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-3.3, -0.1, 0.0]))
        piece_one = self.region_polygon(
            axes,
            np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 2.0], [1.0, 2.0]]),
            GREEN,
            0.3,
        )
        piece_two = self.region_polygon(
            axes,
            np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 3.0], [1.0, 2.0]]),
            BLUE,
            0.3,
        )
        total_poly = self.region_polygon(
            axes,
            np.array([[0.0, 0.0], [2.0, 1.0], [3.0, 3.0], [1.0, 2.0]]),
            ORANGE,
            0.22,
        )
        matrix_block = VGroup(
            MathTex(r"r_1=u+s", font_size=36, color=WHITE),
            MathTex(r"u=(1,0),\quad s=(1,1)", font_size=32, color=WHITE),
            MathTex(r"r_2=(1,2)", font_size=32, color=WHITE),
            MathTex(r"D(u+s,r_2)=D(u,r_2)+D(s,r_2)", font_size=36, color=YELLOW),
            MathTex(r"2+1=3", font_size=38, color=ORANGE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.18).move_to(np.array([2.35, -0.2, 0.0]))
        caption = Text(
            "The orange region is the sum of the green and blue signed areas.",
            font_size=23,
            color=WHITE,
        ).move_to(np.array([0.0, -2.8, 0.0]))

        self.play(FadeIn(label), Create(axes))
        self.play(FadeIn(total_poly), FadeIn(piece_one), FadeIn(piece_two))
        self.play(FadeIn(matrix_block[0]), FadeIn(matrix_block[1]))
        self.play(FadeIn(matrix_block[2]))
        self.play(Write(matrix_block[3]))
        self.play(Write(matrix_block[4]))
        self.play(FadeIn(caption))
        self.wait(1.2)
        self.clear_stage(preserve=(banner,))

    def show_summary(self, banner: Text) -> None:
        summary_title = Text("Summary so far", font_size=28, color=YELLOW)
        summary_title.move_to(np.array([0.0, 2.15, 0.0]))
        lines = property_summary_lines()
        summary = VGroup(
            Text(lines[0], font_size=26, color=WHITE),
            Text(lines[1], font_size=26, color=WHITE),
            Text(lines[2], font_size=26, color=WHITE),
            Text(lines[3], font_size=26, color=WHITE),
            Text("Next we will derive more determinant consequences from these properties.", font_size=24, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22).move_to(np.array([0.0, -0.15, 0.0]))

        self.play(FadeIn(summary_title))
        for item in summary:
            self.play(FadeIn(item))
        self.wait(2.0)

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])

    @staticmethod
    def region_polygon(axes: Axes, vertices: np.ndarray, color, fill_opacity: float) -> Polygon:
        return Polygon(
            *[axes.c2p(float(x), float(y)) for x, y in vertices],
            color=color,
            stroke_width=4,
            fill_color=color,
            fill_opacity=fill_opacity,
        )
