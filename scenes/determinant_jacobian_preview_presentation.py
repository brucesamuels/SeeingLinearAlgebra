"""CP146 presentation: determinants and the Jacobian as local area scaling."""
from __future__ import annotations

import numpy as np
from manim import (
    Arc, BLUE, FadeIn, FadeOut, GREEN, GREY_B, Line, MathTex, NumberPlane,
    MoveToTarget, Polygon, RED, ReplacementTransform, Scene, Text, VGroup, WHITE, YELLOW, Write,
)

from engine.determinant_jacobian_preview import (
    closing_lines,
    jacobian_matrix_tex,
    linear_area_tex,
    linear_example_tex,
    local_area_tex,
    polar_area_tex,
    polar_jacobian_tex,
)


class DeterminantJacobianPreviewPresentation(Scene):
    """Preview the Jacobian determinant as a local area-scale factor."""

    def construct(self) -> None:
        banner = Text("Determinants and Change of Variables", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.22)
        subtitle = Text("A preview of the Jacobian", font_size=26, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.10)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_linear_scaling(banner)
        self.show_local_linearization(banner)
        self.show_jacobian_matrix(banner)
        self.show_linear_example(banner)
        self.show_polar_coordinates(banner)
        self.show_takeaway(banner)

    def stage_title(self, text: str, size: int = 27) -> Text:
        title = Text(text, font_size=size, color=YELLOW)
        title.move_to(np.array([0.0, 2.30, 0.0]))
        return title

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])

    def show_linear_scaling(self, banner: Text) -> None:
        title = self.stage_title("A linear map has one global area scale")
        left = NumberPlane(x_range=[-1, 3, 1], y_range=[-1, 3, 1], x_length=4.3, y_length=3.7)
        left.move_to(np.array([-3.5, -0.35, 0.0]))
        right = NumberPlane(x_range=[-1, 4, 1], y_range=[-1, 3, 1], x_length=4.6, y_length=3.7)
        right.move_to(np.array([3.4, -0.35, 0.0]))

        unit = Polygon(left.c2p(0,0), left.c2p(1,0), left.c2p(1,1), left.c2p(0,1), color=BLUE, fill_opacity=0.30)
        image = Polygon(right.c2p(0,0), right.c2p(2,0), right.c2p(3,1), right.c2p(1,1), color=GREEN, fill_opacity=0.30)
        arrow = MathTex(r"A", font_size=34, color=YELLOW).move_to(np.array([0.0, -0.20, 0.0]))
        formula = MathTex(linear_area_tex(), font_size=25, color=WHITE)
        formula.scale_to_fit_width(9.7)
        formula.move_to(np.array([0.0, -2.50, 0.0]))

        self.play(FadeIn(title), FadeIn(left), FadeIn(right), FadeIn(unit))
        self.play(Write(arrow), FadeIn(image))
        self.play(Write(formula))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_local_linearization(self, banner: Text) -> None:
        title = self.stage_title("A nonlinear map changes its scale from place to place", size=25)
        left = NumberPlane(x_range=[-4,4,1], y_range=[-3,3,1], x_length=4.7, y_length=4.1)
        left.move_to(np.array([-3.2, -0.20, 0.0]))
        patches = VGroup(
            Polygon(left.c2p(-2.8,-1.0), left.c2p(-1.9,-1.0), left.c2p(-1.7,-0.1), left.c2p(-2.6,-0.1), color=BLUE, fill_opacity=0.25),
            Polygon(left.c2p(-0.5,-0.8), left.c2p(0.6,-0.6), left.c2p(0.9,0.3), left.c2p(-0.2,0.1), color=GREEN, fill_opacity=0.25),
            Polygon(left.c2p(1.7,-0.5), left.c2p(3.0,-0.1), left.c2p(3.3,1.0), left.c2p(2.0,0.6), color=RED, fill_opacity=0.22),
        )
        focus = Polygon(
            left.c2p(-0.28,-0.16),
            left.c2p(0.18,-0.06),
            left.c2p(0.30,0.28),
            left.c2p(-0.16,0.18),
            color=YELLOW,
            fill_opacity=0.28,
        )
        zoom_label = Text("zoom in on one tiny patch", font_size=18, color=YELLOW)
        zoom_label.move_to(np.array([0.0, 0.92, 0.0]))

        right = NumberPlane(x_range=[-1,3,1], y_range=[-1,3,1], x_length=4.6, y_length=4.1)
        right.move_to(np.array([3.2, -0.20, 0.0]))
        nonlinear_patch = Polygon(
            right.c2p(0.20,0.30),
            right.c2p(1.18,0.45),
            right.c2p(1.38,1.48),
            right.c2p(0.08,1.15),
            color=BLUE,
            fill_opacity=0.20,
        )
        linear_patch = Polygon(
            right.c2p(0.20,0.30),
            right.c2p(1.20,0.35),
            right.c2p(1.35,1.35),
            right.c2p(0.35,1.30),
            color=GREEN,
            fill_opacity=0.16,
        )

        actual_label = Text("blue: actual nonlinear image", font_size=17, color=BLUE)
        actual_label.move_to(np.array([3.2, 1.73, 0.0]))
        approx_label = Text("green: Jacobian (linear) approximation", font_size=17, color=GREEN)
        approx_label.move_to(np.array([3.2, 1.38, 0.0]))

        left_caption = Text("different patches scale differently", font_size=18, color=WHITE)
        left_caption.move_to(np.array([-3.2, -2.15, 0.0]))
        right_caption = VGroup(
            Text("magnify a sufficiently small patch:", font_size=18, color=WHITE),
            Text("the nonlinear image and its linear approximation nearly agree", font_size=17, color=GREY_B),
        ).arrange(np.array([0,-1,0]), buff=0.12)
        right_caption.scale_to_fit_width(5.5)
        right_caption.move_to(np.array([3.2, -2.12, 0.0]))

        zoom_patch = focus.copy()
        zoom_patch.set_fill(YELLOW, opacity=0.18)
        zoom_patch.set_stroke(YELLOW, width=2.0)
        zoom_patch.generate_target()
        zoom_patch.target.scale(3.6)
        zoom_patch.target.move_to(np.array([3.2,-0.15,0.0]))

        apply_label = Text("apply the nonlinear map", font_size=18, color=BLUE)
        apply_label.move_to(np.array([3.2,1.02,0.0]))

        self.play(FadeIn(title), FadeIn(left), FadeIn(patches), FadeIn(left_caption))
        self.play(FadeIn(focus), FadeIn(zoom_label))
        self.add(zoom_patch)
        self.play(MoveToTarget(zoom_patch), run_time=1.4)
        self.play(FadeIn(right))
        self.play(FadeIn(apply_label))
        self.play(ReplacementTransform(zoom_patch, nonlinear_patch), run_time=1.2)
        self.play(FadeOut(apply_label), FadeIn(actual_label))
        self.play(FadeIn(linear_patch), FadeIn(approx_label), run_time=1.0)
        self.play(FadeIn(right_caption))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_jacobian_matrix(self, banner: Text) -> None:
        title = self.stage_title("The Jacobian is the local linear map")
        intro = MathTex(r"F(u,v)=(x(u,v),\,y(u,v))", font_size=34, color=WHITE)
        intro.move_to(np.array([0.0, 1.28, 0.0]))
        jac = MathTex(jacobian_matrix_tex(), font_size=36, color=BLUE)
        jac.move_to(np.array([0.0, 0.10, 0.0]))
        local = MathTex(local_area_tex(), font_size=38, color=GREEN)
        local.move_to(np.array([0.0, -1.55, 0.0]))
        note = Text("Its determinant tells the local area scale.", font_size=21, color=GREY_B)
        note.move_to(np.array([0.0, -2.60, 0.0]))
        self.play(FadeIn(title), Write(intro))
        self.play(Write(jac))
        self.play(Write(local), FadeIn(note))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_linear_example(self, banner: Text) -> None:
        title = self.stage_title("A linear example: the Jacobian is constant")
        lines = linear_example_tex()
        formulas = VGroup(
            MathTex(lines[0], font_size=28, color=WHITE),
            MathTex(lines[1], font_size=29, color=BLUE),
            MathTex(lines[2], font_size=34, color=GREEN),
        ).arrange(np.array([0,-1,0]), buff=0.30)
        formulas.move_to(np.array([3.25, -0.10, 0.0]))
        formulas.scale_to_fit_width(5.5)

        plane = NumberPlane(x_range=[-1,4,1], y_range=[-1,5,1], x_length=5.0, y_length=4.6)
        plane.move_to(np.array([-3.25,-0.30,0.0]))
        para = Polygon(plane.c2p(0,0), plane.c2p(2,1), plane.c2p(2,4), plane.c2p(0,3), color=GREEN, fill_opacity=0.30)
        area = MathTex(r"\text{area}=6", font_size=28, color=GREEN)
        area.move_to(np.array([-3.25,-2.45,0.0]))

        self.play(FadeIn(title), FadeIn(plane), FadeIn(para), FadeIn(area))
        for line in formulas:
            self.play(Write(line))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_polar_coordinates(self, banner: Text) -> None:
        title = self.stage_title("Polar coordinates give a nonlinear change of variables", size=22)
        title.move_to(np.array([0.0, 2.70, 0.0]))
        lines = polar_jacobian_tex()
        formulas = VGroup(
            MathTex(lines[0], font_size=28, color=WHITE),
            MathTex(lines[1], font_size=28, color=BLUE),
            MathTex(lines[2], font_size=38, color=GREEN),
        ).arrange(np.array([0,-1,0]), buff=0.56)
        formulas.scale_to_fit_width(8.8)
        formulas.move_to(np.array([0.0,-0.60,0.0]))
        formulas[0].shift(np.array([0.0,-0.12,0.0]))
        formulas[2].shift(np.array([0.0,0.12,0.0]))
        self.play(FadeIn(title))
        for line in formulas:
            self.play(Write(line))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_takeaway(self, banner: Text) -> None:
        title = self.stage_title("The big takeaway", size=29)
        theorem = MathTex(r"|\det J|=\text{local area scale factor}", font_size=44, color=GREEN)
        theorem.scale_to_fit_width(10.4)
        theorem.move_to(np.array([0.0,0.82,0.0]))
        lines = closing_lines()
        notes = VGroup(
            Text(lines[0], font_size=20, color=WHITE),
            Text(lines[1], font_size=20, color=BLUE),
            Text(lines[2], font_size=20, color=GREY_B),
        ).arrange(np.array([0,-1,0]), buff=0.25)
        notes.scale_to_fit_width(10.7)
        notes.move_to(np.array([0.0,-1.15,0.0]))
        self.play(FadeIn(title), Write(theorem))
        for line in notes:
            self.play(FadeIn(line))
        self.wait(2.2)
