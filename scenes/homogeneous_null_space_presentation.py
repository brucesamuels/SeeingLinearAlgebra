"""CP115 presentation: homogeneous systems, null space, and multiple special solutions."""

from __future__ import annotations

from manim import (
    Arrow,
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
    NumberPlane,
    ORIGIN,
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

from engine.homogeneous_null_space import HomogeneousNullSpace


class HomogeneousNullSpacePresentation(Scene):
    """Connect homogeneous solutions, null spaces, and particular-plus-special solutions."""

    def construct(self) -> None:
        model = HomogeneousNullSpace()
        snapshot = model.snapshot()

        title = Text("Homogeneous Systems and the Null Space", font_size=39).to_edge(UP, buff=0.26)
        subtitle = Text(
            "What changes when the right-hand side is the zero vector?",
            font_size=24,
        ).next_to(title, DOWN, buff=0.13)
        subtitle.scale_to_fit_width(11.6)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        heading = Text("A homogeneous system has the form A x = 0", font_size=29).move_to(UP * 1.84)
        matrix, display = self._augmented_matrix(snapshot.homogeneous_rref_augmented)
        display.move_to(LEFT * 3.05 + DOWN * 0.28)
        variable_labels = self._variable_labels(matrix)
        concept_panel = self._homogeneous_panel().move_to(RIGHT * 3.18 + DOWN * 0.05)
        footer = Text(
            "The zero vector is always a solution—but it may not be the only one.",
            font_size=23,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        footer.scale_to_fit_width(11.2)
        self.play(FadeIn(heading), FadeIn(display), FadeIn(variable_labels), FadeIn(concept_panel), FadeIn(footer), run_time=1.2)
        self.wait(2.0)

        rhs_box = SurroundingRectangle(matrix.get_columns()[3], color=YELLOW, buff=0.11)
        self.play(Create(rhs_box), run_time=0.7)
        self.wait(0.9)
        self.play(FadeOut(rhs_box), run_time=0.5)

        prompt = VGroup(
            Text("Pause and Predict", font_size=28, color=YELLOW),
            Text("Can a homogeneous system have a nonzero solution?", font_size=24),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.28)
        self.play(FadeOut(footer), FadeIn(prompt), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(prompt), run_time=0.6)

        derive_heading = Text("A free variable can produce nonzero solutions", font_size=29).move_to(UP * 1.84)
        derivation_panel = self._derivation_panel(snapshot.homogeneous_scalar_equations_tex).move_to(RIGHT * 3.18 + DOWN * 0.05)
        free_box = SurroundingRectangle(matrix.get_columns()[2], color=YELLOW, buff=0.11)
        self.play(
            ReplacementTransform(heading, derive_heading),
            ReplacementTransform(concept_panel, derivation_panel),
            Create(free_box),
            run_time=1.1,
        )
        self.wait(2.6)

        special_heading = Text("Strang's special solution", font_size=30).move_to(UP * 1.84)
        special_card = self._special_solution_card().move_to(LEFT * 3.08 + DOWN * 0.15)
        all_card = self._all_solutions_card().move_to(RIGHT * 3.08 + DOWN * 0.15)
        special_footer = Text(
            "Setting t = 0 gives the zero solution; every other t gives another point on the same line.",
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        special_footer.scale_to_fit_width(11.1)
        self.play(
            ReplacementTransform(derive_heading, special_heading),
            FadeOut(display),
            FadeOut(variable_labels),
            FadeOut(derivation_panel),
            FadeOut(free_box),
            FadeIn(special_card),
            FadeIn(all_card),
            FadeIn(special_footer),
            run_time=1.2,
        )
        self.wait(2.2)

        null_heading = Text("The null space of A", font_size=30).move_to(UP * 1.84)
        null_panel = self._null_space_panel(snapshot.null_space_span_tex).move_to(RIGHT * 3.20 + UP * 0.18)
        geometry = self._null_space_geometry().move_to(LEFT * 3.00 + DOWN * 0.55)
        geometry_footer = Text(
            "All multiples of the special solution form a line through the origin.",
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        geometry_footer.scale_to_fit_width(11.1)
        self.play(
            ReplacementTransform(special_heading, null_heading),
            FadeOut(special_card),
            FadeOut(all_card),
            FadeOut(special_footer),
            FadeIn(geometry),
            FadeIn(null_panel),
            FadeIn(geometry_footer),
            run_time=1.2,
        )
        self.wait(2.8)

        rank_heading = Text("A rank-1 system with two free variables", font_size=29).move_to(UP * 1.84)
        rank_matrix, rank_display = self._augmented_matrix(snapshot.rank_one_rref_augmented)
        rank_display.move_to(LEFT * 3.05 + DOWN * 0.28)
        rank_labels = self._variable_labels(rank_matrix)
        rank_panel = self._rank_one_derivation_panel(snapshot.rank_one_scalar_equations_tex).move_to(RIGHT * 3.18 + DOWN * 0.05)
        y_box = SurroundingRectangle(rank_matrix.get_columns()[1], color=BLUE, buff=0.11)
        z_box = SurroundingRectangle(rank_matrix.get_columns()[2], color=GREEN, buff=0.11)
        rank_footer = Text(
            "Now there are two free variables, so we should expect two independent null-space directions.",
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        rank_footer.scale_to_fit_width(11.15)
        self.play(
            ReplacementTransform(null_heading, rank_heading),
            FadeOut(geometry),
            FadeOut(null_panel),
            FadeOut(geometry_footer),
            FadeIn(rank_display),
            FadeIn(rank_labels),
            FadeIn(rank_panel),
            FadeIn(rank_footer),
            Create(y_box),
            Create(z_box),
            run_time=1.25,
        )
        self.wait(2.7)

        explicit_heading = Text("Introduce the particular solution explicitly", font_size=29).move_to(UP * 1.84)
        decomposition = self._decomposition_panel(snapshot.rank_one_solution_tex).move_to(DOWN * 0.08)
        for label in decomposition[2:5]:
            label.set_opacity(0)
        self.play(
            ReplacementTransform(rank_heading, explicit_heading),
            FadeOut(rank_display),
            FadeOut(rank_labels),
            FadeOut(rank_panel),
            FadeOut(rank_footer),
            FadeOut(y_box),
            FadeOut(z_box),
            FadeIn(decomposition),
            run_time=1.2,
        )
        self.wait(2.3)

        particular_box = SurroundingRectangle(decomposition[1][1][1], color=YELLOW, buff=0.10)
        first_special_box = SurroundingRectangle(decomposition[1][1][3], color=BLUE, buff=0.10)
        second_special_box = SurroundingRectangle(decomposition[1][1][5], color=GREEN, buff=0.10)
        particular_label = decomposition[2]
        first_special_label = decomposition[3]
        second_special_label = decomposition[4]
        self.play(Create(particular_box), particular_label.animate.set_opacity(1), run_time=0.7)
        self.wait(0.7)
        self.play(Create(first_special_box), first_special_label.animate.set_opacity(1), run_time=0.7)
        self.wait(0.7)
        self.play(Create(second_special_box), second_special_label.animate.set_opacity(1), run_time=0.7)
        self.wait(1.5)

        compare_heading = Text("Homogeneous vs. nonhomogeneous structure", font_size=29).move_to(UP * 1.84)
        left_card = self._comparison_card(
            heading="Homogeneous: A x = 0",
            equation_tex=r"\mathbf{x}=s\mathbf{s}_1+t\mathbf{s}_2",
            description="only null-space combinations",
            line_color=GREEN,
            translated=False,
        ).move_to(LEFT * 3.15 + DOWN * 0.08)
        right_card = self._comparison_card(
            heading="Nonhomogeneous: A x = b",
            equation_tex=r"\mathbf{x}=\mathbf{x}_p+s\mathbf{s}_1+t\mathbf{s}_2",
            description="particular solution plus null-space combinations",
            line_color=BLUE,
            translated=True,
        ).move_to(RIGHT * 3.15 + DOWN * 0.08)
        compare_footer = Text(
            "The null-space directions stay the same; the particular solution translates the set away from the origin.",
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        compare_footer.scale_to_fit_width(11.2)
        self.play(
            ReplacementTransform(explicit_heading, compare_heading),
            FadeOut(decomposition),
            FadeOut(particular_box),
            FadeOut(first_special_box),
            FadeOut(second_special_box),
            FadeIn(left_card),
            FadeIn(right_card),
            FadeIn(compare_footer),
            run_time=1.25,
        )
        self.wait(3.4)

    def _augmented_matrix(self, values):
        formatted = [[self._format_number(v) for v in row] for row in values]
        matrix = Matrix(formatted, h_buff=0.88, v_buff=0.68).scale(0.93)
        columns = matrix.get_columns()
        separator_x = (columns[2].get_right()[0] + columns[3].get_left()[0]) / 2
        separator = Line(UP * 1.22, DOWN * 1.22, stroke_width=2.0).move_to([separator_x, matrix.get_center()[1], 0])
        return matrix, VGroup(matrix, separator)

    @staticmethod
    def _variable_labels(matrix: Matrix):
        labels = VGroup(
            MathTex("x", font_size=30, color=BLUE),
            MathTex("y", font_size=30, color=GREEN),
            MathTex("z", font_size=30, color=YELLOW),
        )
        for label, column in zip(labels, matrix.get_columns()[:3], strict=True):
            label.move_to([column.get_center()[0], matrix.get_top()[1] + 0.22, 0])
        return labels

    @staticmethod
    def _homogeneous_panel():
        heading = Text("Homogeneous", font_size=28, color=YELLOW)
        formula = MathTex(r"A\mathbf{x}=\mathbf{0}", font_size=42)
        zero = MathTex(r"\mathbf{x}=\mathbf{0}\quad\text{always works}", font_size=31, color=GREEN)
        group = VGroup(heading, formula, zero).arrange(DOWN, buff=0.34)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _derivation_panel(equations_tex: tuple[str, ...]):
        heading = Text("Let the free variable be z = t", font_size=27, color=YELLOW)
        equations = VGroup(
            MathTex(equations_tex[0], font_size=31),
            MathTex(equations_tex[1], font_size=31),
            MathTex(equations_tex[2], font_size=33, color=YELLOW),
            MathTex(equations_tex[3], font_size=34, color=BLUE),
            MathTex(equations_tex[4], font_size=34, color=GREEN),
        ).arrange(DOWN, buff=0.18)
        group = VGroup(heading, equations).arrange(DOWN, buff=0.30)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _special_solution_card():
        heading = Text("Set the free variable to 1", font_size=27, color=YELLOW)
        line = MathTex(r"z=1", font_size=35, color=YELLOW)
        equations = MathTex(r"x=-2,\qquad y=1", font_size=33)
        vector = MathTex(r"\mathbf{s}=\begin{bmatrix}-2\\1\\1\end{bmatrix}", font_size=40, color=GREEN)
        group = VGroup(heading, line, equations, vector).arrange(DOWN, buff=0.25)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _all_solutions_card():
        heading = Text("All homogeneous solutions", font_size=27, color=YELLOW)
        parameter = MathTex(r"z=t", font_size=35, color=YELLOW)
        formula = MathTex(r"\mathbf{x}=t\mathbf{s}", font_size=42, color=GREEN)
        expanded = MathTex(r"\mathbf{x}=t\begin{bmatrix}-2\\1\\1\end{bmatrix}", font_size=37)
        group = VGroup(heading, parameter, formula, expanded).arrange(DOWN, buff=0.25)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _null_space_panel(span_tex: str):
        heading = Text("The null space of A", font_size=28, color=YELLOW)
        definition = MathTex(r"N(A)=\{\mathbf{x}:A\mathbf{x}=\mathbf{0}\}", font_size=32)
        span = MathTex(span_tex, font_size=34)
        group = VGroup(heading, definition, span).arrange(DOWN, buff=0.36)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _null_space_geometry():
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            x_length=7.2,
            y_length=2.7,
            background_line_style={"stroke_opacity": 0.20},
            axis_config={"stroke_opacity": 0.45},
        )
        line = Line(plane.c2p(-3.2, -1.3), plane.c2p(3.2, 1.3), color=GREEN, stroke_width=5)
        origin = Dot(plane.c2p(0, 0), color=RED, radius=0.07)
        arrow = Arrow(plane.c2p(0, 0), plane.c2p(1.45, 0.59), buff=0, color=GREEN, stroke_width=5)
        multiples = VGroup()
        labels = (r"-2\mathbf{s}", r"-\mathbf{s}", r"\mathbf{0}", r"\mathbf{s}", r"2\mathbf{s}")
        for index, t in enumerate((-2, -1, 0, 1, 2)):
            point = plane.c2p(1.45 * t, 0.59 * t)
            dot = Dot(point, color=RED if t == 0 else GREEN, radius=0.055)
            label = MathTex(labels[index], font_size=24)
            label.next_to(dot, UP if t >= 0 else DOWN, buff=0.10)
            multiples.add(dot, label)
        return VGroup(plane, line, origin, arrow, multiples).scale(0.82)

    @staticmethod
    def _rank_one_derivation_panel(equations_tex: tuple[str, ...]):
        heading = Text("Choose values for the two free variables", font_size=27, color=YELLOW)
        equations = VGroup(
            MathTex(equations_tex[0], font_size=31),
            MathTex(equations_tex[1], font_size=32, color=BLUE),
            MathTex(equations_tex[2], font_size=32, color=GREEN),
            MathTex(equations_tex[3], font_size=33),
        ).arrange(DOWN, buff=0.20)
        group = VGroup(heading, equations).arrange(DOWN, buff=0.30)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _decomposition_panel(solution_tex: str):
        heading = Text("One particular solution plus two special solutions", font_size=28, color=YELLOW)
        equation = MathTex(
            r"\mathbf{x}=",
            r"\begin{bmatrix}3\\0\\0\end{bmatrix}",
            r"+s",
            r"\begin{bmatrix}-2\\1\\0\end{bmatrix}",
            r"+t",
            r"\begin{bmatrix}1\\0\\1\end{bmatrix}",
            font_size=36,
        )
        label_band = Line(LEFT * 4.8, RIGHT * 4.8, stroke_opacity=0).set_height(0.75)
        note = Text(
            "The special solutions come from the associated homogeneous system.",
            font_size=22,
            color=YELLOW,
        )
        note.scale_to_fit_width(11.0)
        group = VGroup(heading, equation, label_band, note).arrange(DOWN, buff=0.34)

        particular_label = Text("particular\nsolution", font_size=18, color=YELLOW)
        first_special_label = Text("special\nsolution 1", font_size=18, color=BLUE)
        second_special_label = Text("special\nsolution 2", font_size=18, color=GREEN)
        labels = [particular_label, first_special_label, second_special_label]
        targets = [equation[1], equation[3], equation[5]]
        for label, target in zip(labels, targets, strict=True):
            label.move_to([target.get_center()[0], label_band.get_center()[1], 0])

        box = SurroundingRectangle(VGroup(group, particular_label, first_special_label, second_special_label), color=YELLOW, buff=0.18)
        return VGroup(box, group, particular_label, first_special_label, second_special_label)

    @staticmethod
    def _comparison_card(*, heading: str, equation_tex: str, description: str, line_color, translated: bool):
        title = Text(heading, font_size=24, color=YELLOW)
        equation = MathTex(equation_tex, font_size=34)
        origin = Dot(ORIGIN, color=RED, radius=0.055)
        baseline_y = 0.42 if translated else 0.0
        line = Line(LEFT * 1.55 + UP * baseline_y, RIGHT * 1.55 + UP * baseline_y, color=line_color, stroke_width=5)
        if translated:
            origin.shift(DOWN * 0.40)
        diagram = VGroup(line, origin)
        caption = Text(description, font_size=21, color=line_color)
        group = VGroup(title, equation, diagram, caption).arrange(DOWN, buff=0.27)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
