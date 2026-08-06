from pathlib import Path
SCENE=Path("scenes/determinant_formula_geometry_presentation.py")
def source(): return SCENE.read_text(encoding="utf-8")

def test_scene_class(): assert "class DeterminantFormulaGeometryPresentation(Scene):" in source()

def test_true_bounding_rectangle():
    t=source(); assert "axes.c2p(4,0)" in t and "axes.c2p(0,3)" in t
    assert "width=axes.c2p(4,0)" in t

def test_six_exterior_pieces_and_arithmetic():
    t=source(); assert r"\frac{ac}{2}+bc+\frac{bd}{2}+\frac{bd}{2}+bc+\frac{ac}{2}" in t
    assert r"(a+b)(c+d)-(ac+bd+2bc)" in t

def test_generalized_vertex_labels():
    t=source()
    for token in [r"(0,0)",r"(a,c)",r"(a+b,c+d)",r"(b,d)"]: assert token in t

def test_shoelace_coordinate_array_and_cross_lines():
    t=source(); assert 'rows = [("0","0"),("a","c"),("a+b","c+d"),("b","d"),("0","0")]' in t
    assert "green_lines = VGroup" in t and "red_lines = VGroup" in t
    assert "Line(entries[i][0]" in t and "Line(entries[i][1]" in t

def test_shoelace_arithmetic():
    t=source(); assert r"0c+a(c+d)+(a+b)d+b0=ac+2ad+bd" in t
    assert r"0a+c(a+b)+(c+d)b+d0=ac+2bc+bd" in t
    assert r"=ad-bc" in t

def test_safe_fade():
    t=source(); assert "*[FadeOut(m) for m in list(self.mobjects)]" in t
    assert "VGroup(*self.mobjects)" not in t


def test_red_shoelace_lines_stop_before_coordinate_glyphs():
    t=source()
    assert "entries[i][1].get_left()-np.array([.08,0,0])" in t
    assert "entries[i+1][0].get_right()+np.array([.08,0,0])" in t
    assert "entries[i][1].get_right()+np.array([.08,0,0])" not in t
    assert "entries[i+1][0].get_left()-np.array([.08,0,0])" not in t
