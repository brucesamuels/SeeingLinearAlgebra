"""CP125 presentation: rectangular matrices and the geometry of Ax = b."""

from __future__ import annotations

from manim import (
    Arrow,
    BLUE,
    Circle,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    Line,
    MathTex,
    ORIGIN,
    Polygon,
    RED,
    Rectangle,
    RIGHT,
    Scene,
    Square,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from engine.rectangular_matrices import RectangularMatrices, RectangularShapeCase


class RectangularMatricesPresentation(Scene):
    """Connect matrix shape, rank, column space, and solution geometry."""

    TRANSITION = 2.20
    HIGHLIGHT = 1.35
    READ = 2.65
    HEADING_Y = 2.24
    EXPLANATION_FONT_SIZE = 21

    def construct(self) -> None:
        snapshot = RectangularMatrices().snapshot()

        title = Text("Rectangular Matrices and Ax = b", font_size=42).to_edge(UP, buff=0.27)
        subtitle = Text(
            "Rows count equations, columns count unknowns, and rank counts what can be reached.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.13)
        self._fit_down_only(subtitle, 11.4)
        self.play(Write(title), FadeIn(subtitle), run_time=2.4)

        heading = self._heading("The dimensions must match", 31)
        panel = self._dimension_panel(snapshot).move_to(DOWN * 0.52)
        self.play(FadeIn(heading), FadeIn(panel), run_time=self.TRANSITION)
        self.wait(self.READ)

        shape_heading = self._heading("The shape of A changes the geometry", 31)
        shape_panel = self._shape_cards(snapshot.cases).move_to(DOWN * 0.54)
        self.play(
            FadeOut(heading),
            FadeOut(panel),
            FadeIn(shape_heading),
            FadeIn(shape_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        column_heading = self._heading("Solving means reaching b with a column combination", 29)
        column_panel, reachable_dot, unreachable_dot = self._column_space_panel(snapshot)
        column_panel.move_to(DOWN * 0.58)
        self.play(
            FadeOut(shape_heading),
            FadeOut(shape_panel),
            FadeIn(column_heading),
            FadeIn(column_panel),
            run_time=self.TRANSITION,
        )
        reachable_box = SurroundingRectangle(reachable_dot, color=GREEN, buff=0.10)
        unreachable_box = SurroundingRectangle(unreachable_dot, color=RED, buff=0.10)
        self.play(Create(reachable_box), run_time=self.HIGHLIGHT)
        self.play(Create(unreachable_box), run_time=self.HIGHLIGHT)
        self.wait(self.READ)

        rank_heading = self._heading("Rank measures the dimension of the reachable set", 29)
        rank_panel = self._rank_panel(snapshot).move_to(DOWN * 0.54)
        self.play(
            FadeOut(column_heading),
            FadeOut(column_panel),
            FadeOut(reachable_box),
            FadeOut(unreachable_box),
            FadeIn(rank_heading),
            FadeIn(rank_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        tall_heading = self._heading("Tall matrices: fewer input directions than output directions", 27)
        tall_panel, tall_inside, tall_outside = self._tall_geometry_panel(snapshot.cases[1])
        tall_panel.move_to(DOWN * 0.55)
        self.play(
            FadeOut(rank_heading),
            FadeOut(rank_panel),
            FadeIn(tall_heading),
            FadeIn(tall_panel),
            run_time=self.TRANSITION,
        )
        tall_inside_box = SurroundingRectangle(tall_inside, color=GREEN, buff=0.09)
        tall_outside_box = SurroundingRectangle(tall_outside, color=RED, buff=0.09)
        self.play(Create(tall_inside_box), run_time=self.HIGHLIGHT)
        self.play(Create(tall_outside_box), run_time=self.HIGHLIGHT)
        self.wait(self.READ)

        wide_heading = self._heading("Wide matrices: extra input directions create a null space", 28)
        wide_panel, input_points, output_dot = self._wide_geometry_panel(snapshot.cases[2])
        wide_panel.move_to(DOWN * 0.55)
        self.play(
            FadeOut(tall_heading),
            FadeOut(tall_panel),
            FadeOut(tall_inside_box),
            FadeOut(tall_outside_box),
            FadeIn(wide_heading),
            FadeIn(wide_panel),
            run_time=self.TRANSITION,
        )
        input_boxes = VGroup()
        for point in input_points:
            point_box = SurroundingRectangle(point, color=YELLOW, buff=0.07)
            input_boxes.add(point_box)
            self.play(Create(point_box), run_time=0.55)
        output_box = SurroundingRectangle(output_dot, color=GREEN, buff=0.09)
        self.play(Create(output_box), run_time=self.HIGHLIGHT)
        self.wait(self.READ)

        square_heading = self._heading("Square full-rank matrices can be both onto and one-to-one", 27)
        square_panel = self._square_geometry_panel(snapshot.cases[0]).move_to(DOWN * 0.55)
        self.play(
            FadeOut(wide_heading),
            FadeOut(wide_panel),
            FadeOut(input_boxes),
            FadeOut(output_box),
            FadeIn(square_heading),
            FadeIn(square_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        warning_heading = self._heading("Shape alone does not decide consistency", 30)
        warning_panel = self._shape_warning_panel(snapshot).move_to(DOWN * 0.54)
        self.play(
            FadeOut(square_heading),
            FadeOut(square_panel),
            FadeIn(warning_heading),
            FadeIn(warning_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ + 0.3)

        summary_heading = self._heading("Full-rank possibilities for each matrix shape", 29)
        summary_panel = self._summary_panel(snapshot.cases).move_to(DOWN * 0.56)
        self.play(
            FadeOut(warning_heading),
            FadeOut(warning_panel),
            FadeIn(summary_heading),
            FadeIn(summary_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ + 0.4)

        closing = Text(
            "Next: test overdetermined and underdetermined systems with concrete row reductions.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.28)
        self._fit_down_only(closing, 11.3)
        self.play(FadeIn(closing), run_time=self.TRANSITION)
        self.wait(2.2)

    def _dimension_panel(self, snapshot):
        equation = MathTex(snapshot.dimension_equation_tex, font_size=43, color=YELLOW)
        map_formula = MathTex(snapshot.map_tex, font_size=39)
        count_formula = MathTex(snapshot.equation_count_tex, font_size=29)
        note = Text(
            "The input vector has one coordinate for each column; the output has one coordinate for each row.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(note, 10.8)
        group = VGroup(equation, map_formula, count_formula, note).arrange(DOWN, buff=0.34)
        return self._boxed(group, buff=0.27)

    def _shape_cards(self, cases: tuple[RectangularShapeCase, ...]):
        cards = VGroup()
        for case in cases:
            title = Text(case.name, font_size=27, color=YELLOW)
            matrix_shape = self._matrix_shape(case.rows, case.columns)
            relation = MathTex(case.relation_tex, font_size=31)
            map_formula = MathTex(case.map_tex, font_size=27, color=BLUE)
            if case.name == "Tall":
                descriptor = Text("overdetermined", font_size=19, color=GREEN)
            elif case.name == "Wide":
                descriptor = Text("underdetermined", font_size=19, color=GREEN)
            else:
                descriptor = Text("same number", font_size=19, color=GREEN)
            content = VGroup(title, matrix_shape, relation, map_formula, descriptor).arrange(DOWN, buff=0.16)
            card = self._boxed(content, buff=0.20)
            cards.add(card)
        cards.arrange(RIGHT, buff=0.34)
        self._fit_down_only(cards, 11.4)
        return cards

    def _column_space_panel(self, snapshot):
        formula = MathTex(snapshot.column_combination_tex, font_size=36, color=YELLOW)
        consistency = MathTex(snapshot.consistency_tex, font_size=34)

        output_box = Rectangle(width=5.0, height=2.25, color=BLUE)
        output_label = MathTex(r"\mathbb{R}^m", font_size=28).next_to(output_box, UP, buff=0.10)
        image = Polygon(
            [-1.85, -0.55, 0],
            [0.95, -0.78, 0],
            [1.85, 0.55, 0],
            [-0.95, 0.78, 0],
            color=GREEN,
            fill_opacity=0.18,
        ).move_to(output_box)
        image_label = MathTex(r"\operatorname{Col}(A)", font_size=25, color=GREEN).move_to(image.get_center())
        reachable_dot = Circle(radius=0.09, color=GREEN, fill_opacity=1).move_to(image.get_center() + RIGHT * 0.86 + UP * 0.20)
        reachable_label = MathTex(r"\mathbf{b}_{\mathrm{in}}", font_size=24, color=GREEN).next_to(reachable_dot, RIGHT, buff=0.10)
        unreachable_dot = Circle(radius=0.09, color=RED, fill_opacity=1).move_to(output_box.get_center() + RIGHT * 1.65 + DOWN * 0.72)
        unreachable_label = MathTex(r"\mathbf{b}_{\mathrm{out}}", font_size=24, color=RED).next_to(unreachable_dot, LEFT, buff=0.10)
        diagram = VGroup(
            output_box,
            output_label,
            image,
            image_label,
            reachable_dot,
            reachable_label,
            unreachable_dot,
            unreachable_label,
        )
        group = VGroup(formula, diagram, consistency).arrange(DOWN, buff=0.26)
        return self._boxed(group, buff=0.24), reachable_dot, unreachable_dot

    def _rank_panel(self, snapshot):
        rank = MathTex(snapshot.rank_bound_tex, font_size=40, color=YELLOW)
        col_dimension = MathTex(r"\dim\operatorname{Col}(A)=r", font_size=35, color=GREEN)
        nullity = MathTex(snapshot.nullity_tex, font_size=35, color=BLUE)
        reach_text = Text(
            "Rank counts independent output directions; nullity counts input directions that collapse to zero.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(reach_text, 10.9)
        bars = VGroup(
            self._dimension_bar("input directions", "n", BLUE, 4.2),
            self._dimension_bar("reachable directions", "r", GREEN, 3.0),
            self._dimension_bar("null directions", "n-r", YELLOW, 1.8),
        ).arrange(DOWN, buff=0.18)
        group = VGroup(rank, VGroup(col_dimension, nullity).arrange(RIGHT, buff=0.65), bars, reach_text).arrange(DOWN, buff=0.29)
        return self._boxed(group, buff=0.24)

    def _tall_geometry_panel(self, case: RectangularShapeCase):
        left = self._space_box(r"\mathbb{R}^2", 3.0, 2.15)
        right = self._space_box(r"\mathbb{R}^3", 4.35, 2.65)
        left.move_to(LEFT * 3.55 + DOWN * 0.08)
        right.move_to(RIGHT * 3.15 + DOWN * 0.08)
        arrow = self._map_arrow(left[0], right[0])

        image = Polygon(
            [-1.45, -0.44, 0],
            [0.72, -0.68, 0],
            [1.46, 0.42, 0],
            [-0.70, 0.69, 0],
            color=GREEN,
            fill_opacity=0.18,
        ).move_to(right[0])
        image_label = MathTex(r"\operatorname{Col}(A)", font_size=24, color=GREEN).move_to(image)
        inside = Circle(radius=0.09, color=GREEN, fill_opacity=1).move_to(image.get_center() + RIGHT * 0.68)
        inside_label = Text("reachable", font_size=17, color=GREEN).next_to(inside, UP, buff=0.08)
        outside = Circle(radius=0.09, color=RED, fill_opacity=1).move_to(right[0].get_center() + RIGHT * 1.55 + UP * 0.75)
        outside_label = Text("not reachable", font_size=17, color=RED).next_to(outside, DOWN, buff=0.08)

        formulas = VGroup(
            MathTex(case.rank_bound_tex, font_size=30, color=YELLOW),
            Text(case.geometry_summary, font_size=self.EXPLANATION_FONT_SIZE),
            Text("At full column rank: a reachable b has at most one solution.", font_size=self.EXPLANATION_FONT_SIZE),
        ).arrange(DOWN, buff=0.13)
        self._fit_down_only(formulas, 10.9)
        diagram = VGroup(left, right, arrow, image, image_label, inside, inside_label, outside, outside_label)
        group = VGroup(diagram, formulas).arrange(DOWN, buff=0.30)
        return self._boxed(group, buff=0.21), inside, outside

    def _wide_geometry_panel(self, case: RectangularShapeCase):
        left = self._space_box(r"\mathbb{R}^3", 4.35, 2.65)
        right = self._space_box(r"\mathbb{R}^2", 3.0, 2.15)
        left.move_to(LEFT * 3.15 + DOWN * 0.08)
        right.move_to(RIGHT * 3.55 + DOWN * 0.08)
        arrow = self._map_arrow(left[0], right[0])

        null_line = Line(LEFT * 1.35, RIGHT * 1.35, color=YELLOW).rotate(0.35).move_to(left[0])
        null_label = MathTex(r"\mathbf{x}_p+N(A)", font_size=24, color=YELLOW).next_to(null_line, UP, buff=0.10)
        input_points = VGroup()
        for shift in (-0.72, 0.0, 0.72):
            input_points.add(Circle(radius=0.085, color=YELLOW, fill_opacity=1).move_to(null_line.get_center() + null_line.get_unit_vector() * shift))
        output_dot = Circle(radius=0.10, color=GREEN, fill_opacity=1).move_to(right[0])
        output_label = MathTex(r"\mathbf{b}", font_size=25, color=GREEN).next_to(output_dot, RIGHT, buff=0.10)
        arrows_note = Text("all three inputs map to the same output", font_size=17, color=GREEN).next_to(right[0], DOWN, buff=0.14)

        formulas = VGroup(
            MathTex(case.rank_bound_tex + r",\qquad \dim N(A)\ge1", font_size=30, color=YELLOW),
            Text(case.geometry_summary, font_size=self.EXPLANATION_FONT_SIZE),
            Text("At full row rank: every b is reachable, but never uniquely.", font_size=self.EXPLANATION_FONT_SIZE),
        ).arrange(DOWN, buff=0.13)
        self._fit_down_only(formulas, 10.9)
        diagram = VGroup(left, right, arrow, null_line, null_label, input_points, output_dot, output_label, arrows_note)
        group = VGroup(diagram, formulas).arrange(DOWN, buff=0.30)
        return self._boxed(group, buff=0.21), input_points, output_dot

    def _square_geometry_panel(self, case: RectangularShapeCase):
        left = self._space_box(r"\mathbb{R}^2", 3.35, 2.35)
        right = self._space_box(r"\mathbb{R}^2", 3.35, 2.35)
        left.move_to(LEFT * 3.15)
        right.move_to(RIGHT * 3.15)
        arrow = self._map_arrow(left[0], right[0])

        x_dot = Circle(radius=0.10, color=YELLOW, fill_opacity=1).move_to(left[0].get_center() + LEFT * 0.55 + DOWN * 0.25)
        x_label = MathTex(r"\mathbf{x}", font_size=25, color=YELLOW).next_to(x_dot, LEFT, buff=0.10)
        b_dot = Circle(radius=0.10, color=GREEN, fill_opacity=1).move_to(right[0].get_center() + RIGHT * 0.55 + UP * 0.28)
        b_label = MathTex(r"\mathbf{b}", font_size=25, color=GREEN).next_to(b_dot, RIGHT, buff=0.10)
        full_output = Rectangle(width=3.05, height=2.05, color=GREEN, fill_opacity=0.10).move_to(right[0])
        formulas = VGroup(
            MathTex(r"r=m=n=2", font_size=32, color=YELLOW),
            Text(case.geometry_summary, font_size=self.EXPLANATION_FONT_SIZE),
            MathTex(
                r"\text{For every }\mathbf{b},\ \text{there is exactly one }\mathbf{x}"
                r"\text{ such that }A\mathbf{x}=\mathbf{b}",
                font_size=28,
            ),
        ).arrange(DOWN, buff=0.14)
        diagram = VGroup(left, right, arrow, full_output, x_dot, x_label, b_dot, b_label)
        group = VGroup(diagram, formulas).arrange(DOWN, buff=0.31)
        return self._boxed(group, buff=0.21)

    def _shape_warning_panel(self, snapshot):
        tall_title = Text("Overdetermined", font_size=26, color=YELLOW)
        tall_formula = MathTex(r"m>n", font_size=31)
        tall_text = Text(
            "More equations do not automatically mean inconsistency.\nA compatible b may still have one solution.",
            font_size=self.EXPLANATION_FONT_SIZE,
            line_spacing=1.05,
        )
        tall = self._boxed(VGroup(tall_title, tall_formula, tall_text).arrange(DOWN, buff=0.18), buff=0.22)

        wide_title = Text("Underdetermined", font_size=26, color=YELLOW)
        wide_formula = MathTex(r"m<n", font_size=31)
        wide_text = Text(
            "More unknowns do not automatically mean consistency.\nIf solvable, free variables make solutions nonunique.",
            font_size=self.EXPLANATION_FONT_SIZE,
            line_spacing=1.05,
        )
        wide = self._boxed(VGroup(wide_title, wide_formula, wide_text).arrange(DOWN, buff=0.18), buff=0.22)
        cards = VGroup(tall, wide).arrange(RIGHT, buff=0.42)
        self._fit_down_only(cards, 11.3)

        exact_test = VGroup(
            Text("The exact consistency test is", font_size=self.EXPLANATION_FONT_SIZE),
            MathTex(snapshot.augmented_rank_tex, font_size=34, color=GREEN),
        ).arrange(DOWN, buff=0.15)
        group = VGroup(cards, exact_test).arrange(DOWN, buff=0.34)
        return self._boxed(group, buff=0.22)

    def _summary_panel(self, cases: tuple[RectangularShapeCase, ...]):
        x_positions = (-4.55, -1.65, 1.70, 4.20)
        headers = VGroup(
            Text("shape", font_size=21, color=YELLOW).move_to([x_positions[0], 1.05, 0]),
            Text("full-rank map", font_size=21, color=YELLOW).move_to([x_positions[1], 1.05, 0]),
            Text("every b?", font_size=21, color=YELLOW).move_to([x_positions[2], 1.05, 0]),
            Text("unique when solvable?", font_size=20, color=YELLOW).move_to([x_positions[3], 1.05, 0]),
        )

        summaries = {
            "Square": ("onto and one-to-one", "yes", "yes"),
            "Tall": ("one-to-one, not onto", "no", "yes"),
            "Wide": ("onto, not one-to-one", "yes", "no"),
        }
        rows = VGroup()
        for row_index, case in enumerate(cases):
            map_summary, every_b, unique = summaries[case.name]
            y = 0.42 - 0.62 * row_index
            row = VGroup(
                Text(case.name, font_size=21).move_to([x_positions[0], y, 0]),
                Text(map_summary, font_size=20).move_to([x_positions[1], y, 0]),
                Text(every_b, font_size=21, color=GREEN if every_b == "yes" else RED).move_to([x_positions[2], y, 0]),
                Text(unique, font_size=21, color=GREEN if unique == "yes" else RED).move_to([x_positions[3], y, 0]),
            )
            rows.add(row)
        separator = Line(LEFT * 5.25, RIGHT * 5.25, color=BLUE).move_to(UP * 0.76)
        table = VGroup(headers, separator, rows)

        rule = MathTex(
            r"A\mathbf{x}=\mathbf{b}\text{ is consistent}\iff\mathbf{b}\in\operatorname{Col}(A)",
            font_size=34,
            color=YELLOW,
        )
        caution = Text(
            "These are full-rank possibilities; a rank-deficient matrix reaches less and has a larger null space.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        self._fit_down_only(caution, 10.8)
        group = VGroup(table, rule, caution).arrange(DOWN, buff=0.28)
        self._fit_down_only(group, 11.3)
        return self._boxed(group, buff=0.23)

    def _heading(self, text: str, font_size: int):
        heading = Text(text, font_size=font_size, color=YELLOW)
        self._fit_down_only(heading, 11.4)
        heading.move_to(UP * self.HEADING_Y)
        return heading

    def _matrix_shape(self, rows: int, columns: int):
        cells = VGroup()
        size = 0.28
        for row in range(rows):
            for column in range(columns):
                cell = Square(side_length=size, color=BLUE, fill_opacity=0.18)
                cell.move_to(RIGHT * column * size + DOWN * row * size)
                cells.add(cell)
        cells.move_to([0, 0, 0])
        left_bracket = VGroup(
            Line(UP * (cells.height / 2 + 0.08), DOWN * (cells.height / 2 + 0.08)),
            Line(LEFT * 0.10, RIGHT * 0.02),
            Line(LEFT * 0.10, RIGHT * 0.02),
        )
        left_bracket[0].move_to(cells.get_left() + LEFT * 0.12)
        left_bracket[1].next_to(left_bracket[0].get_top(), RIGHT, buff=0).shift(DOWN * 0.01)
        left_bracket[2].next_to(left_bracket[0].get_bottom(), RIGHT, buff=0).shift(UP * 0.01)
        right_bracket = left_bracket.copy().rotate(3.141592653589793).move_to(cells.get_right() + RIGHT * 0.12)
        return VGroup(cells, left_bracket, right_bracket)

    def _space_box(self, label_tex: str, width: float, height: float):
        box = Rectangle(width=width, height=height, color=BLUE)
        label = MathTex(label_tex, font_size=27).next_to(box, UP, buff=0.09)
        return VGroup(box, label)

    def _map_arrow(self, left_box, right_box):
        start = left_box.get_right() + RIGHT * 0.22
        end = right_box.get_left() + LEFT * 0.22
        arrow = Arrow(
            start=start,
            end=end,
            buff=0,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.14,
        )
        map_label = MathTex(r"A", font_size=25, color=YELLOW).next_to(arrow, UP, buff=0.08)
        action_label = MathTex(
            r"\mathbf{x}\mapsto\mathbf{b}",
            font_size=22,
            color=YELLOW,
        ).next_to(arrow, DOWN, buff=0.08)
        return VGroup(arrow, map_label, action_label)

    def _dimension_bar(self, label: str, symbol: str, color, width: float):
        bar = Rectangle(width=width, height=0.34, color=color, fill_opacity=0.20)
        label_text = Text(label, font_size=18).next_to(bar, LEFT, buff=0.18)
        symbol_tex = MathTex(symbol, font_size=24, color=color).move_to(bar)
        return VGroup(label_text, bar, symbol_tex)

    def _boxed(self, content, *, buff: float = 0.24):
        box = SurroundingRectangle(content, color=BLUE, buff=buff)
        return VGroup(box, content)

    @staticmethod
    def _fit_down_only(mobject, max_width: float):
        if mobject.width > max_width:
            mobject.scale_to_fit_width(max_width)
        return mobject
