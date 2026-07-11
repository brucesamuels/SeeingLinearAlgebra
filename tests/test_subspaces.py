from manim import Create, FadeIn, MathTex
from engine.scene_tools import SeeingScene
from engine.vectors import Vector
from engine.subspaces import Subspace
from engine.visuals.vector_2d import VectorVisual2D
from engine.visuals.subspace_visuals import SpanLineVisual, SpanPlaneVisual
from engine.theme import VECTOR_1, VECTOR_2, COMBINATION, TEXT

class SubspaceEngineSmokeTest(SeeingScene):
    def construct(self):
        v1, v2 = Vector([2,1]), Vector([-1,2])
        full = Subspace([v1,v2])
        plane = SpanPlaneVisual(full)
        a = VectorVisual2D(v1, r"\mathbf v_1", VECTOR_1)
        b = VectorVisual2D(v2, r"\mathbf v_2", VECTOR_2)
        self.play(Create(plane), Create(a.arrow), FadeIn(a.label))
        self.play(Create(b.arrow), FadeIn(b.label))
        self.play(FadeIn(MathTex(r"\operatorname{rank}=2", color=TEXT).to_corner("UR")))
        dep = Subspace([Vector([2,1]), Vector([4,2])])
        self.play(Create(SpanLineVisual(dep, 2.5, COMBINATION)))
        self.wait(1)
