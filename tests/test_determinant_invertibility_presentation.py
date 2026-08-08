from pathlib import Path
SCENE = Path("scenes/determinant_invertibility_presentation.py")

def source() -> str:
    return SCENE.read_text(encoding="utf-8")

def test_scene_class_exists() -> None:
    assert "class DeterminantInvertibilityPresentation(Scene):" in source()

def test_scene_shows_nonzero_determinant_example() -> None:
    text = source()
    assert "A nonzero determinant signals invertibility" in text
    assert "invertible_example()" in text
    assert "invertible_determinant()" in text
    assert "A is invertible" in text

def test_scene_shows_zero_determinant_example() -> None:
    text = source()
    assert "A zero determinant signals singularity" in text
    assert "singular_example()" in text
    assert r"R_2=2R_1" in text
    assert "B cannot be inverted." in text

def test_scene_exhibits_nonzero_null_vector() -> None:
    text = source()
    assert "null_vector_equation_tex()" in text
    assert "singular_null_vector()" in text
    assert "is sent to zero" in text

def test_scene_connects_determinant_to_geometry() -> None:
    text = source()
    assert "Invertibility is also a geometric question" in text
    assert "No dimension is lost" in text
    assert "Dimension collapses" in text
    assert "volume becomes zero" in text

def test_scene_connects_pivots_rank_nullspace_and_invertibility() -> None:
    text = source()
    assert "invertible_chain_tex()" in text
    assert "singular_chain_tex()" in text
    assert "these statements are equivalent" in text

def test_scene_ends_with_square_matrix_test() -> None:
    text = source()
    assert "The determinant is an invertibility test" in text
    assert "This test applies to square matrices." in text

def test_scene_uses_safe_clear_pattern() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_scene_states_nullspace_invertibility_theorem_formally() -> None:
    text = source()
    assert "Invertibility Theorem" in text
    assert "For a square matrix A:" in text
    assert "nullspace_invertibility_theorem_tex()" in text
    assert "homogeneous_system_statement_tex()" in text
    assert "no nonzero vector can be sent to zero" in text
