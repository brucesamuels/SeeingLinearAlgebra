"""Manim presentation: using a Fiedler vector to partition a graph."""

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

from engine.spectral_graph_partition import SpectralGraphPartition


class SpectralGraphPartitionPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "The Fiedler Vector and Spectral Partitioning"

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
            r"\textbf{The Fiedler Vector and Spectral Partitioning}",
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

    def construct(self):
        model = SpectralGraphPartition()
        if model.sign_partition() != ((1, 2, 3), (4,)):
            raise RuntimeError("unexpected sign partition")
        if model.cut_edges((1, 2, 3)) != ((3, 4),):
            raise RuntimeError("unexpected Fiedler cut")
        if model.sweep_scores() != (4 / 3, 2.0):
            raise RuntimeError("unexpected sweep scores")
        if model.best_sweep_partition() != ((4,), (1, 2, 3)):
            raise RuntimeError("unexpected best sweep partition")

        banner, title, heading = self._chrome(
            "The Fiedler vector gives one real number to every vertex."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: recall and visualize the exact Fiedler coordinates.
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.09)
        values = VGroup(
            MathTex(r"1", font_size=28, color=TEAL_C).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"1", font_size=28, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"0", font_size=28, color=YELLOW).next_to(labels[3], UP, buff=0.24),
            MathTex(r"-2", font_size=28, color=ORANGE).next_to(labels[4], RIGHT, buff=0.21),
        )
        fiedler = VGroup(
            self._card("FIEDLER VECTOR", r"\mathbf v_2=(1,1,0,-2)^T", "the λ₂ eigenvector", TEAL_C, width=4.82),
            self._card("INTERPRETATION", r"\text{nearby values prefer to agree}", "the bridge permits the largest change", ORANGE, width=4.82),
        ).arrange(DOWN, buff=0.42).to_edge(RIGHT, buff=0.39).shift(DOWN * 0.01)
        self.play(FadeIn(graph), FadeIn(values), FadeIn(fiedler[0]))
        self.play(ShowPassingFlash(edges[(3, 4)].copy().set_color(ORANGE).set_stroke(width=9)), FadeIn(fiedler[1]))
        self.wait(3.0)

        # Card 2: threshold the coordinates, stating the zero convention.
        heading = self._replace_heading(
            heading, "Use zero as a threshold to propose two groups of vertices."
        )
        self.play(FadeOut(graph), FadeOut(values), FadeOut(fiedler))
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.09)
        values = VGroup(
            MathTex(r"1", font_size=28, color=TEAL_C).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"1", font_size=28, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"0", font_size=28, color=YELLOW).next_to(labels[3], UP, buff=0.24),
            MathTex(r"-2", font_size=28, color=ORANGE).next_to(labels[4], RIGHT, buff=0.21),
        )
        groups = VGroup(
            self._card("NONNEGATIVE SIDE", r"S=\{1,2,3\}", "v_i ≥ 0; assign the zero here", TEAL_C, width=4.72),
            self._card("NEGATIVE SIDE", r"T=\{4\}", "v_i < 0", ORANGE, width=4.72),
            Text("This is one candidate partition.", font_size=25, color=YELLOW),
        ).arrange(DOWN, buff=0.34).to_edge(RIGHT, buff=0.42).shift(DOWN * 0.01)
        self.play(FadeIn(graph), FadeIn(values))
        self.play(
            *[dots[v].animate.set_color(TEAL_C) for v in (1, 2, 3)],
            dots[4].animate.set_color(ORANGE),
            FadeIn(groups[:2]),
        )
        self.play(FadeIn(groups[2]))
        self.wait(3.0)

        # Card 3: define crossing edges and cut size visually.
        heading = self._replace_heading(
            heading, "A cut edge has one endpoint in each proposed group."
        )
        self.play(FadeOut(graph), FadeOut(values), FadeOut(groups))
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 1.02 + DOWN * 0.10)
        triangle_group = VGroup(dots[1], dots[2], dots[3], labels[1], labels[2], labels[3])
        tail_group = VGroup(dots[4], labels[4])
        boxes = VGroup(
            SurroundingRectangle(triangle_group, color=TEAL_C, buff=0.43, stroke_width=2.5),
            SurroundingRectangle(tail_group, color=ORANGE, buff=0.43, stroke_width=2.5),
        )
        cut_label = MathTex(r"\operatorname{cut}(S,T)=1", font_size=42, color=YELLOW).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(graph), FadeIn(boxes))
        self.play(
            *[dots[v].animate.set_color(TEAL_C) for v in (1, 2, 3)],
            dots[4].animate.set_color(ORANGE),
            *[edges[e].animate.set_color(TEAL_C) for e in ((1, 2), (2, 3), (1, 3))],
        )
        self.play(ShowPassingFlash(edges[(3, 4)].copy().set_color(ORANGE).set_stroke(width=11)), edges[(3, 4)].animate.set_color(ORANGE).set_stroke(width=6), FadeIn(cut_label))
        self.wait(3.1)

        # Card 4: compare a plausible alternative cut.
        heading = self._replace_heading(
            heading, "A different grouping cuts two edges instead of one."
        )
        self.play(FadeOut(graph), FadeOut(boxes), FadeOut(cut_label))
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 1.02 + DOWN * 0.10)
        left_group = VGroup(dots[1], dots[2], labels[1], labels[2])
        right_group = VGroup(dots[3], dots[4], labels[3], labels[4])
        boxes = VGroup(
            SurroundingRectangle(left_group, color=TEAL_C, buff=0.43, stroke_width=2.5),
            SurroundingRectangle(right_group, color=ORANGE, buff=0.43, stroke_width=2.5),
        )
        alternative = VGroup(
            MathTex(r"S=\{1,2\},\quad T=\{3,4\}", font_size=34, color=WHITE),
            MathTex(r"\operatorname{cut}(S,T)=2", font_size=42, color=YELLOW),
            Text("crossing edges: {1,3} and {2,3}", font_size=24, color=ORANGE),
        ).arrange(DOWN, buff=0.27).to_edge(DOWN, buff=0.63)
        self.play(FadeIn(graph), FadeIn(boxes))
        self.play(
            *[dots[v].animate.set_color(TEAL_C) for v in (1, 2)],
            *[dots[v].animate.set_color(ORANGE) for v in (3, 4)],
        )
        for edge in ((1, 3), (2, 3)):
            self.play(ShowPassingFlash(edges[edge].copy().set_color(YELLOW).set_stroke(width=10)), edges[edge].animate.set_color(YELLOW).set_stroke(width=6), run_time=0.65)
        self.play(FadeIn(alternative))
        self.wait(3.0)

        # Card 5: introduce a balance-aware cut score.
        heading = self._replace_heading(
            heading, "A useful score counts crossing edges while also accounting for group sizes."
        )
        self.play(FadeOut(graph), FadeOut(boxes), FadeOut(alternative))
        definition = MathTex(
            r"\operatorname{RatioCut}(S,T)=\operatorname{cut}(S,T)"
            r"\left(\frac1{|S|}+\frac1{|T|}\right)",
            font_size=43,
            color=WHITE,
        )
        scores = VGroup(
            self._card("FIEDLER CANDIDATE", r"1\left(\frac13+1\right)=\frac43", "groups {1,2,3} and {4}", TEAL_C, width=5.15),
            self._card("ALTERNATIVE", r"2\left(\frac12+\frac12\right)=2", "groups {1,2} and {3,4}", ORANGE, width=5.15),
        ).arrange(RIGHT, buff=0.52)
        score_note = Text("For these candidates, the smaller score is 4/3.", font_size=26, color=YELLOW)
        score_layout = VGroup(definition, scores, score_note).arrange(DOWN, buff=0.47).move_to(DOWN * 0.02)
        self.play(FadeIn(score_layout[0]))
        self.play(FadeIn(score_layout[1][0]), FadeIn(score_layout[1][1]))
        self.play(FadeIn(score_layout[2]))
        self.wait(3.2)

        # Card 6: encode a discrete cut and recover RatioCut as a quotient.
        heading = self._replace_heading(
            heading, "Encode a proposed cut by two constants chosen to make the coordinates sum to zero."
        )
        self.play(FadeOut(score_layout))
        cut_vector = self._matrix(
            [[r"\frac13"], [r"\frac13"], [r"\frac13"], ["-1"]],
            scale=0.62,
            v_buff=1.08,
        )
        vector_group = VGroup(
            MathTex(r"\mathbf z=", font_size=42, color=YELLOW),
            cut_vector,
            MathTex(r",\qquad \mathbf z^T\mathbf 1=0", font_size=39, color=TEAL_C),
        ).arrange(RIGHT, buff=0.17).move_to(UP * 0.62)
        quotient = MathTex(
            r"\frac{\mathbf z^TL\mathbf z}{\mathbf z^T\mathbf z}"
            r"=\frac{16/9}{4/3}=\frac43"
            r"=\operatorname{RatioCut}(S,T)",
            font_size=43,
            color=GREEN_C,
        ).move_to(DOWN * 1.75)
        vector_note = Text("One constant labels each side; crossing edges create all the energy.", font_size=24, color=ORANGE).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(vector_group))
        self.play(FadeIn(quotient))
        self.play(FadeIn(vector_note))
        self.wait(3.2)

        # Card 7: relax discrete labels to arbitrary real coordinates.
        heading = self._replace_heading(
            heading, "Spectral partitioning replaces a discrete search with a continuous one."
        )
        self.play(FadeOut(vector_group), FadeOut(quotient), FadeOut(vector_note))
        relaxation = VGroup(
            self._card("DISCRETE CUT VECTORS", r"\mathbf z_i\in\left\{\frac1{|S|},-\frac1{|T|}\right\}", "search over vertex groupings", ORANGE, width=5.20),
            MathTex(r"\Longrightarrow", font_size=46, color=YELLOW),
            self._card("ALL REAL VECTORS", r"\mathbf x\perp\mathbf 1", "solve the easier relaxed problem", TEAL_C, width=5.20),
        ).arrange(RIGHT, buff=0.28).move_to(UP * 0.46)
        minimum = MathTex(
            r"\min_{\mathbf x\ne0,\ \mathbf x\perp\mathbf 1}"
            r"\frac{\mathbf x^TL\mathbf x}{\mathbf x^T\mathbf x}"
            r"=\lambda_2,\qquad \text{minimizer }\mathbf v_2",
            font_size=41,
            color=GREEN_C,
        ).move_to(DOWN * 1.08)
        relaxation_note = Text("The Fiedler vector supplies coordinates that guide a discrete cut.", font_size=24, color=YELLOW).to_edge(DOWN, buff=0.68)
        self.play(FadeIn(relaxation[0]))
        self.play(FadeIn(relaxation[1]), FadeIn(relaxation[2]))
        self.play(FadeIn(minimum), FadeIn(relaxation_note))
        self.wait(3.2)

        # Card 8: sweep thresholds between distinct coordinates.
        heading = self._replace_heading(
            heading, "Sort the Fiedler coordinates and test thresholds only between distinct values."
        )
        self.play(FadeOut(relaxation), FadeOut(minimum), FadeOut(relaxation_note))
        order = MathTex(
            r"v_4=-2\quad<\quad v_3=0\quad<\quad v_1=v_2=1",
            font_size=41,
            color=WHITE,
        ).move_to(UP * 1.11)
        candidates = VGroup(
            self._card("AFTER -2", r"\{4\}\mid\{1,2,3\}", "RatioCut = 4/3", GREEN_C, width=5.10),
            self._card("AFTER 0", r"\{3,4\}\mid\{1,2\}", "RatioCut = 2", ORANGE, width=5.10),
        ).arrange(RIGHT, buff=0.58).move_to(DOWN * 0.16)
        best = Text("Best sweep cut: {4} | {1,2,3}", font_size=27, color=YELLOW, weight="BOLD").to_edge(DOWN, buff=0.70)
        self.play(FadeIn(order))
        self.play(FadeIn(candidates[0]))
        self.play(FadeIn(candidates[1]))
        self.play(FadeIn(best))
        self.wait(3.2)

        # Card 9: synthesize the method and bridge to electrical networks.
        heading = self._replace_heading(
            heading, "A continuous eigenvector can reveal a useful discrete division of a graph."
        )
        self.play(FadeOut(order), FadeOut(candidates), FadeOut(best))
        pipeline = VGroup(
            self._card("1. SOLVE", r"L\mathbf v_2=\lambda_2\mathbf v_2", "find the Fiedler coordinates", TEAL_C, width=3.48),
            self._card("2. SWEEP", r"\text{test thresholds}", "turn coordinates into groups", ORANGE, width=3.48),
            self._card("3. SCORE", r"\operatorname{RatioCut}", "choose the best candidate", GREEN_C, width=3.48),
        ).arrange(RIGHT, buff=0.34).move_to(UP * 0.40)
        caution = Text("The method proposes a cut; it does not promise the best cut for every objective.", font_size=23, color=WHITE).move_to(DOWN * 1.07)
        next_question = Text("What if vertex values represent electrical potentials?", font_size=26, color=YELLOW).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(pipeline))
        self.play(FadeIn(caution))
        self.play(FadeIn(next_question))
        self.wait(3.4)
