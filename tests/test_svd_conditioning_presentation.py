from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "svd_conditioning_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_chapter_banner_and_structural_matrices():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "Small Singular Values and Conditioning" in TEXT
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_begins_with_invertible_but_sensitive_map():
    assert '[["4", "0"], ["0", r"\\frac14"]]' in TEXT
    assert r"A:\mathbb R^2\to\mathbb R^2" in TEXT
    assert r"\det(A)=1\ne0" in TEXT
    assert "a bijection" in TEXT
    assert "Invertible does not automatically mean stable." in TEXT


def test_scene_identifies_strong_and_weak_singular_lanes():
    assert r"\sigma_1=4" in TEXT
    assert r"\sigma_2=\frac14" in TEXT
    assert "strong" in TEXT
    assert "weak" in TEXT
    assert r"\sigma_1=16\sigma_2" in TEXT


def test_scene_uses_circle_to_ellipse_geometry():
    assert "Circle(" in TEXT
    assert "Ellipse(" in TEXT
    assert "semiaxes 4 and 1/4" in TEXT
    assert "unit circle becomes a long, thin ellipse" in TEXT


def test_scene_reciprocates_singular_values_and_compares_perturbations():
    assert r"A^{-1}=" in TEXT
    assert r"4\mapsto\frac14" in TEXT
    assert r"\frac14\mapsto4" in TEXT
    assert r"\frac{\varepsilon}{4}v_1" in TEXT
    assert r"4\varepsilon v_2" in TEXT
    assert "sixteen times larger" in TEXT


def test_scene_defines_condition_number_and_error_bound():
    assert r"\kappa_2(A)=\frac{\sigma_{\max}}{\sigma_{\min}}" in TEXT
    assert r"=\frac{4}{1/4}=16" in TEXT
    assert r"\frac{\|\Delta\mathbf x\|}{\|\mathbf x\|}" in TEXT
    assert r"\frac{\|\Delta\mathbf b\|}{\|\mathbf b\|}" in TEXT
    assert "sixteenfold relative amplification" in TEXT


def test_scene_connects_small_zero_singular_values_to_instability():
    assert "BALANCED" in TEXT
    assert "THIN" in TEXT
    assert "COLLAPSED" in TEXT
    assert r"\sigma_{\min}\downarrow0" in TEXT
    assert r"\kappa_2(A)\uparrow\infty" in TEXT
    assert "nearly loses a direction" in TEXT
    assert "amplifies uncertainty" in TEXT


def test_scene_preserves_approximation_scope_and_has_no_checkpoint_labels():
    forbidden = ("truncated SVD", "Eckart", "compression", "PCA")
    assert not any(term.lower() in TEXT.lower() for term in forbidden)
    assert "CP219" not in TEXT
    assert "CP218" not in TEXT
    assert "checkpoint" not in TEXT.lower()
