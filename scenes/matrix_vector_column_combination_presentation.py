from __future__ import annotations
import numpy as np
from manim import *
from engine.matrix_vector_column_combination import evaluate_matrix_vector_column_combination

class MatrixVectorColumnCombinationPresentation(Scene):
    def construct(self):
        s = evaluate_matrix_vector_column_combination()

        title = Text("Matrix–Vector Multiplication", font_size=40).to_edge(UP)
        subtitle = Text(
            "A matrix combines its columns using the entries of the vector.",
            font_size=24,
        ).next_to(title, DOWN, buff=.16)
        self.play(FadeIn(title), FadeIn(subtitle))

        symbolic = self.show_symbolic_product(s)

        prompt = VGroup(
            Text("Pause and Predict", font_size=30, color=YELLOW),
            Text("What role do the entries 2 and 1 play?", font_size=24),
        ).arrange(DOWN, buff=.12).to_edge(DOWN).shift(UP*.10)
        self.play(FadeIn(prompt)); self.wait(2); self.play(FadeOut(prompt))

        formula = self.reveal_column_combination(s, symbolic)
        geometry = self.show_geometric_combination(s, symbolic, formula)
        self.show_conclusion(geometry)

    def show_symbolic_product(self, s):
        matrix = Matrix(
            [["1","-1"],["2","1"]],
            element_to_mobject_config={"font_size":32},
            h_buff=1.10, v_buff=.75,
        )
        entries = matrix.get_entries()
        entries[0].set_color(BLUE); entries[2].set_color(BLUE)
        entries[1].set_color(GREEN); entries[3].set_color(GREEN)

        vector = Matrix([["2"],["1"]], element_to_mobject_config={"font_size":32})
        vector_entries = vector.get_entries()
        vector_entries[0].set_color(BLUE)
        vector_entries[1].set_color(GREEN)

        equation = VGroup(
            MathTex(r"A\mathbf x=", font_size=38),
            matrix,
            vector,
        ).arrange(RIGHT, buff=.16).shift(UP*.35)

        self.play(FadeIn(equation))
        self.wait(1.2)
        return equation

    def reveal_column_combination(self, s, symbolic):
        formula = MathTex(
            r"A\mathbf x="
            r"2\begin{bmatrix}1\\2\end{bmatrix}"
            r"+"
            r"1\begin{bmatrix}-1\\1\end{bmatrix}",
            font_size=42,
        ).next_to(symbolic, DOWN, buff=.50)

        formula.set_color_by_tex(r"2\begin{bmatrix}1\\2\end{bmatrix}", BLUE)
        formula.set_color_by_tex(r"1\begin{bmatrix}-1\\1\end{bmatrix}", GREEN)

        note = Text(
            "The vector entries become coefficients.",
            font_size=27,
            color=YELLOW,
        ).next_to(formula, DOWN, buff=.20)

        self.play(FadeIn(formula))
        self.play(FadeIn(note))
        self.wait(1.5)
        return VGroup(formula, note)

    def show_geometric_combination(self, s, symbolic, formula):
        self.play(FadeOut(symbolic), FadeOut(formula))

        plane = NumberPlane(
            x_range=(-4,4,1), y_range=(-3,6,1),
            x_length=7.4, y_length=5.4,
            background_line_style={"stroke_opacity":.28},
        ).shift(LEFT*.65 + DOWN*.45)
        self.play(Create(plane))

        z = np.zeros(2)
        first = self.arrow(plane, z, s.first_contribution, BLUE, 7)
        second = self.arrow(plane, s.first_contribution, s.reconstructed, GREEN, 7)
        result = self.arrow(plane, z, s.product, YELLOW, 9)

        l1 = MathTex(r"2\mathbf a_1", color=BLUE, font_size=30).next_to(first.get_center(), LEFT, buff=.10)
        l2 = MathTex(r"1\mathbf a_2", color=GREEN, font_size=30).next_to(second.get_center(), RIGHT, buff=.10)
        lr = MathTex(r"A\mathbf x", color=YELLOW, font_size=32).next_to(result.get_end(), RIGHT+UP, buff=.10)

        identity = MathTex(
            r"A\mathbf x=2\mathbf a_1+1\mathbf a_2",
            font_size=34,
        ).to_corner(RIGHT+UP).shift(LEFT*.35+DOWN*1.38)
        identity.set_color_by_tex(r"2\mathbf a_1", BLUE)
        identity.set_color_by_tex(r"1\mathbf a_2", GREEN)

        self.play(FadeIn(identity))
        self.play(GrowArrow(first), FadeIn(l1))
        self.play(GrowArrow(second), FadeIn(l2))
        self.play(GrowArrow(result), FadeIn(lr))

        dot = Dot(plane.c2p(float(s.product[0]), float(s.product[1])), radius=.09, color=WHITE)
        note = Text(
            "The column combination lands exactly at Ax.",
            font_size=27,
            color=GREEN,
        ).to_edge(DOWN).shift(UP*.10)

        self.play(Flash(dot, color=WHITE), FadeIn(dot), FadeIn(note))
        self.wait(1.8)

        return VGroup(plane, first, second, result, l1, l2, lr, identity, dot, note)

    def show_conclusion(self, geometry):
        self.play(FadeOut(geometry))

        heading = Text(
            "Matrix–vector multiplication is a column combination",
            font_size=34,
        )
        general = MathTex(
            r"\begin{bmatrix}\vert&\vert\\"
            r"\mathbf a_1&\mathbf a_2\\"
            r"\vert&\vert\end{bmatrix}"
            r"\begin{bmatrix}x_1\\x_2\end{bmatrix}"
            r"=x_1\mathbf a_1+x_2\mathbf a_2",
            font_size=42,
        )
        general.set_color_by_tex(r"x_1\mathbf a_1", BLUE)
        general.set_color_by_tex(r"x_2\mathbf a_2", GREEN)

        conclusion = Text(
            "The entries of x tell us how much of each column to use.",
            font_size=28,
            color=YELLOW,
        )
        bridge = Text(
            "Next: the row–column rule computes the same result entry by entry.",
            font_size=25,
            color=GREEN,
        )

        group = VGroup(heading, general, conclusion, bridge).arrange(DOWN, buff=.42)
        panel = SurroundingRectangle(group, buff=.40, color=WHITE)
        self.play(FadeIn(VGroup(panel, group)))
        self.wait(3.2)

    def arrow(self, plane, start, end, color, width):
        return Arrow(
            plane.c2p(float(start[0]), float(start[1])),
            plane.c2p(float(end[0]), float(end[1])),
            buff=0, color=color, stroke_width=width,
            max_tip_length_to_length_ratio=.16,
        )
