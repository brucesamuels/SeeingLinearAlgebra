"""CP117 presentation: the complete solution x = x_p + x_n."""

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
    DEGREES,
    Surface,
    ThreeDAxes,
    ThreeDScene,
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

from engine.complete_solution import CompleteSolution


class CompleteSolutionPresentation(ThreeDScene):
    """Develop and visualize the complete solution of a consistent system."""

    def construct(self) -> None:
        model = CompleteSolution()
        snapshot = model.snapshot()

        title = Text("The Complete Solution", font_size=41).to_edge(UP, buff=0.27)
        subtitle = Text(
            "One particular solution plus every null-space direction.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.13)
        subtitle.scale_to_fit_width(11.4)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)
        self.add_fixed_in_frame_mobjects(title, subtitle)

        heading = Text("A complete solution has two parts", font_size=30).move_to(UP * 1.90)
        matrix, display = self._augmented_matrix(snapshot.rref_augmented)
        display.move_to(LEFT * 3.10 + DOWN * 0.25)
        variable_labels = self._variable_labels(matrix)
        structure_panel = self._structure_panel().move_to(RIGHT * 3.18 + DOWN * 0.02)
        footer = Text(
            "The particular part reaches b; the null-space part can be added without changing b.",
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        footer.scale_to_fit_width(11.2)
        self.play(
            FadeIn(heading),
            FadeIn(display),
            FadeIn(variable_labels),
            FadeIn(structure_panel),
            FadeIn(footer),
            run_time=1.2,
        )
        self.wait(2.4)

        particular_heading = Text("Choose one particular solution", font_size=30).move_to(UP * 2.04)
        particular_panel = self._particular_panel(snapshot.particular_solution_tex).move_to(DOWN * 0.34)
        self.play(
            ReplacementTransform(heading, particular_heading),
            FadeOut(display),
            FadeOut(variable_labels),
            FadeOut(structure_panel),
            FadeOut(footer),
            FadeIn(particular_panel),
            run_time=1.15,
        )
        self.wait(2.5)

        null_heading = Text("Add any vector from the associated null space", font_size=27).move_to(UP * 2.28)
        null_heading.scale_to_fit_width(11.3)
        null_panel = self._null_part_panel(snapshot.null_space_solution_tex).move_to(DOWN * 0.46)
        self.play(
            ReplacementTransform(particular_heading, null_heading),
            ReplacementTransform(particular_panel, null_panel),
            run_time=1.15,
        )
        self.wait(2.7)

        prompt = VGroup(
            Text("Pause and Predict", font_size=25, color=YELLOW),
            Text("What is A(xₚ + xₙ) when Axₚ = b and Axₙ = 0?", font_size=22),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.10)
        prompt.scale_to_fit_width(11.2)
        self.play(FadeIn(prompt), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(prompt), run_time=0.6)

        combine_heading = Text("Combine the two parts", font_size=30).move_to(UP * 2.04)
        combine_panel = self._combine_panel(snapshot.complete_solution_tex).move_to(DOWN * 0.38)
        self.play(
            ReplacementTransform(null_heading, combine_heading),
            ReplacementTransform(null_panel, combine_panel),
            run_time=1.15,
        )
        self.wait(2.8)

        verify_heading = Text("Why every vector in this form solves A x = b", font_size=29).move_to(UP * 2.04)
        verify_heading.scale_to_fit_width(11.3)
        verify_panel = self._verification_panel(snapshot.verification_tex).move_to(DOWN * 0.34)
        self.play(
            ReplacementTransform(combine_heading, verify_heading),
            ReplacementTransform(combine_panel, verify_panel),
            run_time=1.15,
        )
        self.wait(2.8)

        converse_heading = Text("Why every solution must have this form", font_size=29).move_to(UP * 2.04)
        converse_panel = self._converse_panel(snapshot.converse_tex).move_to(DOWN * 0.34)
        self.play(
            ReplacementTransform(verify_heading, converse_heading),
            ReplacementTransform(verify_panel, converse_panel),
            run_time=1.15,
        )
        self.wait(3.0)

        geometry_heading = Text("Geometrically: translate the null space by xₚ", font_size=29).move_to(UP * 2.04)
        geometry_heading.scale_to_fit_width(11.2)
        geometry = self._translation_geometry().scale(0.86).move_to(LEFT * 3.15 + DOWN * 0.42)
        geometry_panel = self._geometry_panel().move_to(RIGHT * 3.18 + DOWN * 0.08)
        geometry_footer = Text(
            "All solutions form an affine plane parallel to N(A), passing through xₚ.",
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        geometry_footer.scale_to_fit_width(11.1)
        self.play(FadeOut(converse_heading), FadeOut(converse_panel), run_time=0.65)
        self.add_fixed_in_frame_mobjects(geometry_heading, geometry_panel, geometry_footer)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-52 * DEGREES, zoom=0.92)
        self.play(
            FadeIn(geometry_heading),
            FadeIn(geometry),
            FadeIn(geometry_panel),
            FadeIn(geometry_footer),
            run_time=1.25,
        )
        self.begin_ambient_camera_rotation(rate=0.08)
        self.wait(3.2)

        summary_heading = Text("The complete-solution pattern", font_size=30).move_to(UP * 2.04)
        summary_panel = self._summary_panel().move_to(DOWN * 0.38)
        self.stop_ambient_camera_rotation()
        self.play(
            FadeOut(geometry),
            FadeOut(geometry_heading),
            FadeOut(geometry_panel),
            FadeOut(geometry_footer),
            run_time=0.85,
        )
        self.remove_fixed_in_frame_mobjects(geometry_heading, geometry_panel, geometry_footer)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=0.6)
        self.play(FadeIn(summary_heading), FadeIn(summary_panel), run_time=1.2)
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
    def _structure_panel():
        particular = MathTex(r"A\mathbf{x}_p=\mathbf{b}", font_size=38, color=YELLOW)
        null = MathTex(r"A\mathbf{x}_n=\mathbf{0}", font_size=38, color=GREEN)
        combine = MathTex(r"\mathbf{x}=\mathbf{x}_p+\mathbf{x}_n", font_size=42, color=BLUE)
        group = VGroup(particular, null, combine).arrange(DOWN, buff=0.40)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _particular_panel(particular_tex: str):
        instruction = Text("Set the free variables y and z equal to zero.", font_size=25, color=YELLOW)
        scalar = MathTex(r"y=0,\qquad z=0,\qquad x=3", font_size=37)
        vector = MathTex(particular_tex, font_size=43, color=BLUE)
        check = MathTex(r"A\mathbf{x}_p=\mathbf{b}", font_size=38, color=GREEN)
        group = VGroup(instruction, scalar, vector, check).arrange(DOWN, buff=0.40)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _null_part_panel(null_tex: str):
        basis = MathTex(
            r"N(A)=\operatorname{span}\left\{"
            r"\begin{bmatrix}-2\\1\\0\end{bmatrix},"
            r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
            r"\right\}",
            font_size=35,
            color=YELLOW,
        )
        vector = MathTex(null_tex, font_size=39)
        check = MathTex(r"A\mathbf{x}_n=\mathbf{0}", font_size=38, color=GREEN)
        note = Text("The parameters s and t choose any direction within the null space.", font_size=23)
        note.scale_to_fit_width(11.0)
        group = VGroup(basis, vector, check, note).arrange(DOWN, buff=0.38)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _combine_panel(complete_tex: str):
        structure = MathTex(r"\mathbf{x}=\mathbf{x}_p+\mathbf{x}_n", font_size=41, color=YELLOW)
        equation = MathTex(
            r"\mathbf{x}=",
            r"\begin{bmatrix}3\\0\\0\end{bmatrix}",
            r"+",
            r"s\begin{bmatrix}-2\\1\\0\end{bmatrix}+t\begin{bmatrix}1\\0\\1\end{bmatrix}",
            font_size=35,
        )
        label_band = Line(LEFT * 4.8, RIGHT * 4.8, stroke_opacity=0).set_height(0.60)
        conclusion = Text(
            "This is the complete solution: every choice of s and t gives one solution.",
            font_size=23,
        )
        conclusion.scale_to_fit_width(11.0)
        group = VGroup(structure, equation, label_band, conclusion).arrange(DOWN, buff=0.34)

        particular_label = Text("particular\nsolution", font_size=18, color=BLUE)
        null_label = Text("null-space\ncombination", font_size=18, color=GREEN)
        particular_label.move_to([equation[1].get_center()[0], label_band.get_center()[1], 0])
        null_label.move_to([equation[3].get_center()[0], label_band.get_center()[1], 0])

        box = SurroundingRectangle(VGroup(group, particular_label, null_label), color=YELLOW, buff=0.20)
        return VGroup(box, group, particular_label, null_label)

    @staticmethod
    def _verification_panel(lines: tuple[str, ...]):
        algebra = VGroup(
            MathTex(lines[0], font_size=37),
            MathTex(lines[1], font_size=40, color=YELLOW),
            MathTex(lines[2], font_size=43, color=GREEN),
        ).arrange(DOWN, buff=0.34)
        conclusion = Text("Adding a null-space vector does not change the right-hand side.", font_size=24)
        conclusion.scale_to_fit_width(11.0)
        group = VGroup(algebra, conclusion).arrange(DOWN, buff=0.48)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _converse_panel(lines: tuple[str, ...]):
        algebra = VGroup(
            MathTex(lines[0], font_size=34),
            MathTex(lines[1], font_size=38, color=YELLOW),
            MathTex(lines[2], font_size=38, color=GREEN),
            MathTex(lines[3], font_size=42, color=BLUE),
        ).arrange(DOWN, buff=0.30)
        conclusion = Text("Every solution differs from the particular solution by a null-space vector.", font_size=23)
        conclusion.scale_to_fit_width(11.0)
        group = VGroup(algebra, conclusion).arrange(DOWN, buff=0.42)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _translation_geometry():
        axes = ThreeDAxes(
            x_range=[-4, 5, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=4.8,
            y_length=3.4,
            z_length=3.2,
        )
        axes.set_stroke(opacity=0.55)
        null_plane = Surface(
            lambda u, v: axes.c2p(-2 * u + v, u, v),
            u_range=[-1.2, 1.2],
            v_range=[-1.2, 1.2],
            resolution=(10, 10),
            fill_opacity=0.18,
            checkerboard_colors=[GREEN, GREEN],
            stroke_color=GREEN,
            stroke_opacity=0.30,
        )
        translated_plane = Surface(
            lambda u, v: axes.c2p(3 - 2 * u + v, u, v),
            u_range=[-1.2, 1.2],
            v_range=[-1.2, 1.2],
            resolution=(10, 10),
            fill_opacity=0.20,
            checkerboard_colors=[BLUE, BLUE],
            stroke_color=BLUE,
            stroke_opacity=0.32,
        )
        origin = Dot(axes.c2p(0, 0, 0), color=RED, radius=0.06)
        particular_point = Dot(axes.c2p(3, 0, 0), color=YELLOW, radius=0.07)
        translation = Line(axes.c2p(0, 0, 0), axes.c2p(3, 0, 0), color=YELLOW, stroke_width=4)
        null_label = MathTex(r"N(A)", font_size=28, color=GREEN).move_to(axes.c2p(-2.7, -1.0, -0.8))
        solution_label = MathTex(r"\mathbf{x}_p+N(A)", font_size=28, color=BLUE).move_to(axes.c2p(2.1, 1.15, 1.1))
        xp_label = MathTex(r"\mathbf{x}_p", font_size=26, color=YELLOW).move_to(axes.c2p(3.4, 0.25, 0.0))
        return VGroup(axes, null_plane, translated_plane, origin, particular_point, translation, null_label, solution_label, xp_label)

    @staticmethod
    def _geometry_panel():
        null = MathTex(r"N(A):\ \text{plane through the origin}", font_size=31, color=GREEN)
        translated = MathTex(r"\mathbf{x}_p+N(A):\ \text{parallel translated plane}", font_size=31, color=BLUE)
        point = MathTex(r"\mathbf{x}_p\in\mathbf{x}_p+N(A)", font_size=34, color=YELLOW)
        group = VGroup(null, translated, point).arrange(DOWN, buff=0.42)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _summary_panel():
        formula = MathTex(r"\boxed{\mathbf{x}=\mathbf{x}_p+\mathbf{x}_n}", font_size=48, color=YELLOW)
        conditions = VGroup(
            MathTex(r"A\mathbf{x}_p=\mathbf{b}", font_size=36, color=BLUE),
            MathTex(r"\mathbf{x}_n\in N(A)", font_size=36, color=GREEN),
        ).arrange(RIGHT, buff=1.4)
        steps = VGroup(
            Text("1. Find one particular solution.", font_size=25),
            Text("2. Find a basis for the null space.", font_size=25),
            Text("3. Add every null-space combination to the particular solution.", font_size=25),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        note = Text("Different particular solutions produce the same complete solution set.", font_size=23, color=YELLOW)
        note.scale_to_fit_width(11.0)
        group = VGroup(formula, conditions, steps, note).arrange(DOWN, buff=0.38)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
