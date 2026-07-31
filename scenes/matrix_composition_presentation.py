"""CP87: matrix multiplication as composition of linear transformations."""

from manim import (
    Arrow, BackgroundRectangle, BLUE, Create, DOWN, FadeIn, FadeOut,
    GREEN, LEFT, MathTex, Matrix, NumberPlane, RED, ReplacementTransform,
    RIGHT, Scene, Text, Transform, UP, VGroup, YELLOW,
)

from engine.matrix_composition import MatrixComposition


class MatrixCompositionPresentation(Scene):
    TITLE = "Why Do We Multiply Matrices?"

    def construct(self) -> None:
        s = MatrixComposition().snapshot()

        title = Text(self.TITLE, font_size=40).to_edge(UP)
        subtitle = Text(
            "Two linear transformations can be combined into one.",
            font_size=25,
        ).next_to(title, DOWN, buff=0.18)

        plane = NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-3, 3, 1),
            x_length=7.6,
            y_length=5.0,
            background_line_style={"stroke_opacity": 0.28},
        ).shift(LEFT * 1.35 + DOWN * 0.55)

        matrix_card = self._matrix_card(s)
        flow = MathTex(
            r"\mathbf{x}\xrightarrow{\;B\;}B\mathbf{x}"
            r"\xrightarrow{\;A\;}A(B\mathbf{x})=(AB)\mathbf{x}",
            font_size=31,
        ).to_edge(DOWN).shift(UP * 0.10)

        arrow = self._vector_arrow(plane, s.vector_x, BLUE)
        label = self._vector_label(r"\mathbf{x}", plane, s.vector_x, BLUE)

        self.play(FadeIn(title), FadeIn(subtitle))
        self.play(Create(plane), FadeIn(matrix_card))
        self.play(Create(arrow), FadeIn(label), FadeIn(flow))
        self.wait(0.8)

        step_b = MathTex(
            r"\mathbf{x}\xrightarrow{\;B\;}B\mathbf{x}",
            font_size=29,
        ).next_to(subtitle, DOWN, buff=0.18)

        after_b_arrow = self._vector_arrow(plane, s.after_b, GREEN)
        after_b_label = self._vector_label(
            r"B\mathbf{x}", plane, s.after_b, GREEN
        )

        self.play(FadeIn(step_b))
        self.play(
            Transform(arrow, after_b_arrow),
            ReplacementTransform(label, after_b_label),
            run_time=1.6,
        )
        self.wait(0.7)

        step_a = MathTex(
            r"B\mathbf{x}\xrightarrow{\;A\;}A(B\mathbf{x})",
            font_size=29,
        ).move_to(step_b)

        final_arrow = self._vector_arrow(plane, s.after_a_after_b, YELLOW)
        final_label = self._vector_label(
            r"A(B\mathbf{x})", plane, s.after_a_after_b, YELLOW
        )

        self.play(ReplacementTransform(step_b, step_a))
        self.play(
            Transform(arrow, final_arrow),
            ReplacementTransform(after_b_label, final_label),
            run_time=1.6,
        )
        self.wait(0.8)

        retained_arrow = arrow.copy()
        retained_label = final_label.copy()

        self.play(FadeOut(step_a), FadeOut(arrow), FadeOut(final_label))

        prediction = VGroup(
            Text("Pause and Predict", font_size=31, color=YELLOW),
            Text(
                "Will applying AB all at once land at the same point?",
                font_size=24,
            ),
        ).arrange(DOWN, buff=0.16).next_to(subtitle, DOWN, buff=0.22)

        self.play(FadeIn(prediction))
        self.wait(1.3)
        self.play(FadeOut(prediction))

        replay_arrow = self._vector_arrow(plane, s.vector_x, BLUE)
        replay_label = self._vector_label(
            r"\mathbf{x}", plane, s.vector_x, BLUE
        )
        direct_step = MathTex(
            r"\mathbf{x}\xrightarrow{\;AB\;}(AB)\mathbf{x}",
            font_size=29,
        ).next_to(subtitle, DOWN, buff=0.18)

        self.play(
            Create(replay_arrow),
            FadeIn(replay_label),
            FadeIn(direct_step),
        )

        direct_arrow = self._vector_arrow(plane, s.after_ab, RED)
        direct_label = self._vector_label(
            r"(AB)\mathbf{x}", plane, s.after_ab, RED
        )

        self.play(
            Transform(replay_arrow, direct_arrow),
            ReplacementTransform(replay_label, direct_label),
            run_time=1.8,
        )
        self.play(FadeIn(retained_arrow), FadeIn(retained_label))

        coincidence = Text(
            "The endpoints coincide.",
            font_size=27,
            color=GREEN,
        ).next_to(direct_step, DOWN, buff=0.15)

        self.play(FadeIn(coincidence))
        self.wait(1.0)

        self.play(
            FadeOut(plane), FadeOut(matrix_card), FadeOut(flow),
            FadeOut(replay_arrow), FadeOut(direct_label),
            FadeOut(retained_arrow), FadeOut(retained_label),
            FadeOut(direct_step), FadeOut(coincidence), FadeOut(subtitle),
        )

        self._show_conclusion(s)
        self.wait(1.5)

    def _matrix_card(self, s):
        top = VGroup(
            MathTex("A=", font_size=27),
            self._matrix(s.matrix_a),
            MathTex(r"\qquad B=", font_size=27),
            self._matrix(s.matrix_b),
        ).arrange(RIGHT, buff=0.10)

        bottom = VGroup(
            MathTex("AB=", font_size=27),
            self._matrix(s.product_ab),
        ).arrange(RIGHT, buff=0.10)

        content = VGroup(top, bottom).arrange(DOWN, buff=0.14)
        background = BackgroundRectangle(
            content,
            buff=0.16,
            fill_opacity=0.84,
            stroke_opacity=0.5,
        )
        return VGroup(background, content).to_corner(RIGHT + UP).shift(
            LEFT * 0.18 + DOWN * 1.20
        )

    def _show_conclusion(self, s) -> None:
        heading = Text(
            "Matrix multiplication is composition",
            font_size=36,
        )
        equation = MathTex(
            r"A(B\mathbf{x})=(AB)\mathbf{x}",
            font_size=42,
        )
        order = Text(
            "B acts first. A acts second.",
            font_size=29,
            color=YELLOW,
        )
        comparison = VGroup(
            MathTex(r"AB=" + self._matrix_latex(s.product_ab), font_size=30),
            MathTex(r"BA=" + self._matrix_latex(s.product_ba), font_size=30),
        ).arrange(RIGHT, buff=0.65)

        noncommutative = Text(
            "In general, AB is not equal to BA.",
            font_size=27,
        )
        conclusion = Text(
            "Multiplying matrices combines linear transformations.",
            font_size=29,
            color=GREEN,
        )

        group = VGroup(
            heading, equation, order, comparison, noncommutative, conclusion
        ).arrange(DOWN, buff=0.31)

        self.play(FadeIn(group))

    def _matrix(self, values):
        return Matrix(
            [
                [self._format(values[0, 0]), self._format(values[0, 1])],
                [self._format(values[1, 0]), self._format(values[1, 1])],
            ],
            element_to_mobject_config={"font_size": 23},
        )

    @staticmethod
    def _matrix_latex(values) -> str:
        return (
            r"\begin{bmatrix}"
            f"{int(values[0, 0])}&{int(values[0, 1])}"
            r"\\"
            f"{int(values[1, 0])}&{int(values[1, 1])}"
            r"\end{bmatrix}"
        )

    @staticmethod
    def _format(value: float) -> str:
        rounded = round(float(value))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):.2f}"

    @staticmethod
    def _vector_arrow(plane, vector, color):
        return Arrow(
            plane.c2p(0, 0),
            plane.c2p(float(vector[0]), float(vector[1])),
            buff=0,
            color=color,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.16,
        )

    @staticmethod
    def _vector_label(tex, plane, vector, color):
        endpoint = plane.c2p(float(vector[0]), float(vector[1]))
        return MathTex(tex, font_size=28, color=color).next_to(
            endpoint,
            RIGHT + UP,
            buff=0.10,
        )
