from pathlib import Path

SCENE_PATH = Path("scenes/powers_of_diagonalizable_matrix_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_title_and_diagonalization_recall_are_explicit() -> None:
    text = source()
    assert 'LESSON_TITLE = "Powers of a Diagonalizable Matrix"' in text
    assert r"A=PDP^{-1}" in text


def test_cancellation_derivation_is_shown() -> None:
    text = source()
    assert r"A^2=(PDP^{-1})(PDP^{-1})" in text
    assert r"P^{-1}P" in text
    assert r"\boxed{A^2=PD^2P^{-1}}" in text


def test_general_power_formula_is_shown() -> None:
    assert r"\boxed{A^k=PD^kP^{-1}}" in source()


def test_fourth_power_of_D_is_computed_explicitly() -> None:
    text = source()
    assert r"1^4" in text
    assert r"2^4" in text
    assert r"5^4" in text
    assert r"\begin{bmatrix}1&0&0\\0&16&0\\0&0&625\end{bmatrix}" in text


def test_reconstructed_A_fourth_power_is_displayed() -> None:
    assert r"\begin{bmatrix}422&203&0\\406&219&0\\0&0&1\end{bmatrix}" in source()


def test_student_facing_scene_omits_checkpoint_number() -> None:
    assert "CP176" not in source()
