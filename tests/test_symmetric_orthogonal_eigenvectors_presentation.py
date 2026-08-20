from pathlib import Path

SCENE_PATH = Path("scenes/symmetric_orthogonal_eigenvectors_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_title_and_symmetric_example_are_present() -> None:
    text = source()
    assert 'LESSON_TITLE = "Symmetric Matrices and Orthogonal Eigenvectors"' in text
    assert r"A=\begin{bmatrix}2&1\\1&2\end{bmatrix}" in text
    assert r"A^T=A" in text


def test_example_shows_orthogonal_eigenvectors() -> None:
    text = source()
    assert r"\mathbf v^T\mathbf w=1(1)+1(-1)=0" in text
    assert r"\mathbf v\perp\mathbf w" in text


def test_proof_uses_symmetry_and_distinct_eigenvalues() -> None:
    text = source()
    assert r"\mathbf v^T A\mathbf w" in text
    assert r"(A\mathbf v)^T\mathbf w" in text
    assert r"(\lambda-\mu)\,\mathbf v^T\mathbf w=0" in text
    assert r"\lambda\ne\mu\quad\Longrightarrow\quad\mathbf v^T\mathbf w=0" in text


def test_orthogonal_diagonalization_is_previewed() -> None:
    text = source()
    assert r"Q^TQ=I" in text
    assert r"Q^{-1}=Q^T" in text
    assert r"D=Q^TAQ=\begin{bmatrix}3&0\\0&1\end{bmatrix}" in text
    assert r"\boxed{A=QDQ^T}" in text


def test_student_facing_scene_omits_checkpoint_number() -> None:
    assert "CP178" not in source()
