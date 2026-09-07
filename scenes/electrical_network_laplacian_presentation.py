"""Manim presentation: electrical networks as Laplacian systems."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    BLACK,
    DOWN,
    Dot,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    LEFT,
    Line,
    MathTex,
    Matrix,
    ORANGE,
    RIGHT,
    Scene,
    ShowPassingFlash,
    SurroundingRectangle,
    TEAL_C,
    Tex,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.electrical_network_laplacian import ElectricalNetworkLaplacian


class ElectricalNetworkLaplacianPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Electrical Networks and Laplacian Systems"

    POSITIONS = {
        1: LEFT * 2.15 + UP * 1.15,
        2: LEFT * 2.15 + DOWN * 1.15,
        3: RIGHT * 0.10,
        4: RIGHT * 2.75,
    }

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Tex(
            r"\textbf{GRAPHS, NETWORKS, AND THE LAPLACIAN}",
            font_size=23,
            color=GREY_B,
        ).to_edge(UP, buff=0.16)
        title = Tex(
            r"\textbf{Electrical Networks and Laplacian Systems}",
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

    @classmethod
    def _graph(cls, shift=DOWN * 0.12):
        positions = {vertex: point + shift for vertex, point in cls.POSITIONS.items()}
        edge_order = ((1, 2), (2, 3), (1, 3), (3, 4))
        edges = {
            edge: Line(
                positions[edge[0]], positions[edge[1]], color=GREY_B, stroke_width=4.0
            ).set_z_index(0)
            for edge in edge_order
        }
        dots = {
            vertex: Dot(positions[vertex], radius=0.17, color=YELLOW).set_z_index(2)
            for vertex in (1, 2, 3, 4)
        }
        labels = {
            vertex: MathTex(str(vertex), font_size=29, color=BLACK)
            .move_to(positions[vertex])
            .set_z_index(3)
            for vertex in (1, 2, 3, 4)
        }
        return VGroup(*edges.values(), *dots.values(), *labels.values()), positions, edges, dots, labels

    @staticmethod
    def _matrix(entries, scale=0.67, h_buff=0.78, v_buff=0.67):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _card(label, statement, note, color, width=4.15):
        content = VGroup(
            Text(label, font_size=22, color=color, weight="BOLD"),
            MathTex(statement, font_size=35, color=WHITE),
            Text(note, font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.15)
        if content.width > width - 0.34:
            content.scale_to_fit_width(width - 0.34)
        border = SurroundingRectangle(content, color=color, buff=0.19, stroke_width=2.0)
        return VGroup(border, content)

    @staticmethod
    def _flow_arrow(start, end, color=ORANGE, buff=0.24):
        return Arrow(
            start,
            end,
            buff=buff,
            color=color,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.16,
        ).set_z_index(1)

    def construct(self):
        model = ElectricalNetworkLaplacian()
        voltage = model.solve_source_sink(4, 1)
        injections = model.source_sink_injections(4, 1)
        if not np.allclose(voltage, [0, 1 / 3, 2 / 3, 5 / 3]):
            raise RuntimeError("unexpected electrical potentials")
        if not model.is_kirchhoff_solution(voltage, injections):
            raise RuntimeError("unexpected Kirchhoff solution")
        if not np.allclose(model.energy_balance(voltage, injections), [5 / 3] * 3):
            raise RuntimeError("unexpected electrical energy balance")
        if not np.isclose(model.effective_resistance(4, 1), 5 / 3):
            raise RuntimeError("unexpected effective resistance")

        banner, title, heading = self._chrome(
            "Turn every edge into a unit resistor and assign a potential to every vertex."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: introduce potentials, current, and unit resistors visually.
        graph, positions, edges, _, _ = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        resistance_labels = VGroup(
            *[
                MathTex(r"R=1", font_size=21, color=GREY_B).move_to(
                    (positions[first] + positions[second]) / 2 + offset
                )
                for (first, second), offset in zip(
                    edges,
                    (LEFT * 0.47, DOWN * 0.34, UP * 0.34, UP * 0.32),
                )
            ]
        )
        vocabulary = VGroup(
            self._card("POTENTIAL", r"v_i", "a number assigned to vertex i", TEAL_C, width=4.80),
            self._card("CURRENT", r"I_{i\to j}", "flow along an edge", ORANGE, width=4.80),
            Text("Only potential differences drive current.", font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.36).to_edge(RIGHT, buff=0.41).shift(DOWN * 0.01)
        self.play(FadeIn(graph), FadeIn(resistance_labels))
        self.play(FadeIn(vocabulary))
        self.wait(3.0)

        # Card 2: state Ohm's law first on one edge.
        heading = self._replace_heading(
            heading, "Ohm's law turns a potential difference into edge current."
        )
        self.play(FadeOut(graph), FadeOut(resistance_labels), FadeOut(vocabulary))
        left_point = LEFT * 2.55 + DOWN * 0.10
        right_point = RIGHT * 2.55 + DOWN * 0.10
        edge = Line(left_point, right_point, color=GREY_B, stroke_width=5)
        left_dot = Dot(left_point, radius=0.19, color=TEAL_C)
        right_dot = Dot(right_point, radius=0.19, color=ORANGE)
        endpoints = VGroup(
            MathTex(r"v_3=\frac23", font_size=32, color=TEAL_C).next_to(left_dot, UP, buff=0.30),
            MathTex(r"v_4=\frac53", font_size=32, color=ORANGE).next_to(right_dot, UP, buff=0.30),
            MathTex(r"R=1", font_size=27, color=GREY_B).next_to(edge, DOWN, buff=0.26),
        )
        arrow = self._flow_arrow(right_point, left_point, color=ORANGE, buff=0.26)
        law = VGroup(
            MathTex(r"I_{4\to3}=\frac{v_4-v_3}{R}", font_size=42, color=WHITE),
            MathTex(r"=\frac{5/3-2/3}{1}=1", font_size=42, color=GREEN_C),
            Text("Current flows from higher potential to lower potential.", font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.34).to_edge(DOWN, buff=0.65)
        self.play(FadeIn(edge), FadeIn(left_dot), FadeIn(right_dot), FadeIn(endpoints))
        self.play(FadeIn(arrow), ShowPassingFlash(edge.copy().set_color(ORANGE).set_stroke(width=10)))
        self.play(FadeIn(law))
        self.wait(3.1)

        # Card 3: impose current conservation at an interior vertex.
        heading = self._replace_heading(
            heading, "At an interior vertex, current entering must equal current leaving."
        )
        self.play(FadeOut(edge), FadeOut(left_dot), FadeOut(right_dot), FadeOut(endpoints), FadeOut(arrow), FadeOut(law))
        graph, positions, _, dots, _ = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        arrows = VGroup(
            self._flow_arrow(positions[4], positions[3], color=ORANGE),
            self._flow_arrow(positions[3], positions[1], color=TEAL_C),
            self._flow_arrow(positions[3], positions[2], color=TEAL_C),
        )
        current_labels = VGroup(
            MathTex(r"1", font_size=26, color=ORANGE).move_to((positions[4] + positions[3]) / 2 + UP * 0.31),
            MathTex(r"\frac23", font_size=27, color=TEAL_C).move_to((positions[3] + positions[1]) / 2 + UP * 0.35),
            MathTex(r"\frac13", font_size=27, color=TEAL_C).move_to((positions[3] + positions[2]) / 2 + DOWN * 0.38),
        )
        conservation = VGroup(
            self._card("CURRENT CONSERVATION", r"1=\frac23+\frac13", "nothing accumulates at vertex 3", TEAL_C, width=4.85),
            MathTex(r"\sum_{j\sim i}(v_i-v_j)=b_i", font_size=40, color=WHITE),
            Text("bᵢ is externally injected current; here b₃ = 0.", font_size=23, color=YELLOW),
        ).arrange(DOWN, buff=0.37).to_edge(RIGHT, buff=0.37).shift(DOWN * 0.01)
        self.play(FadeIn(graph), dots[3].animate.set_color(GREEN_C))
        for flow, label in zip(arrows, current_labels):
            self.play(FadeIn(flow), FadeIn(label), run_time=0.55)
        self.play(FadeIn(conservation))
        self.wait(3.1)

        # Card 4: assemble the four conservation equations as Lv=b.
        heading = self._replace_heading(
            heading, "The Laplacian collects all four current-conservation equations at once."
        )
        self.play(FadeOut(graph), FadeOut(arrows), FadeOut(current_labels), FadeOut(conservation))
        laplacian = self._matrix(
            [["2", "-1", "-1", "0"], ["-1", "2", "-1", "0"], ["-1", "-1", "3", "-1"], ["0", "0", "-1", "1"]],
            scale=0.48,
            h_buff=0.72,
            v_buff=0.62,
        )
        potentials = self._matrix([["v_1"], ["v_2"], ["v_3"], ["v_4"]], scale=0.55, v_buff=0.68)
        injection = self._matrix([["-1"], ["0"], ["0"], ["1"]], scale=0.55, v_buff=0.68)
        system = VGroup(
            laplacian,
            potentials,
            MathTex(r"=", font_size=39, color=WHITE),
            injection,
        ).arrange(RIGHT, buff=0.17).move_to(UP * 0.30)
        labels_system = VGroup(
            MathTex(r"L", font_size=33, color=YELLOW).next_to(laplacian, DOWN, buff=0.15),
            MathTex(r"\mathbf v", font_size=33, color=TEAL_C).next_to(potentials, DOWN, buff=0.15),
            MathTex(r"\mathbf b", font_size=33, color=ORANGE).next_to(injection, DOWN, buff=0.15),
        )
        compatibility = VGroup(
            MathTex(r"\mathbf 1^T\mathbf b=-1+0+0+1=0", font_size=38, color=GREEN_C),
            Text("total current injected = total current removed", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.66)
        self.play(FadeIn(system), FadeIn(labels_system))
        self.play(FadeIn(compatibility))
        self.wait(3.2)

        # Card 5: explain singularity as gauge freedom, then choose a reference.
        heading = self._replace_heading(
            heading, "Only potential differences matter, so one reference potential must be chosen."
        )
        self.play(FadeOut(system), FadeOut(labels_system), FadeOut(compatibility))
        gauge = VGroup(
            MathTex(r"\mathbf v=\left(0,\frac13,\frac23,\frac53\right)^T", font_size=42, color=TEAL_C),
            MathTex(
                r"\mathbf v+c\mathbf 1="
                r"\left(c,\frac13+c,\frac23+c,\frac53+c\right)^T",
                font_size=40,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.55).move_to(UP * 0.32)
        gauge_notes = VGroup(
            Text("Adding the same constant changes no edge difference and no current.", font_size=24, color=WHITE),
            MathTex(r"\text{choose ground:}\qquad v_1=0", font_size=40, color=GREEN_C),
        ).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=0.68)
        self.play(FadeIn(gauge[0]))
        self.play(FadeIn(gauge[1]), FadeIn(gauge_notes[0]))
        self.play(FadeIn(gauge_notes[1]))
        self.wait(3.2)

        # Card 6: solve the grounded reduced system exactly.
        heading = self._replace_heading(
            heading, "Ground vertex 1, then solve the remaining nonsingular system."
        )
        self.play(FadeOut(gauge), FadeOut(gauge_notes))
        reduced = self._matrix(
            [["2", "-1", "0"], ["-1", "3", "-1"], ["0", "-1", "1"]],
            scale=0.59,
            h_buff=0.76,
            v_buff=0.68,
        )
        unknowns = self._matrix([["v_2"], ["v_3"], ["v_4"]], scale=0.59, v_buff=0.72)
        rhs = self._matrix([["0"], ["0"], ["1"]], scale=0.59, v_buff=0.72)
        reduced_system = VGroup(reduced, unknowns, MathTex(r"=", font_size=38), rhs).arrange(RIGHT, buff=0.17).move_to(UP * 0.62)
        solution = MathTex(
            r"\mathbf v=\left(0,\frac13,\frac23,\frac53\right)^T",
            font_size=43,
            color=YELLOW,
        ).move_to(DOWN * 1.03)
        solution_note = Text("The source at vertex 4 has the highest potential.", font_size=24, color=ORANGE).to_edge(DOWN, buff=0.66)
        self.play(FadeIn(reduced_system))
        self.play(FadeIn(solution))
        self.play(FadeIn(solution_note))
        self.wait(3.2)

        # Card 7: animate the exact currents through the solved network.
        heading = self._replace_heading(
            heading, "One unit enters at vertex 4, splits through the triangle, and leaves at vertex 1."
        )
        self.play(FadeOut(reduced_system), FadeOut(solution), FadeOut(solution_note))
        graph, positions, _, dots, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        potential_labels = VGroup(
            MathTex(r"0", font_size=27, color=TEAL_C).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"\frac13", font_size=27, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"\frac23", font_size=27, color=GREEN_C).next_to(labels[3], UP, buff=0.24),
            MathTex(r"\frac53", font_size=27, color=ORANGE).next_to(labels[4], RIGHT, buff=0.21),
        )
        flows = VGroup(
            self._flow_arrow(positions[4], positions[3], color=ORANGE),
            self._flow_arrow(positions[3], positions[1], color=GREEN_C),
            self._flow_arrow(positions[3], positions[2], color=TEAL_C),
            self._flow_arrow(positions[2], positions[1], color=TEAL_C),
        )
        flow_labels = VGroup(
            MathTex(r"1", font_size=26, color=ORANGE).move_to((positions[4] + positions[3]) / 2 + UP * 0.31),
            MathTex(r"\frac23", font_size=26, color=GREEN_C).move_to((positions[3] + positions[1]) / 2 + UP * 0.36),
            MathTex(r"\frac13", font_size=26, color=TEAL_C).move_to((positions[3] + positions[2]) / 2 + DOWN * 0.38),
            MathTex(r"\frac13", font_size=26, color=TEAL_C).move_to((positions[2] + positions[1]) / 2 + LEFT * 0.43),
        )
        flow_panel = VGroup(
            self._card("SOURCE", r"b_4=+1", "inject one unit", ORANGE, width=4.60),
            self._card("INTERIOR BALANCE", r"1=\frac23+\frac13", "at vertex 3", GREEN_C, width=4.60),
            self._card("SINK", r"b_1=-1", "remove one unit", TEAL_C, width=4.60),
        ).arrange(DOWN, buff=0.27).to_edge(RIGHT, buff=0.49).shift(DOWN * 0.01)
        self.play(FadeIn(graph), FadeIn(potential_labels), dots[4].animate.set_color(ORANGE), dots[1].animate.set_color(TEAL_C))
        for flow, label in zip(flows, flow_labels):
            self.play(FadeIn(flow), FadeIn(label), run_time=0.52)
        self.play(FadeIn(flow_panel))
        self.wait(3.2)

        # Card 8: connect power, Laplacian energy, and effective resistance.
        heading = self._replace_heading(
            heading, "The Laplacian energy is also the power dissipated by the resistors."
        )
        self.play(FadeOut(graph), FadeOut(potential_labels), FadeOut(flows), FadeOut(flow_labels), FadeOut(flow_panel))
        power = VGroup(
            MathTex(r"\sum_{\text{edges}} I^2R=1^2+\left(\frac23\right)^2+\left(\frac13\right)^2+\left(\frac13\right)^2=\frac53", font_size=38, color=WHITE),
            MathTex(r"\mathbf v^TL\mathbf v=\mathbf b^T\mathbf v=\frac53", font_size=43, color=GREEN_C),
            self._card("EFFECTIVE RESISTANCE", r"R_{\rm eff}=\frac{\Delta V}{I}=\frac{5/3}{1}=\frac53", "the whole network viewed from vertices 4 and 1", ORANGE, width=9.20),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.01)
        power[0].scale_to_fit_width(10.8)
        self.play(FadeIn(power[0]))
        self.play(FadeIn(power[1]))
        self.play(FadeIn(power[2]))
        self.wait(3.3)

        # Card 9: synthesize and bridge to random movement on graphs.
        heading = self._replace_heading(
            heading, "Electrical laws turn a graph into a linear system governed by its Laplacian."
        )
        self.play(FadeOut(power))
        synthesis = VGroup(
            self._card("EDGE LAW", r"I_{i\to j}=v_i-v_j", "unit-resistance Ohm's law", TEAL_C, width=3.50),
            self._card("VERTEX LAW", r"L\mathbf v=\mathbf b", "current conservation", ORANGE, width=3.50),
            self._card("ENERGY", r"\mathbf v^TL\mathbf v", "dissipated power", GREEN_C, width=3.50),
        ).arrange(RIGHT, buff=0.34).move_to(UP * 0.39)
        condition = Text("A solution requires total injected current to equal total removed current.", font_size=23, color=WHITE).move_to(DOWN * 1.07)
        next_question = Text("What if each vertex sends probability equally among its neighbors?", font_size=25, color=YELLOW).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(synthesis))
        self.play(FadeIn(condition))
        self.play(FadeIn(next_question))
        self.wait(3.4)
