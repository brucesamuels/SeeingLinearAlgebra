"""Manim presentation: Laplacian energy as total squared edge variation."""

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

from engine.graph_laplacian_energy import GraphLaplacianEnergy
from engine.simple_undirected_graph import triangle_with_tail_graph


class GraphLaplacianEnergyPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Laplacian Energy: Variation Across Edges"

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
            r"\textbf{Laplacian Energy: Variation Across Edges}",
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

    @staticmethod
    def _l_entries():
        return [["2", "-1", "-1", "0"], ["-1", "2", "-1", "0"], ["-1", "-1", "3", "-1"], ["0", "0", "-1", "1"]]

    def construct(self):
        model = GraphLaplacianEnergy()
        if model.energy_identity([1, 2, 3, 4]) != (7.0, 7.0, 7.0):
            raise RuntimeError("unexpected Laplacian energy")
        if not np.array_equal(model.edge_contributions([1, 2, 3, 4]), [1, 1, 4, 1]):
            raise RuntimeError("unexpected edge energy contributions")
        if model.with_reversed_edge(3).quadratic_energy([1, 2, 3, 4]) != 7:
            raise RuntimeError("energy should not depend on orientation")

        banner, title, heading = self._chrome(
            "Lx gives one neighbor-comparison total at each vertex; can we combine them?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: recall the Laplacian action and ask for one global measure.
        graph, _, _, _, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.11)
        values = VGroup(
            MathTex(r"x_1=1", font_size=27, color=ORANGE).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"x_2=2", font_size=27, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"x_3=3", font_size=27, color=TEAL_C).next_to(labels[3], UP, buff=0.24),
            MathTex(r"x_4=4", font_size=27, color=GREEN_C).next_to(labels[4], RIGHT, buff=0.21),
        )
        local_totals = self._card(
            "LOCAL COMPARISONS",
            r"L\mathbf x=(-3,0,2,1)^T",
            "one output per vertex",
            TEAL_C,
            width=4.85,
        ).to_edge(RIGHT, buff=0.51).shift(UP * 0.34)
        question = Text(
            "We want one number for variation across the whole graph.",
            font_size=25,
            color=YELLOW,
        ).next_to(local_totals, DOWN, buff=0.56)
        question.scale_to_fit_width(4.85)
        self.play(FadeIn(graph), FadeIn(values), FadeIn(local_totals))
        self.play(FadeIn(question))
        self.wait(3.0)

        # Card 2: the quadratic form makes a scalar.
        heading = self._replace_heading(
            heading, "Pair the vertex values with their Laplacian outputs to obtain one scalar."
        )
        self.play(FadeOut(graph), FadeOut(values), FadeOut(local_totals), FadeOut(question))
        row_x = self._matrix([["1", "2", "3", "4"]], scale=0.60, h_buff=0.75, v_buff=0.62)
        laplacian = self._matrix(self._l_entries(), scale=0.50, h_buff=0.72, v_buff=0.62)
        column_x = self._matrix([["1"], ["2"], ["3"], ["4"]], scale=0.60, v_buff=0.66)
        quadratic = VGroup(
            MathTex(r"\mathbf x^TL\mathbf x=", font_size=39, color=YELLOW),
            row_x,
            laplacian,
            column_x,
            MathTex(r"=7", font_size=43, color=GREEN_C),
        ).arrange(RIGHT, buff=0.16).move_to(UP * 0.19)
        calculation = MathTex(
            r"\mathbf x^T(L\mathbf x)=(1,2,3,4)\cdot(-3,0,2,1)=7",
            font_size=34,
            color=WHITE,
        ).next_to(quadratic, DOWN, buff=0.50)
        scalar_note = Text(
            "This scalar is called the Laplacian energy of x.",
            font_size=26,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.62)
        self.play(FadeIn(quadratic[:-1]))
        self.play(FadeIn(quadratic[-1]), FadeIn(calculation))
        self.play(FadeIn(scalar_note))
        self.wait(3.2)

        # Card 3: factor the quadratic form through B.
        heading = self._replace_heading(
            heading, "Substitute L equals B-transpose B and regroup the factors."
        )
        self.play(FadeOut(quadratic), FadeOut(calculation), FadeOut(scalar_note))
        factorization = VGroup(
            MathTex(r"\mathbf x^TL\mathbf x", font_size=45, color=YELLOW),
            MathTex(r"=\mathbf x^TB^TB\mathbf x", font_size=43, color=WHITE),
            MathTex(r"=(B\mathbf x)^T(B\mathbf x)", font_size=43, color=TEAL_C),
            MathTex(r"=\lVert B\mathbf x\rVert^2", font_size=47, color=GREEN_C),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.02)
        interpretation = Text(
            "The energy is the squared length of the edge-difference vector.",
            font_size=26,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(factorization[0]))
        self.play(FadeIn(factorization[1]))
        self.play(FadeIn(factorization[2]))
        self.play(FadeIn(factorization[3]), FadeIn(interpretation))
        self.wait(3.2)

        # Card 4: compute the norm from the four familiar edge differences.
        heading = self._replace_heading(
            heading, "For our values, square each of the four edge differences and add."
        )
        self.play(FadeOut(factorization), FadeOut(interpretation))
        difference_vector = self._matrix([["1"], ["1"], ["2"], ["1"]], scale=0.76, v_buff=0.72)
        norm_work = VGroup(
            VGroup(
                MathTex(r"B\mathbf x=", font_size=43, color=YELLOW),
                difference_vector,
            ).arrange(RIGHT, buff=0.15),
            MathTex(r"\lVert B\mathbf x\rVert^2=1^2+1^2+2^2+1^2", font_size=42, color=WHITE),
            MathTex(r"=1+1+4+1=7", font_size=45, color=GREEN_C),
            Text("Squares keep every contribution nonnegative.", font_size=26, color=ORANGE),
        ).arrange(DOWN, buff=0.31).move_to(DOWN * 0.06)
        self.play(FadeIn(norm_work[0]))
        self.play(FadeIn(norm_work[1]))
        self.play(FadeIn(norm_work[2]), FadeIn(norm_work[3]))
        self.wait(3.1)

        # Card 5: attach each squared contribution to its graph edge.
        heading = self._replace_heading(
            heading, "Each squared difference belongs to one undirected edge."
        )
        self.play(FadeOut(norm_work))
        graph, positions, edges, _, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        values = VGroup(
            MathTex(r"1", font_size=27, color=ORANGE).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"2", font_size=27, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"3", font_size=27, color=TEAL_C).next_to(labels[3], UP, buff=0.24),
            MathTex(r"4", font_size=27, color=GREEN_C).next_to(labels[4], RIGHT, buff=0.21),
        )
        edge_terms = VGroup(
            MathTex(r"(1-2)^2=1", font_size=25, color=TEAL_C).move_to((positions[1] + positions[2]) / 2 + LEFT * 0.65),
            MathTex(r"(2-3)^2=1", font_size=25, color=TEAL_C).move_to((positions[2] + positions[3]) / 2 + DOWN * 0.43),
            MathTex(r"(1-3)^2=4", font_size=25, color=ORANGE).move_to((positions[1] + positions[3]) / 2 + UP * 0.43),
            MathTex(r"(3-4)^2=1", font_size=25, color=GREEN_C).move_to((positions[3] + positions[4]) / 2 + UP * 0.40),
        )
        total = self._card(
            "TOTAL EDGE VARIATION",
            r"1+1+4+1=7",
            "large jumps count more",
            YELLOW,
            width=4.35,
        ).to_edge(RIGHT, buff=0.58).shift(DOWN * 0.01)
        self.play(FadeIn(graph), FadeIn(values))
        colors = (TEAL_C, TEAL_C, ORANGE, GREEN_C)
        for edge, term, color in zip(edges.values(), edge_terms, colors):
            self.play(
                ShowPassingFlash(edge.copy().set_color(color).set_stroke(width=9.0)),
                FadeIn(term),
                run_time=0.72,
            )
        self.play(FadeIn(total))
        self.wait(3.0)

        # Card 6: state the general edge-sum identity.
        heading = self._replace_heading(
            heading, "For any vertex values, Laplacian energy is total squared edge variation."
        )
        self.play(FadeOut(graph), FadeOut(values), FadeOut(edge_terms), FadeOut(total))
        identity = VGroup(
            Text("LAPLACIAN ENERGY IDENTITY", font_size=25, color=YELLOW, weight="BOLD"),
            MathTex(
                r"\mathbf x^TL\mathbf x=\lVert B\mathbf x\rVert^2"
                r"=\sum_{\{i,j\}\in E}(x_i-x_j)^2",
                font_size=43,
                color=WHITE,
            ),
            Text("Each undirected edge is included exactly once.", font_size=25, color=TEAL_C),
            Text("Reverse an orientation: the difference changes sign, but its square does not.", font_size=24, color=GREEN_C),
        ).arrange(DOWN, buff=0.40).move_to(DOWN * 0.02)
        identity[3].scale_to_fit_width(10.5)
        self.play(FadeIn(identity[0]), FadeIn(identity[1]))
        self.play(FadeIn(identity[2]))
        self.play(FadeIn(identity[3]))
        self.wait(3.2)

        # Card 7: prove positive semidefiniteness from squares.
        heading = self._replace_heading(
            heading, "A sum of squares can never be negative, for any choice of x."
        )
        self.play(FadeOut(identity))
        psd = VGroup(
            self._card(
                "POSITIVE SEMIDEFINITE",
                r"\mathbf x^TM\mathbf x\ge0\ \text{for every }\mathbf x",
                "the defining quadratic-form test",
                TEAL_C,
                width=8.20,
            ),
            MathTex(r"\mathbf x^TL\mathbf x=\sum_{\{i,j\}\in E}(x_i-x_j)^2\ge0", font_size=43, color=WHITE),
            MathTex(r"\therefore\quad L\ \text{is positive semidefinite}", font_size=43, color=GREEN_C),
        ).arrange(DOWN, buff=0.44).move_to(DOWN * 0.03)
        self.play(FadeIn(psd[0]))
        self.play(FadeIn(psd[1]))
        self.play(FadeIn(psd[2]))
        self.wait(3.2)

        # Card 8: characterize zero energy on this connected graph.
        heading = self._replace_heading(
            heading, "On this connected graph, zero energy forces every vertex value to agree."
        )
        self.play(FadeOut(psd))
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.10)
        constant_labels = VGroup(
            *[
                MathTex(r"c", font_size=27, color=GREEN_C).next_to(label, direction, buff=0.22)
                for label, direction in zip(
                    labels.values(), (UP + LEFT, DOWN + LEFT, UP, RIGHT)
                )
            ]
        )
        zero_logic = VGroup(
            self._card("ENERGY ZERO", r"(x_i-x_j)^2=0", "on every edge", ORANGE, width=4.30),
            self._card("ENDPOINTS AGREE", r"x_i=x_j", "equality spreads along edges", TEAL_C, width=4.30),
            MathTex(r"\mathbf x=c\mathbf 1", font_size=45, color=GREEN_C),
        ).arrange(DOWN, buff=0.36).to_edge(RIGHT, buff=0.56).shift(DOWN * 0.01)
        self.play(FadeIn(graph), FadeIn(zero_logic[0]))
        self.play(
            *[edge.animate.set_color(TEAL_C).set_stroke(width=5.5) for edge in edges.values()],
            *[dot.animate.set_color(GREEN_C) for dot in dots.values()],
            FadeIn(zero_logic[1]),
        )
        self.play(FadeIn(constant_labels), FadeIn(zero_logic[2]))
        self.wait(3.2)

        # Card 9: synthesis and bridge to components/null space.
        heading = self._replace_heading(
            heading, "Energy connects graph variation, positive semidefiniteness, and constants."
        )
        self.play(FadeOut(graph), FadeOut(constant_labels), FadeOut(zero_logic))
        synthesis = VGroup(
            self._card("QUADRATIC", r"\mathbf x^TL\mathbf x", "one global scalar", TEAL_C, width=3.55),
            self._card("EDGE VIEW", r"\sum(x_i-x_j)^2", "total squared variation", ORANGE, width=3.55),
            self._card("ZERO ENERGY", r"\mathbf x=c\mathbf 1", "on this connected graph", GREEN_C, width=3.55),
        ).arrange(RIGHT, buff=0.35).move_to(UP * 0.40)
        distinction = Text(
            "Local cancellation can give (Lx)i = 0; energy zero requires every edge difference to vanish.",
            font_size=23,
            color=WHITE,
        ).move_to(DOWN * 1.05)
        distinction.scale_to_fit_width(11.0)
        next_question = Text(
            "What changes when the graph has more than one connected component?",
            font_size=25,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.39)
        self.play(FadeIn(synthesis))
        self.play(FadeIn(distinction))
        self.play(FadeIn(next_question))
        self.wait(3.4)
