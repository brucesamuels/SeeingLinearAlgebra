from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "graph_chapter_synthesis_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chrome_and_synthesis_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "Graphs, Networks, and the Laplacian: The Big Picture"' in TEXT
    assert r"\textbf{Graphs, Networks, and the Laplacian: The Big Picture}" in TEXT


def test_scene_validates_renderer_independent_results():
    assert "GraphChapterSynthesis()" in TEXT
    assert 'RuntimeError("unexpected walk count")' in TEXT
    assert 'RuntimeError("unexpected edge differences")' in TEXT
    assert 'RuntimeError("unexpected Laplacian response")' in TEXT
    assert 'RuntimeError("unexpected Laplacian energy")' in TEXT
    assert 'RuntimeError("unexpected Laplacian spectrum")' in TEXT
    assert 'RuntimeError("unexpected PageRank order")' in TEXT


def test_scene_reassembles_matrix_and_operator_spine():
    assert '"CONNECTIONS"' in TEXT
    assert '"DIFFERENCES"' in TEXT
    assert '"VARIATION"' in TEXT
    assert '"PROBABILITY"' in TEXT
    assert r"(A^2)_{14}=1" in TEXT
    assert r"L=B^TB=D-A" in TEXT
    assert r"x^TLx=\|Bx\|^2" in TEXT


def test_scene_connects_subspaces_spectrum_and_partition():
    assert r"\operatorname{Null}(B)" in TEXT
    assert r"\operatorname{Col}(B)" in TEXT
    assert r"\operatorname{Null}(B^T)" in TEXT
    assert r"\operatorname{rank}(B)=n-c=3" in TEXT
    assert r"\operatorname{spec}(L)=(0,1,3,4)" in TEXT
    assert '"FIEDLER SWEEP"' in TEXT
    assert r"\operatorname{RatioCut}=\frac43" in TEXT


def test_scene_revisits_electrical_probability_and_directed_applications():
    assert r"Lv=b" in TEXT
    assert r"R_{\rm eff}(4,1)=\frac53" in TEXT
    assert r"P=AD^{-1}" in TEXT
    assert r"P\pi=\pi" in TEXT
    assert r"G=\frac12S+\frac12U" in TEXT
    assert r"Gr=r" in TEXT
    assert r"3>2>1=4" in TEXT
    assert "displayed_edge = (3, 1) if directed" in TEXT


def test_scene_ends_with_question_driven_recognition_guide():
    assert '"CONNECTIONS AND ROUTES"' in TEXT
    assert '"DIFFERENCES AND ENERGY"' in TEXT
    assert '"STRUCTURE AND FLOW"' in TEXT
    assert '"MOVEMENT AND RANK"' in TEXT
    assert "Choose a graph matrix by asking" in TEXT
    assert "Next: assemble and review the complete chapter" in TEXT


def test_scene_has_ten_cards_high_contrast_vertices_and_safe_close():
    assert TEXT.count("# Card ") == 10
    assert "color=BLACK" in TEXT
    assert "font_size=29" in TEXT
    assert "FadeOut(mobject) for mobject in self.mobjects" in TEXT
