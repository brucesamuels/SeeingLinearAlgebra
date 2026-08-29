from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "positive_definite_cholesky_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects_and_compact_fractions():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT
    assert r"\frac" not in TEXT
    assert r"\tfrac" in TEXT


def test_scene_derives_cholesky_from_ldlt():
    assert r"D^{1/2}" in TEXT
    assert r"R=D^{1/2}L^T" in TEXT
    assert r"A=R^TR" in TEXT


def test_scene_constructs_each_upper_triangular_entry():
    for formula in (
        r"r_{11}=\sqrt4=2",
        r"r_{12}=2/r_{11}=1",
        r"r_{13}=0",
        r"r_{22}=\sqrt{3-r_{12}^2}=\sqrt2",
        r"r_{23}=\tfrac{1-r_{12}r_{13}}{r_{22}}=\tfrac1{\sqrt2}",
        r"r_{33}=\sqrt{2-r_{13}^2-r_{23}^2}=\sqrt{\tfrac32}",
    ):
        assert formula in TEXT


def test_scene_connects_cholesky_to_squared_norm():
    assert r"x^TAx=x^TR^TRx" in TEXT
    assert r"x^TAx=\lVert Rx\rVert^2" in TEXT


def test_scene_has_pause_and_states_unique_positive_diagonal_criterion():
    assert "Pause: what would prevent the next positive square root from existing?" in TEXT
    assert "unique upper-triangular" in TEXT
    assert "positive diagonal" in TEXT
    assert r"A=A^T\ \text{is positive definite}" in TEXT


def test_scene_stays_within_approved_scope():
    forbidden = ("normal equation", "least squares", "covariance")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP204" not in TEXT
