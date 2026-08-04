"""CP111 presentation: the reusable Gaussian elimination algorithm."""

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

from engine.elimination_algorithm import EliminationAlgorithm


class EliminationAlgorithmPresentation(Scene):
    """Make the pivot cycle of Gaussian elimination explicit."""

    TITLE = "The Gaussian Elimination Algorithm"
    STEPS = (
        "1. Find a nonzero pivot.",
        "2. Swap it into position if needed.",
        "3. Clear every entry below it.",
        "4. Move one row down and one column right.",
        "5. Repeat until no pivot remains.",
    )
    PIVOT_COLORS = (BLUE, GREEN, RED)

    def construct(self) -> None:
        snapshot = EliminationAlgorithm().snapshot()

        title = Text(self.TITLE, font_size=39).to_edge(UP, buff=0.28)
        subtitle = Text(
            "Repeat the same pivot cycle until the matrix reaches echelon form.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.14)
        subtitle.scale_to_fit_width(11.5)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        cycle_heading = Text(
            "Cycle 1: pivot position (row 1, column 1)",
            font_size=28,
        ).move_to(UP * 1.62)
        current_matrix, current_display = self._augmented_matrix(snapshot.original_augmented)
        current_display.move_to(LEFT * 2.85 + DOWN * 0.35)
        current_panel = self._algorithm_panel(active_step=0, completed_steps=())
        current_panel.move_to(RIGHT * 3.20 + DOWN * 0.15)
        footer = Text(
            "The first candidate is zero, so the algorithm searches below it.",
            font_size=23,
        ).to_edge(DOWN, buff=0.28)
        footer.scale_to_fit_width(11.4)
        self.play(
            FadeIn(cycle_heading),
            FadeIn(current_display),
            FadeIn(current_panel),
            FadeIn(footer),
            run_time=1.2,
        )
        self.wait(1.8)

        active_box = self._active_region_box(current_matrix, start_row=0, start_column=0)
        zero_box = self._entry_box(current_matrix, 0, 0, RED)
        pivot_candidate = self._entry_box(current_matrix, 1, 0, GREEN)
        self.play(Create(active_box), Create(zero_box), run_time=0.8)
        self.wait(1.1)
        self.play(Create(pivot_candidate), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(zero_box), FadeOut(pivot_candidate), run_time=0.5)

        current_panel = self._replace_panel(
            current_panel,
            active_step=1,
            completed_steps=(0,),
        )
        operation = MathTex(
            snapshot.actions[0].label,
            font_size=35,
            color=YELLOW,
        ).move_to(self._operation_anchor())
        self.play(Write(operation), run_time=0.8)
        current_matrix, current_display = self._replace_matrix(
            current_matrix,
            current_display,
            snapshot.actions[0].result,
            run_time=1.3,
        )
        self.wait(1.0)

        current_panel = self._replace_panel(
            current_panel,
            active_step=2,
            completed_steps=(0, 1),
        )
        pivot_box = self._entry_box(current_matrix, 0, 0, BLUE)
        target_box = SurroundingRectangle(current_matrix.get_rows()[2], color=RED, buff=0.10)
        clear_note = Text(
            "Row 2 already has zero below the pivot; clear row 3.",
            font_size=22,
        ).to_edge(DOWN, buff=0.28)
        clear_note.scale_to_fit_width(11.2)
        self.play(
            ReplacementTransform(footer, clear_note),
            Create(pivot_box),
            Create(target_box),
            run_time=0.8,
        )
        footer = clear_note
        next_operation = MathTex(snapshot.actions[1].label, font_size=35, color=YELLOW).move_to(operation)
        self.play(ReplacementTransform(operation, next_operation), run_time=0.7)
        operation = next_operation
        current_matrix, current_display = self._replace_matrix(
            current_matrix,
            current_display,
            snapshot.actions[1].result,
            run_time=1.3,
        )
        self.play(FadeOut(pivot_box), FadeOut(target_box), run_time=0.5)
        self.wait(1.0)

        current_panel = self._replace_panel(
            current_panel,
            active_step=3,
            completed_steps=(0, 1, 2),
        )
        cycle_two = Text(
            "Cycle 2: pivot position (row 2, column 2)",
            font_size=28,
        ).move_to(cycle_heading)
        second_active = self._active_region_box(current_matrix, start_row=1, start_column=1)
        advance_note = Text(
            "The first pivot column is finished. Shrink the active region.",
            font_size=23,
        ).to_edge(DOWN, buff=0.28)
        self.play(
            ReplacementTransform(cycle_heading, cycle_two),
            ReplacementTransform(active_box, second_active),
            ReplacementTransform(footer, advance_note),
            FadeOut(operation),
            run_time=1.0,
        )
        cycle_heading = cycle_two
        active_box = second_active
        footer = advance_note
        self.wait(1.3)

        current_panel = self._replace_panel(
            current_panel,
            active_step=0,
            completed_steps=(),
        )
        second_pivot = self._entry_box(current_matrix, 1, 1, GREEN)
        find_note = Text(
            "The next candidate is already nonzero: it becomes the second pivot.",
            font_size=22,
        ).to_edge(DOWN, buff=0.28)
        find_note.scale_to_fit_width(11.3)
        self.play(ReplacementTransform(footer, find_note), Create(second_pivot), run_time=0.8)
        footer = find_note
        self.wait(1.2)

        current_panel = self._replace_panel(
            current_panel,
            active_step=1,
            completed_steps=(0,),
        )
        no_swap = Text(
            "No row swap is needed.",
            font_size=24,
            color=GREEN,
        ).move_to(self._operation_anchor())
        self.play(FadeIn(no_swap), run_time=0.7)
        self.wait(1.0)

        current_panel = self._replace_panel(
            current_panel,
            active_step=2,
            completed_steps=(0, 1),
        )
        below_second = self._entry_box(current_matrix, 2, 1, RED)
        self.play(Create(below_second), run_time=0.6)
        operation = MathTex(snapshot.actions[2].label, font_size=35, color=YELLOW).move_to(no_swap)
        self.play(ReplacementTransform(no_swap, operation), run_time=0.7)
        current_matrix, current_display = self._replace_matrix(
            current_matrix,
            current_display,
            snapshot.actions[2].result,
            run_time=1.3,
        )
        self.play(FadeOut(second_pivot), FadeOut(below_second), run_time=0.5)
        self.wait(1.0)

        current_panel = self._replace_panel(
            current_panel,
            active_step=3,
            completed_steps=(0, 1, 2),
        )
        cycle_three = Text(
            "Cycle 3: pivot position (row 3, column 3)",
            font_size=28,
        ).move_to(cycle_heading)
        third_active = self._active_region_box(current_matrix, start_row=2, start_column=2)
        last_note = Text(
            "The final pivot has no rows beneath it, so elimination is complete.",
            font_size=22,
        ).to_edge(DOWN, buff=0.28)
        last_note.scale_to_fit_width(11.3)
        self.play(
            ReplacementTransform(cycle_heading, cycle_three),
            ReplacementTransform(active_box, third_active),
            ReplacementTransform(footer, last_note),
            FadeOut(operation),
            run_time=1.0,
        )
        cycle_heading = cycle_three
        active_box = third_active
        footer = last_note
        third_pivot = self._entry_box(current_matrix, 2, 2, RED)
        self.play(Create(third_pivot), run_time=0.7)
        self.wait(1.5)

        current_panel = self._replace_panel(
            current_panel,
            active_step=4,
            completed_steps=(0, 1, 2, 3),
        )
        finish_note = Text(
            "No active rows remain: stop with row echelon form.",
            font_size=24,
            color=GREEN,
        ).to_edge(DOWN, buff=0.28)
        self.play(ReplacementTransform(footer, finish_note), run_time=0.7)
        footer = finish_note
        self.wait(1.7)

        self.play(
            FadeOut(cycle_heading),
            FadeOut(active_box),
            FadeOut(third_pivot),
            FadeOut(current_display),
            FadeOut(current_panel),
            FadeOut(footer),
            FadeOut(subtitle),
            run_time=1.0,
        )

        summary_heading = Text("One reusable pivot cycle", font_size=31, color=YELLOW)
        summary_heading.next_to(title, DOWN, buff=0.25)
        final_matrix, final_display = self._augmented_matrix(snapshot.echelon_augmented)
        final_display.move_to(LEFT * 3.0 + DOWN * 0.20)
        pivot_boxes = VGroup(
            *[
                self._entry_box(final_matrix, row, column, color)
                for (row, column), color in zip(
                    snapshot.pivot_positions,
                    self.PIVOT_COLORS,
                    strict=True,
                )
            ]
        )
        final_panel = self._algorithm_panel(active_step=None, completed_steps=(0, 1, 2, 3, 4))
        final_panel.move_to(RIGHT * 3.15 + DOWN * 0.10)
        summary_footer = Text(
            "Each cycle creates one pivot and permanently clears its column below.",
            font_size=23,
            color=GREEN,
        ).to_edge(DOWN, buff=0.28)
        summary_footer.scale_to_fit_width(11.5)
        self.play(
            FadeIn(summary_heading),
            FadeIn(final_display),
            Create(pivot_boxes),
            FadeIn(final_panel),
            FadeIn(summary_footer),
            run_time=1.2,
        )
        self.wait(4.0)

    @staticmethod
    def _operation_anchor():
        """Keep operation labels above the matrix and clear of the checklist."""
        return LEFT * 2.85 + UP * 1.02

    def _algorithm_panel(self, *, active_step: int | None, completed_steps: tuple[int, ...]):
        heading = Text("Pivot cycle", font_size=27, color=YELLOW)
        lines = VGroup(
            *[
                Text(
                    text,
                    font_size=22,
                    color=(
                        YELLOW
                        if index == active_step
                        else GREEN
                        if index in completed_steps
                        else WHITE
                    ),
                )
                for index, text in enumerate(self.STEPS)
            ]
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        content = VGroup(heading, lines).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        content.scale_to_fit_width(5.3)
        box = SurroundingRectangle(content, color=BLUE, buff=0.18)
        return VGroup(box, content)

    def _replace_panel(self, old_panel, *, active_step: int | None, completed_steps: tuple[int, ...]):
        new_panel = self._algorithm_panel(
            active_step=active_step,
            completed_steps=completed_steps,
        ).move_to(old_panel)
        self.play(ReplacementTransform(old_panel, new_panel), run_time=0.7)
        return new_panel

    def _replace_matrix(self, current_matrix, current_display, next_values, *, run_time: float):
        next_matrix, next_display = self._augmented_matrix(next_values)
        next_display.move_to(current_display)
        self.play(ReplacementTransform(current_display, next_display), run_time=run_time)
        return next_matrix, next_display

    def _active_region_box(self, matrix, *, start_row: int, start_column: int):
        entries = VGroup(
            *[
                matrix.get_entries()[row * 4 + column]
                for row in range(start_row, 3)
                for column in range(start_column, 4)
            ]
        )
        return SurroundingRectangle(entries, color=BLUE, buff=0.16)

    @staticmethod
    def _entry_box(matrix, row: int, column: int, color):
        entry = matrix.get_entries()[row * 4 + column]
        return SurroundingRectangle(entry, color=color, buff=0.10)

    def _augmented_matrix(self, values):
        formatted = [[self._format_number(value) for value in row] for row in values]
        matrix = Matrix(formatted, h_buff=0.84, v_buff=0.62).scale(0.90)
        columns = matrix.get_columns()
        separator_x = (columns[2].get_right()[0] + columns[3].get_left()[0]) / 2
        separator = Line(UP * 1.14, DOWN * 1.14, stroke_width=2.0).move_to(
            [separator_x, matrix.get_center()[1], 0]
        )
        return matrix, VGroup(matrix, separator)

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
