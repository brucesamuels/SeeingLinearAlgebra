from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "svd_fundamental_subspaces_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_new_chapter_banner_and_structural_matrices():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "Full SVD and the Four Fundamental Subspaces" in TEXT
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_uses_rectangular_rank_one_numerical_spine():
    assert '[["1", "1"], ["1", "1"], ["0", "0"]]' in TEXT
    assert r"A:\mathbb R^2\to\mathbb R^3" in TEXT
    assert r"\operatorname{rank}(A)=1" in TEXT
    assert r"Av_1=2u_1" in TEXT
    assert r"Av_2=0" in TEXT


def test_scene_has_full_svd_pipeline_and_pause():
    assert r"\xrightarrow{\ V^T\ }" in TEXT
    assert r"\xrightarrow{\ \Sigma\ }" in TEXT
    assert r"\xrightarrow{\ U\ }" in TEXT
    assert "Pause: which fundamental subspace contains each singular direction?" in TEXT


def test_scene_assigns_v_columns_to_domain_subspaces():
    assert "V separates the row space from the null space." in TEXT
    assert r"\mathcal R(A^T)=\operatorname{span}\{v_1\}" in TEXT
    assert r"\mathcal N(A)=\operatorname{span}\{v_2\}" in TEXT
    assert r"\mathbb R^2=\mathcal R(A^T)\oplus\mathcal N(A)" in TEXT


def test_scene_assigns_u_columns_to_codomain_subspaces():
    assert "U separates the column space from the left null space." in TEXT
    assert r"\mathcal R(A)=\operatorname{span}\{u_1\}" in TEXT
    assert r"\mathcal N(A^T)=\operatorname{span}\{u_2,u_3\}" in TEXT
    assert r"\mathbb R^3=\mathcal R(A)\oplus\mathcal N(A^T)" in TEXT


def test_scene_displays_full_rectangular_factor_dimensions():
    assert r"U\ (3\times3)" in TEXT
    assert r"\Sigma\ (3\times2)" in TEXT
    assert r"V^T\ (2\times2)" in TEXT
    assert r"m=3,\quad n=2,\quad r=1" in TEXT
    assert r"\dim\mathcal N(A^T)=m-r=2" in TEXT


def test_scene_finishes_with_svd_subspace_organization():
    assert r"V=[\ \mathcal R(A^T)\mid\mathcal N(A)\ ]" in TEXT
    assert r"U=[\ \mathcal R(A)\mid\mathcal N(A^T)\ ]" in TEXT
    assert "Sigma connects the active directions." in TEXT


def test_scene_preserves_later_scope_and_has_no_checkpoint_labels():
    forbidden = ("pseudoinverse", "least-squares", "minimum-norm", "condition number", "Eckart", "PCA")
    assert not any(term.lower() in TEXT.lower() for term in forbidden)
    assert "CP216" not in TEXT
    assert "CP215" not in TEXT
    assert "checkpoint" not in TEXT.lower()
