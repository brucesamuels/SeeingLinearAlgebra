"""CP112 presentation: Gauss–Jordan elimination to RREF."""

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

from engine.gauss_jordan_rref import GaussJordanRREF


class GaussJordanRREFPresentation(Scene):
    """Continue elimination from echelon form to reduced row echelon form."""

    STEP_COLORS = (YELLOW, GREEN, BLUE, RED)

    def construct(self) -> None:
        model = GaussJordanRREF()
        snapshot = model.snapshot()

        title = Text("Gauss–Jordan Elimination", font_size=40).to_edge(UP, buff=0.28)
        subtitle = Text(
            "Continue until every pivot is 1 and each pivot column is otherwise zero.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.14)
        subtitle.scale_to_fit_width(11.6)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        heading = Text("Start from row echelon form", font_size=28).move_to(UP * 1.98)
        matrix, display = self._augmented_matrix(snapshot.echelon_augmented)
        display.move_to(LEFT * 2.85 + DOWN * 0.22)
        checklist = self._checklist().move_to(RIGHT * 3.3 + DOWN * 0.02)
        note = Text(
            "Now work upward: scale pivots to 1 and clear above them.",
            font_size=24,
        ).to_edge(DOWN, buff=0.30)
        note.scale_to_fit_width(11.5)
        self.play(FadeIn(heading), FadeIn(display), FadeIn(checklist), FadeIn(note), run_time=1.2)
        self.wait(2.0)

        current_display = display
        current_matrix = matrix
        current_checklist = checklist
        op_band = None
        current_heading = heading

        for index, step in enumerate(snapshot.steps):
            new_heading = Text(step.description, font_size=27).move_to(UP * 1.98)
            self.play(ReplacementTransform(current_heading, new_heading), run_time=0.8)
            current_heading = new_heading

            new_band = self._operation_band(step.label_tex, self.STEP_COLORS[index])
            new_band.move_to(LEFT * 2.85 + UP * 1.28)
            if op_band is None:
                self.play(FadeIn(new_band), run_time=0.7)
            else:
                self.play(ReplacementTransform(op_band, new_band), run_time=0.7)
            op_band = new_band

            row_box, column_box = self._focus_boxes(current_matrix, index)
            self.play(Create(row_box), Create(column_box), run_time=0.8)

            next_matrix, next_display = self._augmented_matrix(step.result_augmented)
            next_display.move_to(current_display)
            next_checklist = self._checklist(active_index=index).move_to(current_checklist)
            self.play(
                ReplacementTransform(current_display, next_display),
                ReplacementTransform(current_checklist, next_checklist),
                run_time=1.5,
            )
            current_display = next_display
            current_matrix = next_matrix
            current_checklist = next_checklist

            result_box = self._result_box(current_matrix, index)
            self.play(Create(result_box), run_time=0.5)
            self.wait(1.2)
            self.play(FadeOut(row_box), FadeOut(column_box), FadeOut(result_box), run_time=0.5)

        rref_note = Text(
            "In reduced row echelon form, the solution can be read directly.",
            font_size=25,
            color=GREEN,
        ).to_edge(DOWN, buff=0.30)
        rref_note.scale_to_fit_width(11.5)
        self.play(FadeOut(note), FadeIn(rref_note), run_time=0.7)
        self.wait(1.8)

        solution_heading = Text("Read the solution directly from RREF", font_size=29).move_to(UP * 1.98)
        readoff_panel = self._readoff_panel(snapshot.direct_readoff_tex).move_to(RIGHT * 3.35 + DOWN * 0.05)
        self.play(
            ReplacementTransform(current_heading, solution_heading),
            FadeOut(op_band),
            ReplacementTransform(current_checklist, readoff_panel),
            run_time=1.0,
        )
        current_checklist = readoff_panel
        self.wait(2.8)

        compare_heading = Text("Two ways to finish solving", font_size=30).next_to(title, DOWN, buff=0.20)
        left_compare = self._compare_column(
            "Gaussian elimination",
            (
                r"\text{Row echelon form}",
                r"\Downarrow",
                r"\text{Back substitution}",
            ),
        ).move_to(LEFT * 3.15 + DOWN * 0.35)
        right_compare = self._compare_column(
            "Gauss–Jordan elimination",
            (
                r"\text{Reduced row echelon form}",
                r"\Downarrow",
                r"\text{Read the solution directly}",
            ),
        ).move_to(RIGHT * 3.15 + DOWN * 0.35)
        self.play(
            FadeOut(current_display),
            FadeOut(current_checklist),
            FadeOut(solution_heading),
            FadeOut(rref_note),
            ReplacementTransform(subtitle, compare_heading),
            FadeIn(left_compare),
            FadeIn(right_compare),
            run_time=1.2,
        )
        self.wait(4.0)

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
    def _operation_band(label_tex: str, color):
        label = MathTex(label_tex, font_size=34, color=color)
        box = SurroundingRectangle(label, color=color, buff=0.16)
        return VGroup(box, label)

    @staticmethod
    def _checklist(active_index: int | None = None):
        title = Text("RREF goals", font_size=28, color=YELLOW)
        items = [
            "Scale each pivot to 1",
            "Clear above the bottom pivot",
            "Clear above the middle pivot",
            "Read the solution directly",
        ]
        lines = VGroup()
        for index, item in enumerate(items):
            color = YELLOW if active_index == index else WHITE
            bullet = Text("• " + item, font_size=22, color=color)
            lines.add(bullet)
        lines.arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        panel = VGroup(title, lines).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        box = SurroundingRectangle(panel, color=YELLOW, buff=0.16)
        return VGroup(box, panel)

    def _focus_boxes(self, matrix: Matrix, index: int):
        if index == 0:
            row_box = SurroundingRectangle(matrix.get_rows()[2], color=self.STEP_COLORS[index], buff=0.10)
            column_box = SurroundingRectangle(matrix.get_columns()[2], color=self.STEP_COLORS[index], buff=0.12)
        elif index == 1:
            row_box = SurroundingRectangle(matrix.get_rows()[1], color=self.STEP_COLORS[index], buff=0.10)
            column_box = SurroundingRectangle(matrix.get_columns()[2], color=self.STEP_COLORS[index], buff=0.12)
        elif index == 2:
            row_box = SurroundingRectangle(matrix.get_rows()[0], color=self.STEP_COLORS[index], buff=0.10)
            column_box = SurroundingRectangle(matrix.get_columns()[2], color=self.STEP_COLORS[index], buff=0.12)
        else:
            row_box = SurroundingRectangle(matrix.get_rows()[0], color=self.STEP_COLORS[index], buff=0.10)
            column_box = SurroundingRectangle(matrix.get_columns()[1], color=self.STEP_COLORS[index], buff=0.12)
        return row_box, column_box

    def _result_box(self, matrix: Matrix, index: int):
        if index == 0:
            target = matrix.get_entries()[10]  # third row, third col
        elif index == 1:
            target = matrix.get_entries()[6]  # second row, third col becomes 0
        elif index == 2:
            target = matrix.get_entries()[2]  # first row, third col becomes 0
        else:
            target = matrix.get_entries()[1]  # first row, second col becomes 0
        return SurroundingRectangle(target, color=self.STEP_COLORS[index], buff=0.08)

    @staticmethod
    def _readoff_panel(solution_tex: tuple[str, str, str]):
        heading = Text("Direct read-off", font_size=28, color=YELLOW)
        entries = VGroup(*[MathTex(tex, font_size=36) for tex in solution_tex]).arrange(
            DOWN,
            buff=0.24,
        )
        panel = VGroup(heading, entries).arrange(DOWN, buff=0.32)
        box = SurroundingRectangle(panel, color=YELLOW, buff=0.16)
        return VGroup(box, panel)

    @staticmethod
    def _compare_column(title: str, lines_tex: tuple[str, str, str]):
        heading = Text(title, font_size=27, color=YELLOW)
        lines = VGroup(*[MathTex(tex, font_size=30) for tex in lines_tex]).arrange(
            DOWN,
            buff=0.24,
        )
        group = VGroup(heading, lines).arrange(DOWN, buff=0.34)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        if abs(float(value)) < 1e-9:
            return "0"
        return f"{float(value):g}"
