from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "positive_definite_elimination_test_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_connects_elimination_pivots_to_completed_squares():
    assert r"R_2\leftarrow R_2-\frac12R_1" in TEXT
    assert r"p_1=2" in TEXT
    assert r"p_2=\frac32" in TEXT
    assert r"2\left(x_1+\frac12x_2\right)^2+\frac32x_2^2" in TEXT


def test_scene_has_pause_and_predict_beat():
    assert "Pause: if the next pivot were zero or negative" in TEXT


def test_scene_uses_leading_principal_minors_and_ratio_rule():
    assert "leading principal minors" in TEXT.lower()
    assert r"\Delta_1=2" in TEXT
    assert r"\Delta_2=\det" in TEXT
    assert 'MathTex(r"=3"' in TEXT
    assert r"p_k=\frac{\Delta_k}{\Delta_{k-1}}" in TEXT


def test_scene_defines_leading_principal_minors_with_a_three_by_three_example():
    assert r"B_k=\text{the upper-left }k\times k\text{ block}" in TEXT
    assert r"\Delta_k=\det(B_k)" in TEXT
    assert "These determinants are the leading principal minors." in TEXT
    assert '[["4", "2", "0"], ["2", "3", "1"], ["0", "1", "2"]]' in TEXT
    assert r"\Delta_1=4" in TEXT
    assert r"\Delta_2=8" in TEXT
    assert r"\Delta_3=12" in TEXT
    assert r"p_3=\frac{12}{8}=\frac32" in TEXT


def test_scene_states_both_symmetric_positive_definite_tests():
    assert r"A=A^T\ \text{is positive definite}" in TEXT
    assert r"p_1,p_2,\ldots,p_n>0" in TEXT
    assert r"\Delta_1,\Delta_2,\ldots,\Delta_n>0" in TEXT


def test_scene_stays_within_approved_scope():
    forbidden = ("LDL", "Cholesky", "factorization")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP202" not in TEXT
