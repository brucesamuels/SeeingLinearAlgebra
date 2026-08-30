from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "gram_matrix_definiteness_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_derives_nonnegative_gram_energy_and_defines_psd():
    assert r"x^T(A^TA)x=(Ax)^T(Ax)=\lVert Ax\rVert^2\ge0" in TEXT
    assert "positive semidefinite" in TEXT.lower()
    assert r"x^TMx\ge0\quad\text{for every }x" in TEXT
    assert "Negative Gram energy is impossible." in TEXT


def test_scene_reconnects_to_original_matrix_with_independent_columns():
    assert '[["1", "0"], ["1", "1"], ["0", "1"]]' in TEXT
    assert '[["2", "1"], ["1", "2"]]' in TEXT
    assert r"\operatorname{null}(A)=\{0\}" in TEXT


def test_scene_has_pause_and_dependent_column_zero_energy_example():
    assert "Pause: when can a nonzero vector still have zero Gram energy?" in TEXT
    assert '[["1", "2"], ["1", "2"], ["0", "0"]]' in TEXT
    assert '[["-2"], ["1"]]' in TEXT
    assert r"Bx=0" in TEXT
    assert r"x^TB^TBx=\lVert Bx\rVert^2=0" in TEXT


def test_scene_states_general_semidefinite_and_column_independence_results():
    assert r"A^TA\ \text{is always positive semidefinite}" in TEXT
    assert r"A^TA\ \text{is positive definite}" in TEXT
    assert r"A\ \text{has independent columns}" in TEXT


def test_scene_stays_within_approved_scope():
    forbidden = ("normal equation", "least squares", "covariance")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP205" not in TEXT
