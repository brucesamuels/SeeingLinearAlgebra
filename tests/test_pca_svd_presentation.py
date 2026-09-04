from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "pca_svd_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_chapter_banner_and_pca_title():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "Principal Component Analysis through the SVD" in TEXT
    assert "NumberPlane" in TEXT
    assert "Matrix(entries" in TEXT


def test_scene_centers_data_and_defines_row_column_roles():
    assert "coordinate-wise average, or balance point" in TEXT
    assert r"\bar{\mathbf x}=\frac1{6}\sum_{i=1}^{6}\mathbf x_i=(0,0)" in TEXT
    assert r"\mathbf x_i^{\,(c)}=\mathbf x_i-\bar{\mathbf x}" in TEXT
    assert r"X_c=X-\mathbf1\bar{\mathbf x}^{T}=X" in TEXT
    assert "each row becomes a displacement from the average" in TEXT
    assert "PCA now measures spread around what is typical" in TEXT
    assert "Rows are observations" in TEXT
    assert "columns are measured features" in TEXT


def test_scene_connects_svd_to_scores_and_feature_directions():
    assert r"X=U\Sigma V^T" in TEXT
    assert r"\sigma_i u_i=Xv_i" in TEXT
    assert "coordinates of the observations" in TEXT
    assert "axes in feature space" in TEXT


def test_scene_computes_exact_gram_eigenpairs():
    assert r"X^TX=\begin{bmatrix}28&26\\26&28\end{bmatrix}" in TEXT
    assert r"\begin{gathered}\lambda_1=54\\v_1=\frac1{\sqrt2}(1,1)\end{gathered}" in TEXT
    assert r"\begin{gathered}\lambda_2=2\\v_2=\frac1{\sqrt2}(1,-1)\end{gathered}" in TEXT
    assert r"v_1=\frac1{\sqrt2}(1,1)" in TEXT
    assert r"v_2=\frac1{\sqrt2}(1,-1)" in TEXT
    assert r"\sigma_i^2=\lambda_i" in TEXT


def test_scene_visualizes_principal_axes_scores_and_rank_one_projection():
    assert "_principal_axes" in TEXT
    assert "MAJOR AXIS" in TEXT
    assert "MINOR AXIS" in TEXT
    assert r"z=Xv_1=\sigma_1u_1" in TEXT
    assert r"X_1=(Xv_1)v_1^T" in TEXT
    assert "DashedLine" in TEXT
    assert "ReplacementTransform" in TEXT


def test_scene_computes_retained_variation_and_concludes_with_pca():
    assert r"\frac{54}{54+2}=96.4\%" in TEXT
    assert "two coordinates" in TEXT
    assert "one score" in TEXT
    assert "PCA is truncated SVD applied to centered data" in TEXT
    assert r"\boxed{X_k=U_k\Sigma_kV_k^T}" in TEXT


def test_scene_has_ten_headings_and_no_checkpoint_labels():
    assert TEXT.count("heading = self._replace_heading") == 9
    assert "CP222" not in TEXT
    assert "CP221" not in TEXT
    assert "checkpoint" not in TEXT.lower()
