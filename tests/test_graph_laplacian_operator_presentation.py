from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "graph_laplacian_operator_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "The Graph Laplacian: Differences Return"' in TEXT
    assert r"\textbf{The Graph Laplacian: Differences Return}" in TEXT


def test_scene_uses_renderer_independent_model_and_exact_spine():
    assert "from engine.graph_laplacian_operator import GraphLaplacianOperator" in TEXT
    assert "model = GraphLaplacianOperator()" in TEXT
    assert 'RuntimeError("unexpected graph Laplacian")' in TEXT
    assert 'RuntimeError("unexpected Laplacian action")' in TEXT
    assert 'RuntimeError("Laplacian should not depend on orientation")' in TEXT


def test_vertex_numerals_use_high_contrast_black():
    assert "vertex: MathTex(str(vertex), font_size=29, color=BLACK)" in TEXT


def test_scene_recalls_vertex_to_edge_action_before_introducing_transpose():
    assert "B sends vertex values to oriented differences on the edges." in TEXT
    assert '"VERTEX VALUES"' in TEXT
    assert r"\mathbf x=(1,2,3,4)^T" in TEXT
    assert '"EDGE DIFFERENCES"' in TEXT
    assert r"B\mathbf x=(1,1,2,1)^T" in TEXT


def test_scene_explains_b_transpose_as_signed_return_to_vertices():
    assert "B-transpose gathers signed edge values back at each vertex." in TEXT
    assert r"B^T" in TEXT
    assert r"\text{at }v_1:\quad -1-2=-3" in TEXT
    assert "Outgoing differences subtract; incoming differences add." in TEXT


def test_scene_names_laplacian_only_after_showing_composition():
    assert "vertices to edges, then edges to vertices" in TEXT
    assert '"THE GRAPH LAPLACIAN"' in TEXT
    assert r"L=B^TB" in TEXT
    assert TEXT.index("vertices to edges, then edges to vertices") < TEXT.index('"THE GRAPH LAPLACIAN"')


def test_scene_multiplies_structural_matrices():
    assert "return Matrix(entries" in TEXT
    assert r"L=B^TB=" in TEXT
    assert "scale=0.51, h_buff=0.69, v_buff=0.61" in TEXT
    assert "scale=0.60, h_buff=0.74, v_buff=0.64" in TEXT
    assert "vertex by edge" in TEXT
    assert "edge by vertex" in TEXT
    assert "vertex by vertex" in TEXT


def test_scene_reads_laplacian_from_degrees_and_adjacency():
    assert "degrees on the diagonal and minus ones on edges" in TEXT
    assert '"DIAGONAL"' in TEXT
    assert r"L_{ii}=\deg(v_i)" in TEXT
    assert '"OFF DIAGONAL"' in TEXT
    assert r"L_{ij}=-1" in TEXT
    assert r"L=D-A" in TEXT


def test_scene_interprets_one_coordinate_as_neighbor_differences():
    assert "compares one vertex value with all of its neighbors" in TEXT
    assert '"AT VERTEX 1"' in TEXT
    assert r"(L\mathbf x)_1" in TEXT
    assert r"=(x_1-x_2)+(x_1-x_3)" in TEXT
    assert r"=(1-2)+(1-3)=-3" in TEXT
    assert "Compare with each neighbor, then add." in TEXT


def test_scene_computes_full_action_and_explains_zero_coordinate():
    assert "all local neighbor comparisons in one matrix-vector product" in TEXT
    assert r"L\mathbf x=" in TEXT
    assert r'[["-3"], ["0"], ["2"], ["1"]]' in TEXT
    assert r"v_2:\ (2-1)+(2-3)=0" in TEXT
    assert "Zero at v2 means its neighbor comparisons balance." in TEXT


def test_scene_demonstrates_orientation_cancellation():
    assert "Reverse a bookkeeping arrow: both signs flip, so L stays unchanged." in TEXT
    assert '"ORIGINAL ROW"' in TEXT
    assert '"REVERSED ROW"' in TEXT
    assert "edge difference = 2" in TEXT
    assert "edge difference = -2" in TEXT
    assert r"(-\mathbf b_3)^T(-\mathbf b_3)=\mathbf b_3^T\mathbf b_3" in TEXT
    assert r"B'^TB'=B^TB=L" in TEXT


def test_scene_closes_with_constant_null_vector_and_energy_bridge():
    assert r"L\mathbf 1=\mathbf 0" in TEXT
    assert "A constant value has no differences across any edge." in TEXT
    assert "Can one number measure the total variation across all edges?" in TEXT
    assert r"x^TLx" not in TEXT
