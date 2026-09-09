from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "graphs_networks_laplacian_title_card.py"
TEXT = SOURCE.read_text()


def test_title_card_has_chapter_identity_and_thesis():
    assert "GRAPHS, NETWORKS, AND THE LAPLACIAN" in TEXT
    assert "Connections become matrices; matrices reveal structure, flow, and movement." in TEXT
    assert "Which representation fits the graph question?" in TEXT


def test_title_card_uses_recurring_graph_and_four_lenses():
    assert "edges = ((1, 2), (2, 3), (1, 3), (3, 4))" in TEXT
    assert '"CONNECTIONS"' in TEXT
    assert '"DIFFERENCES"' in TEXT
    assert '"VARIATION"' in TEXT
    assert '"MOVEMENT"' in TEXT
    assert r"L=B^TB" in TEXT
    assert r"P\ \text{or}\ G" in TEXT


def test_title_card_uses_high_contrast_vertex_numerals():
    assert "color=BLACK" in TEXT
    assert "font_size=29" in TEXT


def test_title_card_is_unnumbered_and_has_no_checkpoint_label():
    assert "CHAPTER 9" not in TEXT
    assert "CHAPTER 10" not in TEXT
    assert "CP241" not in TEXT
    assert "checkpoint" not in TEXT.lower()
