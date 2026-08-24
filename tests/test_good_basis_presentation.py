from pathlib import Path
SCENE = Path("scenes/good_basis_presentation.py")
def source(): return SCENE.read_text(encoding="utf-8")


def test_identity_and_independence_from_eigenvalue_vocabulary():
    text = source()
    assert 'CHAPTER_BANNER = "CHANGE OF BASIS"' in text
    assert 'LESSON_TITLE = "Why a Good Basis Matters"' in text
    assert "eigenvalue" not in text.lower() and "eigenvector" not in text.lower()
    assert "CP193" not in text


def test_standard_grid_shows_coordinate_mixing():
    text = source()
    assert "Transform(standard_grid, mixed_grid, rate_func=smooth)" in text
    assert r"A\mathbf e_1=(3,1)" in text
    assert r"A\mathbf e_2=(1,3)" in text


def test_good_basis_grid_shows_independent_scaling():
    text = source()
    assert "Transform(basis_grid, scaled_basis_grid, rate_func=smooth)" in text
    assert r"A\mathbf b_1=4\mathbf b_1" in text
    assert r"A\mathbf b_2=2\mathbf b_2" in text
    assert "neither one turns" in text


def test_algebra_uses_structural_matrices_without_raw_bmatrix():
    text = source()
    assert r"\begin{bmatrix}" not in text
    assert r"[A]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}=" in text
    assert 'self._matrix([["4", "0"], ["0", "2"]]' in text
    assert "v_buff=0.95" in text


def test_worked_vector_and_synthesis_are_present():
    text = source()
    assert r"(2,1)_{\mathcal B}\leftrightarrow(3,1)" in text
    assert r"(8,2)_{\mathcal B}\leftrightarrow(10,6)" in text
    assert "A good basis reveals the transformation's natural structure." in text
