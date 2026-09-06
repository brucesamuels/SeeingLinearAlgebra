from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "graph_incidence_encoding_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "The Incidence Matrix: Edges Meet Vertices"' in TEXT
    assert r"\textbf{The Incidence Matrix: Edges Meet Vertices}" in TEXT


def test_vertex_numerals_contrast_with_yellow_and_highlighted_vertices():
    assert "vertex: MathTex(str(vertex), font_size=29, color=BLACK)" in TEXT


def test_scene_uses_renderer_independent_model_and_exact_numerical_spine():
    assert "from engine.graph_incidence_encoding import GraphIncidenceEncoding" in TEXT
    assert "model = GraphIncidenceEncoding()" in TEXT
    assert 'RuntimeError("unexpected incidence matrix")' in TEXT
    assert 'RuntimeError("unexpected oriented edge differences")' in TEXT


def test_scene_distinguishes_bookkeeping_orientation_from_graph_direction():
    assert "An undirected edge has no built-in direction, but we may choose one." in TEXT
    assert '"CHOSEN ORIENTATION"' in TEXT
    assert "bookkeeping for each edge" in TEXT
    assert "The underlying graph is still undirected." in TEXT
    assert "unchanged.scale_to_fit_width(4.45)" in TEXT


def test_scene_declares_edge_and_vertex_orders_and_general_shape():
    assert '"EDGE ORDER"' in TEXT
    assert r"e_1:1\to2\qquad e_2:2\to3" in TEXT
    assert r"e_3:1\to3\qquad e_4:3\to4" in TEXT
    assert '"VERTEX ORDER"' in TEXT
    assert r"B:\ m\text{ edges}\times n\text{ vertices}" in TEXT
    assert "Here m = n = 4, only by coincidence." in TEXT


def test_scene_introduces_tail_head_and_zero_rule_before_full_matrix():
    assert "minus one at its tail and plus one at its head" in TEXT
    assert '"TAIL"' in TEXT
    assert '"HEAD"' in TEXT
    assert '"OTHER"' in TEXT
    assert r'[["-1", "1", "0", "0"]]' in TEXT
    assert "entry_cards.scale_to_fit_width(6.0)" in TEXT


def test_scene_builds_structural_matrix_one_edge_row_at_a_time():
    assert "return Matrix(entries" in TEXT
    assert "incidence.get_brackets()" in TEXT
    assert "for number, ((tail, head), matrix_row, row_label)" in TEXT
    assert "FadeIn(matrix_row)" in TEXT
    assert "Every row has one -1, one +1, and zeros elsewhere." in TEXT


def test_scene_interprets_rows_and_columns():
    assert "Rows describe edges; columns collect one vertex's roles across edges." in TEXT
    assert '"ROW e3"' in TEXT
    assert '"COLUMN v3"' in TEXT
    assert "head twice; tail once" in TEXT


def test_scene_makes_vertex_measurements_and_edge_difference_action_concrete():
    assert "Attach a measurement to each vertex" in TEXT
    assert r"x_1=1" in TEXT
    assert r"x_4=4" in TEXT
    assert r"(B\mathbf x)_3" in TEXT
    assert r"=x_{\rm head}-x_{\rm tail}" in TEXT
    assert r"=x_3-x_1=3-1=2" in TEXT
    assert "This is an oriented edge difference." in TEXT


def test_scene_computes_all_four_edge_differences():
    assert "One matrix-vector product computes all four edge differences." in TEXT
    assert r"B\mathbf x=" in TEXT
    for calculation in (
        r"e_1:\ 2-1=1",
        r"e_2:\ 3-2=1",
        r"e_3:\ 3-1=2",
        r"e_4:\ 4-3=1",
    ):
        assert calculation in TEXT


def test_scene_shows_reorientation_negates_one_row_and_difference_only():
    assert "Reversing an arrow changes a sign, not the underlying graph." in TEXT
    assert '"CHOSEN 1 TO 3"' in TEXT
    assert '"REVERSED 3 TO 1"' in TEXT
    assert r"[-1\ 0\ 1\ 0]\mathbf x=2" in TEXT
    assert r"[1\ 0\ {-1}\ 0]\mathbf x=-2" in TEXT
    assert r"|2|=|-2|" in TEXT


def test_scene_closes_with_constant_signal_and_transpose_bridge():
    assert r"B\mathbf 1=\mathbf 0" in TEXT
    assert "Equal vertex values create zero difference on every edge." in TEXT
    assert "B-transpose sends edge differences back to the vertices" in TEXT
    assert "B^TB" not in TEXT
