"""Manim presentation: Graphs, Networks, and the Laplacian synthesis."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow, BLACK, Create, DOWN, Dot, FadeIn, FadeOut, GREEN_C, GREY_B,
    LEFT, Line, MathTex, Matrix, ORANGE, RIGHT, Scene, ShowPassingFlash,
    SurroundingRectangle, TEAL_C, Tex, Text, UP, VGroup, WHITE, YELLOW,
)

from engine.graph_chapter_synthesis import GraphChapterSynthesis


class GraphChapterSynthesisPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Graphs, Networks, and the Laplacian: The Big Picture"
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
        banner = Tex(r"\textbf{GRAPHS, NETWORKS, AND THE LAPLACIAN}", font_size=23, color=GREY_B).to_edge(UP, buff=0.16)
        title = Tex(r"\textbf{Graphs, Networks, and the Laplacian: The Big Picture}", font_size=31, color=YELLOW).next_to(banner, DOWN, buff=0.11)
        if title.width > 11.7:
            title.scale_to_fit_width(11.7)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(FadeOut(old), run_time=0.27)
        self.play(FadeIn(new), run_time=0.32)
        return new

    @staticmethod
    def _matrix(entries, scale=0.63, h_buff=0.72, v_buff=0.63):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _card(label, formula, note, color, width=4.2, formula_size=34):
        body = VGroup(
            Text(label, font_size=21, color=color, weight="BOLD"),
            MathTex(formula, font_size=formula_size, color=WHITE),
            Text(note, font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.14)
        if body.width > width - 0.34:
            body.scale_to_fit_width(width - 0.34)
        return VGroup(SurroundingRectangle(body, color=color, buff=0.17, stroke_width=2), body)

    @staticmethod
    def _text_card(label, lines, color, width=4.2):
        body = VGroup(
            Text(label, font_size=21, color=color, weight="BOLD"),
            *[Text(line, font_size=19, color=WHITE if index == 0 else GREY_B) for index, line in enumerate(lines)],
        ).arrange(DOWN, buff=0.14)
        if body.width > width - 0.34:
            body.scale_to_fit_width(width - 0.34)
        return VGroup(SurroundingRectangle(body, color=color, buff=0.17, stroke_width=2), body)

    @classmethod
    def _graph(cls, shift=LEFT * 3.25 + DOWN * 0.08, directed=False):
        positions = {vertex: point + shift for vertex, point in cls.BASE_POSITIONS.items()}
        lines = {}
        for edge in cls.EDGES:
            displayed_edge = (3, 1) if directed and edge == (1, 3) else edge
            lines[edge] = (
                Arrow(
                    positions[displayed_edge[0]],
                    positions[displayed_edge[1]],
                    buff=0.23,
                    color=GREY_B,
                    stroke_width=4,
                )
                if directed else Line(positions[edge[0]], positions[edge[1]], color=GREY_B, stroke_width=3.2)
            )
        dots = VGroup(*[Dot(positions[v], radius=0.18, color=YELLOW).set_z_index(3) for v in (1, 2, 3, 4)])
        labels = VGroup(*[MathTex(str(v), font_size=29, color=BLACK).move_to(positions[v]).set_z_index(5) for v in (1, 2, 3, 4)])
        return VGroup(*lines.values(), dots, labels), positions, lines

    def construct(self):
        model = GraphChapterSynthesis()
        if model.walks.walk_count(1, 4, 2) != 1:
            raise RuntimeError("unexpected walk count")
        if not np.allclose(model.edge_differences(), [1, 1, 2, 1]):
            raise RuntimeError("unexpected edge differences")
        if not np.allclose(model.laplacian_response(), [-3, 0, 2, 1]):
            raise RuntimeError("unexpected Laplacian response")
        if model.signal_energy() != 7:
            raise RuntimeError("unexpected Laplacian energy")
        if not np.allclose(model.spectrum_values(), [0, 1, 3, 4]):
            raise RuntimeError("unexpected Laplacian spectrum")
        if model.page_rank_order() != ((3,), (2,), (1, 4)):
            raise RuntimeError("unexpected PageRank order")

        banner, title, heading = self._chrome(
            "One graph can answer many questions—after we choose the representation that fits the question."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: one graph, several linear-algebraic lenses.
        graph, _, _ = self._graph(shift=LEFT * 4.40 + DOWN * 0.12)
        lenses = VGroup(
            self._card("CONNECTIONS", r"A", "who is adjacent?", TEAL_C, 3.05, 39),
            self._card("DIFFERENCES", r"B", "what changes across edges?", ORANGE, 3.05, 39),
            self._card("VARIATION", r"L=B^TB", "how does the graph respond?", GREEN_C, 3.05, 35),
            self._card("PROBABILITY", r"P\ \text{or}\ G", "how does mass move?", YELLOW, 3.05, 34),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.34, 0.34)).move_to(RIGHT * 2.10 + DOWN * 0.08)
        bridge = Arrow(LEFT, RIGHT, color=WHITE, stroke_width=4).move_to(LEFT * 0.45 + DOWN * 0.10)
        self.play(FadeIn(graph), Create(bridge), FadeIn(lenses))
        self.wait(4.0)

        # Card 2: adjacency stores edges and its powers count walks.
        heading = self._replace_heading(heading, "The adjacency matrix records direct connections; its powers count multi-step walks.")
        self.play(FadeOut(graph), FadeOut(bridge), FadeOut(lenses))
        graph, _, lines = self._graph()
        adjacency = self._matrix([["0", "1", "1", "0"], ["1", "0", "1", "0"], ["1", "1", "0", "1"], ["0", "0", "1", "0"]])
        adjacency_panel = VGroup(
            MathTex(r"A=", font_size=42, color=YELLOW), adjacency,
        ).arrange(RIGHT, buff=0.18)
        walk_panel = VGroup(
            MathTex(r"(A^2)_{14}=1", font_size=43, color=GREEN_C),
            Text("one length-two walk:  1–3–4", font_size=23, color=WHITE),
            self._card("QUESTION", r"(A^k)_{ij}", "walks of exactly k steps", TEAL_C, 4.75, 34),
        ).arrange(DOWN, buff=0.34)
        right = VGroup(adjacency_panel, walk_panel).arrange(DOWN, buff=0.36).to_edge(RIGHT, buff=0.45)
        self.play(FadeIn(graph), FadeIn(adjacency_panel))
        self.play(ShowPassingFlash(lines[(1, 3)].copy().set_color(GREEN_C).set_stroke(width=7)), ShowPassingFlash(lines[(3, 4)].copy().set_color(GREEN_C).set_stroke(width=7)))
        self.play(FadeIn(walk_panel))
        self.wait(4.0)

        # Card 3: incidence differences compose into the Laplacian.
        heading = self._replace_heading(heading, "The incidence matrix takes edge differences; the Laplacian returns them to vertices.")
        self.play(FadeOut(graph), FadeOut(right))
        flow = VGroup(
            self._card("VERTEX VALUES", r"x=(1,2,3,4)^T", "data on vertices", TEAL_C, 3.35, 30),
            MathTex(r"\xrightarrow{\ B\ }", font_size=36, color=WHITE),
            self._card("EDGE DIFFERENCES", r"Bx=(1,1,2,1)^T", "head minus tail", ORANGE, 3.45, 29),
            MathTex(r"\xrightarrow{\ B^T\ }", font_size=36, color=WHITE),
            self._card("VERTEX RESPONSE", r"Lx=(-3,0,2,1)^T", "neighbor comparisons", GREEN_C, 3.45, 29),
        ).arrange(RIGHT, buff=0.18)
        composition = VGroup(
            flow,
            MathTex(r"L=B^TB=D-A", font_size=50, color=YELLOW),
            Text("Temporary edge orientations disappear in the composition.", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.03)
        self.play(FadeIn(flow))
        self.play(FadeIn(composition[1:]))
        self.wait(4.1)

        # Card 4: energy and the fundamental subspaces expose structure.
        heading = self._replace_heading(heading, "Energy measures variation, while incidence subspaces identify components and cycles.")
        self.play(FadeOut(composition))
        energy = VGroup(
            MathTex(r"x^TLx=\|Bx\|^2=\sum_{\{i,j\}\in E}(x_i-x_j)^2=7", font_size=42, color=YELLOW),
            Text("A sum of squares makes every graph Laplacian positive semidefinite.", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.30)
        subspaces = VGroup(
            self._card("COMPONENTS", r"\operatorname{Null}(B)", "one constant per component", ORANGE, 3.55, 29),
            self._card("GRADIENTS", r"\operatorname{Col}(B)", "compatible edge differences", GREEN_C, 3.55, 29),
            self._card("CYCLES", r"\operatorname{Null}(B^T)", "conserved circulations", TEAL_C, 3.55, 29),
        ).arrange(RIGHT, buff=0.30)
        structure = VGroup(energy, subspaces, MathTex(r"\operatorname{Null}(L)=\operatorname{Null}(B)", font_size=39, color=WHITE)).arrange(DOWN, buff=0.43).move_to(DOWN * 0.02)
        self.play(FadeIn(energy))
        self.play(FadeIn(subspaces))
        self.play(FadeIn(structure[2]))
        self.wait(4.2)

        # Card 5: dimensions count components and cycles.
        heading = self._replace_heading(heading, "The dimensions of graph subspaces count connectivity and independent circulation.")
        self.play(FadeOut(structure))
        dimensions = VGroup(
            MathTex(r"n=4,\qquad m=4,\qquad c=1", font_size=45, color=YELLOW),
            VGroup(
                self._card("RANK", r"\operatorname{rank}(B)=n-c=3", "three independent contrasts", GREEN_C, 3.75, 28),
                self._card("NULLITY", r"\dim\operatorname{Null}(B)=c=1", "one component constant", ORANGE, 3.75, 27),
                self._card("LEFT NULLITY", r"\dim\operatorname{Null}(B^T)=m-n+c=1", "one independent cycle", TEAL_C, 3.75, 24),
            ).arrange(RIGHT, buff=0.28),
            Text("Delete the bridge: components increase.  Delete a cycle edge: circulations decrease.", font_size=23, color=WHITE),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.02)
        self.play(FadeIn(dimensions[0]))
        self.play(FadeIn(dimensions[1]))
        self.play(FadeIn(dimensions[2]))
        self.wait(4.2)

        # Card 6: the low Laplacian spectrum reveals a weak split.
        heading = self._replace_heading(heading, "The low Laplacian spectrum measures connectedness and suggests a partition.")
        self.play(FadeOut(dimensions))
        graph, positions, lines = self._graph()
        fiedler_labels = VGroup(
            MathTex("1", font_size=30, color=TEAL_C).next_to(positions[1], UP, buff=0.30),
            MathTex("1", font_size=30, color=TEAL_C).next_to(positions[2], DOWN, buff=0.30),
            MathTex("0", font_size=30, color=TEAL_C).next_to(positions[3], UP, buff=0.30),
            MathTex("-2", font_size=30, color=ORANGE).next_to(positions[4], UP, buff=0.30),
        )
        spectral = VGroup(
            MathTex(r"\operatorname{spec}(L)=(0,1,3,4)", font_size=43, color=YELLOW),
            MathTex(r"\lambda_2=1,\qquad v_2=(1,1,0,-2)^T", font_size=39, color=WHITE),
            self._card("FIEDLER SWEEP", r"\{1,2,3\}\mid\{4\}", "the bridge is the only cut edge", GREEN_C, 5.10, 33),
            MathTex(r"\operatorname{RatioCut}=\frac43", font_size=39, color=TEAL_C),
        ).arrange(DOWN, buff=0.33).to_edge(RIGHT, buff=0.33)
        self.play(FadeIn(graph), FadeIn(fiedler_labels), FadeIn(spectral[:2]))
        self.play(ShowPassingFlash(lines[(3, 4)].copy().set_color(ORANGE).set_stroke(width=8)))
        self.play(FadeIn(spectral[2:]))
        self.wait(4.2)

        # Card 7: Laplacian systems model electrical networks.
        heading = self._replace_heading(heading, "In an electrical network, the same Laplacian enforces current conservation.")
        self.play(FadeOut(graph), FadeOut(fiedler_labels), FadeOut(spectral))
        electrical = VGroup(
            VGroup(
                self._card("EDGE LAW", r"I_{ij}=v_i-v_j", "unit resistance", TEAL_C, 3.45, 31),
                self._card("VERTEX LAW", r"Lv=b", "net current equals injection", GREEN_C, 3.45, 34),
                self._card("BALANCE", r"\mathbf1^Tb=0", "injection equals withdrawal", ORANGE, 3.45, 34),
            ).arrange(RIGHT, buff=0.30),
            MathTex(r"b=(-1,0,0,1)^T\quad\Longrightarrow\quad v=\left(0,\frac13,\frac23,\frac53\right)^T", font_size=39, color=YELLOW),
            MathTex(r"R_{\rm eff}(4,1)=\frac53", font_size=42, color=WHITE),
            Text("Grounding one vertex removes the constant-potential ambiguity.", font_size=23, color=GREY_B),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.02)
        self.play(FadeIn(electrical[0]))
        self.play(FadeIn(electrical[1:]))
        self.wait(4.2)

        # Card 8: normalized adjacency produces a random walk.
        heading = self._replace_heading(heading, "Normalizing by degree turns the graph into a probability-preserving random walk.")
        self.play(FadeOut(electrical))
        probability = VGroup(
            MathTex(r"P=AD^{-1},\qquad p_{k+1}=Pp_k", font_size=48, color=YELLOW),
            VGroup(
                self._card("COLUMNS", r"\mathbf1^TP=\mathbf1^T", "outgoing probabilities sum to one", TEAL_C, 4.65, 29),
                self._card("STEADY STATE", r"P\pi=\pi", "probability no longer changes", GREEN_C, 4.65, 34),
            ).arrange(RIGHT, buff=0.42),
            MathTex(r"\pi=\left(\frac14,\frac14,\frac38,\frac18\right)^T", font_size=43, color=WHITE),
            Text("For this undirected walk, steady probability is proportional to degree.", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.43).move_to(DOWN * 0.02)
        self.play(FadeIn(probability[0]))
        self.play(FadeIn(probability[1]))
        self.play(FadeIn(probability[2:]))
        self.wait(4.2)

        # Card 9: directed links require repair before ranking.
        heading = self._replace_heading(heading, "For directed links, repair and teleportation create a stable PageRank model.")
        self.play(FadeOut(probability))
        directed_graph, _, _ = self._graph(directed=True)
        repair_cards = VGroup(
            self._text_card("REPAIR", ("replace dangling columns", "so probability is preserved"), ORANGE, 2.55),
            self._text_card("TELEPORT", ("allow a uniform jump", "so every state communicates"), TEAL_C, 2.55),
        ).arrange(RIGHT, buff=0.25)
        ranking = VGroup(
            MathTex(r"G=\frac12S+\frac12U", font_size=47, color=YELLOW),
            repair_cards,
            MathTex(r"Gr=r,\qquad r=\left(\frac{11}{49},\frac{13}{49},\frac27,\frac{11}{49}\right)^T", font_size=34, color=WHITE),
            self._card("RANKING", r"3>2>1=4", "incoming support is weighted recursively", GREEN_C, 4.85, 35),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 2.95 + DOWN * 0.10)
        if ranking.height > 4.65:
            ranking.scale_to_fit_height(4.65)
        self.play(FadeIn(directed_graph), FadeIn(ranking[:2]))
        self.play(FadeIn(ranking[2:]))
        self.wait(4.3)

        # Card 10: choose the matrix by the graph question.
        heading = self._replace_heading(heading, "Choose a graph matrix by asking what information the problem needs.")
        self.play(FadeOut(directed_graph), FadeOut(ranking))
        guide = VGroup(
            self._text_card("CONNECTIONS AND ROUTES", ("A records edges", "Aᵏ counts walks"), TEAL_C, 3.55),
            self._text_card("DIFFERENCES AND ENERGY", ("B compares endpoints", "L=BᵀB gathers variation"), ORANGE, 3.55),
            self._text_card("STRUCTURE AND FLOW", ("subspaces find components and cycles", "Lv=b models conserved flow"), GREEN_C, 3.55),
            self._text_card("MOVEMENT AND RANK", ("P evolves probabilities", "G ranks directed links"), YELLOW, 3.55),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.38, 0.38))
        conclusion = VGroup(
            guide,
            Text("The picture supplies the relationships; linear algebra makes them computable.", font_size=26, color=YELLOW),
            Text("Next: assemble and review the complete chapter.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.02)
        self.play(FadeIn(guide))
        self.play(FadeIn(conclusion[1:]))
        self.wait(4.5)
        self.play(*[FadeOut(mobject) for mobject in self.mobjects])
