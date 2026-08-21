"""Manim presentation for solving a first-order system with eigenvectors."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    Arrow, Axes, FadeIn, FadeOut, MathTex, ReplacementTransform,
    Scene, Text, VGroup,
)

from engine.first_order_system_eigenvectors import FirstOrderSystemEigenvectorsLesson

DOWN=np.array([0.0,-1.0,0.0]); UP=np.array([0.0,1.0,0.0]); LEFT=np.array([-1.0,0.0,0.0]); RIGHT=np.array([1.0,0.0,0.0])


class FirstOrderSystemEigenvectorsPresentation(Scene):
    CHAPTER_BANNER="EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE="Solving a First-Order System with Eigenvectors"

    def _heading(self,text:str)->Text:
        item=Text(text,font_size=27,color=WHITE)
        if item.width>11.7: item.scale_to_fit_width(11.7)
        return item

    def _chrome(self,heading_text:str):
        banner=Text(self.CHAPTER_BANNER,font_size=22,color=GREY_B,weight="BOLD").to_edge(UP,buff=0.16)
        title=Text(self.LESSON_TITLE,font_size=32,color=YELLOW,weight="BOLD").next_to(banner,DOWN,buff=0.12)
        heading=self._heading(heading_text).next_to(title,DOWN,buff=0.17)
        return banner,title,heading

    def _replace_heading(self,old:Text,text:str)->Text:
        new=self._heading(text).move_to(old)
        self.play(ReplacementTransform(old,new),run_time=0.5)
        return new

    def construct(self)->None:
        lesson=FirstOrderSystemEigenvectorsLesson()
        banner,title,heading=self._chrome("Eigenvectors turn a coupled differential system into independent exponential modes.")
        self.play(FadeIn(banner),FadeIn(title),FadeIn(heading),run_time=0.8)

        # Card 1: introduce the system.
        system=MathTex(r"\mathbf x'(t)=A\mathbf x(t)",font_size=50,color=YELLOW)
        Atex=MathTex(r"A=\begin{bmatrix}3&1\\1&3\end{bmatrix}",font_size=46,color=WHITE)
        components=MathTex(
            r"\begin{cases}x_1'=3x_1+x_2\\x_2'=x_1+3x_2\end{cases}",
            font_size=42,color=WHITE,
        )
        intro=VGroup(system,Atex,components).arrange(DOWN,buff=0.5).shift(DOWN*0.2)
        self.play(FadeIn(system)); self.play(FadeIn(Atex)); self.play(FadeIn(components)); self.wait(1.4)

        # Card 2: exponential eigenvector ansatz.
        heading=self._replace_heading(heading,"Look for a solution that keeps a fixed direction while its length changes.")
        self.play(FadeOut(intro))
        ansatz=MathTex(r"\mathbf x(t)=e^{\lambda t}\mathbf v",font_size=48,color=ORANGE)
        derivative=MathTex(r"\mathbf x'(t)=\lambda e^{\lambda t}\mathbf v",font_size=44,color=WHITE)
        rhs=MathTex(r"A\mathbf x(t)=e^{\lambda t}A\mathbf v",font_size=44,color=WHITE)
        implication=MathTex(r"\lambda e^{\lambda t}\mathbf v=e^{\lambda t}A\mathbf v",font_size=43,color=YELLOW)
        eigen=MathTex(r"\boxed{A\mathbf v=\lambda\mathbf v}",font_size=50,color=GREEN_C)
        ansatz_group=VGroup(ansatz,derivative,rhs,implication,eigen).arrange(DOWN,buff=0.38).shift(DOWN*0.12)
        for item in ansatz_group: self.play(FadeIn(item),run_time=0.45)
        self.wait(1.5)

        # Card 3: use known eigenpairs.
        heading=self._replace_heading(heading,"Each eigenpair gives one independent exponential solution.")
        self.play(FadeOut(ansatz_group))
        q1=MathTex(r"\mathbf q_1=\frac1{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\quad \lambda_1=4",font_size=39,color=GREEN_C)
        q2=MathTex(r"\mathbf q_2=\frac1{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix},\quad \lambda_2=2",font_size=39,color=BLUE_C)
        s1=MathTex(r"\mathbf x_1(t)=e^{4t}\mathbf q_1",font_size=43,color=GREEN_C)
        s2=MathTex(r"\mathbf x_2(t)=e^{2t}\mathbf q_2",font_size=43,color=BLUE_C)
        general=MathTex(r"\boxed{\mathbf x(t)=c_1e^{4t}\mathbf q_1+c_2e^{2t}\mathbf q_2}",font_size=43,color=YELLOW)
        modes=VGroup(q1,q2,s1,s2,general).arrange(DOWN,buff=0.36).shift(DOWN*0.08)
        for item in modes: self.play(FadeIn(item),run_time=0.42)
        self.wait(1.5)

        # Card 4: impose initial condition.
        heading=self._replace_heading(heading,"Use the initial condition to determine the two mode amplitudes.")
        self.play(FadeOut(modes))
        ic=MathTex(r"\mathbf x(0)=\begin{bmatrix}2\\0\end{bmatrix}",font_size=46,color=ORANGE)
        decomp=MathTex(r"\begin{bmatrix}2\\0\end{bmatrix}=\sqrt2\,\mathbf q_1+\sqrt2\,\mathbf q_2",font_size=42,color=WHITE)
        coeffs=MathTex(r"c_1=c_2=\sqrt2",font_size=44,color=YELLOW)
        sol1=MathTex(r"\mathbf x(t)=\sqrt2 e^{4t}\mathbf q_1+\sqrt2 e^{2t}\mathbf q_2",font_size=41,color=WHITE)
        sol2=MathTex(r"\boxed{\mathbf x(t)=\begin{bmatrix}e^{4t}+e^{2t}\\e^{4t}-e^{2t}\end{bmatrix}}",font_size=44,color=GREEN_C)
        ivp=VGroup(ic,decomp,coeffs,sol1,sol2).arrange(DOWN,buff=0.36).scale(0.96).shift(DOWN*0.42)
        for item in ivp: self.play(FadeIn(item),run_time=0.42)
        self.wait(1.6)

        # Card 5: visualize direction of solution.
        heading=self._replace_heading(heading,"The faster exponential mode controls the long-term direction.")
        self.play(FadeOut(ivp))
        axes=Axes(x_range=[-0.15,1.2,0.5],y_range=[-0.15,1.2,0.5],x_length=5.2,y_length=5.2,tips=False)
        axes.shift(LEFT*2.6+DOWN*0.45)
        origin=axes.c2p(0,0)
        q1dir=lesson.dominant_direction()
        q1arrow=Arrow(origin,axes.c2p(*(0.95*q1dir)),buff=0,color=GREEN_C,stroke_width=6)
        q1label=MathTex(r"\mathbf q_1",font_size=32,color=GREEN_C).next_to(q1arrow.get_end(),UP,buff=0.12)
        times=[0.0,0.25,0.5,1.0]
        colors=[ORANGE,BLUE_C,WHITE,YELLOW]
        arrows=[]
        for t,color in zip(times,colors):
            d=lesson.normalized_solution_direction(t)
            arrows.append(Arrow(origin,axes.c2p(*(0.95*d)),buff=0,color=color,stroke_width=5))
        labels=VGroup(*[MathTex(fr"t={t:g}",font_size=29,color=c) for t,c in zip(times,colors)]).arrange(DOWN,aligned_edge=LEFT,buff=0.3).to_edge(RIGHT,buff=1.0).shift(DOWN*0.2)
        relation=MathTex(r"\frac{e^{2t}}{e^{4t}}=e^{-2t}\longrightarrow0",font_size=40,color=YELLOW).to_edge(RIGHT,buff=0.75).shift(UP*1.55)
        self.play(FadeIn(axes),FadeIn(q1arrow),FadeIn(q1label),FadeIn(relation))
        for a,l in zip(arrows,labels): self.play(FadeIn(a),FadeIn(l),run_time=0.42)
        self.wait(1.6)

        # Card 6: synthesis.
        heading=self._replace_heading(heading,"Eigenvectors decouple the system into scalar exponential equations.")
        self.play(FadeOut(axes),FadeOut(q1arrow),FadeOut(q1label),FadeOut(relation),*(FadeOut(a) for a in arrows),FadeOut(labels))
        coord=MathTex(r"\mathbf x(t)=Q\mathbf y(t)",font_size=45,color=WHITE)
        transformed=MathTex(r"\mathbf y'(t)=D\mathbf y(t)",font_size=46,color=YELLOW)
        scalar=MathTex(r"y_1'=4y_1,\qquad y_2'=2y_2",font_size=44,color=GREEN_C)
        payoff=Text("A coupled vector system becomes two independent scalar differential equations.",font_size=27,color=WHITE)
        final=VGroup(coord,transformed,scalar,payoff).arrange(DOWN,buff=0.52).shift(DOWN*0.1)
        self.play(FadeIn(coord)); self.play(FadeIn(transformed)); self.play(FadeIn(scalar)); self.play(FadeIn(payoff)); self.wait(2.0)
