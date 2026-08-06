"""CP133 presentation: determinant consequences derived from the foundational properties."""
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

from engine.determinant_consequences import (
    build_dependent_rows_example,
    build_equal_rows_example,
    build_row_replacement_example,
    build_zero_row_example,
    summary_lines,
)


class DeterminantConsequencesPresentation(Scene):
    """Continue the determinant-properties sequence with derived consequences."""

    def construct(self) -> None:
        banner = Text("Properties of the Determinant", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = Text(
            "Now we derive new consequences from the earlier properties.",
            font_size=24,
            color=GREY_B,
        ).next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_equal_rows_property(banner)
        self.show_zero_row_property(banner)
        self.show_row_replacement_property(banner)
        self.show_dependent_rows_property(banner)
        self.show_summary(banner)

    def show_equal_rows_property(self, banner: Text) -> None:
        label = Text("Property 4: Equal rows imply determinant zero", font_size=28, color=YELLOW)
        label.move_to(np.array([0.0, 2.2, 0.0]))
        example = build_equal_rows_example()

        axes = Axes(
            x_range=[-0.4, 3.3, 1],
            y_range=[-0.4, 3.3, 1],
            x_length=5.0,
            y_length=5.0,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-3.4, -0.55, 0.0]))
        poly = self.region_polygon(axes, example.image_vertices, ORANGE, 0.32)
        matrix = Matrix([[1, 2], [1, 2]], element_to_mobject_config={"font_size": 34})
        matrix.move_to(np.array([3.25, 1.3, 0.0]))
        general_statement = MathTex(r"\det\!\begin{bmatrix}a&b\\a&b\end{bmatrix}", font_size=34, color=WHITE)
        negated_statement = MathTex(r"=-\det\!\begin{bmatrix}a&b\\a&b\end{bmatrix}", font_size=34, color=RED)
        conclusion = MathTex(r"\therefore\ \det\!\begin{bmatrix}a&b\\a&b\end{bmatrix}=0", font_size=36, color=YELLOW)
        general_statement.move_to(np.array([3.25, 0.1, 0.0]))
        negated_statement.move_to(np.array([3.25, -0.65, 0.0]))
        conclusion.move_to(np.array([3.25, -1.45, 0.0]))
        caption = Text(
            "Swapping equal rows changes nothing, so the determinant must equal its own negative.",
            font_size=22,
            color=WHITE,
        )
        caption.scale_to_fit_width(11.2)
        caption.move_to(np.array([0.0, -3.15, 0.0]))

        self.play(FadeIn(label), Create(axes), FadeIn(poly), FadeIn(matrix))
        self.play(Write(general_statement))
        self.play(Write(negated_statement))
        self.play(Write(conclusion))
        self.play(FadeIn(caption))
        self.wait(1.1)
        self.clear_stage((banner,))

    def show_zero_row_property(self, banner: Text) -> None:
        label = Text("Property 5: A zero row implies determinant zero", font_size=28, color=YELLOW)
        label.move_to(np.array([0.0, 2.2, 0.0]))
        example = build_zero_row_example()

        axes = Axes(
            x_range=[-0.4, 3.3, 1],
            y_range=[-0.4, 3.3, 1],
            x_length=5.0,
            y_length=5.0,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-3.3, -0.5, 0.0]))
        poly = self.region_polygon(axes, example.image_vertices, BLUE, 0.32)
        matrix = Matrix([[0, 0], [1, 2]], element_to_mobject_config={"font_size": 34})
        matrix.move_to(np.array([3.0, 1.15, 0.0]))
        derivation = VGroup(
            MathTex(r"D(0,r_2)=D(0+0,r_2)", font_size=34, color=WHITE),
            MathTex(r"=D(0,r_2)+D(0,r_2)", font_size=34, color=GREEN),
            MathTex(r"\therefore\ D(0,r_2)=0", font_size=36, color=YELLOW),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.16).move_to(np.array([3.05, -0.9, 0.0]))
        caption = Text(
            "A zero row contributes no signed area, so the determinant collapses to zero.",
            font_size=22,
            color=WHITE,
        )
        caption.scale_to_fit_width(11.0)
        caption.move_to(np.array([0.0, -3.15, 0.0]))

        self.play(FadeIn(label), Create(axes), FadeIn(poly), FadeIn(matrix))
        self.play(Write(derivation[0]))
        self.play(Write(derivation[1]))
        self.play(Write(derivation[2]))
        self.play(FadeIn(caption))
        self.wait(1.1)
        self.clear_stage((banner,))

    def show_row_replacement_property(self, banner: Text) -> None:
        label = Text(
            "Property 6: Adding a multiple of one row\n"
            "to another leaves the determinant unchanged",
            font_size=23,
            color=YELLOW,
            line_spacing=0.9,
        )
        label.move_to(np.array([0.0, 2.7, 0.0]))
        example = build_row_replacement_example()

        left_matrix = Matrix([[2, 1], [1, 2]], element_to_mobject_config={"font_size": 30})
        right_matrix = Matrix([[0, -3], [1, 2]], element_to_mobject_config={"font_size": 30})
        left_matrix.move_to(np.array([-3.6, 1.55, 0.0]))
        right_matrix.move_to(np.array([3.6, 1.55, 0.0]))
        operation = MathTex(r"r_1\to r_1-2r_2", font_size=28, color=WHITE)
        operation.move_to(np.array([0.0, 1.55, 0.0]))

        left_axes = Axes(
            x_range=[-0.4, 3.4, 1],
            y_range=[-0.4, 3.4, 1],
            x_length=3.9,
            y_length=3.9,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-3.6, -0.75, 0.0]))
        right_axes = Axes(
            x_range=[-1.2, 3.4, 1],
            y_range=[-3.6, 3.0, 1],
            x_length=4.1,
            y_length=4.1,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([3.6, -0.75, 0.0]))
        left_poly = self.region_polygon(left_axes, example.original.image_vertices, ORANGE, 0.34)
        right_poly = self.region_polygon(right_axes, example.replaced.image_vertices, GREEN, 0.34)

        left_det = MathTex(r"\det(A)=3", font_size=28, color=ORANGE)
        right_det = MathTex(r"\det(r_1-2r_2,r_2)=3", font_size=28, color=GREEN)
        left_det.move_to(np.array([-3.6, -2.55, 0.0]))
        right_det.move_to(np.array([3.6, -2.55, 0.0]))

        derivation_line_one = MathTex(
            r"D(r_1+kr_2,r_2)=D(r_1,r_2)+kD(r_2,r_2)",
            font_size=25,
            color=WHITE,
        )
        derivation_line_two = MathTex(r"=D(r_1,r_2)+k\cdot 0=D(r_1,r_2)", font_size=27, color=YELLOW)
        derivation_line_one.move_to(np.array([0.0, -3.0, 0.0]))
        derivation_line_two.move_to(np.array([0.0, -3.5, 0.0]))

        self.play(FadeIn(label))
        self.play(FadeIn(left_matrix), FadeIn(right_matrix), FadeIn(operation))
        self.play(Create(left_axes), Create(right_axes), FadeIn(left_poly), FadeIn(right_poly))
        self.play(Write(left_det), Write(right_det))
        self.play(Write(derivation_line_one))
        self.play(Write(derivation_line_two))
        self.wait(1.1)
        self.clear_stage((banner,))

    def show_dependent_rows_property(self, banner: Text) -> None:
        label = Text("Property 7: Dependent rows imply determinant zero", font_size=28, color=YELLOW)
        label.move_to(np.array([0.0, 2.2, 0.0]))
        example = build_dependent_rows_example()

        axes = Axes(
            x_range=[-0.4, 5.2, 1],
            y_range=[-0.4, 3.4, 1],
            x_length=5.4,
            y_length=4.6,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-3.1, -0.5, 0.0]))
        poly = self.region_polygon(axes, example.image_vertices, RED, 0.28)
        matrix = Matrix([[2, 4], [1, 2]], element_to_mobject_config={"font_size": 34})
        matrix.move_to(np.array([3.1, 1.15, 0.0]))
        derivation = VGroup(
            MathTex(r"r_1=2r_2", font_size=34, color=WHITE),
            MathTex(r"D(r_1,r_2)=D(2r_2,r_2)=2D(r_2,r_2)", font_size=32, color=GREEN),
            MathTex(r"\therefore\ D(r_1,r_2)=0", font_size=36, color=YELLOW),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.16).move_to(np.array([3.15, -0.8, 0.0]))
        caption = Text(
            "If one row depends on the other, the matrix cannot create two-dimensional area.",
            font_size=22,
            color=WHITE,
        )
        caption.scale_to_fit_width(11.0)
        caption.move_to(np.array([0.0, -3.1, 0.0]))

        self.play(FadeIn(label), Create(axes), FadeIn(poly), FadeIn(matrix))
        self.play(Write(derivation[0]))
        self.play(Write(derivation[1]))
        self.play(Write(derivation[2]))
        self.play(FadeIn(caption))
        self.wait(1.1)
        self.clear_stage((banner,))

    def show_summary(self, banner: Text) -> None:
        label = Text("Summary so far", font_size=28, color=YELLOW)
        label.move_to(np.array([0.0, 2.2, 0.0]))
        lines = summary_lines()
        summary = VGroup(
            Text(lines[0], font_size=24, color=WHITE),
            Text(lines[1], font_size=24, color=WHITE),
            Text(lines[2], font_size=24, color=WHITE),
            Text(lines[3], font_size=24, color=WHITE),
            Text("These consequences will support elimination, triangular matrices, and invertibility.", font_size=23, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22).move_to(np.array([0.0, -0.2, 0.0]))
        self.play(FadeIn(label))
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
