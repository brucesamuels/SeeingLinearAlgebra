from pathlib import Path

SCENE_PATH=Path("scenes/eigenvalues_chapter_review_presentation.py")


def source()->str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_review_title_and_core_eigenpair_equation() -> None:
    text=source()
    assert 'LESSON_TITLE="Chapter Review"' in text
    assert r"A\mathbf v=\lambda\mathbf v" in text


def test_null_space_and_characteristic_equation_are_recalled() -> None:
    text=source()
    assert r"\det(A-\lambda I)=0" in text
    assert r"E_\lambda=\operatorname{Null}(A-\lambda I)" in text


def test_diagonalization_and_powers_are_recalled() -> None:
    text=source()
    assert r"D=P^{-1}AP" in text
    assert r"\boxed{A=PDP^{-1}}" in text
    assert r"\boxed{A^k=PD^kP^{-1}}" in text


def test_diagonalizability_criterion_is_explicit() -> None:
    text=source()
    assert r"\sum_\lambda \dim E_\lambda=n" in text
    assert "enough independent eigenvectors" in text


def test_spectral_theorem_is_recalled() -> None:
    text=source()
    assert r"A^T=A" in text
    assert r"Q^TQ=I" in text
    assert r"\boxed{A=QDQ^T}" in text


def test_ode_and_difference_equation_applications_are_recalled() -> None:
    text=source()
    assert r"\mathbf x'=A\mathbf x" in text
    assert r"\mathbf y'=D\mathbf y" in text
    assert r"\mathbf x_{n+1}=A\mathbf x_n" in text
    assert r"\mathbf x_n=A^n\mathbf x_0" in text


def test_student_facing_scene_omits_checkpoint_number() -> None:
    assert "CP183" not in source()
