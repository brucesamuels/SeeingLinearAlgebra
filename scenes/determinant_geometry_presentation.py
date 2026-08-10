"""CP145 presentation: determinant as signed area and volume scaling."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE, FadeIn, FadeOut, GREEN, GREY_B, MathTex, NumberPlane, Polygon,
    RED, Scene, Text, VGroup, WHITE, YELLOW, Write, Line, Dot, Arrow,
    ReplacementTransform,
)

from engine.determinant_geometry import (
    area_example_det,
    area_example_matrix,
    closing_lines,
    product_scaling_tex,
    signed_scale_tex,
    singular_det,
    theorem_tex,
    volume_scale,
)


class DeterminantGeometryPresentation(Scene):
    """Visualize determinant magnitude as area/volume scaling and sign as orientation."""

    def construct(self) -> None:
        banner = Text("The Geometry of the Determinant", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.22)
        subtitle = Text("Signed area and volume scaling", font_size=26, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.10)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_unit_square_map(banner)
        self.show_area_scale(banner)
        self.show_orientation(banner)
        self.show_singular_collapse(banner)
        self.show_volume_scale(banner)
        self.show_volume_collapse(banner)
        self.show_multiplicativity_geometry(banner)
        self.show_takeaway(banner)

    def stage_title(self, text: str, size: int = 27) -> Text:
        title = Text(text, font_size=size, color=YELLOW)
        title.move_to(np.array([0.0, 2.28, 0.0]))
        return title

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])

    def show_unit_square_map(self, banner: Text) -> None:
        title = self.stage_title("A matrix sends the unit square to a parallelogram")
        matrix = MathTex(r"A=\begin{bmatrix}2&1\\0&1\end{bmatrix}", font_size=31, color=WHITE)
        matrix.move_to(np.array([0.0, 1.55, 0.0]))

        plane = NumberPlane(x_range=[-1, 4, 1], y_range=[-1, 3, 1], x_length=6.2, y_length=4.0)
        plane.move_to(np.array([0.0, -0.45, 0.0]))
        origin = plane.c2p(0, 0)
        unit = Polygon(plane.c2p(0,0), plane.c2p(1,0), plane.c2p(1,1), plane.c2p(0,1), color=BLUE, fill_opacity=0.30)
        image = Polygon(plane.c2p(0,0), plane.c2p(2,0), plane.c2p(3,1), plane.c2p(1,1), color=GREEN, fill_opacity=0.30)
        e1 = Arrow(origin, plane.c2p(1,0), buff=0, color=BLUE)
        e2 = Arrow(origin, plane.c2p(0,1), buff=0, color=BLUE)
        a1 = Arrow(origin, plane.c2p(2,0), buff=0, color=GREEN)
        a2 = Arrow(origin, plane.c2p(1,1), buff=0, color=GREEN)
        labels = VGroup(
            MathTex(r"\mathbf e_1", font_size=22, color=BLUE).next_to(e1, np.array([0,-1,0]), buff=0.08),
            MathTex(r"\mathbf e_2", font_size=22, color=BLUE).next_to(e2, np.array([-1,0,0]), buff=0.08),
        )

        self.play(FadeIn(title), Write(matrix))
        self.play(FadeIn(plane), FadeIn(unit), FadeIn(e1), FadeIn(e2), FadeIn(labels))
        self.wait(0.8)
        self.play(ReplacementTransform(unit, image), ReplacementTransform(e1, a1), ReplacementTransform(e2, a2), FadeOut(labels))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_area_scale(self, banner: Text) -> None:
        title = self.stage_title("The determinant measures area scaling")
        plane = NumberPlane(x_range=[-1, 4, 1], y_range=[-1, 3, 1], x_length=6.2, y_length=4.0)
        plane.move_to(np.array([-2.6, -0.35, 0.0]))
        image = Polygon(plane.c2p(0,0), plane.c2p(2,0), plane.c2p(3,1), plane.c2p(1,1), color=GREEN, fill_opacity=0.35)
        formula = VGroup(
            MathTex(r"\det(A)=2", font_size=35, color=GREEN),
            MathTex(r"\text{unit area }1\longmapsto\text{ area }2", font_size=27, color=WHITE),
            MathTex(theorem_tex(), font_size=31, color=BLUE),
        ).arrange(np.array([0.0,-1.0,0.0]), buff=0.32)
        formula.scale_to_fit_width(6.2)
        formula.move_to(np.array([3.35, -0.40, 0.0]))
        self.play(FadeIn(title), FadeIn(plane), FadeIn(image))
        for line in formula:
            self.play(Write(line))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_orientation(self, banner: Text) -> None:
        title = self.stage_title("The sign records orientation")
        left_axes = NumberPlane(x_range=[-2,2,1], y_range=[-1,2,1], x_length=4.2, y_length=3.2).move_to(np.array([-3.4,-0.45,0.0]))
        right_axes = NumberPlane(x_range=[-2,2,1], y_range=[-1,2,1], x_length=4.2, y_length=3.2).move_to(np.array([3.4,-0.45,0.0]))
        pos = Polygon(left_axes.c2p(0,0), left_axes.c2p(1,0), left_axes.c2p(2,1), left_axes.c2p(1,1), color=GREEN, fill_opacity=0.28)
        neg = Polygon(right_axes.c2p(0,0), right_axes.c2p(-1,0), right_axes.c2p(-1,1), right_axes.c2p(0,1), color=RED, fill_opacity=0.28)
        left_text = VGroup(
            MathTex(r"\det(A)>0", font_size=31, color=GREEN),
            Text("orientation preserved", font_size=21, color=WHITE),
        ).arrange(np.array([0,-1,0]), buff=0.14).move_to(np.array([-3.4,-2.35,0.0]))
        right_text = VGroup(
            MathTex(r"\det(A)<0", font_size=31, color=RED),
            Text("orientation reversed", font_size=21, color=WHITE),
        ).arrange(np.array([0,-1,0]), buff=0.14).move_to(np.array([3.4,-2.35,0.0]))
        self.play(FadeIn(title), FadeIn(left_axes), FadeIn(right_axes), FadeIn(pos), FadeIn(neg))
        self.play(FadeIn(left_text), FadeIn(right_text))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_singular_collapse(self, banner: Text) -> None:
        title = self.stage_title("If det(A)=0, area collapses")
        plane = NumberPlane(x_range=[-1,4,1], y_range=[-1,3,1], x_length=6.6, y_length=4.0).move_to(np.array([0.0,-0.35,0.0]))
        unit = Polygon(plane.c2p(0,0), plane.c2p(1,0), plane.c2p(1,1), plane.c2p(0,1), color=BLUE, fill_opacity=0.28)
        collapsed = Line(plane.c2p(0,0), plane.c2p(3,3), color=RED, stroke_width=8)
        formula = MathTex(r"\det(A)=0\quad\Longleftrightarrow\quad\text{no area remains}", font_size=29, color=RED)
        formula.move_to(np.array([0.0,-2.45,0.0]))
        self.play(FadeIn(title), FadeIn(plane), FadeIn(unit))
        self.wait(0.6)
        self.play(ReplacementTransform(unit, collapsed))
        self.play(Write(formula))
        self.wait(1.8)
        self.clear_stage((banner,))

    def projected_box(self, center: np.ndarray, sx: float, sy: float, sz: float, color=WHITE) -> VGroup:
        ex = np.array([sx, 0.0, 0.0])
        ey = np.array([0.45*sy, 0.55*sy, 0.0])
        ez = np.array([0.0, 0.75*sz, 0.0])
        pts = [
            center,
            center+ex,
            center+ey,
            center+ex+ey,
            center+ez,
            center+ex+ez,
            center+ey+ez,
            center+ex+ey+ez,
        ]
        edges = [(0,1),(0,2),(1,3),(2,3),(4,5),(4,6),(5,7),(6,7),(0,4),(1,5),(2,6),(3,7)]
        return VGroup(*[Line(pts[i], pts[j], color=color, stroke_width=3) for i,j in edges])

    def show_volume_scale(self, banner: Text) -> None:
        title = self.stage_title("In 3D, determinant magnitude scales volume")
        unit = self.projected_box(np.array([-4.8,-1.35,0.0]), 1.2, 1.2, 1.2, BLUE)
        image = self.projected_box(np.array([0.2,-1.35,0.0]), 2.4, 1.8, 1.2, GREEN)
        left_label = VGroup(Text("unit cube", font_size=22, color=BLUE), MathTex(r"V=1", font_size=25, color=WHITE)).arrange(np.array([0,-1,0]), buff=0.12).move_to(np.array([-3.8,-2.45,0.0]))
        right_label = VGroup(Text("image parallelepiped", font_size=22, color=GREEN), MathTex(r"V=|\det(A)|=3", font_size=25, color=WHITE)).arrange(np.array([0,-1,0]), buff=0.12).move_to(np.array([2.2,-2.45,0.0]))
        arrow = MathTex(r"A", font_size=34, color=YELLOW).move_to(np.array([-0.55,-0.30,0.0]))
        self.play(FadeIn(title), FadeIn(unit), FadeIn(left_label))
        self.play(Write(arrow), FadeIn(image), FadeIn(right_label))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_volume_collapse(self, banner: Text) -> None:
        title = self.stage_title("A singular 3D map flattens volume")
        box = self.projected_box(np.array([-3.9,-1.45,0.0]), 2.0, 1.6, 1.5, BLUE)
        flat = Polygon(np.array([1.0,-1.3,0.0]), np.array([4.0,-1.3,0.0]), np.array([4.8,0.2,0.0]), np.array([1.8,0.2,0.0]), color=RED, fill_opacity=0.25)
        arrow = MathTex(r"A", font_size=34, color=YELLOW).move_to(np.array([-0.55,-0.25,0.0]))
        result = VGroup(
            MathTex(r"\det(A)=0", font_size=34, color=RED),
            Text("volume collapses to zero", font_size=22, color=WHITE),
        ).arrange(np.array([0,-1,0]), buff=0.18).move_to(np.array([3.0,-2.15,0.0]))
        self.play(FadeIn(title), FadeIn(box))
        self.play(Write(arrow), FadeIn(flat), FadeIn(result))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_multiplicativity_geometry(self, banner: Text) -> None:
        title = self.stage_title("Successive volume scalings multiply")
        lines = product_scaling_tex()
        body = VGroup(
            MathTex(lines[0], font_size=28, color=BLUE),
            MathTex(lines[1], font_size=28, color=GREEN),
            MathTex(lines[2], font_size=31, color=YELLOW),
        ).arrange(np.array([0,-1,0]), buff=0.38)
        body.scale_to_fit_width(10.4)
        body.move_to(np.array([0.0,-0.15,0.0]))
        cue = Text("This is the geometric meaning of det(AB)=det(A)det(B).", font_size=21, color=GREY_B)
        cue.move_to(np.array([0.0,-2.35,0.0]))
        self.play(FadeIn(title))
        for line in body:
            self.play(Write(line))
        self.play(FadeIn(cue))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_takeaway(self, banner: Text) -> None:
        title = self.stage_title("The big takeaway", size=29)
        theorem = MathTex(signed_scale_tex(), font_size=43, color=GREEN)
        theorem.scale_to_fit_width(10.5)
        theorem.move_to(np.array([0.0,0.85,0.0]))
        lines = closing_lines()
        notes = VGroup(
            Text(lines[0], font_size=21, color=WHITE),
            Text(lines[1], font_size=21, color=BLUE),
            Text(lines[2], font_size=21, color=GREY_B),
        ).arrange(np.array([0,-1,0]), buff=0.28)
        notes.scale_to_fit_width(10.7)
        notes.move_to(np.array([0.0,-1.15,0.0]))
        self.play(FadeIn(title), Write(theorem))
        for line in notes:
            self.play(FadeIn(line))
        self.wait(2.2)
