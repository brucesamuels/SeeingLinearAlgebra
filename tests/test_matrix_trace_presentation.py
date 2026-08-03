from pathlib import Path

SOURCE_PATH = Path("scenes/matrix_trace_presentation.py")


def source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_scene_and_title_are_present() -> None:
    text = source()
    assert "class MatrixTracePresentation(Scene)" in text
    assert 'TITLE = "The Trace of a Matrix"' in text


def test_scene_defines_trace_and_highlights_diagonal() -> None:
    text = source()
    assert "Add the entries on the main diagonal" in text
    assert r"\operatorname{tr}(A)=3+5+6=14" in text
    assert r"\operatorname{tr}(A)=\sum_{i=1}^{n}a_{ii}" in text
    assert "diagonal_indices = (0, 4, 8)" in text


def test_scene_distinguishes_scalar_output() -> None:
    text = source()
    assert r"A+B\longrightarrow\text{matrix}" in text
    assert r"AB\longrightarrow\text{matrix}" in text
    assert r"\operatorname{tr}(A)\longrightarrow\text{number}" in text
    assert "scalar-valued function" in text


def test_scene_requires_square_matrices() -> None:
    text = source()
    assert "Trace requires a square matrix" in text
    assert r"2\times3" in text
    assert r"\operatorname{tr}(A)\text{ is not defined}" in text


def test_scene_includes_linearity() -> None:
    text = source()
    assert r"\operatorname{tr}(A+B)" in text
    assert r"\operatorname{tr}(A)+\operatorname{tr}(B)" in text
    assert r"\operatorname{tr}(cA)=c\,\operatorname{tr}(A)" in text


def test_scene_connects_product_order_to_equal_trace() -> None:
    text = source()
    assert r"AB\neq BA" in text
    assert r"\operatorname{tr}(AB)=\operatorname{tr}(BA)" in text
    assert "changes the matrix—but not the trace" in text


def test_scene_includes_predict_eigenvalue_preview_and_cp102_bridge() -> None:
    text = source()
    assert "Pause and Predict" in text
    assert r"4+3+(-2)=5" in text
    assert "trace will reveal information about eigenvalues" in text
    assert "Next: matrix transposition." in text


def test_key_objects_fit_within_frame() -> None:
    text = source()
    assert "explanation.scale_to_fit_width(11.2)" in text
    assert "products.scale_to_fit_width(10.4)" in text
    assert "move_to(DOWN * 2.22)" in text
