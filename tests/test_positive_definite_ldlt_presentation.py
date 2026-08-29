from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "positive_definite_ldlt_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_records_three_pivots_and_multipliers():
    assert r"p_1=4" in TEXT
    assert r"p_2=2" in TEXT
    assert r"p_3=\tfrac{3}{2}" in TEXT
    assert r"\ell_{21}=\tfrac{2}{4}=\tfrac{1}{2}" in TEXT
    assert r"\ell_{31}=0" in TEXT
    assert r"\ell_{32}=\tfrac{1}{2}" in TEXT


def test_scene_assembles_and_verifies_ldlt():
    assert r"A=LDL^T" in TEXT
    assert "model.lower_factor()" in TEXT
    assert "model.diagonal_entries()" in TEXT
    assert "model.reconstruct()" in TEXT


def test_scene_connects_factorization_to_completed_squares():
    assert r"y=L^Tx" in TEXT
    assert r"x^TAx=y^TDy" in TEXT
    assert r"4\left(x_1+\tfrac{1}{2}x_2\right)^2" in TEXT
    assert r"2\left(x_2+\tfrac{1}{2}x_3\right)^2" in TEXT
    assert r"+\tfrac{3}{2}x_3^2" in TEXT


def test_scene_has_pause_and_states_positive_diagonal_test():
    assert "Pause: which factor decides whether the energy is always positive?" in TEXT
    assert r"d_1,d_2,\ldots,d_n>0" in TEXT
    assert r"A=A^T\ \text{is positive definite}" in TEXT


def test_scene_stays_within_approved_scope():
    forbidden = ("Cholesky", "R^TR", "square root")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP203" not in TEXT
