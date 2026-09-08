from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "graph_fundamental_subspaces_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chrome_and_graph_specific_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "The Fundamental Subspaces of a Graph"' in TEXT
    assert r"\textbf{The Fundamental Subspaces of a Graph}" in TEXT


def test_scene_validates_renderer_independent_graph_results():
    assert "GraphFundamentalSubspaces()" in TEXT
    assert "GraphFundamentalSubspaces.without_edge((3, 4))" in TEXT
    assert "GraphFundamentalSubspaces.without_edge((1, 3))" in TEXT
    assert 'RuntimeError("unexpected incidence dimensions")' in TEXT
    assert 'RuntimeError("unexpected bridge deletion")' in TEXT
    assert 'RuntimeError("unexpected cycle deletion")' in TEXT
    assert 'RuntimeError("unexpected edge differences")' in TEXT
    assert 'RuntimeError("unexpected cycle circulation")' in TEXT
    assert 'RuntimeError("unexpected Laplacian reachability")' in TEXT


def test_opening_places_four_subspaces_in_vertex_and_edge_spaces():
    assert "incidence matrix" in TEXT
    assert "VERTEX SPACE" in TEXT
    assert "EDGE SPACE" in TEXT
    assert '"ROW SPACE"' in TEXT
    assert '"NULL SPACE"' in TEXT
    assert '"COLUMN SPACE"' in TEXT
    assert '"LEFT NULL SPACE"' in TEXT
    assert "take edge differences" in TEXT


def test_null_space_records_connected_components():
    assert r"B(a,a,a,a)^T=0" in TEXT
    assert r"\operatorname{Null}(B)=\operatorname{span}\{\mathbf1\}" in TEXT
    assert "Equality propagates along paths" in TEXT
    assert r"\dim\operatorname{Null}(B)=1" in TEXT
    assert "one connected component" in TEXT


def test_bridge_deletion_creates_second_component_direction():
    assert "Deleting the bridge creates a second independent component constant" in TEXT
    assert r"x=(a,a,a,b)^T" in TEXT
    assert r"\operatorname{Null}(B_{\rm split})" in TEXT
    assert r"\dim\operatorname{Null}(B)=c" in TEXT


def test_row_space_is_interpreted_as_balanced_vertex_contrasts():
    assert "Row(B) contains the vertex contrasts" in TEXT
    assert r"\operatorname{Row}(B)=\operatorname{Null}(B)^\perp" in TEXT
    assert r"\mathbf1^Tz=0" in TEXT
    assert '"BALANCED"' in TEXT


def test_column_space_is_interpreted_as_compatible_edge_differences():
    assert "Col(B) contains exactly the edge differences" in TEXT
    assert r"Bx=(1,1,2,1)^T\in\operatorname{Col}(B)" in TEXT
    assert r"(x_2-x_1)+(x_3-x_2)-(x_3-x_1)=0" in TEXT
    assert '"CYCLE CONSISTENCY"' in TEXT


def test_left_null_space_is_interpreted_as_cycle_circulation():
    assert "circulate without accumulating" in TEXT
    assert r"q=(1,1,-1,0)^T" in TEXT
    assert r"B^Tq=0" in TEXT
    assert '"CYCLE SPACE"' in TEXT
    assert "one independent circulation" in TEXT


def test_dimension_formulas_count_components_and_cycles():
    assert r"\operatorname{rank}(B)=n-c" in TEXT
    assert r"\dim\operatorname{Null}(B)=c" in TEXT
    assert r"\dim\operatorname{Null}(B^T)=m-n+c" in TEXT
    assert '"TRIANGLE WITH TAIL"' in TEXT
    assert '"DELETE THE BRIDGE"' in TEXT
    assert '"DELETE A TRIANGLE EDGE"' in TEXT


def test_vertex_and_edge_spaces_receive_graph_specific_decompositions():
    assert r"\mathbb R^V=\operatorname{Row}(B)\oplus\operatorname{Null}(B)" in TEXT
    assert r"\mathbb R^E=\operatorname{Col}(B)\oplus\operatorname{Null}(B^T)" in TEXT
    assert '"CONTRASTS"' in TEXT
    assert '"COMPONENT CONSTANTS"' in TEXT
    assert '"GRADIENTS"' in TEXT
    assert '"CIRCULATIONS"' in TEXT


def test_laplacian_inherits_incidence_spaces():
    assert r"L=B^TB=L^T" in TEXT
    assert r"\operatorname{Null}(L)=\operatorname{Null}(B)" in TEXT
    assert r"\operatorname{Col}(L)=\operatorname{Row}(B)" in TEXT
    assert r"\operatorname{Col}(L)=\mathbf1^\perp" in TEXT


def test_final_card_connects_subspaces_to_laplacian_systems():
    assert r"Lv=b\iff\mathbf1^Tb=0" in TEXT
    assert r"v\mapsto v+c\mathbf1" in TEXT
    assert "total injection must balance" in TEXT
    assert "constant shifts change no edge difference" in TEXT
    assert "graph structure into linear-algebraic structure" in TEXT


def test_scene_has_ten_cards_high_contrast_vertices_and_safe_close():
    assert TEXT.count("# Card ") == 10
    assert "color=BLACK" in TEXT
    assert "font_size=29" in TEXT
    assert "Next: assemble the graph" in TEXT
