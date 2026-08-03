from pathlib import Path

SOURCE_PATH = Path("scenes/row_column_rule_presentation.py")


def source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_scene_and_title_are_present() -> None:
    text = source()
    assert "class RowColumnRulePresentation(Scene)" in text
    assert 'TITLE = "The Row–Column Rule"' in text


def test_scene_connects_rows_and_columns() -> None:
    text = source()
    assert "The same product, viewed two ways" in text
    assert "Column combinations build the vector" in text
    assert r"x_1\mathbf{a}_1+x_2\mathbf{a}_2+x_3\mathbf{a}_3" in text
    assert r"\text{row}_1(A)\cdot\mathbf{x}" in text


def test_scene_animates_first_and_second_rows() -> None:
    text = source()
    assert "_show_first_row_computation" in text
    assert "_show_second_row_computation" in text
    assert "matrix.get_rows()[0]" in text
    assert "matrix.get_rows()[1]" in text
    assert r"(2)(3)+(-1)(2)+(3)(-1)=1" in text
    assert r"(1)(3)+(4)(2)+(-2)(-1)=13" in text


def test_scene_states_general_rule() -> None:
    text = source()
    assert r"(A\mathbf{x})_i" in text
    assert r"\sum_{j=1}^{n}a_{ij}x_j" in text
    assert "Pair corresponding positions, multiply, then add." in text


def test_scene_explains_dimensions() -> None:
    text = source()
    assert r"A_{m\times n}\mathbf{x}_{n\times1}" in text
    assert r"(A\mathbf{x})_{m\times1}" in text
    assert r"A_{2\times3}\mathbf{x}_{2\times1}" in text
    assert "inner dimensions match" in text


def test_scene_includes_pause_predict_and_bridge() -> None:
    text = source()
    assert "Pause and Predict" in text
    assert "What is the second entry of A x?" in text
    assert r"(-3)(5)+(4)(-1)=-19" in text
    assert "same product we already built from the columns" in text
    assert "multiply two matrices" in text


def test_key_groups_are_sized_for_frame() -> None:
    text = source()
    assert "product.scale_to_fit_width(10.2)" in text
    assert "example.scale_to_fit_width(7.6)" in text
    assert "move_to(DOWN * 1.9)" in text
