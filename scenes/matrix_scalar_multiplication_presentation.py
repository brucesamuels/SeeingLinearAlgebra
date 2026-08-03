from __future__ import annotations
from manim import BLUE,DOWN,FadeIn,FadeOut,GREEN,MathTex,Matrix,ORANGE,RED,RIGHT,Scene,Text,UP,VGroup,Write,YELLOW
from engine.matrix_scalar_multiplication import MATRIX_SCALAR_MULTIPLICATION_LESSON, scalar_entry_steps

class MatrixScalarMultiplicationPresentation(Scene):
    TITLE="Scalar Multiplication of Matrices"
    @staticmethod
    def _matrix(data,scale=0.82):
        return Matrix([[str(v) for v in row] for row in data],h_buff=0.88,v_buff=0.64).scale(scale)
    def construct(self):
        title=Text(self.TITLE,weight="BOLD").scale(0.66).to_edge(UP,buff=0.28)
        subtitle=Text("One scalar acts on every entry").scale(0.42).next_to(title,DOWN,buff=0.16)
        self.play(Write(title),FadeIn(subtitle,shift=UP*0.1)); self.wait(0.8)
        self._show_meaning(subtitle); self._show_entrywise_example(); self._show_negative_and_zero_scalars(); self._show_properties(); self._show_transformation_connection(); self._show_reflection()
    def _show_meaning(self,subtitle):
        q=Text("What does a scalar do to a matrix?").scale(0.52).move_to(UP*1.15)
        rule=MathTex(r"(cA)_{ij}=c\,a_{ij}",color=YELLOW).scale(1.0).move_to(UP*0.1)
        e=Text("Multiply every entry by the same number.").scale(0.44).move_to(DOWN*0.95)
        s=Text("The dimensions of the matrix do not change.").scale(0.4).move_to(DOWN*1.65)
        self.play(FadeOut(subtitle),Write(q)); self.play(Write(rule)); self.play(FadeIn(e)); self.play(FadeIn(s)); self.wait(1.6); self.play(FadeOut(q),FadeOut(rule),FadeOut(e),FadeOut(s))
    def _show_entrywise_example(self):
        L=MATRIX_SCALAR_MULTIPLICATION_LESSON
        h=Text("Scale each entry",weight="BOLD").scale(0.52).move_to(UP*2.12)
        scalar=MathTex(str(L.scalar)).scale(0.95); matrix=self._matrix(L.matrix); eq=MathTex("=").scale(0.95); result=self._matrix(L.scaled_matrix)
        group=VGroup(scalar,matrix,eq,result).arrange(RIGHT,buff=0.42); group.scale_to_fit_width(10.8); group.move_to(UP*0.35)
        self.play(Write(h)); self.play(Write(scalar),FadeIn(matrix))
        me,re=matrix.get_entries(),result.get_entries(); colors=(BLUE,GREEN,ORANGE,RED)
        for i,step in enumerate(scalar_entry_steps(L.scalar,L.matrix)):
            me[i].set_color(colors[i]); re[i].set_color(colors[i]); calc=MathTex(rf"{step.scalar}({step.original_value})={step.result}",color=colors[i]).scale(0.68).move_to(DOWN*1.3)
            self.play(FadeIn(calc),run_time=0.3); self.wait(0.4); self.play(FadeOut(calc),run_time=0.2)
        self.play(Write(eq),FadeIn(result)); dims=MathTex(r"2\times2\longrightarrow2\times2",color=YELLOW).scale(0.72).move_to(DOWN*1.35); self.play(Write(dims)); self.wait(1.5); self.play(FadeOut(h),FadeOut(group),FadeOut(dims))
    def _show_negative_and_zero_scalars(self):
        L=MATRIX_SCALAR_MULTIPLICATION_LESSON
        h=Text("Negative and zero scalars",weight="BOLD").scale(0.5).move_to(UP*2.12)
        neg=VGroup(MathTex(str(L.negative_scalar)),self._matrix(L.matrix,0.72),MathTex("="),self._matrix(L.negative_scaled_matrix,0.72)).arrange(RIGHT,buff=0.34); neg.scale_to_fit_width(9.5); neg.move_to(UP*0.62)
        note=Text("A negative scalar changes every entry's sign and magnitude.").scale(0.38).next_to(neg,DOWN,buff=0.34)
        zero=MathTex(r"0A=0",color=YELLOW).scale(0.95).move_to(DOWN*1.4)
        zero_note=Text("Here 0 is the zero matrix with the same dimensions as A.").scale(0.38).move_to(DOWN*2.08)
        self.play(Write(h),FadeIn(neg)); self.play(FadeIn(note)); self.play(Write(zero)); self.play(FadeIn(zero_note)); self.wait(1.7); self.play(FadeOut(h),FadeOut(neg),FadeOut(note),FadeOut(zero),FadeOut(zero_note))
    def _show_properties(self):
        h=Text("Scalar multiplication distributes over addition",weight="BOLD").scale(0.47).move_to(UP*2.1)
        p1=MathTex(r"c(A+B)=cA+cB",color=YELLOW).scale(0.92).move_to(UP*0.8)
        p2=MathTex(r"(c+d)A=cA+dA").scale(0.88).move_to(DOWN*0.15)
        p3=MathTex(r"c(dA)=(cd)A").scale(0.88).move_to(DOWN*1.05)
        note=Text("These laws work entry by entry.").scale(0.4).move_to(DOWN*1.9)
        self.play(Write(h)); self.play(Write(p1)); self.play(Write(p2)); self.play(Write(p3)); self.play(FadeIn(note)); self.wait(1.7); self.play(FadeOut(h),FadeOut(p1),FadeOut(p2),FadeOut(p3),FadeOut(note))
    def _show_transformation_connection(self):
        h=Text("What happens to the transformation?",weight="BOLD").scale(0.49).move_to(UP*2.1)
        formula=MathTex(r"(cA)\mathbf{x}=c(A\mathbf{x})",color=YELLOW).scale(0.95).move_to(UP*0.45)
        e=Text("Scaling the matrix scales every output vector by c.").scale(0.42).move_to(DOWN*0.55)
        b=Text("Next: A x as a combination of the columns of A.").scale(0.4).move_to(DOWN*1.35)
        self.play(Write(h)); self.play(Write(formula)); self.play(FadeIn(e)); self.play(FadeIn(b)); self.wait(1.8); self.play(FadeOut(h),FadeOut(formula),FadeOut(e),FadeOut(b))
    def _show_reflection(self):
        p=Text("Pause and Predict",weight="BOLD",color=YELLOW).scale(0.52).move_to(UP*1.65)
        q=Text("What is the lower-right entry of −3A?").scale(0.47).move_to(UP*0.78)
        example=VGroup(MathTex("A="),self._matrix(((2,1),(-4,5)),0.7)).arrange(RIGHT,buff=0.2).move_to(DOWN*0.2)
        a=MathTex(r"-3(5)=-15",color=GREEN).scale(0.9).move_to(DOWN*1.45)
        self.play(Write(p),FadeIn(q),FadeIn(example)); self.wait(2.2); self.play(Write(a)); self.wait(1.2); self.play(FadeOut(p),FadeOut(q),FadeOut(example),FadeOut(a))
        r=Text("A scalar multiplies every entry of a matrix.",weight="BOLD").scale(0.5).move_to(UP*0.6)
        u=Text("The matrix keeps the same dimensions.").scale(0.43).move_to(DOWN*0.05)
        n=Text("Next: matrix–vector multiplication as a column combination.").scale(0.41).move_to(DOWN*0.82)
        self.play(Write(r)); self.play(FadeIn(u)); self.play(FadeIn(n)); self.wait(2.0)
