"""Manim presentation: connected components and the Laplacian null space."""

from __future__ import annotations

import numpy as np
from manim import (
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

from engine.graph_laplacian_null_space import GraphLaplacianNullSpace
from engine.simple_undirected_graph import triangle_with_tail_graph


class GraphLaplacianNullSpacePresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Connected Components and the Laplacian Null Space"

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
            r"\textbf{Connected Components and the Laplacian Null Space}",
            font_size=31,
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
    def _graph(cls, shift=DOWN * 0.12, include_bridge=True):
        graph = triangle_with_tail_graph()
        positions = {vertex: point + shift for vertex, point in cls.POSITIONS.items()}
        graph_edges = graph.edges if include_bridge else graph.edges[:-1]
        edges = {
            edge: Line(
                positions[edge[0]], positions[edge[1]], color=GREY_B, stroke_width=4.0
            ).set_z_index(0)
            for edge in graph_edges
        }
        dots = {
            vertex: Dot(positions[vertex], radius=0.17, color=YELLOW).set_z_index(2)
            for vertex in graph.vertices
        }
        labels = {
            vertex: MathTex(str(vertex), font_size=29, color=BLACK)
            .move_to(positions[vertex])
            .set_z_index(3)
            for vertex in graph.vertices
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

    def construct(self):
        model = GraphLaplacianNullSpace()
        connected = GraphLaplacianNullSpace(triangle_with_tail_graph())
        if model.components != ((1, 2, 3), (4,)) or model.nullity != 2:
            raise RuntimeError("unexpected connected components")
        if not np.array_equal(model.component_constant_signal([2, 5]), [2, 2, 2, 5]):
            raise RuntimeError("unexpected componentwise-constant signal")
        if model.null_space_characterization([2, 2, 2, 5]) != (True, True):
            raise RuntimeError("unexpected Laplacian null vector")
        if connected.nullity != 1:
            raise RuntimeError("connected graph should have one null direction")

        banner, title, heading = self._chrome(
            "On a connected graph, zero energy forced one constant across all vertices."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: recall the connected case from CP231.
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.10)
        constant_labels = VGroup(
            *[
                MathTex(r"c", font_size=27, color=GREEN_C).next_to(label, direction, buff=0.22)
                for label, direction in zip(labels.values(), (UP + LEFT, DOWN + LEFT, UP, RIGHT))
            ]
        )
        recall = VGroup(
            self._card("ZERO ENERGY", r"\mathbf x^TL\mathbf x=0", "every edge difference is zero", TEAL_C, width=4.70),
            MathTex(r"\operatorname{Null}(L)=\operatorname{span}\{\mathbf 1\}", font_size=38, color=GREEN_C),
            Text("one connected component, one free constant", font_size=23, color=GREY_B),
        ).arrange(DOWN, buff=0.36).to_edge(RIGHT, buff=0.43).shift(DOWN * 0.02)
        self.play(
            FadeIn(graph),
            *[edge.animate.set_color(TEAL_C).set_stroke(width=5.2) for edge in edges.values()],
            *[dot.animate.set_color(GREEN_C) for dot in dots.values()],
        )
        self.play(FadeIn(constant_labels), FadeIn(recall))
        self.wait(3.0)

        # Card 2: remove the bridge and reveal two components.
        heading = self._replace_heading(
            heading, "Remove the bridge: no path remains between vertex 4 and the triangle."
        )
        self.play(FadeOut(graph), FadeOut(constant_labels), FadeOut(recall))
        graph, positions, edges, dots, labels = self._graph(shift=LEFT * 1.02 + DOWN * 0.10)
        bridge = edges[(3, 4)]
        bridge_label = Text("bridge", font_size=23, color=ORANGE).next_to(bridge, UP, buff=0.13)
        self.play(FadeIn(graph), FadeIn(bridge_label))
        self.play(ShowPassingFlash(bridge.copy().set_color(ORANGE).set_stroke(width=10)), run_time=0.9)
        self.play(FadeOut(bridge), FadeOut(bridge_label))
        triangle_group = VGroup(dots[1], dots[2], dots[3], labels[1], labels[2], labels[3])
        isolated_group = VGroup(dots[4], labels[4])
        boxes = VGroup(
            SurroundingRectangle(triangle_group, color=TEAL_C, buff=0.43, stroke_width=2.5),
            SurroundingRectangle(isolated_group, color=ORANGE, buff=0.43, stroke_width=2.5),
        )
        component_names = VGroup(
            MathTex(r"C_1=\{1,2,3\}", font_size=31, color=TEAL_C).next_to(boxes[0], DOWN, buff=0.18),
            MathTex(r"C_2=\{4\}", font_size=31, color=ORANGE).next_to(boxes[1], DOWN, buff=0.18),
        )
        count_note = Text("The split graph has two connected components.", font_size=27, color=WHITE).to_edge(DOWN, buff=0.68)
        self.play(FadeIn(boxes), FadeIn(component_names), FadeIn(count_note))
        self.wait(3.0)

        # Card 3: independent constants on disconnected components have zero energy.
        heading = self._replace_heading(
            heading, "With no edge between the components, their constants may differ."
        )
        self.play(FadeOut(graph), FadeOut(boxes), FadeOut(component_names), FadeOut(count_note))
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.09, include_bridge=False)
        values = VGroup(
            *[
                MathTex(symbol, font_size=28, color=color).next_to(labels[vertex], direction, buff=0.22)
                for vertex, symbol, color, direction in (
                    (1, r"a", TEAL_C, UP + LEFT),
                    (2, r"a", TEAL_C, DOWN + LEFT),
                    (3, r"a", TEAL_C, UP),
                    (4, r"b", ORANGE, RIGHT),
                )
            ]
        )
        zero_edges = VGroup(
            MathTex(r"(a-a)^2=0", font_size=24, color=TEAL_C).move_to(LEFT * 4.83 + DOWN * 0.10),
            MathTex(r"(a-a)^2=0", font_size=24, color=TEAL_C).move_to(LEFT * 3.15 + UP * 0.73),
            MathTex(r"(a-a)^2=0", font_size=24, color=TEAL_C).move_to(LEFT * 3.15 + DOWN * 0.78),
        )
        result = VGroup(
            self._card("COMPONENTWISE CONSTANT", r"\mathbf x=(a,a,a,b)^T", "a and b are independent", ORANGE, width=4.82),
            MathTex(r"\mathbf x^TL\mathbf x=0", font_size=43, color=GREEN_C),
            Text("No edge compares a with b.", font_size=25, color=YELLOW),
        ).arrange(DOWN, buff=0.38).to_edge(RIGHT, buff=0.39).shift(DOWN * 0.03)
        self.play(FadeIn(graph), FadeIn(values))
        self.play(
            *[edge.animate.set_color(TEAL_C).set_stroke(width=5.5) for edge in edges.values()],
            FadeIn(zero_edges),
        )
        self.play(FadeIn(result))
        self.wait(3.1)

        # Card 4: verify the null equation structurally.
        heading = self._replace_heading(
            heading, "The split graph's Laplacian sends every such vector to zero."
        )
        self.play(FadeOut(graph), FadeOut(values), FadeOut(zero_edges), FadeOut(result))
        laplacian = self._matrix(
            [["2", "-1", "-1", "0"], ["-1", "2", "-1", "0"], ["-1", "-1", "2", "0"], ["0", "0", "0", "0"]],
            scale=0.54,
            h_buff=0.73,
            v_buff=0.65,
        )
        signal = self._matrix([["a"], ["a"], ["a"], ["b"]], scale=0.65, v_buff=0.66)
        zero = self._matrix([["0"], ["0"], ["0"], ["0"]], scale=0.65, v_buff=0.66)
        null_equation = VGroup(
            MathTex(r"L_{\rm split}\mathbf x=", font_size=39, color=YELLOW),
            laplacian,
            signal,
            MathTex(r"=", font_size=39, color=WHITE),
            zero,
        ).arrange(RIGHT, buff=0.18).move_to(UP * 0.20)
        explanation = Text(
            "The first three rows compare equal values; the isolated vertex has a zero row.",
            font_size=24,
            color=TEAL_C,
        ).to_edge(DOWN, buff=0.78)
        explanation.scale_to_fit_width(11.0)
        self.play(FadeIn(null_equation[:-1]))
        self.play(FadeIn(null_equation[-1]), FadeIn(explanation))
        self.wait(3.1)

        # Card 5: build one null vector for each component.
        heading = self._replace_heading(
            heading, "Mark one component at a time to obtain two independent null vectors."
        )
        self.play(FadeOut(null_equation), FadeOut(explanation))
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 2.82 + DOWN * 0.09, include_bridge=False)
        first_indicator = self._matrix([["1"], ["1"], ["1"], ["0"]], scale=0.63, v_buff=0.66)
        second_indicator = self._matrix([["0"], ["0"], ["0"], ["1"]], scale=0.63, v_buff=0.66)
        basis = VGroup(
            VGroup(MathTex(r"\mathbf u_1=", font_size=35, color=TEAL_C), first_indicator).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"\mathbf u_2=", font_size=35, color=ORANGE), second_indicator).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.70).to_edge(RIGHT, buff=0.38).shift(DOWN * 0.06)
        basis_note = Text("Each vector is 1 on its component and 0 elsewhere.", font_size=24, color=WHITE).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(graph), FadeIn(basis[0]))
        self.play(
            *[dots[v].animate.set_color(TEAL_C) for v in (1, 2, 3)],
            *[edges[e].animate.set_color(TEAL_C).set_stroke(width=5.2) for e in edges],
        )
        self.play(FadeIn(basis[1]), dots[4].animate.set_color(ORANGE))
        self.play(FadeIn(basis_note))
        self.wait(3.0)

        # Card 6: the indicators span every null vector.
        heading = self._replace_heading(
            heading, "Scale and add the component indicators to make every zero-energy signal."
        )
        self.play(FadeOut(graph), FadeOut(basis), FadeOut(basis_note))
        u_one = self._matrix([["1"], ["1"], ["1"], ["0"]], scale=0.58, v_buff=0.64)
        u_two = self._matrix([["0"], ["0"], ["0"], ["1"]], scale=0.58, v_buff=0.64)
        combination = VGroup(
            MathTex(r"a", font_size=39, color=TEAL_C),
            u_one,
            MathTex(r"+b", font_size=39, color=ORANGE),
            u_two,
            MathTex(r"=", font_size=39, color=WHITE),
            self._matrix([["a"], ["a"], ["a"], ["b"]], scale=0.58, v_buff=0.64),
        ).arrange(RIGHT, buff=0.15).move_to(UP * 0.37)
        null_span = MathTex(
            r"\operatorname{Null}(L_{\rm split})=\operatorname{span}\{\mathbf u_1,\mathbf u_2\}",
            font_size=41,
            color=GREEN_C,
        ).move_to(DOWN * 1.28)
        dimension = Text("two independent component constants  →  nullity 2", font_size=25, color=YELLOW).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(combination[:2]))
        self.play(FadeIn(combination[2:4]))
        self.play(FadeIn(combination[4:]), FadeIn(null_span))
        self.play(FadeIn(dimension))
        self.wait(3.1)

        # Card 7: prove the general characterization from the energy identity.
        heading = self._replace_heading(
            heading, "The energy identity proves both directions of the component theorem."
        )
        self.play(FadeOut(combination), FadeOut(null_span), FadeOut(dimension))
        proof = VGroup(
            self._card(
                "IF Lx = 0",
                r"0=\mathbf x^TL\mathbf x=\sum_{\{i,j\}\in E}(x_i-x_j)^2",
                "every edge forces equal endpoint values",
                TEAL_C,
                width=10.30,
            ),
            self._card(
                "IF x IS CONSTANT ON EACH COMPONENT",
                r"B\mathbf x=\mathbf 0\quad\Longrightarrow\quad L\mathbf x=B^TB\mathbf x=\mathbf 0",
                "every edge stays inside one component",
                ORANGE,
                width=10.30,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.05)
        self.play(FadeIn(proof[0]))
        self.play(FadeIn(proof[1]))
        self.wait(3.3)

        # Card 8: compare the connected and split recurring graphs.
        heading = self._replace_heading(
            heading, "Removing one bridge creates one additional independent zero direction."
        )
        self.play(FadeOut(proof))
        comparison = VGroup(
            self._card(
                "CONNECTED GRAPH",
                r"\operatorname{Null}(L)=\operatorname{span}\{\mathbf 1\}",
                "1 component  →  nullity 1",
                TEAL_C,
                width=5.25,
            ),
            self._card(
                "SPLIT GRAPH",
                r"\operatorname{Null}(L)=\operatorname{span}\{\mathbf u_1,\mathbf u_2\}",
                "2 components  →  nullity 2",
                ORANGE,
                width=5.25,
            ),
        ).arrange(RIGHT, buff=0.55).move_to(UP * 0.27)
        bridge_effect = Text(
            "Vertex 4 can now choose its constant independently of the triangle.",
            font_size=26,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.82)
        self.play(FadeIn(comparison[0]))
        self.play(FadeIn(comparison[1]))
        self.play(FadeIn(bridge_effect))
        self.wait(3.1)

        # Card 9: state the theorem and bridge to the Laplacian spectrum.
        heading = self._replace_heading(
            heading, "The Laplacian null space records exactly how the graph is connected."
        )
        self.play(FadeOut(comparison), FadeOut(bridge_effect))
        theorem = VGroup(
            Text("COMPONENT–NULLITY THEOREM", font_size=25, color=YELLOW, weight="BOLD"),
            MathTex(
                r"\operatorname{Null}(L)=\{\text{vectors constant on each component}\}",
                font_size=37,
                color=WHITE,
            ),
            MathTex(
                r"\dim\operatorname{Null}(L)=\text{number of connected components}",
                font_size=39,
                color=GREEN_C,
            ),
            Text("Each component contributes one independent zero direction.", font_size=25, color=TEAL_C),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.20)
        next_question = Text(
            "After the zero directions, what does the first positive eigenvalue reveal?",
            font_size=25,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.72)
        next_question.scale_to_fit_width(10.8)
        self.play(FadeIn(theorem[0]), FadeIn(theorem[1]))
        self.play(FadeIn(theorem[2]), FadeIn(theorem[3]))
        self.play(FadeIn(next_question))
        self.wait(3.4)
