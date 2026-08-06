from pathlib import Path

def source() -> str:
    return Path("scenes/determinant_orientation_presentation.py").read_text(encoding="utf-8")

def test_scene_class_exists():
    assert "class DeterminantOrientationPresentation(Scene):" in source()

def test_scene_shows_positive_and_negative_determinants():
    text = source()
    assert r"\det(A)=+2" in text
    assert r"\det(B)=-2" in text

def test_scene_compares_equal_area_magnitudes():
    assert r"|\det(A)|=|\det(B)|=2" in source()

def test_scene_uses_orientation_language():
    text = source()
    assert "orientation preserved" in text
    assert "orientation reversed" in text

def test_square_is_transformed_in_place():
    text = source()
    assert "Transform(square, pos_poly)" in text
    assert "Transform(square, neg_poly)" in text
    assert "square.copy()" not in text

def test_scene_fades_heterogeneous_mobjects_individually():
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects)]" in text
    assert "VGroup(*self.mobjects)" not in text
