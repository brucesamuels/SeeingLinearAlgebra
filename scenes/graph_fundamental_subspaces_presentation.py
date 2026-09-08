"""Manim presentation: fundamental subspaces of graph incidence matrices."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow, BLACK, Circle, Create, DOWN, Dot, FadeIn, FadeOut, GREEN_C,
    GREY_B, LEFT, Line, MathTex, Matrix, ORANGE, RIGHT, Scene,
    ShowPassingFlash, SurroundingRectangle, TEAL_C, Tex, Text, UP, VGroup,
    WHITE, YELLOW,
)

from engine.graph_fundamental_subspaces import GraphFundamentalSubspaces


class GraphFundamentalSubspacesPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "The Fundamental Subspaces of a Graph"
    BASE_POSITIONS = {
        1: LEFT * 1.25 + UP * 0.95,
        2: LEFT * 1.25 + DOWN * 0.95,
        3: RIGHT * 0.85,
        4: RIGHT * 2.65,
    }
    EDGES = ((1, 2), (2, 3), (1, 3), (3, 4))

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
            r"\textbf{The Fundamental Subspaces of a Graph}",
            font_size=32,
            color=YELLOW,
        ).next_to(banner, DOWN, buff=0.11)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(FadeOut(old), run_time=0.25)
        self.play(FadeIn(new), run_time=0.30)
        return new

    @staticmethod
    def _matrix(entries, scale=0.67, h_buff=0.78, v_buff=0.67):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _card(label, formula, note, color, width=4.25, formula_size=35):
        body = VGroup(
            Text(label, font_size=22, color=color, weight="BOLD"),
            MathTex(formula, font_size=formula_size, color=WHITE),
            Text(note, font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.15)
        if body.width > width - 0.34:
            body.scale_to_fit_width(width - 0.34)
        return VGroup(SurroundingRectangle(body, color=color, buff=0.18, stroke_width=2), body)

    @staticmethod
    def _text_card(label, lines, color, width=4.25):
        body = VGroup(
            Text(label, font_size=22, color=color, weight="BOLD"),
            *[Text(line, font_size=20, color=WHITE if index == 0 else GREY_B) for index, line in enumerate(lines)],
        ).arrange(DOWN, buff=0.15)
        if body.width > width - 0.34:
            body.scale_to_fit_width(width - 0.34)
        return VGroup(SurroundingRectangle(body, color=color, buff=0.18, stroke_width=2), body)

    @classmethod
    def _graph(cls, shift=LEFT * 3.25 + DOWN * 0.08, removed_edge=None):
        positions = {vertex: point + shift for vertex, point in cls.BASE_POSITIONS.items()}
        visible_edges = tuple(edge for edge in cls.EDGES if frozenset(edge) != frozenset(removed_edge or ()))
        lines = {
            edge: Line(positions[edge[0]], positions[edge[1]], color=GREY_B, stroke_width=3.2)
            for edge in visible_edges
        }
        dots = {
            vertex: Dot(positions[vertex], radius=0.18, color=YELLOW).set_z_index(3)
            for vertex in (1, 2, 3, 4)
        }
        labels = {
            vertex: MathTex(str(vertex), font_size=29, color=BLACK).move_to(positions[vertex]).set_z_index(5)
            for vertex in (1, 2, 3, 4)
        }
        return VGroup(*lines.values(), *dots.values(), *labels.values()), positions, lines, dots

    @classmethod
    def _oriented_graph(cls, shift=LEFT * 3.25 + DOWN * 0.08):
        positions = {vertex: point + shift for vertex, point in cls.BASE_POSITIONS.items()}
        arrows = {
            edge: Arrow(positions[edge[0]], positions[edge[1]], buff=0.23, color=GREY_B, stroke_width=4.0)
            for edge in cls.EDGES
        }
        dots = VGroup(*[
            Dot(positions[vertex], radius=0.18, color=YELLOW).set_z_index(3)
            for vertex in (1, 2, 3, 4)
        ])
        labels = VGroup(*[
            MathTex(str(vertex), font_size=29, color=BLACK).move_to(positions[vertex]).set_z_index(5)
            for vertex in (1, 2, 3, 4)
        ])
        return VGroup(*arrows.values(), dots, labels), positions, arrows

    def construct(self):
        model = GraphFundamentalSubspaces()
        split = GraphFundamentalSubspaces.without_edge((3, 4))
        tree = GraphFundamentalSubspaces.without_edge((1, 3))
        if (model.rank, model.nullity, model.left_nullity) != (3, 1, 1):
            raise RuntimeError("unexpected incidence dimensions")
        if (split.component_count, split.nullity, split.left_nullity) != (2, 2, 1):
            raise RuntimeError("unexpected bridge deletion")
        if (tree.component_count, tree.nullity, tree.left_nullity) != (1, 1, 0):
            raise RuntimeError("unexpected cycle deletion")
        if not np.allclose(model.edge_differences([1, 2, 3, 4]), [1, 1, 2, 1]):
            raise RuntimeError("unexpected edge differences")
        if not np.allclose(model.vertex_accumulation(model.cycle_flow()), np.zeros(4)):
            raise RuntimeError("unexpected cycle circulation")
        if not model.laplacian_output_is_reachable([-1, 0, 0, 1]):
            raise RuntimeError("unexpected Laplacian reachability")

        banner, title, heading = self._chrome(
            "For an incidence matrix, the four subspaces describe vertex structure and edge structure."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: place all four subspaces around the incidence map.
        vertex_side = VGroup(
            Text("VERTEX SPACE  Rᵛ", font_size=24, color=YELLOW, weight="BOLD"),
            self._card("ROW SPACE", r"\operatorname{Row}(B)", "balanced vertex contrasts", TEAL_C, 4.15, 31),
            self._card("NULL SPACE", r"\operatorname{Null}(B)", "values constant on components", ORANGE, 4.15, 31),
        ).arrange(DOWN, buff=0.27)
        edge_side = VGroup(
            Text("EDGE SPACE  Rᵉ", font_size=24, color=YELLOW, weight="BOLD"),
            self._card("COLUMN SPACE", r"\operatorname{Col}(B)", "compatible edge differences", GREEN_C, 4.15, 31),
            self._card("LEFT NULL SPACE", r"\operatorname{Null}(B^T)", "circulations around cycles", YELLOW, 4.15, 31),
        ).arrange(DOWN, buff=0.27)
        map_arrow = VGroup(
            Arrow(LEFT, RIGHT, color=WHITE, stroke_width=4),
            MathTex(r"B", font_size=42, color=YELLOW),
            Text("take edge differences", font_size=18, color=GREY_B),
        ).arrange(DOWN, buff=0.08)
        master = VGroup(vertex_side, map_arrow, edge_side).arrange(RIGHT, buff=0.44).move_to(DOWN * 0.12)
        self.play(FadeIn(vertex_side), Create(map_arrow[0]), FadeIn(map_arrow[1:]), FadeIn(edge_side))
        self.wait(4.0)

        # Card 2: Null(B) records constants on connected components.
        heading = self._replace_heading(heading, "Null(B) consists of vertex values that produce zero difference on every edge.")
        self.play(FadeOut(master))
        graph, positions, lines, _ = self._graph()
        value_labels = VGroup(*[
            MathTex("a", font_size=32, color=ORANGE).next_to(positions[vertex], UP, buff=0.32)
            for vertex in (1, 2, 3, 4)
        ])
        null_panel = VGroup(
            MathTex(r"B(a,a,a,a)^T=0", font_size=43, color=ORANGE),
            MathTex(r"\operatorname{Null}(B)=\operatorname{span}\{\mathbf1\}", font_size=42, color=YELLOW),
            Text("Equality propagates along paths, so a connected graph has one constant.", font_size=22, color=WHITE),
            self._card("GRAPH PROPERTY", r"\dim\operatorname{Null}(B)=1", "one connected component", GREEN_C, 5.25, 33),
        ).arrange(DOWN, buff=0.33).to_edge(RIGHT, buff=0.28)
        null_panel[2].scale_to_fit_width(5.25)
        self.play(FadeIn(graph), FadeIn(value_labels))
        self.play(*[ShowPassingFlash(line.copy().set_color(ORANGE).set_stroke(width=7)) for line in lines.values()])
        self.play(FadeIn(null_panel))
        self.wait(4.0)

        # Card 3: deleting a bridge increases the null space.
        heading = self._replace_heading(heading, "Deleting the bridge creates a second independent component constant.")
        self.play(FadeOut(graph), FadeOut(value_labels), FadeOut(null_panel))
        split_graph, split_positions, _, _ = self._graph(removed_edge=(3, 4))
        split_values = VGroup(
            *[MathTex("a", font_size=32, color=TEAL_C).next_to(split_positions[v], UP, buff=0.32) for v in (1, 2, 3)],
            MathTex("b", font_size=32, color=ORANGE).next_to(split_positions[4], UP, buff=0.32),
        )
        split_panel = VGroup(
            MathTex(r"x=(a,a,a,b)^T", font_size=42, color=WHITE),
            MathTex(r"\operatorname{Null}(B_{\rm split})=\operatorname{span}\left\{(1,1,1,0)^T,(0,0,0,1)^T\right\}", font_size=34, color=YELLOW),
            self._card("COMPONENT THEOREM", r"\dim\operatorname{Null}(B)=c", "one basis direction per component", GREEN_C, 5.45, 34),
        ).arrange(DOWN, buff=0.36).to_edge(RIGHT, buff=0.25)
        split_panel[1].scale_to_fit_width(5.55)
        self.play(FadeIn(split_graph), FadeIn(split_values))
        self.play(FadeIn(split_panel))
        self.wait(4.0)

        # Card 4: Row(B) is the balanced vertex contrast space.
        heading = self._replace_heading(heading, "Row(B) contains the vertex contrasts that remain after constants are removed.")
        self.play(FadeOut(split_graph), FadeOut(split_values), FadeOut(split_panel))
        rows = VGroup(
            self._matrix([["-1"], ["1"], ["0"], ["0"]], scale=0.54, v_buff=0.66),
            self._matrix([["0"], ["-1"], ["1"], ["0"]], scale=0.54, v_buff=0.66),
            self._matrix([["0"], ["0"], ["-1"], ["1"]], scale=0.54, v_buff=0.66),
        ).arrange(RIGHT, buff=0.42)
        row_left = VGroup(
            Text("THREE INDEPENDENT EDGE CONTRASTS", font_size=21, color=TEAL_C, weight="BOLD"),
            rows,
        ).arrange(DOWN, buff=0.30).move_to(LEFT * 2.70 + DOWN * 0.03)
        row_panel = VGroup(
            MathTex(r"\operatorname{Row}(B)=\operatorname{Null}(B)^\perp", font_size=41, color=YELLOW),
            MathTex(r"=\{z\in\mathbb R^4:\mathbf1^Tz=0\}", font_size=41, color=GREEN_C),
            self._card("BALANCED", r"z_1+z_2+z_3+z_4=0", "positive and negative contrasts cancel", TEAL_C, 5.05, 32),
            Text("The row space has dimension three because one constant direction is invisible.", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.32).to_edge(RIGHT, buff=0.31)
        row_panel[3].scale_to_fit_width(5.15)
        self.play(FadeIn(row_left), FadeIn(row_panel))
        self.wait(4.0)

        # Card 5: Col(B) is the space of compatible edge differences.
        heading = self._replace_heading(heading, "Col(B) contains exactly the edge differences that can come from vertex values.")
        self.play(FadeOut(row_left), FadeOut(row_panel))
        oriented, _, arrows = self._oriented_graph()
        difference_labels = VGroup(
            MathTex("1", font_size=27, color=GREEN_C).next_to(arrows[(1, 2)], LEFT, buff=0.12),
            MathTex("1", font_size=27, color=GREEN_C).next_to(arrows[(2, 3)], DOWN, buff=0.12),
            MathTex("2", font_size=27, color=GREEN_C).next_to(arrows[(1, 3)], UP, buff=0.10),
            MathTex("1", font_size=27, color=GREEN_C).next_to(arrows[(3, 4)], UP, buff=0.10),
        )
        column_panel = VGroup(
            MathTex(r"x=(1,2,3,4)^T", font_size=37, color=WHITE),
            MathTex(r"Bx=(1,1,2,1)^T\in\operatorname{Col}(B)", font_size=39, color=GREEN_C),
            MathTex(r"(x_2-x_1)+(x_3-x_2)-(x_3-x_1)=0", font_size=34, color=TEAL_C),
            self._card("CYCLE CONSISTENCY", r"y_1+y_2-y_3=0", "differences around the triangle must close", YELLOW, 5.25, 33),
        ).arrange(DOWN, buff=0.32).to_edge(RIGHT, buff=0.27)
        self.play(FadeIn(oriented), FadeIn(difference_labels))
        self.play(FadeIn(column_panel))
        self.wait(4.1)

        # Card 6: Null(B^T) is cycle circulation.
        heading = self._replace_heading(heading, "Null(Bᵀ) contains edge flows that circulate without accumulating at a vertex.")
        self.play(FadeOut(oriented), FadeOut(difference_labels), FadeOut(column_panel))
        graph, positions, _, _ = self._graph()
        cycle_arrows = VGroup(
            Arrow(positions[1], positions[2], buff=0.23, color=TEAL_C, stroke_width=5),
            Arrow(positions[2], positions[3], buff=0.23, color=TEAL_C, stroke_width=5),
            Arrow(positions[3], positions[1], buff=0.23, color=TEAL_C, stroke_width=5),
        )
        cycle_labels = VGroup(
            MathTex("1", font_size=26, color=TEAL_C).next_to(cycle_arrows[0], LEFT, buff=0.12),
            MathTex("1", font_size=26, color=TEAL_C).next_to(cycle_arrows[1], DOWN, buff=0.12),
            MathTex("1", font_size=26, color=TEAL_C).next_to(cycle_arrows[2], UP, buff=0.12),
        )
        cycle_panel = VGroup(
            MathTex(r"q=(1,1,-1,0)^T", font_size=42, color=TEAL_C),
            MathTex(r"B^Tq=0", font_size=47, color=YELLOW),
            Text("At every vertex, incoming cycle flow equals outgoing cycle flow.", font_size=22, color=WHITE),
            self._card("CYCLE SPACE", r"\operatorname{Null}(B^T)=\operatorname{span}\{q\}", "one independent circulation", GREEN_C, 5.25, 31),
        ).arrange(DOWN, buff=0.34).to_edge(RIGHT, buff=0.28)
        cycle_panel[2].scale_to_fit_width(5.20)
        self.play(FadeIn(graph))
        self.play(*[Create(arrow) for arrow in cycle_arrows], FadeIn(cycle_labels))
        self.play(FadeIn(cycle_panel))
        self.wait(4.1)

        # Card 7: rank and nullities count graph structure.
        heading = self._replace_heading(heading, "The dimensions of the incidence subspaces count components and independent cycles.")
        self.play(FadeOut(graph), FadeOut(cycle_arrows), FadeOut(cycle_labels), FadeOut(cycle_panel))
        formulas = VGroup(
            MathTex(r"\operatorname{rank}(B)=n-c", font_size=44, color=YELLOW),
            MathTex(r"\dim\operatorname{Null}(B)=c", font_size=42, color=ORANGE),
            MathTex(r"\dim\operatorname{Null}(B^T)=m-n+c", font_size=42, color=TEAL_C),
        ).arrange(DOWN, buff=0.30).move_to(LEFT * 3.05 + DOWN * 0.02)
        comparisons = VGroup(
            self._text_card("TRIANGLE WITH TAIL", ("n=4, m=4, c=1", "one component; one cycle"), GREEN_C, 4.85),
            self._text_card("DELETE THE BRIDGE", ("n=4, m=3, c=2", "two components; one cycle"), ORANGE, 4.85),
            self._text_card("DELETE A TRIANGLE EDGE", ("n=4, m=3, c=1", "one component; no cycle"), TEAL_C, 4.85),
        ).arrange(DOWN, buff=0.28).to_edge(RIGHT, buff=0.38)
        self.play(FadeIn(formulas))
        self.play(FadeIn(comparisons))
        self.wait(4.2)

        # Card 8: both ambient spaces split into structural parts.
        heading = self._replace_heading(heading, "The four subspaces separate constants from contrasts and gradients from circulation.")
        self.play(FadeOut(formulas), FadeOut(comparisons))
        vertex_split = VGroup(
            Text("VERTEX DATA", font_size=23, color=YELLOW, weight="BOLD"),
            MathTex(r"\mathbb R^V=\operatorname{Row}(B)\oplus\operatorname{Null}(B)", font_size=38, color=WHITE),
            self._card("CONTRASTS", r"\mathbf1^Tz=0", "detected across edges", TEAL_C, 4.65, 33),
            self._card("COMPONENT CONSTANTS", r"Bz=0", "invisible across edges", ORANGE, 4.65, 33),
        ).arrange(DOWN, buff=0.26)
        edge_split = VGroup(
            Text("EDGE DATA", font_size=23, color=YELLOW, weight="BOLD"),
            MathTex(r"\mathbb R^E=\operatorname{Col}(B)\oplus\operatorname{Null}(B^T)", font_size=36, color=WHITE),
            self._card("GRADIENTS", r"y=Bx", "compatible potential differences", GREEN_C, 4.65, 33),
            self._card("CIRCULATIONS", r"B^Ty=0", "closed cycle flows", YELLOW, 4.65, 33),
        ).arrange(DOWN, buff=0.26)
        splits = VGroup(vertex_split, edge_split).arrange(RIGHT, buff=0.50).move_to(DOWN * 0.03)
        self.play(FadeIn(vertex_split))
        self.play(FadeIn(edge_split))
        self.wait(4.2)

        # Card 9: L inherits the vertex-side incidence spaces.
        heading = self._replace_heading(heading, "The Laplacian inherits its zero space and active space from the incidence matrix.")
        self.play(FadeOut(splits))
        laplacian = VGroup(
            MathTex(r"L=B^TB=L^T", font_size=49, color=YELLOW),
            VGroup(
                self._card("ZERO SPACE", r"\operatorname{Null}(L)=\operatorname{Null}(B)", "constants on components", ORANGE, 5.10, 31),
                self._card("ACTIVE SPACE", r"\operatorname{Col}(L)=\operatorname{Row}(B)", "balanced vertex contrasts", TEAL_C, 5.10, 31),
            ).arrange(RIGHT, buff=0.45),
            MathTex(r"\operatorname{Null}(L)=\operatorname{span}\{\mathbf1\},\qquad \operatorname{Col}(L)=\mathbf1^\perp", font_size=40, color=GREEN_C),
            Text("Symmetry makes the Laplacian's row and column spaces coincide.", font_size=23, color=WHITE),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.02)
        self.play(FadeIn(laplacian[0]))
        self.play(FadeIn(laplacian[1]))
        self.play(FadeIn(laplacian[2:]))
        self.wait(4.2)

        # Card 10: subspaces explain Laplacian solvability and ambiguity.
        heading = self._replace_heading(heading, "Graph subspaces tell us which Laplacian systems are solvable and why solutions are not unique.")
        self.play(FadeOut(laplacian))
        conclusion = VGroup(
            VGroup(
                self._card("SOLVABILITY", r"Lv=b\iff\mathbf1^Tb=0", "total injection must balance", GREEN_C, 5.10, 34),
                self._card("NONUNIQUENESS", r"v\mapsto v+c\mathbf1", "constant shifts change no edge difference", ORANGE, 5.10, 34),
            ).arrange(RIGHT, buff=0.45),
            VGroup(
                self._card("COMPONENTS", r"\operatorname{Null}(B)", "one constant per component", TEAL_C, 3.45, 30),
                self._card("EDGE DIFFERENCES", r"\operatorname{Col}(B)", "cycle-consistent gradients", GREEN_C, 3.45, 30),
                self._card("CYCLES", r"\operatorname{Null}(B^T)", "conserved circulations", YELLOW, 3.45, 30),
            ).arrange(RIGHT, buff=0.28),
            Text("The fundamental subspaces turn graph structure into linear-algebraic structure.", font_size=25, color=YELLOW),
            Text("Next: assemble the graph, energy, spectrum, flow, and probability viewpoints.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.04)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2:]))
        self.wait(4.4)
        self.play(*[FadeOut(mobject) for mobject in self.mobjects])
