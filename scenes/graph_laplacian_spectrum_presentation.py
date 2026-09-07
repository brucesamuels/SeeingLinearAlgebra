"""Manim presentation: Laplacian eigenvalues and the spectral gap."""

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
    NumberLine,
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

from engine.graph_laplacian_spectrum import GraphLaplacianSpectrum
from engine.simple_undirected_graph import triangle_with_tail_graph


class GraphLaplacianSpectrumPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Laplacian Eigenvalues and the Spectral Gap"

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
            r"\textbf{Laplacian Eigenvalues and the Spectral Gap}",
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
    def _graph(cls, shift=DOWN * 0.12, include_bridge=True):
        graph = triangle_with_tail_graph()
        positions = {vertex: point + shift for vertex, point in cls.POSITIONS.items()}
        graph_edges = graph.edges if include_bridge else graph.edges[:-1]
        edges = {
            edge: Line(
                positions[edge[0]], positions[edge[1]], color=GREY_B, stroke_width=4.0
            ).set_z_index(0)
            for edge in graph_edges
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
    def _spectrum_line():
        line = NumberLine(
            x_range=[0, 4, 1],
            length=8.2,
            include_numbers=True,
            font_size=25,
            color=GREY_B,
            tick_size=0.08,
        )
        values = (0, 1, 3, 4)
        colors = (GREEN_C, ORANGE, TEAL_C, YELLOW)
        dots = VGroup(
            *[Dot(line.n2p(value), radius=0.13, color=color) for value, color in zip(values, colors)]
        )
        labels = VGroup(
            *[
                MathTex(rf"\lambda_{index}={value}", font_size=28, color=color).next_to(dot, UP, buff=0.20)
                for index, (value, color, dot) in enumerate(zip(values, colors, dots), start=1)
            ]
        )
        return line, dots, labels

    def construct(self):
        model = GraphLaplacianSpectrum()
        split = GraphLaplacianSpectrum(triangle_with_tail_graph().without_edge((3, 4)))
        if not np.allclose(model.ordered_eigenvalues(), [0, 1, 3, 4]):
            raise RuntimeError("unexpected recurring Laplacian spectrum")
        if not model.is_eigenpair(1, [1, 1, 0, -2]):
            raise RuntimeError("unexpected second Laplacian mode")
        if model.rayleigh_quotient([1, 1, 0, -2]) != 1:
            raise RuntimeError("unexpected second-mode Rayleigh quotient")
        if not np.allclose(split.ordered_eigenvalues(), [0, 0, 3, 3]):
            raise RuntimeError("unexpected split-graph spectrum")

        banner, title, heading = self._chrome(
            "Each connected component contributed a zero-eigenvalue direction."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: reconnect the null space with the zero eigenvalue.
        graph, _, edges, dots, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.10)
        values = VGroup(
            *[
                MathTex(r"1", font_size=27, color=GREEN_C).next_to(label, direction, buff=0.22)
                for label, direction in zip(labels.values(), (UP + LEFT, DOWN + LEFT, UP, RIGHT))
            ]
        )
        zero_mode = VGroup(
            self._card("CONSTANT MODE", r"\mathbf v_1=(1,1,1,1)^T", "one value across the connected graph", TEAL_C, width=4.82),
            MathTex(r"L\mathbf v_1=0\mathbf v_1", font_size=42, color=GREEN_C),
            MathTex(r"\lambda_1=0", font_size=44, color=YELLOW),
        ).arrange(DOWN, buff=0.36).to_edge(RIGHT, buff=0.40).shift(DOWN * 0.02)
        self.play(FadeIn(graph), FadeIn(values))
        self.play(
            *[edge.animate.set_color(TEAL_C).set_stroke(width=5.2) for edge in edges.values()],
            *[dot.animate.set_color(GREEN_C) for dot in dots.values()],
            FadeIn(zero_mode),
        )
        self.wait(3.0)

        # Card 2: order the exact spectrum on a number line.
        heading = self._replace_heading(
            heading, "Because L is symmetric and positive semidefinite, its eigenvalues are real and nonnegative."
        )
        self.play(FadeOut(graph), FadeOut(values), FadeOut(zero_mode))
        order = MathTex(r"0=\lambda_1\le\lambda_2\le\lambda_3\le\lambda_4", font_size=41, color=WHITE).move_to(UP * 1.05)
        line, spectrum_dots, spectrum_labels = self._spectrum_line()
        line.move_to(DOWN * 0.25)
        for dot, label, value in zip(spectrum_dots, spectrum_labels, (0, 1, 3, 4)):
            dot.move_to(line.n2p(value))
            label.next_to(dot, UP, buff=0.20)
        spectrum_note = Text("Recurring graph spectrum: 0, 1, 3, 4", font_size=27, color=YELLOW).to_edge(DOWN, buff=0.74)
        self.play(FadeIn(order), FadeIn(line))
        for dot, label in zip(spectrum_dots, spectrum_labels):
            self.play(FadeIn(dot), FadeIn(label), run_time=0.42)
        self.play(FadeIn(spectrum_note))
        self.wait(3.0)

        # Card 3: verify the exact second eigenpair structurally.
        heading = self._replace_heading(
            heading, "The first mode above zero changes slowly across the graph."
        )
        self.play(FadeOut(order), FadeOut(line), FadeOut(spectrum_dots), FadeOut(spectrum_labels), FadeOut(spectrum_note))
        laplacian = self._matrix(
            [["2", "-1", "-1", "0"], ["-1", "2", "-1", "0"], ["-1", "-1", "3", "-1"], ["0", "0", "-1", "1"]],
            scale=0.48,
            h_buff=0.72,
            v_buff=0.62,
        )
        vector_left = self._matrix([["1"], ["1"], ["0"], ["-2"]], scale=0.58, v_buff=0.64)
        vector_right = self._matrix([["1"], ["1"], ["0"], ["-2"]], scale=0.58, v_buff=0.64)
        eigenpair = VGroup(
            laplacian,
            vector_left,
            MathTex(r"=1", font_size=40, color=ORANGE),
            vector_right,
        ).arrange(RIGHT, buff=0.16).move_to(UP * 0.28)
        mode_name = MathTex(r"\mathbf v_2=(1,1,0,-2)^T,\qquad \lambda_2=1", font_size=39, color=YELLOW).move_to(DOWN * 1.24)
        mode_note = Text("The entries sum to zero, so this mode is perpendicular to the constant mode.", font_size=24, color=TEAL_C).to_edge(DOWN, buff=0.68)
        mode_note.scale_to_fit_width(10.8)
        self.play(FadeIn(eigenpair[:-2]))
        self.play(FadeIn(eigenpair[-2:]), FadeIn(mode_name))
        self.play(FadeIn(mode_note))
        self.wait(3.1)

        # Card 4: place the second mode on the graph and compute its energy.
        heading = self._replace_heading(
            heading, "Its largest change occurs across the lone edge leading to vertex 4."
        )
        self.play(FadeOut(eigenpair), FadeOut(mode_name), FadeOut(mode_note))
        graph, positions, edges, dots, labels = self._graph(shift=LEFT * 2.72 + DOWN * 0.08)
        mode_values = VGroup(
            MathTex(r"1", font_size=27, color=TEAL_C).next_to(labels[1], UP + LEFT, buff=0.22),
            MathTex(r"1", font_size=27, color=TEAL_C).next_to(labels[2], DOWN + LEFT, buff=0.22),
            MathTex(r"0", font_size=27, color=YELLOW).next_to(labels[3], UP, buff=0.24),
            MathTex(r"-2", font_size=27, color=ORANGE).next_to(labels[4], RIGHT, buff=0.21),
        )
        edge_terms = VGroup(
            MathTex(r"0", font_size=25, color=GREY_B).move_to((positions[1] + positions[2]) / 2 + LEFT * 0.46),
            MathTex(r"1", font_size=25, color=TEAL_C).move_to((positions[2] + positions[3]) / 2 + DOWN * 0.36),
            MathTex(r"1", font_size=25, color=TEAL_C).move_to((positions[1] + positions[3]) / 2 + UP * 0.36),
            MathTex(r"4", font_size=27, color=ORANGE).move_to((positions[3] + positions[4]) / 2 + UP * 0.36),
        )
        energy = VGroup(
            self._card("SQUARED EDGE CHANGES", r"0+1+1+4=6", "the bridge contributes the largest share", ORANGE, width=4.85),
            MathTex(r"\mathbf v_2^TL\mathbf v_2=6", font_size=41, color=GREEN_C),
        ).arrange(DOWN, buff=0.42).to_edge(RIGHT, buff=0.39).shift(DOWN * 0.02)
        self.play(FadeIn(graph), FadeIn(mode_values))
        for edge, term, color in zip(edges.values(), edge_terms, (GREY_B, TEAL_C, TEAL_C, ORANGE)):
            self.play(ShowPassingFlash(edge.copy().set_color(color).set_stroke(width=9)), FadeIn(term), run_time=0.60)
        self.play(FadeIn(energy))
        self.wait(3.0)

        # Card 5: normalize energy by vector length with the Rayleigh quotient.
        heading = self._replace_heading(
            heading, "To compare directions fairly, divide their energy by their squared length."
        )
        self.play(FadeOut(graph), FadeOut(mode_values), FadeOut(edge_terms), FadeOut(energy))
        quotient = VGroup(
            Text("RAYLEIGH QUOTIENT", font_size=25, color=YELLOW, weight="BOLD"),
            MathTex(r"R(\mathbf x)=\frac{\mathbf x^TL\mathbf x}{\mathbf x^T\mathbf x}", font_size=47, color=WHITE),
            MathTex(r"R(\mathbf v_2)=\frac{6}{1^2+1^2+0^2+(-2)^2}=\frac66=1", font_size=41, color=GREEN_C),
            Text("variation per unit of squared size", font_size=25, color=TEAL_C),
        ).arrange(DOWN, buff=0.40).move_to(DOWN * 0.02)
        scale_note = Text("Scaling a vector changes neither this quotient nor its direction.", font_size=24, color=ORANGE).to_edge(DOWN, buff=0.68)
        self.play(FadeIn(quotient[0]), FadeIn(quotient[1]))
        self.play(FadeIn(quotient[2]), FadeIn(quotient[3]))
        self.play(FadeIn(scale_note))
        self.wait(3.2)

        # Card 6: characterize lambda_2 by the least nonconstant energy quotient.
        heading = self._replace_heading(
            heading, "Exclude the constant direction, then seek the least possible normalized variation."
        )
        self.play(FadeOut(quotient), FadeOut(scale_note))
        restriction = self._card(
            "REMOVE THE CONSTANT MODE",
            r"\mathbf x^T\mathbf 1=0\quad\Longleftrightarrow\quad x_1+\cdots+x_n=0",
            "look only in directions perpendicular to all constants",
            TEAL_C,
            width=9.45,
        )
        minimum = MathTex(
            r"\lambda_2=\min_{\mathbf x\ne\mathbf 0,\ \mathbf x\perp\mathbf 1}"
            r"\frac{\mathbf x^TL\mathbf x}{\mathbf x^T\mathbf x}",
            font_size=45,
            color=GREEN_C,
        )
        meaning = Text("λ₂ is the cheapest nonconstant pattern of variation.", font_size=26, color=YELLOW)
        minimization = VGroup(restriction, minimum, meaning).arrange(DOWN, buff=0.48).move_to(DOWN * 0.03)
        self.play(FadeIn(minimization[0]))
        self.play(FadeIn(minimization[1]))
        self.play(FadeIn(minimization[2]))
        self.wait(3.2)

        # Card 7: define the gap and connect its positivity to connectedness.
        heading = self._replace_heading(
            heading, "The second-smallest Laplacian eigenvalue is called the spectral gap."
        )
        self.play(FadeOut(minimization))
        gap = VGroup(
            self._card("SPECTRAL GAP", r"\lambda_2", "also called algebraic connectivity", YELLOW, width=5.10),
            VGroup(
                self._card("CONNECTED", r"\lambda_2>0", "only one zero direction", TEAL_C, width=4.75),
                self._card("DISCONNECTED", r"\lambda_2=0", "at least two zero directions", ORANGE, width=4.75),
            ).arrange(RIGHT, buff=0.48),
            Text("The gap closes exactly when the graph separates.", font_size=26, color=GREEN_C),
        ).arrange(DOWN, buff=0.46).move_to(DOWN * 0.03)
        self.play(FadeIn(gap[0]))
        self.play(FadeIn(gap[1][0]), FadeIn(gap[1][1]))
        self.play(FadeIn(gap[2]))
        self.wait(3.2)

        # Card 8: compare spectra before and after deleting the bridge.
        heading = self._replace_heading(
            heading, "Deleting the bridge turns the second eigenvalue into another zero."
        )
        self.play(FadeOut(gap))
        spectra = VGroup(
            self._card("CONNECTED", r"0,\ \boxed{1},\ 3,\ 4", "bridge present: λ₂ = 1", TEAL_C, width=5.20),
            MathTex(r"\xrightarrow{\ \text{remove }\{3,4\}\ }", font_size=36, color=ORANGE),
            self._card("TWO COMPONENTS", r"0,\ \boxed{0},\ 3,\ 3", "bridge absent: λ₂ = 0", ORANGE, width=5.20),
        ).arrange(RIGHT, buff=0.31).move_to(UP * 0.30)
        interpretation = VGroup(
            Text("The extra component creates an extra zero mode.", font_size=26, color=GREEN_C),
            Text("A smaller positive gap signals a lower-energy way to vary across the graph.", font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.30).to_edge(DOWN, buff=0.69)
        self.play(FadeIn(spectra[0]))
        self.play(FadeIn(spectra[1]), FadeIn(spectra[2]))
        self.play(FadeIn(interpretation))
        self.wait(3.2)

        # Card 9: synthesize and preview the Fiedler vector.
        heading = self._replace_heading(
            heading, "The low end of the Laplacian spectrum summarizes connectivity."
        )
        self.play(FadeOut(spectra), FadeOut(interpretation))
        synthesis = VGroup(
            self._card("ZEROS", r"\#\{\lambda_i=0\}", "number of components", TEAL_C, width=3.45),
            self._card("GAP", r"\lambda_2", "strength above disconnection", ORANGE, width=3.45),
            self._card("SECOND MODE", r"L\mathbf v_2=\lambda_2\mathbf v_2", "cheapest nonconstant variation", GREEN_C, width=3.45),
        ).arrange(RIGHT, buff=0.34).move_to(UP * 0.35)
        fiedler = Text("The eigenvector v₂ is called a Fiedler vector.", font_size=27, color=YELLOW).move_to(DOWN * 1.18)
        next_question = Text("Can its signs reveal a useful division of the vertices?", font_size=25, color=TEAL_C).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(synthesis))
        self.play(FadeIn(fiedler))
        self.play(FadeIn(next_question))
        self.wait(3.4)
