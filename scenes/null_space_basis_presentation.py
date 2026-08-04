"""CP116 presentation: building a basis for the null space."""

from __future__ import annotations

from manim import (
    BLUE,
    Create,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    Line,
    MathTex,
    Matrix,
    ORIGIN,
    Polygon,
    RED,
    ReplacementTransform,
    RIGHT,
    Scene,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from engine.null_space_basis import NullSpaceBasis


class NullSpaceBasisPresentation(Scene):
    """Construct, verify, and visualize a basis for N(A)."""

    def construct(self) -> None:
        model = NullSpaceBasis()
        snapshot = model.snapshot()

        title = Text("A Basis for the Null Space", font_size=40).to_edge(UP, buff=0.27)
        subtitle = Text(
            "Build one special solution for each free variable.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.13)
        subtitle.scale_to_fit_width(11.5)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        heading = Text("Start from the homogeneous RREF system", font_size=29).move_to(UP * 1.86)
        matrix, display = self._augmented_matrix(snapshot.rref_augmented)
        display.move_to(LEFT * 3.10 + DOWN * 0.24)
        variable_labels = self._variable_labels(matrix)
        roles_panel = self._roles_panel().move_to(RIGHT * 3.18 + DOWN * 0.05)
        footer = Text(
            "The y- and z-columns have no pivots, so y and z are free variables.",
            font_size=23,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        footer.scale_to_fit_width(11.2)
        self.play(
            FadeIn(heading),
            FadeIn(display),
            FadeIn(variable_labels),
            FadeIn(roles_panel),
            FadeIn(footer),
            run_time=1.2,
        )
        self.wait(2.0)

        y_box = SurroundingRectangle(matrix.get_columns()[1], color=BLUE, buff=0.11)
        z_box = SurroundingRectangle(matrix.get_columns()[2], color=GREEN, buff=0.11)
        self.play(Create(y_box), Create(z_box), run_time=0.9)
        self.wait(1.4)

        prompt = VGroup(
            Text("Pause and Predict", font_size=28, color=YELLOW),
            Text("How many special solutions should two free variables produce?", font_size=24),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.28)
        self.play(FadeOut(footer), FadeIn(prompt), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(prompt), run_time=0.6)

        special_heading = Text("Turn on one free variable at a time", font_size=29).move_to(UP * 1.86)
        special_panel, first_vector, second_vector = self._special_solution_panel()
        special_panel.move_to(DOWN * 0.28)
        self.play(
            ReplacementTransform(heading, special_heading),
            FadeOut(display),
            FadeOut(variable_labels),
            FadeOut(roles_panel),
            FadeOut(y_box),
            FadeOut(z_box),
            FadeIn(special_panel),
            run_time=1.2,
        )
        self.wait(2.4)

        first_box = SurroundingRectangle(first_vector, color=BLUE, buff=0.11)
        second_box = SurroundingRectangle(second_vector, color=GREEN, buff=0.11)
        self.play(Create(first_box), run_time=0.7)
        self.wait(0.8)
        self.play(Create(second_box), run_time=0.7)
        self.wait(1.4)

        verify_heading = Text("First check: both vectors lie in N(A)", font_size=29).move_to(UP * 2.04)
        verify_panel = self._verification_panel().move_to(DOWN * 0.28)
        self.play(
            ReplacementTransform(special_heading, verify_heading),
            FadeOut(first_box),
            FadeOut(second_box),
            ReplacementTransform(special_panel, verify_panel),
            run_time=1.15,
        )
        self.wait(2.5)

        span_heading = Text("Second check: they span every null-space solution", font_size=29).move_to(UP * 2.04)
        span_panel = self._span_panel().move_to(DOWN * 0.30)
        self.play(
            ReplacementTransform(verify_heading, span_heading),
            ReplacementTransform(verify_panel, span_panel),
            run_time=1.15,
        )
        self.wait(2.6)

        independent_heading = Text("Third check: the two vectors are independent", font_size=29).move_to(UP * 1.86)
        independent_panel = self._independence_panel().move_to(DOWN * 0.30)
        self.play(
            ReplacementTransform(span_heading, independent_heading),
            ReplacementTransform(span_panel, independent_panel),
            run_time=1.15,
        )
        self.wait(2.7)

        basis_heading = Text("Therefore these vectors form a basis for N(A)", font_size=29).move_to(UP * 1.86)
        basis_panel = self._basis_panel().move_to(RIGHT * 3.15 + DOWN * 0.05)
        geometry = self._null_space_plane().move_to(LEFT * 3.05 + DOWN * 0.35)
        geometry_footer = Text(
            "Two independent directions span a plane through the origin in R³.",
            font_size=23,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        geometry_footer.scale_to_fit_width(11.1)
        self.play(
            ReplacementTransform(independent_heading, basis_heading),
            FadeOut(independent_panel),
            FadeIn(geometry),
            FadeIn(basis_panel),
            FadeIn(geometry_footer),
            run_time=1.25,
        )
        self.wait(3.0)

        summary_heading = Text("Free variables determine null-space dimension", font_size=29).move_to(UP * 1.86)
        summary_panel = self._summary_panel().move_to(DOWN * 0.42)
        self.play(
            ReplacementTransform(basis_heading, summary_heading),
            FadeOut(geometry),
            FadeOut(basis_panel),
            FadeOut(geometry_footer),
            FadeIn(summary_panel),
            run_time=1.2,
        )
        self.wait(3.5)

    def _augmented_matrix(self, values):
        formatted = [[self._format_number(v) for v in row] for row in values]
        matrix = Matrix(formatted, h_buff=0.88, v_buff=0.68).scale(0.93)
        columns = matrix.get_columns()
        separator_x = (columns[2].get_right()[0] + columns[3].get_left()[0]) / 2
        separator = Line(UP * 1.22, DOWN * 1.22, stroke_width=2.0).move_to(
            [separator_x, matrix.get_center()[1], 0]
        )
        return matrix, VGroup(matrix, separator)

    @staticmethod
    def _variable_labels(matrix: Matrix):
        labels = VGroup(
            MathTex("x", font_size=30, color=YELLOW),
            MathTex("y", font_size=30, color=BLUE),
            MathTex("z", font_size=30, color=GREEN),
        )
        for label, column in zip(labels, matrix.get_columns()[:3], strict=True):
            label.move_to([column.get_center()[0], matrix.get_top()[1] + 0.22, 0])
        return labels

    @staticmethod
    def _roles_panel():
        heading = Text("Pivot and free variables", font_size=27, color=YELLOW)
        equation = MathTex(r"x+2y-z=0", font_size=36)
        pivot = Text("x: pivot variable", font_size=23, color=YELLOW)
        free = VGroup(
            Text("y: free variable", font_size=23, color=BLUE),
            Text("z: free variable", font_size=23, color=GREEN),
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        group = VGroup(heading, equation, pivot, free).arrange(DOWN, buff=0.28)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _special_solution_panel():
        first_title = Text("Set y = 1, z = 0", font_size=24, color=BLUE)
        first_equation = MathTex(r"x=-2", font_size=32)
        first_vector = MathTex(
            r"\mathbf{s}_1=\begin{bmatrix}-2\\1\\0\end{bmatrix}",
            font_size=39,
            color=BLUE,
        )
        first_card = VGroup(first_title, first_equation, first_vector).arrange(DOWN, buff=0.22)

        second_title = Text("Set y = 0, z = 1", font_size=24, color=GREEN)
        second_equation = MathTex(r"x=1", font_size=32)
        second_vector = MathTex(
            r"\mathbf{s}_2=\begin{bmatrix}1\\0\\1\end{bmatrix}",
            font_size=39,
            color=GREEN,
        )
        second_card = VGroup(second_title, second_equation, second_vector).arrange(DOWN, buff=0.22)

        cards = VGroup(first_card, second_card).arrange(RIGHT, buff=1.25, aligned_edge=UP)
        instruction = Text(
            "The free-variable entries form the coordinate unit patterns (1,0) and (0,1).",
            font_size=22,
            color=YELLOW,
        )
        instruction.scale_to_fit_width(11.0)
        group = VGroup(cards, instruction).arrange(DOWN, buff=0.52)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group), first_vector, second_vector

    @staticmethod
    def _verification_panel():
        first = MathTex(
            r"A\mathbf{s}_1="
            r"\begin{bmatrix}1&2&-1\end{bmatrix}"
            r"\begin{bmatrix}-2\\1\\0\end{bmatrix}=0",
            font_size=35,
            color=BLUE,
        )
        second = MathTex(
            r"A\mathbf{s}_2="
            r"\begin{bmatrix}1&2&-1\end{bmatrix}"
            r"\begin{bmatrix}1\\0\\1\end{bmatrix}=0",
            font_size=35,
            color=GREEN,
        )
        conclusion = Text("Both vectors belong to N(A).", font_size=25, color=YELLOW)
        group = VGroup(first, second, conclusion).arrange(DOWN, buff=0.48)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _span_panel():
        scalar = MathTex(r"y=s,\qquad z=t,\qquad x=-2s+t", font_size=35, color=YELLOW)
        vector = MathTex(
            r"\mathbf{x}="
            r"s\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
            r"t\begin{bmatrix}1\\0\\1\end{bmatrix}",
            font_size=39,
        )
        span = MathTex(
            r"N(A)=\operatorname{span}\left\{\mathbf{s}_1,\mathbf{s}_2\right\}",
            font_size=39,
            color=YELLOW,
        )
        conclusion = Text("Every null-space vector is a combination of the two special solutions.", font_size=23)
        conclusion.scale_to_fit_width(11.0)
        group = VGroup(scalar, vector, span, conclusion).arrange(DOWN, buff=0.38)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _independence_panel():
        equation = MathTex(
            r"c_1\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
            r"c_2\begin{bmatrix}1\\0\\1\end{bmatrix}="
            r"\begin{bmatrix}0\\0\\0\end{bmatrix}",
            font_size=37,
        )
        coordinate_readout = VGroup(
            MathTex(r"\text{second coordinate: }c_1=0", font_size=34, color=BLUE),
            MathTex(r"\text{third coordinate: }c_2=0", font_size=34, color=GREEN),
        ).arrange(DOWN, buff=0.26)
        conclusion = Text("Only the trivial combination works, so the vectors are independent.", font_size=23, color=YELLOW)
        conclusion.scale_to_fit_width(11.0)
        group = VGroup(equation, coordinate_readout, conclusion).arrange(DOWN, buff=0.44)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _basis_panel():
        heading = Text("Basis and dimension", font_size=28, color=YELLOW)
        basis = MathTex(
            r"\mathcal{B}_{N(A)}="
            r"\left\{"
            r"\begin{bmatrix}-2\\1\\0\end{bmatrix},"
            r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
            r"\right\}",
            font_size=34,
        )
        dimension = MathTex(r"\dim N(A)=2", font_size=39, color=YELLOW)
        group = VGroup(heading, basis, dimension).arrange(DOWN, buff=0.38)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _null_space_plane():
        plane = Polygon(
            LEFT * 2.35 + DOWN * 0.85,
            RIGHT * 1.90 + DOWN * 0.55,
            RIGHT * 2.35 + UP * 0.85,
            LEFT * 1.90 + UP * 0.55,
            color=GREEN,
            fill_opacity=0.16,
            stroke_width=3,
        )
        origin = Dot(ORIGIN, color=RED, radius=0.065)
        s1 = Line(ORIGIN, LEFT * 1.35 + UP * 0.52, color=BLUE, stroke_width=6)
        s2 = Line(ORIGIN, RIGHT * 1.15 + UP * 0.68, color=GREEN, stroke_width=6)
        s1_label = MathTex(r"\mathbf{s}_1", font_size=28, color=BLUE).next_to(s1.get_end(), UP, buff=0.10)
        s2_label = MathTex(r"\mathbf{s}_2", font_size=28, color=GREEN).next_to(s2.get_end(), UP, buff=0.10)
        plane_label = MathTex(r"N(A)", font_size=34, color=YELLOW).move_to(DOWN * 1.25)
        return VGroup(plane, origin, s1, s2, s1_label, s2_label, plane_label)

    @staticmethod
    def _summary_panel():
        steps = VGroup(
            Text("1. Find the free variables.", font_size=25),
            Text("2. Turn on one free variable at a time.", font_size=25),
            Text("3. The resulting special solutions form a null-space basis.", font_size=25),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        count = MathTex(
            r"\#\text{ free variables}=\#\text{ basis vectors}=\dim N(A)",
            font_size=36,
            color=YELLOW,
        )
        rank_nullity = MathTex(r"1+2=3\qquad(\operatorname{rank}A+\operatorname{nullity}A=3)", font_size=33)
        note = Text("A particular solution is not part of a basis for N(A) unless it also solves A x = 0.", font_size=22, color=BLUE)
        note.scale_to_fit_width(11.0)
        group = VGroup(steps, count, rank_nullity, note).arrange(DOWN, buff=0.32)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
