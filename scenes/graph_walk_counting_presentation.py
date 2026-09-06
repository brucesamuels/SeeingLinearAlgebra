"""Manim presentation: powers of an adjacency matrix count walks."""

from __future__ import annotations

import numpy as np
from manim import (
    Circle,
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

from engine.graph_walk_counting import GraphWalkCounting
from engine.simple_undirected_graph import triangle_with_tail_graph


class GraphWalkCountingPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Matrix Powers Count Walks"

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
            r"\textbf{Matrix Powers Count Walks}",
            font_size=34,
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
        graph = triangle_with_tail_graph()
        positions = {vertex: point + shift for vertex, point in cls.POSITIONS.items()}
        edges = {
            edge: Line(
                positions[edge[0]],
                positions[edge[1]],
                color=GREY_B,
                stroke_width=4.2,
            ).set_z_index(0)
            for edge in graph.edges
        }
        dots = {
            vertex: Dot(positions[vertex], radius=0.17, color=YELLOW).set_z_index(2)
            for vertex in graph.vertices
        }
        labels = {
            vertex: MathTex(str(vertex), font_size=29, color=WHITE)
            .move_to(positions[vertex])
            .set_z_index(3)
            for vertex in graph.vertices
        }
        group = VGroup(*edges.values(), *dots.values(), *labels.values())
        return group, positions, edges, dots, labels

    @staticmethod
    def _matrix(entries, scale=0.67, h_buff=0.78, v_buff=0.67):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _card(label, statement, note, color, width=4.15):
        content = VGroup(
            Text(label, font_size=23, color=color, weight="BOLD"),
            MathTex(statement, font_size=36, color=WHITE),
            Text(note, font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.16)
        if content.width > width - 0.34:
            content.scale_to_fit_width(width - 0.34)
        border = SurroundingRectangle(content, color=color, buff=0.19, stroke_width=2.0)
        return VGroup(border, content)

    @staticmethod
    def _adjacency_entries():
        return [
            ["0", "1", "1", "0"],
            ["1", "0", "1", "0"],
            ["1", "1", "0", "1"],
            ["0", "0", "1", "0"],
        ]

    @staticmethod
    def _power_entries(power):
        return [[str(int(value)) for value in row] for row in power]

    @staticmethod
    def _edge_key(first, second):
        return (first, second) if first < second else (second, first)

    def _trace_route(self, route, positions, edges, marker, color=ORANGE, run_time=0.72):
        for first, second in zip(route, route[1:]):
            edge = edges[self._edge_key(first, second)]
            self.play(
                ShowPassingFlash(
                    edge.copy().set_color(color).set_stroke(width=9.0),
                    time_width=0.72,
                ),
                marker.animate.move_to(positions[second]),
                run_time=run_time,
            )

    def construct(self):
        model = GraphWalkCounting()
        expected_a2 = np.array(
            [[2, 1, 1, 1], [1, 2, 1, 1], [1, 1, 3, 0], [1, 1, 0, 1]]
        )
        expected_a3 = np.array(
            [[2, 3, 4, 1], [3, 2, 4, 1], [4, 4, 2, 3], [1, 1, 3, 0]]
        )
        if not np.array_equal(model.matrix_power(2), expected_a2):
            raise RuntimeError("unexpected square of adjacency matrix")
        if not np.array_equal(model.matrix_power(3), expected_a3):
            raise RuntimeError("unexpected cube of adjacency matrix")
        if model.walks(1, 1, 2) != ((1, 2, 1), (1, 3, 1)):
            raise RuntimeError("unexpected two-step return walks")

        banner, title, heading = self._chrome(
            "A walk follows edges; its length is the number of edge-steps."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: recall walks and exact length.
        graph, positions, edges, _, _ = self._graph(shift=LEFT * 2.45 + DOWN * 0.12)
        walk_card = self._card(
            "A TWO-STEP WALK",
            r"1\to3\to1",
            "vertices may repeat",
            TEAL_C,
            width=4.35,
        ).to_edge(RIGHT, buff=0.72).shift(UP * 0.26)
        exact_note = Text(
            "Length 2 means exactly two edges are used.",
            font_size=25,
            color=GREEN_C,
        )
        exact_note.scale_to_fit_width(4.35).next_to(walk_card, DOWN, buff=0.48)
        marker = (
            Circle(radius=0.26, color=ORANGE, stroke_width=5.0)
            .move_to(positions[1])
            .set_z_index(5)
        )
        self.play(FadeIn(graph), FadeIn(walk_card), FadeIn(marker))
        self._trace_route((1, 3, 1), positions, edges, marker, run_time=0.86)
        self.play(FadeIn(exact_note))
        self.wait(2.6)

        # Card 2: A counts one-step walks.
        heading = self._replace_heading(
            heading, "The adjacency matrix already counts walks of length one."
        )
        self.play(FadeOut(graph), FadeOut(walk_card), FadeOut(exact_note), FadeOut(marker))
        graph, positions, edges, _, _ = self._graph(shift=LEFT * 3.45 + DOWN * 0.12)
        adjacency = self._matrix(self._adjacency_entries(), scale=0.74, h_buff=0.86, v_buff=0.70)
        matrix_group = VGroup(MathTex(r"A=", font_size=44, color=YELLOW), adjacency).arrange(
            RIGHT, buff=0.14
        ).to_edge(RIGHT, buff=0.78).shift(DOWN * 0.08)
        examples = VGroup(
            MathTex(r"a_{13}=1", font_size=34, color=TEAL_C),
            Text("one direct edge-step", font_size=22, color=GREY_B),
            MathTex(r"a_{14}=0", font_size=34, color=ORANGE),
            Text("no direct edge-step", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.16).next_to(matrix_group, LEFT, buff=0.48)
        self.play(FadeIn(graph), FadeIn(matrix_group))
        self.play(
            ShowPassingFlash(edges[(1, 3)].copy().set_color(TEAL_C).set_stroke(width=8.0)),
            FadeIn(examples[0]),
            FadeIn(examples[1]),
        )
        self.play(FadeIn(examples[2]), FadeIn(examples[3]))
        self.wait(2.8)

        # Card 3: intermediate vertices create two-step walks.
        heading = self._replace_heading(
            heading, "A two-step walk is determined by its intermediate vertex."
        )
        self.play(FadeOut(graph), FadeOut(matrix_group), FadeOut(examples))
        graph, positions, edges, _, _ = self._graph(shift=LEFT * 2.55 + DOWN * 0.12)
        route_cards = VGroup(
            self._card("VIA VERTEX 2", r"1\to2\to1", "two edge-steps", TEAL_C, width=4.05),
            self._card("VIA VERTEX 3", r"1\to3\to1", "two edge-steps", ORANGE, width=4.05),
        ).arrange(DOWN, buff=0.40).to_edge(RIGHT, buff=0.73).shift(DOWN * 0.02)
        marker = (
            Circle(radius=0.26, color=TEAL_C, stroke_width=5.0)
            .move_to(positions[1])
            .set_z_index(5)
        )
        self.play(FadeIn(graph), FadeIn(route_cards[0]), FadeIn(marker))
        self._trace_route((1, 2, 1), positions, edges, marker, color=TEAL_C, run_time=0.78)
        self.play(marker.animate.set_color(ORANGE), FadeIn(route_cards[1]))
        self._trace_route((1, 3, 1), positions, edges, marker, color=ORANGE, run_time=0.78)
        self.wait(2.5)

        # Card 4: one entry of A^2 is a dot product.
        heading = self._replace_heading(
            heading, "Matrix multiplication checks every possible intermediate vertex."
        )
        self.play(FadeOut(graph), FadeOut(route_cards), FadeOut(marker))
        row = self._matrix([["0", "1", "1", "0"]], scale=0.74, h_buff=0.82, v_buff=0.64)
        column = self._matrix([["0"], ["1"], ["1"], ["0"]], scale=0.74, h_buff=0.76, v_buff=0.64)
        entry_product = VGroup(
            MathTex(r"(A^2)_{11}=", font_size=42, color=YELLOW),
            row,
            MathTex(r"\cdot", font_size=36, color=GREY_B),
            column,
        ).arrange(RIGHT, buff=0.24).move_to(UP * 0.52)
        expansion = MathTex(
            r"0\cdot0+1\cdot1+1\cdot1+0\cdot0=2",
            font_size=39,
            color=WHITE,
        ).next_to(entry_product, DOWN, buff=0.43)
        routes = MathTex(
            r"1\to2\to1\qquad 1\to3\to1",
            font_size=38,
            color=TEAL_C,
        ).next_to(expansion, DOWN, buff=0.46)
        caption = Text(
            "The two nonzero products correspond to the two walks.",
            font_size=26,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(entry_product))
        self.play(FadeIn(expansion))
        self.play(FadeIn(routes), FadeIn(caption))
        self.wait(3.2)

        # Card 5: a different entry counts a different endpoint pair.
        heading = self._replace_heading(
            heading, "From vertex 1 to vertex 4, there is one walk of length two."
        )
        self.play(FadeOut(entry_product), FadeOut(expansion), FadeOut(routes), FadeOut(caption))
        graph, positions, edges, _, _ = self._graph(shift=LEFT * 2.55 + DOWN * 0.12)
        tail_math = VGroup(
            MathTex(r"(A^2)_{14}", font_size=45, color=YELLOW),
            MathTex(r"=0\cdot0+1\cdot0+1\cdot1+0\cdot0", font_size=34, color=WHITE),
            MathTex(r"=1", font_size=46, color=GREEN_C),
            MathTex(r"1\to3\to4", font_size=39, color=TEAL_C),
        ).arrange(DOWN, buff=0.28).to_edge(RIGHT, buff=0.72).shift(DOWN * 0.02)
        marker = (
            Circle(radius=0.26, color=ORANGE, stroke_width=5.0)
            .move_to(positions[1])
            .set_z_index(5)
        )
        self.play(FadeIn(graph), FadeIn(tail_math[:3]), FadeIn(marker))
        self._trace_route((1, 3, 4), positions, edges, marker, run_time=0.86)
        self.play(FadeIn(tail_math[3]))
        self.wait(2.8)

        # Card 6: every entry of A^2 is a walk count.
        heading = self._replace_heading(
            heading, "Computing every row-column product fills the entire square."
        )
        self.play(FadeOut(graph), FadeOut(tail_math), FadeOut(marker))
        square = self._matrix(self._power_entries(expected_a2), scale=0.82, h_buff=0.90, v_buff=0.74)
        square_group = VGroup(MathTex(r"A^2=", font_size=48, color=YELLOW), square).arrange(
            RIGHT, buff=0.17
        ).move_to(UP * 0.10)
        entries = list(square.get_entries())
        box_11 = SurroundingRectangle(entries[0], color=TEAL_C, buff=0.10, stroke_width=2.4)
        box_14 = SurroundingRectangle(entries[3], color=ORANGE, buff=0.10, stroke_width=2.4)
        box_34 = SurroundingRectangle(entries[11], color=GREEN_C, buff=0.10, stroke_width=2.4)
        interpretations = VGroup(
            MathTex(r"(A^2)_{11}=2", font_size=32, color=TEAL_C),
            MathTex(r"(A^2)_{14}=1", font_size=32, color=ORANGE),
            MathTex(r"(A^2)_{34}=0", font_size=32, color=GREEN_C),
        ).arrange(RIGHT, buff=0.75).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(square_group))
        self.play(FadeIn(box_11), FadeIn(interpretations[0]))
        self.play(FadeIn(box_14), FadeIn(interpretations[1]))
        self.play(FadeIn(box_34), FadeIn(interpretations[2]))
        self.wait(3.0)

        # Card 7: a cube counts three-step walks, including repetitions.
        heading = self._replace_heading(
            heading, "Multiplying once more appends one more edge-step to every walk."
        )
        self.play(
            FadeOut(square_group),
            FadeOut(box_11),
            FadeOut(box_14),
            FadeOut(box_34),
            FadeOut(interpretations),
        )
        cube = self._matrix(self._power_entries(expected_a3), scale=0.72, h_buff=0.84, v_buff=0.69)
        cube_group = VGroup(MathTex(r"A^3=A^2A=", font_size=42, color=YELLOW), cube).arrange(
            RIGHT, buff=0.16
        ).to_edge(LEFT, buff=0.78).shift(DOWN * 0.06)
        cube_entry = list(cube.get_entries())[2]
        cube_box = SurroundingRectangle(cube_entry, color=ORANGE, buff=0.10, stroke_width=2.5)
        route_list = VGroup(
            Text("FOUR THREE-STEP WALKS FROM 1 TO 3", font_size=22, color=ORANGE, weight="BOLD"),
            MathTex(r"1\to2\to1\to3", font_size=29, color=WHITE),
            MathTex(r"1\to3\to1\to3", font_size=29, color=WHITE),
            MathTex(r"1\to3\to2\to3", font_size=29, color=WHITE),
            MathTex(r"1\to3\to4\to3", font_size=29, color=WHITE),
            Text("Walks may revisit vertices.", font_size=24, color=GREEN_C),
        ).arrange(DOWN, buff=0.18).to_edge(RIGHT, buff=0.67).shift(DOWN * 0.04)
        self.play(FadeIn(cube_group), FadeIn(cube_box))
        self.play(FadeIn(route_list[:5]))
        self.play(FadeIn(route_list[5]))
        self.wait(3.2)

        # Card 8: state the general counting rule and its mechanism.
        heading = self._replace_heading(
            heading, "The pattern continues: the exponent records the exact walk length."
        )
        self.play(FadeOut(cube_group), FadeOut(cube_box), FadeOut(route_list))
        rule = self._card(
            "WALK-COUNTING RULE",
            r"(A^k)_{ij}=\#\{\text{length-}k\text{ walks }i\to j\}",
            "exactly k edge-steps",
            TEAL_C,
            width=8.65,
        ).move_to(UP * 0.66)
        mechanism = VGroup(
            self._card("ONE STEP", r"A", "records direct choices", ORANGE, width=3.35),
            self._card("APPEND A STEP", r"A^kA", "sum over the next choice", GREEN_C, width=3.75),
            self._card("K STEPS", r"A^k", "counts completed walks", YELLOW, width=3.35),
        ).arrange(RIGHT, buff=0.34).to_edge(DOWN, buff=0.52)
        self.play(FadeIn(rule))
        self.play(FadeIn(mechanism[0]))
        self.play(FadeIn(mechanism[1]))
        self.play(FadeIn(mechanism[2]))
        self.wait(3.2)

        # Card 9: synthesis and bridge to incidence matrices.
        heading = self._replace_heading(
            heading, "Matrix multiplication turns local connections into multi-step information."
        )
        self.play(FadeOut(rule), FadeOut(mechanism))
        synthesis = VGroup(
            self._card("GRAPH", r"i\!-\!j", "available edge-steps", TEAL_C, width=3.45),
            self._card("ADJACENCY", r"A", "one-step walk counts", ORANGE, width=3.45),
            self._card("POWERS", r"A^k", "k-step walk counts", GREEN_C, width=3.45),
        ).arrange(RIGHT, buff=0.42).move_to(UP * 0.22)
        closing = Text(
            "Next: give each edge an orientation and encode it with signs.",
            font_size=27,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(synthesis))
        self.play(FadeIn(closing))
        self.wait(3.2)
