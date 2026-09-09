"""Opening title card for Graphs, Networks, and the Laplacian."""

from manim import (
    BLACK, DOWN, Dot, FadeIn, GREEN_C, GREY_B, LEFT, Line, MathTex,
    ORANGE, RIGHT, Scene, SurroundingRectangle, TEAL_C, Text, UP,
    VGroup, WHITE, YELLOW,
)


class GraphsNetworksLaplacianTitleCard(Scene):
    """Introduce the chapter through one graph and four algebraic lenses."""

    @staticmethod
    def _card(label, formula, note, color):
        body = VGroup(
            Text(label, font_size=21, color=color, weight="BOLD"),
            MathTex(formula, font_size=38, color=WHITE),
            Text(note, font_size=18, color=GREY_B),
        ).arrange(DOWN, buff=0.13)
        border = SurroundingRectangle(body, color=color, buff=0.16, stroke_width=2)
        return VGroup(border, body)

    @staticmethod
    def _graph():
        positions = {
            1: LEFT * 1.05 + UP * 0.90,
            2: LEFT * 1.05 + DOWN * 0.90,
            3: RIGHT * 0.75,
            4: RIGHT * 2.25,
        }
        edges = ((1, 2), (2, 3), (1, 3), (3, 4))
        lines = VGroup(*[
            Line(positions[first], positions[second], color=GREY_B, stroke_width=3.5)
            for first, second in edges
        ])
        dots = VGroup(*[
            Dot(positions[vertex], radius=0.19, color=YELLOW).set_z_index(3)
            for vertex in (1, 2, 3, 4)
        ])
        labels = VGroup(*[
            MathTex(str(vertex), font_size=29, color=BLACK)
            .move_to(positions[vertex]).set_z_index(5)
            for vertex in (1, 2, 3, 4)
        ])
        return VGroup(lines, dots, labels)

    def construct(self):
        eyebrow = Text("SEEING LINEAR ALGEBRA", font_size=24, color=GREY_B, weight="BOLD")
        title = Text(
            "GRAPHS, NETWORKS, AND THE LAPLACIAN",
            font_size=48,
            color=YELLOW,
            weight="BOLD",
        )
        if title.width > 12.2:
            title.scale_to_fit_width(12.2)
        subtitle = Text(
            "Connections become matrices; matrices reveal structure, flow, and movement.",
            font_size=28,
            color=WHITE,
        )
        if subtitle.width > 11.8:
            subtitle.scale_to_fit_width(11.8)
        headings = VGroup(eyebrow, title, subtitle).arrange(DOWN, buff=0.21).move_to(UP * 2.15)

        graph = self._graph().scale(1.06).move_to(LEFT * 3.45 + DOWN * 0.26)
        lenses = VGroup(
            self._card("CONNECTIONS", r"A", "adjacency and walks", TEAL_C),
            self._card("DIFFERENCES", r"B", "changes across edges", ORANGE),
            self._card("VARIATION", r"L=B^TB", "energy and spectrum", GREEN_C),
            self._card("MOVEMENT", r"P\ \text{or}\ G", "probability and ranking", YELLOW),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.38, 0.34)).move_to(RIGHT * 2.25 + DOWN * 0.23)

        question = Text(
            "Which representation fits the graph question?",
            font_size=28,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.28)

        self.play(FadeIn(headings), run_time=0.9)
        self.play(FadeIn(graph), run_time=0.8)
        self.play(FadeIn(lenses), run_time=0.9)
        self.play(FadeIn(question), run_time=0.6)
        self.wait(2.5)
