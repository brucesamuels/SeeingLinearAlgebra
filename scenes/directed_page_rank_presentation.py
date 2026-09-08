"""Manim presentation: directed graphs, teleportation, and PageRank."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    BLACK,
    Circle,
    Create,
    DOWN,
    Dot,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    LEFT,
    MathTex,
    Matrix,
    ORANGE,
    RED_C,
    RIGHT,
    Scene,
    ShowPassingFlash,
    SurroundingRectangle,
    TEAL_C,
    Tex,
    Text,
    Transform,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.directed_page_rank import DirectedPageRank


class DirectedPageRankPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Directed Graphs and PageRank"

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
            r"\textbf{Directed Graphs and PageRank}",
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
        edge_order = ((1, 2), (2, 3), (3, 1), (3, 4))
        arrows = {
            edge: Arrow(
                positions[edge[0]],
                positions[edge[1]],
                buff=0.23,
                color=GREY_B,
                stroke_width=4.3,
                tip_length=0.18,
            ).set_z_index(0)
            for edge in edge_order
        }
        dots = {
            vertex: Dot(positions[vertex], radius=0.17, color=YELLOW).set_z_index(3)
            for vertex in (1, 2, 3, 4)
        }
        labels = {
            vertex: MathTex(str(vertex), font_size=29, color=BLACK)
            .move_to(positions[vertex])
            .set_z_index(4)
            for vertex in (1, 2, 3, 4)
        }
        return VGroup(*arrows.values(), *dots.values(), *labels.values()), positions, arrows, dots, labels

    @staticmethod
    def _matrix(entries, scale=0.67, h_buff=0.78, v_buff=0.67):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _align_scalar_entries(matrix, amount=0.22):
        for entry in matrix.get_entries():
            if entry.get_tex_string() in {"0", "1"}:
                entry.shift(UP * amount)
        return matrix

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
    def _probability_marks(positions, values, color=TEAL_C):
        marks = VGroup()
        for vertex, value in zip((1, 2, 3, 4), values):
            halo = Circle(
                radius=0.23 + 0.52 * np.sqrt(value),
                color=color,
                stroke_width=3.0,
                fill_color=color,
                fill_opacity=0.15 + 0.48 * value,
            ).move_to(positions[vertex]).set_z_index(1)
            marks.add(halo)
        return marks

    def construct(self):
        model = DirectedPageRank()
        uniform = model.uniform_distribution()
        p0, p1, p2 = model.trajectory(uniform, 2)
        rank = model.page_rank()
        if model.directed_edges != ((1, 2), (2, 3), (3, 1), (3, 4)):
            raise RuntimeError("unexpected directed graph")
        if not np.allclose(model.google_matrix().sum(axis=0), np.ones(4)):
            raise RuntimeError("unexpected Google matrix")
        if not np.allclose(p1, [7 / 32, 9 / 32, 9 / 32, 7 / 32]):
            raise RuntimeError("unexpected PageRank iteration")
        if not np.allclose(rank, [11 / 49, 13 / 49, 2 / 7, 11 / 49]):
            raise RuntimeError("unexpected PageRank vector")
        if not np.allclose(model.stationary_residual(), np.zeros(4)):
            raise RuntimeError("unexpected PageRank residual")

        banner, title, heading = self._chrome(
            "A directed edge is an arrow: its source may point to its destination."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: introduce direction as graph vocabulary, not a drawing convention.
        graph, positions, arrows, _, _ = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        arrow_group = VGroup(*arrows.values())
        vertex_group = VGroup(*graph[len(arrows):])
        direction_panel = VGroup(
            self._card("SOURCE", r"1", "where the arrow begins", TEAL_C, width=4.72),
            self._card("DESTINATION", r"2", "where the arrow points", ORANGE, width=4.72),
            MathTex(r"1\to2\quad\not\Rightarrow\quad2\to1", font_size=39, color=YELLOW),
            Text("Direction is part of the graph's data.", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.27).scale(0.91).to_edge(RIGHT, buff=0.40).shift(DOWN * 0.10)
        self.play(FadeIn(vertex_group))
        for arrow in arrow_group:
            self.play(Create(arrow), run_time=0.55)
        self.play(FadeIn(direction_panel))
        self.wait(2.9)

        # Card 2: outgoing links control choices and reveal a dangling vertex.
        heading = self._replace_heading(
            heading, "A directed walk chooses among outgoing links; vertex 4 has none."
        )
        self.play(FadeOut(direction_panel))
        out_labels = VGroup(
            *[
                MathTex(rf"d_{{{vertex}}}^{{\rm out}}={degree}", font_size=27, color=color).next_to(
                    positions[vertex], direction, buff=0.25
                )
                for vertex, degree, direction, color in (
                    (1, 1, UP, TEAL_C),
                    (2, 1, DOWN, TEAL_C),
                    (3, 2, DOWN, GREEN_C),
                    (4, 0, UP, ORANGE),
                )
            ]
        )
        choice_panel = VGroup(
            self._card("FROM VERTEX 3", r"\frac12\text{ to 1},\ \frac12\text{ to 4}", "two outgoing choices", GREEN_C, width=4.82),
            self._card("AT VERTEX 4", r"d_4^{\rm out}=0", "no next link to follow", ORANGE, width=4.82),
            Text("A vertex with no outgoing link is called dangling.", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.31).to_edge(RIGHT, buff=0.36).shift(DOWN * 0.18)
        self.play(FadeIn(out_labels), FadeIn(choice_panel))
        self.play(arrows[(3, 1)].animate.set_color(GREEN_C), arrows[(3, 4)].animate.set_color(GREEN_C))
        self.play(ShowPassingFlash(Circle(radius=0.31, color=ORANGE).move_to(positions[4]).set_stroke(width=6)))
        self.wait(3.0)

        # Card 3: encode link following and expose the zero dangling column.
        heading = self._replace_heading(
            heading, "The link matrix records destinations by column, just as in the undirected walk."
        )
        self.play(FadeOut(graph), FadeOut(out_labels), FadeOut(choice_panel))
        raw = self._align_scalar_entries(
            self._matrix(
                [
                    ["0", "0", r"\frac12", "0"],
                    ["1", "0", "0", "0"],
                    ["0", "1", "0", "0"],
                    ["0", "0", r"\frac12", "0"],
                ],
                scale=0.60,
                h_buff=0.98,
                v_buff=1.16,
            )
        ).move_to(LEFT * 1.62 + DOWN * 0.03)
        raw_label = MathTex(r"H=", font_size=40, color=YELLOW).next_to(raw, LEFT, buff=0.30)
        zero_column = SurroundingRectangle(raw.get_columns()[3], color=ORANGE, buff=0.11, stroke_width=3)
        column_panel = VGroup(
            MathTex(r"\mathbf 1^TH=(1,1,1,0)", font_size=40, color=TEAL_C),
            Text("Columns 1 through 3 distribute all their mass.", font_size=22, color=WHITE),
            self._card("COLUMN 4", r"H_{\cdot4}=0", "probability would disappear", ORANGE, width=4.72),
        ).arrange(DOWN, buff=0.37).to_edge(RIGHT, buff=0.40).shift(DOWN * 0.06)
        self.play(FadeIn(raw_label), FadeIn(raw))
        self.play(Create(zero_column), FadeIn(column_panel))
        self.wait(3.1)

        # Card 4: repair the dangling column from first principles.
        heading = self._replace_heading(
            heading, "At a dead end, restart uniformly so that no probability is lost."
        )
        self.play(FadeOut(raw_label), FadeOut(raw), FadeOut(zero_column), FadeOut(column_panel))
        old_column = self._matrix([["0"], ["0"], ["0"], ["0"]], scale=0.67, v_buff=0.91)
        new_column = self._matrix(
            [[r"\frac14"], [r"\frac14"], [r"\frac14"], [r"\frac14"]],
            scale=0.62,
            v_buff=1.48,
        )
        old_label = MathTex(r"H_{\cdot4}", font_size=34, color=ORANGE).next_to(old_column, UP, buff=0.22)
        new_label = MathTex(r"S_{\cdot4}", font_size=34, color=GREEN_C).next_to(new_column, UP, buff=0.22)
        repair = VGroup(
            VGroup(old_column, old_label),
            MathTex(r"\Longrightarrow", font_size=47, color=YELLOW),
            VGroup(new_column, new_label),
        ).arrange(RIGHT, buff=0.70).move_to(UP * 0.18)
        repair_notes = VGroup(
            Text("The repaired link matrix S sends a dangling vertex equally to all four vertices.", font_size=23, color=WHITE),
            MathTex(r"\mathbf 1^TS=\mathbf 1^T", font_size=41, color=TEAL_C),
            Text("Every column now preserves probability.", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(repair[0]))
        self.play(FadeIn(repair[1]), FadeIn(repair[2]))
        self.play(FadeIn(repair_notes))
        self.wait(3.1)

        # Card 5: add teleportation to every step.
        heading = self._replace_heading(
            heading, "Teleportation gives every step a small chance to jump anywhere."
        )
        self.play(FadeOut(repair), FadeOut(repair_notes))
        mechanisms = VGroup(
            self._card("FOLLOW A LINK", r"\alpha=\frac12", "use the repaired link matrix S", TEAL_C, width=4.48),
            self._card("JUMP ANYWHERE", r"1-\alpha=\frac12", "choose any vertex uniformly", ORANGE, width=4.48),
        ).arrange(RIGHT, buff=0.65).move_to(UP * 0.66)
        google_definition = VGroup(
            MathTex(r"G=\frac12S+\frac12U", font_size=46, color=YELLOW),
            MathTex(r"U=\frac14\mathbf 1\mathbf 1^T", font_size=40, color=GREEN_C),
            Text("Each destination receives a teleportation baseline of 1/8.", font_size=23, color=WHITE),
        ).arrange(DOWN, buff=0.30).to_edge(DOWN, buff=0.68)
        self.play(FadeIn(mechanisms[0]))
        self.play(FadeIn(mechanisms[1]))
        self.play(FadeIn(google_definition))
        self.wait(3.1)

        # Card 6: display the exact positive Google matrix structurally.
        heading = self._replace_heading(
            heading, "The Google matrix combines link structure with a uniform safety net."
        )
        self.play(FadeOut(mechanisms), FadeOut(google_definition))
        google = self._matrix(
            [
                [r"\frac18", r"\frac18", r"\frac38", r"\frac14"],
                [r"\frac58", r"\frac18", r"\frac18", r"\frac14"],
                [r"\frac18", r"\frac58", r"\frac18", r"\frac14"],
                [r"\frac18", r"\frac18", r"\frac38", r"\frac14"],
            ],
            scale=0.60,
            h_buff=1.03,
            v_buff=1.52,
        ).move_to(LEFT * 1.35 + DOWN * 0.02)
        google_label = MathTex(r"G=", font_size=40, color=YELLOW).next_to(google, LEFT, buff=0.30)
        google_panel = VGroup(
            self._card("POSITIVE", r"G_{ij}>0", "every vertex can reach every destination in one step", GREEN_C, width=4.66),
            self._card("STOCHASTIC", r"\mathbf 1^TG=\mathbf 1^T", "every column sums to one", TEAL_C, width=4.66),
        ).arrange(DOWN, buff=0.38).to_edge(RIGHT, buff=0.42).shift(DOWN * 0.04)
        self.play(FadeIn(google_label), FadeIn(google))
        self.play(FadeIn(google_panel))
        self.wait(3.1)

        # Card 7: iterate from an initially uniform distribution.
        heading = self._replace_heading(
            heading, "Repeated multiplication moves probability toward a stable ranking."
        )
        self.play(FadeOut(google_label), FadeOut(google), FadeOut(google_panel))
        graph, positions, _, _, _ = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        marks = self._probability_marks(positions, p0, ORANGE)
        states = VGroup(
            MathTex(r"p_0=\left(\frac14,\frac14,\frac14,\frac14\right)^T", font_size=39, color=ORANGE),
            MathTex(r"p_1=Gp_0=\left(\frac7{32},\frac9{32},\frac9{32},\frac7{32}\right)^T", font_size=37, color=TEAL_C),
            MathTex(r"p_2=G p_1=\left(\frac{57}{256},\frac{67}{256},\frac{75}{256},\frac{57}{256}\right)^T", font_size=34, color=GREEN_C),
            Text("The changing halo sizes show the changing probability mass.", font_size=21, color=YELLOW),
        ).arrange(DOWN, buff=0.34).to_edge(RIGHT, buff=0.28).shift(UP * 0.10)
        states[1].scale_to_fit_width(5.05)
        states[2].scale_to_fit_width(5.10)
        self.play(FadeIn(graph), FadeIn(marks), FadeIn(states[0]))
        p1_marks = self._probability_marks(positions, p1, TEAL_C)
        self.play(Transform(marks, p1_marks), FadeIn(states[1]), run_time=1.25)
        p2_marks = self._probability_marks(positions, p2, GREEN_C)
        self.play(Transform(marks, p2_marks), FadeIn(states[2]), run_time=1.25)
        self.play(FadeIn(states[3]))
        self.wait(2.8)

        # Card 8: define PageRank as the stationary distribution of G.
        heading = self._replace_heading(
            heading, "PageRank is the probability distribution unchanged by another Google-matrix step."
        )
        self.play(FadeOut(graph), FadeOut(marks), FadeOut(states))
        page_rank = VGroup(
            self._card("PAGERANK", r"Gr=r", "the stationary distribution of G", GREEN_C, width=6.10),
            MathTex(r"r=\left(\frac{11}{49},\frac{13}{49},\frac27,\frac{11}{49}\right)^T", font_size=45, color=YELLOW),
            Text("A larger entry means a larger long-run share of visits.", font_size=24, color=WHITE),
            MathTex(r"r_1+r_2+r_3+r_4=1", font_size=38, color=TEAL_C),
        ).arrange(DOWN, buff=0.36).move_to(DOWN * 0.07)
        self.play(FadeIn(page_rank[0]))
        self.play(FadeIn(page_rank[1]))
        self.play(FadeIn(page_rank[2:]))
        self.wait(3.1)

        # Card 9: interpret the exact ranking on the graph.
        heading = self._replace_heading(
            heading, "Rank flows through incoming links, and a source divides its support among its exits."
        )
        self.play(FadeOut(page_rank))
        graph, positions, arrows, _, _ = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        rank_marks = self._probability_marks(positions, rank, GREEN_C)
        rank_labels = VGroup(
            *[
                MathTex(value, font_size=25, color=WHITE).next_to(positions[vertex], direction, buff=0.70)
                for vertex, value, direction in (
                    (1, r"\frac{11}{49}", UP),
                    (2, r"\frac{13}{49}", DOWN),
                    (3, r"\frac27", DOWN),
                    (4, r"\frac{11}{49}", UP),
                )
            ]
        )
        interpretation = VGroup(
            MathTex(r"r_i=\frac12(Sr)_i+\frac18", font_size=43, color=TEAL_C),
            Text("link-following support + teleportation baseline", font_size=22, color=GREY_B),
            self._card("RANK ORDER", r"3>2>1=4", "vertex 3 receives the largest long-run share", ORANGE, width=4.82),
            Text("Support from vertex 3 is split between its two outgoing links.", font_size=21, color=YELLOW),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.31).shift(DOWN * 0.04)
        self.play(FadeIn(graph), FadeIn(rank_marks), FadeIn(rank_labels))
        self.play(arrows[(2, 3)].animate.set_color(GREEN_C), FadeIn(interpretation))
        self.wait(3.1)

        # Card 10: synthesize the ranking pipeline and preview chapter synthesis.
        heading = self._replace_heading(
            heading, "Direction creates link flow; teleportation makes the ranking robust."
        )
        self.play(FadeOut(graph), FadeOut(rank_marks), FadeOut(rank_labels), FadeOut(interpretation))
        synthesis = VGroup(
            self._card("DIRECT", r"j\to i", "arrows distinguish sources from destinations", TEAL_C, width=3.56),
            self._card("REPAIR", r"G=\frac12S+\frac12U", "dead ends cannot lose probability", GREEN_C, width=3.56),
            self._card("RANK", r"Gr=r", "equilibrium turns repeated visits into a score", ORANGE, width=3.56),
        ).arrange(RIGHT, buff=0.30).move_to(UP * 0.76)
        conclusion = VGroup(
            MathTex(r"r=\left(\frac{11}{49},\frac{13}{49},\frac27,\frac{11}{49}\right)^T", font_size=42, color=YELLOW),
            Text("The ranking depends on both the directed links and the chosen teleportation rule.", font_size=23, color=WHITE),
        ).arrange(DOWN, buff=0.28).move_to(DOWN * 1.02)
        preview = Text(
            "Next: assemble the chapter's graph, matrix, energy, spectrum, and flow viewpoints.",
            font_size=23,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.68)
        self.play(FadeIn(synthesis))
        self.play(FadeIn(conclusion))
        self.play(FadeIn(preview))
        self.wait(3.2)

        self.play(*[FadeOut(mobject) for mobject in self.mobjects])
