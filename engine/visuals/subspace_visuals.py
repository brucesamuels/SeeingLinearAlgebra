from manim import Line, NumberPlane, VGroup
from engine.theme import COMBINATION, GRID
from engine.subspaces import Subspace

class SpanLineVisual(VGroup):
    def __init__(self, subspace: Subspace, extent=6.0, color=COMBINATION):
        if subspace.dimension != 1:
            raise ValueError("A one-dimensional subspace is required.")
        d = subspace.basis[0].components
        if subspace.ambient_dimension == 2:
            start, end = [-extent*d[0],-extent*d[1],0], [extent*d[0],extent*d[1],0]
        elif subspace.ambient_dimension == 3:
            start, end = list(-extent*d), list(extent*d)
        else:
            raise ValueError("Direct line display is supported only in R^2 or R^3.")
        self.line = Line(start, end, color=color)
        self.subspace = subspace
        super().__init__(self.line)

class SpanPlaneVisual(NumberPlane):
    def __init__(self, subspace: Subspace, **kwargs):
        if subspace.ambient_dimension != 2 or subspace.dimension != 2:
            raise ValueError("This visual currently represents full R^2.")
        super().__init__(background_line_style={
            "stroke_color": GRID, "stroke_width": 1, "stroke_opacity": .5
        }, **kwargs)
        self.subspace = subspace
