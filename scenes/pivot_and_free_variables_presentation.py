"""CP114 presentation: parameter method and Strang's special-solution method."""

from __future__ import annotations

from manim import (
    BLUE,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    Line,
    MathTex,
    Matrix,
    RED,
    ReplacementTransform,
    RIGHT,
    Scene,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
)

from engine.pivot_and_free_variables import PivotAndFreeVariables


class PivotAndFreeVariablesPresentation(Scene):
    """Present pivot/free variables using both textbook and Strang viewpoints."""

    def construct(self) -> None:
        model = PivotAndFreeVariables()
        snapshot = model.snapshot()

        title = Text("Pivot and Free Variables", font_size=40).to_edge(UP, buff=0.28)
        subtitle = Text(
            "An infinite solution set can be described in more than one helpful way.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.14)
        subtitle.scale_to_fit_width(11.6)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        heading = Text("Read the pivot pattern", font_size=29).move_to(UP * 1.88)
        matrix, display = self._augmented_matrix(snapshot.rref_augmented)
        display.move_to(LEFT * 2.95 + DOWN * 0.22)
        variable_labels = self._variable_labels(matrix)
        roles_panel = self._roles_panel().move_to(RIGHT * 3.25 + DOWN * 0.10)
        footer = Text(
            "Pivot columns give pivot variables. A non-pivot column gives a free variable.",
            font_size=23,
        ).to_edge(DOWN, buff=0.30)
        footer.scale_to_fit_width(11.5)
        self.play(
            FadeIn(heading),
            FadeIn(display),
            FadeIn(variable_labels),
            FadeIn(roles_panel),
            FadeIn(footer),
            run_time=1.2,
        )
        self.wait(1.8)

        pivot_boxes = VGroup(
            SurroundingRectangle(matrix.get_columns()[0], color=BLUE, buff=0.11),
            SurroundingRectangle(matrix.get_columns()[1], color=GREEN, buff=0.11),
        )
        pivot_note = Text("Pivot columns: x and y", font_size=26, color=GREEN).move_to(LEFT * 2.95 + UP * 1.28)
        self.play(Create(pivot_boxes), FadeIn(pivot_note), run_time=0.9)
        self.wait(1.4)
        self.play(FadeOut(pivot_note), FadeOut(pivot_boxes), run_time=0.6)

        free_box = SurroundingRectangle(matrix.get_columns()[2], color=YELLOW, buff=0.11)
        free_note = Text("No pivot in the z-column: z is free", font_size=27, color=YELLOW).move_to(
            LEFT * 2.95 + UP * 1.28
        )
        self.play(Create(free_box), FadeIn(free_note), run_time=0.9)
        self.wait(1.8)

        prompt = VGroup(
            Text("Pause and Predict", font_size=28, color=YELLOW),
            Text("How can we describe every solution when z is free?", font_size=24),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.28)
        self.play(FadeOut(footer), FadeIn(prompt), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(prompt), run_time=0.6)

        parameter_heading = Text("Method 1: Let the free variable be z = t", font_size=29).move_to(UP * 1.88)
        parameter_panel = self._parameter_panel(snapshot.scalar_equations_tex).move_to(RIGHT * 3.25 + DOWN * 0.10)
        self.play(
            ReplacementTransform(heading, parameter_heading),
            FadeOut(free_note),
            FadeOut(free_box),
            ReplacementTransform(roles_panel, parameter_panel),
            run_time=1.0,
        )
        self.wait(2.5)

        param_heading = Text("Textbook parameter form", font_size=29).move_to(UP * 1.88)
        parametric = self._parametric_panel().move_to(DOWN * 0.05)
        self.play(
            ReplacementTransform(parameter_heading, param_heading),
            FadeOut(display),
            FadeOut(variable_labels),
            FadeOut(parameter_panel),
            FadeIn(parametric),
            run_time=1.1,
        )
        self.wait(2.0)

        method_note = Text(
            "Here t is the parameter that records the free variable.",
            font_size=24,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.28)
        method_note.scale_to_fit_width(11.2)
        self.play(FadeIn(method_note), run_time=0.7)
        self.wait(1.5)

        strang_heading = Text("Method 2: Strang's special-solution viewpoint", font_size=28).move_to(UP * 1.88)
        strang_panel = self._strang_panel().move_to(DOWN * 0.58)
        self.play(
            ReplacementTransform(param_heading, strang_heading),
            FadeOut(method_note),
            ReplacementTransform(parametric, strang_panel),
            run_time=1.2,
        )
        self.wait(2.8)

        particular_box = SurroundingRectangle(strang_panel[1][1][0], color=BLUE, buff=0.10)
        special_box = SurroundingRectangle(strang_panel[1][2][0], color=GREEN, buff=0.10)
        particular_label = Text("particular solution:\nset z = 0", font_size=20, color=BLUE).next_to(
            strang_panel[1][1][0], DOWN, buff=0.16
        )
        special_label = Text("special solution:\nset z = 1", font_size=20, color=GREEN).next_to(
            strang_panel[1][1][1], DOWN, buff=0.16
        )
        self.play(Create(particular_box), FadeIn(particular_label), run_time=0.8)
        self.wait(1.0)
        self.play(Create(special_box), FadeIn(special_label), run_time=0.8)
        self.wait(1.6)

        final_summary = self._final_summary().move_to(DOWN * 0.22)
        self.play(
            FadeOut(particular_box),
            FadeOut(special_box),
            FadeOut(particular_label),
            FadeOut(special_label),
            FadeOut(strang_heading),
            ReplacementTransform(strang_panel, final_summary),
            run_time=1.1,
        )
        self.wait(3.8)

    def _augmented_matrix(self, values):
        formatted = [[self._format_number(v) for v in row] for row in values]
        matrix = Matrix(formatted, h_buff=0.86, v_buff=0.66).scale(0.95)
        columns = matrix.get_columns()
        separator_x = (columns[2].get_right()[0] + columns[3].get_left()[0]) / 2
        separator = Line(UP * 1.20, DOWN * 1.20, stroke_width=2.0).move_to(
            [separator_x, matrix.get_center()[1], 0]
        )
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
    def _roles_panel():
        heading = Text("Variable roles", font_size=28, color=YELLOW)
        lines = VGroup(
            Text("x: pivot variable", font_size=24, color=BLUE),
            Text("y: pivot variable", font_size=24, color=GREEN),
            Text("z: free variable", font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        panel = VGroup(heading, lines).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        box = SurroundingRectangle(panel, color=YELLOW, buff=0.18)
        return VGroup(box, panel)

    @staticmethod
    def _parameter_panel(equations_tex: tuple[str, ...]):
        heading = Text("Textbook method", font_size=27, color=YELLOW)
        equations = VGroup(
            MathTex(equations_tex[0], font_size=31),
            MathTex(equations_tex[1], font_size=31),
            MathTex(equations_tex[2], font_size=33, color=YELLOW),
            MathTex(equations_tex[3], font_size=33, color=BLUE),
            MathTex(equations_tex[4], font_size=33, color=GREEN),
        ).arrange(DOWN, buff=0.18)
        panel = VGroup(heading, equations).arrange(DOWN, buff=0.28)
        box = SurroundingRectangle(panel, color=YELLOW, buff=0.18)
        return VGroup(box, panel)

    @staticmethod
    def _parametric_panel():
        heading = Text("Parametric vector form", font_size=29, color=YELLOW)
        equation = MathTex(
            r"\begin{bmatrix}x\\y\\z\end{bmatrix}=",
            r"\begin{bmatrix}4\\1\\0\end{bmatrix}",
            r"+t",
            r"\begin{bmatrix}-2\\1\\1\end{bmatrix}",
            font_size=42,
        )
        group = VGroup(heading, equation).arrange(DOWN, buff=0.48)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _strang_panel():
        heading = Text("Strang's viewpoint", font_size=29, color=YELLOW)
        cards = VGroup(
            VGroup(
                Text("Set z = 0", font_size=24, color=BLUE),
                MathTex(r"\begin{bmatrix}4\\1\\0\end{bmatrix}", font_size=40, color=BLUE),
            ).arrange(DOWN, buff=0.18),
            VGroup(
                Text("Set z = 1", font_size=24, color=GREEN),
                MathTex(r"\begin{bmatrix}-2\\1\\1\end{bmatrix}", font_size=40, color=GREEN),
            ).arrange(DOWN, buff=0.18),
        ).arrange(RIGHT, buff=1.2)
        footer = Text(
            "Every solution = particular solution + t(special solution)",
            font_size=22,
        )
        footer.scale_to_fit_width(10.8)
        group = VGroup(heading, cards, footer).arrange(DOWN, buff=0.66)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _final_summary():
        heading = Text("Two descriptions, one solution set", font_size=29, color=YELLOW)
        left = VGroup(
            Text("Textbook", font_size=26, color=YELLOW),
            MathTex(
                r"\begin{bmatrix}x\\y\\z\end{bmatrix}=",
                r"\begin{bmatrix}4\\1\\0\end{bmatrix}",
                r"+t",
                r"\begin{bmatrix}-2\\1\\1\end{bmatrix}",
                font_size=36,
            ),
        ).arrange(DOWN, buff=0.22)
        right = VGroup(
            Text("Strang", font_size=26, color=YELLOW),
            Text("particular solution", font_size=21, color=BLUE),
            MathTex(r"\begin{bmatrix}4\\1\\0\end{bmatrix}", font_size=34, color=BLUE),
            Text("plus t times the special solution", font_size=21, color=GREEN),
            MathTex(r"\begin{bmatrix}-2\\1\\1\end{bmatrix}", font_size=34, color=GREEN),
        ).arrange(DOWN, buff=0.12)
        columns = VGroup(left, right).arrange(RIGHT, buff=1.35, aligned_edge=UP)
        footer = Text(
            "If there were more free variables, we would build more special solutions—one at a time.",
            font_size=23,
            color=YELLOW,
        )
        footer.scale_to_fit_width(11.2)
        group = VGroup(heading, columns, footer).arrange(DOWN, buff=0.42)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
