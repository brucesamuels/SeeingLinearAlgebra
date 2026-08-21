"""Manim presentation for the Chapter 7 eigenvalues/eigenvectors review."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    FadeIn, FadeOut, MathTex, ReplacementTransform, Scene, Text, VGroup,
)

from engine.eigenvalues_chapter_review import EigenvaluesChapterReview

DOWN=np.array([0.0,-1.0,0.0]); UP=np.array([0.0,1.0,0.0]); LEFT=np.array([-1.0,0.0,0.0]); RIGHT=np.array([1.0,0.0,0.0])


class EigenvaluesChapterReviewPresentation(Scene):
    CHAPTER_BANNER="EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE="Chapter Review"

    def _heading(self,text:str)->Text:
        item=Text(text,font_size=27,color=WHITE)
        if item.width>11.7: item.scale_to_fit_width(11.7)
        return item

    def _chrome(self,heading_text:str):
        banner=Text(self.CHAPTER_BANNER,font_size=22,color=GREY_B,weight="BOLD").to_edge(UP,buff=0.16)
        title=Text(self.LESSON_TITLE,font_size=32,color=YELLOW,weight="BOLD").next_to(banner,DOWN,buff=0.12)
        heading=self._heading(heading_text).next_to(title,DOWN,buff=0.17)
        return banner,title,heading

    def _replace_heading(self,old,text:str):
        new=self._heading(text).move_to(old)
        self.play(ReplacementTransform(old,new),run_time=0.5)
        return new

    def _stack(self,*items,buff=0.42,shift=0.0,scale=1.0):
        group=VGroup(*items).arrange(DOWN,buff=buff)
        if scale!=1.0: group.scale(scale)
        group.shift(DOWN*shift)
        return group

    def construct(self)->None:
        review=EigenvaluesChapterReview()
        assert len(review.topics())==6
        banner,title,heading=self._chrome("One idea connects the entire chapter: choose coordinates adapted to the transformation.")
        self.play(FadeIn(banner),FadeIn(title),FadeIn(heading),run_time=0.8)

        # Card 1: chapter map.
        row1=VGroup(
            Text("special directions",font_size=28,color=ORANGE),
            MathTex(r"\longrightarrow",font_size=34,color=GREY_B),
            Text("eigenpairs",font_size=28,color=GREEN_C),
            MathTex(r"\longrightarrow",font_size=34,color=GREY_B),
            Text("eigenspaces",font_size=28,color=BLUE_C),
        ).arrange(RIGHT,buff=0.28)
        row2=VGroup(
            Text("eigenbasis",font_size=28,color=ORANGE),
            MathTex(r"\longrightarrow",font_size=34,color=GREY_B),
            Text("diagonalization",font_size=28,color=GREEN_C),
            MathTex(r"\longrightarrow",font_size=34,color=GREY_B),
            Text("applications",font_size=28,color=BLUE_C),
        ).arrange(RIGHT,buff=0.28)
        map_group=VGroup(row1,row2).arrange(DOWN,buff=0.75).shift(DOWN*0.1)
        self.play(FadeIn(row1)); self.play(FadeIn(row2)); self.wait(1.4)

        # Card 2: finding eigenvalues/eigenvectors/eigenspaces.
        heading=self._replace_heading(heading,"Finding eigenvectors means solving a null-space problem.")
        self.play(FadeOut(map_group))
        definition=MathTex(r"A\mathbf v=\lambda\mathbf v,\qquad \mathbf v\ne\mathbf0",font_size=45,color=YELLOW)
        rearrange=MathTex(r"(A-\lambda I)\mathbf v=\mathbf0",font_size=45,color=WHITE)
        characteristic=MathTex(r"\det(A-\lambda I)=0",font_size=46,color=ORANGE)
        eigenspace=MathTex(r"E_\lambda=\operatorname{Null}(A-\lambda I)",font_size=46,color=GREEN_C)
        card2=self._stack(definition,rearrange,characteristic,eigenspace,buff=0.48,shift=0.15)
        for item in card2: self.play(FadeIn(item),run_time=0.42)
        self.wait(1.5)

        # Card 3: diagonalization and powers.
        heading=self._replace_heading(heading,"When eigenvectors form a basis, the transformation becomes diagonal.")
        self.play(FadeOut(card2))
        P=MathTex(r"P=[\mathbf v_1\ \cdots\ \mathbf v_n]",font_size=43,color=WHITE)
        D=MathTex(r"D=P^{-1}AP",font_size=45,color=ORANGE)
        factor=MathTex(r"\boxed{A=PDP^{-1}}",font_size=50,color=YELLOW)
        powers=MathTex(r"\boxed{A^k=PD^kP^{-1}}",font_size=48,color=GREEN_C)
        card3=self._stack(P,D,factor,powers,buff=0.48,shift=0.15)
        for item in card3: self.play(FadeIn(item),run_time=0.42)
        self.wait(1.5)

        # Card 4: when diagonalization can fail.
        heading=self._replace_heading(heading,"Repeated eigenvalues are harmless if their eigenspaces are large enough.")
        self.play(FadeOut(card3))
        am=MathTex(r"\text{algebraic multiplicity}=\text{multiplicity as a root}",font_size=38,color=WHITE)
        gm=MathTex(r"\text{geometric multiplicity}=\dim E_\lambda",font_size=40,color=ORANGE)
        criterion=MathTex(r"\boxed{\sum_\lambda \dim E_\lambda=n}",font_size=50,color=YELLOW)
        note=Text("Diagonalizable means: enough independent eigenvectors to form a basis.",font_size=28,color=GREEN_C)
        card4=self._stack(am,gm,criterion,note,buff=0.50,shift=0.16,scale=0.96)
        for item in card4: self.play(FadeIn(item),run_time=0.42)
        self.wait(1.5)

        # Card 5: symmetric matrices and spectral theorem.
        heading=self._replace_heading(heading,"Real symmetric matrices give the best possible eigenvector basis.")
        self.play(FadeOut(card4))
        symmetry=MathTex(r"A^T=A",font_size=48,color=WHITE)
        orthogonal=MathTex(r"\lambda_i\ne\lambda_j\quad\Longrightarrow\quad \mathbf q_i^T\mathbf q_j=0",font_size=42,color=GREEN_C)
        qtq=MathTex(r"Q^TQ=I\qquad\Longrightarrow\qquad Q^{-1}=Q^T",font_size=43,color=ORANGE)
        spectral=MathTex(r"\boxed{A=QDQ^T}",font_size=52,color=YELLOW)
        card5=self._stack(symmetry,orthogonal,qtq,spectral,buff=0.48,shift=0.16)
        for item in card5: self.play(FadeIn(item),run_time=0.42)
        self.wait(1.5)

        # Card 6: applications and final synthesis.
        heading=self._replace_heading(heading,"Eigenvector coordinates separate coupled behavior into independent modes.")
        self.play(FadeOut(card5))
        dynamics=MathTex(r"A^k\mathbf x=\sum_i c_i\lambda_i^k\mathbf v_i",font_size=42,color=WHITE)
        ode=MathTex(r"\mathbf x'=A\mathbf x\quad\Longrightarrow\quad \mathbf y'=D\mathbf y",font_size=42,color=GREEN_C)
        fib=MathTex(r"\mathbf x_{n+1}=A\mathbf x_n\quad\Longrightarrow\quad \mathbf x_n=A^n\mathbf x_0",font_size=41,color=ORANGE)
        takeaway=MathTex(r"\boxed{\text{Choose an eigenvector basis, and the transformation separates into scalar modes.}}",font_size=36,color=YELLOW)
        card6=self._stack(dynamics,ode,fib,takeaway,buff=0.52,shift=0.18,scale=0.96)
        for item in card6: self.play(FadeIn(item),run_time=0.45)
        self.wait(2.0)
