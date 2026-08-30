from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "least_squares_uniqueness_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_reuses_cp205_matrix_and_clean_normal_equations():
    assert '[["1", "0"], ["1", "1"], ["0", "1"]]' in TEXT
    assert '[["2", "1"], ["1", "2"]]' in TEXT
    assert '[["3"], ["3"]]' in TEXT
    assert r"\boxed{A^TA\widehat x=A^Tb}" in TEXT


def test_scene_has_pause_and_positive_definite_uniqueness_chain():
    assert "Pause: why must this system have exactly one solution?" in TEXT
    assert "Positive definiteness makes the normal-equation matrix invertible." in TEXT
    assert r"\operatorname{null}(A^TA)=\{0\}" in TEXT
    assert r"\widehat x=(1,1)^T" in TEXT


def test_scene_verifies_residual_orthogonality():
    assert r"r=b-A\widehat x=" in TEXT
    assert r"A^Tr=" in TEXT
    assert '[["1"], ["-1"], ["1"]]' in TEXT
    assert '[["0"], ["0"]]' in TEXT


def test_scene_contrasts_dependent_columns_and_nonunique_coefficients():
    assert '[["1", "2"], ["1", "2"], ["0", "0"]]' in TEXT
    assert r"Bx_1=Bx_2=(3,3,0)^T" in TEXT
    assert r"z=(-2,1)^T,\qquad Bz=0" in TEXT
    assert r"B(x+tz)=Bx+tBz=Bx" in TEXT
    assert "No unique coefficient vector" in TEXT


def test_scene_states_final_full_rank_result_and_stays_in_scope():
    assert r"A\ \text{has full column rank}" in TEXT
    assert r"\widehat x\ \text{is the unique least-squares coefficient vector}" in TEXT
    forbidden = ("covariance", "pseudoinverse", "condition number", "gradient descent")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP206" not in TEXT
