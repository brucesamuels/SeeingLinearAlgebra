"""Manim presentation: orienting edges and building an incidence matrix."""

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

from engine.graph_incidence_encoding import GraphIncidenceEncoding
from engine.simple_undirected_graph import triangle_with_tail_graph


class GraphIncidenceEncodingPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "The Incidence Matrix: Edges Meet Vertices"

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
            r"\textbf{The Incidence Matrix: Edges Meet Vertices}",
            font_size=32,
            color=YELLOW,
        ).next_to(banner, DOWN, buff=0.11)
        if title.width > 11.7:
            title.scale_to_fit_width(11.7)
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
                stroke_width=4.0,
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
        graph_group = VGroup(*edges.values(), *dots.values(), *labels.values())
        return graph_group, positions, edges, arrows, dots, labels

    @staticmethod
    def _edge_labels(positions):
        offsets = (LEFT * 0.34, DOWN * 0.30, UP * 0.29, UP * 0.29)
        return VGroup(
            *[
                MathTex(rf"e_{index}", font_size=27, color=ORANGE).move_to(
                    (positions[tail] + positions[head]) / 2 + offset
                )
                for index, ((tail, head), offset) in enumerate(
                    zip(GraphIncidenceEncodingPresentation.ORIENTED_EDGES, offsets), start=1
                )
            ]
        )

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
    def _incidence_entries():
        return [
            ["-1", "1", "0", "0"],
            ["0", "-1", "1", "0"],
            ["-1", "0", "1", "0"],
            ["0", "0", "-1", "1"],
        ]

    def construct(self):
        model = GraphIncidenceEncoding()
        expected_b = np.array(
            [[-1, 1, 0, 0], [0, -1, 1, 0], [-1, 0, 1, 0], [0, 0, -1, 1]]
        )
        if model.oriented_edges != self.ORIENTED_EDGES:
            raise RuntimeError("unexpected oriented edge order")
        if not np.array_equal(model.incidence_matrix(), expected_b):
            raise RuntimeError("unexpected incidence matrix")
        if not np.array_equal(model.edge_differences([1, 2, 3, 4]), [1, 1, 2, 1]):
            raise RuntimeError("unexpected oriented edge differences")

        banner, title, heading = self._chrome(
            "An undirected edge has no built-in direction, but we may choose one."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: orientation is bookkeeping, not a change to the graph.
        graph, _, _, arrows, _, _ = self._graph(shift=LEFT * 2.55 + DOWN * 0.10)
        orientation_card = self._card(
            "CHOSEN ORIENTATION",
            r"\text{tail}\longrightarrow\text{head}",
            "bookkeeping for each edge",
            TEAL_C,
            width=4.45,
        ).to_edge(RIGHT, buff=0.68).shift(UP * 0.30)
        unchanged = Text(
            "The underlying graph is still undirected.",
            font_size=24,
            color=GREEN_C,
        )
        unchanged.scale_to_fit_width(4.45).next_to(orientation_card, DOWN, buff=0.52)
        self.play(FadeIn(graph), FadeIn(orientation_card))
        for arrow in arrows.values():
            self.play(FadeIn(arrow), run_time=0.42)
        self.play(FadeIn(unchanged))
        self.wait(2.8)

        # Card 2: edge order, vertex order, and general matrix shape.
        heading = self._replace_heading(
            heading, "Rows follow an edge order; columns follow the vertex order."
        )
        self.play(FadeOut(graph), FadeOut(VGroup(*arrows.values())), FadeOut(orientation_card), FadeOut(unchanged))
        graph, positions, _, arrows, _, _ = self._graph(shift=LEFT * 2.80 + DOWN * 0.11)
        edge_labels = self._edge_labels(positions)
        edge_order = VGroup(
            Text("EDGE ORDER", font_size=23, color=ORANGE, weight="BOLD"),
            MathTex(r"e_1:1\to2\qquad e_2:2\to3", font_size=29, color=WHITE),
            MathTex(r"e_3:1\to3\qquad e_4:3\to4", font_size=29, color=WHITE),
            Text("VERTEX ORDER", font_size=23, color=YELLOW, weight="BOLD"),
            MathTex(r"1,\ 2,\ 3,\ 4", font_size=36, color=WHITE),
            MathTex(r"B:\ m\text{ edges}\times n\text{ vertices}", font_size=30, color=GREEN_C),
            Text("Here m = n = 4, only by coincidence.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.22).to_edge(RIGHT, buff=0.57).shift(DOWN * 0.02)
        self.play(FadeIn(graph), FadeIn(VGroup(*arrows.values())), FadeIn(edge_labels))
        self.play(FadeIn(edge_order[:3]))
        self.play(FadeIn(edge_order[3:]))
        self.wait(3.0)

        # Card 3: build one incidence row from tail and head.
        heading = self._replace_heading(
            heading, "Each edge row records minus one at its tail and plus one at its head."
        )
        self.play(FadeOut(graph), FadeOut(VGroup(*arrows.values())), FadeOut(edge_labels), FadeOut(edge_order))
        graph, positions, edges, arrows, dots, _ = self._graph(shift=LEFT * 2.75 + DOWN * 0.12)
        e1_arrow = arrows[(1, 2)]
        row = self._matrix([["-1", "1", "0", "0"]], scale=0.82, h_buff=0.90, v_buff=0.65)
        column_labels = VGroup(
            *[
                MathTex(rf"v_{vertex}", font_size=26, color=YELLOW).next_to(column, UP, buff=0.20)
                for vertex, column in zip(model.vertex_order, row.get_columns())
            ]
        )
        entry_cards = VGroup(
            self._card("TAIL", r"-1", "edge leaves vertex 1", ORANGE, width=2.75),
            self._card("HEAD", r"+1", "edge enters vertex 2", TEAL_C, width=2.75),
            self._card("OTHER", r"0", "not an endpoint", GREEN_C, width=2.75),
        ).arrange(RIGHT, buff=0.30)
        entry_cards.scale_to_fit_width(6.0)
        row_group = VGroup(
            MathTex(r"e_1:1\to2", font_size=36, color=ORANGE),
            row,
            entry_cards,
        ).arrange(DOWN, buff=0.44).to_edge(RIGHT, buff=0.46).shift(DOWN * 0.03)
        self.play(FadeIn(graph), FadeIn(e1_arrow))
        self.play(
            dots[1].animate.set_color(ORANGE),
            dots[2].animate.set_color(TEAL_C),
            ShowPassingFlash(edges[(1, 2)].copy().set_color(YELLOW).set_stroke(width=8.0)),
        )
        self.play(FadeIn(row_group[0]), FadeIn(row_group[1]), FadeIn(column_labels))
        self.play(FadeIn(row_group[2]))
        self.wait(3.0)

        # Card 4: reveal B edge by edge.
        heading = self._replace_heading(
            heading, "Apply the same rule to each oriented edge to build B."
        )
        self.play(FadeOut(graph), FadeOut(e1_arrow), FadeOut(row_group), FadeOut(column_labels))
        graph, positions, edges, arrows, dots, _ = self._graph(shift=LEFT * 2.78 + DOWN * 0.10)
        edge_labels = self._edge_labels(positions)
        incidence = self._matrix(self._incidence_entries(), scale=0.67, h_buff=0.84, v_buff=0.69)
        incidence.move_to(RIGHT * 2.48 + DOWN * 0.26)
        matrix_label = MathTex(r"B=", font_size=43, color=YELLOW).next_to(incidence, LEFT, buff=0.15)
        row_labels = VGroup(
            *[
                MathTex(rf"e_{number}", font_size=27, color=ORANGE).next_to(row, RIGHT, buff=0.27)
                for number, row in enumerate(incidence.get_rows(), start=1)
            ]
        )
        vertex_labels = VGroup(
            *[
                MathTex(rf"v_{vertex}", font_size=25, color=YELLOW).next_to(column, UP, buff=0.19)
                for vertex, column in zip(model.vertex_order, incidence.get_columns())
            ]
        )
        note = Text(
            "Every row has one -1, one +1, and zeros elsewhere.",
            font_size=23,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.43).shift(RIGHT * 2.02)
        faint_arrows = VGroup(*arrows.values()).set_opacity(0.32)
        self.play(FadeIn(graph), FadeIn(faint_arrows), FadeIn(edge_labels))
        self.play(FadeIn(matrix_label), FadeIn(incidence.get_brackets()), FadeIn(vertex_labels))
        for number, ((tail, head), matrix_row, row_label) in enumerate(
            zip(model.oriented_edges, incidence.get_rows(), row_labels), start=1
        ):
            arrow = arrows[(tail, head)]
            self.play(
                arrow.animate.set_opacity(1).set_color(ORANGE),
                dots[tail].animate.set_color(ORANGE),
                dots[head].animate.set_color(TEAL_C),
                FadeIn(row_label),
                run_time=0.42,
            )
            self.play(FadeIn(matrix_row), run_time=0.52)
            self.wait(0.28)
            self.play(
                arrow.animate.set_color(TEAL_C),
                dots[tail].animate.set_color(YELLOW),
                dots[head].animate.set_color(YELLOW),
                run_time=0.28,
            )
        self.play(FadeIn(note))
        self.wait(2.7)

        # Card 5: rows describe edges; columns describe vertex roles.
        heading = self._replace_heading(
            heading, "Rows describe edges; columns collect one vertex's roles across edges."
        )
        self.play(
            FadeOut(graph), FadeOut(faint_arrows), FadeOut(edge_labels), FadeOut(matrix_label),
            FadeOut(incidence), FadeOut(row_labels), FadeOut(vertex_labels), FadeOut(note)
        )
        incidence = self._matrix(self._incidence_entries(), scale=0.77, h_buff=0.88, v_buff=0.72)
        matrix_group = VGroup(MathTex(r"B=", font_size=45, color=YELLOW), incidence).arrange(
            RIGHT, buff=0.15
        ).to_edge(LEFT, buff=0.86).shift(DOWN * 0.05)
        row_box = SurroundingRectangle(incidence.get_rows()[2], color=ORANGE, buff=0.09, stroke_width=2.4)
        column_box = SurroundingRectangle(incidence.get_columns()[2], color=TEAL_C, buff=0.09, stroke_width=2.4)
        readings = VGroup(
            self._card("ROW e3", r"1\to3", "-1 at v1; +1 at v3", ORANGE, width=3.75),
            self._card("COLUMN v3", r"0,1,1,-1", "head twice; tail once", TEAL_C, width=3.75),
        ).arrange(DOWN, buff=0.42).to_edge(RIGHT, buff=0.66).shift(DOWN * 0.02)
        self.play(FadeIn(matrix_group))
        self.play(FadeIn(row_box), FadeIn(readings[0]))
        self.play(FadeIn(column_box), FadeIn(readings[1]))
        self.wait(3.0)

        # Card 6: B acts on vertex measurements by taking head minus tail.
        heading = self._replace_heading(
            heading, "Attach a measurement to each vertex; B compares the endpoints of every edge."
        )
        self.play(FadeOut(matrix_group), FadeOut(row_box), FadeOut(column_box), FadeOut(readings))
        graph, positions, _, arrows, _, labels = self._graph(shift=LEFT * 2.78 + DOWN * 0.12)
        value_labels = VGroup(
            MathTex(r"x_1=1", font_size=27, color=TEAL_C).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"x_2=2", font_size=27, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"x_3=3", font_size=27, color=ORANGE).next_to(labels[3], UP, buff=0.24),
            MathTex(r"x_4=4", font_size=27, color=GREEN_C).next_to(labels[4], RIGHT, buff=0.21),
        )
        comparison = VGroup(
            Text("EDGE e3 IS ORIENTED 1 TO 3", font_size=23, color=ORANGE, weight="BOLD"),
            MathTex(r"(B\mathbf x)_3", font_size=42, color=YELLOW),
            MathTex(r"=x_{\rm head}-x_{\rm tail}", font_size=37, color=WHITE),
            MathTex(r"=x_3-x_1=3-1=2", font_size=37, color=GREEN_C),
            Text("This is an oriented edge difference.", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.25).to_edge(RIGHT, buff=0.51).shift(DOWN * 0.02)
        all_arrows = VGroup(*arrows.values()).set_opacity(0.34)
        self.play(FadeIn(graph), FadeIn(all_arrows), FadeIn(value_labels))
        self.play(arrows[(1, 3)].animate.set_opacity(1).set_color(ORANGE), FadeIn(comparison[0]))
        self.play(FadeIn(comparison[1:4]))
        self.play(FadeIn(comparison[4]))
        self.wait(3.1)

        # Card 7: compute every edge difference at once.
        heading = self._replace_heading(
            heading, "One matrix-vector product computes all four edge differences."
        )
        self.play(FadeOut(graph), FadeOut(all_arrows), FadeOut(value_labels), FadeOut(comparison))
        incidence = self._matrix(self._incidence_entries(), scale=0.55, h_buff=0.77, v_buff=0.65)
        x_vector = self._matrix([["1"], ["2"], ["3"], ["4"]], scale=0.61, v_buff=0.68)
        differences = self._matrix([["1"], ["1"], ["2"], ["1"]], scale=0.61, v_buff=0.68)
        product = VGroup(
            MathTex(r"B\mathbf x=", font_size=40, color=YELLOW),
            incidence,
            x_vector,
            MathTex(r"=", font_size=37, color=YELLOW),
            differences,
        ).arrange(RIGHT, buff=0.17).to_edge(LEFT, buff=0.52).shift(DOWN * 0.03)
        calculations = VGroup(
            MathTex(r"e_1:\ 2-1=1", font_size=29, color=TEAL_C),
            MathTex(r"e_2:\ 3-2=1", font_size=29, color=TEAL_C),
            MathTex(r"e_3:\ 3-1=2", font_size=29, color=ORANGE),
            MathTex(r"e_4:\ 4-3=1", font_size=29, color=GREEN_C),
        ).arrange(DOWN, buff=0.27).to_edge(RIGHT, buff=0.63).shift(DOWN * 0.03)
        self.play(FadeIn(product[:3]))
        self.play(FadeIn(product[3:]), FadeIn(calculations))
        self.wait(3.3)

        # Card 8: reverse one bookkeeping arrow.
        heading = self._replace_heading(
            heading, "Reversing an arrow changes a sign, not the underlying graph."
        )
        self.play(FadeOut(product), FadeOut(calculations))
        graph, _, _, arrows, _, _ = self._graph(shift=LEFT * 2.78 + DOWN * 0.12)
        forward_arrow = arrows[(1, 3)]
        reverse_arrow = Arrow(
            forward_arrow.get_end(),
            forward_arrow.get_start(),
            buff=0,
            color=ORANGE,
            stroke_width=4.2,
            tip_length=0.19,
        ).set_z_index(1)
        comparisons = VGroup(
            self._card("CHOSEN 1 TO 3", r"[-1\ 0\ 1\ 0]\mathbf x=2", "head minus tail", TEAL_C, width=4.55),
            self._card("REVERSED 3 TO 1", r"[1\ 0\ {-1}\ 0]\mathbf x=-2", "the row is negated", ORANGE, width=4.55),
            MathTex(r"|2|=|-2|", font_size=38, color=GREEN_C),
            Text("The edge and the size of its difference are unchanged.", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.29).to_edge(RIGHT, buff=0.48).shift(DOWN * 0.02)
        other_arrows = VGroup(*[arrow for edge, arrow in arrows.items() if edge != (1, 3)]).set_opacity(0.35)
        self.play(FadeIn(graph), FadeIn(other_arrows), FadeIn(forward_arrow), FadeIn(comparisons[0]))
        self.play(FadeOut(forward_arrow), FadeIn(reverse_arrow), FadeIn(comparisons[1]))
        self.play(FadeIn(comparisons[2:]))
        self.wait(3.1)

        # Card 9: synthesis, constant signal, and bridge to B^T.
        heading = self._replace_heading(
            heading, "The incidence matrix turns vertex values into oriented edge differences."
        )
        self.play(FadeOut(graph), FadeOut(other_arrows), FadeOut(reverse_arrow), FadeOut(comparisons))
        synthesis = VGroup(
            self._card("ROWS", r"e_1,\ldots,e_m", "one row per edge", TEAL_C, width=3.45),
            self._card("COLUMNS", r"v_1,\ldots,v_n", "one column per vertex", ORANGE, width=3.45),
            self._card("ACTION", r"B\mathbf x", "head-minus-tail differences", GREEN_C, width=3.45),
        ).arrange(RIGHT, buff=0.40).move_to(UP * 0.55)
        constant = VGroup(
            MathTex(r"B\mathbf 1=\mathbf 0", font_size=42, color=YELLOW),
            Text("Equal vertex values create zero difference on every edge.", font_size=25, color=WHITE),
        ).arrange(DOWN, buff=0.19).move_to(DOWN * 0.88)
        next_question = Text(
            "What happens when B-transpose sends edge differences back to the vertices?",
            font_size=25,
            color=TEAL_C,
        ).to_edge(DOWN, buff=0.36)
        self.play(FadeIn(synthesis))
        self.play(FadeIn(constant))
        self.play(FadeIn(next_question))
        self.wait(3.4)
