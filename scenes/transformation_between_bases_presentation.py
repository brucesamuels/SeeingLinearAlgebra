"""Manim presentation: Changing a Transformation Between Two Bases."""
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, PURPLE_C, TEAL_C, WHITE, YELLOW,
    DOWN, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, Line, MathTex, Matrix, NumberPlane,
    ReplacementTransform, Scene, Text, Transform, TransformFromCopy, VGroup, smooth,
)


class TransformationBetweenBasesPresentation(Scene):
    CHAPTER_BANNER = "CHANGE OF BASIS"
    LESSON_TITLE = "Changing a Transformation Between Two Bases"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.6:
            item.scale_to_fit_width(11.6)
        return item

    def _chrome(self, heading_text):
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD").to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=30, color=YELLOW, weight="BOLD").next_to(banner, DOWN, buff=0.12)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.17)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.6)
        return new

    @staticmethod
    def _fit(group):
        if group.width > 11.2:
            group.scale_to_fit_width(11.2)
        if group.height > 4.65:
            group.scale_to_fit_height(4.65)
        group.move_to(DOWN * 0.42)
        return group

    @staticmethod
    def _matrix(entries, scale=0.80, v_buff=0.95):
        return Matrix(entries, v_buff=v_buff, h_buff=1.0).scale(scale)

    @staticmethod
    def _augmented(left, right, scale=0.78):
        """One structural Matrix with a divider between its two blocks."""
        import numpy as np
        entries = [list(left[row]) + list(right[row]) for row in range(2)]
        matrix = Matrix(entries, v_buff=0.95, h_buff=0.90)
        columns = matrix.get_columns()
        divider_x = (columns[1].get_right()[0] + columns[2].get_left()[0]) / 2
        divider_center = np.array([divider_x, matrix.get_center()[1], 0.0])
        divider = Line(
            divider_center + UP * matrix.height * 0.34,
            divider_center + DOWN * matrix.height * 0.34,
            color=WHITE, stroke_width=2.4,
        )
        return VGroup(matrix, divider).scale(scale)

    @staticmethod
    def _grid(plane, first, second, first_color, second_color):
        import numpy as np
        first, second = np.asarray(first), np.asarray(second)
        lines = VGroup()
        for fixed_first in range(-5, 8):
            start = fixed_first * first - 6 * second
            end = fixed_first * first + 6 * second
            lines.add(Line(
                plane.c2p(*start), plane.c2p(*end), color=second_color,
                stroke_width=3.4 if fixed_first == 0 else 2.0,
                stroke_opacity=1.0 if fixed_first == 0 else 0.82,
            ))
        for fixed_second in range(-6, 7):
            start = -5 * first + fixed_second * second
            end = 7 * first + fixed_second * second
            lines.add(Line(
                plane.c2p(*start), plane.c2p(*end), color=first_color,
                stroke_width=3.4 if fixed_second == 0 else 2.0,
                stroke_opacity=1.0 if fixed_second == 0 else 0.82,
            ))
        return lines

    def construct(self):
        import numpy as np

        banner, title, heading = self._chrome("What if the matrix we start with is already in a nonstandard basis?")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))
        opening = self._fit(VGroup(
            MathTex(r"[T]_{\mathcal B}\quad\longrightarrow\quad[T]_{\mathcal C}", font_size=72, color=YELLOW),
            Text("We want a direct translation between two coordinate languages.", font_size=34, color=WHITE),
            Text("The standard basis does not need to appear in the route.", font_size=33, color=ORANGE),
        ).arrange(DOWN, buff=0.58))
        self.play(FadeIn(opening[0])); self.play(FadeIn(opening[1])); self.play(FadeIn(opening[2])); self.wait(1.8)

        heading = self._replace_heading(heading, "First watch the fixed geometric transformation on the B-grid.")
        self.play(FadeOut(opening))
        plane = NumberPlane(
            x_range=[-2, 10, 1], y_range=[-5, 6, 1], x_length=7.0, y_length=5.8,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.4, "stroke_opacity": 0.42},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.6},
        ).shift(DOWN * 0.42)
        b1v, b2v = np.array([1, 1]), np.array([1, -1])
        c1v, c2v = np.array([1, 1]), np.array([2, 0])
        grid_b = self._grid(plane, b1v, b2v, GREEN_C, BLUE_C)
        grid_c = self._grid(plane, c1v, c2v, TEAL_C, PURPLE_C)
        b1 = Arrow(plane.c2p(0, 0), plane.c2p(*b1v), buff=0, color=GREEN_C, stroke_width=7)
        b2 = Arrow(plane.c2p(0, 0), plane.c2p(*b2v), buff=0, color=BLUE_C, stroke_width=7)
        c1 = Arrow(plane.c2p(0, 0), plane.c2p(*c1v), buff=0, color=TEAL_C, stroke_width=7)
        c2 = Arrow(plane.c2p(0, 0), plane.c2p(*c2v), buff=0, color=PURPLE_C, stroke_width=7)
        vector = Arrow(plane.c2p(0, 0), plane.c2p(3, 1), buff=0, color=ORANGE, stroke_width=9)
        image = Arrow(plane.c2p(0, 0), plane.c2p(8, 2), buff=0, color=YELLOW, stroke_width=9)
        vector_label_b = MathTex(r"[\mathbf v]_{\mathcal B}=(2,1)", font_size=37, color=ORANGE).next_to(vector.get_end(), UP, buff=0.10)
        image_label_b = MathTex(r"[T\mathbf v]_{\mathcal B}=(5,3)", font_size=37, color=YELLOW).next_to(image.get_end(), UP, buff=0.10)
        basis_b = MathTex(r"\mathcal B=\{(1,1),(1,-1)\}", font_size=34, color=WHITE)
        matrix_b_readout = VGroup(
            MathTex(r"[T]_{\mathcal B}=", font_size=36, color=WHITE),
            self._matrix([["2", "1"], ["0", "3"]], 0.55),
        ).arrange(RIGHT, buff=0.10)
        graphic_readout_b = VGroup(basis_b, matrix_b_readout).arrange(RIGHT, buff=0.55).to_edge(DOWN, buff=0.10)
        self.play(Create(grid_b), FadeIn(b1), FadeIn(b2), FadeIn(vector), FadeIn(vector_label_b), FadeIn(graphic_readout_b))
        self.wait(0.9)
        self.play(TransformFromCopy(vector, image), FadeIn(image_label_b), run_time=2.3)
        self.wait(1.5)

        heading = self._replace_heading(heading, "Now move the entire coordinate grid from B to C.")
        vector_label_c = MathTex(r"[\mathbf v]_{\mathcal C}=(1,1)", font_size=37, color=ORANGE).move_to(vector_label_b)
        image_label_c = MathTex(r"[T\mathbf v]_{\mathcal C}=(2,3)", font_size=37, color=YELLOW).move_to(image_label_b)
        basis_c = MathTex(r"\mathcal C=\{(1,1),(2,0)\}", font_size=34, color=WHITE)
        matrix_c_readout = VGroup(
            MathTex(r"[T]_{\mathcal C}=", font_size=36, color=WHITE),
            self._matrix([["2", "0"], ["0", "3"]], 0.55),
        ).arrange(RIGHT, buff=0.10)
        graphic_readout_c = VGroup(basis_c, matrix_c_readout).arrange(RIGHT, buff=0.55).move_to(graphic_readout_b)
        self.play(
            Transform(grid_b, grid_c, rate_func=smooth),
            Transform(b1, c1), Transform(b2, c2),
            ReplacementTransform(vector_label_b, vector_label_c),
            ReplacementTransform(image_label_b, image_label_c),
            ReplacementTransform(graphic_readout_b, graphic_readout_c),
            run_time=4.0,
        )
        fixed_note = Text("The orange and yellow geometric vectors did not move.", font_size=29, color=WHITE).to_edge(DOWN, buff=0.12)
        self.play(ReplacementTransform(graphic_readout_c, fixed_note)); self.wait(1.8)

        heading = self._replace_heading(heading, "Build the transition matrix by rewriting each B-basis vector in the C-basis.")
        self.play(
            FadeOut(vector), FadeOut(image), FadeOut(vector_label_c), FadeOut(image_label_c),
            FadeOut(fixed_note),
        )
        c1_label = MathTex(r"\mathbf c_1=\mathbf b_1", font_size=35, color=TEAL_C).next_to(c1.get_end(), UP, buff=0.10)
        c2_label = MathTex(r"\mathbf c_2", font_size=35, color=PURPLE_C).next_to(c2.get_end(), UP, buff=0.10)
        negative_c1 = Arrow(plane.c2p(0, 0), plane.c2p(-1, -1), buff=0, color=TEAL_C, stroke_width=7)
        shifted_c2 = Arrow(plane.c2p(-1, -1), plane.c2p(1, -1), buff=0, color=PURPLE_C, stroke_width=7)
        b2_target = Arrow(plane.c2p(0, 0), plane.c2p(1, -1), buff=0, color=YELLOW, stroke_width=9)
        b2_label = MathTex(r"\mathbf b_2", font_size=36, color=YELLOW).next_to(b2_target.get_end(), DOWN, buff=0.10)
        combinations = VGroup(
            MathTex(r"\mathbf b_1=1\mathbf c_1+0\mathbf c_2", font_size=38, color=WHITE),
            MathTex(r"\mathbf b_2=-\mathbf c_1+\mathbf c_2", font_size=38, color=WHITE),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.10)
        self.play(FadeIn(c1_label), FadeIn(c2_label), FadeIn(combinations[0]))
        self.play(Create(negative_c1), Create(shifted_c2), FadeIn(b2_target), FadeIn(b2_label), FadeIn(combinations[1]), run_time=2.5)
        self.wait(1.8)

        heading = self._replace_heading(heading, "The coefficient columns of those linear combinations form the transition matrix.")
        self.play(
            FadeOut(grid_b), FadeOut(b1), FadeOut(b2), FadeOut(c1_label), FadeOut(c2_label),
            FadeOut(negative_c1), FadeOut(shifted_c2), FadeOut(b2_target), FadeOut(b2_label),
            FadeOut(combinations),
        )
        first_column = VGroup(
            MathTex(r"[\mathbf b_1]_{\mathcal C}=", font_size=45),
            self._matrix([["1"], ["0"]], 0.78),
        ).arrange(RIGHT, buff=0.12)
        second_column = VGroup(
            MathTex(r"[\mathbf b_2]_{\mathcal C}=", font_size=45),
            self._matrix([["-1"], ["1"]], 0.78),
        ).arrange(RIGHT, buff=0.12)
        column_row = VGroup(first_column, second_column).arrange(RIGHT, buff=0.75)
        assembled = VGroup(
            MathTex(
                r"Q_{\mathcal C\leftarrow\mathcal B}="
                r"\big[\,[\mathbf b_1]_{\mathcal C}\ \ [\mathbf b_2]_{\mathcal C}\,\big]=",
                font_size=43, color=YELLOW,
            ),
            self._matrix([["1", "-1"], ["0", "1"]], 0.82),
        ).arrange(RIGHT, buff=0.14)
        column_note = Text("Each column tells how to build one old basis vector from the new basis vectors.", font_size=28, color=ORANGE)
        column_card = self._fit(VGroup(column_row, assembled, column_note).arrange(DOWN, buff=0.48))
        self.play(FadeIn(column_row)); self.play(FadeIn(assembled)); self.play(FadeIn(column_note)); self.wait(2.0)

        heading = self._replace_heading(heading, "Substitution shows why the same columns convert every coordinate vector.")
        self.play(FadeOut(column_card))
        substitution = VGroup(
            MathTex(r"\mathbf v=x\mathbf b_1+y\mathbf b_2", font_size=48),
            MathTex(r"=x\mathbf c_1+y(-\mathbf c_1+\mathbf c_2)", font_size=48),
            MathTex(r"=(x-y)\mathbf c_1+y\mathbf c_2", font_size=48, color=YELLOW),
        ).arrange(DOWN, buff=0.24)
        coordinate_action = VGroup(
            MathTex(r"[\mathbf v]_{\mathcal C}=", font_size=46),
            self._matrix([["1", "-1"], ["0", "1"]], 0.76),
            MathTex(r"[\mathbf v]_{\mathcal B}", font_size=46),
        ).arrange(RIGHT, buff=0.15)
        substitution_card = self._fit(VGroup(substitution, coordinate_action).arrange(DOWN, buff=0.50))
        self.play(FadeIn(substitution[0])); self.play(FadeIn(substitution[1])); self.play(FadeIn(substitution[2])); self.play(FadeIn(coordinate_action)); self.wait(2.1)

        heading = self._replace_heading(heading, "The familiar inverse formula is a consequence of those linear combinations.")
        self.play(FadeOut(substitution_card))
        matrix_equation = MathTex(
            r"P_{\mathcal C}Q_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal B}",
            font_size=62, color=WHITE,
        )
        solve_for_q = MathTex(
            r"\boxed{Q_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal C}^{-1}P_{\mathcal B}}",
            font_size=62, color=YELLOW,
        )
        consequence_note = Text("The columns of this matrix equation are exactly the two linear-combination equations.", font_size=29, color=ORANGE)
        consequence_card = self._fit(VGroup(matrix_equation, solve_for_q, consequence_note).arrange(DOWN, buff=0.52))
        self.play(FadeIn(matrix_equation)); self.play(FadeIn(solve_for_q)); self.play(FadeIn(consequence_note)); self.wait(2.0)

        heading = self._replace_heading(heading, "Convert C-input coordinates into B, apply T, then convert back to C.")
        self.play(FadeOut(consequence_card))
        route = MathTex(
            r"[\mathbf v]_{\mathcal C}"
            r"\xrightarrow{\quad Q_{\mathcal B\leftarrow\mathcal C}\quad}"
            r"[\mathbf v]_{\mathcal B}"
            r"\xrightarrow{\quad[T]_{\mathcal B}\quad}"
            r"[T\mathbf v]_{\mathcal B}"
            r"\xrightarrow{\quad Q_{\mathcal C\leftarrow\mathcal B}\quad}"
            r"[T\mathbf v]_{\mathcal C}",
            font_size=43, color=WHITE,
        )
        route_note = Text("No standard-coordinate stage is required.", font_size=34, color=ORANGE)
        pipeline = self._fit(VGroup(route, route_note).arrange(DOWN, buff=0.62))
        self.play(FadeIn(route)); self.play(FadeIn(route_note)); self.wait(1.9)

        heading = self._replace_heading(heading, "The two direct transition matrices are inverses.")
        self.play(FadeOut(pipeline))
        transitions = VGroup(
            MathTex(r"Q_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal C}^{-1}P_{\mathcal B}=", font_size=45),
            self._matrix([["1", "-1"], ["0", "1"]], 0.82),
        ).arrange(RIGHT, buff=0.15)
        reverse = VGroup(
            MathTex(r"Q_{\mathcal B\leftarrow\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}^{-1}=", font_size=45),
            self._matrix([["1", "1"], ["0", "1"]], 0.82),
        ).arrange(RIGHT, buff=0.15)
        inverse_product = VGroup(
            self._matrix([["1", "1"], ["0", "1"]], 0.68),
            self._matrix([["1", "-1"], ["0", "1"]], 0.68),
            MathTex("=", font_size=44),
            self._matrix([["1", "0"], ["0", "1"]], 0.68),
        ).arrange(RIGHT, buff=0.15)
        direction_note = Text("Go from B to C and back to B: every coordinate vector is unchanged.", font_size=28, color=ORANGE)
        transition_card = self._fit(VGroup(transitions, reverse, inverse_product, direction_note).arrange(DOWN, buff=0.34))
        self.play(FadeIn(transitions)); self.play(FadeIn(reverse)); self.play(FadeIn(inverse_product)); self.play(FadeIn(direction_note)); self.wait(2.0)

        heading = self._replace_heading(heading, "A row-reduction procedure computes the transition matrix efficiently.")
        self.play(FadeOut(transition_card))
        general_start = MathTex(r"\left[P_{\mathcal C}\mid P_{\mathcal B}\right]", font_size=54)
        general_end = MathTex(r"\left[I\mid Q_{\mathcal C\leftarrow\mathcal B}\right]", font_size=54)
        procedure = VGroup(
            general_start,
            MathTex(r"\xrightarrow{\quad\text{row operations}\quad}", font_size=46, color=YELLOW),
            general_end,
        ).arrange(RIGHT, buff=0.28)
        labels = VGroup(
            Text("new / output basis", font_size=27, color=TEAL_C),
            Text("old / input basis", font_size=27, color=GREEN_C),
        ).arrange(RIGHT, buff=1.1)
        rule = Text("Reduce the new-basis block to I; the right block becomes old-to-new.", font_size=30, color=ORANGE)
        procedure_card = self._fit(VGroup(labels, procedure, rule).arrange(DOWN, buff=0.50))
        self.play(FadeIn(labels)); self.play(FadeIn(procedure)); self.play(FadeIn(rule)); self.wait(2.1)

        heading = self._replace_heading(heading, "For our bases, reduce the augmented matrix one row operation at a time.")
        self.play(FadeOut(procedure_card))
        state = self._augmented([["1", "2"], ["1", "0"]], [["1", "1"], ["1", "-1"]], 0.92).move_to(DOWN * 0.28)
        operation = MathTex(r"[P_{\mathcal C}\mid P_{\mathcal B}]", font_size=43, color=WHITE).next_to(state, DOWN, buff=0.30)
        self.play(FadeIn(state), FadeIn(operation)); self.wait(0.8)

        state_1 = self._augmented([["1", "2"], ["0", "-2"]], [["1", "1"], ["0", "-2"]], 0.92).move_to(state)
        operation_1 = MathTex(r"R_2\leftarrow R_2-R_1", font_size=43, color=YELLOW).move_to(operation)
        self.play(ReplacementTransform(state, state_1), ReplacementTransform(operation, operation_1), run_time=1.2)
        self.wait(0.7)

        state_2 = self._augmented([["1", "2"], ["0", "1"]], [["1", "1"], ["0", "1"]], 0.92).move_to(state_1)
        operation_2 = MathTex(r"R_2\leftarrow-\tfrac12R_2", font_size=43, color=YELLOW).move_to(operation_1)
        self.play(ReplacementTransform(state_1, state_2), ReplacementTransform(operation_1, operation_2), run_time=1.2)
        self.wait(0.7)

        state_3 = self._augmented([["1", "0"], ["0", "1"]], [["1", "-1"], ["0", "1"]], 0.92).move_to(state_2)
        operation_3 = MathTex(r"R_1\leftarrow R_1-2R_2", font_size=43, color=YELLOW).move_to(operation_2)
        self.play(ReplacementTransform(state_2, state_3), ReplacementTransform(operation_2, operation_3), run_time=1.2)
        result = VGroup(
            MathTex(r"Q_{\mathcal C\leftarrow\mathcal B}=", font_size=42, color=ORANGE),
            self._matrix([["1", "-1"], ["0", "1"]], 0.68),
        ).arrange(RIGHT, buff=0.12).next_to(operation_3, DOWN, buff=0.20)
        self.play(FadeIn(result)); self.wait(2.0)

        heading = self._replace_heading(heading, "Conjugate by the direct coordinate-change matrix.")
        self.play(FadeOut(state_3), FadeOut(operation_3), FadeOut(result))
        action = MathTex(
            r"[T\mathbf v]_{\mathcal C}="
            r"Q_{\mathcal C\leftarrow\mathcal B}[T]_{\mathcal B}"
            r"Q_{\mathcal B\leftarrow\mathcal C}[\mathbf v]_{\mathcal C}",
            font_size=52, color=WHITE,
        )
        formula = MathTex(
            r"\boxed{[T]_{\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}"
            r"[T]_{\mathcal B}Q_{\mathcal B\leftarrow\mathcal C}}",
            font_size=57, color=YELLOW,
        )
        equivalent = MathTex(
            r"[T]_{\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}"
            r"[T]_{\mathcal B}Q_{\mathcal C\leftarrow\mathcal B}^{-1}",
            font_size=50, color=ORANGE,
        )
        derivation = self._fit(VGroup(action, formula, equivalent).arrange(DOWN, buff=0.46))
        self.play(FadeIn(action)); self.play(FadeIn(formula)); self.play(FadeIn(equivalent)); self.wait(2.0)

        heading = self._replace_heading(heading, "Compute the matrix directly—without passing through standard coordinates.")
        self.play(FadeOut(derivation))
        givens = VGroup(
            VGroup(MathTex(r"[T]_{\mathcal B}=", font_size=45), self._matrix([["2", "1"], ["0", "3"]], 0.78)).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"Q_{\mathcal C\leftarrow\mathcal B}=", font_size=45), self._matrix([["1", "-1"], ["0", "1"]], 0.78)).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"Q_{\mathcal B\leftarrow\mathcal C}=", font_size=45), self._matrix([["1", "1"], ["0", "1"]], 0.78)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.42)
        product = VGroup(
            MathTex(r"[T]_{\mathcal C}=", font_size=44, color=YELLOW),
            self._matrix([["1", "-1"], ["0", "1"]], 0.72),
            self._matrix([["2", "1"], ["0", "3"]], 0.72),
            self._matrix([["1", "1"], ["0", "1"]], 0.72),
            MathTex("=", font_size=46, color=YELLOW),
            self._matrix([["2", "0"], ["0", "3"]], 0.78),
        ).arrange(RIGHT, buff=0.12).set_color(YELLOW)
        computation = self._fit(VGroup(givens, product).arrange(DOWN, buff=0.56))
        self.play(FadeIn(givens)); self.play(FadeIn(product)); self.wait(2.0)

        heading = self._replace_heading(heading, "Verify the same input and output entirely in C-coordinates.")
        self.play(FadeOut(computation))
        b_line = VGroup(
            MathTex(r"\mathcal B:\quad", font_size=45, color=GREEN_C),
            self._matrix([["2", "1"], ["0", "3"]], 0.78),
            self._matrix([["2"], ["1"]], 0.78),
            MathTex("=", font_size=46), self._matrix([["5"], ["3"]], 0.78),
        ).arrange(RIGHT, buff=0.15)
        c_line = VGroup(
            MathTex(r"\mathcal C:\quad", font_size=45, color=TEAL_C),
            self._matrix([["2", "0"], ["0", "3"]], 0.78),
            self._matrix([["1"], ["1"]], 0.78),
            MathTex("=", font_size=46), self._matrix([["2"], ["3"]], 0.78),
        ).arrange(RIGHT, buff=0.15)
        check = MathTex(
            r"(2,1)_{\mathcal B}\leftrightarrow(1,1)_{\mathcal C},\qquad"
            r"(5,3)_{\mathcal B}\leftrightarrow(2,3)_{\mathcal C}",
            font_size=46, color=ORANGE,
        )
        verification = self._fit(VGroup(b_line, c_line, check).arrange(DOWN, buff=0.42))
        self.play(FadeIn(b_line)); self.play(FadeIn(c_line)); self.play(FadeIn(check)); self.wait(2.0)

        heading = self._replace_heading(heading, "The transformation is unchanged; only its matrix description changes.")
        self.play(FadeOut(verification))
        final = self._fit(VGroup(
            MathTex(r"[T]_{\mathcal B}\quad\longleftrightarrow\quad[T]_{\mathcal C}", font_size=67, color=WHITE),
            MathTex(
                r"\boxed{[T]_{\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}"
                r"[T]_{\mathcal B}Q_{\mathcal C\leftarrow\mathcal B}^{-1}}",
                font_size=58, color=YELLOW,
            ),
            Text("Same geometric action. A different coordinate language.", font_size=33, color=ORANGE),
        ).arrange(DOWN, buff=0.52))
        self.play(FadeIn(final)); self.wait(2.2)
