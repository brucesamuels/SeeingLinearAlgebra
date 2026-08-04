"""CP108 presentation: why row replacement preserves solutions."""

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

from engine.row_replacement_preserves_solutions import (
    RowReplacementPreservesSolutions,
)


class RowReplacementPreservesSolutionsPresentation(Scene):
    """Explain preservation by forward implication and reversibility."""

    TITLE = "Why Does Row Replacement Preserve Solutions?"

    def construct(self) -> None:
        model = RowReplacementPreservesSolutions()
        snapshot = model.snapshot()

        title = Text(self.TITLE, font_size=39).to_edge(UP, buff=0.28)
        subtitle = Text(
            "A legal replacement changes an equation—but loses no information.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.14)
        self.play(Write(title), FadeIn(subtitle), run_time=1.2)

        original_heading = Text("Start with the original system", font_size=29)
        original_system = self._equation_group((r"E_1:\ x+y=2", r"E_2:\ 2x-y=1"))
        original_group = VGroup(original_heading, original_system).arrange(
            DOWN,
            buff=0.40,
        ).move_to(DOWN * 0.05)
        self.play(FadeIn(original_heading), Write(original_system), run_time=1.4)

        solution_badge = VGroup(
            Text("Common solution", font_size=23),
            MathTex(r"(x,y)=(1,1)", color=GREEN, font_size=35),
        ).arrange(DOWN, buff=0.10).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(solution_badge), run_time=0.7)
        self.wait(2.0)

        operation = MathTex(
            r"R_2\leftarrow R_2-2R_1",
            color=YELLOW,
            font_size=39,
        ).next_to(original_group, DOWN, buff=0.42)
        first_box = SurroundingRectangle(original_system[0], color=BLUE, buff=0.10)
        second_box = SurroundingRectangle(original_system[1], color=YELLOW, buff=0.10)
        self.play(Write(operation), run_time=0.8)
        self.play(Create(first_box), Create(second_box), run_time=0.7)
        self.wait(0.8)

        self.play(
            FadeOut(solution_badge),
            FadeOut(first_box),
            FadeOut(second_box),
            FadeOut(original_heading),
            FadeOut(original_system),
            run_time=0.8,
        )

        forward_heading = Text(
            "Every original solution satisfies the replacement equation",
            font_size=28,
        ).next_to(subtitle, DOWN, buff=0.34)
        derivation = VGroup(
            MathTex(r"(2x-y)-2(x+y)=1-2(2)", font_size=36),
            MathTex(r"-3y=-3", color=YELLOW, font_size=42),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.15)
        forward_note = Text(
            "Subtracting equal quantities from equal quantities preserves equality.",
            font_size=24,
        ).to_edge(DOWN, buff=0.34)
        forward_note.scale_to_fit_width(11.4)
        self.play(
            ReplacementTransform(operation, forward_heading),
            Write(derivation[0]),
            run_time=1.1,
        )
        self.play(ReplacementTransform(derivation[0].copy(), derivation[1]), run_time=1.0)
        self.play(FadeIn(forward_note), run_time=0.6)
        self.wait(2.2)

        self.play(FadeOut(forward_note), FadeOut(derivation), run_time=0.7)

        compare_heading = Text("Original system and transformed system", font_size=29)
        compare_heading.next_to(subtitle, DOWN, buff=0.34)
        original_small = self._equation_group((r"x+y=2", r"2x-y=1"), font_size=35)
        transformed_small = self._equation_group((r"x+y=2", r"-3y=-3"), font_size=35)
        original_label = Text("Original", font_size=25, color=BLUE)
        transformed_label = Text("After replacement", font_size=25, color=YELLOW)
        left_panel = VGroup(original_label, original_small).arrange(DOWN, buff=0.28)
        right_panel = VGroup(transformed_label, transformed_small).arrange(DOWN, buff=0.28)
        panels = VGroup(left_panel, right_panel).arrange(RIGHT, buff=1.65).move_to(DOWN * 0.05)
        implication = MathTex(r"\Longrightarrow", font_size=42).move_to(DOWN * 0.05)
        self.play(
            ReplacementTransform(forward_heading, compare_heading),
            FadeIn(left_panel),
            FadeIn(right_panel),
            Write(implication),
            run_time=1.2,
        )

        verification = VGroup(
            MathTex(r"1+1=2", color=GREEN, font_size=31),
            MathTex(r"-3(1)=-3", color=GREEN, font_size=31),
        ).arrange(RIGHT, buff=1.45).to_edge(DOWN, buff=0.35)
        self.play(Write(verification), run_time=0.9)
        self.wait(2.0)

        prompt = VGroup(
            Text("But did we lose any solutions?", font_size=29, color=YELLOW),
            Text("Can the original second equation be recovered?", font_size=25),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.26)
        self.play(FadeOut(verification), FadeIn(prompt), run_time=0.7)
        self.wait(2.2)
        self.play(FadeOut(prompt), run_time=0.5)

        self.play(
            FadeOut(compare_heading),
            FadeOut(left_panel),
            FadeOut(right_panel),
            FadeOut(implication),
            run_time=0.8,
        )

        reverse_heading = Text(
            "The replacement is reversible",
            font_size=30,
            color=YELLOW,
        ).next_to(subtitle, DOWN, buff=0.34)
        inverse_operation = MathTex(
            r"R_2\leftarrow R_2+2R_1",
            font_size=39,
            color=YELLOW,
        )
        recovery = VGroup(
            MathTex(r"(-3y)+2(x+y)=-3+2(2)", font_size=35),
            MathTex(r"2x-y=1", color=GREEN, font_size=42),
        ).arrange(DOWN, buff=0.32)
        reverse_group = VGroup(inverse_operation, recovery).arrange(
            DOWN,
            buff=0.45,
        ).move_to(DOWN * 0.15)
        reverse_note = Text(
            "The original equation is recovered, so no information was lost.",
            font_size=25,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(reverse_heading), Write(inverse_operation), run_time=0.9)
        self.play(Write(recovery[0]), run_time=0.9)
        self.play(ReplacementTransform(recovery[0].copy(), recovery[1]), run_time=0.9)
        self.play(FadeIn(reverse_note), run_time=0.6)
        self.wait(2.3)

        self.play(
            FadeOut(reverse_heading),
            FadeOut(reverse_group),
            FadeOut(reverse_note),
            run_time=0.8,
        )

        matrix_heading = Text("The same reversible move in the augmented matrix", font_size=28)
        matrix_heading.next_to(subtitle, DOWN, buff=0.34)
        original_matrix, original_display = self._augmented_matrix(snapshot.original_augmented)
        transformed_matrix, transformed_display = self._augmented_matrix(
            snapshot.transformed_augmented
        )
        original_display.move_to(LEFT * 3.1 + DOWN * 0.05)
        transformed_display.move_to(RIGHT * 3.1 + DOWN * 0.05)
        forward_arrow = MathTex(
            r"R_2\leftarrow R_2-2R_1",
            color=YELLOW,
            font_size=31,
        ).move_to(UP * 0.45)
        backward_arrow = MathTex(
            r"R_2\leftarrow R_2+2R_1",
            color=GREEN,
            font_size=31,
        ).move_to(DOWN * 0.75)
        center_line = Line(UP * 0.05, DOWN * 0.05, stroke_width=0)
        self.play(FadeIn(matrix_heading), FadeIn(original_display), run_time=0.9)
        self.play(Write(forward_arrow), FadeIn(transformed_display), run_time=1.0)
        self.play(Write(backward_arrow), run_time=0.8)
        matrix_note = Text(
            "Forward and inverse row replacements connect the same two systems.",
            font_size=24,
        ).to_edge(DOWN, buff=0.32)
        self.play(FadeIn(matrix_note), run_time=0.6)
        self.wait(2.2)

        self.play(
            FadeOut(matrix_heading),
            FadeOut(original_display),
            FadeOut(transformed_display),
            FadeOut(forward_arrow),
            FadeOut(backward_arrow),
            FadeOut(matrix_note),
            run_time=0.9,
        )

        conclusion_heading = Text("Why the solution set is preserved", font_size=31, color=YELLOW)
        general_forward = MathTex(
            r"R_i\leftarrow R_i+cR_j",
            font_size=42,
        )
        general_reverse = MathTex(
            r"R_i\leftarrow R_i-cR_j",
            font_size=42,
        )
        conclusion = VGroup(
            Text("The new equation follows from the old equations.", font_size=26),
            Text("The old equation is recovered by the inverse replacement.", font_size=26),
            Text("Therefore both systems have exactly the same solutions.", font_size=27, color=GREEN),
        ).arrange(DOWN, buff=0.20)
        final_group = VGroup(
            conclusion_heading,
            general_forward,
            general_reverse,
            conclusion,
        ).arrange(DOWN, buff=0.34).move_to(DOWN * 0.18)
        final_group.scale_to_fit_width(11.5)
        self.play(FadeIn(final_group), run_time=1.0)
        self.wait(4.0)

    def _equation_group(
        self,
        equation_tex: tuple[str, str],
        *,
        font_size: int = 39,
    ) -> VGroup:
        return VGroup(
            *[MathTex(tex, font_size=font_size) for tex in equation_tex]
        ).arrange(DOWN, buff=0.48, aligned_edge=LEFT)

    def _augmented_matrix(self, values) -> tuple[Matrix, VGroup]:
        display_values = [
            [
                str(int(round(float(value))))
                if abs(float(value) - round(float(value))) < 1e-9
                else f"{float(value):g}"
                for value in row
            ]
            for row in values
        ]
        matrix = Matrix(display_values, h_buff=0.78, v_buff=0.62).scale(0.92)
        columns = matrix.get_columns()
        separator_x = (columns[1].get_right()[0] + columns[2].get_left()[0]) / 2
        separator = Line(UP * 0.85, DOWN * 0.85, stroke_width=2.0).move_to(
            [separator_x, matrix.get_center()[1], 0]
        )
        display = VGroup(matrix.get_brackets(), matrix.get_entries(), separator)
        return matrix, display
