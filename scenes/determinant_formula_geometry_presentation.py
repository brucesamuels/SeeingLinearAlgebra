"""CP131: true encasing rectangle and visual shoelace derivation."""
from __future__ import annotations
import numpy as np
from manim import (
    BLUE, GREEN, GREY_B, ORANGE, RED, WHITE, YELLOW,
    Axes, DashedLine, FadeIn, FadeOut, Line, MathTex, Matrix,
    Polygon, Rectangle, Scene, Text, VGroup, Write,
)
from engine.determinant_formula_geometry import build_symbolic_derivation, final_statement


class DeterminantFormulaGeometryPresentation(Scene):
    def construct(self) -> None:
        data = build_symbolic_derivation()
        title = Text("Where Does ad - bc Come From?", font_size=42)
        title.to_edge(np.array([0., 1., 0.]), buff=0.28)
        subtitle = Text("Two generalized-coordinate pictures.", font_size=25, color=GREY_B)
        subtitle.next_to(title, np.array([0., -1., 0.]), buff=0.14)
        self.play(Write(title), FadeIn(subtitle))

        # Representative geometry carrying generalized labels.
        axes = Axes(
            x_range=[-0.4, 4.6, 1], y_range=[-0.4, 3.7, 1],
            x_length=6.2, y_length=4.9, tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(np.array([-3.2, -0.55, 0.]))
        O = np.array([0., 0.]); U = np.array([3., 1.]); V = np.array([1., 2.]); W = U + V
        para = self.poly(axes, [O, U, W, V], ORANGE, 0.34)
        bounding = Rectangle(
            width=axes.c2p(4,0)[0]-axes.c2p(0,0)[0],
            height=axes.c2p(0,3)[1]-axes.c2p(0,0)[1],
            color=YELLOW, stroke_width=4,
        ).move_to((axes.c2p(0,0)+axes.c2p(4,3))/2)
        self.play(FadeIn(axes), FadeIn(para))
        labels = VGroup(
            MathTex(r"(0,0)", font_size=27).move_to(axes.c2p(-.05,-.27)),
            MathTex(r"(a,c)", font_size=29, color=GREEN).move_to(axes.c2p(3.25,.75)),
            MathTex(r"(a+b,c+d)", font_size=29, color=YELLOW).move_to(axes.c2p(4.05,3.35)),
            MathTex(r"(b,d)", font_size=29, color=BLUE).move_to(axes.c2p(.6,2.35)),
        )
        self.play(FadeIn(labels))

        method1 = Text("Method 1: Encasement", font_size=29).move_to(np.array([3.15,2.25,0.]))
        self.play(FadeIn(method1), FadeIn(bounding))

        # Six exterior pieces exactly filling the bounding rectangle outside the parallelogram.
        pieces = [
            self.poly(axes, [[0,0],[3,0],[3,1]], RED, .20),          # ac/2
            self.poly(axes, [[3,0],[4,0],[4,1],[3,1]], RED, .20),    # bc
            self.poly(axes, [[3,1],[4,1],[4,3]], RED, .20),          # bd/2
            self.poly(axes, [[0,0],[0,2],[1,2]], RED, .20),          # bd/2
            self.poly(axes, [[0,2],[1,2],[1,3],[0,3]], RED, .20),    # bc
            self.poly(axes, [[1,2],[1,3],[4,3]], RED, .20),          # ac/2
        ]
        piece_labels = VGroup(
            MathTex(r"\frac{ac}{2}", font_size=24, color=RED).move_to(axes.c2p(2.2,.25)),
            MathTex(r"bc", font_size=24, color=RED).move_to(axes.c2p(3.5,.45)),
            MathTex(r"\frac{bd}{2}", font_size=24, color=RED).move_to(axes.c2p(3.72,1.75)),
            MathTex(r"\frac{bd}{2}", font_size=24, color=RED).move_to(axes.c2p(.25,1.25)),
            MathTex(r"bc", font_size=24, color=RED).move_to(axes.c2p(.45,2.55)),
            MathTex(r"\frac{ac}{2}", font_size=24, color=RED).move_to(axes.c2p(2.2,2.72)),
        )
        guides = VGroup(
            DashedLine(axes.c2p(3,0), axes.c2p(3,1), color=GREY_B),
            DashedLine(axes.c2p(4,1), axes.c2p(3,1), color=GREY_B),
            DashedLine(axes.c2p(0,2), axes.c2p(1,2), color=GREY_B),
            DashedLine(axes.c2p(1,3), axes.c2p(1,2), color=GREY_B),
        )
        self.play(*[FadeIn(p) for p in pieces], FadeIn(guides), FadeIn(piece_labels))

        arithmetic = VGroup(
            MathTex(r"A_{\rm box}=(a+b)(c+d)", font_size=30, color=YELLOW),
            MathTex(r"A_{\rm outside}=\frac{ac}{2}+bc+\frac{bd}{2}+\frac{bd}{2}+bc+\frac{ac}{2}", font_size=27, color=RED),
            MathTex(r"=ac+bd+2bc", font_size=29, color=RED),
            MathTex(r"A_{\rm para}=(a+b)(c+d)-(ac+bd+2bc)", font_size=29),
            MathTex(r"=ad-bc", font_size=38, color=YELLOW),
        ).arrange(np.array([0.,-1.,0.]), buff=.15).move_to(np.array([3.15,-1.05,0.]))
        for line in arithmetic:
            self.play(FadeIn(line))
        self.wait(1.4)

        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (title,)])

        # Shoelace as a coordinate array with repeated first row and crossed diagonals.
        method2 = Text("Method 2: Shoelace / Green's Formula", font_size=29).move_to(np.array([0.,2.45,0.]))
        self.play(FadeIn(method2))
        rows = [("0","0"),("a","c"),("a+b","c+d"),("b","d"),("0","0")]
        x_header = MathTex("x", font_size=30, color=WHITE).move_to(np.array([-2.6,1.75,0.]))
        y_header = MathTex("y", font_size=30, color=WHITE).move_to(np.array([-.7,1.75,0.]))
        entries = []
        y_positions = [1.2,.45,-.3,-1.05,-1.8]
        for (xv,yv), ypos in zip(rows,y_positions):
            xmob = MathTex(xv, font_size=31).move_to(np.array([-2.6,ypos,0.]))
            ymob = MathTex(yv, font_size=31).move_to(np.array([-.7,ypos,0.]))
            entries.append((xmob,ymob))
        coord_group = VGroup(x_header,y_header,*[m for pair in entries for m in pair])
        self.play(FadeIn(coord_group))

        green_lines = VGroup(*[
            Line(entries[i][0].get_right()+np.array([.08,0,0]), entries[i+1][1].get_left()-np.array([.08,0,0]), color=GREEN, stroke_width=4)
            for i in range(4)
        ])
        red_lines = VGroup(*[
            Line(entries[i][1].get_left()-np.array([.08,0,0]), entries[i+1][0].get_right()+np.array([.08,0,0]), color=RED, stroke_width=4)
            for i in range(4)
        ])
        self.play(FadeIn(green_lines))
        forward = MathTex(r"0c+a(c+d)+(a+b)d+b0=ac+2ad+bd", font_size=29, color=GREEN)
        forward.move_to(np.array([3.0,.8,0.]))
        self.play(FadeIn(forward))
        self.play(FadeIn(red_lines))
        backward = MathTex(r"0a+c(a+b)+(c+d)b+d0=ac+2bc+bd", font_size=29, color=RED)
        backward.move_to(np.array([3.0,-.2,0.]))
        self.play(FadeIn(backward))
        result = VGroup(
            MathTex(r"A=\frac12(\text{green}-\text{red})", font_size=30),
            MathTex(r"=\frac12[(ac+2ad+bd)-(ac+2bc+bd)]", font_size=29),
            MathTex(r"=ad-bc", font_size=40, color=YELLOW),
        ).arrange(np.array([0.,-1.,0.]), buff=.18).move_to(np.array([3.0,-1.45,0.]))
        for line in result:
            self.play(FadeIn(line))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in list(self.mobjects)])
        final_formula = MathTex(r"\det\!\begin{bmatrix}a&b\\c&d\end{bmatrix}=ad-bc", font_size=47, color=YELLOW)
        closing = Text(final_statement(), font_size=29, color=WHITE).scale_to_fit_width(11.5)
        closing.next_to(final_formula, np.array([0.,-1.,0.]), buff=.5)
        self.play(Write(final_formula), FadeIn(closing))
        self.wait(2.5)

    @staticmethod
    def poly(axes: Axes, vertices, color, opacity):
        return Polygon(*[axes.c2p(float(x),float(y)) for x,y in vertices], color=color, stroke_width=3, fill_color=color, fill_opacity=opacity)
