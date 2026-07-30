"""CP83: Which Transformations Are Linear?"""
from __future__ import annotations
import numpy as np
from manim import *
from engine.linearity_tests import evaluate_linearity, radial_nonlinear, shear, translation
class WhichTransformationsAreLinearPresentation(Scene):
    def construct(self):
        title=Text("Which Transformations Are Linear?",font_size=42).to_edge(UP)
        subtitle=Text("A transformation must preserve the structure of vector space.",font_size=24).next_to(title,DOWN,buff=.18)
        self.play(FadeIn(title),FadeIn(subtitle)); self.wait(1.2)
        plane=NumberPlane(x_range=(-4,4,1),y_range=(-3,3,1),x_length=8.2,y_length=5.2,background_line_style={"stroke_opacity":.35}).shift(DOWN*.35)
        self.play(Create(plane))
        origin=Dot(plane.c2p(0,0),color=RED,radius=.075); origin_label=MathTex(r"\mathbf{0}",font_size=30).next_to(origin,DOWN+LEFT,buff=.08)
        self.play(FadeIn(origin),FadeIn(origin_label))
        self.origin_test(plane,origin); self.homogeneity_test(plane); self.additivity_test(plane); self.final_definition(plane,origin,origin_label)
    def pt(self,plane,v): return plane.c2p(float(v[0]),float(v[1]))
    def header(self,tex,caption):
        g=VGroup(MathTex(tex,font_size=38),Text(caption,font_size=23)).arrange(DOWN,buff=.12)
        return g.to_corner(LEFT+UP).shift(RIGHT*.35+DOWN*1.25)
    def status(self,text,color):
        label=Text(text,font_size=25,color=color); return VGroup(SurroundingRectangle(label,buff=.14,color=color),label).to_corner(RIGHT+UP).shift(LEFT*.35+DOWN*1.4)
    def origin_test(self,plane,origin):
        h=self.header(r"T(\mathbf{0})=\mathbf{0}","Every linear transformation fixes the origin."); self.play(FadeIn(h)); self.wait(1)
        s=evaluate_linearity("Translation",translation); t0=Dot(self.pt(plane,s.origin_image),color=YELLOW,radius=.085); t0l=MathTex(r"T(\mathbf{0})",font_size=30).next_to(t0,RIGHT,buff=.1)
        d=Arrow(origin.get_center(),t0.get_center(),buff=.08,color=YELLOW); name=Text("Translation",font_size=29,color=YELLOW).next_to(h,DOWN,buff=.35); fail=self.status("Fails immediately",RED)
        self.play(FadeIn(name),GrowArrow(d),FadeIn(t0),FadeIn(t0l)); self.play(FadeIn(fail)); self.wait(1.5); self.play(FadeOut(VGroup(name,d,t0,t0l,fail)))
        name2=Text("Origin-fixing nonlinear map",font_size=28,color=ORANGE).next_to(h,DOWN,buff=.35); passes=self.status("Passes this test only",ORANGE)
        self.play(FadeIn(name2),FadeIn(passes)); self.wait(1.2)
        warning=Text("Fixing the origin is necessary—but not sufficient.",font_size=27,color=ORANGE).to_edge(DOWN).shift(UP*.25)
        self.play(FadeIn(warning)); self.wait(1.6); self.play(FadeOut(VGroup(h,name2,passes,warning)))
    def homogeneity_test(self,plane):
        h=self.header(r"T(c\mathbf{v})=cT(\mathbf{v})","Scaling before or after gives the same result."); self.play(FadeIn(h))
        v=np.array([1.25,.75]); c=1.7; lin=evaluate_linearity("Shear",shear,vector=v,scalar=c); non=evaluate_linearity("Radial",radial_nonlinear,vector=v,scalar=c)
        base=Arrow(plane.c2p(0,0),self.pt(plane,v),buff=0,color=BLUE); a=Arrow(plane.c2p(0,0),self.pt(plane,lin.homogeneity_left),buff=0,color=GREEN); b=Arrow(plane.c2p(0,0),self.pt(plane,lin.homogeneity_right),buff=0,color=YELLOW); label=Text("Shear: the two paths meet",font_size=27,color=GREEN).to_edge(DOWN)
        transformed_base=base.copy(); self.play(GrowArrow(base)); self.play(Transform(transformed_base,a),GrowArrow(b),FadeIn(label)); self.wait(1.4); self.play(FadeOut(VGroup(base,transformed_base,b,label)))
        a2=Arrow(plane.c2p(0,0),self.pt(plane,non.homogeneity_left),buff=0,color=ORANGE); b2=Arrow(plane.c2p(0,0),self.pt(plane,non.homogeneity_right),buff=0,color=YELLOW); bad=Text("Nonlinear map: the endpoints separate",font_size=27,color=RED).to_edge(DOWN)
        self.play(GrowArrow(a2),GrowArrow(b2),FadeIn(bad)); self.wait(1.5); self.play(FadeOut(VGroup(h,a2,b2,bad)))
    def additivity_test(self,plane):
        h=self.header(r"T(\mathbf{u}+\mathbf{v})=T(\mathbf{u})+T(\mathbf{v})","Adding before or after gives the same result."); self.play(FadeIn(h))
        u=np.array([-.65,1.]); v=np.array([1.35,.55]); result=evaluate_linearity("Shear",shear,vector=v,other=u); tu,tv=shear(u),shear(v)
        ua=Arrow(plane.c2p(0,0),self.pt(plane,tu),buff=0,color=BLUE); va=Arrow(self.pt(plane,tu),self.pt(plane,tu+tv),buff=0,color=GREEN); direct=Arrow(plane.c2p(0,0),self.pt(plane,result.additivity_left),buff=0,color=YELLOW); cap=Text("The transformed parallelogram still closes.",font_size=27,color=GREEN).to_edge(DOWN)
        self.play(GrowArrow(ua),GrowArrow(va)); self.play(GrowArrow(direct),FadeIn(cap)); self.wait(1.7); self.play(FadeOut(VGroup(h,ua,va,direct,cap)))
    def final_definition(self,plane,origin,origin_label):
        self.play(FadeOut(VGroup(plane,origin,origin_label)))
        heading=Text("A transformation is linear when both rules hold:",font_size=31)
        equations=VGroup(MathTex(r"T(c\mathbf{v})=cT(\mathbf{v})",font_size=42),MathTex(r"T(\mathbf{u}+\mathbf{v})=T(\mathbf{u})+T(\mathbf{v})",font_size=42)).arrange(DOWN,buff=.32)
        conclusion=Text("Linear transformations preserve every linear combination.",font_size=28,color=YELLOW)
        group=VGroup(heading,equations,conclusion).arrange(DOWN,buff=.42); panel=SurroundingRectangle(group,buff=.35,color=WHITE)
        self.play(FadeIn(VGroup(panel,group))); self.wait(2.5)
