from manim import Arrow, MathTex, VGroup, ORIGIN, UP
from engine.theme import TEXT, VECTOR_1
from engine.vectors import Vector

class VectorVisual2D(VGroup):
    def __init__(self, vector: Vector, label=r"\mathbf{v}", color=VECTOR_1):
        if vector.dimension != 2:
            raise ValueError("VectorVisual2D requires a vector in R^2.")
        end = [vector.components[0], vector.components[1], 0]
        arrow = Arrow(ORIGIN, end, buff=0, color=color)
        tex = MathTex(label, color=TEXT).scale(0.8).next_to(arrow.get_end(), UP)
        self.vector, self.arrow, self.label = vector, arrow, tex
        super().__init__(arrow, tex)
