from pathlib import Path

SOURCE_PATH = Path("scenes/matrix_matrix_multiplication_presentation.py")


def source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_scene_and_title_are_present() -> None:
    text = source()
    assert "class MatrixMatrixMultiplicationPresentation(Scene)" in text
    assert 'TITLE = "Matrix–Matrix Multiplication"' in text


def test_scene_explains_dimension_rule() -> None:
    text = source()
    assert r"A_{m\times n}B_{n\times p}=C_{m\times p}" in text
    assert "inner dimensions must match" in text
    assert "outer dimensions determine the product" in text
    assert r"(2\times3)(3\times2)\longrightarrow2\times2" in text


def test_scene_animates_all_four_entries() -> None:
    text = source()
    assert "left.get_rows()[0]" in text
    assert "right.get_columns()[0]" in text
    assert r"(1)(2)+(2)(-1)+(-1)(5)=-5" in text
    assert r"(1)(1)+(2)(3)+(-1)(2)=5" in text
    assert r"(3)(2)+(0)(-1)+(4)(5)=26" in text
    assert r"(3)(1)+(0)(3)+(4)(2)=11" in text


def test_scene_states_general_entry_rule() -> None:
    text = source()
    assert r"c_{ij}=\sum_{k=1}^{n}a_{ik}b_{kj}" in text
    assert "row i of A and column j of B" in text
    assert "not entrywise multiplication" in text


def test_scene_covers_incompatible_dimensions() -> None:
    text = source()
    assert r"A_{2\times3}B_{2\times2}" in text
    assert r"AB\text{ is not defined}" in text
    assert "equal matrix sizes are not required" in text


def test_scene_includes_pause_predict_and_composition_bridge() -> None:
    text = source()
    assert "Pause and Predict" in text
    assert "What is the upper-right entry of AB?" in text
    assert r"(1)(4)+(2)(-2)=0" in text
    assert "composition of transformations" in text


def test_key_groups_fit_within_frame() -> None:
    text = source()
    assert "product.scale_to_fit_width(11.6)" in text
    assert "example.scale_to_fit_width(8.0)" in text
    assert "move_to(DOWN * 1.95)" in text
