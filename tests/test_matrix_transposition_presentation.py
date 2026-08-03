from pathlib import Path

SOURCE_PATH = Path("scenes/matrix_transposition_presentation.py")


def source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_scene_and_title_are_present() -> None:
    text = source()
    assert "class MatrixTranspositionPresentation(Scene)" in text
    assert 'TITLE = "Matrix Transposition"' in text


def test_scene_shows_rows_becoming_columns() -> None:
    text = source()
    assert "Turn each row into a column" in text
    assert "original.get_rows()[0]" in text
    assert "transposed.get_columns()[0]" in text
    assert r"A\longrightarrow A^T" in text


def test_scene_states_entry_rule() -> None:
    text = source()
    assert r"(A^T)_{ij}=a_{ji}" in text
    assert r"a_{23}=4" in text
    assert r"(A^T)_{32}=4" in text


def test_scene_explains_dimension_reversal_and_double_transpose() -> None:
    text = source()
    assert r"A_{m\times n}\longrightarrow A^T_{n\times m}" in text
    assert r"2\times3\longrightarrow3\times2" in text
    assert r"(A^T)^T=A" in text


def test_scene_includes_basic_properties() -> None:
    text = source()
    assert r"(A+B)^T=A^T+B^T" in text
    assert r"(cA)^T=cA^T" in text


def test_scene_reverses_product_order_and_proves_the_rule() -> None:
    text = source()
    assert r"(AB)^T=B^TA^T" in text
    assert "reverses the order" in text
    assert "Proof by comparing the (i, j) entries" in text
    assert r"\bigl((AB)^T\bigr)_{ij}" in text
    assert r"(AB)_{ji}" in text
    assert r"\sum_k a_{jk}b_{ki}" in text
    assert r"\sum_k (B^T)_{ik}(A^T)_{kj}" in text
    assert r"(B^TA^T)_{ij}" in text
    assert "Every corresponding entry is equal" in text


def test_scene_introduces_symmetric_matrices() -> None:
    text = source()
    assert "unchanged by transposition" in text
    assert r"A^T=A" in text
    assert "called symmetric" in text


def test_scene_includes_pause_predict_and_bridge() -> None:
    text = source()
    assert "Pause and Predict" in text
    assert r"A\text{ is }4\times7" in text
    assert r"A^T\text{ is }7\times4" in text
    assert "Next: order, identity, and undoing." in text


def test_key_groups_fit_within_frame() -> None:
    text = source()
    assert "display.scale_to_fit_width(10.8)" in text
    assert "comparison.scale_to_fit_width(10.6)" in text
