"""CP113 presentation: read the solution-set type directly from RREF."""

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

from engine.rref_solution_sets import RREFSolutionCase, RREFSolutionSets


class RREFSolutionSetsPresentation(Scene):
    """Show the unique, inconsistent, and free-variable outcomes in RREF."""

    def construct(self) -> None:
        snapshot = RREFSolutionSets().snapshot()

        title = Text("Three Possible Solution Sets", font_size=40).to_edge(UP, buff=0.28)
        subtitle = Text(
            "Reduced row echelon form reveals the answer immediately.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.14)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        case_heading = Text(snapshot.cases[0].name, font_size=31, color=GREEN).move_to(UP * 1.68)
        matrix, matrix_display = self._augmented_matrix(snapshot.cases[0].augmented)
        matrix_display.move_to(LEFT * 3.05 + DOWN * 0.22)
        interpretation = self._interpretation_panel(snapshot.cases[0]).move_to(RIGHT * 3.15 + DOWN * 0.10)
        footer = Text(
            "A pivot in every variable column gives one value for every variable.",
            font_size=24,
            color=GREEN,
        ).to_edge(DOWN, buff=0.30)
        footer.scale_to_fit_width(11.5)
        pivot_boxes = self._pivot_boxes(matrix, snapshot.cases[0], GREEN)
        self.play(
            FadeIn(case_heading),
            FadeIn(matrix_display),
            Create(pivot_boxes),
            FadeIn(interpretation),
            FadeIn(footer),
            run_time=1.3,
        )
        self.wait(3.0)

        prompt = VGroup(
            Text("Pause and Predict", font_size=28, color=YELLOW),
            Text("What does the last row say?", font_size=25),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.28)

        no_case = snapshot.cases[1]
        no_heading = Text(no_case.name, font_size=31, color=RED).move_to(case_heading)
        no_matrix, no_display = self._augmented_matrix(no_case.augmented)
        no_display.move_to(matrix_display)
        self.play(
            ReplacementTransform(case_heading, no_heading),
            ReplacementTransform(matrix_display, no_display),
            FadeOut(pivot_boxes),
            FadeOut(interpretation),
            FadeOut(footer),
            FadeIn(prompt),
            run_time=1.2,
        )
        self.wait(2.2)
        contradiction_box = SurroundingRectangle(no_matrix.get_rows()[2], color=RED, buff=0.11)
        contradiction = MathTex(r"0=1", font_size=40, color=RED).move_to(RIGHT * 3.15 + UP * 0.40)
        impossible = Text("This equation is impossible.", font_size=25, color=RED).next_to(
            contradiction,
            DOWN,
            buff=0.25,
        )
        no_footer = Text(
            "A contradictory row means the system has no common solution.",
            font_size=24,
            color=RED,
        ).to_edge(DOWN, buff=0.30)
        no_footer.scale_to_fit_width(11.5)
        self.play(
            FadeOut(prompt),
            Create(contradiction_box),
            FadeIn(contradiction),
            FadeIn(impossible),
            FadeIn(no_footer),
            run_time=1.0,
        )
        self.wait(3.0)

        infinite_case = snapshot.cases[2]
        infinite_heading = Text(infinite_case.name, font_size=31, color=YELLOW).move_to(no_heading)
        infinite_matrix, infinite_display = self._augmented_matrix(infinite_case.augmented)
        infinite_display.move_to(no_display)
        infinite_interpretation = self._interpretation_panel(infinite_case).move_to(RIGHT * 3.15 + DOWN * 0.03)
        free_box = SurroundingRectangle(infinite_matrix.get_columns()[2], color=YELLOW, buff=0.12)
        zero_row_box = SurroundingRectangle(infinite_matrix.get_rows()[2], color=GREEN, buff=0.11)
        infinite_footer = Text(
            "The system is consistent, but z is free—so one parameter generates infinitely many solutions.",
            font_size=23,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.28)
        infinite_footer.scale_to_fit_width(11.6)
        self.play(
            ReplacementTransform(no_heading, infinite_heading),
            ReplacementTransform(no_display, infinite_display),
            FadeOut(contradiction_box),
            FadeOut(contradiction),
            FadeOut(impossible),
            FadeOut(no_footer),
            Create(free_box),
            Create(zero_row_box),
            FadeIn(infinite_interpretation),
            FadeIn(infinite_footer),
            run_time=1.3,
        )
        self.wait(3.5)

        self.play(
            FadeOut(infinite_heading),
            FadeOut(infinite_display),
            FadeOut(free_box),
            FadeOut(zero_row_box),
            FadeOut(infinite_interpretation),
            FadeOut(infinite_footer),
            FadeOut(subtitle),
            run_time=1.0,
        )

        summary_heading = Text("What to look for in RREF", font_size=31).next_to(title, DOWN, buff=0.22)
        cards = VGroup(
            self._summary_card(
                "Unique",
                "Pivot in every\nvariable column",
                GREEN,
            ),
            self._summary_card(
                "No solution",
                "Contradictory row\n0 = nonzero",
                RED,
            ),
            self._summary_card(
                "Infinite",
                "Consistent system\nwith a free variable",
                YELLOW,
            ),
        ).arrange(RIGHT, buff=0.42)
        cards.scale_to_fit_width(12.5)
        cards.move_to(DOWN * 0.35)
        closing = Text(
            "RREF does more than solve the system—it exposes the structure of the solution set.",
            font_size=24,
            color=BLUE,
        ).to_edge(DOWN, buff=0.30)
        closing.scale_to_fit_width(11.6)
        self.play(FadeIn(summary_heading), FadeIn(cards), FadeIn(closing), run_time=1.2)
        self.wait(4.0)

    def _augmented_matrix(self, values):
        formatted = [[self._format_number(value) for value in row] for row in values]
        matrix = Matrix(formatted, h_buff=0.86, v_buff=0.66).scale(0.95)
        columns = matrix.get_columns()
        separator_x = (columns[2].get_right()[0] + columns[3].get_left()[0]) / 2
        separator = Line(UP * 1.20, DOWN * 1.20, stroke_width=2.0).move_to(
            [separator_x, matrix.get_center()[1], 0]
        )
        return matrix, VGroup(matrix, separator)

    @staticmethod
    def _pivot_boxes(matrix: Matrix, case: RREFSolutionCase, color):
        boxes = []
        for row_index, column_index in enumerate(case.pivot_columns):
            entry = matrix.get_entries()[row_index * 4 + column_index]
            boxes.append(SurroundingRectangle(entry, color=color, buff=0.08))
        return VGroup(*boxes)

    @staticmethod
    def _interpretation_panel(case: RREFSolutionCase):
        color = {
            "unique": GREEN,
            "none": RED,
            "infinite": YELLOW,
        }[case.classification]
        heading = Text(case.name, font_size=28, color=color)
        equations = VGroup(*[MathTex(tex, font_size=35) for tex in case.interpretation_tex]).arrange(
            DOWN,
            buff=0.22,
        )
        panel = VGroup(heading, equations).arrange(DOWN, buff=0.32)
        box = SurroundingRectangle(panel, color=color, buff=0.18)
        return VGroup(box, panel)

    @staticmethod
    def _summary_card(title: str, body: str, color):
        heading = Text(title, font_size=28, color=color)
        description = Text(body, font_size=22, line_spacing=0.85)
        group = VGroup(heading, description).arrange(DOWN, buff=0.30)
        box = SurroundingRectangle(group, color=color, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        if abs(float(value)) < 1e-9:
            return "0"
        return f"{float(value):g}"
