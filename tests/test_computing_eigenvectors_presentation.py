from pathlib import Path

SCENE_PATH = Path("scenes/computing_eigenvectors_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_title_and_method_are_explicit() -> None:
    text = source()
    assert 'LESSON_TITLE = "Computing Eigenvectors"' in text
    assert r"E_\lambda=\operatorname{Null}(A-\lambda I)" in text
    assert r"(A-\lambda I)\mathbf v=\mathbf 0" in text
    assert r"\lambda=1,\ 2,\ 5" in text


def test_lambda_one_case_is_fully_worked_line_by_line() -> None:
    text = source()
    assert r"E_1=\operatorname{Null}(A-I)" in text
    assert r"A-I=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}-\begin{bmatrix}1&0&0\\0&1&0\\0&0&1\end{bmatrix}" in text
    assert r"=\begin{bmatrix}3&1&0\\2&2&0\\0&0&0\end{bmatrix}" in text
    assert r"3x+y=0" in text
    assert r"2x+2y=0" in text
    assert r"x=0,\ y=0,\ z\text{ free}" in text
    assert r"E_1=\operatorname{span}" in text


def test_lambda_two_case_is_fully_worked_line_by_line() -> None:
    text = source()
    assert r"E_2=\operatorname{Null}(A-2I)" in text
    assert r"A-2I=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}-\begin{bmatrix}2&0&0\\0&2&0\\0&0&2\end{bmatrix}" in text
    assert r"=\begin{bmatrix}2&1&0\\2&1&0\\0&0&-1\end{bmatrix}" in text
    assert r"2x+y=0" in text
    assert r"z=0" in text
    assert r"x=t,\ y=-2t,\ z=0" in text
    assert r"\begin{bmatrix}1\\-2\\0\end{bmatrix}" in text


def test_lambda_five_case_is_fully_worked_line_by_line() -> None:
    text = source()
    assert r"E_5=\operatorname{Null}(A-5I)" in text
    assert r"A-5I=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}-\begin{bmatrix}5&0&0\\0&5&0\\0&0&5\end{bmatrix}" in text
    assert r"=\begin{bmatrix}-1&1&0\\2&-2&0\\0&0&-4\end{bmatrix}" in text
    assert r"-x+y=0" in text
    assert r"z=0" in text
    assert r"x=t,\ y=t,\ z=0" in text
    assert r"\begin{bmatrix}1\\1\\0\end{bmatrix}" in text


def test_definition_check_is_shown_for_lambda_two() -> None:
    text = source()
    assert r"A\begin{bmatrix}1\\-2\\0\end{bmatrix}" in text
    assert r"=2\begin{bmatrix}1\\-2\\0\end{bmatrix}" in text
    assert "null-space computation produced" in text


def test_final_summary_collects_all_three_eigenspaces() -> None:
    text = source()
    assert r"E_1=\operatorname{Null}(A-I)=\operatorname{span}" in text
    assert r"E_2=\operatorname{Null}(A-2I)=\operatorname{span}" in text
    assert r"E_5=\operatorname{Null}(A-5I)=\operatorname{span}" in text
    assert "For each eigenvalue, we find the null space of A−λI." in text


def test_scene_remains_fixed_2d_and_student_facing() -> None:
    text = source()
    assert "class ComputingEigenvectorsPresentation(Scene):" in text
    assert "ThreeDScene" not in text
    assert "CP173" not in text


def test_headings_emphasize_null_space_tasks() -> None:
    text = source()
    assert "For λ=1, find Null(A−I) by solving line by line." in text
    assert "For λ=2, find Null(A−2I) by solving line by line." in text
    assert "For λ=5, find Null(A−5I) by solving line by line." in text


def test_final_card_establishes_an_eigenvector_basis_for_r3() -> None:
    text = source()
    assert "The three eigenvectors are linearly independent." in text
    assert r"\mathbf v_1=\begin{bmatrix}0\\0\\1\end{bmatrix}" in text
    assert r"\mathbf v_2=\begin{bmatrix}1\\-2\\0\end{bmatrix}" in text
    assert r"\mathbf v_3=\begin{bmatrix}1\\1\\0\end{bmatrix}" in text
    assert r"\mathcal B=\left\{\mathbf v_1,\mathbf v_2,\mathbf v_3\right\}\text{ is a basis for }\mathbb R^3" in text
    assert "Enough independent eigenvectors give us an eigenvector basis." in text
