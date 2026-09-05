from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "graph_vocabulary_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_opens_graph_chapter_with_vocabulary_first_title():
    assert "GRAPHS, NETWORKS, AND THE LAPLACIAN" in TEXT
    assert "What Is a Graph? Objects, Connections, and Routes" in TEXT
    assert "What information remains" in TEXT


def test_scene_introduces_vertices_and_edges_before_algebraic_encoding():
    assert '"VERTEX"' in TEXT
    assert '"EDGE"' in TEXT
    assert r"G=(V,E)" in TEXT
    assert r"V=\{1,2,3,4\}" in TEXT
    assert r"E=\{\{1,2\},\{2,3\},\{1,3\},\{3,4\}\}" in TEXT
    assert "Matrix(" not in TEXT
    assert "adjacency matrix" not in TEXT.lower()


def test_card_two_raises_note_and_shows_it_before_graph_rearrangement():
    assert ").arrange(DOWN, buff=0.21).to_edge(DOWN, buff=0.72)" in TEXT
    note_animation = TEXT.index("FadeIn(geometry_note)")
    rearrangement = TEXT.index("ReplacementTransform(graph, alternate)")
    assert note_animation < rearrangement


def test_scene_explains_neighbors_and_degree_on_the_recurring_graph():
    assert '"ADJACENT"' in TEXT
    assert r"N(3)=\{1,2,4\}" in TEXT
    assert '"DEGREE"' in TEXT
    assert r"d_1=2,\quad d_2=2" in TEXT
    assert r"d_3=3,\quad d_4=1" in TEXT
    assert "degree sequence: 2, 2, 3, 1" in TEXT


def test_scene_distinguishes_walks_paths_and_edge_counting():
    assert '"WALK"' in TEXT
    assert r"4\to3\to1\to2\to3\to1" in TEXT
    assert "vertices and edges may repeat" in TEXT
    assert "length = 5 edges" in TEXT
    assert '"PATH"' in TEXT
    assert r"4\to3\to1\to2" in TEXT
    assert "no repeated vertices" in TEXT
    assert "length = 3 edges" in TEXT


def test_walk_and_path_markers_are_prominent_and_move_slowly():
    assert TEXT.count("radius=0.14") == 2
    assert TEXT.count("set_stroke(WHITE, width=2.6)") == 2
    assert "run_time=0.75" in TEXT
    assert "run_time=0.85" in TEXT


def test_scene_builds_connectedness_before_connected_components():
    connected = TEXT.index('"CONNECTED"')
    components = TEXT.index("connected components")
    assert connected < components
    assert "every pair has a path between it" in TEXT
    assert r"\{1,2,3\}" in TEXT
    assert r"\{4\}" in TEXT
    assert "Two components" in TEXT


def test_scene_closes_with_next_representation_question_and_no_checkpoint_labels():
    assert "Can zeros and ones store exactly the same connections?" in TEXT
    assert '"OBJECTS"' in TEXT
    assert '"CONNECTIONS"' in TEXT
    assert '"ROUTES"' in TEXT
    assert ").arrange(RIGHT, buff=0.36).to_edge(DOWN, buff=0.62)" in TEXT
    assert "CP226" not in TEXT
    assert "checkpoint" not in TEXT.lower()
