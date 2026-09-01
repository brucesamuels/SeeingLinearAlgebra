from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "positive_definiteness_summary_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_contrasts_three_energy_classifications():
    assert "POSITIVE DEFINITE" in TEXT
    assert "POSITIVE SEMIDEFINITE" in TEXT
    assert "INDEFINITE" in TEXT
    assert r"x^TAx>0\quad(x\ne0)" in TEXT
    assert r"x^TBx\ge0" in TEXT
    assert r"x^TCx\text{ has both signs}" in TEXT
    assert "Pause: which matrices have strictly positive energy" in TEXT


def test_scene_summarizes_energy_and_eigenvalue_tests():
    assert r"x^TAx>0\quad\forall x\ne0" in TEXT
    assert r"\lambda_1=1,\ \lambda_2=3" in TEXT
    assert r"x^TAx=\lambda_1c_1^2+\lambda_2c_2^2" in TEXT


def test_scene_summarizes_pivot_and_minor_tests():
    assert r"p_1=2,\quad p_2=\frac32" in TEXT
    assert r"\Delta_1=2,\quad\Delta_2=3" in TEXT
    assert r"p_k=\frac{\Delta_k}{\Delta_{k-1}}" in TEXT


def test_scene_summarizes_ldl_and_cholesky_tests():
    assert "LDLᵀ" in TEXT
    assert r"x^TAx=y^TDy" in TEXT
    assert r"A=R^TR" in TEXT
    assert r"x^TAx=\lVert Rx\rVert^2" in TEXT
    assert "Positive diagonal D and invertible R" in TEXT


def test_scene_builds_six_part_toolkit_and_practical_decision_map():
    for title in ("ENERGY", "EIGENVALUES", "PIVOTS", "LEADING MINORS", "CHOLESKY"):
        assert title in TEXT
    for title in ("GEOMETRY", "SPECTRAL DATA", "ELIMINATION", "SOLVING"):
        assert title in TEXT
    assert "Different computations — the same conclusion." in TEXT


def test_scene_reconnects_major_applications_and_final_message():
    assert "GRAM MATRICES" in TEXT
    assert "COVARIANCE" in TEXT
    assert "SVD" in TEXT
    assert "MINIMIZATION" in TEXT
    assert r"x^TA^TAx=\lVert Ax\rVert^2" in TEXT
    assert r"\lambda_i(A^TA)=\sigma_i^2" in TEXT
    assert "positive energy" in TEXT
    assert "unique minimum" in TEXT
    assert "unique solution" in TEXT


def test_scene_is_standalone_without_checkpoint_references():
    assert "CP212" not in TEXT
    assert "CP211" not in TEXT
    assert "checkpoint" not in TEXT.lower()
