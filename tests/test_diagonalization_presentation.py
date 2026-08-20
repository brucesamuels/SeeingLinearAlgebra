from pathlib import Path

SCENE_PATH = Path("scenes/diagonalization_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_starts_with_given_a_and_p() -> None:
    text = source()
    assert 'LESSON_TITLE = "Diagonalization"' in text
    assert r"A=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}" in text
    assert r"P=[\mathbf v_1\ \mathbf v_2\ \mathbf v_3]" in text


def test_scene_solves_for_d_algebraically() -> None:
    text = source()
    assert r"AP=PD" in text
    assert r"P^{-1}AP=P^{-1}PD" in text
    assert r"\boxed{D=P^{-1}AP}" in text
    assert "we do not assume its entries in advance" in text


def test_p_inverse_is_computed_explicitly() -> None:
    text = source()
    assert r"P^{-1}=\begin{bmatrix}0&0&1\\\frac13&-\frac13&0\\\frac23&\frac13&0\end{bmatrix}" in text


def test_d_multiplication_is_worked_before_diagonal_result() -> None:
    text = source()
    assert r"P^{-1}A=" in text
    assert r"=\begin{bmatrix}0&0&1\\\frac23&-\frac23&0\\\frac{10}{3}&\frac53&0\end{bmatrix}" in text
    assert r"D=(P^{-1}A)P=" in text
    assert r"\boxed{D=\begin{bmatrix}1&0&0\\0&2&0\\0&0&5\end{bmatrix}}" in text


def test_eigenvalues_are_identified_only_after_d_is_derived() -> None:
    text = source()
    derivation = text.index(r"\boxed{D=\begin{bmatrix}1&0&0\\0&2&0\\0&0&5\end{bmatrix}}")
    interpretation = text.index("The diagonal entries 1, 2, and 5 are the corresponding eigenvalues.")
    assert derivation < interpretation


def test_factorization_is_recovered_from_derived_d() -> None:
    text = source()
    assert r"D=P^{-1}AP" in text
    assert r"PD=AP" in text
    assert r"PDP^{-1}=A" in text
    assert r"\boxed{A=PDP^{-1}}" in text


def test_right_to_left_interpretation_is_explicit() -> None:
    text = source()
    assert r'_replace_math_heading(heading, r"\text{Read }A=PDP^{-1}\text{ from right to left.}")' in text
    assert r"[\mathbf x]_{\mathcal B}" in text
    assert r"[A\mathbf x]_{\mathcal B}" in text
    assert 'standard → eigenbasis' in text
    assert 'apply the diagonal action' in text
    assert 'eigenbasis → standard' in text


def test_student_scene_omits_checkpoint_number() -> None:
    assert "CP175" not in source()


def test_math_notation_in_headings_uses_mathtex() -> None:
    text = source()
    assert r'_replace_math_heading(heading, r"\text{First compute }P^{-1}\text{.}")' in text
    assert r'_replace_math_heading(heading, r"\text{Now evaluate }D=P^{-1}AP\text{ step by step.}")' in text
    assert r'_replace_math_heading(heading, r"\text{Now rewrite }D=P^{-1}AP\text{ as a factorization of }A\text{.}")' in text
    assert r'_replace_math_heading(heading, r"\text{Read }A=PDP^{-1}\text{ from right to left.}")' in text
    assert '_replace_heading(heading, "First compute P^{-1}.")' not in text
