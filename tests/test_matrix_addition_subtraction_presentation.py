from pathlib import Path

SOURCE_PATH = Path("scenes/matrix_addition_subtraction_presentation.py")


def source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_scene_and_title_are_present() -> None:
    text = source()
    assert "class MatrixAdditionSubtractionPresentation(Scene)" in text
    assert 'TITLE = "Matrix Addition and Subtraction"' in text


def test_scene_teaches_equal_dimension_requirement() -> None:
    text = source()
    assert "same number of rows and columns" in text
    assert r"A_{m\times n}+B_{m\times n}" in text
    assert r"A_{2\times 3}+B_{3\times 2}" in text
    assert r"\text{not defined}" in text


def test_scene_animates_entrywise_addition() -> None:
    text = source()
    assert "_show_addition_example" in text
    assert "entrywise_steps(" in text
    assert r"(A+B)_{ij}=a_{ij}+b_{ij}" in text
    assert "left.get_entries()" in text
    assert "right.get_entries()" in text
    assert "result.get_entries()" in text


def test_scene_connects_subtraction_to_addition_of_negative() -> None:
    text = source()
    assert r"A-B" in text
    assert r"A+(-B)" in text
    assert "negate_matrix(" in text
    assert "Negate every entry of B" in text


def test_scene_includes_pause_predict_and_reflection() -> None:
    text = source()
    assert "Pause and Predict" in text
    assert "What is the first entry of A − B?" in text
    assert "Matrix addition and subtraction are entrywise operations." in text
    assert "Next: multiplying every entry by a scalar." in text


def test_text_is_scaled_and_positioned_below_title() -> None:
    text = source()
    assert "scale_to_fit_width(12.4)" in text
    assert "move_to(UP * 2.15)" in text
    assert "takeaway.next_to(rewritten_equation, DOWN, buff=0.42)" in text
