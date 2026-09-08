from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "directed_page_rank_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "Directed Graphs and PageRank"' in TEXT
    assert r"\textbf{Directed Graphs and PageRank}" in TEXT


def test_scene_uses_renderer_independent_model_and_exact_spine():
    assert "from engine.directed_page_rank import DirectedPageRank" in TEXT
    assert "model = DirectedPageRank()" in TEXT
    assert 'RuntimeError("unexpected directed graph")' in TEXT
    assert 'RuntimeError("unexpected Google matrix")' in TEXT
    assert 'RuntimeError("unexpected PageRank iteration")' in TEXT
    assert 'RuntimeError("unexpected PageRank vector")' in TEXT
    assert 'RuntimeError("unexpected PageRank residual")' in TEXT


def test_vertex_numerals_use_high_contrast_black():
    assert "vertex: MathTex(str(vertex), font_size=29, color=BLACK)" in TEXT


def test_scene_defines_directed_edge_vocabulary_visually():
    assert "A directed edge is an arrow" in TEXT
    assert '"SOURCE"' in TEXT
    assert "where the arrow begins" in TEXT
    assert '"DESTINATION"' in TEXT
    assert "where the arrow points" in TEXT
    assert r"1\to2\quad\not\Rightarrow\quad2\to1" in TEXT
    assert "Direction is part of the graph's data." in TEXT


def test_scene_defines_out_degree_and_dangling_vertex():
    assert "chooses among outgoing links" in TEXT
    assert r"d_4^{\rm out}=0" in TEXT
    assert "no next link to follow" in TEXT
    assert "called dangling" in TEXT


def test_scene_encodes_raw_link_matrix_and_zero_column_structurally():
    assert "link matrix records destinations by column" in TEXT
    assert r"H=" in TEXT
    assert r"\mathbf 1^TH=(1,1,1,0)" in TEXT
    assert r"H_{\cdot4}=0" in TEXT
    assert "probability would disappear" in TEXT
    assert "v_buff=1.16" in TEXT
    assert "_align_scalar_entries" in TEXT


def test_scene_repairs_dangling_column_uniformly():
    assert "restart uniformly" in TEXT
    assert r"H_{\cdot4}" in TEXT
    assert r"S_{\cdot4}" in TEXT
    assert "equally to all four vertices" in TEXT
    assert r"\mathbf 1^TS=\mathbf 1^T" in TEXT
    assert "v_buff=1.48" in TEXT


def test_scene_introduces_teleportation_and_google_matrix_from_first_principles():
    assert "Teleportation gives every step" in TEXT
    assert '"FOLLOW A LINK"' in TEXT
    assert '"JUMP ANYWHERE"' in TEXT
    assert r"G=\frac12S+\frac12U" in TEXT
    assert r"U=\frac14\mathbf 1\mathbf 1^T" in TEXT
    assert "baseline of 1/8" in TEXT


def test_scene_displays_exact_positive_column_stochastic_google_matrix():
    assert "uniform safety net" in TEXT
    assert '"POSITIVE"' in TEXT
    assert r"G_{ij}>0" in TEXT
    assert '"STOCHASTIC"' in TEXT
    assert r"\mathbf 1^TG=\mathbf 1^T" in TEXT
    assert "v_buff=1.52" in TEXT


def test_scene_animates_exact_early_iterations():
    assert "toward a stable ranking" in TEXT
    assert r"p_0=\left(\frac14,\frac14,\frac14,\frac14\right)^T" in TEXT
    assert r"p_1=Gp_0=\left(\frac7{32},\frac9{32},\frac9{32},\frac7{32}\right)^T" in TEXT
    assert r"p_2=G p_1=\left(\frac{57}{256},\frac{67}{256},\frac{75}{256},\frac{57}{256}\right)^T" in TEXT
    assert "Transform(marks, p1_marks)" in TEXT
    assert "Transform(marks, p2_marks)" in TEXT


def test_scene_defines_page_rank_as_stationary_distribution():
    assert '"PAGERANK"' in TEXT
    assert r"Gr=r" in TEXT
    assert "stationary distribution of G" in TEXT
    assert r"r=\left(\frac{11}{49},\frac{13}{49},\frac27,\frac{11}{49}\right)^T" in TEXT
    assert "larger long-run share of visits" in TEXT


def test_scene_interprets_recursive_support_and_exact_rank_order():
    assert "source divides its support among its exits" in TEXT
    assert r"r_i=\frac12(Sr)_i+\frac18" in TEXT
    assert "link-following support + teleportation baseline" in TEXT
    assert r"3>2>1=4" in TEXT
    assert "buff=0.70" in TEXT


def test_scene_synthesizes_pipeline_and_previews_chapter_synthesis():
    assert '"DIRECT"' in TEXT
    assert '"REPAIR"' in TEXT
    assert '"RANK"' in TEXT
    assert "depends on both the directed links and the chosen teleportation rule" in TEXT
    assert "assemble the chapter's graph, matrix, energy, spectrum, and flow viewpoints" in TEXT


def test_bottom_text_uses_safe_spacing():
    assert "to_edge(DOWN, buff=0.70)" in TEXT
    assert "to_edge(DOWN, buff=0.68)" in TEXT
