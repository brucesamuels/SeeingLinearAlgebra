"""CP119 presentation: elementary matrices and complete row reduction."""

from __future__ import annotations

from fractions import Fraction

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
    Write,
    YELLOW,
)

from engine.elementary_matrices import (
    ElementaryMatrixCase,
    ElementaryMatrices,
    RowReductionStep,
)


class ElementaryMatricesPresentation(Scene):
    """Show elementary matrices, their inverses, and a full reduction product."""

    TRANSITION = 1.65
    HIGHLIGHT = 1.15
    READ = 2.2
    HEADING_Y = 2.18
    EXPLANATION_FONT_SIZE = 21

    def construct(self) -> None:
        snapshot = ElementaryMatrices().snapshot()

        title = Text("Elementary Matrices", font_size=41).to_edge(UP, buff=0.27)
        subtitle = Text(
            "Row operations, inverse operations, and complete row reduction as matrix multiplication.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.13)
        subtitle.scale_to_fit_width(11.4)
        self.play(Write(title), FadeIn(subtitle), run_time=1.9)

        heading = Text("Start with the identity matrix", font_size=30).move_to(UP * self.HEADING_Y)
        panel = self._definition_panel(snapshot.identity, snapshot.definition_tex).move_to(DOWN * 0.44)
        self.play(FadeIn(heading), FadeIn(panel), run_time=self.TRANSITION)
        self.wait(2.6)

        next_heading = Text("There are three types of elementary matrices", font_size=29).move_to(UP * self.HEADING_Y)
        next_panel = self._operation_overview().move_to(DOWN * 0.42)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.8)

        for case, accent, forward_title, inverse_title in (
            (snapshot.swap, BLUE, "Row interchange: perform the swap", "Undo the interchange with the same matrix"),
            (snapshot.scale, GREEN, "Row scaling: perform the scaling", "Undo the scaling with the reciprocal factor"),
            (snapshot.replacement, YELLOW, "Row replacement: perform the addition", "Undo the replacement with the opposite multiple"),
        ):
            heading, panel = self._show_forward_and_inverse(
                heading,
                panel,
                case,
                accent,
                forward_title,
                inverse_title,
            )

        next_heading = Text("Why the elementary matrix multiplies on the left", font_size=29).move_to(UP * self.HEADING_Y)
        next_panel = self._left_multiplication_panel(snapshot.left_multiplication_tex).move_to(DOWN * 0.46)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.8)

        next_heading = Text("A complete row reduction", font_size=30).move_to(UP * self.HEADING_Y)
        next_panel = self._reduction_overview_panel(snapshot).move_to(DOWN * 0.52)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.0)

        for step in snapshot.reduction_steps:
            next_heading = Text(f"Reduction step {step.index}", font_size=30).move_to(UP * self.HEADING_Y)
            next_panel, result_matrix = self._reduction_step_panel(step)
            next_panel.move_to(DOWN * 0.48)
            self.play(
                ReplacementTransform(heading, next_heading),
                ReplacementTransform(panel, next_panel),
                run_time=self.TRANSITION,
            )
            row_boxes = self._row_boxes(result_matrix, step.changed_rows, BLUE if step.index == 1 else GREEN)
            self.play(*[Create(box) for box in row_boxes], run_time=self.HIGHLIGHT)
            self.wait(1.9)
            self.play(*[FadeOut(box) for box in row_boxes], run_time=0.65)
            heading, panel = next_heading, next_panel

        next_heading = Text(
            "The four matrices multiply into one row-reduction matrix",
            font_size=24,
        ).move_to(UP * 2.32)
        next_heading.scale_to_fit_width(10.8)
        next_panel = self._cumulative_products_panel(snapshot).move_to(DOWN * 0.74)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.4)

        next_heading = Text("The complete product reduces A to I", font_size=30).move_to(UP * self.HEADING_Y)
        next_panel = self._reduction_matrix_panel(snapshot).move_to(DOWN * 0.50)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.2)

        next_heading = Text("Reverse the reduction with inverse elementary matrices", font_size=28).move_to(UP * self.HEADING_Y)
        next_heading.scale_to_fit_width(11.2)
        next_panel = self._reverse_overview_panel().move_to(DOWN * 0.46)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(2.8)

        for reverse_position, step in enumerate(snapshot.reverse_steps, start=1):
            original_index = step.index
            next_heading = self._reverse_step_heading(reverse_position, original_index)
            next_panel, result_matrix = self._reverse_step_panel(step)
            next_panel.move_to(DOWN * 0.48)
            self.play(
                ReplacementTransform(heading, next_heading),
                ReplacementTransform(panel, next_panel),
                run_time=self.TRANSITION,
            )
            row_boxes = self._row_boxes(result_matrix, step.changed_rows, YELLOW)
            self.play(*[Create(box) for box in row_boxes], run_time=self.HIGHLIGHT)
            self.wait(1.8)
            self.play(*[FadeOut(box) for box in row_boxes], run_time=0.65)
            heading, panel = next_heading, next_panel

        next_heading = Text("Forward and reverse factorizations", font_size=30).move_to(UP * self.HEADING_Y)
        next_panel = self._factorization_panel(snapshot).move_to(DOWN * 0.58)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        heading, panel = next_heading, next_panel
        self.wait(3.3)

        next_heading = Text("Elementary matrices encode the entire reduction", font_size=29).move_to(UP * self.HEADING_Y)
        next_heading.scale_to_fit_width(11.2)
        next_panel = self._summary_panel().move_to(DOWN * 0.48)
        self.play(
            ReplacementTransform(heading, next_heading),
            ReplacementTransform(panel, next_panel),
            run_time=self.TRANSITION,
        )
        self.wait(3.8)

    def _show_forward_and_inverse(
        self,
        heading,
        panel,
        case: ElementaryMatrixCase,
        accent,
        forward_title: str,
        inverse_title: str,
    ):
        forward_heading = Text(forward_title, font_size=29).move_to(UP * self.HEADING_Y)
        forward_panel, _, _, forward_result = self._product_panel(case)
        forward_panel.move_to(DOWN * 0.48)
        self.play(
            ReplacementTransform(heading, forward_heading),
            ReplacementTransform(panel, forward_panel),
            run_time=self.TRANSITION,
        )
        boxes = self._row_boxes(forward_result, case.changed_rows, accent)
        self.play(*[Create(box) for box in boxes], run_time=self.HIGHLIGHT)
        self.wait(self.READ)

        inverse_heading = Text(inverse_title, font_size=28).move_to(UP * self.HEADING_Y)
        inverse_heading.scale_to_fit_width(11.2)
        inverse_panel, _, _, inverse_result = self._inverse_product_panel(case)
        inverse_panel.move_to(DOWN * 0.48)
        self.play(
            ReplacementTransform(forward_heading, inverse_heading),
            FadeOut(forward_panel),
            *[FadeOut(box) for box in boxes],
            FadeIn(inverse_panel),
            run_time=self.TRANSITION,
        )
        inverse_boxes = self._row_boxes(inverse_result, case.changed_rows, accent)
        self.play(*[Create(box) for box in inverse_boxes], run_time=self.HIGHLIGHT)
        self.wait(self.READ)
        self.play(*[FadeOut(box) for box in inverse_boxes], run_time=0.65)
        return inverse_heading, inverse_panel

    @staticmethod
    def _definition_panel(identity, definition_tex: str):
        identity_matrix = ElementaryMatricesPresentation._matrix_mobject(identity, scale=0.80)
        arrow = MathTex(r"\xrightarrow{\text{one row operation}}", font_size=36, color=YELLOW)
        elementary = MathTex("E", font_size=58, color=BLUE)
        construction = VGroup(identity_matrix, arrow, elementary).arrange(RIGHT, buff=0.52)
        labels = VGroup(MathTex("I", font_size=31), MathTex("E", font_size=31, color=BLUE))
        labels[0].next_to(identity_matrix, UP, buff=0.16)
        labels[1].next_to(elementary, UP, buff=0.16)
        construction_with_labels = VGroup(construction, labels)
        definition = MathTex(definition_tex, font_size=31)
        definition.scale_to_fit_width(10.8)
        group = VGroup(construction_with_labels, definition).arrange(DOWN, buff=0.46)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _operation_overview():
        cards = VGroup(
            ElementaryMatricesPresentation._operation_card("Interchange", r"R_i\leftrightarrow R_j", "swap two rows", BLUE),
            ElementaryMatricesPresentation._operation_card("Scale", r"R_i\leftarrow cR_i", "c is nonzero", GREEN),
            ElementaryMatricesPresentation._operation_card("Replace", r"R_i\leftarrow R_i+cR_j", "add a row multiple", YELLOW),
        ).arrange(RIGHT, buff=0.42, aligned_edge=UP)
        footer = Text(
            "Apply the chosen row operation to I; the resulting matrix is elementary.",
            font_size=ElementaryMatricesPresentation.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        )
        ElementaryMatricesPresentation._shrink_to_fit_width(footer, 11.0)
        return VGroup(cards, footer).arrange(DOWN, buff=0.48)

    @staticmethod
    def _operation_card(title: str, operation_tex: str, note: str, accent):
        heading = Text(title, font_size=25, color=accent)
        operation = MathTex(operation_tex, font_size=32)
        explanation = Text(note, font_size=ElementaryMatricesPresentation.EXPLANATION_FONT_SIZE)
        group = VGroup(heading, operation, explanation).arrange(DOWN, buff=0.24)
        box = SurroundingRectangle(group, color=accent, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _product_panel(case: ElementaryMatrixCase):
        return ElementaryMatricesPresentation._matrix_product_panel(
            left=case.elementary_matrix,
            middle=case.source_matrix,
            result=case.product_matrix,
            left_label="E",
            middle_label="A",
            result_label="EA",
            operation_tex=case.operation_tex,
            explanation=case.explanation,
            left_color=BLUE,
            result_color=GREEN,
        )

    @staticmethod
    def _inverse_product_panel(case: ElementaryMatrixCase):
        return ElementaryMatricesPresentation._matrix_product_panel(
            left=case.inverse_matrix,
            middle=case.product_matrix,
            result=case.source_matrix,
            left_label=r"E^{-1}",
            middle_label="EA",
            result_label="A",
            operation_tex=case.inverse_operation_tex,
            explanation="The inverse elementary matrix restores the original matrix.",
            left_color=RED,
            result_color=BLUE,
        )

    @staticmethod
    def _matrix_product_panel(
        *,
        left,
        middle,
        result,
        left_label: str,
        middle_label: str,
        result_label: str,
        operation_tex: str,
        explanation: str,
        left_color,
        result_color,
    ):
        left_matrix = ElementaryMatricesPresentation._matrix_mobject(left, scale=0.62)
        middle_matrix = ElementaryMatricesPresentation._matrix_mobject(middle, scale=0.62)
        result_matrix = ElementaryMatricesPresentation._matrix_mobject(result, scale=0.62)
        times = MathTex(r"\cdot", font_size=40)
        equals = MathTex("=", font_size=40)
        row = VGroup(left_matrix, times, middle_matrix, equals, result_matrix).arrange(RIGHT, buff=0.27)
        labels = VGroup(
            MathTex(left_label, font_size=28, color=left_color),
            MathTex(middle_label, font_size=28),
            MathTex(result_label, font_size=28, color=result_color),
        )
        for label, matrix in zip(labels, (left_matrix, middle_matrix, result_matrix), strict=True):
            label.next_to(matrix, UP, buff=0.12)
        operation = MathTex(operation_tex, font_size=34, color=YELLOW)
        note = Text(explanation, font_size=ElementaryMatricesPresentation.EXPLANATION_FONT_SIZE)
        ElementaryMatricesPresentation._shrink_to_fit_width(note, 10.9)
        group = VGroup(VGroup(row, labels), operation, note).arrange(DOWN, buff=0.34)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group), left_matrix, middle_matrix, result_matrix

    @staticmethod
    def _row_boxes(matrix: Matrix, rows: tuple[int, ...], color):
        matrix_rows = matrix.get_rows()
        return VGroup(*[SurroundingRectangle(matrix_rows[row], color=color, buff=0.08) for row in rows])

    @staticmethod
    def _left_multiplication_panel(left_tex: str):
        principle = MathTex(left_tex, font_size=35, color=YELLOW)
        example_e = ElementaryMatricesPresentation._matrix_mobject([[1, 0, 0], [0, 1, 0], [2, 0, 1]], scale=0.72)
        row = MathTex(r"[\,2\quad0\quad1\,]", font_size=35, color=RED)
        arrow = MathTex(r"\Longrightarrow", font_size=37)
        combination = MathTex(r"(EA)_{3*}=2R_1+R_3", font_size=38, color=GREEN)
        example = VGroup(example_e, row, arrow, combination).arrange(RIGHT, buff=0.34)
        note = Text(
            "Each row of E specifies the linear combination of rows of A that becomes a new row.",
            font_size=ElementaryMatricesPresentation.EXPLANATION_FONT_SIZE,
        )
        ElementaryMatricesPresentation._shrink_to_fit_width(note, 11.0)
        group = VGroup(principle, example, note).arrange(DOWN, buff=0.42)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _reduction_overview_panel(snapshot):
        source = ElementaryMatricesPresentation._matrix_mobject(snapshot.reduction_source, scale=0.68)
        identity = ElementaryMatricesPresentation._matrix_mobject(snapshot.identity, scale=0.68)
        arrow = MathTex(r"\xrightarrow{\ E_4E_3E_2E_1\ }", font_size=36, color=YELLOW)
        row = VGroup(source, arrow, identity).arrange(RIGHT, buff=0.50)
        labels = VGroup(MathTex("A_0", font_size=29), MathTex("I", font_size=29, color=GREEN))
        labels[0].next_to(source, UP, buff=0.12)
        labels[1].next_to(identity, UP, buff=0.12)
        operations = VGroup(
            *[
                MathTex(rf"E_{step.index}:\ {step.operation_tex}", font_size=28)
                for step in snapshot.reduction_steps
            ]
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        group = VGroup(VGroup(row, labels), operations).arrange(DOWN, buff=0.38)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _reduction_step_panel(step: RowReductionStep):
        left = ElementaryMatricesPresentation._matrix_mobject(step.elementary_matrix, scale=0.56)
        middle = ElementaryMatricesPresentation._matrix_mobject(step.source_matrix, scale=0.56)
        result = ElementaryMatricesPresentation._matrix_mobject(step.product_matrix, scale=0.56)
        row = VGroup(left, MathTex(r"\cdot", font_size=38), middle, MathTex("=", font_size=38), result).arrange(RIGHT, buff=0.24)
        labels = VGroup(
            MathTex(rf"E_{step.index}", font_size=27, color=BLUE),
            MathTex(rf"A_{step.index-1}", font_size=27),
            MathTex(rf"A_{step.index}", font_size=27, color=GREEN),
        )
        for label, matrix in zip(labels, (left, middle, result), strict=True):
            label.next_to(matrix, UP, buff=0.11)
        operation = MathTex(step.operation_tex, font_size=34, color=YELLOW)
        group = VGroup(VGroup(row, labels), operation).arrange(DOWN, buff=0.34)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        panel = VGroup(box, group)
        return panel, result

    @staticmethod
    def _cumulative_products_panel(snapshot):
        cards = VGroup()
        for index, product in enumerate(snapshot.cumulative_products, start=1):
            label_tex = "E_1" if index == 1 else rf"E_{index}\cdots E_1"
            label = MathTex(rf"P_{index}={label_tex}", font_size=25, color=YELLOW)
            matrix = ElementaryMatricesPresentation._matrix_mobject(product, scale=0.40)
            card_group = VGroup(label, matrix).arrange(DOWN, buff=0.18)
            card_box = SurroundingRectangle(card_group, color=BLUE if index < 4 else GREEN, buff=0.16)
            cards.add(VGroup(card_box, card_group))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.58, 0.38))
        chain = MathTex(r"P_4=E_4E_3E_2E_1", font_size=36, color=GREEN)
        group = VGroup(cards, chain).arrange(DOWN, buff=0.30)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _reduction_matrix_panel(snapshot):
        p_matrix = ElementaryMatricesPresentation._matrix_mobject(snapshot.reduction_matrix, scale=0.56)
        a_matrix = ElementaryMatricesPresentation._matrix_mobject(snapshot.reduction_source, scale=0.58)
        identity = ElementaryMatricesPresentation._matrix_mobject(snapshot.identity, scale=0.58)
        row = VGroup(p_matrix, MathTex(r"\cdot", font_size=38), a_matrix, MathTex("=", font_size=38), identity).arrange(RIGHT, buff=0.25)
        labels = VGroup(
            MathTex(r"P=E_4E_3E_2E_1", font_size=26, color=BLUE),
            MathTex("A", font_size=27),
            MathTex("I", font_size=27, color=GREEN),
        )
        for label, matrix in zip(labels, (p_matrix, a_matrix, identity), strict=True):
            label.next_to(matrix, UP, buff=0.12)
        conclusion = MathTex(r"PA=I\quad\Longrightarrow\quad P=A^{-1}", font_size=39, color=YELLOW)
        group = VGroup(VGroup(row, labels), conclusion).arrange(DOWN, buff=0.42)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        return VGroup(box, group)

    @staticmethod
    def _reverse_overview_panel():
        forward = MathTex(r"E_4E_3E_2E_1A=I", font_size=42, color=GREEN)
        reverse = MathTex(r"A=E_1^{-1}E_2^{-1}E_3^{-1}E_4^{-1}I", font_size=40, color=YELLOW)
        instruction = Text(
            "To rebuild A from I, apply the inverse operations in reverse chronological order.",
            font_size=ElementaryMatricesPresentation.EXPLANATION_FONT_SIZE,
        )
        ElementaryMatricesPresentation._shrink_to_fit_width(instruction, 11.0)
        order = MathTex(r"E_4^{-1}\ \to\ E_3^{-1}\ \to\ E_2^{-1}\ \to\ E_1^{-1}", font_size=35, color=BLUE)
        group = VGroup(forward, reverse, instruction, order).arrange(DOWN, buff=0.36)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _reverse_step_heading(reverse_position: int, original_index: int):
        prose = Text(f"Reverse step {reverse_position}: apply", font_size=29)
        symbol = MathTex(rf"E_{{{original_index}}}^{{-1}}", font_size=31, color=RED)
        return VGroup(prose, symbol).arrange(RIGHT, buff=0.12).move_to(
            UP * ElementaryMatricesPresentation.HEADING_Y
        )

    @staticmethod
    def _reverse_step_panel(step: RowReductionStep):
        left = ElementaryMatricesPresentation._matrix_mobject(step.elementary_matrix, scale=0.56)
        middle = ElementaryMatricesPresentation._matrix_mobject(step.source_matrix, scale=0.56)
        result = ElementaryMatricesPresentation._matrix_mobject(step.product_matrix, scale=0.56)
        row = VGroup(left, MathTex(r"\cdot", font_size=38), middle, MathTex("=", font_size=38), result).arrange(RIGHT, buff=0.24)
        labels = VGroup(
            MathTex(rf"E_{step.index}^{{-1}}", font_size=27, color=RED),
            MathTex(rf"A_{step.index}", font_size=27),
            MathTex(rf"A_{step.index-1}", font_size=27, color=GREEN),
        )
        for label, matrix in zip(labels, (left, middle, result), strict=True):
            label.next_to(matrix, UP, buff=0.11)
        operation = MathTex(step.operation_tex, font_size=34, color=YELLOW)
        group = VGroup(VGroup(row, labels), operation).arrange(DOWN, buff=0.34)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.18)
        panel = VGroup(box, group)
        return panel, result

    @staticmethod
    def _factorization_panel(snapshot):
        forward = MathTex(r"A^{-1}=E_4E_3E_2E_1", font_size=44, color=GREEN)
        reverse = MathTex(r"A=E_1^{-1}E_2^{-1}E_3^{-1}E_4^{-1}", font_size=42, color=YELLOW)
        numeric = ElementaryMatricesPresentation._matrix_mobject(snapshot.reduction_matrix, scale=0.56)
        numeric_label = MathTex(r"A^{-1}=", font_size=34, color=BLUE)
        numeric_row = VGroup(numeric_label, numeric).arrange(RIGHT, buff=0.28)
        note = Text(
            "The inverse of a product reverses the order of the factors.",
            font_size=ElementaryMatricesPresentation.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(forward, reverse, numeric_row, note).arrange(DOWN, buff=0.34)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _summary_panel():
        statements = VGroup(
            MathTex(r"EA=\text{one row operation on }A", font_size=36, color=BLUE),
            MathTex(r"E^{-1}(EA)=A", font_size=39, color=YELLOW),
            MathTex(r"E_k\cdots E_2E_1A=R", font_size=39, color=GREEN),
            MathTex(r"A=E_1^{-1}E_2^{-1}\cdots E_k^{-1}R", font_size=37),
        ).arrange(DOWN, buff=0.34)
        conclusion = Text(
            "A complete row reduction is one matrix multiplication built from elementary matrices.",
            font_size=ElementaryMatricesPresentation.EXPLANATION_FONT_SIZE,
        )
        ElementaryMatricesPresentation._shrink_to_fit_width(conclusion, 11.0)
        group = VGroup(statements, conclusion).arrange(DOWN, buff=0.42)
        box = SurroundingRectangle(group, color=YELLOW, buff=0.20)
        return VGroup(box, group)

    @staticmethod
    def _shrink_to_fit_width(mobject, max_width: float):
        """Shrink oversized text without enlarging short explanatory text."""
        if mobject.width > max_width:
            mobject.scale_to_fit_width(max_width)
        return mobject

    @staticmethod
    def _matrix_mobject(matrix, *, scale: float):
        """Create a compact matrix with extra row spacing for fractional entries."""
        formatted = ElementaryMatricesPresentation._format_matrix(matrix)
        has_fraction = any(r"\tfrac" in entry for row in formatted for entry in row)
        v_buff = 1.25 if has_fraction else 0.80
        return Matrix(formatted, h_buff=0.95, v_buff=v_buff).scale(scale)

    @staticmethod
    def _format_matrix(matrix):
        return [[ElementaryMatricesPresentation._format_number(value) for value in row] for row in matrix]

    @staticmethod
    def _format_number(value: float) -> str:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) < 1e-9:
            return str(rounded)
        fraction = Fraction(float(value)).limit_denominator(12)
        if abs(float(fraction) - float(value)) < 1e-9:
            sign = "-" if fraction.numerator < 0 else ""
            numerator = abs(fraction.numerator)
            return rf"{sign}\tfrac{{{numerator}}}{{{fraction.denominator}}}"
        return f"{float(value):g}"
