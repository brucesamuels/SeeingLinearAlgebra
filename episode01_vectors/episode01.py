from __future__ import annotations

import numpy as np
from manim import *

from common.branding import BrooklynTechTitle
from common.components import GlowArrow, equation_panel
from common.theme import (
    BACKGROUND,
    BLUE_VEC,
    CYAN,
    FAILURE,
    GREEN_VEC,
    GRID,
    MUTED,
    PURPLE,
    RED_VEC,
    SUCCESS,
    TEXT,
    YELLOW,
    apply_theme,
    soft_grid_2d,
)

apply_theme()


class Episode01Vectors(Scene):
    """Seeing Linear Algebra — Episode 1.

    Development follows Mr. Samuels' lesson:
    viewpoints -> equivalent vectors -> scalar multiplication -> addition ->
    magnitude -> unit vectors -> standard basis and coordinates ->
    linear combinations -> span in R, R^2, R^3, and R^n.
    """

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.branded_opening()
        self.three_viewpoints()
        self.equivalent_vectors()
        self.scalar_multiplication()
        self.vector_addition()
        self.magnitude_and_norm()
        self.unit_vectors()
        self.standard_basis_and_coordinates()
        self.linear_combinations()
        self.span_across_dimensions()
        self.closing_bridge()

    def clear_scene(self, *mobjects: Mobject, run_time: float = 0.65) -> None:
        targets = Group(*[m for m in mobjects if m is not None])
        if len(targets):
            self.play(FadeOut(targets), run_time=run_time)

    # ------------------------------------------------------------------
    # Opening and three viewpoints
    # ------------------------------------------------------------------
    def branded_opening(self) -> None:
        grid = soft_grid_2d((-7, 7, 1), (-4, 4, 1)).set_opacity(0.22)
        vector = Arrow(ORIGIN, 2.7 * RIGHT + 1.4 * UP, buff=0, color=BLUE_VEC, stroke_width=7)
        title = BrooklynTechTitle(
            "Episode 1",
            "Vectors",
            "Magnitude, unit vectors, coordinates, and span",
        ).scale(0.88)

        self.play(FadeIn(grid), GrowArrow(vector), run_time=1.1)
        self.play(FadeIn(title, shift=0.15 * UP), run_time=1.0)
        self.wait(1.4)
        self.clear_scene(grid, vector, title)

    def three_viewpoints(self) -> None:
        heading = Text("Three perspectives on a vector", font_size=39, color=TEXT, weight=BOLD).to_edge(UP)

        arrow_icon = Arrow(LEFT * 0.8, RIGHT * 0.8 + UP * 0.45, buff=0, color=BLUE_VEC, stroke_width=7)
        list_icon = MathTex(r"\begin{bmatrix}v_1\\v_2\\\vdots\\v_n\end{bmatrix}", color=CYAN, font_size=46)
        abstract_icon = MathTex(r"\mathbf v\in V", color=PURPLE, font_size=52)

        cards = VGroup(
            self.perspective_card("PHYSICIST", "an arrow", arrow_icon, BLUE_VEC),
            self.perspective_card("COMPUTER SCIENTIST", "an ordered list", list_icon, CYAN),
            self.perspective_card("MATHEMATICIAN", "an abstract object", abstract_icon, PURPLE),
        ).arrange(RIGHT, buff=0.3).scale(0.91).shift(DOWN * 0.25)

        line = Text("Three languages. One mathematical object.", font_size=30, color=MUTED).to_edge(DOWN)
        self.play(Write(heading))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.18) for c in cards], lag_ratio=0.2), run_time=1.8)
        self.play(Write(line))
        self.wait(1.2)
        self.clear_scene(heading, cards, line)

    def perspective_card(self, title: str, body: str, icon: Mobject, color: ManimColor) -> VGroup:
        box = RoundedRectangle(
            width=4.0,
            height=3.25,
            corner_radius=0.16,
            stroke_color=color,
            stroke_opacity=0.8,
            fill_color="#10182A",
            fill_opacity=0.93,
        )
        t = Text(title, font_size=18, color=color, weight=BOLD)
        b = Text(body, font_size=27, color=TEXT)
        icon = icon.copy().scale_to_fit_height(1.25)
        content = VGroup(t, icon, b).arrange(DOWN, buff=0.25)
        content.move_to(box)
        return VGroup(box, content)

    # ------------------------------------------------------------------
    # Equivalent vectors — restored from the first version
    # ------------------------------------------------------------------
    def equivalent_vectors(self) -> None:
        plane = soft_grid_2d()
        heading = Text("Equal vectors: same magnitude and direction", font_size=36, color=TEXT, weight=BOLD).to_edge(UP)
        base = np.array([2.4, 1.6, 0.0])
        starts = [
            np.array([-5.2, 0.8, 0.0]),
            np.array([-1.5, -2.6, 0.0]),
            np.array([1.3, 0.5, 0.0]),
            np.array([3.6, -2.2, 0.0]),
        ]
        arrows = VGroup(*[
            Arrow(s, s + base, buff=0, color=BLUE_VEC, stroke_width=6, max_tip_length_to_length_ratio=0.13)
            for s in starts
        ])
        question = Text("Different locations — different vectors?", font_size=29, color=MUTED).to_edge(DOWN)

        self.play(Create(plane), Write(heading))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.18), FadeIn(question), run_time=1.6)
        self.wait(0.8)

        origin_arrows = VGroup(*[
            Arrow(ORIGIN, base, buff=0, color=BLUE_VEC, stroke_width=6, max_tip_length_to_length_ratio=0.13)
            for _ in arrows
        ])
        self.play(
            *[Transform(a, b) for a, b in zip(arrows, origin_arrows)],
            Transform(question, Text("Position is irrelevant; length and direction determine the vector.", font_size=27, color=CYAN).to_edge(DOWN)),
            run_time=1.7,
        )
        length_tag = Text("same magnitude", font_size=25, color=YELLOW).next_to(base / 2, UP, buff=0.35)
        direction_tag = Text("same direction", font_size=25, color=GREEN_VEC).next_to(base / 2, DOWN, buff=0.35)
        self.play(FadeIn(length_tag), FadeIn(direction_tag))
        self.wait(1.2)
        self.clear_scene(plane, heading, arrows, question, length_tag, direction_tag)

    # ------------------------------------------------------------------
    # Scalar multiplication and addition
    # ------------------------------------------------------------------
    def scalar_multiplication(self) -> None:
        plane = soft_grid_2d()
        heading = Text("Scalar multiplication", font_size=39, color=TEXT, weight=BOLD).to_edge(UP)
        tracker = ValueTracker(1.0)
        base = np.array([2.35, 1.45, 0.0])
        arrow = always_redraw(lambda: Arrow(
            ORIGIN,
            tracker.get_value() * base,
            buff=0,
            color=YELLOW,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.13,
        ))
        formula = always_redraw(lambda: MathTex(
            rf"c\mathbf v,\qquad c={tracker.get_value():.2f}",
            color=YELLOW,
            font_size=38,
        ).to_corner(UR, buff=0.38))
        description = Text("", font_size=28, color=CYAN).to_edge(DOWN)

        self.play(Create(plane), Write(heading))
        self.add(arrow, formula)
        stages = [
            (2.0, "|c|>1 stretches"),
            (0.45, "0<|c|<1 shrinks"),
            (-1.25, "c<0 reverses direction"),
            (0.0, "c=0 collapses to the zero vector"),
        ]
        for value, words in stages:
            new_description = Text(words, font_size=28, color=CYAN).to_edge(DOWN)
            self.play(tracker.animate.set_value(value), Transform(description, new_description), run_time=1.05)
            self.wait(0.45)
        self.clear_scene(plane, heading, arrow, formula, description)

    def vector_addition(self) -> None:
        plane = soft_grid_2d()
        heading = Text("Vector addition", font_size=39, color=TEXT, weight=BOLD).to_edge(UP)
        u = np.array([2.8, 0.9, 0.0])
        v = np.array([1.0, 2.0, 0.0])
        u_arrow = Arrow(ORIGIN, u, buff=0, color=BLUE_VEC, stroke_width=7)
        v_arrow = Arrow(ORIGIN, v, buff=0, color=RED_VEC, stroke_width=7)
        v_shifted = Arrow(u, u + v, buff=0, color=RED_VEC, stroke_width=7)
        result = Arrow(ORIGIN, u + v, buff=0, color=YELLOW, stroke_width=8)
        u_label = MathTex(r"\mathbf u", color=BLUE_VEC, font_size=32).next_to(u, DR)
        v_label = MathTex(r"\mathbf v", color=RED_VEC, font_size=32).next_to(v, UL)
        result_label = MathTex(r"\mathbf u+\mathbf v", color=YELLOW, font_size=34).next_to(u + v, UR)
        operation = MathTex(
            r"\underbrace{\mathbf u}_{\text{first vector}}+"
            r"\underbrace{\mathbf v}_{\text{translate tip-to-tail}}",
            color=TEXT,
            font_size=37,
        ).to_corner(DL, buff=0.35)

        self.play(Create(plane), Write(heading))
        self.play(GrowArrow(u_arrow), FadeIn(u_label), GrowArrow(v_arrow), FadeIn(v_label))
        self.play(TransformFromCopy(v_arrow, v_shifted), run_time=1.0)
        self.play(GrowArrow(result), FadeIn(result_label), Write(operation))
        self.wait(1.2)
        self.clear_scene(plane, heading, u_arrow, v_arrow, v_shifted, result, u_label, v_label, result_label, operation)

    # ------------------------------------------------------------------
    # Magnitude, unit vectors, standard basis, coordinates
    # ------------------------------------------------------------------
    def magnitude_and_norm(self) -> None:
        plane = soft_grid_2d()
        heading = Text("Magnitude: the Euclidean norm", font_size=38, color=TEXT, weight=BOLD).to_edge(UP)
        v = np.array([3.0, -4.0, 0.0])
        arrow = Arrow(ORIGIN, v, buff=0, color=BLUE_VEC, stroke_width=8)
        horizontal = Line(ORIGIN, 3 * RIGHT, color=RED_VEC, stroke_width=5)
        vertical = Line(3 * RIGHT, v, color=GREEN_VEC, stroke_width=5)
        right_angle = RightAngle(horizontal, vertical, length=0.22, color=MUTED)
        labels = VGroup(
            MathTex("3", color=RED_VEC, font_size=32).next_to(horizontal, DOWN),
            MathTex("4", color=GREEN_VEC, font_size=32).next_to(vertical, RIGHT),
            MathTex(r"\|\mathbf v\|", color=YELLOW, font_size=34).next_to(arrow.get_center(), LEFT),
        )
        worked = equation_panel(
            MathTex(r"\mathbf v=\begin{bmatrix}3\\-4\end{bmatrix}", color=TEXT, font_size=39),
            MathTex(r"\|\mathbf v\|=\sqrt{3^2+(-4)^2}=5", color=YELLOW, font_size=36),
            width=5.1,
        ).to_corner(UR, buff=0.38)
        general = MathTex(r"\|\mathbf v\|=\sqrt{v_1^2+v_2^2+\cdots+v_n^2}", color=CYAN, font_size=39).to_edge(DOWN)

        self.play(Create(plane), Write(heading), GrowArrow(arrow))
        self.play(Create(horizontal), Create(vertical), Create(right_angle), FadeIn(labels))
        self.play(FadeIn(worked, shift=LEFT * 0.15))
        self.wait(1.0)
        self.play(Write(general))
        self.wait(1.2)
        self.clear_scene(plane, heading, arrow, horizontal, vertical, right_angle, labels, worked, general)

    def unit_vectors(self) -> None:
        plane = soft_grid_2d()
        heading = Text("Unit vectors: preserve direction, set length to 1", font_size=36, color=TEXT, weight=BOLD).to_edge(UP)
        tracker = ValueTracker(1.0)
        base = np.array([3.0, -4.0, 0.0])
        arrow = always_redraw(lambda: Arrow(
            ORIGIN,
            tracker.get_value() * base,
            buff=0,
            color=BLUE_VEC,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.12,
        ))
        formula = MathTex(
            r"\widehat{\mathbf v}=\frac{\mathbf v}{\|\mathbf v\|}"
            r"=\frac15\begin{bmatrix}3\\-4\end{bmatrix}"
            r"=\begin{bmatrix}3/5\\-4/5\end{bmatrix}",
            color=TEXT,
            font_size=38,
        ).to_corner(UR, buff=0.35)
        length = always_redraw(lambda: MathTex(
            rf"\text{{length}}={5*abs(tracker.get_value()):.2f}",
            color=YELLOW,
            font_size=34,
        ).to_corner(DL, buff=0.4))

        self.play(Create(plane), Write(heading), FadeIn(formula))
        self.add(arrow, length)
        self.wait(0.6)
        self.play(tracker.animate.set_value(0.2), run_time=1.8, rate_func=smooth)
        verified = MathTex(r"\|\widehat{\mathbf v}\|=1", color=SUCCESS, font_size=42).to_edge(DOWN)
        self.play(Write(verified))
        self.wait(1.1)
        self.clear_scene(plane, heading, arrow, formula, length, verified)

    def standard_basis_and_coordinates(self) -> None:
        # Put the title at the upper-left and the formulas at the lower-right,
        # leaving the basis labels completely unobscured.
        plane = soft_grid_2d((-6, 6, 1), (-3.5, 3.5, 1))
        heading = Text("Standard basis vectors", font_size=35, color=TEXT, weight=BOLD).to_corner(UL, buff=0.3)
        e1 = Arrow(ORIGIN, RIGHT, buff=0, color=BLUE_VEC, stroke_width=8)
        e2 = Arrow(ORIGIN, UP, buff=0, color=RED_VEC, stroke_width=8)
        e1_label = MathTex(r"\mathbf e_1", color=BLUE_VEC, font_size=34).next_to(e1.get_end(), DOWN)
        e2_label = MathTex(r"\mathbf e_2", color=RED_VEC, font_size=34).next_to(e2.get_end(), LEFT)
        definitions = equation_panel(
            MathTex(r"\mathbf e_1=\begin{bmatrix}1\\0\end{bmatrix}", color=BLUE_VEC, font_size=35),
            MathTex(r"\mathbf e_2=\begin{bmatrix}0\\1\end{bmatrix}", color=RED_VEC, font_size=35),
            width=3.4,
        ).to_corner(DR, buff=0.32)

        self.play(Create(plane), FadeIn(heading))
        self.play(GrowArrow(e1), FadeIn(e1_label), GrowArrow(e2), FadeIn(e2_label), FadeIn(definitions))
        unit_note = Text("Each is a unit step along one coordinate axis.", font_size=27, color=MUTED).to_edge(DOWN)
        self.play(Write(unit_note))
        self.wait(0.9)

        target = np.array([3.0, 2.0, 0.0])
        three_e1 = Arrow(ORIGIN, 3 * RIGHT, buff=0, color=BLUE_VEC, stroke_width=7)
        two_e2_shifted = Arrow(3 * RIGHT, target, buff=0, color=RED_VEC, stroke_width=7)
        target_arrow = Arrow(ORIGIN, target, buff=0, color=YELLOW, stroke_width=8)
        coordinates = MathTex(
            r"\begin{bmatrix}3\\2\end{bmatrix}=3\mathbf e_1+2\mathbf e_2",
            color=TEXT,
            font_size=42,
        ).to_corner(UR, buff=0.38)
        instructions = Text("Coordinates are instructions: scale the unit steps, then add.", font_size=26, color=CYAN).to_edge(DOWN)

        self.play(FadeOut(unit_note), Transform(e1, three_e1), run_time=1.0)
        self.play(GrowArrow(two_e2_shifted), run_time=0.9)
        self.play(GrowArrow(target_arrow), Write(coordinates), Transform(unit_note, instructions))
        self.wait(1.25)
        self.clear_scene(plane, heading, e1, e2, e1_label, e2_label, definitions, two_e2_shifted, target_arrow, coordinates, unit_note)

    # ------------------------------------------------------------------
    # Linear combinations and span
    # ------------------------------------------------------------------
    def linear_combinations(self) -> None:
        plane = soft_grid_2d()
        heading = Text("Linear combinations", font_size=39, color=TEXT, weight=BOLD).to_edge(UP)
        v = np.array([2.3, 0.7, 0.0])
        w = np.array([-0.7, 1.8, 0.0])
        a, b = 1.4, 1.2
        av = a * v
        bw = b * w
        av_arrow = Arrow(ORIGIN, av, buff=0, color=BLUE_VEC, stroke_width=7)
        bw_arrow = Arrow(ORIGIN, bw, buff=0, color=RED_VEC, stroke_width=7)
        bw_shifted = Arrow(av, av + bw, buff=0, color=RED_VEC, stroke_width=7)
        result = Arrow(ORIGIN, av + bw, buff=0, color=YELLOW, stroke_width=8)

        scale_label = MathTex(r"a\mathbf v", color=BLUE_VEC, font_size=39).next_to(av_arrow.get_center(), DOWN)
        scale_label2 = MathTex(r"b\mathbf w", color=RED_VEC, font_size=39).next_to(bw_arrow.get_center(), LEFT)
        formula = MathTex(
            r"\underbrace{a\mathbf v}_{\text{scalar multiplication}}+"
            r"\underbrace{b\mathbf w}_{\text{scalar multiplication}}"
            r"\quad\xrightarrow{\text{vector addition}}\quad a\mathbf v+b\mathbf w",
            color=TEXT,
            font_size=34,
        ).to_edge(DOWN)

        self.play(Create(plane), Write(heading))
        self.play(GrowArrow(av_arrow), FadeIn(scale_label))
        self.play(GrowArrow(bw_arrow), FadeIn(scale_label2))
        self.play(TransformFromCopy(bw_arrow, bw_shifted))
        self.play(GrowArrow(result), Write(formula))
        self.wait(1.25)
        self.clear_scene(plane, heading, av_arrow, bw_arrow, bw_shifted, result, scale_label, scale_label2, formula)

    def span_across_dimensions(self) -> None:
        # R^1: one nonzero vector gives a line.
        heading = Text("Span: all possible linear combinations", font_size=37, color=TEXT, weight=BOLD).to_edge(UP)
        line = NumberLine(x_range=[-6, 6, 1], length=10, color=GRID, include_numbers=False)
        v = Arrow(ORIGIN, 1.8 * RIGHT, buff=0, color=BLUE_VEC, stroke_width=8)
        formula = MathTex(r"\operatorname{span}\{\mathbf v\}=\{c\mathbf v:c\in\mathbb R\}", color=TEXT, font_size=39).to_edge(DOWN)
        dots = VGroup(*[Dot(c * 0.9 * RIGHT, radius=0.045, color=BLUE_VEC) for c in range(-6, 7)])

        self.play(Write(heading), Create(line), GrowArrow(v))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), Write(formula), run_time=1.4)
        badge = self.dimension_badge("one independent direction", "a line", 1)
        self.play(FadeIn(badge))
        self.wait(0.8)
        self.clear_scene(line, v, dots, formula, badge)

        # R^2: show scalar multiples first, then addition sweeps a lattice/plane.
        plane = soft_grid_2d()
        v2 = np.array([1.7, 0.5, 0.0])
        w2 = np.array([-0.4, 1.5, 0.0])
        v_arrow = Arrow(ORIGIN, v2, buff=0, color=BLUE_VEC, stroke_width=7)
        w_arrow = Arrow(ORIGIN, w2, buff=0, color=RED_VEC, stroke_width=7)
        scalar_lines = VGroup(
            Line(-4 * v2, 4 * v2, color=BLUE_VEC, stroke_width=4).set_opacity(0.7),
            Line(-4 * w2, 4 * w2, color=RED_VEC, stroke_width=4).set_opacity(0.7),
        )
        lattice = VGroup(*[
            Dot(i * v2 + j * w2, radius=0.035, color=CYAN)
            for i in np.linspace(-3, 3, 13)
            for j in np.linspace(-2, 2, 9)
            if abs((i * v2 + j * w2)[0]) < 6.6 and abs((i * v2 + j * w2)[1]) < 3.6
        ])
        plane_formula = MathTex(r"a\mathbf v+b\mathbf w", color=YELLOW, font_size=46).to_edge(DOWN)
        badge2 = self.dimension_badge("two independent directions", r"the plane $\mathbb R^2$", 2)

        self.play(Create(plane), GrowArrow(v_arrow), GrowArrow(w_arrow))
        self.play(Create(scalar_lines), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p) for p in lattice], lag_ratio=0.002), Write(plane_formula), run_time=2.0)
        self.play(FadeIn(badge2))
        self.wait(0.9)
        self.clear_scene(plane, v_arrow, w_arrow, scalar_lines, lattice, plane_formula, badge2)

        # R^3: rotate a plane and add a third independent direction.
        self.play(Transform(heading, Text("The same idea continues in higher dimensions", font_size=37, color=TEXT, weight=BOLD).to_edge(UP)))
        axes = ThreeDAxes(
            x_range=(-4, 4, 1), y_range=(-4, 4, 1), z_range=(-3, 3, 1),
            x_length=7.0, y_length=7.0, z_length=5.0,
            axis_config={"color": GRID, "stroke_opacity": 0.75},
        )
        # In a regular Scene, project a 3D-looking plane and three vectors for robust rendering.
        plane_poly = Polygon(
            np.array([-3.3, -1.7, 0]), np.array([1.5, -2.5, 0]),
            np.array([3.3, 1.7, 0]), np.array([-1.5, 2.5, 0]),
            fill_color=PURPLE, fill_opacity=0.22, stroke_color=PURPLE, stroke_opacity=0.6,
        )
        r3_vectors = VGroup(
            Arrow(ORIGIN, 2.1 * RIGHT + 0.5 * UP, buff=0, color=BLUE_VEC, stroke_width=7),
            Arrow(ORIGIN, -0.6 * RIGHT + 1.9 * UP, buff=0, color=RED_VEC, stroke_width=7),
            Arrow(ORIGIN, 0.45 * RIGHT + 2.5 * UP, buff=0, color=GREEN_VEC, stroke_width=7),
        )
        depth_hint = VGroup(*[
            Line(np.array([-3.2 + k * 0.5, -1.8, 0]), np.array([-1.6 + k * 0.5, 2.4, 0]), color=GRID, stroke_opacity=0.35)
            for k in range(10)
        ])
        r3_formula = MathTex(r"a\mathbf v+b\mathbf w+c\mathbf u", color=YELLOW, font_size=45).to_edge(DOWN)
        badge3 = self.dimension_badge("three independent directions", r"space $\mathbb R^3$", 3)
        self.play(FadeIn(axes), FadeIn(plane_poly), FadeIn(depth_hint), LaggedStart(*[GrowArrow(a) for a in r3_vectors], lag_ratio=0.25))
        self.play(Write(r3_formula), FadeIn(badge3))
        self.wait(1.0)
        self.clear_scene(axes, plane_poly, depth_hint, r3_vectors, r3_formula, badge3)

        # R^n: algebra replaces impossible visualization.
        chain = VGroup(
            MathTex(r"c_1\mathbf v_1", color=BLUE_VEC, font_size=40),
            MathTex(r"c_1\mathbf v_1+c_2\mathbf v_2", color=CYAN, font_size=40),
            MathTex(r"c_1\mathbf v_1+c_2\mathbf v_2+c_3\mathbf v_3", color=PURPLE, font_size=40),
            MathTex(r"c_1\mathbf v_1+\cdots+c_n\mathbf v_n", color=YELLOW, font_size=46),
        ).arrange(DOWN, buff=0.3)
        rn = MathTex(r"\mathbb R^1\to\mathbb R^2\to\mathbb R^3\to\mathbb R^n", color=TEXT, font_size=44).to_edge(DOWN)
        self.play(LaggedStart(*[Write(x) for x in chain], lag_ratio=0.35), run_time=2.2)
        self.play(Write(rn))
        self.wait(1.35)
        self.clear_scene(heading, chain, rn)

    def dimension_badge(self, top: str, bottom: str, number: int) -> VGroup:
        box = RoundedRectangle(width=3.25, height=1.55, corner_radius=0.14, stroke_color=PURPLE, fill_color="#111A2D", fill_opacity=0.9)
        n = Integer(number, font_size=45, color=YELLOW)
        t = Text(top, font_size=17, color=MUTED)
        b = Text(bottom.replace("$", ""), font_size=22, color=TEXT)
        content = VGroup(t, n, b).arrange(DOWN, buff=0.04).move_to(box)
        return VGroup(box, content).to_corner(UR, buff=0.3)

    # ------------------------------------------------------------------
    # Close with a bridge to Episode 2
    # ------------------------------------------------------------------
    def closing_bridge(self) -> None:
        title = Text("Scalar multiplication + vector addition", font_size=40, color=TEXT, weight=BOLD)
        arrow1 = MathTex(r"\Downarrow", color=MUTED, font_size=42)
        lc = Text("linear combinations", font_size=44, color=CYAN, weight=BOLD)
        arrow2 = MathTex(r"\Downarrow", color=MUTED, font_size=42)
        span = Text("span", font_size=50, color=YELLOW, weight=BOLD)
        chain = VGroup(title, arrow1, lc, arrow2, span).arrange(DOWN, buff=0.18)
        next_line = Text("Next: What makes a span a subspace?", font_size=27, color=MUTED).to_edge(DOWN)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.12) for x in chain], lag_ratio=0.25), run_time=2.0)
        self.play(FadeIn(next_line))
        self.wait(1.4)
        self.clear_scene(chain, next_line)
