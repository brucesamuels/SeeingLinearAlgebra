from pathlib import Path

SCENE_PATH = Path("scenes/fibonacci_difference_equation_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_title_and_recurrence_are_explicit() -> None:
    text = source()
    assert 'LESSON_TITLE="Fibonacci and Difference Equations"' in text
    assert r"F_{n+1}=F_n+F_{n-1}" in text


def test_matrix_state_recurrence_is_derived() -> None:
    text = source()
    assert r"\mathbf x_n=\begin{bmatrix}F_{n+1}\\F_n\end{bmatrix}" in text
    assert r"\boxed{\mathbf x_{n+1}=A\mathbf x_n}" in text
    assert r"A=\begin{bmatrix}1&1\\1&0\end{bmatrix}" in text


def test_matrix_power_and_diagonalization_are_connected() -> None:
    text = source()
    assert r"\boxed{\mathbf x_n=A^n\mathbf x_0}" in text
    assert r"\boxed{A=PDP^{-1}}" in text
    assert r"A^n=PD^nP^{-1}" in text


def test_binet_formula_is_derived_and_checked() -> None:
    text = source()
    assert r"\boxed{F_n=\frac{\phi^n-\psi^n}{\sqrt5}}" in text
    assert r"F_8=\frac{\phi^8-\psi^8}{\sqrt5}=21" in text


def test_dominant_eigenvalue_connection_is_explicit() -> None:
    text = source()
    assert r"|\phi|>1" in text
    assert r"|\psi|<1" in text
    assert r"\frac{F_{n+1}}{F_n}\longrightarrow\phi" in text


def test_no_raw_latex_in_text_objects() -> None:
    text = source()
    assert 'Text("P^{-1}' not in text
    assert 'Text("A^n' not in text


def test_adjacent_tex_fragments_do_not_merge_commands() -> None:
    text = source()
    assert r"\qquadA" not in text
    assert r"\quadA" not in text


def test_student_facing_scene_omits_checkpoint_number() -> None:
    assert "CP182" not in source()


def test_card_four_uses_math_rendered_heading_for_A_power_n() -> None:
    text = source()
    assert 'heading=self._replace_mixed_heading(heading,"Diagonalizing A makes",r"A^n","easy to compute.")' in text


def test_card_five_stack_is_lowered_to_avoid_subheading_collision() -> None:
    text = source()
    assert 'card5=self._stack(vphi,vpsi,Ptex,Dtex,diag,buff=0.28,shift=0.42,scale=0.92)' in text


def test_card_seven_uses_math_rendered_heading_for_F_n() -> None:
    text = source()
    assert 'heading=self._replace_mixed_heading(heading,"Extracting the second component gives a closed formula for",r"F_n",".")' in text
