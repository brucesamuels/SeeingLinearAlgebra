"""CP110 presentation: solve from echelon form by back substitution."""

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

from engine.back_substitution import BackSubstitution


class BackSubstitutionPresentation(Scene):
    """Solve the echelon system upward and verify the answer."""

    TITLE = "Back Substitution"
    STEP_COLORS = (RED, GREEN, BLUE)

    def construct(self) -> None:
        model = BackSubstitution()
        snapshot = model.snapshot()

        title = Text(self.TITLE, font_size=40).to_edge(UP, buff=0.28)
        subtitle = Text(
            "Start with the bottom row and work upward.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.14)
        self.play(Write(title), FadeIn(subtitle), run_time=1.3)

        heading = Text("Row echelon form from Gaussian elimination", font_size=29).move_to(UP * 1.65)
        matrix, display = self._augmented_matrix(snapshot.echelon_augmented)
        display.move_to(LEFT * 2.9 + DOWN * 0.32)
        value_panel = self._empty_value_panel().move_to(RIGHT * 3.05 + DOWN * 0.15)
        guidance = Text(
            "Each lower row has fewer unknowns than the row above it.",
            font_size=24,
        ).to_edge(DOWN, buff=0.30)
        guidance.scale_to_fit_width(11.4)
        self.play(FadeIn(heading), FadeIn(display), FadeIn(value_panel), FadeIn(guidance), run_time=1.2)
        self.wait(2.0)

        step_heading = None
        current_value_panel = value_panel
        for step_index, step in enumerate(snapshot.steps):
            row_index = 2 - step_index
            color = self.STEP_COLORS[step_index]
            new_heading = Text(
                {
                    0: "Bottom row: solve for z",
                    1: "Use z = 1 to solve for y",
                    2: "Use y = 1 and z = 1 to solve for x",
                }[step_index],
                font_size=28,
            ).move_to(UP * 0.92)
            if step_heading is None:
                self.play(FadeIn(new_heading), run_time=0.8)
            else:
                self.play(ReplacementTransform(step_heading, new_heading), run_time=0.8)
            step_heading = new_heading

            row_box = SurroundingRectangle(matrix.get_rows()[row_index], color=color, buff=0.11)
            self.play(Create(row_box), run_time=0.7)

            algebra = self._algebra_panel(step.equation_tex, step.solved_tex, color)
            algebra.move_to(DOWN * 2.35 + RIGHT * 0.05)
            self.play(FadeIn(algebra), run_time=0.9)
            self.wait(1.8)

            next_value_panel = self._value_panel(snapshot.steps[: step_index + 1])
            next_value_panel.move_to(current_value_panel)
            self.play(ReplacementTransform(current_value_panel, next_value_panel), run_time=0.9)
            current_value_panel = next_value_panel
            self.wait(1.0)
            self.play(FadeOut(algebra), FadeOut(row_box), run_time=0.6)

        solve_note = Text(
            "Back substitution recovers the unique solution (1, 1, 1).",
            font_size=25,
            color=GREEN,
        ).to_edge(DOWN, buff=0.28)
        solve_note.scale_to_fit_width(11.5)
        self.play(FadeOut(guidance), run_time=0.5)
        self.play(FadeIn(solve_note), run_time=0.7)
        self.wait(2.0)

        self.play(
            FadeOut(heading),
            FadeOut(step_heading),
            FadeOut(display),
            FadeOut(current_value_panel),
            FadeOut(solve_note),
            FadeOut(subtitle),
            run_time=1.0,
        )

        verify_heading = Text("Verify the solution in the original system", font_size=30)
        verify_heading.next_to(title, DOWN, buff=0.22)
        solution_badge = MathTex(
            r"(x,y,z)=(1,1,1)",
            font_size=38,
            color=YELLOW,
        ).next_to(verify_heading, DOWN, buff=0.30)
        original_group = self._original_system_group(snapshot.original_equations_tex)
        original_group.move_to(LEFT * 3.25 + DOWN * 0.38)
        check_panel = self._verification_panel().move_to(RIGHT * 3.05 + DOWN * 0.38)
        footer = Text(
            "The same vector satisfies every original equation.",
            font_size=25,
            color=GREEN,
        ).to_edge(DOWN, buff=0.30)
        footer.scale_to_fit_width(11.5)
        self.play(
            FadeIn(verify_heading),
            FadeIn(solution_badge),
            FadeIn(original_group),
            run_time=1.2,
        )
        self.play(FadeIn(check_panel), FadeIn(footer), run_time=0.9)
        self.wait(4.0)

    def _augmented_matrix(self, values):
        formatted = [[self._format_number(v) for v in row] for row in values]
        matrix = Matrix(formatted, h_buff=0.86, v_buff=0.64).scale(0.94)
        columns = matrix.get_columns()
        separator_x = (columns[2].get_right()[0] + columns[3].get_left()[0]) / 2
        separator = Line(UP * 1.18, DOWN * 1.18, stroke_width=2.0).move_to(
            [separator_x, matrix.get_center()[1], 0]
        )
        return matrix, VGroup(matrix, separator)

    def _empty_value_panel(self):
        heading = Text("Known values", font_size=28, color=YELLOW)
        blank = Text("none yet", font_size=24, color=WHITE)
        panel = VGroup(heading, blank).arrange(DOWN, buff=0.28)
        box = SurroundingRectangle(panel, color=YELLOW, buff=0.18)
        return VGroup(box, panel)

    def _value_panel(self, steps):
        heading = Text("Known values", font_size=28, color=YELLOW)
        values = VGroup(
            *[
                MathTex(step.solved_tex, font_size=34, color=self.STEP_COLORS[index])
                for index, step in enumerate(steps)
            ]
        ).arrange(DOWN, buff=0.20)
        panel = VGroup(heading, values).arrange(DOWN, buff=0.28)
        box = SurroundingRectangle(panel, color=YELLOW, buff=0.18)
        return VGroup(box, panel)

    @staticmethod
    def _algebra_panel(equation_tex: str, solved_tex: str, color):
        equation = MathTex(equation_tex, font_size=36)
        arrow = MathTex(r"\Longrightarrow", font_size=32, color=color)
        solved = MathTex(solved_tex, font_size=38, color=color)
        group = VGroup(equation, arrow, solved).arrange(RIGHT, buff=0.22)
        box = SurroundingRectangle(group, color=color, buff=0.16)
        return VGroup(box, group)

    @staticmethod
    def _original_system_group(equations_tex: tuple[str, str, str]):
        heading = Text("Original system", font_size=28)
        equations = VGroup(*[MathTex(eq, font_size=36) for eq in equations_tex]).arrange(
            DOWN,
            buff=0.28,
            aligned_edge=LEFT,
        )
        return VGroup(heading, equations).arrange(DOWN, buff=0.38)

    @staticmethod
    def _verification_panel():
        heading = Text("Check with x = y = z = 1", font_size=28, color=YELLOW)
        checks = VGroup(
            MathTex(r"1+1+1=3", font_size=33, color=BLUE),
            MathTex(r"2(1)-1+1=2", font_size=33, color=GREEN),
            MathTex(r"1+2(1)-1=2", font_size=33, color=RED),
        ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        panel = VGroup(heading, checks).arrange(DOWN, buff=0.34)
        box = SurroundingRectangle(panel, color=YELLOW, buff=0.18)
        return VGroup(box, panel)

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
