from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "positive_definite_eigenvalue_test_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_has_live_directional_energy_and_extreme_directions():
    assert "ValueTracker" in TEXT
    assert "model.directional_energy(theta.get_value())" in TEXT
    assert r"q(u_+)=3" in TEXT
    assert r"q(u_-)=1" in TEXT
    assert r"1\le x^T A x\le3" in TEXT


def test_scene_connects_eigenvectors_to_quadratic_energy():
    assert r"Au_+=3u_+" in TEXT
    assert r"Au_-=1u_-" in TEXT
    assert r"u^T A u=u^T(\lambda u)=\lambda\,u^Tu=\boxed{\lambda}" in TEXT
    assert r"x^T A x=\sum_i\lambda_i c_i^2" in TEXT


def test_scene_states_symmetric_eigenvalue_test():
    assert r"A=A^T\ \text{is positive definite}" in TEXT
    assert r"\lambda_i>0\ \text{for every eigenvalue}" in TEXT
    assert r"\lambda_1=1>0,\qquad\lambda_2=3>0" in TEXT


def test_scene_stays_within_approved_scope():
    forbidden = ("pivot", "minor", "LDL", "Cholesky")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP201" not in TEXT
