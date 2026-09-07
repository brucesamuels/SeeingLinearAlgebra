"""Manim presentation: random walks and Markov chains on a graph."""

from __future__ import annotations

import numpy as np
from manim import (
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
    Transform,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.graph_random_walk import GraphRandomWalk


class GraphRandomWalkPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Random Walks and Markov Chains"

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
            r"\textbf{Random Walks and Markov Chains}",
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
            vertex: Dot(positions[vertex], radius=0.17, color=YELLOW).set_z_index(3)
            for vertex in (1, 2, 3, 4)
        }
        labels = {
            vertex: MathTex(str(vertex), font_size=29, color=BLACK)
            .move_to(positions[vertex])
            .set_z_index(4)
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

    @staticmethod
    def _probability_marks(positions, values, color=TEAL_C):
        marks = VGroup()
        for vertex, value in zip((1, 2, 3, 4), values):
            if value > 1e-10:
                halo = Circle(
                    radius=0.23 + 0.43 * np.sqrt(value),
                    color=color,
                    stroke_width=3.0,
                    fill_color=color,
                    fill_opacity=0.16 + 0.30 * value,
                ).move_to(positions[vertex]).set_z_index(1)
                marks.add(halo)
        return marks

    def construct(self):
        model = GraphRandomWalk()
        start = model.point_mass(4)
        trajectory = model.trajectory(start, 4)
        stationary = model.stationary_distribution()
        late = model.evolve(start, 24)
        if not np.allclose(trajectory[4], [11 / 36, 11 / 36, 1 / 6, 2 / 9]):
            raise RuntimeError("unexpected random-walk trajectory")
        if not np.allclose(stationary, [1 / 4, 1 / 4, 3 / 8, 1 / 8]):
            raise RuntimeError("unexpected stationary distribution")
        if model.total_variation_distance(late, stationary) >= 0.001:
            raise RuntimeError("unexpected convergence behavior")
        if not np.allclose(model.stationary_laplacian_residual(), np.zeros(4)):
            raise RuntimeError("unexpected Laplacian connection")

        banner, title, heading = self._chrome(
            "A random walk chooses one neighboring vertex at each step."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: define the walk visually, without assuming probability vocabulary.
        graph, positions, edges, dots, _ = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        walker = Dot(positions[3], radius=0.11, color=ORANGE).set_z_index(5)
        choices = VGroup(
            *[
                edges[edge].copy().set_color(ORANGE).set_stroke(width=8)
                for edge in ((1, 3), (2, 3), (3, 4))
            ]
        )
        explanation = VGroup(
            self._card("CURRENT VERTEX", r"3", "the walk is here now", ORANGE, width=4.75),
            self._card("NEXT STEP", r"1,\ 2,\ \text{or }4", "choose one neighbor uniformly", TEAL_C, width=4.75),
            Text("Three choices means probability 1/3 for each.", font_size=23, color=YELLOW),
            Text("Only the current vertex matters: the Markov property.", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.31).to_edge(RIGHT, buff=0.43)
        self.play(FadeIn(graph), FadeIn(walker), dots[3].animate.set_color(GREEN_C))
        for choice in choices:
            self.play(ShowPassingFlash(choice), run_time=0.55)
        self.play(FadeIn(explanation))
        self.wait(2.8)

        # Card 2: connect degree to the one-step probabilities.
        heading = self._replace_heading(
            heading, "The degree tells us how many equally likely choices a vertex has."
        )
        self.play(FadeOut(walker), FadeOut(choices), FadeOut(explanation))
        degree_labels = VGroup(
            *[
                MathTex(rf"d_{vertex}={degree}", font_size=28, color=TEAL_C).next_to(
                    dots[vertex], direction, buff=0.22
                )
                for vertex, degree, direction in (
                    (1, 2, UP), (2, 2, DOWN), (3, 3, DOWN), (4, 1, UP)
                )
            ]
        )
        degree_panel = VGroup(
            self._card("FROM VERTEX 1", r"\frac1{d_1}=\frac12", "one half along either edge", TEAL_C, width=4.75),
            self._card("FROM VERTEX 3", r"\frac1{d_3}=\frac13", "one third along any edge", GREEN_C, width=4.75),
            self._card("FROM VERTEX 4", r"\frac1{d_4}=1", "only one possible move", ORANGE, width=4.75),
        ).arrange(DOWN, buff=0.24).scale(0.86).to_edge(RIGHT, buff=0.43).shift(DOWN * 0.32)
        self.play(FadeIn(degree_labels), FadeIn(degree_panel))
        self.wait(2.9)

        # Card 3: build the transition matrix column by column.
        heading = self._replace_heading(
            heading, "Column j records where probability moves when the walk leaves vertex j."
        )
        self.play(FadeOut(graph), FadeOut(degree_labels), FadeOut(degree_panel))
        transition = self._matrix(
            [
                ["0", r"\frac12", r"\frac13", "0"],
                [r"\frac12", "0", r"\frac13", "0"],
                [r"\frac12", r"\frac12", "0", "1"],
                ["0", "0", r"\frac13", "0"],
            ],
            scale=0.60,
            h_buff=0.98,
            v_buff=1.16,
        ).move_to(LEFT * 1.18 + DOWN * 0.04)
        for entry in transition.get_entries():
            if entry.get_tex_string() in {"0", "1"}:
                entry.shift(UP * 0.22)
        matrix_label = MathTex(r"P=A D^{-1}", font_size=40, color=YELLOW).next_to(transition, LEFT, buff=0.42)
        source_labels = VGroup(
            *[
                MathTex(rf"j={vertex}", font_size=25, color=TEAL_C).next_to(column, UP, buff=0.20)
                for vertex, column in enumerate(transition.get_columns(), start=1)
            ]
        )
        rule = VGroup(
            MathTex(r"p_{k+1}=Pp_k", font_size=43, color=GREEN_C),
            Text("We use column probability vectors.", font_size=23, color=WHITE),
            MathTex(r"\mathbf 1^TP=\mathbf 1^T", font_size=37, color=TEAL_C),
            Text("Every column sums to 1.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.24).to_edge(RIGHT, buff=0.43).shift(DOWN * 0.10)
        self.play(FadeIn(matrix_label), FadeIn(transition.get_brackets()))
        for column, label in zip(transition.get_columns(), source_labels):
            highlight = SurroundingRectangle(column, color=ORANGE, buff=0.10, stroke_width=2.5)
            self.play(FadeIn(label), Create(highlight), run_time=0.35)
            self.play(FadeIn(column), run_time=0.42)
            self.play(FadeOut(highlight), FadeOut(label), run_time=0.20)
        self.play(FadeIn(rule))
        self.wait(3.0)

        # Card 4: introduce a distribution as movable probability mass.
        heading = self._replace_heading(
            heading, "A probability distribution records how likely the walker is to be at each vertex."
        )
        self.play(FadeOut(matrix_label), FadeOut(transition), FadeOut(source_labels), FadeOut(rule))
        graph, positions, edge_map, _, _ = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        p0_marks = self._probability_marks(positions, trajectory[0], ORANGE)
        p1_marks = self._probability_marks(positions, trajectory[1], TEAL_C)
        walker = Dot(positions[4], radius=0.11, color=ORANGE).set_z_index(5)
        distributions = VGroup(
            MathTex(r"p_0=(0,0,0,1)^T", font_size=38, color=ORANGE),
            Text("certain to start at vertex 4", font_size=22, color=GREY_B),
            MathTex(r"p_1=Pp_0=(0,0,1,0)^T", font_size=38, color=TEAL_C),
            Text("vertex 4 has only one neighbor: vertex 3", font_size=22, color=GREY_B),
            Text("Each entry is nonnegative, and all four entries sum to 1.", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.24).to_edge(RIGHT, buff=0.35)
        self.play(FadeIn(graph), FadeIn(p0_marks), FadeIn(walker), FadeIn(distributions[0:2]))
        self.play(
            walker.animate.move_to(positions[3]),
            ShowPassingFlash(edge_map[(3, 4)].copy().set_color(ORANGE).set_stroke(width=10)),
            Transform(p0_marks, p1_marks),
            run_time=1.5,
        )
        self.play(FadeIn(distributions[2:]))
        self.wait(2.9)

        # Card 5: show probability spreading through exact early states.
        heading = self._replace_heading(
            heading, "Matrix multiplication moves and recombines all the probability mass."
        )
        self.play(FadeOut(walker), FadeOut(distributions))
        marks = p0_marks
        state_tex = MathTex(r"p_1=(0,0,1,0)^T", font_size=38, color=TEAL_C).to_edge(RIGHT, buff=0.62).shift(UP * 0.72)
        state_note = Text("At every step, the four entries still sum to 1.", font_size=23, color=YELLOW).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(state_tex), FadeIn(state_note))
        formulas = (
            r"p_2=\left(\frac13,\frac13,0,\frac13\right)^T",
            r"p_3=\left(\frac16,\frac16,\frac23,0\right)^T",
            r"p_4=\left(\frac{11}{36},\frac{11}{36},\frac16,\frac29\right)^T",
        )
        for step, formula in zip((2, 3, 4), formulas):
            new_marks = self._probability_marks(positions, trajectory[step], TEAL_C)
            new_tex = MathTex(formula, font_size=38, color=TEAL_C).move_to(state_tex)
            if new_tex.width > 5.2:
                new_tex.scale_to_fit_width(5.2)
            self.play(Transform(marks, new_marks), Transform(state_tex, new_tex), run_time=1.20)
            self.wait(0.35)
        self.wait(2.3)

        # Card 6: define stationarity and verify the exact distribution.
        heading = self._replace_heading(
            heading, "A stationary distribution looks unchanged after one more step."
        )
        self.play(FadeOut(graph), FadeOut(marks), FadeOut(state_tex), FadeOut(state_note))
        stationary_definition = VGroup(
            self._card("STATIONARY", r"P\pi=\pi", "one step leaves the distribution unchanged", GREEN_C, width=6.2),
            MathTex(r"\pi=\left(\frac14,\frac14,\frac38,\frac18\right)^T", font_size=45, color=YELLOW),
            MathTex(
                r"P\left(\frac14,\frac14,\frac38,\frac18\right)^T"
                r"=\left(\frac14,\frac14,\frac38,\frac18\right)^T",
                font_size=37,
                color=TEAL_C,
            ),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.05)
        stationary_definition[2].scale_to_fit_width(10.8)
        self.play(FadeIn(stationary_definition[0]))
        self.play(FadeIn(stationary_definition[1]))
        self.play(FadeIn(stationary_definition[2]))
        self.wait(3.0)

        # Card 7: explain the degree-proportional stationary distribution visually.
        heading = self._replace_heading(
            heading, "At equilibrium, higher-degree vertices receive more probability traffic."
        )
        self.play(FadeOut(stationary_definition))
        graph, positions, _, _, _ = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        stationary_marks = self._probability_marks(positions, stationary, GREEN_C)
        fraction_labels = VGroup(
            *[
                MathTex(value, font_size=26, color=WHITE).next_to(positions[vertex], direction, buff=0.68)
                for vertex, value, direction in (
                    (1, r"\frac14", UP), (2, r"\frac14", DOWN),
                    (3, r"\frac38", DOWN), (4, r"\frac18", UP)
                )
            ]
        )
        degree_reason = VGroup(
            MathTex(r"(d_1,d_2,d_3,d_4)=(2,2,3,1)", font_size=37, color=TEAL_C),
            MathTex(r"\pi_i=\frac{d_i}{2|E|}=\frac{d_i}{8}", font_size=42, color=GREEN_C),
            Text("Every edge contributes one arrival route at each endpoint.", font_size=22, color=WHITE),
            Text("Degree 3 gets the largest share; degree 1 gets the smallest.", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.35)
        self.play(FadeIn(graph), FadeIn(stationary_marks), FadeIn(fraction_labels))
        self.play(FadeIn(degree_reason))
        self.wait(3.0)

        # Card 8: connect stationarity back to the Laplacian null space.
        heading = self._replace_heading(
            heading, "The stationary equation is another form of the Laplacian null-space equation."
        )
        self.play(FadeOut(graph), FadeOut(stationary_marks), FadeOut(fraction_labels), FadeOut(degree_reason))
        derivation = VGroup(
            MathTex(r"P\pi=\pi", font_size=43, color=GREEN_C),
            MathTex(r"A D^{-1}\pi=\pi", font_size=43, color=WHITE),
            MathTex(r"(D-A)D^{-1}\pi=0", font_size=43, color=WHITE),
            MathTex(r"L D^{-1}\pi=0", font_size=46, color=YELLOW),
        ).arrange(DOWN, buff=0.31).move_to(LEFT * 2.15 + DOWN * 0.05)
        null_connection = VGroup(
            MathTex(r"D^{-1}\pi=\frac18\mathbf 1", font_size=43, color=TEAL_C),
            Text("Earlier: the constant vector spans Null(L).", font_size=23, color=WHITE),
            self._card("SAME STRUCTURE", r"L\mathbf 1=0", "connectivity reappears inside the walk", ORANGE, width=4.85),
        ).arrange(DOWN, buff=0.38).to_edge(RIGHT, buff=0.38).shift(DOWN * 0.02)
        for line in derivation:
            self.play(FadeIn(line), run_time=0.48)
        self.play(FadeIn(null_connection))
        self.wait(3.1)

        # Card 9: synthesize and state the convergence qualification carefully.
        heading = self._replace_heading(
            heading, "For this connected graph with an odd cycle, repeated steps approach equilibrium."
        )
        self.play(FadeOut(derivation), FadeOut(null_connection))
        synthesis = VGroup(
            self._card("MOVE", r"p_{k+1}=Pp_k", "degrees set the transition probabilities", TEAL_C, width=3.62),
            self._card("PRESERVE", r"\mathbf 1^Tp_k=1", "total probability remains one", GREEN_C, width=3.62),
            self._card("SETTLE", r"p_k\longrightarrow\pi", "the triangle prevents an endless two-step alternation", ORANGE, width=3.62),
        ).arrange(RIGHT, buff=0.30).move_to(UP * 0.50)
        late_state = MathTex(
            r"p_{24}\approx(0.2501,0.2501,0.3746,0.1252)^T\approx\pi",
            font_size=38,
            color=YELLOW,
        ).move_to(DOWN * 1.06)
        preview = Text(
            "Next: how can directed links and occasional jumps turn a walk into a ranking?",
            font_size=24,
            color=WHITE,
        ).to_edge(DOWN, buff=0.68)
        self.play(FadeIn(synthesis))
        self.play(FadeIn(late_state))
        self.play(FadeIn(preview))
        self.wait(3.2)

        self.play(*[FadeOut(mobject) for mobject in self.mobjects])
