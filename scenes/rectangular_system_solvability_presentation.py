"""CP126 presentation: solvability of over- and underdetermined systems."""

from __future__ import annotations

from manim import (
    Arrow,
    BLUE,
    Circle,
    DOWN,
    DL,
    DR,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    Line,
    MathTex,
    Polygon,
    RED,
    Rectangle,
    RIGHT,
    Scene,
    SurroundingRectangle,
    Text,
    UP,
    UL,
    UR,
    VGroup,
    Write,
    YELLOW,
)

from engine.rectangular_system_solvability import RectangularSystemSolvability


class RectangularSystemSolvabilityPresentation(Scene):
    """Use rank and column-space membership to classify rectangular systems."""

    TRANSITION = 2.20
    HIGHLIGHT = 1.35
    READ = 2.75
    HEADING_Y = 2.25
    EXPLANATION_FONT_SIZE = 21

    def construct(self) -> None:
        snapshot = RectangularSystemSolvability.snapshot()

        title = Text(
            "Overdetermined and Underdetermined Systems",
            font_size=40,
        ).to_edge(UP, buff=0.27)
        subtitle = Text(
            "Shape limits the possibilities; rank and the right-hand side decide solvability.",
            font_size=23,
        ).next_to(title, DOWN, buff=0.13)
        self._fit_down_only(subtitle, 11.4)
        self.play(Write(title), FadeIn(subtitle), run_time=2.4)

        heading = self._heading("One criterion governs every matrix shape", 31)
        panel = self._common_panel(snapshot).move_to(DOWN * 0.52)
        self.play(FadeIn(heading), FadeIn(panel), run_time=self.TRANSITION)
        self.wait(self.READ)

        over_geometry_heading = self._heading(
            "Overdetermined: the columns reach only part of the output space",
            26,
        )
        over_geometry_heading.move_to(UP * 2.36)
        over_geometry_panel = self._over_geometry_panel(snapshot.overdetermined).move_to(DOWN * 0.64)
        self.play(
            FadeOut(heading),
            FadeOut(panel),
            FadeIn(over_geometry_heading),
            FadeIn(over_geometry_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        compatible_heading = self._heading("A compatible right-hand side gives one solution", 29)
        compatible_panel = self._over_compatible_panel(snapshot.overdetermined).move_to(DOWN * 0.54)
        self.play(
            FadeOut(over_geometry_heading),
            FadeOut(over_geometry_panel),
            FadeIn(compatible_heading),
            FadeIn(compatible_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        incompatible_heading = self._heading("An incompatible right-hand side creates a contradiction", 28)
        incompatible_panel = self._over_incompatible_panel(snapshot.overdetermined).move_to(DOWN * 0.54)
        self.play(
            FadeOut(compatible_heading),
            FadeOut(compatible_panel),
            FadeIn(incompatible_heading),
            FadeIn(incompatible_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        over_rule_heading = self._heading("Full column rank gives at most one solution", 29)
        over_rule_panel = self._over_rule_panel(snapshot.overdetermined).move_to(DOWN * 0.53)
        self.play(
            FadeOut(incompatible_heading),
            FadeOut(incompatible_panel),
            FadeIn(over_rule_heading),
            FadeIn(over_rule_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        under_example_heading = self._heading("Underdetermined: a free variable remains", 30)
        under_example_panel = self._under_example_panel(snapshot.underdetermined).move_to(DOWN * 0.53)
        self.play(
            FadeOut(over_rule_heading),
            FadeOut(over_rule_panel),
            FadeIn(under_example_heading),
            FadeIn(under_example_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        under_solution_heading = self._heading("One particular solution plus the null space", 29)
        under_solution_panel = self._under_solution_panel(snapshot.underdetermined).move_to(DOWN * 0.54)
        self.play(
            FadeOut(under_example_heading),
            FadeOut(under_example_panel),
            FadeIn(under_solution_heading),
            FadeIn(under_solution_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        under_rule_heading = self._heading("Every consistent underdetermined system is nonunique", 28)
        under_rule_panel = self._under_rule_panel(snapshot.underdetermined).move_to(DOWN * 0.53)
        self.play(
            FadeOut(under_solution_heading),
            FadeOut(under_solution_panel),
            FadeIn(under_rule_heading),
            FadeIn(under_rule_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        counterexample_heading = self._heading("Wide does not automatically mean consistent", 29)
        counterexample_panel = self._wide_counterexample_panel(snapshot.underdetermined).move_to(DOWN * 0.53)
        self.play(
            FadeOut(under_rule_heading),
            FadeOut(under_rule_panel),
            FadeIn(counterexample_heading),
            FadeIn(counterexample_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ)

        summary_heading = self._heading("The solvability conditions", 31)
        summary_panel = self._summary_panel(snapshot).move_to(DOWN * 0.54)
        self.play(
            FadeOut(counterexample_heading),
            FadeOut(counterexample_panel),
            FadeIn(summary_heading),
            FadeIn(summary_panel),
            run_time=self.TRANSITION,
        )
        self.wait(self.READ + 0.5)

        closing = Text(
            "Inconsistent overdetermined systems will later motivate least-squares approximation.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.28)
        self._fit_down_only(closing, 11.3)
        self.play(FadeIn(closing), run_time=self.TRANSITION)
        self.wait(2.2)

    def _common_panel(self, snapshot):
        shape = MathTex(r"A\in\mathbb{R}^{m\times n},\qquad\mathbf{b}\in\mathbb{R}^m", font_size=38)
        column_rule = MathTex(snapshot.common_consistency_tex, font_size=36, color=YELLOW)
        rank_rule = MathTex(snapshot.augmented_rank_tex, font_size=35, color=GREEN)
        dimension_rule = MathTex(snapshot.solution_count_tex, font_size=30)
        note = Text(
            "Column-space membership decides existence; nullity decides uniqueness.",
            font_size=self.EXPLANATION_FONT_SIZE,
        )
        group = VGroup(shape, column_rule, rank_rule, dimension_rule, note).arrange(DOWN, buff=0.28)
        self._fit_down_only(group, 11.0)
        return self._boxed(group, buff=0.26)

    def _over_geometry_panel(self, over):
        left = self._space_box(r"\mathbb{R}^2", 3.05, 2.20)
        right = self._space_box_3d(r"\mathbb{R}^3", 4.55, 2.55)
        left.move_to(LEFT * 3.55 + UP * 0.10)
        right.move_to(RIGHT * 3.15 + UP * 0.10)
        arrow = self._map_arrow(left[0], right[0])

        input_origin = left[0].get_center() + LEFT * 0.55 + DOWN * 0.36
        input_axes = VGroup(
            Line(
                input_origin + LEFT * 0.58,
                input_origin + RIGHT * 1.36,
                color=GREEN,
                stroke_width=2.5,
            ),
            Line(
                input_origin + DOWN * 0.46,
                input_origin + UP * 1.10,
                color=GREEN,
                stroke_width=2.5,
            ),
        )
        input_vector = Arrow(
            input_origin,
            input_origin + RIGHT * 0.92 + UP * 0.62,
            buff=0,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18,
        )
        input_label = MathTex(r"\mathbf{x}", font_size=24, color=YELLOW).next_to(
            input_vector.get_end(), UP, buff=0.05
        )

        image = Polygon(
            [-1.78, -0.48, 0],
            [0.95, -0.75, 0],
            [1.78, 0.48, 0],
            [-0.95, 0.75, 0],
            color=GREEN,
            fill_opacity=0.18,
        ).move_to(right[0])
        image_label = MathTex(r"\operatorname{Col}(A)", font_size=24, color=GREEN).move_to(image)
        inside = Circle(radius=0.095, color=GREEN, fill_opacity=1).move_to(image.get_center() + LEFT * 0.65 + UP * 0.16)
        outside = Circle(radius=0.095, color=RED, fill_opacity=1).move_to(right[0].get_center() + RIGHT * 1.65 + DOWN * 0.74)
        inside_label = MathTex(r"\mathbf{b}_{\rm good}", font_size=23, color=GREEN).next_to(inside, UP, buff=0.09)
        outside_label = MathTex(r"\mathbf{b}_{\rm bad}", font_size=23, color=RED).next_to(outside, LEFT, buff=0.09)
        inside_box = SurroundingRectangle(inside, color=GREEN, buff=0.09)
        outside_box = SurroundingRectangle(outside, color=RED, buff=0.09)

        formula = VGroup(
            MathTex(over.matrix_tex, font_size=33, color=YELLOW),
            MathTex(over.column_space_condition_tex, font_size=31, color=GREEN),
            Text("The image is a plane inside the three-dimensional output space.", font_size=self.EXPLANATION_FONT_SIZE),
        ).arrange(DOWN, buff=0.14)
        diagram = VGroup(
            left,
            right,
            arrow,
            input_axes,
            input_vector,
            input_label,
            image,
            image_label,
            inside,
            inside_label,
            outside,
            outside_label,
            inside_box,
            outside_box,
        )
        group = VGroup(diagram, formula).arrange(DOWN, buff=0.30)
        self._fit_down_only(group, 11.2)
        return self._boxed(group, buff=0.22)

    def _over_compatible_panel(self, over):
        data = VGroup(
            MathTex(over.matrix_tex, font_size=35, color=YELLOW),
            MathTex(r"\mathbf{b}=\begin{bmatrix}2\\-1\\1\end{bmatrix}", font_size=35, color=GREEN),
        ).arrange(RIGHT, buff=0.85)
        reduction = VGroup(
            MathTex(over.compatible_augmented_tex, font_size=31),
            MathTex(r"\xrightarrow{\ R_3\leftarrow R_3-R_1-R_2\ }", font_size=27, color=YELLOW),
            MathTex(over.compatible_reduced_tex, font_size=31),
        ).arrange(RIGHT, buff=0.25)
        conclusion = VGroup(
            MathTex(r"0=0", font_size=34, color=GREEN),
            MathTex(r"\mathbf{x}=\begin{bmatrix}2\\-1\end{bmatrix}", font_size=36, color=YELLOW),
            Text("The third equation agrees with the first two.", font_size=self.EXPLANATION_FONT_SIZE),
        ).arrange(DOWN, buff=0.13)
        group = VGroup(data, reduction, conclusion).arrange(DOWN, buff=0.30)
        self._fit_down_only(group, 11.2)
        return self._boxed(group, buff=0.23)

    def _over_incompatible_panel(self, over):
        data = VGroup(
            MathTex(over.matrix_tex, font_size=35, color=YELLOW),
            MathTex(r"\mathbf{b}=\begin{bmatrix}2\\-1\\0\end{bmatrix}", font_size=35, color=RED),
        ).arrange(RIGHT, buff=0.85)
        reduction = VGroup(
            MathTex(over.incompatible_augmented_tex, font_size=31),
            MathTex(r"\xrightarrow{\ R_3\leftarrow R_3-R_1-R_2\ }", font_size=27, color=YELLOW),
            MathTex(over.incompatible_reduced_tex, font_size=31),
        ).arrange(RIGHT, buff=0.25)
        contradiction = MathTex(r"0=-1", font_size=38, color=RED)
        contradiction_box = SurroundingRectangle(contradiction, color=RED, buff=0.13)
        conclusion = VGroup(
            VGroup(contradiction_box, contradiction),
            Text("The proposed output lies outside the column space, so no solution exists.", font_size=self.EXPLANATION_FONT_SIZE),
        ).arrange(DOWN, buff=0.18)
        group = VGroup(data, reduction, conclusion).arrange(DOWN, buff=0.30)
        self._fit_down_only(group, 11.2)
        return self._boxed(group, buff=0.23)

    def _over_rule_panel(self, over):
        rank = MathTex(over.full_column_rank_tex, font_size=36, color=YELLOW)
        left_card = self._rule_card(
            "Compatible",
            r"\mathbf{b}\in\operatorname{Col}(A)",
            "exactly one solution",
            GREEN,
        )
        right_card = self._rule_card(
            "Incompatible",
            r"\mathbf{b}\notin\operatorname{Col}(A)",
            "no solution",
            RED,
        )
        cards = VGroup(left_card, right_card).arrange(RIGHT, buff=0.52)
        limitation = VGroup(
            MathTex(r"\operatorname{rank}(A)\le n<m", font_size=32),
            Text("A tall matrix cannot reach every vector in the output space.", font_size=self.EXPLANATION_FONT_SIZE),
        ).arrange(DOWN, buff=0.12)
        group = VGroup(rank, cards, limitation).arrange(DOWN, buff=0.30)
        self._fit_down_only(group, 11.2)
        return self._boxed(group, buff=0.23)

    def _under_example_panel(self, under):
        data = VGroup(
            MathTex(under.matrix_tex, font_size=36, color=YELLOW),
            MathTex(r"\mathbf{b}=\begin{bmatrix}2\\-1\end{bmatrix}", font_size=36, color=GREEN),
        ).arrange(RIGHT, buff=0.85)
        augmented = MathTex(under.augmented_tex, font_size=35)
        equations = MathTex(r"x+z=2,\qquad y+z=-1", font_size=34)
        parameter = MathTex(under.parameter_equations_tex, font_size=34, color=YELLOW)
        note = Text("The third variable is free because there are only two pivots.", font_size=self.EXPLANATION_FONT_SIZE)
        group = VGroup(data, augmented, equations, parameter, note).arrange(DOWN, buff=0.25)
        self._fit_down_only(group, 11.0)
        return self._boxed(group, buff=0.23)

    def _under_solution_panel(self, under):
        solution = MathTex(under.complete_solution_tex, font_size=36, color=YELLOW)

        left = self._space_box(r"\mathbb{R}^3", 4.35, 2.15)
        right = self._space_box(r"\mathbb{R}^2", 3.05, 2.15)
        left.move_to(LEFT * 3.45)
        right.move_to(RIGHT * 3.55)
        arrow = self._map_arrow(left[0], right[0])
        family = Line(LEFT * 1.35, RIGHT * 1.35, color=YELLOW).rotate(0.30).move_to(left[0])
        family_label = MathTex(r"\mathbf{x}_p+N(A)", font_size=23, color=YELLOW).next_to(family, UP, buff=0.08)
        points = VGroup()
        for shift in (-0.78, 0.0, 0.78):
            points.add(Circle(radius=0.085, color=YELLOW, fill_opacity=1).move_to(family.get_center() + family.get_unit_vector() * shift))
        output = Circle(radius=0.10, color=GREEN, fill_opacity=1).move_to(right[0])
        output_label = MathTex(r"\mathbf{b}", font_size=24, color=GREEN).next_to(output, RIGHT, buff=0.09)
        diagram = VGroup(left, right, arrow, family, family_label, points, output, output_label)
        caption = Text(
            "Every point on the solution line maps to the same output.",
            font_size=self.EXPLANATION_FONT_SIZE,
            color=GREEN,
        )
        group = VGroup(solution, diagram, caption).arrange(DOWN, buff=0.28)
        self._fit_down_only(group, 11.2)
        return self._boxed(group, buff=0.22)

    def _under_rule_panel(self, under):
        rank = MathTex(under.full_row_rank_tex, font_size=36, color=YELLOW)
        existence = self._rule_card(
            "Full row rank",
            r"\operatorname{rank}(A)=m",
            "every right-hand side is reachable",
            GREEN,
        )
        uniqueness = self._rule_card(
            "More unknowns",
            r"\dim N(A)=n-m>0",
            "every solution belongs to an infinite family",
            YELLOW,
        )
        cards = VGroup(existence, uniqueness).arrange(RIGHT, buff=0.44)
        general = VGroup(
            MathTex(r"m<n\Longrightarrow n-\operatorname{rank}(A)\ge n-m>0", font_size=31),
            Text("Therefore an underdetermined system can have no solution or infinitely many, but never exactly one.", font_size=self.EXPLANATION_FONT_SIZE),
        ).arrange(DOWN, buff=0.13)
        self._fit_down_only(general, 10.9)
        group = VGroup(rank, cards, general).arrange(DOWN, buff=0.28)
        self._fit_down_only(group, 11.2)
        return self._boxed(group, buff=0.22)

    def _wide_counterexample_panel(self, under):
        data = VGroup(
            MathTex(r"\widetilde A=\begin{bmatrix}1&0&1\\2&0&2\end{bmatrix}", font_size=35, color=YELLOW),
            MathTex(r"\mathbf{b}=\begin{bmatrix}1\\0\end{bmatrix}", font_size=35, color=RED),
        ).arrange(RIGHT, buff=0.85)
        reduction = VGroup(
            MathTex(under.deficient_augmented_tex, font_size=32),
            MathTex(r"\xrightarrow{\ R_2\leftarrow R_2-2R_1\ }", font_size=27, color=YELLOW),
            MathTex(under.deficient_reduced_tex, font_size=32),
        ).arrange(RIGHT, buff=0.26)
        contradiction = MathTex(r"0=-2", font_size=38, color=RED)
        contradiction_box = SurroundingRectangle(contradiction, color=RED, buff=0.13)
        explanation = VGroup(
            VGroup(contradiction_box, contradiction),
            MathTex(r"\operatorname{rank}(\widetilde A)=1<m=2", font_size=32),
            Text("The columns span only a line in the output plane, so some right-hand sides are unreachable.", font_size=self.EXPLANATION_FONT_SIZE),
        ).arrange(DOWN, buff=0.15)
        group = VGroup(data, reduction, explanation).arrange(DOWN, buff=0.29)
        self._fit_down_only(group, 11.2)
        return self._boxed(group, buff=0.23)

    def _summary_panel(self, snapshot):
        tall = VGroup(
            Text("Overdetermined", font_size=27, color=YELLOW),
            MathTex(r"m>n", font_size=31),
            Text("Full column rank:", font_size=self.EXPLANATION_FONT_SIZE, color=GREEN),
            Text("compatible -> one solution", font_size=self.EXPLANATION_FONT_SIZE),
            Text("incompatible -> no solution", font_size=self.EXPLANATION_FONT_SIZE),
            Text("never solvable for every b", font_size=self.EXPLANATION_FONT_SIZE, color=RED),
        ).arrange(DOWN, buff=0.14)
        wide = VGroup(
            Text("Underdetermined", font_size=27, color=YELLOW),
            MathTex(r"m<n", font_size=31),
            Text("Whenever consistent:", font_size=self.EXPLANATION_FONT_SIZE, color=GREEN),
            Text("infinitely many solutions", font_size=self.EXPLANATION_FONT_SIZE),
            Text("full row rank -> every b", font_size=self.EXPLANATION_FONT_SIZE),
            Text("never exactly one solution", font_size=self.EXPLANATION_FONT_SIZE, color=RED),
        ).arrange(DOWN, buff=0.14)
        cards = VGroup(self._boxed(tall, buff=0.22), self._boxed(wide, buff=0.22)).arrange(RIGHT, buff=0.55)
        common = VGroup(
            MathTex(snapshot.common_consistency_tex, font_size=33, color=YELLOW),
            MathTex(snapshot.augmented_rank_tex, font_size=32, color=GREEN),
        ).arrange(DOWN, buff=0.15)
        group = VGroup(cards, common).arrange(DOWN, buff=0.34)
        self._fit_down_only(group, 11.2)
        return self._boxed(group, buff=0.22)

    def _rule_card(self, title: str, formula_tex: str, conclusion: str, color):
        title_text = Text(title, font_size=25, color=color)
        formula = MathTex(formula_tex, font_size=30)
        conclusion_text = Text(conclusion, font_size=self.EXPLANATION_FONT_SIZE, color=color)
        content = VGroup(title_text, formula, conclusion_text).arrange(DOWN, buff=0.16)
        self._fit_down_only(content, 5.0)
        return self._boxed(content, buff=0.20)

    def _heading(self, text: str, font_size: int):
        heading = Text(text, font_size=font_size, color=YELLOW)
        self._fit_down_only(heading, 11.4)
        heading.move_to(UP * self.HEADING_Y)
        return heading

    def _space_box(self, label_tex: str, width: float, height: float):
        box = Rectangle(width=width, height=height, color=BLUE)
        label = MathTex(label_tex, font_size=27).next_to(box, UP, buff=0.09)
        return VGroup(box, label)

    def _space_box_3d(self, label_tex: str, width: float, height: float):
        front = Rectangle(width=width * 0.78, height=height * 0.78, color=BLUE)
        back = Rectangle(width=width * 0.78, height=height * 0.78, color=BLUE)
        offset = LEFT * 0.45 + UP * 0.28
        back.shift(offset)
        connectors = VGroup(
            Line(back.get_corner(UL), front.get_corner(UL), color=BLUE),
            Line(back.get_corner(UR), front.get_corner(UR), color=BLUE),
            Line(back.get_corner(DL), front.get_corner(DL), color=BLUE),
            Line(back.get_corner(DR), front.get_corner(DR), color=BLUE),
        )
        axes = VGroup(
            Arrow(front.get_center(), front.get_center() + RIGHT * 1.05, buff=0, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.18),
            Arrow(front.get_center(), front.get_center() + UP * 0.92, buff=0, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.18),
            Arrow(front.get_center(), front.get_center() + LEFT * 0.62 + DOWN * 0.42, buff=0, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.18),
        )
        frame = VGroup(back, connectors, front, axes)
        label = MathTex(label_tex, font_size=27).next_to(frame, UP, buff=0.09)
        return VGroup(frame, label)

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
        action_label = MathTex(r"\mathbf{x}\mapsto\mathbf{b}", font_size=22, color=YELLOW).next_to(arrow, DOWN, buff=0.08)
        return VGroup(arrow, map_label, action_label)

    def _boxed(self, content, *, buff: float = 0.24):
        box = SurroundingRectangle(content, color=BLUE, buff=buff)
        return VGroup(box, content)

    @staticmethod
    def _fit_down_only(mobject, max_width: float):
        if mobject.width > max_width:
            mobject.scale_to_fit_width(max_width)
        return mobject
