from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "electrical_network_laplacian_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chapter_chrome_and_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "Electrical Networks and Laplacian Systems"' in TEXT
    assert r"\textbf{Electrical Networks and Laplacian Systems}" in TEXT


def test_scene_uses_renderer_independent_model_and_exact_electrical_spine():
    assert "from engine.electrical_network_laplacian import ElectricalNetworkLaplacian" in TEXT
    assert "model = ElectricalNetworkLaplacian()" in TEXT
    assert 'RuntimeError("unexpected electrical potentials")' in TEXT
    assert 'RuntimeError("unexpected Kirchhoff solution")' in TEXT
    assert 'RuntimeError("unexpected electrical energy balance")' in TEXT
    assert 'RuntimeError("unexpected effective resistance")' in TEXT


def test_vertex_numerals_use_high_contrast_black():
    assert "vertex: MathTex(str(vertex), font_size=29, color=BLACK)" in TEXT


def test_scene_introduces_electrical_vocabulary_from_first_principles():
    assert "Turn every edge into a unit resistor" in TEXT
    assert '"POTENTIAL"' in TEXT
    assert "a number assigned to vertex i" in TEXT
    assert '"CURRENT"' in TEXT
    assert "flow along an edge" in TEXT
    assert "Only potential differences drive current." in TEXT


def test_scene_introduces_ohms_law_on_one_exact_edge():
    assert "Ohm's law turns a potential difference into edge current." in TEXT
    assert r"v_3=\frac23" in TEXT
    assert r"v_4=\frac53" in TEXT
    assert r"I_{4\to3}=\frac{v_4-v_3}{R}" in TEXT
    assert r"=\frac{5/3-2/3}{1}=1" in TEXT
    assert "higher potential to lower potential" in TEXT


def test_scene_introduces_kirchhoff_conservation_locally():
    assert "current entering must equal current leaving" in TEXT
    assert '"CURRENT CONSERVATION"' in TEXT
    assert r"1=\frac23+\frac13" in TEXT
    assert r"\sum_{j\sim i}(v_i-v_j)=b_i" in TEXT
    assert "externally injected current" in TEXT


def test_scene_assembles_structural_laplacian_system_and_compatibility():
    assert "collects all four current-conservation equations" in TEXT
    assert '[["v_1"], ["v_2"], ["v_3"], ["v_4"]]' in TEXT
    assert '[["-1"], ["0"], ["0"], ["1"]]' in TEXT
    assert r"\mathbf 1^T\mathbf b=-1+0+0+1=0" in TEXT
    assert "total current injected = total current removed" in TEXT


def test_scene_explains_gauge_freedom_and_ground_reference():
    assert "Only potential differences matter" in TEXT
    assert r"\mathbf v+c\mathbf 1=" in TEXT
    assert "Adding the same constant changes no edge difference and no current." in TEXT
    assert r"\text{choose ground:}\qquad v_1=0" in TEXT


def test_scene_solves_grounded_reduced_system_with_legible_fractions():
    assert "Ground vertex 1" in TEXT
    assert '[["2", "-1", "0"], ["-1", "3", "-1"], ["0", "-1", "1"]]' in TEXT
    assert '[["v_2"], ["v_3"], ["v_4"]]' in TEXT
    assert r"\mathbf v=\left(0,\frac13,\frac23,\frac53\right)^T" in TEXT
    assert "source at vertex 4 has the highest potential" in TEXT


def test_scene_animates_exact_source_split_and_sink_currents():
    assert "One unit enters at vertex 4" in TEXT
    assert '"SOURCE"' in TEXT
    assert r"b_4=+1" in TEXT
    assert '"INTERIOR BALANCE"' in TEXT
    assert '"SINK"' in TEXT
    assert r"b_1=-1" in TEXT
    assert "Arrow(" in TEXT


def test_scene_connects_energy_power_and_effective_resistance():
    assert "power dissipated by the resistors" in TEXT
    assert r"\sum_{\text{edges}} I^2R=" in TEXT
    assert r"\mathbf v^TL\mathbf v=\mathbf b^T\mathbf v=\frac53" in TEXT
    assert '"EFFECTIVE RESISTANCE"' in TEXT
    assert r"R_{\rm eff}=\frac{\Delta V}{I}=\frac{5/3}{1}=\frac53" in TEXT


def test_scene_synthesizes_electrical_laws_and_previews_random_walks():
    assert '"EDGE LAW"' in TEXT
    assert '"VERTEX LAW"' in TEXT
    assert '"ENERGY"' in TEXT
    assert "solution requires total injected current" in TEXT
    assert "What if each vertex sends probability equally among its neighbors?" in TEXT
