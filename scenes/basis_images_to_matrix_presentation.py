from __future__ import annotations
import numpy as np
from manim import *
from engine.basis_images_to_matrix import evaluate_basis_images_to_matrix

class BasisImagesToMatrixPresentation(Scene):
    def construct(self):
        s = evaluate_basis_images_to_matrix()

        title = Text("From Basis Images to a Matrix", font_size=40).to_edge(UP)
        subtitle = Text(
            "The matrix is already hidden inside the transformed basis.",
            font_size=24,
        ).next_to(title, DOWN, buff=.16)
        self.play(FadeIn(title), FadeIn(subtitle))

        plane = NumberPlane(
            x_range=(-4,4,1), y_range=(-3,3,1),
            x_length=7.8, y_length=5.1,
            background_line_style={"stroke_opacity":.28},
        ).shift(LEFT*1.2 + DOWN*.48)
        self.play(Create(plane))

        images = self.show_basis_images(plane, s)
        coords = self.read_coordinates(plane, s)

        prompt = VGroup(
            Text("Pause and Predict", font_size=30, color=YELLOW),
            Text("How should these two coordinate columns be organized?", font_size=24),
        ).arrange(DOWN, buff=.12).to_edge(DOWN).shift(UP*.08)
        self.play(FadeIn(prompt)); self.wait(2); self.play(FadeOut(prompt))

        matrix_group = self.assemble_matrix(coords)
        explanation = self.explain_columns(plane, images, coords, matrix_group)

        self.play(FadeOut(explanation))
        self.final_card()

    def p(self, plane, v):
        return plane.c2p(float(v[0]), float(v[1]))

    def vector_arrow(self, plane, v, color):
        return Arrow(
            plane.c2p(0,0), self.p(plane,v), buff=0, color=color,
            stroke_width=7, max_tip_length_to_length_ratio=.16,
        )

    def show_basis_images(self, plane, s):
        a = self.vector_arrow(plane, s.te1, BLUE)
        b = self.vector_arrow(plane, s.te2, GREEN)
        la = MathTex(r"T(\mathbf e_1)", color=BLUE, font_size=30).next_to(a.get_end(), RIGHT, buff=.08)
        lb = MathTex(r"T(\mathbf e_2)", color=GREEN, font_size=30).next_to(b.get_end(), LEFT, buff=.08)
        heading = Text(
            "Everything is encoded in these two vectors.",
            font_size=25,
        ).to_corner(RIGHT+UP).shift(LEFT*.2+DOWN*1.28)
        self.play(FadeIn(heading))
        self.play(GrowArrow(a), GrowArrow(b), FadeIn(la), FadeIn(lb))
        self.wait(1)
        return VGroup(heading,a,b,la,lb)

    def read_coordinates(self, plane, s):
        x1,y1=s.te1
        x2,y2=s.te2
        guides = VGroup(
            DashedLine(self.p(plane,s.te1), self.p(plane,[x1,0]), color=BLUE, stroke_opacity=.55),
            DashedLine(self.p(plane,s.te1), self.p(plane,[0,y1]), color=BLUE, stroke_opacity=.55),
            DashedLine(self.p(plane,s.te2), self.p(plane,[x2,0]), color=GREEN, stroke_opacity=.55),
            DashedLine(self.p(plane,s.te2), self.p(plane,[0,y2]), color=GREEN, stroke_opacity=.55),
        )

        c1 = Matrix([[self.fmt(x1)],[self.fmt(y1)]], element_to_mobject_config={"font_size":28})
        c2 = Matrix([[self.fmt(x2)],[self.fmt(y2)]], element_to_mobject_config={"font_size":28})
        g1 = VGroup(MathTex(r"T(\mathbf e_1)=",font_size=29,color=BLUE),c1).arrange(RIGHT,buff=.1)
        g2 = VGroup(MathTex(r"T(\mathbf e_2)=",font_size=29,color=GREEN),c2).arrange(RIGHT,buff=.1)
        readout = VGroup(g1,g2).arrange(DOWN,buff=.35,aligned_edge=LEFT).to_corner(RIGHT+UP).shift(LEFT*.15+DOWN*1.72)

        self.play(Create(guides[0]), Create(guides[1]), FadeIn(g1))
        self.wait(.7)
        self.play(Create(guides[2]), Create(guides[3]), FadeIn(g2))
        self.wait(1)
        return VGroup(guides,readout)

    def assemble_matrix(self, coords):
        first_column = coords[1][0][1]
        second_column = coords[1][1][1]

        assembled_matrix = Matrix(
            [
                [self.fmt(1.15), self.fmt(0.55)],
                [self.fmt(-0.20), self.fmt(1.05)],
            ],
            element_to_mobject_config={"font_size": 29},
            h_buff=1.05,
            v_buff=0.72,
        )

        entries = assembled_matrix.get_entries()
        entries[0].set_color(BLUE)
        entries[2].set_color(BLUE)
        entries[1].set_color(GREEN)
        entries[3].set_color(GREEN)

        label = MathTex(r"A=", font_size=34)
        matrix_display = VGroup(
            label,
            assembled_matrix,
        ).arrange(RIGHT, buff=0.12)

        matrix_display.to_edge(DOWN).shift(UP * 0.34)

        first_target = VGroup(entries[0], entries[2])
        second_target = VGroup(entries[1], entries[3])

        self.play(
            TransformFromCopy(first_column.get_entries(), first_target),
            TransformFromCopy(second_column.get_entries(), second_target),
            FadeIn(assembled_matrix.get_brackets()),
            FadeIn(label),
        )

        message = Text(
            "The transformed basis vectors become the columns.",
            font_size=27,
            color=YELLOW,
        ).next_to(matrix_display, UP, buff=.18)

        self.play(FadeIn(message))
        self.wait(1.5)

        return VGroup(matrix_display, message)

    def explain_columns(self, plane, images, coords, matrix_group):
        self.play(
            FadeOut(plane),
            FadeOut(images),
            FadeOut(coords),
            FadeOut(matrix_group),
        )
        self.wait(0.35)

        symbolic_matrix = Matrix(
            [
                [self.fmt(1.15), self.fmt(0.55)],
                [self.fmt(-0.20), self.fmt(1.05)],
            ],
            element_to_mobject_config={"font_size": 31},
            h_buff=1.05,
            v_buff=0.72,
        )

        entries = symbolic_matrix.get_entries()
        entries[0].set_color(BLUE)
        entries[2].set_color(BLUE)
        entries[1].set_color(GREEN)
        entries[3].set_color(GREEN)

        matrix_display = VGroup(
            MathTex(r"A=", font_size=36),
            symbolic_matrix,
        ).arrange(RIGHT, buff=0.14)

        heading = Text(
            "Why these vectors become columns",
            font_size=32,
        )

        decomposition = MathTex(
            r"\mathbf x=x_1\mathbf e_1+x_2\mathbf e_2",
            font_size=37,
        )

        transformed = MathTex(
            r"T(\mathbf x)=x_1T(\mathbf e_1)+x_2T(\mathbf e_2)",
            font_size=37,
        )

        note = Text(
            "Every output is a linear combination of the two columns.",
            font_size=26,
            color=YELLOW,
        )

        symbolic_screen = VGroup(
            heading,
            matrix_display,
            decomposition,
            transformed,
            note,
        ).arrange(DOWN, buff=0.34).shift(DOWN * 0.15)

        self.play(FadeIn(heading))
        self.play(FadeIn(matrix_display))
        self.play(FadeIn(decomposition), FadeIn(transformed))
        self.play(FadeIn(note))
        self.wait(4.0)

        return symbolic_screen

    def final_card(self):
        group = VGroup(
            Text("The matrix records the basis images",font_size=35),
            MathTex(
                r"A=\begin{bmatrix}\vert&\vert\\T(\mathbf e_1)&T(\mathbf e_2)\\\vert&\vert\end{bmatrix}",
                font_size=40,
            ),
            Text("The first column is T(e₁). The second column is T(e₂).",font_size=27,color=YELLOW),
            Text("The columns of a matrix are the images of the basis vectors.",font_size=28,color=GREEN),
            Text("Next: matrix-vector multiplication combines those columns.",font_size=26),
        ).arrange(DOWN,buff=.37)
        panel = SurroundingRectangle(group,buff=.38,color=WHITE)
        self.play(FadeIn(VGroup(panel,group))); self.wait(3)

    @staticmethod
    def fmt(value):
        r=round(float(value),2)
        return str(int(r)) if abs(r-round(r))<1e-9 else f"{r:.2f}"
