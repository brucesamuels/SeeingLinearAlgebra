from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "svd_zero_singular_value_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_opens_new_chapter_and_uses_structural_matrices():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "What Does a Zero Singular Value Mean?" in TEXT
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_animates_circle_to_segment_collapse():
    assert "Circle(" in TEXT
    assert "circle_samples(32)" in TEXT
    assert "mapped_circle_samples(32)" in TEXT
    assert "dot.animate.move_to" in TEXT
    assert "Watch the unit circle collapse onto a line segment." in TEXT


def test_scene_distinguishes_surviving_and_lost_directions():
    assert r"Av_1=2u_1" in TEXT
    assert r"Av_2=0" in TEXT
    assert "One direction survives" in TEXT
    assert "Pause: where is the lost direction recorded in the SVD?" in TEXT


def test_scene_connects_gram_eigenvalues_and_singular_values():
    assert r"\lambda_1=4" in TEXT
    assert r"\lambda_2=0" in TEXT
    assert r"\sigma_i=\sqrt{\lambda_i(A^TA)}" in TEXT
    assert r"\sigma_1=2" in TEXT
    assert r"\sigma_2=0" in TEXT


def test_scene_connects_zero_singular_value_to_null_space_and_rank():
    assert r"v_2\in\mathcal N(A)" in TEXT
    assert r"\mathcal N(A)=\operatorname{span}\{v_2\}" in TEXT
    assert r"\operatorname{rank}(A)=\#\{\sigma_i>0\}" in TEXT
    assert r"A=2u_1v_1^T" in TEXT


def test_scene_finishes_with_scope_appropriate_conclusions():
    assert r"\boxed{\sigma_i=0\ \Longleftrightarrow\ Av_i=0}" in TEXT
    assert "positive singular values" in TEXT
    forbidden = ("pseudoinverse", "least-squares", "condition number", "Eckart", "PCA", "image compression")
    assert not any(term.lower() in TEXT.lower() for term in forbidden)


def test_scene_is_standalone_without_checkpoint_references():
    assert "CP215" not in TEXT
    assert "CP214" not in TEXT
    assert "checkpoint" not in TEXT.lower()
