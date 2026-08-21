"""Manim presentation for Fibonacci and difference equations."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    Axes, Dot, FadeIn, FadeOut, MathTex, ReplacementTransform,
    Scene, Text, VGroup,
)

from engine.fibonacci_difference_equation import FibonacciDifferenceEquationLesson

DOWN=np.array([0.0,-1.0,0.0]); UP=np.array([0.0,1.0,0.0]); LEFT=np.array([-1.0,0.0,0.0]); RIGHT=np.array([1.0,0.0,0.0])


class FibonacciDifferenceEquationPresentation(Scene):
    CHAPTER_BANNER="EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE="Fibonacci and Difference Equations"

    def _heading(self,text:str)->Text:
        item=Text(text,font_size=27,color=WHITE)
        if item.width>11.7: item.scale_to_fit_width(11.7)
        return item

    def _mixed_heading(self,left_text:str,math_text:str,right_text:str=""):
        left=Text(left_text,font_size=27,color=WHITE)
        math=MathTex(math_text,font_size=32,color=YELLOW)
        pieces=[left,math]
        if right_text:
            right=Text(right_text,font_size=27,color=WHITE)
            pieces.append(right)
        group=VGroup(*pieces).arrange(RIGHT,buff=0.14)
        if group.width>11.7:
            group.scale_to_fit_width(11.7)
        return group

    def _chrome(self,heading_text:str):
        banner=Text(self.CHAPTER_BANNER,font_size=22,color=GREY_B,weight="BOLD").to_edge(UP,buff=0.16)
        title=Text(self.LESSON_TITLE,font_size=32,color=YELLOW,weight="BOLD").next_to(banner,DOWN,buff=0.12)
        heading=self._heading(heading_text).next_to(title,DOWN,buff=0.17)
        return banner,title,heading

    def _replace_heading(self,old,text:str):
        new=self._heading(text).move_to(old)
        self.play(ReplacementTransform(old,new),run_time=0.5)
        return new

    def _replace_mixed_heading(self,old,left_text:str,math_text:str,right_text:str=""):
        new=self._mixed_heading(left_text,math_text,right_text).move_to(old)
        self.play(ReplacementTransform(old,new),run_time=0.5)
        return new

    def _stack(self,*items,buff=0.38,shift=0.0,scale=1.0):
        group=VGroup(*items).arrange(DOWN,buff=buff)
        if scale!=1.0: group.scale(scale)
        group.shift(DOWN*shift)
        return group

    def construct(self)->None:
        lesson=FibonacciDifferenceEquationLesson()
        banner,title,heading=self._chrome("A familiar recurrence can be rewritten as repeated matrix multiplication.")
        self.play(FadeIn(banner),FadeIn(title),FadeIn(heading),run_time=0.8)

        # Card 1: Fibonacci recurrence.
        recurrence=MathTex(r"F_{n+1}=F_n+F_{n-1}",font_size=52,color=YELLOW)
        initial=MathTex(r"F_0=0,\qquad F_1=1",font_size=44,color=WHITE)
        values=MathTex(r"0,\,1,\,1,\,2,\,3,\,5,\,8,\,13,\,\ldots",font_size=42,color=ORANGE)
        card1=self._stack(recurrence,initial,values,buff=0.52,shift=0.15)
        for item in card1: self.play(FadeIn(item),run_time=0.45)
        self.wait(1.4)

        # Card 2: state vector and matrix recurrence.
        heading=self._replace_heading(heading,"Store two consecutive Fibonacci numbers in one state vector.")
        self.play(FadeOut(card1))
        state=MathTex(r"\mathbf x_n=\begin{bmatrix}F_{n+1}\\F_n\end{bmatrix}",font_size=48,color=ORANGE)
        next_state=MathTex(
            r"\mathbf x_{n+1}=\begin{bmatrix}F_{n+2}\\F_{n+1}\end{bmatrix}"
            r"=\begin{bmatrix}F_{n+1}+F_n\\F_{n+1}\end{bmatrix}",
            font_size=41,color=WHITE,
        )
        matrix_rule=MathTex(
            r"\boxed{\mathbf x_{n+1}=A\mathbf x_n},\qquad "
            r"A=\begin{bmatrix}1&1\\1&0\end{bmatrix}",
            font_size=43,color=GREEN_C,
        )
        card2=self._stack(state,next_state,matrix_rule,buff=0.46,shift=0.24)
        for item in card2: self.play(FadeIn(item),run_time=0.45)
        self.wait(1.5)

        # Card 3: matrix powers.
        heading=self._replace_heading(heading,"Repeated substitution turns the recurrence into a matrix power.")
        self.play(FadeOut(card2))
        x0=MathTex(r"\mathbf x_0=\begin{bmatrix}F_1\\F_0\end{bmatrix}=\begin{bmatrix}1\\0\end{bmatrix}",font_size=45,color=ORANGE)
        chain=MathTex(
            r"\mathbf x_1=A\mathbf x_0,\quad "
            r"\mathbf x_2=A^2\mathbf x_0,\quad "
            r"\ldots,\quad "
            r"\mathbf x_n=A^n\mathbf x_0",
            font_size=40,color=WHITE,
        )
        target=MathTex(r"\boxed{\mathbf x_n=A^n\mathbf x_0}",font_size=50,color=YELLOW)
        card3=self._stack(x0,chain,target,buff=0.55,shift=0.15)
        for item in card3: self.play(FadeIn(item),run_time=0.45)
        self.wait(1.5)

        # Card 4: eigenvalues.
        heading=self._replace_mixed_heading(heading,"Diagonalizing A makes",r"A^n","easy to compute.")
        self.play(FadeOut(card3))
        char=MathTex(
            r"\det(A-\lambda I)="
            r"\begin{vmatrix}1-\lambda&1\\1&-\lambda\end{vmatrix}"
            r"=\lambda^2-\lambda-1",
            font_size=40,color=WHITE,
        )
        roots=MathTex(
            r"\lambda_{1,2}=\frac{1\pm\sqrt5}{2}",
            font_size=46,color=YELLOW,
        )
        names=MathTex(
            r"\phi=\frac{1+\sqrt5}{2},\qquad "
            r"\psi=\frac{1-\sqrt5}{2}",
            font_size=45,color=ORANGE,
        )
        card4=self._stack(char,roots,names,buff=0.55,shift=0.18)
        for item in card4: self.play(FadeIn(item),run_time=0.45)
        self.wait(1.5)

        # Card 5: eigenvectors and diagonalization.
        heading=self._replace_heading(heading,"The two eigenvalues give two independent eigendirections.")
        self.play(FadeOut(card4))
        vphi=MathTex(r"\mathbf v_\phi=\begin{bmatrix}\phi\\1\end{bmatrix}",font_size=44,color=GREEN_C)
        vpsi=MathTex(r"\mathbf v_\psi=\begin{bmatrix}\psi\\1\end{bmatrix}",font_size=44,color=BLUE_C)
        Ptex=MathTex(r"P=\begin{bmatrix}\phi&\psi\\1&1\end{bmatrix}",font_size=43,color=WHITE)
        Dtex=MathTex(r"D=\begin{bmatrix}\phi&0\\0&\psi\end{bmatrix}",font_size=43,color=YELLOW)
        diag=MathTex(r"\boxed{A=PDP^{-1}}",font_size=48,color=ORANGE)
        card5=self._stack(vphi,vpsi,Ptex,Dtex,diag,buff=0.28,shift=0.42,scale=0.92)
        for item in card5: self.play(FadeIn(item),run_time=0.42)
        self.wait(1.5)

        # Card 6: nth power.
        heading=self._replace_heading(heading,"Powers now act only on the diagonal entries.")
        self.play(FadeOut(card5))
        power=MathTex(r"A^n=PD^nP^{-1}",font_size=48,color=YELLOW)
        Dn=MathTex(r"D^n=\begin{bmatrix}\phi^n&0\\0&\psi^n\end{bmatrix}",font_size=46,color=GREEN_C)
        state_power=MathTex(r"\mathbf x_n=PD^nP^{-1}\mathbf x_0",font_size=45,color=WHITE)
        card6=self._stack(power,Dn,state_power,buff=0.58,shift=0.14)
        for item in card6: self.play(FadeIn(item),run_time=0.45)
        self.wait(1.5)

        # Card 7: derive Binet's formula.
        heading=self._replace_mixed_heading(heading,"Extracting the second component gives a closed formula for",r"F_n",".")
        self.play(FadeOut(card6))
        inverse=MathTex(
            r"P^{-1}=\frac1{\sqrt5}"
            r"\begin{bmatrix}1&-\psi\\-1&\phi\end{bmatrix}",
            font_size=42,color=WHITE,
        )
        product=MathTex(
            r"\mathbf x_n=A^n\mathbf x_0"
            r"=\frac1{\sqrt5}"
            r"\begin{bmatrix}\phi^{n+1}-\psi^{n+1}\\\phi^n-\psi^n\end{bmatrix}",
            font_size=41,color=WHITE,
        )
        binet=MathTex(
            r"\boxed{F_n=\frac{\phi^n-\psi^n}{\sqrt5}}",
            font_size=50,color=YELLOW,
        )
        card7=self._stack(inverse,product,binet,buff=0.52,shift=0.20)
        for item in card7: self.play(FadeIn(item),run_time=0.45)
        self.wait(1.6)

        # Card 8: check an actual Fibonacci number.
        heading=self._replace_heading(heading,"The closed form reproduces the exact Fibonacci numbers.")
        self.play(FadeOut(card7))
        check=MathTex(
            r"F_8=\frac{\phi^8-\psi^8}{\sqrt5}=21",
            font_size=48,color=ORANGE,
        )
        state8=MathTex(
            r"\mathbf x_8=A^8\mathbf x_0=\begin{bmatrix}34\\21\end{bmatrix}",
            font_size=46,color=WHITE,
        )
        note=Text("The matrix-power and closed-form viewpoints agree.",font_size=28,color=GREEN_C)
        card8=self._stack(check,state8,note,buff=0.62,shift=0.12)
        for item in card8: self.play(FadeIn(item),run_time=0.45)
        self.wait(1.5)

        # Card 9: dominant eigenvalue and golden ratio.
        heading=self._replace_heading(heading,"The dominant eigenvalue explains the golden-ratio limit.")
        self.play(FadeOut(card8))
        dominant=MathTex(r"|\phi|>1,\qquad |\psi|<1",font_size=46,color=YELLOW)
        vanish=MathTex(r"\psi^n\longrightarrow0",font_size=45,color=BLUE_C)
        ratio=MathTex(r"\boxed{\frac{F_{n+1}}{F_n}\longrightarrow\phi}",font_size=50,color=GREEN_C)
        ratios=MathTex(r"1,\ 2,\ 1.5,\ 1.667,\ 1.6,\ 1.625,\ldots",font_size=39,color=ORANGE)
        card9=self._stack(dominant,vanish,ratio,ratios,buff=0.48,shift=0.18)
        for item in card9: self.play(FadeIn(item),run_time=0.45)
        self.wait(1.6)

        # Card 10: synthesis.
        heading=self._replace_heading(heading,"Eigenvectors turn a recurrence into powers of independent scalar modes.")
        self.play(FadeOut(card9))
        discrete=MathTex(r"\mathbf x_{n+1}=A\mathbf x_n",font_size=46,color=WHITE)
        diagonal=MathTex(r"A=PDP^{-1}\quad\Longrightarrow\quad A^n=PD^nP^{-1}",font_size=43,color=YELLOW)
        final=MathTex(r"\boxed{F_n=\frac{\phi^n-\psi^n}{\sqrt5}}",font_size=50,color=GREEN_C)
        takeaway=Text("A famous difference equation becomes simple in an eigenvector basis.",font_size=28,color=WHITE)
        card10=self._stack(discrete,diagonal,final,takeaway,buff=0.52,shift=0.12)
        for item in card10: self.play(FadeIn(item),run_time=0.45)
        self.wait(2.0)
