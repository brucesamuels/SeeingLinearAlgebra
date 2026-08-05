"""CP118 presentation: rank, pivots, and consistency."""

from __future__ import annotations

from manim import (
    Arrow,
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
    Write,
    YELLOW,
)

from engine.rank_pivots_consistency import RankConsistencyCase, RankPivotsConsistency


class RankPivotsConsistencyPresentation(Scene):
    """Read consistency and solution count from pivots and rank."""

    def construct(self) -> None:
        snapshot = RankPivotsConsistency().snapshot()

        title = Text("Rank, Pivots, and Consistency", font_size=40).to_edge(UP, buff=0.27)
        subtitle = Text(
            "The RREF matrix tells us whether a system can be solved—and how many solutions it has.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.13)
        subtitle.scale_to_fit_width(11.5)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        heading = Text("Pivots determine rank", font_size=29).move_to(UP * 1.92)
        matrix, display = self._augmented_matrix(snapshot.infinite.rref_augmented)
        display.move_to(LEFT * 3.08 + DOWN * 0.30)
        labels = self._column_labels(matrix)
        pivot_boxes = self._pivot_boxes(matrix, ((0, 0), (1, 1)), color=BLUE)
        rank_panel = self._pivot_rank_panel(snapshot.infinite).move_to(RIGHT * 3.18 + DOWN * 0.12)
        footer = Text(
            "Rank is the number of pivot rows—or equivalently, the number of pivot columns.",
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.28)
        footer.scale_to_fit_width(11.2)
        self.play(
            FadeIn(heading),
            FadeIn(display),
            FadeIn(labels),
            FadeIn(rank_panel),
            FadeIn(footer),
            run_time=1.2,
        )
        self.play(*[Create(box) for box in pivot_boxes], run_time=0.9)
        self.wait(2.3)

        compare_heading = Text("Consistency is a comparison of two ranks", font_size=29).move_to(UP * 1.96)
        consistent_card = self._comparison_card(
            snapshot.infinite,
            title="Equal ranks",
            accent=GREEN,
            contradiction=False,
        ).move_to(LEFT * 3.18 + DOWN * 0.28)
        inconsistent_card = self._comparison_card(
            snapshot.inconsistent,
            title="An augmented-column pivot",
            accent=RED,
            contradiction=True,
        ).move_to(RIGHT * 3.18 + DOWN * 0.28)
        self.play(
            ReplacementTransform(heading, compare_heading),
            FadeOut(display),
            FadeOut(labels),
            FadeOut(rank_panel),
            FadeOut(footer),
            *[FadeOut(box) for box in pivot_boxes],
            FadeIn(consistent_card),
            FadeIn(inconsistent_card),
            run_time=1.25,
        )
        self.wait(2.8)

        prompt = VGroup(
            Text("Pause and Predict", font_size=27, color=YELLOW),
            Text("Which matrix represents a solvable system? What feature decides?", font_size=23),
        ).arrange(DOWN, buff=0.14).move_to(DOWN * 0.20)
        prompt_box = SurroundingRectangle(prompt, color=YELLOW, buff=0.24)
        self.play(
            FadeOut(compare_heading),
            FadeOut(consistent_card),
            FadeOut(inconsistent_card),
            FadeIn(prompt_box),
            FadeIn(prompt),
            run_time=0.9,
        )
        self.wait(2.4)

        unique_heading = Text("Equal ranks and a pivot in every variable column", font_size=28).move_to(UP * 1.96)
        unique_heading.scale_to_fit_width(11.2)
        unique_matrix, unique_display = self._augmented_matrix(snapshot.unique.rref_augmented)
        unique_display.move_to(LEFT * 3.08 + DOWN * 0.28)
        unique_labels = self._column_labels(unique_matrix)
        unique_boxes = self._pivot_boxes(unique_matrix, ((0, 0), (1, 1), (2, 2)), color=BLUE)
        unique_panel = self._classification_panel(snapshot.unique, accent=GREEN).move_to(RIGHT * 3.18 + DOWN * 0.10)
        unique_footer = Text(
            "There are no free variables, so back substitution produces one solution.",
            font_size=22,
            color=GREEN,
        ).to_edge(DOWN, buff=0.28)
        unique_footer.scale_to_fit_width(11.1)
        self.play(
            FadeOut(prompt_box),
            FadeOut(prompt),
            FadeIn(unique_heading),
            FadeIn(unique_display),
            FadeIn(unique_labels),
            FadeIn(unique_panel),
            FadeIn(unique_footer),
            run_time=1.2,
        )
        self.play(*[Create(box) for box in unique_boxes], run_time=0.9)
        self.wait(2.5)

        infinite_heading = Text("Equal ranks but fewer pivots than variables", font_size=29).move_to(UP * 1.96)
        infinite_matrix, infinite_display = self._augmented_matrix(snapshot.infinite.rref_augmented)
        infinite_display.move_to(LEFT * 3.08 + DOWN * 0.28)
        infinite_labels = self._column_labels(infinite_matrix)
        infinite_boxes = self._pivot_boxes(infinite_matrix, ((0, 0), (1, 1)), color=BLUE)
        free_box = SurroundingRectangle(infinite_matrix.get_columns()[2], color=YELLOW, buff=0.10)
        infinite_panel = self._classification_panel(snapshot.infinite, accent=YELLOW).move_to(RIGHT * 3.18 + DOWN * 0.10)
        infinite_footer = Text(
            "The nonpivot z-column creates one free variable and therefore infinitely many solutions.",
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.28)
        infinite_footer.scale_to_fit_width(11.2)
        self.play(
            ReplacementTransform(unique_heading, infinite_heading),
            FadeOut(unique_display),
            FadeOut(unique_labels),
            FadeOut(unique_panel),
            FadeOut(unique_footer),
            *[FadeOut(box) for box in unique_boxes],
            FadeIn(infinite_display),
            FadeIn(infinite_labels),
            FadeIn(infinite_panel),
            FadeIn(infinite_footer),
            run_time=1.2,
        )
        self.play(*[Create(box) for box in infinite_boxes], Create(free_box), run_time=0.9)
        self.wait(2.6)

        inconsistent_heading = Text("An augmented-column pivot destroys consistency", font_size=29).move_to(UP * 1.96)
        inconsistent_matrix, inconsistent_display = self._augmented_matrix(snapshot.inconsistent.rref_augmented)
        inconsistent_display.move_to(LEFT * 3.08 + DOWN * 0.28)
        inconsistent_labels = self._column_labels(inconsistent_matrix)
        coefficient_boxes = self._pivot_boxes(inconsistent_matrix, ((0, 0), (1, 1)), color=BLUE)
        augmented_box = self._pivot_boxes(inconsistent_matrix, ((2, 3),), color=RED)[0]
        inconsistent_panel = self._classification_panel(snapshot.inconsistent, accent=RED).move_to(RIGHT * 3.18 + DOWN * 0.10)
        inconsistent_footer = MathTex(r"0=3\quad\Longrightarrow\quad\text{no solution}", font_size=37, color=RED).to_edge(DOWN, buff=0.28)
        self.play(
            ReplacementTransform(infinite_heading, inconsistent_heading),
            FadeOut(infinite_display),
            FadeOut(infinite_labels),
            FadeOut(infinite_panel),
            FadeOut(infinite_footer),
            *[FadeOut(box) for box in infinite_boxes],
            FadeOut(free_box),
            FadeIn(inconsistent_display),
            FadeIn(inconsistent_labels),
            FadeIn(inconsistent_panel),
            FadeIn(inconsistent_footer),
            run_time=1.2,
        )
        self.play(*[Create(box) for box in coefficient_boxes], Create(augmented_box), run_time=0.9)
        self.wait(2.7)

        decision_heading = Text("Read the solution type from rank and pivots", font_size=29).move_to(UP * 1.96)
        decision_tree = self._decision_tree().move_to(DOWN * 0.35)
        decision_footer = MathTex(
            r"\#\text{ free variables}=n-\operatorname{rank}(A)",
            font_size=35,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.24)
        self.play(
            ReplacementTransform(inconsistent_heading, decision_heading),
            FadeOut(inconsistent_display),
            FadeOut(inconsistent_labels),
            FadeOut(inconsistent_panel),
            FadeOut(inconsistent_footer),
            *[FadeOut(box) for box in coefficient_boxes],
            FadeOut(augmented_box),
            FadeIn(decision_tree),
            FadeIn(decision_footer),
            run_time=1.25,
        )
        self.wait(3.5)

    def _augmented_matrix(self, values):
        formatted = [[self._format_number(value) for value in row] for row in values]
        matrix = Matrix(formatted, h_buff=0.84, v_buff=0.65).scale(0.92)
        columns = matrix.get_columns()
        separator_x = (columns[2].get_right()[0] + columns[3].get_left()[0]) / 2
        separator = Line(UP * 1.18, DOWN * 1.18, stroke_width=2.0).move_to(
            [separator_x, matrix.get_center()[1], 0]
        )
        return matrix, VGroup(matrix, separator)

    @staticmethod
    def _column_labels(matrix: Matrix):
        labels = VGroup(
            MathTex("x", font_size=29, color=BLUE),
            MathTex("y", font_size=29, color=BLUE),
            MathTex("z", font_size=29, color=YELLOW),
            MathTex("b", font_size=29, color=GREEN),
        )
        for label, column in zip(labels, matrix.get_columns(), strict=True):
            label.move_to([column.get_center()[0], matrix.get_top()[1] + 0.23, 0])
        return labels

    @staticmethod
    def _pivot_boxes(matrix: Matrix, positions: tuple[tuple[int, int], ...], *, color):
        entries = matrix.get_entries()
        boxes = VGroup()
        for row, column in positions:
            boxes.add(SurroundingRectangle(entries[row * 4 + column], color=color, buff=0.10))
        return boxes

    @staticmethod
    def _pivot_rank_panel(case: RankConsistencyCase):
        rank = MathTex(r"\operatorname{rank}(A)=2", font_size=39, color=BLUE)
        pivots = Text("two pivots", font_size=26, color=YELLOW)
        columns = Text("pivot columns: x and y", font_size=23)
        free = Text("nonpivot column: z", font_size=23, color=YELLOW)
        group = VGroup(rank, pivots, columns, free).arrange(DOWN, buff=0.31)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    def _comparison_card(self, case: RankConsistencyCase, *, title: str, accent, contradiction: bool):
        card_title = Text(title, font_size=24, color=accent)
        matrix, display = self._augmented_matrix(case.rref_augmented)
        display.scale(0.67)
        if contradiction:
            comparison = MathTex(r"\operatorname{rank}(A)=2<3=\operatorname{rank}([A\mid\mathbf b])", font_size=25, color=RED)
            verdict = Text("inconsistent", font_size=24, color=RED)
            marker = SurroundingRectangle(matrix.get_entries()[11], color=RED, buff=0.08)
        else:
            comparison = MathTex(r"\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b])=2", font_size=25, color=GREEN)
            verdict = Text("consistent", font_size=24, color=GREEN)
            marker = VGroup()
        group = VGroup(card_title, display, comparison, verdict).arrange(DOWN, buff=0.24)
        box = SurroundingRectangle(group, color=accent, buff=0.18)
        if contradiction:
            marker.move_to(matrix.get_entries()[11])
        return VGroup(box, group, marker)

    @staticmethod
    def _classification_panel(case: RankConsistencyCase, *, accent):
        rank_a = MathTex(
            rf"\operatorname{{rank}}(A)={case.coefficient_rank}",
            font_size=37,
            color=BLUE,
        )
        rank_augmented = MathTex(
            rf"\operatorname{{rank}}([A\mid\mathbf b])={case.augmented_rank}",
            font_size=35,
            color=GREEN if case.is_consistent else RED,
        )
        if case.solution_type == "unique":
            comparison = MathTex(r"3=n", font_size=35, color=GREEN)
            verdict = Text("one solution", font_size=28, color=GREEN)
            detail = Text("no free variables", font_size=23)
        elif case.solution_type == "infinite":
            comparison = MathTex(r"2<n=3", font_size=35, color=YELLOW)
            verdict = Text("infinitely many solutions", font_size=27, color=YELLOW)
            detail = Text("one free variable", font_size=23)
        else:
            comparison = MathTex(r"2<3", font_size=35, color=RED)
            verdict = Text("no solution", font_size=28, color=RED)
            detail = Text("contradictory row", font_size=23)
        group = VGroup(rank_a, rank_augmented, comparison, verdict, detail).arrange(DOWN, buff=0.28)
        box = SurroundingRectangle(group, color=accent, buff=0.19)
        return VGroup(box, group)

    @staticmethod
    def _decision_tree():
        root_text = MathTex(
            r"\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b])?",
            font_size=34,
        )
        root_box = SurroundingRectangle(root_text, color=YELLOW, buff=0.18)
        root = VGroup(root_box, root_text).move_to(UP * 0.95)

        none_text = Text("No solution", font_size=27, color=RED)
        none_box = SurroundingRectangle(none_text, color=RED, buff=0.20)
        none = VGroup(none_box, none_text).move_to(LEFT * 3.35 + DOWN * 0.85)

        second_text = MathTex(r"\operatorname{rank}(A)=n?", font_size=34)
        second_box = SurroundingRectangle(second_text, color=BLUE, buff=0.18)
        second = VGroup(second_box, second_text).move_to(RIGHT * 2.15 + DOWN * 0.30)

        unique_text = Text("Unique solution", font_size=25, color=GREEN)
        unique_box = SurroundingRectangle(unique_text, color=GREEN, buff=0.20)
        unique = VGroup(unique_box, unique_text).move_to(RIGHT * 0.80 + DOWN * 2.10)

        infinite_text = Text("Infinitely many solutions", font_size=24, color=YELLOW)
        infinite_box = SurroundingRectangle(infinite_text, color=YELLOW, buff=0.20)
        infinite = VGroup(infinite_box, infinite_text).move_to(RIGHT * 4.15 + DOWN * 2.10)

        root_no = Arrow(root.get_bottom(), none.get_top(), buff=0.10, stroke_width=3)
        root_yes = Arrow(root.get_bottom() + RIGHT * 0.55, second.get_top() + LEFT * 0.30, buff=0.10, stroke_width=3)
        unique_arrow = Arrow(second.get_bottom() + LEFT * 0.35, unique.get_top(), buff=0.10, stroke_width=3)
        infinite_arrow = Arrow(second.get_bottom() + RIGHT * 0.35, infinite.get_top(), buff=0.10, stroke_width=3)

        no_label = Text("No", font_size=20, color=RED).next_to(root_no, LEFT, buff=0.06)
        yes_label = Text("Yes", font_size=20, color=GREEN).next_to(root_yes, RIGHT, buff=0.06)
        equals_label = MathTex(r"=n", font_size=23, color=GREEN).next_to(unique_arrow, LEFT, buff=0.06)
        less_label = MathTex(r"<n", font_size=23, color=YELLOW).next_to(infinite_arrow, RIGHT, buff=0.06)

        return VGroup(
            root,
            none,
            second,
            unique,
            infinite,
            root_no,
            root_yes,
            unique_arrow,
            infinite_arrow,
            no_label,
            yes_label,
            equals_label,
            less_label,
        )

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        return f"{float(value):g}"
