"""Manim presentation: introductory graph vocabulary from first principles."""

from __future__ import annotations

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    LEFT,
    Line,
    MathTex,
    MoveAlongPath,
    ORANGE,
    ReplacementTransform,
    RIGHT,
    Scene,
    SurroundingRectangle,
    TEAL_C,
    Tex,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    Dot,
)

from engine.simple_undirected_graph import triangle_with_tail_graph


class GraphVocabularyPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "What Is a Graph? Objects, Connections, and Routes"

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
            r"\textbf{What Is a Graph? Objects, Connections, and Routes}",
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
    def _graph(cls, shift=DOWN * 0.12, omitted_edges=(), positions=None):
        graph = triangle_with_tail_graph()
        omitted = {frozenset(edge) for edge in omitted_edges}
        base_positions = cls.POSITIONS if positions is None else positions
        positions = {vertex: point + shift for vertex, point in base_positions.items()}
        edges = {
            edge: Line(
                positions[edge[0]],
                positions[edge[1]],
                color=GREY_B,
                stroke_width=4.2,
            ).set_z_index(0)
            for edge in graph.edges
            if frozenset(edge) not in omitted
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
    def _definition_card(term, definition, color, width=4.35):
        content = VGroup(
            Text(term, font_size=25, color=color, weight="BOLD"),
            Text(definition, font_size=22, color=WHITE, line_spacing=0.95),
        ).arrange(DOWN, buff=0.18)
        if content.width > width - 0.35:
            content.scale_to_fit_width(width - 0.35)
        border = SurroundingRectangle(content, color=color, buff=0.20, stroke_width=2.0)
        return VGroup(border, content)

    def construct(self):
        model = triangle_with_tail_graph()
        if model.degree_sequence() != (2, 2, 3, 1):
            raise RuntimeError("unexpected introductory graph degrees")
        if not model.is_walk((4, 3, 1, 2, 3, 1)):
            raise RuntimeError("unexpected introductory walk")
        if model.without_edge((3, 4)).connected_components() != ((1, 2, 3), (4,)):
            raise RuntimeError("unexpected introductory graph components")

        banner, title, heading = self._chrome(
            "What information remains when we keep only which places are directly connected?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        graph, positions, edges, dots, number_labels = self._graph()
        place_names = VGroup(
            Text("LIBRARY", font_size=22, color=TEAL_C).next_to(dots[1], UP + LEFT, buff=0.18),
            Text("STUDIO", font_size=22, color=ORANGE).next_to(dots[2], DOWN + LEFT, buff=0.18),
            Text("LAB", font_size=22, color=GREEN_C).next_to(dots[3], UP, buff=0.24),
            Text("GYM", font_size=22, color=TEAL_C).next_to(dots[4], RIGHT, buff=0.22),
        )
        core = VGroup(*edges.values(), *dots.values())
        opening_note = Text(
            "A line means there is a direct route between two places.",
            font_size=27,
            color=WHITE,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(core), FadeIn(place_names))
        self.play(FadeIn(opening_note))
        self.wait(2.6)

        heading = self._replace_heading(
            heading, "A graph keeps the relationships and discards irrelevant geometry."
        )
        alternate_positions = {
            1: LEFT * 2.60 + UP * 0.72,
            2: LEFT * 1.55 + DOWN * 1.28,
            3: RIGHT * 0.25 + UP * 0.62,
            4: RIGHT * 2.70 + DOWN * 0.82,
        }
        alternate, _, _, _, _ = self._graph(
            shift=DOWN * 0.08,
            positions=alternate_positions,
        )
        geometry_note = VGroup(
            Text("long or short edge", font_size=24, color=GREY_B),
            Text("straight or slanted edge", font_size=24, color=GREY_B),
            Text("same direct connections", font_size=28, color=GREEN_C, weight="BOLD"),
        ).arrange(DOWN, buff=0.21).to_edge(DOWN, buff=0.72)
        self.play(
            FadeOut(place_names),
            FadeOut(opening_note),
            FadeIn(VGroup(*number_labels.values())),
            FadeIn(geometry_note),
        )
        self.play(ReplacementTransform(graph, alternate), run_time=0.85)
        graph = alternate
        self.wait(2.5)

        heading = self._replace_heading(
            heading, "Vertices are the objects; edges are the direct relationships."
        )
        self.play(FadeOut(graph), FadeOut(geometry_note))
        graph, _, _, _, _ = self._graph(shift=LEFT * 2.55 + DOWN * 0.18)
        definitions = VGroup(
            self._definition_card("VERTEX", "one object in the graph", TEAL_C),
            self._definition_card("EDGE", "one direct relationship", ORANGE),
            MathTex(
                r"G=(V,E)",
                font_size=48,
                color=YELLOW,
            ),
            MathTex(
                r"V=\{1,2,3,4\}",
                font_size=34,
                color=WHITE,
            ),
            MathTex(
                r"E=\{\{1,2\},\{2,3\},\{1,3\},\{3,4\}\}",
                font_size=27,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.20).to_edge(RIGHT, buff=0.46).shift(DOWN * 0.12)
        self.play(FadeIn(graph))
        self.play(FadeIn(definitions[0]), FadeIn(definitions[1]))
        self.play(FadeIn(definitions[2:]))
        self.wait(3.1)

        heading = self._replace_heading(
            heading, "Adjacent vertices share an edge; each one's neighbors are one edge away."
        )
        self.play(FadeOut(graph), FadeOut(definitions))
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 2.55 + DOWN * 0.18)
        neighbor_edges = VGroup(edges[(2, 3)], edges[(1, 3)], edges[(3, 4)])
        neighbors = VGroup(
            self._definition_card("ADJACENT", "joined by one edge", TEAL_C),
            MathTex(r"N(3)=\{1,2,4\}", font_size=43, color=YELLOW),
            Text("The neighbors of 3", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.75).shift(DOWN * 0.05)
        self.play(FadeIn(graph), FadeIn(neighbors[0]))
        self.play(
            dots[3].animate.set_color(ORANGE).scale(1.18),
            neighbor_edges.animate.set_color(TEAL_C).set_stroke(width=6),
            dots[1].animate.set_color(TEAL_C),
            dots[2].animate.set_color(TEAL_C),
            dots[4].animate.set_color(TEAL_C),
        )
        self.play(FadeIn(neighbors[1:]))
        self.wait(2.8)

        heading = self._replace_heading(
            heading, "The degree of a vertex counts the edges that meet it."
        )
        self.play(FadeOut(graph), FadeOut(neighbors))
        graph, _, _, dots, _ = self._graph(shift=LEFT * 2.55 + DOWN * 0.18)
        degree_readout = VGroup(
            self._definition_card("DEGREE", "number of incident edges", ORANGE),
            MathTex(r"d_1=2,\quad d_2=2", font_size=39, color=WHITE),
            MathTex(r"d_3=3,\quad d_4=1", font_size=39, color=WHITE),
            Text("degree sequence: 2, 2, 3, 1", font_size=27, color=GREEN_C),
        ).arrange(DOWN, buff=0.31).to_edge(RIGHT, buff=0.60).shift(DOWN * 0.05)
        self.play(FadeIn(graph), FadeIn(degree_readout[0]))
        for vertex, formula in zip((1, 2, 3, 4), (degree_readout[1], degree_readout[1], degree_readout[2], degree_readout[2])):
            self.play(dots[vertex].animate.set_color(ORANGE).scale(1.14), run_time=0.24)
            self.play(dots[vertex].animate.set_color(YELLOW).scale(1 / 1.14), run_time=0.18)
            if formula not in self.mobjects:
                self.play(FadeIn(formula), run_time=0.25)
        self.play(FadeIn(degree_readout[3]))
        self.wait(2.6)

        heading = self._replace_heading(
            heading, "A walk follows edges and may revisit vertices or edges."
        )
        self.play(FadeOut(graph), FadeOut(degree_readout))
        graph, positions, _, _, _ = self._graph(shift=LEFT * 2.45 + DOWN * 0.18)
        walk_route = (4, 3, 1, 2, 3, 1)
        walk_panel = VGroup(
            self._definition_card("WALK", "a sequence joined edge by edge", ORANGE),
            MathTex(r"4\to3\to1\to2\to3\to1", font_size=35, color=WHITE),
            Text("vertices and edges may repeat", font_size=24, color=GREY_B),
            Text("length = 5 edges", font_size=28, color=YELLOW, weight="BOLD"),
        ).arrange(DOWN, buff=0.29).to_edge(RIGHT, buff=0.44).shift(DOWN * 0.05)
        marker = (
            Dot(positions[4], radius=0.14, color=ORANGE)
            .set_stroke(WHITE, width=2.6)
            .set_z_index(5)
        )
        self.play(FadeIn(graph), FadeIn(walk_panel), FadeIn(marker))
        for first, second in zip(walk_route, walk_route[1:]):
            self.play(
                MoveAlongPath(marker, Line(positions[first], positions[second])),
                run_time=0.75,
            )
        self.wait(2.6)

        heading = self._replace_heading(
            heading, "A path is a walk that does not repeat a vertex."
        )
        self.play(FadeOut(graph), FadeOut(walk_panel), FadeOut(marker))
        graph, positions, _, _, _ = self._graph(shift=LEFT * 2.45 + DOWN * 0.18)
        path_route = (4, 3, 1, 2)
        path_panel = VGroup(
            self._definition_card("PATH", "a walk with no repeated vertices", TEAL_C),
            MathTex(r"4\to3\to1\to2", font_size=42, color=WHITE),
            Text("four vertices", font_size=23, color=GREY_B),
            Text("length = 3 edges", font_size=28, color=YELLOW, weight="BOLD"),
        ).arrange(DOWN, buff=0.29).to_edge(RIGHT, buff=0.69).shift(DOWN * 0.05)
        marker = (
            Dot(positions[4], radius=0.14, color=TEAL_C)
            .set_stroke(WHITE, width=2.6)
            .set_z_index(5)
        )
        self.play(FadeIn(graph), FadeIn(path_panel), FadeIn(marker))
        for first, second in zip(path_route, path_route[1:]):
            self.play(
                MoveAlongPath(marker, Line(positions[first], positions[second])),
                run_time=0.85,
            )
        self.wait(2.8)

        heading = self._replace_heading(
            heading, "A graph is connected when every vertex can reach every other by a path."
        )
        self.play(FadeOut(graph), FadeOut(path_panel), FadeOut(marker))
        graph, _, edges, dots, _ = self._graph(shift=LEFT * 2.35 + DOWN * 0.18)
        connected_panel = VGroup(
            self._definition_card("CONNECTED", "every pair has a path between it", GREEN_C),
            MathTex(r"4\to3\to1", font_size=34, color=TEAL_C),
            MathTex(r"4\to3\to2", font_size=34, color=ORANGE),
            Text("From 4, every vertex is reachable.", font_size=25, color=WHITE),
        ).arrange(DOWN, buff=0.27).to_edge(RIGHT, buff=0.50).shift(DOWN * 0.05)
        self.play(FadeIn(graph), FadeIn(connected_panel[0]))
        self.play(
            VGroup(*edges.values()).animate.set_color(GREEN_C).set_stroke(width=5.5),
            VGroup(*dots.values()).animate.set_color(GREEN_C),
        )
        self.play(FadeIn(connected_panel[1:]))
        self.wait(3.0)

        heading = self._replace_heading(
            heading, "Removing one connection can separate the graph into connected components."
        )
        self.play(FadeOut(graph), FadeOut(connected_panel))
        graph, _, _, dots, labels = self._graph(
            shift=LEFT * 1.10 + DOWN * 0.18,
            omitted_edges=((3, 4),),
        )
        triangle = VGroup(dots[1], dots[2], dots[3], labels[1], labels[2], labels[3])
        isolated = VGroup(dots[4], labels[4])
        component_boxes = VGroup(
            SurroundingRectangle(triangle, color=TEAL_C, buff=0.42, stroke_width=2.4),
            SurroundingRectangle(isolated, color=ORANGE, buff=0.42, stroke_width=2.4),
        )
        component_labels = VGroup(
            MathTex(r"\{1,2,3\}", font_size=32, color=TEAL_C).next_to(component_boxes[0], DOWN, buff=0.18),
            MathTex(r"\{4\}", font_size=32, color=ORANGE).next_to(component_boxes[1], DOWN, buff=0.18),
        )
        removed_edge = Line(
            self.POSITIONS[3] + LEFT * 1.10 + DOWN * 0.18,
            self.POSITIONS[4] + LEFT * 1.10 + DOWN * 0.18,
            color=ORANGE,
            stroke_width=6,
        )
        removed_mark = Text("removed", font_size=22, color=ORANGE).next_to(removed_edge, UP, buff=0.12)
        components_note = Text(
            "Two components: within each group, paths still exist.",
            font_size=27,
            color=WHITE,
        ).to_edge(DOWN, buff=0.37)
        self.play(FadeIn(graph), FadeIn(removed_edge), FadeIn(removed_mark))
        self.play(FadeOut(removed_edge), FadeOut(removed_mark))
        self.play(FadeIn(component_boxes), FadeIn(component_labels), FadeIn(components_note))
        self.wait(3.2)

        heading = self._replace_heading(
            heading, "A graph turns a picture of relationships into a precise mathematical object."
        )
        self.play(FadeOut(graph), FadeOut(component_boxes), FadeOut(component_labels), FadeOut(components_note))
        graph, _, _, _, _ = self._graph(shift=UP * 0.10)
        takeaways = VGroup(
            self._definition_card("OBJECTS", "vertices", TEAL_C, width=3.15),
            self._definition_card("CONNECTIONS", "edges", ORANGE, width=3.15),
            self._definition_card("ROUTES", "walks and paths", GREEN_C, width=3.15),
        ).arrange(RIGHT, buff=0.36).to_edge(DOWN, buff=0.62)
        question = Text(
            "Can zeros and ones store exactly the same connections?",
            font_size=28,
            color=YELLOW,
            weight="BOLD",
        ).next_to(graph, DOWN, buff=0.38)
        self.play(FadeIn(graph))
        self.play(FadeIn(takeaways))
        self.play(FadeIn(question))
        self.wait(3.4)
