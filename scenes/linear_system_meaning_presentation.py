"""CP105 presentation: what it means to solve A x = b."""

from __future__ import annotations

from manim import (
    Axes,
    BLUE,
    Create,
    DEGREES,
    DOWN,
    Dot,
    Dot3D,
    FadeIn,
    FadeOut,
    FadeTransform,
    GREEN,
    LEFT,
    Line,
    MathTex,
    Matrix,
    RED,
    RIGHT,
    Surface,
    SurroundingRectangle,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
)

from engine.linear_system_meaning import LinearSystemMeaning


class LinearSystemMeaningPresentation(ThreeDScene):
    """Introduce one system through 2D geometry, 3D geometry, and algebra."""

    TITLE = r"What Does It Mean to Solve $A\mathbf{x}=\mathbf{b}$?"
    LINE_COLORS = (BLUE, GREEN)
    PLANE_COLORS = (BLUE, GREEN, RED)

    def construct(self) -> None:
        system = LinearSystemMeaning()
        planar_snapshot = system.planar_snapshot()
        snapshot = system.snapshot()

        title = Text(
            "What Does It Mean to Solve A x = b?",
            font_size=40,
            color=WHITE,
        ).to_edge(UP, buff=0.28)
        subtitle = Text(
            "In the plane, solving means finding where the graphs meet.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.14)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(Write(title), FadeIn(subtitle), run_time=1.3)

        axes_2d, lines, point_2d, system_label_2d = self._build_planar_picture(system)
        self.play(Create(axes_2d), run_time=1.2)
        for line in lines:
            self.play(Create(line), run_time=0.8)
        self.play(FadeIn(point_2d), FadeIn(system_label_2d), run_time=0.8)

        planar_solution_label = MathTex(
            r"(x,y)=(1,1)",
            font_size=34,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.40)
        self.add_fixed_in_frame_mobjects(planar_solution_label)
        self.play(FadeIn(planar_solution_label), run_time=0.7)
        self.wait(1.8)
        self.play(FadeOut(planar_solution_label), run_time=0.4)

        transition = VGroup(
            Text("The same idea extends beyond the plane.", font_size=27),
            Text("In three dimensions, the solution is where three planes meet.", font_size=24),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.36)
        self.add_fixed_in_frame_mobjects(transition)
        self.play(FadeIn(transition), run_time=0.8)
        self.wait(1.8)

        self.play(
            FadeOut(axes_2d),
            *[FadeOut(line) for line in lines],
            FadeOut(point_2d),
            FadeOut(system_label_2d),
            FadeOut(transition),
            FadeOut(subtitle),
            run_time=1.0,
        )

        subtitle_3d = Text(
            "In three dimensions, three equations can describe one common point.",
            font_size=24,
        ).next_to(title, DOWN, buff=0.14)
        self.add_fixed_in_frame_mobjects(subtitle_3d)
        self.play(FadeIn(subtitle_3d), run_time=0.6)

        axes, planes, intersection = self._build_plane_picture(system, snapshot)
        self.set_camera_orientation(
            phi=67 * DEGREES,
            theta=-48 * DEGREES,
            zoom=0.82,
        )
        self.play(Create(axes), run_time=1.4)
        for plane in planes:
            self.play(FadeIn(plane), run_time=0.8)
        self.play(FadeIn(intersection), run_time=0.7)
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(2.8)
        self.stop_ambient_camera_rotation()

        point_label = MathTex(
            r"(x,y,z)=(1,1,1)",
            font_size=34,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(point_label)
        self.play(FadeIn(point_label), run_time=0.8)
        self.wait(1.8)

        self.play(
            FadeOut(axes),
            *[FadeOut(plane) for plane in planes],
            FadeOut(intersection),
            FadeOut(point_label),
            FadeOut(subtitle_3d),
            run_time=1.1,
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=0.8)

        equations, matrix_equation, headings, divider = self._build_algebra_views()
        algebra_objects = VGroup(equations, matrix_equation, headings, divider)
        self.add_fixed_in_frame_mobjects(algebra_objects)
        self.play(
            FadeIn(headings),
            FadeIn(divider),
            Write(equations),
            Write(matrix_equation),
            run_time=2.0,
        )
        self.wait(3.2)

        prompt = self._build_prediction_prompt()
        self.add_fixed_in_frame_mobjects(prompt)
        self.play(FadeIn(prompt), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(prompt), run_time=0.6)

        self.play(
            FadeOut(equations),
            FadeOut(headings[0]),
            FadeOut(divider),
            headings[1].animate.move_to(UP * 1.72),
            matrix_equation.animate.move_to(UP * 0.10).scale(1.15),
            run_time=1.2,
        )
        self.wait(0.8)

        (
            focus_heading,
            focus_equation,
            focus_caption,
            matrix_block,
            vector_block,
            rhs_block,
        ) = self._build_matrix_vector_focus()
        self.play(
            FadeTransform(headings[1], focus_heading),
            FadeOut(matrix_equation),
            FadeIn(focus_equation),
            FadeIn(focus_caption),
            run_time=0.9,
        )
        row_products = self._animate_row_by_column(
            focus_equation,
            matrix_block,
            vector_block,
            rhs_block,
        )

        column_heading, column_formula, column_view = self._build_column_view()
        self.play(
            FadeOut(focus_caption),
            FadeOut(focus_equation),
            FadeOut(row_products),
            FadeTransform(focus_heading, column_heading),
            FadeIn(column_formula),
            run_time=1.2,
        )
        self.wait(3.6)

        solution_line = MathTex(
            r"x=1,\qquad y=1,\qquad z=1",
            font_size=36,
            color=YELLOW,
        ).next_to(column_view, DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(solution_line)
        self.play(Write(solution_line), run_time=1.0)
        self.wait(2.0)

        conclusion = self._build_conclusion()
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(
            FadeOut(column_view),
            FadeOut(solution_line),
            FadeIn(conclusion),
            run_time=1.0,
        )
        self.wait(4.0)

    def _build_planar_picture(self, system):
        axes = Axes(
            x_range=[-0.5, 2.5, 1],
            y_range=[-0.5, 2.5, 1],
            x_length=5.6,
            y_length=5.0,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.25)

        lines = VGroup()
        for row_index, color in enumerate(self.LINE_COLORS):
            line = axes.plot(
                lambda x, i=row_index: system.line_height(i, x),
                x_range=[-0.25, 2.25],
                color=color,
                stroke_width=5,
            )
            lines.add(line)

        point = Dot(
            point=axes.c2p(1, 1),
            radius=0.09,
            color=YELLOW,
        )
        system_label = MathTex(
            r"\begin{aligned}x+y&=2\\x-y&=0\end{aligned}",
            font_size=35,
        ).to_edge(RIGHT, buff=0.55).shift(DOWN * 0.10)
        return axes, lines, point, system_label

    def _build_plane_picture(self, system, snapshot):
        axes = ThreeDAxes(
            x_range=[-0.5, 2.5, 1],
            y_range=[-0.5, 2.5, 1],
            z_range=[-1.0, 3.0, 1],
            x_length=5.2,
            y_length=5.2,
            z_length=4.6,
        ).shift(DOWN * 0.25)

        planes = VGroup()
        for row_index, color in enumerate(self.PLANE_COLORS):
            plane = Surface(
                lambda u, v, i=row_index: axes.c2p(
                    u,
                    v,
                    system.plane_height(i, u, v),
                ),
                u_range=[-0.25, 2.25],
                v_range=[-0.25, 2.25],
                resolution=(10, 10),
                fill_opacity=0.34,
                checkerboard_colors=[color, color],
                stroke_color=color,
                stroke_width=0.45,
            )
            planes.add(plane)

        intersection = Dot3D(
            point=axes.c2p(*snapshot.solution),
            radius=0.10,
            color=YELLOW,
        )
        return axes, planes, intersection

    def _build_algebra_views(self):
        left_heading = Text("System of equations", font_size=27).move_to(
            LEFT * 3.45 + UP * 1.72
        )
        right_heading = Text("Matrix equation", font_size=27).move_to(
            RIGHT * 3.25 + UP * 1.72
        )
        headings = VGroup(left_heading, right_heading)

        equations = MathTex(
            r"\begin{aligned}"
            r"x+y+z&=3\\"
            r"2x-y+z&=2\\"
            r"x+2y-z&=2"
            r"\end{aligned}",
            font_size=39,
        ).move_to(LEFT * 3.35 + DOWN * 0.05)

        matrix_equation = MathTex(
            r"\begin{bmatrix}"
            r"1&1&1\\2&-1&1\\1&2&-1"
            r"\end{bmatrix}"
            r"\begin{bmatrix}x\\y\\z\end{bmatrix}"
            r"="
            r"\begin{bmatrix}3\\2\\2\end{bmatrix}",
            font_size=35,
        ).move_to(RIGHT * 3.05 + DOWN * 0.05)

        divider = Line(UP * 1.45, DOWN * 2.15, stroke_width=1.2)
        return equations, matrix_equation, headings, divider

    def _build_prediction_prompt(self):
        heading = Text("Pause and Predict", font_size=29, color=YELLOW)
        question = Text(
            "What do the entries of x control?",
            font_size=26,
        ).next_to(heading, DOWN, buff=0.18)
        return VGroup(heading, question).arrange(DOWN, buff=0.18).to_edge(
            DOWN,
            buff=0.34,
        )

    def _build_matrix_vector_focus(self):
        heading = Text(
            "Read the product row by column",
            font_size=29,
        ).move_to(UP * 1.72)
        matrix_block = Matrix(
            [[1, 1, 1], [2, -1, 1], [1, 2, -1]],
            h_buff=0.75,
            v_buff=0.58,
        )
        vector_block = Matrix(
            [[r"x"], [r"y"], [r"z"]],
            v_buff=0.58,
        )
        equals = MathTex(r"=", font_size=42)
        rhs_block = Matrix(
            [[3], [2], [2]],
            v_buff=0.58,
        )
        equation = VGroup(
            matrix_block,
            vector_block,
            equals,
            rhs_block,
        ).arrange(RIGHT, buff=0.34)
        equation.scale(0.88)
        equation.move_to(UP * 0.20)
        caption = Text(
            "Each row of A dots with x to produce one entry of b.",
            font_size=25,
        ).move_to(UP * 1.18)
        return (
            heading,
            equation,
            caption,
            matrix_block,
            vector_block,
            rhs_block,
        )

    def _animate_row_by_column(
        self,
        focus_equation,
        matrix_block,
        vector_block,
        rhs_block,
    ):
        row_products = VGroup(
            MathTex(r"1(x)+1(y)+1(z)=3", font_size=30, color=BLUE),
            MathTex(r"2(x)-1(y)+1(z)=2", font_size=30, color=GREEN),
            MathTex(r"1(x)+2(y)-1(z)=2", font_size=30, color=RED),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        row_products.move_to(DOWN * 1.62)

        rows = matrix_block.get_rows()
        vector_entries = vector_block.get_entries()
        rhs_entries = rhs_block.get_entries()
        colors = (BLUE, GREEN, RED)

        for row, rhs_entry, product, color in zip(
            rows,
            rhs_entries,
            row_products,
            colors,
            strict=True,
        ):
            row_box = SurroundingRectangle(row, color=color, buff=0.08)
            vector_box = SurroundingRectangle(
                vector_entries,
                color=color,
                buff=0.08,
            )
            output_box = SurroundingRectangle(
                rhs_entry,
                color=color,
                buff=0.08,
            )
            self.play(
                Create(row_box),
                Create(vector_box),
                Create(output_box),
                row.animate.set_color(color),
                vector_entries.animate.set_color(color),
                rhs_entry.animate.set_color(color),
                Write(product),
                run_time=1.1,
            )
            self.wait(1.0)
            self.play(
                FadeOut(row_box),
                FadeOut(vector_box),
                FadeOut(output_box),
                row.animate.set_color(WHITE),
                vector_entries.animate.set_color(WHITE),
                rhs_entry.animate.set_color(WHITE),
                run_time=0.45,
            )

        self.wait(1.6)
        return row_products

    def _build_column_view(self):
        heading = Text(
            "The same system as a column combination",
            font_size=29,
        )
        formula = MathTex(
            r"x\begin{bmatrix}1\\2\\1\end{bmatrix}"
            r"+y\begin{bmatrix}1\\-1\\2\end{bmatrix}"
            r"+z\begin{bmatrix}1\\1\\-1\end{bmatrix}"
            r"=\begin{bmatrix}3\\2\\2\end{bmatrix}",
            font_size=38,
        )
        formula.set_color_by_tex("x", BLUE)
        formula.set_color_by_tex("y", GREEN)
        formula.set_color_by_tex("z", RED)
        formula.scale_to_fit_width(11.6)
        group = VGroup(heading, formula).arrange(DOWN, buff=0.58)
        group.move_to(DOWN * 0.12)
        heading.move_to(group[0])
        formula.move_to(group[1])
        return heading, formula, group

    def _build_conclusion(self):
        line_one = Text(
            "The entries of x are coefficients.",
            font_size=31,
        )
        equation = MathTex(
            r"x\mathbf{a}_1+y\mathbf{a}_2+z\mathbf{a}_3=\mathbf{b}",
            font_size=46,
        )
        line_two = Text(
            "Solving A x = b means finding those coefficients.",
            font_size=31,
        )
        group = VGroup(line_one, equation, line_two).arrange(DOWN, buff=0.38)
        group.scale_to_fit_width(11.5)
        group.move_to(DOWN * 0.10)
        return group
