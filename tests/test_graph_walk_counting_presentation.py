from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "graph_walk_counting_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "Matrix Powers Count Walks"' in TEXT
    assert r"\textbf{GRAPHS, NETWORKS, AND THE LAPLACIAN}" in TEXT
    assert r"\textbf{Matrix Powers Count Walks}" in TEXT


def test_scene_uses_renderer_independent_model_and_checks_exact_powers():
    assert "from engine.graph_walk_counting import GraphWalkCounting" in TEXT
    assert "model = GraphWalkCounting()" in TEXT
    assert 'RuntimeError("unexpected square of adjacency matrix")' in TEXT
    assert 'RuntimeError("unexpected cube of adjacency matrix")' in TEXT


def test_scene_recalls_that_walk_length_counts_edges_and_allows_repetition():
    assert "A walk follows edges; its length is the number of edge-steps." in TEXT
    assert r"1\to3\to1" in TEXT
    assert "Length 2 means exactly two edges are used." in TEXT
    assert "exact_note.scale_to_fit_width(4.35)" in TEXT
    assert "vertices may repeat" in TEXT
    assert "Walks may revisit vertices." in TEXT


def test_scene_animates_walks_prominently_and_at_deliberate_speed():
    assert "def _trace_route" in TEXT
    assert "ShowPassingFlash" in TEXT
    assert ".set_stroke(width=9.0)" in TEXT
    assert "marker.animate.move_to" in TEXT
    assert "run_time=0.86" in TEXT
    assert "Circle(radius=0.26" in TEXT
    assert "stroke_width=5.0" in TEXT


def test_scene_connects_adjacency_entries_to_one_step_walks():
    assert "The adjacency matrix already counts walks of length one." in TEXT
    assert r"a_{13}=1" in TEXT
    assert "one direct edge-step" in TEXT
    assert r"a_{14}=0" in TEXT
    assert "no direct edge-step" in TEXT


def test_scene_builds_two_step_counts_through_intermediate_vertices():
    assert "A two-step walk is determined by its intermediate vertex." in TEXT
    assert '"VIA VERTEX 2"' in TEXT
    assert '"VIA VERTEX 3"' in TEXT
    assert r"(A^2)_{11}=" in TEXT
    assert r'MathTex(r"\cdot", font_size=36, color=GREY_B)' in TEXT
    assert r"0\cdot0+1\cdot1+1\cdot1+0\cdot0=2" in TEXT
    assert "The two nonzero products correspond to the two walks." in TEXT


def test_scene_uses_the_unique_two_step_tail_walk_as_second_example():
    assert "From vertex 1 to vertex 4, there is one walk of length two." in TEXT
    assert r"(A^2)_{14}" in TEXT
    assert r"1\to3\to4" in TEXT


def test_scene_displays_square_structurally_and_interprets_entries():
    assert "square = self._matrix" in TEXT
    assert r"A^2=" in TEXT
    assert r"(A^2)_{11}=2" in TEXT
    assert r"(A^2)_{14}=1" in TEXT
    assert r"(A^2)_{34}=0" in TEXT
    assert ").arrange(RIGHT, buff=0.75).to_edge(DOWN, buff=0.70)" in TEXT


def test_scene_uses_a_cube_to_show_four_repeating_walks():
    assert r"A^3=A^2A=" in TEXT
    assert "FOUR THREE-STEP WALKS FROM 1 TO 3" in TEXT
    for route in (
        r"1\to2\to1\to3",
        r"1\to3\to1\to3",
        r"1\to3\to2\to3",
        r"1\to3\to4\to3",
    ):
        assert route in TEXT


def test_scene_states_general_rule_only_after_numerical_examples():
    rule = r"(A^k)_{ij}=\#\{\text{length-}k\text{ walks }i\to j\}"
    assert rule in TEXT
    assert TEXT.index(r"(A^2)_{11}=") < TEXT.index(rule)
    assert '"ONE STEP"' in TEXT
    assert '"APPEND A STEP"' in TEXT
    assert '"K STEPS"' in TEXT
    assert "exactly k edge-steps" in TEXT


def test_scene_uses_structural_matrices_and_reserves_next_topic():
    assert "return Matrix(entries" in TEXT
    assert "Matrix Powers Count Walks" in TEXT
    assert "Next: give each edge an orientation and encode it with signs." in TEXT
    assert "Laplacian" not in TEXT.replace("GRAPHS, NETWORKS, AND THE LAPLACIAN", "")
