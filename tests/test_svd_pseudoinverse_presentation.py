from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "svd_pseudoinverse_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_chapter_banner_and_structural_matrices():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "The Pseudoinverse: Undo What Can Be Undone" in TEXT
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_begins_with_impossibility_of_ordinary_inverse():
    assert '[["1", "1"], ["1", "1"], ["0", "0"]]' in TEXT
    assert r"A:\mathbb R^2\to\mathbb R^3" in TEXT
    assert r"A^{-1}\ \text{does not exist}" in TEXT
    assert "rectangular" in TEXT
    assert "rank one" in TEXT


def test_scene_has_active_lost_lanes_and_prediction():
    assert r"\sigma_1=2" in TEXT
    assert r"\sigma_2=0" in TEXT
    assert "survives" in TEXT
    assert "lost" in TEXT
    assert "Pause: when we reverse the SVD" in TEXT


def test_scene_defines_zero_safe_reciprocal_rule():
    assert r"\sigma_i^+=" in TEXT
    assert r"2\mapsto\frac12" in TEXT
    assert r"0\mapsto0" in TEXT
    assert "Never divide by zero." in TEXT
    assert r"\Sigma^+=" in TEXT


def test_scene_builds_pseudoinverse_and_reverses_dimensions():
    assert r"\boxed{A^+=V\Sigma^+U^T}" in TEXT
    assert r"A^+:\mathbb R^3\to\mathbb R^2" in TEXT
    assert r"\frac14" in TEXT
    assert r"A^+=\frac12v_1u_1^T" in TEXT


def test_scene_distinguishes_recovered_and_lost_inputs():
    assert r"A^+Av_1=v_1" in TEXT
    assert r"A^+Av_2=0" in TEXT
    assert r"A^+A\ne I_2" in TEXT
    assert "information is gone" in TEXT


def test_scene_interprets_round_trips_as_projections():
    assert r"A^+A=" in TEXT
    assert r"P_{\mathcal R(A^T)}" in TEXT
    assert r"AA^+=" in TEXT
    assert r"P_{\mathcal R(A)}" in TEXT
    assert "remove the null-space component" in TEXT
    assert "remove the left-null-space component" in TEXT


def test_scene_preserves_next_lesson_scope_and_has_no_checkpoint_labels():
    forbidden = ("least-squares", "minimum-norm", "normal equations", "condition number", "Eckart", "PCA")
    assert not any(term.lower() in TEXT.lower() for term in forbidden)
    assert "CP217" not in TEXT
    assert "CP216" not in TEXT
    assert "checkpoint" not in TEXT.lower()
