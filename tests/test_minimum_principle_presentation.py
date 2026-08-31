from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "minimum_principle_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_defines_rayleigh_quotient_and_scale_invariance():
    assert r"R_A(x)=\frac{x^TAx}{x^Tx},\qquad x\ne0" in TEXT
    assert r"R_A(cx)=\frac{(cx)^TA(cx)}{(cx)^T(cx)}" in TEXT
    assert r"=\frac{c^2x^TAx}{c^2x^Tx}=R_A(x)" in TEXT
    assert "measures a direction, not its length" in TEXT


def test_scene_uses_exact_three_by_three_example_and_eigenpairs():
    assert '[["2", "1", "0"], ["1", "2", "0"], ["0", "0", "4"]]' in TEXT
    assert r"\lambda_1=1" in TEXT
    assert r"\lambda_2=3" in TEXT
    assert r"\lambda_3=4" in TEXT
    assert r"v_1=\frac1{\sqrt2}" in TEXT
    assert r"v_2=\frac1{\sqrt2}" in TEXT


def test_scene_derives_weighted_average_and_bounds():
    assert r"x=c_1v_1+c_2v_2+c_3v_3" in TEXT
    assert r"x^TAx=c_1^2+3c_2^2+4c_3^2" in TEXT
    assert r"w_i\ge0,\qquad w_1+w_2+w_3=1" in TEXT
    assert r"\boxed{1\le R_A(x)\le4}" in TEXT


def test_scene_has_pause_and_successive_constrained_minima():
    assert "Pause: what happens if the lowest-energy direction is excluded?" in TEXT
    assert r"\boxed{\lambda_1=\min_{x\ne0}R_A(x)=1}" in TEXT
    assert r"x\perp v_1\quad\Longrightarrow\quad c_1=0" in TEXT
    assert r"x\perp v_1,v_2\quad\Longrightarrow\quad x=c_3v_3" in TEXT
    assert r"\min R_A=\lambda_1" in TEXT
    assert r"\min R_A=\lambda_2" in TEXT
    assert r"\min R_A=\lambda_3" in TEXT


def test_scene_finishes_with_general_minimum_principle_and_preserves_scope():
    assert "SUCCESSIVE MINIMUM PRINCIPLE" in TEXT
    assert r"x\perp v_1,\ldots,v_{k-1}" in TEXT
    assert r"\frac{x^TAx}{x^Tx}" in TEXT
    forbidden = ("finite element", "Ritz", "Galerkin", "generalized eigenvalue")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)


def test_scene_is_standalone_without_checkpoint_references():
    assert "CP210" not in TEXT
    assert "CP209" not in TEXT
    assert "checkpoint" not in TEXT.lower()
