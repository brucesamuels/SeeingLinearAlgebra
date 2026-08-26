from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "change_of_basis_title_card.py"
TEXT = SOURCE.read_text()


def test_title_card_has_chapter_identity_and_thesis():
    assert "CHANGE OF BASIS" in TEXT
    assert "One object. Many coordinate languages." in TEXT
    assert "What changes—and what stays the same?" in TEXT


def test_title_card_keeps_fixed_vector_during_basis_change():
    change = TEXT.split("FadeOut(standard_grid)", 1)[1].split("run_time=1.6", 1)[0]
    assert "FadeOut(fixed_vector)" not in change
    assert "Transform(fixed_vector" not in change


def test_title_card_has_no_chapter_number_or_checkpoint_number():
    assert "CP197" not in TEXT
    assert "Checkpoint 197" not in TEXT
    assert "CHAPTER 8" not in TEXT

