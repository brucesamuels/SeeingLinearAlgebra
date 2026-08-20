from pathlib import Path

SCENE = Path("scenes/repeated_eigenvalues_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_title_and_two_contrast_matrices_are_present() -> None:
    text = source()
    assert 'LESSON_TITLE = "Repeated Eigenvalues and Diagonalizability"' in text
    assert r"A_1=\begin{bmatrix}2&0\\0&2\end{bmatrix}" in text
    assert r"A_2=\begin{bmatrix}2&1\\0&2\end{bmatrix}" in text


def test_same_repeated_characteristic_polynomial_is_shown() -> None:
    text = source()
    assert r"\det(A_i-\lambda I)=(2-\lambda)^2" in text
    assert r"\lambda=2\quad\text{with multiplicity }2" in text


def test_good_and_bad_eigenspaces_are_worked() -> None:
    text = source()
    assert r"E_2=\operatorname{Null}(0)=\mathbb R^2" in text
    assert r"E_2=\operatorname{span}\left\{\begin{bmatrix}1\\0\end{bmatrix}\right\}" in text


def test_algebraic_and_geometric_multiplicity_are_defined() -> None:
    text = source()
    assert "Algebraic multiplicity" in text
    assert "Geometric multiplicity" in text
    assert r"1\leq \text{geometric multiplicity}\leq \text{algebraic multiplicity}" in text


def test_diagonalizability_criterion_is_explicit() -> None:
    text = source()
    assert r"\sum_{\lambda}\dim E_\lambda=n" in text
    assert r"\text{geometric multiplicity}=\text{algebraic multiplicity}" in text
    assert "no invertible eigenvector matrix" in text


def test_student_facing_scene_has_no_checkpoint_number() -> None:
    assert "CP177" not in source()
