from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "spectral_graph_partition_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "The Fiedler Vector and Spectral Partitioning"' in TEXT
    assert r"\textbf{The Fiedler Vector and Spectral Partitioning}" in TEXT


def test_scene_uses_renderer_independent_model_and_exact_cut_spine():
    assert "from engine.spectral_graph_partition import SpectralGraphPartition" in TEXT
    assert "model = SpectralGraphPartition()" in TEXT
    assert 'RuntimeError("unexpected sign partition")' in TEXT
    assert 'RuntimeError("unexpected Fiedler cut")' in TEXT
    assert 'RuntimeError("unexpected sweep scores")' in TEXT
    assert 'RuntimeError("unexpected best sweep partition")' in TEXT


def test_vertex_numerals_use_high_contrast_black():
    assert "vertex: MathTex(str(vertex), font_size=29, color=BLACK)" in TEXT


def test_scene_recalls_exact_fiedler_coordinates_on_graph():
    assert '"FIEDLER VECTOR"' in TEXT
    assert r"\mathbf v_2=(1,1,0,-2)^T" in TEXT
    assert "the λ₂ eigenvector" in TEXT
    assert "bridge permits the largest change" in TEXT
    assert ".set_stroke(width=9)" in TEXT


def test_scene_states_zero_threshold_convention_explicitly():
    assert "Use zero as a threshold" in TEXT
    assert '"NONNEGATIVE SIDE"' in TEXT
    assert r"S=\{1,2,3\}" in TEXT
    assert "assign the zero here" in TEXT
    assert r"T=\{4\}" in TEXT
    assert "This is one candidate partition." in TEXT


def test_scene_defines_cut_edges_and_counts_bridge_cut():
    assert "A cut edge has one endpoint in each proposed group." in TEXT
    assert r"\operatorname{cut}(S,T)=1" in TEXT
    assert 'edges[(3, 4)]' in TEXT
    assert ".set_stroke(width=11)" in TEXT


def test_scene_compares_two_edge_alternative_cut():
    assert "different grouping cuts two edges" in TEXT
    assert r"S=\{1,2\},\quad T=\{3,4\}" in TEXT
    assert r"\operatorname{cut}(S,T)=2" in TEXT
    assert "crossing edges: {1,3} and {2,3}" in TEXT


def test_scene_introduces_ratio_cut_from_first_principles():
    assert "counts crossing edges while also accounting for group sizes" in TEXT
    assert r"\operatorname{RatioCut}(S,T)=\operatorname{cut}(S,T)" in TEXT
    assert r"1\left(\frac13+1\right)=\frac43" in TEXT
    assert r"2\left(\frac12+\frac12\right)=2" in TEXT


def test_scene_connects_discrete_cut_vector_to_rayleigh_quotient():
    assert "two constants chosen to make the coordinates sum to zero" in TEXT
    assert r'[[r"\frac13"], [r"\frac13"], [r"\frac13"], ["-1"]]' in TEXT
    assert r"\mathbf z^T\mathbf 1=0" in TEXT
    assert r"=\frac{16/9}{4/3}=\frac43" in TEXT
    assert r"=\operatorname{RatioCut}(S,T)" in TEXT


def test_scene_explains_continuous_relaxation():
    assert "replaces a discrete search with a continuous one" in TEXT
    assert '"DISCRETE CUT VECTORS"' in TEXT
    assert '"ALL REAL VECTORS"' in TEXT
    assert r"\mathbf x\perp\mathbf 1" in TEXT
    assert r"=\lambda_2,\qquad \text{minimizer }\mathbf v_2" in TEXT


def test_scene_sweeps_only_distinct_fiedler_coordinates():
    assert "thresholds only between distinct values" in TEXT
    assert r"v_4=-2\quad<\quad v_3=0\quad<\quad v_1=v_2=1" in TEXT
    assert r"\{4\}\mid\{1,2,3\}" in TEXT
    assert r"\{3,4\}\mid\{1,2\}" in TEXT
    assert "Best sweep cut: {4} | {1,2,3}" in TEXT


def test_scene_synthesizes_method_with_scope_caution_and_electrical_preview():
    assert '"1. SOLVE"' in TEXT
    assert '"2. SWEEP"' in TEXT
    assert '"3. SCORE"' in TEXT
    assert "does not promise the best cut for every objective" in TEXT
    assert "What if vertex values represent electrical potentials?" in TEXT
