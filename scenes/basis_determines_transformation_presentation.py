from __future__ import annotations
import numpy as np
from manim import *
from engine.basis_determines_transformation import evaluate_basis_determination

class BasisDeterminesTransformationPresentation(Scene):
    def construct(self):
        s = evaluate_basis_determination()

        title = Text("A Basis Determines the Transformation", font_size=40).to_edge(UP)
        subtitle = Text(
            "Know the images of the basis vectors, and every other image follows.",
            font_size=24,
        ).next_to(title, DOWN, buff=.16)
        self.play(FadeIn(title), FadeIn(subtitle))

        plane = NumberPlane(
            x_range=(-4,4,1), y_range=(-3,3,1),
            x_length=8.2, y_length=5.2,
            background_line_style={"stroke_opacity":.28},
        ).shift(LEFT*.65 + DOWN*.5)
        self.play(Create(plane))

        basis = self.show_basis(plane, s)
        original = self.show_x(plane, s, basis)

        prompt = VGroup(
            Text("Pause and Predict", font_size=30, color=YELLOW),
            Text("Can T(x) be predicted from T(e₁) and T(e₂)?", font_size=24),
        ).arrange(DOWN, buff=.12).to_edge(DOWN).shift(UP*.08)
        self.play(FadeIn(prompt)); self.wait(2); self.play(FadeOut(prompt))

        images = self.show_basis_images(plane, s, basis)
        retained = self.show_direct_image(plane, s, original)

        note = Text(
            "Retain T(x). Rebuild it from the transformed basis.",
            font_size=24, color=GREY_B,
        ).to_edge(DOWN).shift(UP*.08)
        self.play(FadeIn(note)); self.wait(.8)
        self.play(FadeOut(basis), FadeOut(original), FadeOut(images[0]), FadeOut(note))

        rebuilt = self.rebuild_image(plane, s, retained)
        self.play(FadeOut(retained), FadeOut(rebuilt))
        second = self.second_example(plane, s)
        self.wait(1)

        self.play(FadeOut(plane), FadeOut(images[1:]), FadeOut(second))
        self.final_card()

    def p(self, plane, v):
        return plane.c2p(float(v[0]), float(v[1]))

    def arrow(self, plane, start, end, color, width=6):
        return Arrow(
            self.p(plane,start), self.p(plane,end), buff=0,
            color=color, stroke_width=width,
            max_tip_length_to_length_ratio=.16,
        )

    def show_basis(self, plane, s):
        z=np.zeros(2)
        e1=self.arrow(plane,z,s.e1,BLUE)
        e2=self.arrow(plane,z,s.e2,GREEN)
        l1=MathTex(r"\mathbf e_1",color=BLUE,font_size=30).next_to(e1.get_end(),DOWN,buff=.08)
        l2=MathTex(r"\mathbf e_2",color=GREEN,font_size=30).next_to(e2.get_end(),LEFT,buff=.08)
        self.play(GrowArrow(e1),GrowArrow(e2),FadeIn(l1),FadeIn(l2))
        return VGroup(e1,e2,l1,l2)

    def show_x(self, plane, s, basis):
        z=np.zeros(2)
        a=self.arrow(plane,z,2*s.e1,BLUE)
        b=self.arrow(plane,2*s.e1,s.x,GREEN)
        x=self.arrow(plane,z,s.x,YELLOW,8)
        la=MathTex(r"2\mathbf e_1",color=BLUE,font_size=28).next_to(a.get_center(),DOWN,buff=.08)
        lb=MathTex(r"\mathbf e_2",color=GREEN,font_size=28).next_to(b.get_center(),RIGHT,buff=.08)
        lx=MathTex(r"\mathbf x=2\mathbf e_1+\mathbf e_2",color=YELLOW,font_size=29).next_to(x.get_end(),RIGHT+UP,buff=.1)
        self.play(TransformFromCopy(basis[0],a),FadeIn(la))
        self.play(TransformFromCopy(basis[1],b),FadeIn(lb))
        self.play(GrowArrow(x),FadeIn(lx)); self.wait(1)
        return VGroup(a,b,x,la,lb,lx)

    def show_basis_images(self, plane, s, basis):
        heading=Text("Transform the basis vectors",font_size=26).to_corner(RIGHT+UP).shift(LEFT*.3+DOWN*1.25)
        a=self.arrow(plane,np.zeros(2),s.te1,BLUE,7)
        b=self.arrow(plane,np.zeros(2),s.te2,GREEN,7)
        la=MathTex(r"T(\mathbf e_1)",color=BLUE,font_size=29).next_to(a.get_end(),RIGHT,buff=.08)
        lb=MathTex(r"T(\mathbf e_2)",color=GREEN,font_size=29).next_to(b.get_end(),LEFT,buff=.08)
        self.play(FadeIn(heading))
        self.play(TransformFromCopy(basis[0],a),TransformFromCopy(basis[1],b),FadeIn(la),FadeIn(lb))
        return VGroup(heading,a,b,la,lb)

    def show_direct_image(self, plane, s, original):
        a=self.arrow(plane,np.zeros(2),s.tx,ORANGE,9)
        l=MathTex(r"T(\mathbf x)",color=ORANGE,font_size=31).next_to(a.get_end(),LEFT+DOWN,buff=.1)
        self.play(TransformFromCopy(original[2],a),FadeIn(l)); self.wait(1.8)
        return VGroup(a,l)

    def rebuild_image(self, plane, s, retained):
        z=np.zeros(2)
        a=self.arrow(plane,z,2*s.te1,BLUE)
        b=self.arrow(plane,2*s.te1,s.rebuilt_tx,GREEN)
        r=self.arrow(plane,z,s.rebuilt_tx,YELLOW,7)
        la=MathTex(r"2T(\mathbf e_1)",color=BLUE,font_size=28).next_to(a.get_center(),DOWN,buff=.08)
        lb=MathTex(r"T(\mathbf e_2)",color=GREEN,font_size=28).next_to(b.get_center(),RIGHT,buff=.08)
        lr=MathTex(r"2T(\mathbf e_1)+T(\mathbf e_2)",color=YELLOW,font_size=28).next_to(r.get_end(),RIGHT+UP,buff=.1)
        self.play(GrowArrow(a),FadeIn(la))
        self.play(GrowArrow(b),FadeIn(lb))
        self.play(GrowArrow(r),FadeIn(lr))
        dot=Dot(self.p(plane,s.rebuilt_tx),color=WHITE,radius=.09)
        msg=Text("The reconstruction lands exactly at T(x).",font_size=27,color=GREEN).to_edge(DOWN).shift(UP*.08)
        self.play(Flash(dot,color=WHITE),FadeIn(dot),FadeIn(msg)); self.wait(1.4); self.play(FadeOut(msg))
        return VGroup(a,b,r,la,lb,lr,dot)

    def second_example(self, plane, s):
        c=np.array([-1.,2.])
        x=c[0]*s.e1+c[1]*s.e2
        tx=s.matrix@x
        rebuilt=c[0]*s.te1+c[1]*s.te2
        a=self.arrow(plane,np.zeros(2),tx,ORANGE,8)
        b=self.arrow(plane,np.zeros(2),rebuilt,YELLOW,6)
        la=MathTex(r"T(-\mathbf e_1+2\mathbf e_2)",color=ORANGE,font_size=28).next_to(a.get_end(),LEFT+DOWN,buff=.1)
        lb=MathTex(r"-T(\mathbf e_1)+2T(\mathbf e_2)",color=YELLOW,font_size=27).next_to(b.get_end(),RIGHT+UP,buff=.1)
        self.play(GrowArrow(a),FadeIn(la)); self.wait(.7)
        self.play(GrowArrow(b),FadeIn(lb))
        d=Dot(self.p(plane,tx),color=WHITE,radius=.085)
        self.play(Flash(d,color=WHITE),FadeIn(d))
        return VGroup(a,b,la,lb,d)

    def final_card(self):
        group=VGroup(
            Text("The basis images determine every output",font_size=34),
            MathTex(r"\mathbf x=x_1\mathbf e_1+x_2\mathbf e_2",font_size=39),
            MathTex(r"T(\mathbf x)=x_1T(\mathbf e_1)+x_2T(\mathbf e_2)",font_size=42,color=YELLOW),
            Text("A linear transformation is completely determined by its action on a basis.",font_size=27,color=GREEN),
            Text("Next: those basis images become the columns of a matrix.",font_size=26),
        ).arrange(DOWN,buff=.36)
        panel=SurroundingRectangle(group,buff=.38,color=WHITE)
        self.play(FadeIn(VGroup(panel,group))); self.wait(3)
