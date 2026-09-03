from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "truncated_svd_approximation_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_chapter_banner_and_structural_matrices():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "Truncated SVD and the Best Low-Rank Approximation" in TEXT
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_starts_with_ordered_singular_values():
    assert r"\sigma_1=5" in TEXT
    assert r"\sigma_2=2" in TEXT
    assert r"\sigma_3=\frac12" in TEXT
    assert r"\sigma_1\ge\sigma_2\ge\sigma_3\ge0" in TEXT


def test_scene_writes_svd_as_rank_one_layers():
    assert r"A=\sigma_1u_1v_1^T+\sigma_2u_2v_2^T+\sigma_3u_3v_3^T" in TEXT
    assert r"A=5u_1v_1^T+2u_2v_2^T+\frac12u_3v_3^T" in TEXT
    assert "Each outer product contributes one independent direction." in TEXT
    assert "_mode_bar" in TEXT


def test_scene_constructs_rank_two_truncation_and_residual():
    assert r"A_2=5u_1v_1^T+2u_2v_2^T" in TEXT
    assert "discarded" in TEXT
    assert r"A-A_2=\frac12u_3v_3^T" in TEXT
    assert "Only the weakest singular direction is missing." in TEXT


def test_scene_computes_spectral_and_frobenius_errors():
    assert r"\|A-A_2\|_2=\sigma_3=\frac12" in TEXT
    assert r"\|A-A_2\|_F=\sqrt{\sigma_3^2}=\frac12" in TEXT
    assert "largest omitted stretch" in TEXT
    assert "energy of omitted stretches" in TEXT


def test_scene_states_eckart_young_optimality():
    assert "ECKART–YOUNG THEOREM" in TEXT
    assert r"\min_{\operatorname{rank}(B)\le k}\|A-B\|_2=\sigma_{k+1}" in TEXT
    assert r"\sqrt{\sum_{i>k}\sigma_i^2}" in TEXT
    assert r"A_2\ \text{is optimal}" in TEXT


def test_scene_compares_wrong_component_choice_and_approximation_ladder():
    assert "KEEP 5 AND 2" in TEXT
    assert "KEEP 5 AND 1/2" in TEXT
    assert "a worse rank-two choice" in TEXT
    assert "RANK 1" in TEXT
    assert "RANK 2" in TEXT
    assert "RANK 3" in TEXT
    assert "spectral error 1/2" in TEXT


def test_scene_concludes_with_truncated_svd_formula_and_preserves_later_scope():
    assert r"\boxed{A_k=\sum_{i=1}^{k}\sigma_i u_i v_i^T}" in TEXT
    assert "strongest rank-one layers" in TEXT
    assert "Lower rank means a simpler model" in TEXT
    forbidden = ("image compression", "pixel", "PCA", "principal component", "covariance")
    assert not any(term.lower() in TEXT.lower() for term in forbidden)
    assert "CP220" not in TEXT
    assert "CP219" not in TEXT
    assert "checkpoint" not in TEXT.lower()
