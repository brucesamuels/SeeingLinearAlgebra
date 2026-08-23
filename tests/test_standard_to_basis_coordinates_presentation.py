from pathlib import Path

SCENE_PATH = Path("scenes/standard_to_basis_coordinates_presentation.py")


def source():
    return SCENE_PATH.read_text(encoding="utf-8")


def test_identity_and_no_student_facing_checkpoint_number():
    text = source()
    assert 'CHAPTER_BANNER = "CHANGE OF BASIS"' in text
    assert 'LESSON_TITLE = "From Standard Coordinates to Basis Coordinates"' in text
    assert "CP190" not in text and "CHAPTER 8" not in text


def test_opening_problem_and_direction_are_explicit():
    text = source()
    assert "How do we translate a vector's standard coordinates" in text
    assert "into coordinates in a nonstandard basis?" in text
    assert r"[\mathbf v]_{\mathcal E}\xrightarrow{\qquad ?\qquad}[\mathbf v]_{\mathcal B}" in text


def test_vector_remains_fixed_while_grid_and_label_change():
    text = source()
    assert text.count("vector = Arrow") == 1
    assert "Transform(standard_grid, basis_grid, rate_func=smooth)" in text
    assert "basis_grid = self._basis_grid(plane)" in text
    assert "ReplacementTransform(vector" not in text
    assert r"[\mathbf v]_{\mathcal E}=(4,2)" in text
    assert r"[\mathbf v]_{\mathcal B}=(3,1)" in text


def test_grid_is_pronounced_and_entire_grid_is_transformed():
    text = source()
    assert "def _standard_grid(plane):" in text
    assert "def _basis_grid(plane):" in text
    assert "stroke_width=3.2 if is_axis else 1.8" in text
    assert "stroke_opacity=1.0 if is_axis else 0.88" in text
    assert "plane.c2p(x - 3, x + 3), plane.c2p(x + 5, x - 5)" in text
    assert "plane.c2p(-2 + y, -2 - y), plane.c2p(6 + y, 6 - y)" in text
    assert "run_time=4.0" in text


def test_inverse_formula_and_detailed_numerical_example():
    text = source()
    assert r"\boxed{[\mathbf v]_{\mathcal B}=P_{\mathcal B}^{-1}[\mathbf v]_{\mathcal E}}" in text
    assert r"\det(P_{\mathcal B})=-2" in text
    assert r"1(4)+1(2)" in text
    assert r"1(4)+(-1)(2)" in text
    assert r"\begin{bmatrix}3\\1\end{bmatrix}" in text


def test_large_math_and_safe_full_width_cards():
    text = source()
    assert "font_size=66, color=YELLOW" in text
    assert "font_size=65, color=YELLOW" in text
    assert "group.scale_to_fit_width(11.2)" in text
