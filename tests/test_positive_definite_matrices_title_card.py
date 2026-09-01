from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "positive_definite_matrices_title_card.py"
TEXT = SOURCE.read_text()


def test_title_card_has_chapter_identity_and_thesis():
    assert "POSITIVE DEFINITE MATRICES" in TEXT
    assert "Energy, structure, and unique minima." in TEXT
    assert "How can one property appear in so many forms?" in TEXT


def test_title_card_uses_structural_matrix_and_core_equivalences():
    assert "RIGHT" in TEXT
    assert "Matrix([[" in TEXT
    assert r"x^TAx>0" in TEXT
    assert r"\lambda_i>0" in TEXT
    assert r"A=R^TR" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_title_card_has_no_checkpoint_or_chapter_number():
    assert "CP213" not in TEXT
    assert "Checkpoint 213" not in TEXT
    assert "CHAPTER 8" not in TEXT
