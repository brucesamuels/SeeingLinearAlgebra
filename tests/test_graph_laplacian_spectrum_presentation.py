from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "graph_laplacian_spectrum_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "Laplacian Eigenvalues and the Spectral Gap"' in TEXT
    assert r"\textbf{Laplacian Eigenvalues and the Spectral Gap}" in TEXT


def test_scene_uses_renderer_independent_model_and_exact_spectral_spine():
    assert "from engine.graph_laplacian_spectrum import GraphLaplacianSpectrum" in TEXT
    assert "model = GraphLaplacianSpectrum()" in TEXT
    assert 'RuntimeError("unexpected recurring Laplacian spectrum")' in TEXT
    assert 'RuntimeError("unexpected second Laplacian mode")' in TEXT
    assert 'RuntimeError("unexpected second-mode Rayleigh quotient")' in TEXT
    assert 'RuntimeError("unexpected split-graph spectrum")' in TEXT


def test_vertex_numerals_use_high_contrast_black():
    assert "vertex: MathTex(str(vertex), font_size=29, color=BLACK)" in TEXT


def test_scene_reconnects_null_space_to_zero_eigenvalue():
    assert "Each connected component contributed a zero-eigenvalue direction." in TEXT
    assert '"CONSTANT MODE"' in TEXT
    assert r"\mathbf v_1=(1,1,1,1)^T" in TEXT
    assert r"L\mathbf v_1=0\mathbf v_1" in TEXT
    assert r"\lambda_1=0" in TEXT


def test_scene_orders_and_reveals_exact_spectrum():
    assert "symmetric and positive semidefinite" in TEXT
    assert r"0=\lambda_1\le\lambda_2\le\lambda_3\le\lambda_4" in TEXT
    assert "Recurring graph spectrum: 0, 1, 3, 4" in TEXT
    assert "NumberLine(" in TEXT


def test_scene_structurally_verifies_second_eigenpair():
    assert "The first mode above zero changes slowly" in TEXT
    assert '[["1"], ["1"], ["0"], ["-2"]]' in TEXT
    assert r"\mathbf v_2=(1,1,0,-2)^T,\qquad \lambda_2=1" in TEXT
    assert "entries sum to zero" in TEXT


def test_scene_places_second_mode_and_energy_on_graph():
    assert "largest change occurs across the lone edge" in TEXT
    assert '"SQUARED EDGE CHANGES"' in TEXT
    assert r"0+1+1+4=6" in TEXT
    assert "bridge contributes the largest share" in TEXT
    assert r"\mathbf v_2^TL\mathbf v_2=6" in TEXT
    assert ".set_stroke(width=9)" in TEXT


def test_scene_introduces_rayleigh_quotient_concretely():
    assert "divide their energy by their squared length" in TEXT
    assert "RAYLEIGH QUOTIENT" in TEXT
    assert r"R(\mathbf x)=\frac{\mathbf x^TL\mathbf x}{\mathbf x^T\mathbf x}" in TEXT
    assert r"R(\mathbf v_2)=\frac{6}{1^2+1^2+0^2+(-2)^2}=\frac66=1" in TEXT
    assert "variation per unit of squared size" in TEXT


def test_scene_characterizes_lambda_two_by_mean_zero_minimization():
    assert "Exclude the constant direction" in TEXT
    assert '"REMOVE THE CONSTANT MODE"' in TEXT
    assert r"\mathbf x^T\mathbf 1=0\quad\Longleftrightarrow\quad x_1+\cdots+x_n=0" in TEXT
    assert r"\lambda_2=\min_" in TEXT
    assert "cheapest nonconstant pattern of variation" in TEXT


def test_scene_defines_gap_and_connectivity_criterion():
    assert "second-smallest Laplacian eigenvalue is called the spectral gap" in TEXT
    assert "also called algebraic connectivity" in TEXT
    assert r"\lambda_2>0" in TEXT
    assert r"\lambda_2=0" in TEXT
    assert "gap closes exactly when the graph separates" in TEXT


def test_scene_compares_bridge_present_and_removed_spectra():
    assert r"0,\ \boxed{1},\ 3,\ 4" in TEXT
    assert r"0,\ \boxed{0},\ 3,\ 3" in TEXT
    assert r"\text{remove }\{3,4\}" in TEXT
    assert "extra component creates an extra zero mode" in TEXT
    assert "smaller positive gap" in TEXT


def test_scene_previews_fiedler_vector_without_partitioning():
    assert '"ZEROS"' in TEXT
    assert '"GAP"' in TEXT
    assert '"SECOND MODE"' in TEXT
    assert "The eigenvector v₂ is called a Fiedler vector." in TEXT
    assert "Can its signs reveal a useful division of the vertices?" in TEXT
    assert "partition" not in TEXT.lower()
