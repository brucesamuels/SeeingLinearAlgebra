from pathlib import Path

SCENE_PATH = Path("scenes/spectral_theorem_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_title_and_core_factorization_are_present() -> None:
    text = source()
    assert 'LESSON_TITLE = "The Spectral Theorem"' in text
    assert r"Q^TQ=I" in text
    assert r"Q^{-1}=Q^T" in text
    assert r"\boxed{A=QDQ^T}" in text


def test_d_is_derived_from_qtaq() -> None:
    text = source()
    assert r"D=Q^{-1}AQ=Q^TAQ" in text
    assert r"=\begin{bmatrix}3&0\\0&1\end{bmatrix}" in text


def test_explicit_reconstruction_is_shown() -> None:
    text = source()
    assert r"A=" in text
    assert r"\begin{bmatrix}2&1\\1&2\end{bmatrix}" in text


def test_geometric_three_step_interpretation_is_present() -> None:
    text = source()
    assert r"Q^T:\ \text{move into eigenvector coordinates}" in text
    assert r"D:\ \text{scale by }3\text{ and }1" in text
    assert r"Q:\ \text{move back to standard coordinates}" in text


def test_student_scene_has_no_checkpoint_number() -> None:
    assert "CP179" not in source()


def test_displayed_intermediate_products_are_algebraically_correct() -> None:
    text = source()
    assert r"=\frac12\begin{bmatrix}3&3\\1&-1\end{bmatrix}" in text
    assert r"IAI=QDQ^T" in text
    assert "IQAI" not in text


def test_final_card_renders_inverse_and_transpose_as_math() -> None:
    text = source()
    assert r"\text{No arbitrary inverse is needed: }Q^{-1}\text{ becomes }Q^T." in text
    assert 'Text("No arbitrary inverse is needed: Q^{-1} becomes Q^T."' not in text
