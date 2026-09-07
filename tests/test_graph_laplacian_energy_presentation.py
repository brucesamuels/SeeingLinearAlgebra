from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "graph_laplacian_energy_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "Laplacian Energy: Variation Across Edges"' in TEXT
    assert r"\textbf{Laplacian Energy: Variation Across Edges}" in TEXT


def test_scene_uses_renderer_independent_model_and_exact_energy_spine():
    assert "from engine.graph_laplacian_energy import GraphLaplacianEnergy" in TEXT
    assert "model = GraphLaplacianEnergy()" in TEXT
    assert 'RuntimeError("unexpected Laplacian energy")' in TEXT
    assert 'RuntimeError("unexpected edge energy contributions")' in TEXT
    assert 'RuntimeError("energy should not depend on orientation")' in TEXT


def test_vertex_numerals_use_high_contrast_black():
    assert "vertex: MathTex(str(vertex), font_size=29, color=BLACK)" in TEXT


def test_scene_begins_with_local_laplacian_output_and_global_question():
    assert "Lx gives one neighbor-comparison total at each vertex" in TEXT
    assert '"LOCAL COMPARISONS"' in TEXT
    assert r"L\mathbf x=(-3,0,2,1)^T" in TEXT
    assert "one number for variation across the whole graph" in TEXT


def test_scene_introduces_quadratic_form_as_a_scalar():
    assert r"\mathbf x^TL\mathbf x=" in TEXT
    assert r"\mathbf x^T(L\mathbf x)=(1,2,3,4)\cdot(-3,0,2,1)=7" in TEXT
    assert "This scalar is called the Laplacian energy of x." in TEXT
    assert "return Matrix(entries" in TEXT


def test_scene_factors_energy_through_incidence_matrix():
    assert "Substitute L equals B-transpose B" in TEXT
    assert r"=\mathbf x^TB^TB\mathbf x" in TEXT
    assert r"=(B\mathbf x)^T(B\mathbf x)" in TEXT
    assert r"=\lVert B\mathbf x\rVert^2" in TEXT
    assert "squared length of the edge-difference vector" in TEXT


def test_scene_computes_exact_sum_of_four_squares():
    assert r"B\mathbf x=" in TEXT
    assert r'[["1"], ["1"], ["2"], ["1"]]' in TEXT
    assert r"\lVert B\mathbf x\rVert^2=1^2+1^2+2^2+1^2" in TEXT
    assert r"=1+1+4+1=7" in TEXT
    assert "Squares keep every contribution nonnegative." in TEXT


def test_scene_attaches_each_contribution_to_one_graph_edge():
    for term in (
        r"(1-2)^2=1",
        r"(2-3)^2=1",
        r"(1-3)^2=4",
        r"(3-4)^2=1",
    ):
        assert term in TEXT
    assert '"TOTAL EDGE VARIATION"' in TEXT
    assert "large jumps count more" in TEXT
    assert ".set_stroke(width=9.0)" in TEXT


def test_scene_states_general_energy_identity_and_orientation_independence():
    identity = r"\mathbf x^TL\mathbf x=\lVert B\mathbf x\rVert^2"
    edge_sum = r"=\sum_{\{i,j\}\in E}(x_i-x_j)^2"
    assert identity in TEXT
    assert edge_sum in TEXT
    assert "Each undirected edge is included exactly once." in TEXT
    assert "the difference changes sign, but its square does not" in TEXT


def test_scene_proves_positive_semidefiniteness_from_definition():
    assert '"POSITIVE SEMIDEFINITE"' in TEXT
    assert r"\mathbf x^TM\mathbf x\ge0\ \text{for every }\mathbf x" in TEXT
    assert r"\sum_{\{i,j\}\in E}(x_i-x_j)^2\ge0" in TEXT
    assert r"L\ \text{is positive semidefinite}" in TEXT


def test_scene_characterizes_zero_energy_only_for_current_connected_graph():
    assert "On this connected graph, zero energy forces every vertex value to agree." in TEXT
    assert '"ENERGY ZERO"' in TEXT
    assert r"(x_i-x_j)^2=0" in TEXT
    assert '"ENDPOINTS AGREE"' in TEXT
    assert r"\mathbf x=c\mathbf 1" in TEXT


def test_scene_distinguishes_local_balance_from_zero_energy_and_previews_components():
    assert "Local cancellation can give (Lx)i = 0" in TEXT
    assert "energy zero requires every edge difference to vanish" in TEXT
    assert "What changes when the graph has more than one connected component?" in TEXT
    assert "eigenvalue" not in TEXT.lower()

