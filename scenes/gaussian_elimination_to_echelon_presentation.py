"""CP109 presentation: Gaussian elimination to row echelon form."""

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

from engine.gaussian_elimination_to_echelon import GaussianEliminationToEchelon


class GaussianEliminationToEchelonPresentation(Scene):
    """Use four elementary operations to reach row echelon form."""

    TITLE = "Gaussian Elimination: Reaching Echelon Form"
    PIVOT_COLORS = (BLUE, GREEN, RED)

    def construct(self) -> None:
        model = GaussianEliminationToEchelon()
        snapshot = model.snapshot()

        title = Text(self.TITLE, font_size=39).to_edge(UP, buff=0.28)
        subtitle = Text(
            "Use row operations to create zeros below each pivot.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.14)
        self.play(Write(title), FadeIn(subtitle), run_time=1.5)

        stage_heading = Text("Start with the augmented matrix", font_size=29).move_to(
            UP * 1.65
        )
        current_matrix, current_display = self._augmented_matrix(snapshot.stages[0])
        current_display.move_to(DOWN * 0.58)
        goal = Text(
            "Work from left to right: choose a pivot, then clear the entries below it.",
            font_size=24,
        ).to_edge(DOWN, buff=0.30)
        goal.scale_to_fit_width(11.5)
        self.play(FadeIn(stage_heading), FadeIn(current_display), FadeIn(goal), run_time=1.4)
        self.wait(2.3)

        first_pivot = self._entry_box(current_matrix, 0, 0, BLUE)
        below_first = VGroup(
            self._entry_box(current_matrix, 1, 0, YELLOW),
            self._entry_box(current_matrix, 2, 0, YELLOW),
        )
        self.play(Create(first_pivot), Create(below_first), run_time=1.0)
        self.wait(1.3)
        self.play(FadeOut(first_pivot), FadeOut(below_first), FadeOut(goal), run_time=0.8)

        operation_label = None
        current_matrix, current_display, stage_heading, operation_label = self._show_step(
            current_matrix=current_matrix,
            current_display=current_display,
            next_values=snapshot.stages[1],
            stage_heading=stage_heading,
            new_heading="Clear the first entry below the pivot",
            old_operation=operation_label,
            operation_tex=snapshot.operations[0].label,
            source_row=0,
            target_row=1,
            result_entry=(1, 0),
        )

        current_matrix, current_display, stage_heading, operation_label = self._show_step(
            current_matrix=current_matrix,
            current_display=current_display,
            next_values=snapshot.stages[2],
            stage_heading=stage_heading,
            new_heading="Clear the remaining entry in column 1",
            old_operation=operation_label,
            operation_tex=snapshot.operations[1].label,
            source_row=0,
            target_row=2,
            result_entry=(2, 0),
        )

        first_column_note = Text(
            "The first pivot now has zeros beneath it.",
            font_size=25,
            color=GREEN,
        ).to_edge(DOWN, buff=0.30)
        column_box = SurroundingRectangle(
            current_matrix.get_columns()[0],
            color=BLUE,
            buff=0.12,
        )
        self.play(Create(column_box), FadeIn(first_column_note), run_time=0.9)
        self.wait(1.9)
        self.play(FadeOut(column_box), FadeOut(first_column_note), run_time=0.7)

        prompt = VGroup(
            Text("Pause and Predict", font_size=29, color=YELLOW),
            Text("Which remaining row gives the cleanest second pivot?", font_size=25),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(prompt), run_time=0.9)
        self.wait(2.7)
        self.play(FadeOut(prompt), run_time=0.7)

        current_matrix, current_display, stage_heading, operation_label = self._show_step(
            current_matrix=current_matrix,
            current_display=current_display,
            next_values=snapshot.stages[3],
            stage_heading=stage_heading,
            new_heading="Move the row with leading entry 1 into pivot position",
            old_operation=operation_label,
            operation_tex=snapshot.operations[2].label,
            source_row=2,
            target_row=1,
            result_entry=(1, 1),
            is_swap=True,
        )

        second_pivot = self._entry_box(current_matrix, 1, 1, GREEN)
        below_second = self._entry_box(current_matrix, 2, 1, YELLOW)
        self.play(Create(second_pivot), Create(below_second), run_time=0.9)
        self.wait(1.3)
        self.play(FadeOut(second_pivot), FadeOut(below_second), run_time=0.7)

        current_matrix, current_display, stage_heading, operation_label = self._show_step(
            current_matrix=current_matrix,
            current_display=current_display,
            next_values=snapshot.stages[4],
            stage_heading=stage_heading,
            new_heading="Clear the entry below the second pivot",
            old_operation=operation_label,
            operation_tex=snapshot.operations[3].label,
            source_row=1,
            target_row=2,
            result_entry=(2, 1),
        )

        echelon_note = Text(
            "Each pivot has zeros beneath it: the matrix is in row echelon form.",
            font_size=24,
            color=GREEN,
        ).to_edge(DOWN, buff=0.28)
        echelon_note.scale_to_fit_width(11.5)
        pivot_boxes = VGroup(
            *[
                self._entry_box(current_matrix, row, column, color)
                for (row, column), color in zip(
                    snapshot.pivot_positions,
                    self.PIVOT_COLORS,
                    strict=True,
                )
            ]
        )
        self.play(Create(pivot_boxes), FadeIn(echelon_note), run_time=1.0)
        self.wait(2.5)

        self.play(
            FadeOut(stage_heading),
            FadeOut(operation_label),
            FadeOut(current_display),
            FadeOut(pivot_boxes),
            FadeOut(echelon_note),
            FadeOut(subtitle),
            run_time=1.1,
        )

        definition_heading = Text("Row echelon form", font_size=32, color=YELLOW)
        definition_heading.next_to(title, DOWN, buff=0.32)
        final_matrix, final_display = self._augmented_matrix(snapshot.echelon_augmented)
        final_display.move_to(LEFT * 3.25 + DOWN * 0.25)
        final_pivots = VGroup(
            *[
                self._entry_box(final_matrix, row, column, color)
                for (row, column), color in zip(
                    snapshot.pivot_positions,
                    self.PIVOT_COLORS,
                    strict=True,
                )
            ]
        )
        checklist = VGroup(
            Text("• Nonzero rows come first.", font_size=25),
            Text("• Each pivot lies right of the pivot above.", font_size=25),
            Text("• Every entry below a pivot is zero.", font_size=25),
        ).arrange(DOWN, buff=0.30, aligned_edge=LEFT)
        checklist.move_to(RIGHT * 2.85 + DOWN * 0.15)
        checklist.scale_to_fit_width(6.1)
        next_lesson = Text(
            "Gaussian elimination stops here. Back substitution comes next.",
            font_size=25,
            color=GREEN,
        ).to_edge(DOWN, buff=0.30)
        next_lesson.scale_to_fit_width(11.5)
        self.play(
            FadeIn(definition_heading),
            FadeIn(final_display),
            Create(final_pivots),
            FadeIn(checklist),
            run_time=1.5,
        )
        self.play(FadeIn(next_lesson), run_time=0.9)
        self.wait(4.0)

    def _show_step(
        self,
        *,
        current_matrix,
        current_display,
        next_values,
        stage_heading,
        new_heading: str,
        old_operation,
        operation_tex: str,
        source_row: int,
        target_row: int,
        result_entry: tuple[int, int],
        is_swap: bool = False,
    ):
        new_stage_heading = Text(new_heading, font_size=28).move_to(stage_heading)
        operation = MathTex(operation_tex, font_size=36, color=YELLOW).move_to(UP * 0.92)
        source_color = GREEN if not is_swap else BLUE
        target_color = RED if not is_swap else GREEN
        source_box = SurroundingRectangle(
            current_matrix.get_rows()[source_row],
            color=source_color,
            buff=0.11,
        )
        target_box = SurroundingRectangle(
            current_matrix.get_rows()[target_row],
            color=target_color,
            buff=0.11,
        )
        animations = [ReplacementTransform(stage_heading, new_stage_heading)]
        if old_operation is None:
            animations.append(Write(operation))
        else:
            animations.append(ReplacementTransform(old_operation, operation))
        self.play(*animations, run_time=1.0)
        self.play(Create(source_box), Create(target_box), run_time=0.8)

        next_matrix, next_display = self._augmented_matrix(next_values)
        next_display.move_to(current_display)
        self.play(
            ReplacementTransform(current_display, next_display),
            FadeOut(source_box),
            FadeOut(target_box),
            run_time=1.5,
        )
        result_box = self._entry_box(next_matrix, *result_entry, GREEN)
        self.play(Create(result_box), run_time=0.5)
        self.wait(1.1)
        self.play(FadeOut(result_box), run_time=0.4)
        return next_matrix, next_display, new_stage_heading, operation

    def _augmented_matrix(self, values):
        formatted = [
            [self._format_number(value) for value in row]
            for row in values
        ]
        matrix = Matrix(formatted, h_buff=0.86, v_buff=0.64).scale(0.94)
        columns = matrix.get_columns()
        separator_x = (columns[2].get_right()[0] + columns[3].get_left()[0]) / 2
        separator = Line(
            UP * 1.18,
            DOWN * 1.18,
            stroke_width=2.0,
        ).move_to([separator_x, matrix.get_center()[1], 0])
        display = VGroup(matrix, separator)
        return matrix, display

    @staticmethod
    def _entry_box(matrix, row: int, column: int, color):
        entry = matrix.get_entries()[row * 4 + column]
        return SurroundingRectangle(entry, color=color, buff=0.10)

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
