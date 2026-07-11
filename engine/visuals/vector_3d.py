from manim import Arrow3D, MathTex, VGroup
from engine.theme import TEXT, VECTOR_1
from engine.vectors import Vector

class VectorVisual3D(VGroup):
    def __init__(self, vector: Vector, label=r"\mathbf{v}", color=VECTOR_1):
        if vector.dimension != 3:
            raise ValueError("VectorVisual3D requires a vector in R^3.")
        end = list(vector.components)
        arrow = Arrow3D(start=[0,0,0], end=end, color=color)
        tex = MathTex(label, color=TEXT).scale(0.7).move_to(end).shift([.25,.25,.25])
        self.vector, self.arrow, self.label = vector, arrow, tex
        super().__init__(arrow, tex)
