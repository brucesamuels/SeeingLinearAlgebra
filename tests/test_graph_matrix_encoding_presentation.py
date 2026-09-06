from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "graph_matrix_encoding_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_graph_chapter_banner_and_matrix_encoding_title():
    assert "GRAPHS, NETWORKS, AND THE LAPLACIAN" in TEXT
    assert "Adjacency and Degree Matrices: From Picture to Array" in TEXT
    assert "Can zeros and ones store exactly the same connections" in TEXT


def test_scene_uses_structural_manim_matrices():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT
    assert "_adjacency_entries" in TEXT


def test_scene_requires_one_matching_row_and_column_order():
    assert '"VERTEX ORDER"' in TEXT
    assert '"ROWS"' in TEXT
    assert '"COLUMNS"' in TEXT
    assert "Changing the order changes the array, but not the graph." in TEXT


def test_scene_defines_adjacency_entries_and_builds_all_rows_from_neighbors():
    assert r"a_{ij}=\begin{cases}" in TEXT
    assert "share an edge" in TEXT
    assert "Each labeled row records one vertex's neighbors." in TEXT
    assert "for vertex, row, row_label in zip" in TEXT
    assert "incident_edges" in TEXT
    assert "model.graph.neighbors(vertex)" in TEXT
    assert "ShowPassingFlash(" in TEXT
    assert "time_width=0.70" in TEXT
    assert "run_time=0.80" in TEXT
    assert 'rf"v_{vertex}"' in TEXT
    assert 'font_size=30, color=ORANGE' in TEXT
    assert r"\text{row 3}=[\,1\quad1\quad0\quad1\,]" in TEXT


def test_scene_connects_graph_structure_to_matrix_structure():
    assert '"UNDIRECTED"' in TEXT
    assert r"a_{ij}=a_{ji}" in TEXT
    assert '"NO LOOPS"' in TEXT
    assert r"a_{ii}=0" in TEXT


def test_scene_recovers_degrees_from_row_sums_and_builds_degree_matrix():
    for equation in (
        r"0+1+1+0=2",
        r"1+0+1+0=2",
        r"1+1+0+1=3",
        r"0+0+1+0=1",
    ):
        assert equation in TEXT
    assert "Multiplying by the all-ones vector adds each row." in TEXT
    assert r"A\mathbf 1=" in TEXT
    assert r"=\mathbf d=D\mathbf 1" in TEXT
    assert "One equation now packages all four row sums." in TEXT
    assert ").arrange(DOWN, buff=0.25).move_to(DOWN * 0.50)" in TEXT


def test_scene_interprets_matrix_vector_multiplication_as_neighbor_sums():
    assert "the product A times x adds neighboring values" in TEXT
    assert r"x_1=1" in TEXT
    assert r"x_4=4" in TEXT
    assert r"(A\mathbf x)_1=x_2+x_3=2+3=5" in TEXT
    assert '"5"], ["4"], ["7"], ["3"' in TEXT
    assert ").to_edge(DOWN, buff=0.74).shift(RIGHT * 2.25)" in TEXT


def test_scene_closes_with_three_views_and_reserves_powers_for_next_lesson():
    assert '"ADJACENCY\\nMATRIX"' in TEXT
    assert '"DEGREE\\nMATRIX"' in TEXT
    assert '"MATRIX\\nACTION"' in TEXT
    assert "What can repeated multiplication by A reveal?" in TEXT
    assert r"A^2" not in TEXT
    assert "CP227" not in TEXT
    assert "checkpoint" not in TEXT.lower()
