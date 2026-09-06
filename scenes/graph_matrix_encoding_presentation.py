"""Manim presentation: encoding a graph with adjacency and degree matrices."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    DashedLine,
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

from engine.graph_matrix_encoding import GraphMatrixEncoding
from engine.simple_undirected_graph import triangle_with_tail_graph


class GraphMatrixEncodingPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Adjacency and Degree Matrices: From Picture to Array"

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
            r"\textbf{Adjacency and Degree Matrices: From Picture to Array}",
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

    def construct(self):
        model = GraphMatrixEncoding()
        expected_a = np.array(self._adjacency_entries(), dtype=int)
        if not np.array_equal(model.adjacency_matrix(), expected_a):
            raise RuntimeError("unexpected adjacency matrix")
        if not np.array_equal(model.degree_vector(), [2, 2, 3, 1]):
            raise RuntimeError("unexpected graph degrees")
        if not np.array_equal(model.neighbor_sums([1, 2, 3, 4]), [5, 4, 7, 3]):
            raise RuntimeError("unexpected neighbor sums")

        banner, title, heading = self._chrome(
            "Can zeros and ones store exactly the same connections as the picture?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        graph, positions, edges, dots, _ = self._graph(shift=LEFT * 2.45 + DOWN * 0.14)
        direct = self._card("DIRECT EDGE", r"1", "vertices 1 and 3", TEAL_C, width=3.55)
        absent = self._card("NO DIRECT EDGE", r"0", "vertices 1 and 4", ORANGE, width=3.55)
        code = VGroup(direct, absent).arrange(DOWN, buff=0.42).to_edge(RIGHT, buff=0.72).shift(DOWN * 0.05)
        missing = DashedLine(
            positions[1], positions[4], color=ORANGE, stroke_width=3.0, dash_length=0.15
        ).set_opacity(0.58)
        self.play(FadeIn(graph))
        self.play(edges[(1, 3)].animate.set_color(TEAL_C).set_stroke(width=6), FadeIn(direct))
        self.play(FadeIn(missing), FadeIn(absent))
        self.wait(2.8)

        heading = self._replace_heading(
            heading, "Choose one vertex order and use it for both the rows and the columns."
        )
        self.play(FadeOut(graph), FadeOut(code), FadeOut(missing))
        ordering = VGroup(
            Text("VERTEX ORDER", font_size=25, color=YELLOW, weight="BOLD"),
            MathTex(r"1,\ 2,\ 3,\ 4", font_size=51, color=WHITE),
            VGroup(
                self._card("ROWS", r"1,2,3,4", "starting vertex", TEAL_C, width=3.5),
                self._card("COLUMNS", r"1,2,3,4", "ending vertex", ORANGE, width=3.5),
            ).arrange(RIGHT, buff=0.62),
            Text(
                "Changing the order changes the array, but not the graph.",
                font_size=27,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.05)
        self.play(FadeIn(ordering[0]), FadeIn(ordering[1]))
        self.play(FadeIn(ordering[2]))
        self.play(FadeIn(ordering[3]))
        self.wait(2.8)

        heading = self._replace_heading(
            heading, "The entry in row i, column j is one for adjacent vertices, and zero otherwise."
        )
        self.play(FadeOut(ordering))
        graph, _, edges, dots, _ = self._graph(shift=LEFT * 2.70 + DOWN * 0.05)
        adjacency = self._matrix(self._adjacency_entries(), scale=0.67, h_buff=0.80, v_buff=0.68)
        adjacency.move_to(RIGHT * 2.65 + DOWN * 0.38)
        matrix_label = MathTex(r"A=", font_size=42, color=YELLOW).next_to(
            adjacency, LEFT, buff=0.15
        )
        entry_rule = MathTex(
            r"a_{ij}=\begin{cases}1&\text{if }i\text{ and }j\text{ share an edge},\\"
            r"0&\text{otherwise,}\end{cases}",
            font_size=29,
            color=WHITE,
        ).move_to(RIGHT * 2.65 + UP * 1.37)
        row_labels = VGroup(
            *[
                MathTex(rf"v_{vertex}", font_size=30, color=ORANGE).next_to(
                    row, RIGHT, buff=0.28
                )
                for vertex, row in zip(model.vertex_order, adjacency.get_rows())
            ]
        )
        row_note = Text(
            "Each labeled row records one vertex's neighbors.",
            font_size=24,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.37).shift(RIGHT * 2.15)
        row_build = VGroup(matrix_label, adjacency, entry_rule, row_labels, row_note)
        self.play(FadeIn(graph), FadeIn(entry_rule))
        self.play(FadeIn(matrix_label), FadeIn(adjacency.get_brackets()))
        for vertex, row, row_label in zip(
            model.vertex_order,
            adjacency.get_rows(),
            row_labels,
        ):
            incident_edges = [edge for edge in model.graph.edges if vertex in edge]
            neighbors = model.graph.neighbors(vertex)
            self.play(
                FadeIn(row_label),
                dots[vertex].animate.set_color(ORANGE).scale(1.16),
                *[dots[neighbor].animate.set_color(TEAL_C) for neighbor in neighbors],
                run_time=0.45,
            )
            self.play(
                *[
                    ShowPassingFlash(
                        edges[edge].copy().set_color(ORANGE).set_stroke(width=8.0),
                        time_width=0.70,
                    )
                    for edge in incident_edges
                ],
                run_time=0.80,
            )
            self.wait(0.30)
            self.play(FadeIn(row), run_time=0.52)
            self.wait(0.40)
            self.play(
                dots[vertex].animate.set_color(YELLOW).scale(1 / 1.16),
                *[dots[neighbor].animate.set_color(YELLOW) for neighbor in neighbors],
                run_time=0.30,
            )
        self.play(FadeIn(row_note))
        self.wait(2.6)

        heading = self._replace_heading(
            heading, "Each row is a zero-one description of one vertex's neighbors."
        )
        self.play(FadeOut(graph), FadeOut(row_build))
        adjacency = self._matrix(self._adjacency_entries(), scale=0.79, h_buff=0.88, v_buff=0.72)
        row_three = adjacency.get_rows()[2]
        completed = VGroup(
            VGroup(MathTex(r"A=", font_size=47, color=YELLOW), adjacency).arrange(RIGHT, buff=0.16),
            MathTex(r"\text{row 3}=[\,1\quad1\quad0\quad1\,]", font_size=39, color=TEAL_C),
            Text("Vertex 3 neighbors vertices 1, 2, and 4.", font_size=27, color=WHITE),
        ).arrange(DOWN, buff=0.40).move_to(DOWN * 0.03)
        row_box = SurroundingRectangle(row_three, color=TEAL_C, buff=0.10, stroke_width=2.5)
        self.play(FadeIn(completed[0]))
        self.play(FadeIn(row_box), FadeIn(completed[1]))
        self.play(FadeIn(completed[2]))
        self.wait(3.0)

        heading = self._replace_heading(
            heading, "An undirected simple graph makes A symmetric with zeros on its diagonal."
        )
        self.play(FadeOut(completed), FadeOut(row_box))
        adjacency = self._matrix(self._adjacency_entries(), scale=0.78, h_buff=0.88, v_buff=0.72)
        entries = list(adjacency.get_entries())
        for index in (0, 5, 10, 15):
            entries[index].set_color(ORANGE)
        for index, value in enumerate(expected_a.flat):
            if value == 1:
                entries[index].set_color(TEAL_C)
        structure = VGroup(
            VGroup(MathTex(r"A=", font_size=45, color=YELLOW), adjacency).arrange(RIGHT, buff=0.15),
            VGroup(
                self._card("UNDIRECTED", r"a_{ij}=a_{ji}", "paired entries match", TEAL_C, width=4.1),
                self._card("NO LOOPS", r"a_{ii}=0", "diagonal entries vanish", ORANGE, width=4.1),
            ).arrange(DOWN, buff=0.38),
        ).arrange(RIGHT, buff=1.00).move_to(DOWN * 0.02)
        self.play(FadeIn(structure[0]))
        self.play(FadeIn(structure[1][0]))
        self.play(FadeIn(structure[1][1]))
        self.wait(3.1)

        heading = self._replace_heading(
            heading, "Adding the entries in row i gives the degree of vertex i."
        )
        self.play(FadeOut(structure))
        adjacency = self._matrix(self._adjacency_entries(), scale=0.68, h_buff=0.82, v_buff=0.68)
        row_sums = VGroup(
            MathTex(r"0+1+1+0=2", font_size=31, color=TEAL_C),
            MathTex(r"1+0+1+0=2", font_size=31, color=TEAL_C),
            MathTex(r"1+1+0+1=3", font_size=31, color=ORANGE),
            MathTex(r"0+0+1+0=1", font_size=31, color=GREEN_C),
        ).arrange(DOWN, buff=0.28)
        degrees = self._matrix([["2"], ["2"], ["3"], ["1"]], scale=0.72, v_buff=0.76)
        degree_count = VGroup(
            VGroup(MathTex(r"A=", font_size=42, color=YELLOW), adjacency).arrange(RIGHT, buff=0.13),
            row_sums,
            VGroup(MathTex(r"\mathbf d=", font_size=40, color=YELLOW), degrees).arrange(RIGHT, buff=0.13),
        ).arrange(RIGHT, buff=0.82).move_to(DOWN * 0.03)
        self.play(FadeIn(degree_count[0]))
        for row, equation in zip(adjacency.get_rows(), row_sums):
            box = SurroundingRectangle(row, color=equation.color, buff=0.08, stroke_width=2.1)
            self.play(FadeIn(box), FadeIn(equation), run_time=0.48)
            self.play(FadeOut(box), run_time=0.20)
        self.play(FadeIn(degree_count[2]))
        self.wait(3.0)

        heading = self._replace_heading(
            heading, "The degree matrix places those four degrees on its diagonal."
        )
        self.play(FadeOut(degree_count))
        degree_matrix = self._matrix(
            [["2", "0", "0", "0"], ["0", "2", "0", "0"], ["0", "0", "3", "0"], ["0", "0", "0", "1"]],
            scale=0.77,
            h_buff=0.88,
            v_buff=0.72,
        )
        ones = self._matrix([["1"], ["1"], ["1"], ["1"]], scale=0.64, v_buff=0.70)
        degree_vector = self._matrix([["2"], ["2"], ["3"], ["1"]], scale=0.64, v_buff=0.70)
        ones_label = VGroup(
            MathTex(r"\mathbf 1=", font_size=38, color=YELLOW),
            ones,
        ).arrange(RIGHT, buff=0.12)
        degree_result = VGroup(
            MathTex(r"A\mathbf 1=", font_size=38, color=GREEN_C),
            degree_vector,
            MathTex(r"=\mathbf d=D\mathbf 1", font_size=38, color=GREEN_C),
        ).arrange(RIGHT, buff=0.16)
        degree_display = VGroup(
            VGroup(MathTex(r"D=", font_size=44, color=YELLOW), degree_matrix).arrange(RIGHT, buff=0.14),
            Text("Multiplying by the all-ones vector adds each row.", font_size=27, color=WHITE),
            VGroup(ones_label, degree_result).arrange(RIGHT, buff=0.50),
            Text("One equation now packages all four row sums.", font_size=27, color=WHITE),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 0.50)
        self.play(FadeIn(degree_display[0]))
        self.play(FadeIn(degree_display[1]))
        self.play(FadeIn(ones_label))
        self.play(FadeIn(degree_result), FadeIn(degree_display[3]))
        self.wait(3.2)

        heading = self._replace_heading(
            heading, "For any vertex values x, the product A times x adds neighboring values."
        )
        self.play(FadeOut(degree_display))
        graph, _, _, _, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.12)
        value_labels = VGroup(
            MathTex(r"x_1=1", font_size=28, color=TEAL_C).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"x_2=2", font_size=28, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"x_3=3", font_size=28, color=ORANGE).next_to(labels[3], UP, buff=0.25),
            MathTex(r"x_4=4", font_size=28, color=GREEN_C).next_to(labels[4], RIGHT, buff=0.22),
        )
        adjacency = self._matrix(self._adjacency_entries(), scale=0.48, h_buff=0.72, v_buff=0.62)
        x_vector = self._matrix([["1"], ["2"], ["3"], ["4"]], scale=0.55, v_buff=0.66)
        result = self._matrix([["5"], ["4"], ["7"], ["3"]], scale=0.55, v_buff=0.66)
        multiplication = VGroup(
            adjacency,
            x_vector,
            MathTex(r"=", font_size=39, color=YELLOW),
            result,
        ).arrange(RIGHT, buff=0.20).to_edge(RIGHT, buff=0.38).shift(DOWN * 0.02)
        product_note = MathTex(
            r"(A\mathbf x)_1=x_2+x_3=2+3=5",
            font_size=35,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.74).shift(RIGHT * 2.25)
        self.play(FadeIn(graph), FadeIn(value_labels))
        self.play(FadeIn(adjacency), FadeIn(x_vector))
        self.play(FadeIn(multiplication[2]), FadeIn(result), FadeIn(product_note))
        self.wait(3.5)

        heading = self._replace_heading(
            heading, "The picture and the matrices are different views of the same relationships."
        )
        self.play(FadeOut(graph), FadeOut(value_labels), FadeOut(multiplication), FadeOut(product_note))
        summary = VGroup(
            self._card("ADJACENCY\nMATRIX", r"A", "which vertices are neighbors", TEAL_C, width=3.55),
            self._card("DEGREE\nMATRIX", r"D", "how many neighbors each has", ORANGE, width=3.55),
            self._card("MATRIX\nACTION", r"A\mathbf x", "add neighboring values", GREEN_C, width=3.55),
        ).arrange(RIGHT, buff=0.35).move_to(UP * 0.15)
        next_question = Text(
            "What can repeated multiplication by A reveal?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(summary))
        self.play(FadeIn(next_question))
        self.wait(3.6)
