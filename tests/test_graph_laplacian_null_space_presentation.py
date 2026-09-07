from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "graph_laplacian_null_space_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "Connected Components and the Laplacian Null Space"' in TEXT
    assert r"\textbf{Connected Components and the Laplacian Null Space}" in TEXT


def test_scene_uses_renderer_independent_model_and_exact_component_spine():
    assert "from engine.graph_laplacian_null_space import GraphLaplacianNullSpace" in TEXT
    assert "model = GraphLaplacianNullSpace()" in TEXT
    assert "GraphLaplacianNullSpace(triangle_with_tail_graph())" in TEXT
    assert 'RuntimeError("unexpected connected components")' in TEXT
    assert 'RuntimeError("unexpected componentwise-constant signal")' in TEXT
    assert 'RuntimeError("unexpected Laplacian null vector")' in TEXT


def test_vertex_numerals_use_high_contrast_black():
    assert "vertex: MathTex(str(vertex), font_size=29, color=BLACK)" in TEXT


def test_scene_recalls_connected_zero_energy_case():
    assert "On a connected graph, zero energy forced one constant" in TEXT
    assert r"\operatorname{Null}(L)=\operatorname{span}\{\mathbf 1\}" in TEXT
    assert "one connected component, one free constant" in TEXT


def test_scene_removes_bridge_and_labels_two_components():
    assert "Remove the bridge" in TEXT
    assert 'bridge = edges[(3, 4)]' in TEXT
    assert r"C_1=\{1,2,3\}" in TEXT
    assert r"C_2=\{4\}" in TEXT
    assert "two connected components" in TEXT


def test_scene_shows_independent_constants_have_zero_energy():
    assert "their constants may differ" in TEXT
    assert r"\mathbf x=(a,a,a,b)^T" in TEXT
    assert r"(a-a)^2=0" in TEXT
    assert "No edge compares a with b." in TEXT


def test_scene_structurally_verifies_laplacian_null_equation():
    for row in (
        '["2", "-1", "-1", "0"]',
        '["-1", "2", "-1", "0"]',
        '["-1", "-1", "2", "0"]',
        '["0", "0", "0", "0"]',
    ):
        assert row in TEXT
    assert '[["a"], ["a"], ["a"], ["b"]]' in TEXT
    assert "isolated vertex has a zero row" in TEXT


def test_scene_constructs_component_indicator_basis():
    assert r"\mathbf u_1=" in TEXT
    assert r"\mathbf u_2=" in TEXT
    assert '[["1"], ["1"], ["1"], ["0"]]' in TEXT
    assert '[["0"], ["0"], ["0"], ["1"]]' in TEXT
    assert "1 on its component and 0 elsewhere" in TEXT


def test_scene_spans_all_componentwise_constant_null_vectors():
    assert "Scale and add the component indicators" in TEXT
    assert r"\operatorname{Null}(L_{\rm split})=\operatorname{span}\{\mathbf u_1,\mathbf u_2\}" in TEXT
    assert "nullity 2" in TEXT


def test_scene_proves_both_directions_from_energy_and_incidence():
    assert "energy identity proves both directions" in TEXT
    assert '"IF Lx = 0"' in TEXT
    assert r"0=\mathbf x^TL\mathbf x=\sum_{\{i,j\}\in E}(x_i-x_j)^2" in TEXT
    assert '"IF x IS CONSTANT ON EACH COMPONENT"' in TEXT
    assert r"B\mathbf x=\mathbf 0\quad\Longrightarrow\quad L\mathbf x=B^TB\mathbf x=\mathbf 0" in TEXT


def test_scene_compares_connected_and_split_nullities():
    assert '"CONNECTED GRAPH"' in TEXT
    assert '"SPLIT GRAPH"' in TEXT
    assert "1 component  →  nullity 1" in TEXT
    assert "2 components  →  nullity 2" in TEXT
    assert "additional independent zero direction" in TEXT


def test_scene_states_general_component_nullity_theorem_and_previews_spectrum():
    assert "COMPONENT–NULLITY THEOREM" in TEXT
    assert r"\operatorname{Null}(L)=\{\text{vectors constant on each component}\}" in TEXT
    assert r"\dim\operatorname{Null}(L)=\text{number of connected components}" in TEXT
    assert "Each component contributes one independent zero direction." in TEXT
    assert "first positive eigenvalue" in TEXT
