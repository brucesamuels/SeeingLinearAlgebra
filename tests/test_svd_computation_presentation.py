from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "svd_computation_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_computes_gram_eigenpairs_and_singular_values():
    assert '[["1", "1"], ["1", "-1"], ["1", "1"]]' in TEXT
    assert '[["3", "1"], ["1", "3"]]' in TEXT
    assert r"(\lambda-4)(\lambda-2)=0" in TEXT
    assert r"\lambda_1=4" in TEXT
    assert r"\sigma_1=\sqrt4=2" in TEXT
    assert r"\sigma_2=\sqrt2" in TEXT


def test_scene_has_pause_and_recovers_left_vectors_without_second_eigenproblem():
    assert "Pause: how can we recover U without solving another eigenvalue problem?" in TEXT
    assert r"\boxed{u_i=\frac{Bv_i}{\sigma_i}}" in TEXT
    assert "No second eigenvalue computation is needed." in TEXT
    assert r"Bv_1=" in TEXT
    assert r"Bv_2=" in TEXT


def test_scene_assembles_dimensioned_thin_svd_and_reconstructs():
    assert r"U\ (3\times2)" in TEXT
    assert r"\Sigma\ (2\times2)" in TEXT
    assert r"V^T\ (2\times2)" in TEXT
    assert r"U\Sigma V^T=" in TEXT
    assert "The thin factors reproduce every entry of B." in TEXT


def test_scene_explains_paired_sign_ambiguity():
    assert r"u_i\mapsto -u_i" in TEXT
    assert r"v_i\mapsto -v_i" in TEXT
    assert r"\sigma_i(-u_i)(-v_i)^T=\sigma_i u_iv_i^T" in TEXT


def test_scene_finishes_with_reusable_five_step_recipe_and_preserves_scope():
    for step in range(1, 6):
        assert f'self._step({step},' in TEXT
    forbidden = ("pseudoinverse", "low-rank", "zero singular value", "minimum principle")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP209" not in TEXT


def test_scene_is_standalone_without_checkpoint_references():
    assert "CP208" not in TEXT
    assert "checkpoint" not in TEXT.lower()
    assert "The SVD separates a matrix into three meaningful factors." in TEXT
