"""Manim presentation: Positive Definite Matrices — Finite Elements and Energy."""
from __future__ import annotations

import numpy as np
from manim import (
    Axes, Dot, DOWN, FadeIn, FadeOut, GREEN_C, GREY_B, LEFT, MathTex,
    Matrix, NumberLine, ORANGE, RIGHT, Scene, SurroundingRectangle, TEAL_C,
    Tex, Text, UP, VGroup, VMobject, WHITE, YELLOW,
)

from engine.finite_element_energy import FiniteElementEnergy1D


class FiniteElementEnergyPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "Finite Elements: Turning Energy into a Matrix"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Tex(
            r"\textbf{POSITIVE DEFINITE MATRICES}", font_size=24, color=GREY_B
        ).to_edge(UP, buff=0.16)
        title = Tex(
            r"\textbf{Finite Elements: Turning Energy into a Matrix}",
            font_size=32,
            color=YELLOW,
        ).next_to(banner, DOWN, buff=0.11)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(FadeOut(old), run_time=0.18)
        self.play(FadeIn(new), run_time=0.22)
        return new

    @staticmethod
    def _matrix(entries, scale=0.72, h_buff=0.90, v_buff=0.80):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _compact_entries(matrix, factor=0.78):
        entries = list(matrix.get_entries())
        centers = [entry.get_center().copy() for entry in entries]
        for entry, center in zip(entries, centers):
            entry.scale(factor).move_to(center)
        return entries

    @staticmethod
    def _polyline(axes, x_values, y_values, color, stroke_width=6):
        graph = VMobject(color=color, stroke_width=stroke_width)
        graph.set_points_as_corners(
            [axes.c2p(float(x), float(y)) for x, y in zip(x_values, y_values)]
        )
        return graph

    @staticmethod
    def _recipe_card(number, label, formula, color):
        content = VGroup(
            Text(f"STEP {number}", font_size=21, color=color, weight="BOLD"),
            Text(label, font_size=27, color=WHITE, weight="BOLD"),
            MathTex(formula, font_size=36, color=color),
        ).arrange(DOWN, buff=0.16)
        border = SurroundingRectangle(content, color=color, buff=0.22, stroke_width=2.1)
        return VGroup(border, content)

    def construct(self):
        model = FiniteElementEnergy1D()
        if not np.allclose(model.stiffness_matrix(), [[6, -3], [-3, 6]]):
            raise RuntimeError("unexpected finite-element stiffness matrix")
        if not np.allclose(model.load_vector(), [1 / 3, 1 / 3]):
            raise RuntimeError("unexpected finite-element load vector")
        if not np.allclose(model.solve(), [1 / 9, 1 / 9]):
            raise RuntimeError("unexpected finite-element solution")

        banner, title, heading = self._chrome(
            "How can a differential equation become a positive definite matrix problem?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        problem = VGroup(
            Text("A taut string under a uniform downward load", font_size=31, color=YELLOW, weight="BOLD"),
            VGroup(
                MathTex(r"x", font_size=38, color=TEAL_C),
                Text("position along the string", font_size=27),
                MathTex(r"u(x)", font_size=38, color=ORANGE),
                Text("downward displacement", font_size=27),
            ).arrange(RIGHT, buff=0.28),
            MathTex(r"-u''(x)=1,\qquad 0<x<1", font_size=51, color=WHITE),
            Text("Find the shape of the displaced string.", font_size=29, color=GREEN_C),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.05)
        self.play(FadeIn(problem[0]))
        self.play(FadeIn(problem[1]))
        self.play(FadeIn(problem[2]), FadeIn(problem[3]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The differential equation expresses vertical force balance."
        )
        self.play(FadeOut(problem))
        force_balance = VGroup(
            MathTex(r"-T\,u''(x)=q(x)", font_size=53, color=WHITE),
            VGroup(
                VGroup(
                    MathTex(r"T", font_size=38, color=TEAL_C),
                    Text("string tension", font_size=27),
                ).arrange(RIGHT, buff=0.16),
                VGroup(
                    MathTex(r"q(x)", font_size=38, color=ORANGE),
                    Text("downward load per unit length", font_size=27),
                ).arrange(RIGHT, buff=0.16),
            ).arrange(RIGHT, buff=0.70),
            Text(
                "A positive downward load makes the displacement curve concave down: u″(x) < 0.",
                font_size=28,
                color=GREEN_C,
            ),
            MathTex(
                r"T=1,\quad q(x)=1\quad\Longrightarrow\quad -u''(x)=1",
                font_size=43,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.40).move_to(DOWN * 0.04)
        self.play(FadeIn(force_balance[0]))
        self.play(FadeIn(force_balance[1]))
        self.play(FadeIn(force_balance[2]))
        self.play(FadeIn(force_balance[3]))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "The endpoint values describe two fixed supports."
        )
        self.play(FadeOut(force_balance))
        boundary_conditions = VGroup(
            VGroup(
                MathTex(r"u(0)=0", font_size=47, color=TEAL_C),
                Text("left end fixed at zero displacement", font_size=28),
            ).arrange(RIGHT, buff=0.40),
            VGroup(
                MathTex(r"u(1)=0", font_size=47, color=ORANGE),
                Text("right end fixed at zero displacement", font_size=28),
            ).arrange(RIGHT, buff=0.40),
            Text(
                "These are boundary conditions in space, not initial conditions in time.",
                font_size=29,
                color=YELLOW,
                weight="BOLD",
            ),
            Text(
                "The string may move between the supports, but its endpoints cannot.",
                font_size=28,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.46).move_to(DOWN * 0.04)
        self.play(FadeIn(boundary_conditions[0]))
        self.play(FadeIn(boundary_conditions[1]))
        self.play(FadeIn(boundary_conditions[2]))
        self.play(FadeIn(boundary_conditions[3]))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "The solution is the function that minimizes this energy."
        )
        self.play(FadeOut(boundary_conditions))
        continuous_energy = VGroup(
            MathTex(
                r"J(u)=\frac12\int_0^1\bigl(u'(x)\bigr)^2\,dx"
                r"-\int_0^1u(x)\,dx",
                font_size=48,
                color=WHITE,
            ),
            VGroup(
                Text("elastic energy", font_size=27, color=TEAL_C),
                Text("work done by the load", font_size=27, color=ORANGE),
            ).arrange(RIGHT, buff=1.05),
            Text(
                "Finite elements replace the unknown function by finitely many coefficients.",
                font_size=29,
                color=GREEN_C,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.04)
        self.play(FadeIn(continuous_energy[0]))
        self.play(FadeIn(continuous_energy[1]))
        self.play(FadeIn(continuous_energy[2]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Divide the interval into three finite elements."
        )
        self.play(FadeOut(continuous_energy))
        mesh_line = NumberLine(
            x_range=[0, 1, 1 / 3],
            length=8.2,
            include_numbers=False,
            include_tip=False,
            color=WHITE,
        ).move_to(DOWN * 0.10)
        node_values = [0, 1 / 3, 2 / 3, 1]
        node_labels = ["0", r"\frac13", r"\frac23", "1"]
        dots = VGroup(
            *[Dot(mesh_line.n2p(value), radius=0.085, color=YELLOW) for value in node_values]
        )
        labels = VGroup(
            *[
                MathTex(label, font_size=34).next_to(mesh_line.n2p(value), DOWN, buff=0.24)
                for value, label in zip(node_values, node_labels)
            ]
        )
        elements = VGroup(
            *[
                Text(f"element {index + 1}", font_size=25, color=color).move_to(
                    mesh_line.n2p((index + 0.5) / 3) + UP * 0.55
                )
                for index, color in enumerate((TEAL_C, ORANGE, GREEN_C))
            ]
        )
        mesh_note = Text(
            "The endpoint values are fixed; only the two interior node values are unknown.",
            font_size=28,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(mesh_line), FadeIn(dots), FadeIn(labels))
        self.play(FadeIn(elements), FadeIn(mesh_note))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Each interior node gets one piecewise-linear hat function."
        )
        self.play(FadeOut(mesh_line), FadeOut(dots), FadeOut(labels), FadeOut(elements), FadeOut(mesh_note))
        basis_axes = Axes(
            x_range=[0, 1, 1 / 3],
            y_range=[0, 1.15, 0.5],
            x_length=7.8,
            y_length=3.4,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * 0.25)
        phi_one = self._polyline(basis_axes, [0, 1 / 3, 2 / 3, 1], [0, 1, 0, 0], TEAL_C)
        phi_two = self._polyline(basis_axes, [0, 1 / 3, 2 / 3, 1], [0, 0, 1, 0], ORANGE)
        basis_labels = VGroup(
            MathTex(r"\phi_1", font_size=36, color=TEAL_C).next_to(
                basis_axes.c2p(1 / 3, 1), UP + LEFT, buff=0.08
            ),
            MathTex(r"\phi_2", font_size=36, color=ORANGE).next_to(
                basis_axes.c2p(2 / 3, 1), UP + RIGHT, buff=0.08
            ),
        )
        basis_note = Text(
            "Each hat equals 1 at its own node and 0 at every other node.",
            font_size=28,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(basis_axes))
        self.play(FadeIn(phi_one), FadeIn(basis_labels[0]))
        self.play(FadeIn(phi_two), FadeIn(basis_labels[1]), FadeIn(basis_note))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The approximate solution is determined by two coefficients."
        )
        self.play(FadeOut(basis_axes), FadeOut(phi_one), FadeOut(phi_two), FadeOut(basis_labels), FadeOut(basis_note))
        approximation = VGroup(
            MathTex(r"u_h(x)=c_1\phi_1(x)+c_2\phi_2(x)", font_size=52, color=WHITE),
            MathTex(
                r"c_1=u_h\!\left(\frac13\right),\qquad{}"
                r"c_2=u_h\!\left(\frac23\right)",
                font_size=44,
                color=YELLOW,
            ),
            Text(
                "Choosing a function has become choosing a vector c.",
                font_size=30,
                color=GREEN_C,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.55).move_to(DOWN * 0.05)
        self.play(FadeIn(approximation[0]))
        self.play(FadeIn(approximation[1]))
        self.play(FadeIn(approximation[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Every element contributes the same two-by-two stiffness matrix."
        )
        self.play(FadeOut(approximation))
        local_matrix = self._matrix([["1", "-1"], ["-1", "1"]], scale=0.76)
        local = VGroup(
            MathTex(r"h=\frac13", font_size=43, color=TEAL_C),
            VGroup(
                MathTex(r"K^{(e)}=\frac1h", font_size=43, color=WHITE),
                local_matrix,
                MathTex(r"=3", font_size=43, color=YELLOW),
                self._matrix([["1", "-1"], ["-1", "1"]], scale=0.76),
            ).arrange(RIGHT, buff=0.18),
            Text(
                "Neighboring node values are coupled through their difference.",
                font_size=29,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.04)
        self.play(FadeIn(local[0]))
        self.play(FadeIn(local[1]))
        self.play(FadeIn(local[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Assembly adds overlapping element contributions."
        )
        self.play(FadeOut(local))
        full_k = self._matrix(
            [["3", "-3", "0", "0"], ["-3", "6", "-3", "0"],
             ["0", "-3", "6", "-3"], ["0", "0", "-3", "3"]],
            scale=0.55,
            h_buff=0.88,
            v_buff=0.72,
        )
        reduced_k = self._matrix([["6", "-3"], ["-3", "6"]], scale=0.76)
        assembly = VGroup(
            VGroup(Text("assembled", font_size=25, color=TEAL_C), full_k).arrange(DOWN, buff=0.18),
            MathTex(r"\xrightarrow{\ u(0)=u(1)=0\ }", font_size=38, color=YELLOW),
            VGroup(Text("interior unknowns", font_size=25, color=ORANGE), reduced_k).arrange(DOWN, buff=0.18),
        ).arrange(RIGHT, buff=0.42).move_to(DOWN * 0.02)
        if assembly.width > 11.2:
            assembly.scale_to_fit_width(11.2)
        assembly_note = Text(
            "The reduced 2-by-2 matrix K is positive definite.",
            font_size=28,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(assembly[0]))
        self.play(FadeIn(assembly[1]), FadeIn(assembly[2]))
        self.play(FadeIn(assembly_note))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The load vector comes from the area under each hat."
        )
        self.play(FadeOut(assembly), FadeOut(assembly_note))
        load_vector = self._matrix([[r"\frac13"], [r"\frac13"]], scale=0.82, v_buff=1.05)
        self._compact_entries(load_vector, 0.80)
        load = VGroup(
            MathTex(r"f_i=\int_0^1\phi_i(x)\,dx", font_size=46, color=WHITE),
            MathTex(
                r"\text{area of each hat}=\frac12\left(\frac23\right)(1)=\frac13",
                font_size=41,
                color=YELLOW,
            ),
            VGroup(MathTex(r"f=", font_size=43, color=ORANGE), load_vector).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, buff=0.44).move_to(DOWN * 0.04)
        self.play(FadeIn(load[0]))
        self.play(FadeIn(load[1]))
        self.play(FadeIn(load[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The continuous energy has become a quadratic function of c."
        )
        self.play(FadeOut(load))
        discrete = VGroup(
            MathTex(r"J(c)=\frac12c^TKc-f^Tc", font_size=53, color=WHITE),
            MathTex(
                r"c^TKc=\int_0^1\bigl(u_h'(x)\bigr)^2\,dx>0"
                r"\quad(c\ne0)",
                font_size=43,
                color=TEAL_C,
            ),
            Text(
                "Positive definiteness guarantees one unique minimizer.",
                font_size=30,
                color=GREEN_C,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.52).move_to(DOWN * 0.04)
        self.play(FadeIn(discrete[0]))
        self.play(FadeIn(discrete[1]))
        self.play(FadeIn(discrete[2]))
        self.wait(2.0)

        prediction = Text(
            "Pause: what equation must the minimizing coefficients satisfy?",
            font_size=30,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "At the minimum, the gradient of the discrete energy is zero."
        )
        self.play(FadeOut(discrete))
        system = VGroup(
            MathTex(r"\nabla J(c)=Kc-f=0", font_size=48, color=WHITE),
            MathTex(r"\boxed{Kc=f}", font_size=55, color=YELLOW),
            MathTex(
                r"c_1=c_2=\frac19",
                font_size=48,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.04)
        self.play(FadeIn(system[0]))
        self.play(FadeIn(system[1]))
        self.play(FadeIn(system[2]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The two coefficients determine the piecewise-linear solution."
        )
        self.play(FadeOut(system))
        solution_axes = Axes(
            x_range=[0, 1, 1 / 3],
            y_range=[0, 0.15, 0.05],
            x_length=7.8,
            y_length=3.8,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * 0.25)
        exact_graph = solution_axes.plot(
            lambda x: 0.5 * x * (1 - x), x_range=[0, 1], color=GREY_B, stroke_width=4
        )
        approximate_graph = self._polyline(
            solution_axes,
            model.nodes,
            model.nodal_values(),
            YELLOW,
            stroke_width=7,
        )
        solution_dots = VGroup(
            *[
                Dot(solution_axes.c2p(float(x), float(y)), radius=0.075, color=YELLOW)
                for x, y in zip(model.nodes, model.nodal_values())
            ]
        )
        graph_labels = VGroup(
            Text("exact curve", font_size=25, color=GREY_B).move_to(
                solution_axes.c2p(0.78, 0.137)
            ),
            MathTex(r"u_h", font_size=35, color=YELLOW).move_to(
                solution_axes.c2p(0.50, 0.085)
            ),
        )
        nodal_note = MathTex(
            r"(0,\,\tfrac19,\,\tfrac19,\,0)", font_size=37, color=GREEN_C
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(solution_axes), FadeIn(exact_graph), FadeIn(graph_labels[0]))
        self.play(FadeIn(approximate_graph), FadeIn(solution_dots), FadeIn(graph_labels[1]))
        self.play(FadeIn(nodal_note))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Finite elements turn an energy-minimization problem into linear algebra."
        )
        self.play(
            FadeOut(solution_axes), FadeOut(exact_graph), FadeOut(approximate_graph),
            FadeOut(solution_dots), FadeOut(graph_labels), FadeOut(nodal_note)
        )
        recipe = VGroup(
            self._recipe_card(1, "Mesh", r"0=x_0<\cdots<x_n=1", TEAL_C),
            self._recipe_card(2, "Choose basis", r"u_h=\sum c_i\phi_i", ORANGE),
            self._recipe_card(3, "Assemble", r"K,\ f", YELLOW),
            self._recipe_card(4, "Solve", r"Kc=f", GREEN_C),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.04)
        if recipe.width > 11.4:
            recipe.scale_to_fit_width(11.4)
        conclusion = Text(
            "positive energy  →  positive definite matrix  →  unique approximation",
            font_size=27,
            color=WHITE,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(recipe[0]), FadeIn(recipe[1]))
        self.play(FadeIn(recipe[2]), FadeIn(recipe[3]))
        self.play(FadeIn(conclusion))
        self.wait(2.8)
