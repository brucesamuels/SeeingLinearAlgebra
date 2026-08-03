from pathlib import Path

SOURCE_PATH = Path(
    "scenes/matrix_multiplication_composition_presentation.py"
)


def source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_scene_and_title_are_present() -> None:
    text = source()
    assert "class MatrixMultiplicationCompositionPresentation(Scene)" in text
    assert 'TITLE = "Matrix Multiplication as Composition"' in text


def test_scene_introduces_sequential_transformations() -> None:
    text = source()
    assert "Apply A first, then apply B" in text
    assert r"B(A\mathbf{x})=(BA)\mathbf{x}" in text
    assert "output of A becomes the input to B" in text


def test_scene_animates_geometric_composition() -> None:
    text = source()
    assert "horizontal shear" in text
    assert "reflect across the y-axis" in text
    assert r"\mathbf{x}=(2,1)" in text
    assert r"A\mathbf{x}=(3,1)" in text
    assert r"B(A\mathbf{x})=(-3,1)" in text


def test_scene_shows_product_matrix() -> None:
    text = source()
    assert r"BA=" in text
    assert r"\begin{bmatrix}-1&-1\\0&1\end{bmatrix}" in text
    assert r"\begin{bmatrix}-3\\1\end{bmatrix}" in text


def test_scene_explains_rightmost_matrix_first() -> None:
    text = source()
    assert "rightmost matrix act first" in text
    assert r"(BA)\mathbf{x}=B(A\mathbf{x})" in text
    assert "A must act on x before B" in text


def test_scene_includes_pause_predict_and_noncommutativity_bridge() -> None:
    text = source()
    assert "Pause and Predict" in text
    assert "In CBx, which matrix acts first?" in text
    assert "B acts first." in text
    assert "reversing the order usually changes the result" in text


def test_key_groups_are_sized_for_frame() -> None:
    text = source()
    assert "sequence.scale_to_fit_width(10.8)" in text
    assert "expression.scale_to_fit_width(6.8)" in text
    assert "equation.scale_to_fit_width(9.4)" in text
