from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "svd_chapter_synthesis_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_chapter_banner_and_big_picture_title():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "Singular Values, Rank, and Approximation: The Big Picture" in TEXT
    assert r"A=U\Sigma V^T" in TEXT


def test_scene_summarizes_zero_small_and_large_singular_values():
    assert '"ZERO"' in TEXT
    assert '"SMALL"' in TEXT
    assert '"LARGE"' in TEXT
    assert "direction is lost" in TEXT
    assert "inverse is sensitive" in TEXT
    assert "effect is dominant" in TEXT


def test_scene_connects_positive_singular_values_to_four_subspaces():
    assert r"r=\#\{i:\sigma_i>0\}=\operatorname{rank}(A)" in TEXT
    assert "ROW SPACE" in TEXT
    assert "NULL SPACE" in TEXT
    assert "COLUMN SPACE" in TEXT
    assert "LEFT NULL SPACE" in TEXT
    assert "reachable outputs: the image" in TEXT


def test_scene_uses_image_and_preimage_language_for_pseudoinverse():
    assert r"A^+=V\Sigma^+U^T" in TEXT
    assert "CLOSEST IMAGE" in TEXT
    assert "SHORTEST PRE-IMAGE" in TEXT
    assert r"AA^+\mathbf b\in\operatorname{Col}(A)" in TEXT
    assert r"\mathbf x^+=A^+\mathbf b" in TEXT
    assert "leave every zero singular value at zero" in TEXT


def test_scene_summarizes_conditioning_and_truncated_svd():
    assert r"\kappa_2(A)=\frac{\sigma_1}{\sigma_2}=6" in TEXT
    assert "Invertible does not necessarily mean numerically stable" in TEXT
    assert r"A_k=\sum_{i=1}^{k}\sigma_i u_i v_i^T" in TEXT
    assert r"\|A-A_k\|_F^2=\sum_{i>k}\sigma_i^2" in TEXT
    assert "No other rank-k matrix has smaller" in TEXT


def test_scene_connects_image_compression_and_pca():
    assert "IMAGE COMPRESSION" in TEXT
    assert r"X_c\approx U_k\Sigma_kV_k^T" in TEXT
    assert "pixels become a matrix" in TEXT
    assert "observations become a centered matrix" in TEXT
    assert "Large singular values identify the structure worth preserving" in TEXT


def test_scene_contains_four_way_recognition_guide_and_closing_claim():
    assert "INVERSE" in TEXT
    assert "PSEUDOINVERSE" in TEXT
    assert "TRUNCATED SVD" in TEXT
    assert "centered data need fewer coordinates" in TEXT
    for word in ("PRESERVES", "LOSES", "AMPLIFIES", "APPROXIMATES"):
        assert word in TEXT
    assert "Read the spectrum" in TEXT


def test_scene_has_nine_cards_and_no_checkpoint_labels():
    assert TEXT.count("heading = self._replace_heading") == 8
    assert TEXT.count("self.wait(4.") == 9
    assert "run_time=0.28" in TEXT
    assert "run_time=0.32" in TEXT
    assert "CP223" not in TEXT
    assert "CP222" not in TEXT
    assert "checkpoint" not in TEXT.lower()
