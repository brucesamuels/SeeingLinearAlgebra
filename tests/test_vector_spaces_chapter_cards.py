from pathlib import Path

SCENE = Path("scenes/vector_spaces_chapter_cards.py")


def test_scene_defines_opening_four_sections_and_closing() -> None:
    source = SCENE.read_text(encoding="utf-8")
    for class_name in (
        "VectorSpacesChapterOpening",
        "VectorSpacesSectionOne",
        "VectorSpacesSectionTwo",
        "VectorSpacesSectionThree",
        "VectorSpacesSectionFour",
        "VectorSpacesChapterClosing",
    ):
        assert f"class {class_name}" in source


def test_opening_asks_chapter_question() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "CHAPTER_QUESTION" in source
    assert 'Text("CHAPTER 2"' in source


def test_closing_reuses_rank_nullity_and_orthogonal_decompositions() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\operatorname{rank}(A)+\operatorname{nullity}(A)=n" in source
    assert r"\mathbb R^n=\operatorname{row}(A)\oplus\operatorname{null}(A)" in source
    assert r"\mathbb R^m=\operatorname{col}(A)\oplus\operatorname{null}(A^T)" in source


def test_closing_reflection_is_wrapped_to_stay_on_screen() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "A matrix organizes directions into what survives, what disappears," in source
    assert "what can be produced, and what remains unreachable." in source
    assert 'font_size=27' in source
