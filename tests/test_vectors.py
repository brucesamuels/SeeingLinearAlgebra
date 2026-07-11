from manim import Create, FadeIn
from engine.scene_tools import SeeingScene
from engine.vectors import Vector, LinearCombination
from engine.visuals.vector_2d import VectorVisual2D
from engine.theme import VECTOR_1, VECTOR_2, COMBINATION

class VectorEngineSmokeTest(SeeingScene):
    def construct(self):
        v, w = Vector([3,2]), Vector([-1,1])
        c = LinearCombination([(1,v),(2,w)]).value
        visuals = [
            VectorVisual2D(v, r"\mathbf v", VECTOR_1),
            VectorVisual2D(w, r"\mathbf w", VECTOR_2),
            VectorVisual2D(c, r"\mathbf v+2\mathbf w", COMBINATION),
        ]
        for obj in visuals:
            self.play(Create(obj.arrow), FadeIn(obj.label))
        self.wait(1)
