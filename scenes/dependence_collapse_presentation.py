"""Checkpoint 70: dependence as geometric collapse."""
from __future__ import annotations
import numpy as np
from manim import Arrow, Create, DecimalNumber, DOWN, FadeIn, FadeOut, LEFT, MathTex, NumberPlane, RIGHT, Scene, Text, UP, ValueTracker, VGroup, linear
from engine.dependence_collapse import DependenceCollapse
from engine.manim_dependence_collapse import ManimDependenceCollapse

QUESTION="Does every second vector create a plane?"
PREDICT="What happens when the two directions become the same?"
KEY="A new vector enlarges the span only when it adds a new direction."
DEPENDENCE="The vectors are linearly dependent."
BG="#0A0D13"; GRID="#3A4256"; TEXT="#E8EAED"; MUTED="#9AA4B2"; U="#5DADE2"; V="#AF7AC5"; FIELD="#55D6BE"; ACCENT="#4FC3F7"

class DependenceCollapsePresentation(Scene):
    def construct(self)->None:
        self.camera.background_color=BG
        model=DependenceCollapse(np.array([2.2,0.55]),np.array([-0.45,1.8]))
        progress=ValueTracker(0.0)
        plane=NumberPlane(x_range=(-7,7,1),y_range=(-4,4,1),x_length=12.5,y_length=7.0,background_line_style={"stroke_color":GRID,"stroke_width":1,"stroke_opacity":0.35},axis_config={"stroke_color":MUTED}).shift(DOWN*0.2)
        map_point=lambda x: plane.c2p(*x)
        pairs=np.array([(a,b) for a in np.linspace(-2.8,2.8,15) for b in np.linspace(-2.8,2.8,15)],dtype=float)
        snap=model.snapshot(0.0)
        display=ManimDependenceCollapse(snap,map_point,model.endpoints_for(0.0,pairs),u_kwargs={"color":U,"stroke_width":7},v_kwargs={"color":V,"stroke_width":7},polygon_kwargs={"color":FIELD,"fill_color":FIELD,"fill_opacity":0.20,"stroke_width":2},dot_kwargs={"color":FIELD,"radius":0.022,"fill_opacity":0.55,"stroke_width":0})
        display.mobject.add_updater(lambda _m: display.update(model.snapshot(progress.get_value()),model.endpoints_for(progress.get_value(),pairs)))
        title=Text(QUESTION,font_size=38,color=TEXT).to_edge(UP,buff=0.32)
        predict=VGroup(Text("PAUSE AND PREDICT",font_size=20,color=ACCENT),Text(PREDICT,font_size=28,color=TEXT)).arrange(DOWN,buff=0.12).to_corner(UP+LEFT,buff=0.5).shift(DOWN*0.7)
        area_label=MathTex(r"\text{relative area}=",font_size=30,color=TEXT); area=DecimalNumber(1.0,num_decimal_places=2,font_size=30,color=FIELD); area.add_updater(lambda n:n.set_value(model.snapshot(progress.get_value()).area_ratio)); readout=VGroup(area_label,area).arrange(RIGHT,buff=0.1).to_corner(UP+RIGHT,buff=0.5).shift(DOWN*0.6)
        u_label=MathTex(r"\mathbf u",font_size=36,color=U).move_to(map_point(np.array([2.2,0.55]))+DOWN*0.25)
        v_label=MathTex(r"\mathbf v",font_size=36,color=V)
        v_label.add_updater(lambda m:m.move_to(map_point(model.snapshot(progress.get_value()).generator_v)+LEFT*0.25))
        self.play(FadeIn(title),Create(plane)); self.play(FadeIn(display.mobject),FadeIn(u_label),FadeIn(v_label),FadeIn(readout)); self.wait(1.0)
        self.play(FadeIn(predict)); self.wait(2.3); self.play(FadeOut(predict))
        self.play(progress.animate.set_value(0.88),run_time=5.0,rate_func=linear); self.wait(0.8)
        almost=Text("The plane is losing a direction.",font_size=28,color=MUTED).to_edge(DOWN,buff=0.35)
        self.play(FadeIn(almost)); self.wait(1.5); self.play(FadeOut(almost))
        self.play(progress.animate.set_value(1.0),run_time=2.0,rate_func=linear)
        display.mobject.clear_updaters(); area.clear_updaters(); v_label.clear_updaters()
        final=model.snapshot(1.0); display.update(final,model.endpoints_for(1.0,pairs)); area.set_value(0.0); v_label.move_to(map_point(final.generator_v)+UP*0.25)
        equation=MathTex(r"\mathbf v=c\mathbf u",font_size=40,color=TEXT).to_edge(DOWN,buff=0.75)
        dependence=Text(DEPENDENCE,font_size=30,color=ACCENT).next_to(equation,UP,buff=0.22)
        key=Text(KEY,font_size=26,color=MUTED).next_to(dependence,UP,buff=0.22)
        self.play(FadeIn(equation)); self.play(FadeIn(dependence)); self.play(FadeIn(key)); self.wait(2.8)
