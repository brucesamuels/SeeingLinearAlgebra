from pathlib import Path
SCENE = Path("scenes/transformation_matrix_basis_presentation.py")
def source(): return SCENE.read_text(encoding="utf-8")


def test_identity_and_no_chapter_number():
    text = source()
    assert 'CHAPTER_BANNER = "CHANGE OF BASIS"' in text
    assert 'LESSON_TITLE = "The Matrix of a Transformation in Another Basis"' in text
    assert "CP192" not in text


def test_pipeline_and_similarity_formula():
    text = source()
    assert r"[\mathbf v]_{\mathcal B}" in text
    assert r"\xrightarrow{\quad P_{\mathcal B}\quad}\mathbf v" in text
    assert r"\xrightarrow{\quad A\quad}A\mathbf v" in text
    assert r"\xrightarrow{\quad P_{\mathcal B}^{-1}\quad}[A\mathbf v]_{\mathcal B}" in text
    assert r"\boxed{[A]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}}" in text


def test_geometry_distinguishes_real_motion_from_coordinate_change():
    text = source()
    assert r"\mathbf v=(3,2)" in text
    assert r"A\mathbf v=(6,2)" in text
    assert "Transform(vector, transformed_vector)" in text
    assert "The transformation genuinely moves the vector." in text


def test_same_transformation_is_shown_on_the_b_grid():
    text = source()
    assert "Transform(standard_grid, basis_grid, rate_func=smooth)" in text
    assert "run_time=4.0" in text
    assert r"(3,2)_{\mathcal E}" in text
    assert r"(6,2)_{\mathcal E}" in text
    assert r"(1,2)_{\mathcal B}" in text
    assert r"(4,2)_{\mathcal B}" in text
    assert r"[A]_{\mathcal B}:(1,2)_{\mathcal B}\longmapsto(4,2)_{\mathcal B}" in text
    assert "ReplacementTransform(input_vector" not in text


def test_structural_matrices_and_numerical_verification():
    text = source()
    assert r"\begin{bmatrix}" not in text
    assert 'self._matrix([["2", "1"], ["0", "1"]]' in text
    assert 'self._matrix([["4"], ["2"]]' in text
    assert r"(1,2)_{\mathcal B}\leftrightarrow(3,2)" in text
    assert "v_buff=0.95" in text
