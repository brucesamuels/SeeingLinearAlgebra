from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "covariance_definiteness_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects_for_covariance_computations():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_defines_mean_centering_and_population_covariance_before_definiteness():
    assert r"\mu=\frac14\sum_{i=1}^4p_i=(3,2)" in TEXT
    assert r"c_i=p_i-\mu" in TEXT
    assert "population covariance matrix" in TEXT
    assert r"\boxed{\Sigma=\frac1m\sum_{i=1}^m c_ic_i^T=\frac1m C^TC}" in TEXT
    assert TEXT.index("population covariance matrix") < TEXT.index("positive semidefinite")


def test_scene_explains_covariance_entries():
    assert "variance of each coordinate" in TEXT
    assert "how coordinates vary together" in TEXT
    assert '[["2", "1"], ["1", "1"]]' in TEXT


def test_scene_connects_directional_variance_to_squared_norm():
    assert r"Cv=(-2,0,0,2)^T" in TEXT
    assert r"v^T\Sigma v=2" in TEXT
    assert r"\boxed{v^T\Sigma v=\frac1m\lVert Cv\rVert^2\ge0}" in TEXT


def test_scene_has_pause_and_zero_variance_line_example():
    assert "Pause: when can a nonzero direction have zero variance?" in TEXT
    assert '[["-1", "-2"], ["0", "0"], ["1", "2"]]' in TEXT
    assert r"v=(-2,1)^T\ne0" in TEXT
    assert r"Dv=0" in TEXT
    assert "All projections onto v collapse to zero." in TEXT


def test_scene_states_final_rank_criterion_and_stays_in_scope():
    assert r"\Sigma\ \text{is always positive semidefinite}" in TEXT
    assert r"C\ \text{has full column rank}" in TEXT
    assert "Sample covariance uses 1/(m−1)" in TEXT
    forbidden = ("principal component", "correlation matrix", "whitening", "statistical inference")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP207" not in TEXT
