from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "svd_image_compression_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_chapter_banner_images_and_structural_matrix():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "Image Compression with the SVD" in TEXT
    assert "ImageMobject" in TEXT
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_treats_grayscale_image_as_brightness_matrix():
    assert "32 x 32 IMAGE" in TEXT
    assert r"A\in\mathbb R^{32\times32}" in TEXT
    assert r"0\le a_{ij}\le1" in TEXT
    assert "1024 brightness values" in TEXT


def test_scene_explains_rank_one_image_layers_and_spectrum():
    assert r"A=\sum_{i=1}^{32}\sigma_i u_i v_i^T" in TEXT
    assert "one rank-one image layer" in TEXT
    assert "importance of that layer" in TEXT
    assert "_spectrum" in TEXT
    assert r"\sigma_1\ge\sigma_2\ge\cdots\ge\sigma_{32}\ge0" in TEXT


def test_scene_shows_rank_one_four_and_eight_reconstructions():
    assert "RANK 1" in TEXT
    assert "RANK 4" in TEXT
    assert "RANK 8" in TEXT
    assert r"A_1=\sigma_1u_1v_1^T" in TEXT
    assert r"A_4=\sum_{i=1}^{4}\sigma_i u_i v_i^T" in TEXT
    assert r"A_8=\sum_{i=1}^{8}\sigma_i u_i v_i^T" in TEXT
    assert "retained energy" in TEXT
    assert "relative error" in TEXT


def test_scene_defines_error_and_retained_energy():
    assert r"\|A-A_k\|_F^2=\sum_{i>k}\sigma_i^2" in TEXT
    assert r"E_k=\frac{\sum_{i=1}^{k}\sigma_i^2}{\sum_i\sigma_i^2}" in TEXT
    assert "energies =" in TEXT
    assert "relative_errors =" in TEXT


def test_scene_computes_storage_tradeoff():
    assert r"mn=32\cdot32=1024" in TEXT
    assert r"k(m+n+1)=4(32+32+1)=260" in TEXT
    assert "four left vectors, values, and right vectors" in TEXT
    assert "storage_fraction(4)" in TEXT
    assert "compression_ratio(4)" in TEXT


def test_scene_compares_images_and_concludes_with_rank_choice():
    assert "Increasing rank trades storage" in TEXT
    assert "ORIGINAL" in TEXT
    assert "SMALL k" in TEXT
    assert "LARGE k" in TEXT
    assert r"\boxed{A_k=\sum_{i=1}^{k}\sigma_i u_i v_i^T}" in TEXT
    assert "balance simplicity and visual fidelity" in TEXT


def test_scene_preserves_pca_scope_and_has_no_checkpoint_labels():
    forbidden = ("PCA", "principal component", "covariance", "RGB", "color channel")
    assert not any(term.lower() in TEXT.lower() for term in forbidden)
    assert "CP221" not in TEXT
    assert "CP220" not in TEXT
    assert "checkpoint" not in TEXT.lower()
