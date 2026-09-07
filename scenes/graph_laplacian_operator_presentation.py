"""Manim presentation: the graph Laplacian as B-transpose B and D minus A."""

from __future__ import annotations

import numpy as np
from manim import (
    BLACK,
    DOWN,
    Arrow,
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

from engine.graph_laplacian_operator import GraphLaplacianOperator
from engine.simple_undirected_graph import triangle_with_tail_graph


class GraphLaplacianOperatorPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "The Graph Laplacian: Differences Return"

    POSITIONS = {
        1: LEFT * 2.15 + UP * 1.15,
        2: LEFT * 2.15 + DOWN * 1.15,
        3: RIGHT * 0.10,
        4: RIGHT * 2.75,
    }
    ORIENTED_EDGES = ((1, 2), (2, 3), (1, 3), (3, 4))

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
            r"\textbf{The Graph Laplacian: Differences Return}",
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
        graph = triangle_with_tail_graph()
        positions = {vertex: point + shift for vertex, point in cls.POSITIONS.items()}
        edges = {
            edge: Line(
                positions[edge[0]], positions[edge[1]], color=GREY_B, stroke_width=4.0
            ).set_z_index(0)
            for edge in graph.edges
        }
        arrows = {
            edge: Arrow(
                positions[edge[0]],
                positions[edge[1]],
                buff=0.24,
                color=TEAL_C,
                stroke_width=3.5,
                tip_length=0.18,
            ).set_z_index(1)
            for edge in cls.ORIENTED_EDGES
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
        return VGroup(*edges.values(), *dots.values(), *labels.values()), positions, edges, arrows, dots, labels

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
    def _b_entries():
        return [["-1", "1", "0", "0"], ["0", "-1", "1", "0"], ["-1", "0", "1", "0"], ["0", "0", "-1", "1"]]

    @staticmethod
    def _bt_entries():
        return [["-1", "0", "-1", "0"], ["1", "-1", "0", "0"], ["0", "1", "1", "-1"], ["0", "0", "0", "1"]]

    @staticmethod
    def _l_entries():
        return [["2", "-1", "-1", "0"], ["-1", "2", "-1", "0"], ["-1", "-1", "3", "-1"], ["0", "0", "-1", "1"]]

    def construct(self):
        model = GraphLaplacianOperator()
        expected_l = np.array(
            [[2, -1, -1, 0], [-1, 2, -1, 0], [-1, -1, 3, -1], [0, 0, -1, 1]]
        )
        if not np.array_equal(model.laplacian_matrix(), expected_l):
            raise RuntimeError("unexpected graph Laplacian")
        if not np.array_equal(model.apply([1, 2, 3, 4]), [-3, 0, 2, 1]):
            raise RuntimeError("unexpected Laplacian action")
        if not np.array_equal(model.with_reversed_edge(3).laplacian_matrix(), expected_l):
            raise RuntimeError("Laplacian should not depend on orientation")

        banner, title, heading = self._chrome(
            "B sends vertex values to oriented differences on the edges."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: recall Bx as vertex-to-edge data.
        graph, _, _, arrows, _, labels = self._graph(shift=LEFT * 2.76 + DOWN * 0.11)
        values = VGroup(
            MathTex(r"x_1=1", font_size=27, color=TEAL_C).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"x_2=2", font_size=27, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"x_3=3", font_size=27, color=ORANGE).next_to(labels[3], UP, buff=0.24),
            MathTex(r"x_4=4", font_size=27, color=GREEN_C).next_to(labels[4], RIGHT, buff=0.21),
        )
        pipeline = VGroup(
            self._card("VERTEX VALUES", r"\mathbf x=(1,2,3,4)^T", "one value per vertex", TEAL_C, width=4.70),
            MathTex(r"\xrightarrow{\quad B\quad}", font_size=39, color=YELLOW),
            self._card("EDGE DIFFERENCES", r"B\mathbf x=(1,1,2,1)^T", "head minus tail", ORANGE, width=4.70),
        ).arrange(DOWN, buff=0.32).to_edge(RIGHT, buff=0.48).shift(DOWN * 0.02)
        self.play(FadeIn(graph), FadeIn(VGroup(*arrows.values())), FadeIn(values))
        self.play(FadeIn(pipeline[0]))
        self.play(FadeIn(pipeline[1]), FadeIn(pipeline[2]))
        self.wait(3.0)

        # Card 2: B-transpose returns signed edge data to vertices.
        heading = self._replace_heading(
            heading, "B-transpose gathers signed edge values back at each vertex."
        )
        self.play(FadeOut(graph), FadeOut(VGroup(*arrows.values())), FadeOut(values), FadeOut(pipeline))
        edge_vector = self._matrix([["1"], ["1"], ["2"], ["1"]], scale=0.66, v_buff=0.70)
        bt = self._matrix(self._bt_entries(), scale=0.59, h_buff=0.78, v_buff=0.67)
        returned = self._matrix([["-3"], ["0"], ["2"], ["1"]], scale=0.66, v_buff=0.70)
        return_product = VGroup(
            MathTex(r"B^T", font_size=42, color=YELLOW), bt, edge_vector,
            MathTex(r"=", font_size=39, color=YELLOW), returned,
        ).arrange(RIGHT, buff=0.18).move_to(UP * 0.33)
        v1_check = MathTex(
            r"\text{at }v_1:\quad -1-2=-3",
            font_size=38,
            color=ORANGE,
        ).next_to(return_product, DOWN, buff=0.44)
        sign_note = Text(
            "Outgoing differences subtract; incoming differences add.",
            font_size=26,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.64)
        self.play(FadeIn(return_product[:3]))
        self.play(FadeIn(return_product[3:]), FadeIn(v1_check))
        self.play(FadeIn(sign_note))
        self.wait(3.2)

        # Card 3: name the composition.
        heading = self._replace_heading(
            heading, "Compose the two trips: vertices to edges, then edges to vertices."
        )
        self.play(FadeOut(return_product), FadeOut(v1_check), FadeOut(sign_note))
        composition = VGroup(
            self._card("VERTICES", r"\mathbf x", "starting values", TEAL_C, width=3.15),
            MathTex(r"\xrightarrow{\ B\ }", font_size=37, color=YELLOW),
            self._card("EDGES", r"B\mathbf x", "differences", ORANGE, width=3.15),
            MathTex(r"\xrightarrow{\ B^T\ }", font_size=37, color=YELLOW),
            self._card("VERTICES", r"B^TB\mathbf x", "returned differences", GREEN_C, width=3.40),
        ).arrange(RIGHT, buff=0.20).move_to(UP * 0.52)
        definition = VGroup(
            Text("THE GRAPH LAPLACIAN", font_size=26, color=YELLOW, weight="BOLD"),
            MathTex(r"L=B^TB", font_size=52, color=WHITE),
            Text("a vertex-to-vertex operator", font_size=25, color=GREY_B),
        ).arrange(DOWN, buff=0.20).move_to(DOWN * 1.15)
        self.play(FadeIn(composition[:3]))
        self.play(FadeIn(composition[3:]))
        self.play(FadeIn(definition))
        self.wait(3.2)

        # Card 4: calculate B^T B structurally.
        heading = self._replace_heading(
            heading, "For the recurring graph, multiplying B-transpose by B gives L."
        )
        self.play(FadeOut(composition), FadeOut(definition))
        bt = self._matrix(self._bt_entries(), scale=0.51, h_buff=0.69, v_buff=0.61)
        b = self._matrix(self._b_entries(), scale=0.51, h_buff=0.69, v_buff=0.61)
        laplacian = self._matrix(self._l_entries(), scale=0.60, h_buff=0.74, v_buff=0.64)
        product = VGroup(
            MathTex(r"L=B^TB=", font_size=38, color=YELLOW),
            bt,
            b,
            MathTex(r"=", font_size=36, color=YELLOW),
            laplacian,
        ).arrange(RIGHT, buff=0.14).move_to(DOWN * 0.06)
        source_labels = VGroup(
            Text("vertex by edge", font_size=20, color=TEAL_C).next_to(bt, UP, buff=0.24),
            Text("edge by vertex", font_size=20, color=ORANGE).next_to(b, UP, buff=0.24),
            Text("vertex by vertex", font_size=20, color=GREEN_C).next_to(laplacian, UP, buff=0.24),
        )
        self.play(FadeIn(product[:3]), FadeIn(source_labels[:2]))
        self.play(FadeIn(product[3:]), FadeIn(source_labels[2]))
        self.wait(3.3)

        # Card 5: read L directly from degrees and adjacency.
        heading = self._replace_heading(
            heading, "The same matrix places degrees on the diagonal and minus ones on edges."
        )
        self.play(FadeOut(product), FadeOut(source_labels))
        laplacian = self._matrix(self._l_entries(), scale=0.78, h_buff=0.88, v_buff=0.72)
        matrix_group = VGroup(MathTex(r"L=", font_size=46, color=YELLOW), laplacian).arrange(
            RIGHT, buff=0.15
        ).to_edge(LEFT, buff=0.86).shift(DOWN * 0.03)
        entries = list(laplacian.get_entries())
        diagonal_boxes = VGroup(
            *[SurroundingRectangle(entries[index], color=ORANGE, buff=0.08, stroke_width=2.1) for index in (0, 5, 10, 15)]
        )
        readings = VGroup(
            self._card("DIAGONAL", r"L_{ii}=\deg(v_i)", "number of neighbors", ORANGE, width=4.15),
            self._card("OFF DIAGONAL", r"L_{ij}=-1", "when i and j share an edge", TEAL_C, width=4.15),
            MathTex(r"L=D-A", font_size=45, color=GREEN_C),
        ).arrange(DOWN, buff=0.34).to_edge(RIGHT, buff=0.62).shift(DOWN * 0.02)
        self.play(FadeIn(matrix_group), FadeIn(diagonal_boxes), FadeIn(readings[0]))
        self.play(FadeIn(readings[1]))
        self.play(FadeIn(readings[2]))
        self.wait(3.2)

        # Card 6: one coordinate is a local neighbor comparison.
        heading = self._replace_heading(
            heading, "Each coordinate compares one vertex value with all of its neighbors."
        )
        self.play(FadeOut(matrix_group), FadeOut(diagonal_boxes), FadeOut(readings))
        graph, _, edges, _, _, labels = self._graph(shift=LEFT * 2.76 + DOWN * 0.11)
        values = VGroup(
            MathTex(r"x_1=1", font_size=27, color=ORANGE).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"x_2=2", font_size=27, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"x_3=3", font_size=27, color=TEAL_C).next_to(labels[3], UP, buff=0.24),
            MathTex(r"x_4=4", font_size=27, color=GREEN_C).next_to(labels[4], RIGHT, buff=0.21),
        )
        local = VGroup(
            Text("AT VERTEX 1", font_size=24, color=ORANGE, weight="BOLD"),
            MathTex(r"(L\mathbf x)_1", font_size=43, color=YELLOW),
            MathTex(r"=(x_1-x_2)+(x_1-x_3)", font_size=35, color=WHITE),
            MathTex(r"=(1-2)+(1-3)=-3", font_size=35, color=GREEN_C),
            Text("Compare with each neighbor, then add.", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.25).to_edge(RIGHT, buff=0.48).shift(DOWN * 0.02)
        self.play(FadeIn(graph), FadeIn(values), FadeIn(local[0]))
        self.play(
            ShowPassingFlash(edges[(1, 2)].copy().set_color(ORANGE).set_stroke(width=8.0)),
            ShowPassingFlash(edges[(1, 3)].copy().set_color(ORANGE).set_stroke(width=8.0)),
        )
        self.play(FadeIn(local[1:4]))
        self.play(FadeIn(local[4]))
        self.wait(3.2)

        # Card 7: compute the full action and interpret a balanced coordinate.
        heading = self._replace_heading(
            heading, "L computes all local neighbor comparisons in one matrix-vector product."
        )
        self.play(FadeOut(graph), FadeOut(values), FadeOut(local))
        laplacian = self._matrix(self._l_entries(), scale=0.55, h_buff=0.77, v_buff=0.65)
        x_vector = self._matrix([["1"], ["2"], ["3"], ["4"]], scale=0.61, v_buff=0.68)
        result = self._matrix([["-3"], ["0"], ["2"], ["1"]], scale=0.61, v_buff=0.68)
        action = VGroup(
            MathTex(r"L\mathbf x=", font_size=40, color=YELLOW), laplacian, x_vector,
            MathTex(r"=", font_size=37, color=YELLOW), result,
        ).arrange(RIGHT, buff=0.17).to_edge(LEFT, buff=0.52).shift(DOWN * 0.02)
        coordinate_checks = VGroup(
            MathTex(r"v_1:\ -3", font_size=30, color=ORANGE),
            MathTex(r"v_2:\ (2-1)+(2-3)=0", font_size=30, color=TEAL_C),
            MathTex(r"v_3:\ 2", font_size=30, color=GREEN_C),
            MathTex(r"v_4:\ 1", font_size=30, color=GREEN_C),
            Text("Zero at v2 means its neighbor comparisons balance.", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.24).to_edge(RIGHT, buff=0.49).shift(DOWN * 0.02)
        self.play(FadeIn(action[:3]))
        self.play(FadeIn(action[3:]), FadeIn(coordinate_checks[:4]))
        self.play(FadeIn(coordinate_checks[4]))
        self.wait(3.2)

        # Card 8: arbitrary edge orientation disappears in B^T B.
        heading = self._replace_heading(
            heading, "Reverse a bookkeeping arrow: both signs flip, so L stays unchanged."
        )
        self.play(FadeOut(action), FadeOut(coordinate_checks))
        graph, _, _, arrows, _, _ = self._graph(shift=LEFT * 2.78 + DOWN * 0.12)
        forward_arrow = arrows[(1, 3)]
        reverse_arrow = Arrow(
            forward_arrow.get_end(), forward_arrow.get_start(), buff=0,
            color=ORANGE, stroke_width=4.2, tip_length=0.19,
        ).set_z_index(1)
        other_arrows = VGroup(*[arrow for edge, arrow in arrows.items() if edge != (1, 3)]).set_opacity(0.34)
        cancellation = VGroup(
            self._card("ORIGINAL ROW", r"\mathbf b_3=[-1\ 0\ 1\ 0]", "edge difference = 2", TEAL_C, width=4.55),
            self._card("REVERSED ROW", r"-\mathbf b_3=[1\ 0\ {-1}\ 0]", "edge difference = -2", ORANGE, width=4.55),
            MathTex(r"(-\mathbf b_3)^T(-\mathbf b_3)=\mathbf b_3^T\mathbf b_3", font_size=34, color=GREEN_C),
            MathTex(r"B'^TB'=B^TB=L", font_size=42, color=YELLOW),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.02)
        self.play(FadeIn(graph), FadeIn(other_arrows), FadeIn(forward_arrow), FadeIn(cancellation[0]))
        self.play(FadeOut(forward_arrow), FadeIn(reverse_arrow), FadeIn(cancellation[1]))
        self.play(FadeIn(cancellation[2]))
        self.play(FadeIn(cancellation[3]))
        self.wait(3.2)

        # Card 9: synthesis, constants, and bridge to energy.
        heading = self._replace_heading(
            heading, "The Laplacian measures how vertex values differ across the graph."
        )
        self.play(FadeOut(graph), FadeOut(other_arrows), FadeOut(reverse_arrow), FadeOut(cancellation))
        synthesis = VGroup(
            self._card("INCIDENCE", r"L=B^TB", "differences out and back", TEAL_C, width=3.55),
            self._card("GRAPH DATA", r"L=D-A", "degrees minus adjacency", ORANGE, width=3.55),
            self._card("LOCAL ACTION", r"(L\mathbf x)_i", "own-minus-neighbor sums", GREEN_C, width=3.55),
        ).arrange(RIGHT, buff=0.35).move_to(UP * 0.57)
        constant = VGroup(
            MathTex(r"L\mathbf 1=\mathbf 0", font_size=43, color=YELLOW),
            Text("A constant value has no differences across any edge.", font_size=25, color=WHITE),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 0.87)
        next_question = Text(
            "Can one number measure the total variation across all edges?",
            font_size=25,
            color=TEAL_C,
        ).to_edge(DOWN, buff=0.37)
        self.play(FadeIn(synthesis))
        self.play(FadeIn(constant))
        self.play(FadeIn(next_question))
        self.wait(3.4)
