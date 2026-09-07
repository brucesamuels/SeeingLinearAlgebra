from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "graph_random_walk_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "Random Walks and Markov Chains"' in TEXT
    assert r"\textbf{Random Walks and Markov Chains}" in TEXT


def test_scene_uses_renderer_independent_model_and_exact_spine():
    assert "from engine.graph_random_walk import GraphRandomWalk" in TEXT
    assert "model = GraphRandomWalk()" in TEXT
    assert 'RuntimeError("unexpected random-walk trajectory")' in TEXT
    assert 'RuntimeError("unexpected stationary distribution")' in TEXT
    assert 'RuntimeError("unexpected convergence behavior")' in TEXT
    assert 'RuntimeError("unexpected Laplacian connection")' in TEXT


def test_vertex_numerals_use_high_contrast_black():
    assert "vertex: MathTex(str(vertex), font_size=29, color=BLACK)" in TEXT


def test_scene_defines_random_walk_and_markov_idea_from_first_principles():
    assert "chooses one neighboring vertex at each step" in TEXT
    assert '"CURRENT VERTEX"' in TEXT
    assert '"NEXT STEP"' in TEXT
    assert "choose one neighbor uniformly" in TEXT
    assert "probability 1/3 for each" in TEXT
    assert "Only the current vertex matters: the Markov property." in TEXT


def test_scene_connects_degrees_to_exact_one_step_probabilities():
    assert "degree tells us how many equally likely choices" in TEXT
    assert r"\frac1{d_1}=\frac12" in TEXT
    assert r"\frac1{d_3}=\frac13" in TEXT
    assert r"\frac1{d_4}=1" in TEXT
    assert ").scale(0.86).to_edge(RIGHT, buff=0.43).shift(DOWN * 0.32)" in TEXT


def test_scene_builds_column_stochastic_transition_matrix_structurally():
    assert "Column j records where probability moves" in TEXT
    assert r"P=A D^{-1}" in TEXT
    assert "transition.get_columns()" in TEXT
    assert "We use column probability vectors." in TEXT
    assert r"p_{k+1}=Pp_k" in TEXT
    assert "Every column sums to 1." in TEXT
    assert "v_buff=1.16" in TEXT
    assert 'entry.get_tex_string() in {"0", "1"}' in TEXT
    assert "entry.shift(UP * 0.22)" in TEXT


def test_scene_introduces_probability_distribution_concretely():
    assert "records how likely the walker is to be at each vertex" in TEXT
    assert r"p_0=(0,0,0,1)^T" in TEXT
    assert "certain to start at vertex 4" in TEXT
    assert r"p_1=Pp_0=(0,0,1,0)^T" in TEXT
    assert "nonnegative" in TEXT
    assert "sum to 1" in TEXT


def test_scene_animates_exact_probability_spreading():
    assert "moves and recombines all the probability mass" in TEXT
    assert r"p_2=\left(\frac13,\frac13,0,\frac13\right)^T" in TEXT
    assert r"p_3=\left(\frac16,\frac16,\frac23,0\right)^T" in TEXT
    assert r"p_4=\left(\frac{11}{36},\frac{11}{36},\frac16,\frac29\right)^T" in TEXT
    assert "Transform(marks, new_marks)" in TEXT


def test_scene_defines_and_verifies_stationarity():
    assert "looks unchanged after one more step" in TEXT
    assert '"STATIONARY"' in TEXT
    assert r"P\pi=\pi" in TEXT
    assert r"\pi=\left(\frac14,\frac14,\frac38,\frac18\right)^T" in TEXT


def test_scene_explains_degree_proportional_stationary_distribution():
    assert "higher-degree vertices receive more probability traffic" in TEXT
    assert r"(d_1,d_2,d_3,d_4)=(2,2,3,1)" in TEXT
    assert r"\pi_i=\frac{d_i}{2|E|}=\frac{d_i}{8}" in TEXT
    assert "Degree 3 gets the largest share" in TEXT
    assert "direction, buff=0.68" in TEXT


def test_scene_connects_stationarity_to_laplacian_null_space():
    assert "another form of the Laplacian null-space equation" in TEXT
    assert r"A D^{-1}\pi=\pi" in TEXT
    assert r"L D^{-1}\pi=0" in TEXT
    assert r"D^{-1}\pi=\frac18\mathbf 1" in TEXT
    assert r"L\mathbf 1=0" in TEXT


def test_scene_qualifies_convergence_and_previews_ranking():
    assert "For this connected graph with an odd cycle" in TEXT
    assert '"MOVE"' in TEXT
    assert '"PRESERVE"' in TEXT
    assert '"SETTLE"' in TEXT
    assert r"p_{24}\approx" in TEXT
    assert "directed links and occasional jumps" in TEXT


def test_bottom_text_uses_safe_spacing():
    assert "to_edge(DOWN, buff=0.72)" in TEXT
    assert "to_edge(DOWN, buff=0.68)" in TEXT
