from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "singular_values_rank_approximation_title_card.py"
TEXT = SOURCE.read_text()


def test_title_card_has_chapter_identity_and_thesis():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "What matrices preserve, lose, amplify, and approximate." in TEXT
    assert "What does each singular value tell us?" in TEXT


def test_title_card_presents_svd_and_three_roles():
    assert r"A=U\Sigma V^T" in TEXT
    assert '"INPUT"' in TEXT
    assert '"STRETCH"' in TEXT
    assert '"OUTPUT"' in TEXT
    assert "preferred directions" in TEXT
    assert "singular values" in TEXT
    assert "images of directions" in TEXT


def test_title_card_is_unnumbered_and_has_no_checkpoint_label():
    assert "CHAPTER 8" not in TEXT
    assert "CHAPTER 9" not in TEXT
    assert "CP224" not in TEXT
    assert "checkpoint" not in TEXT.lower()
