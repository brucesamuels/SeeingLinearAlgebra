from pathlib import Path

SCENE_PATH = Path("scenes/eigenspaces_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_is_fixed_2d_with_coordinate_grid() -> None:
    text = source()
    assert "class EigenspacesPresentation(Scene):" in text
    assert "NumberPlane(" in text
    assert "ThreeDScene" not in text


def test_scene_begins_with_scalar_multiple_family_before_null_space() -> None:
    text = source()
    family = text.index(r"A(c\mathbf v)=cA\mathbf v=c(2\mathbf v)=2(c\mathbf v)")
    null_space = text.index(r"(A-\lambda I)\mathbf v=\mathbf 0")
    assert family < null_space
    assert "Every nonzero scalar multiple is also an eigenvector." in text


def test_scene_explicitly_handles_zero_vector_subtlety() -> None:
    text = source()
    assert "0 is in the subspace, but 0 is not an eigenvector." in text
    assert "Eigenvectors are the nonzero vectors in an eigenspace." in text


def test_scene_derives_null_space_equation_step_by_step() -> None:
    text = source()
    first = text.index(r"A\mathbf v=\lambda\mathbf v")
    second = text.index(r"A\mathbf v-\lambda\mathbf v=\mathbf 0")
    third = text.index(r"(A-\lambda I)\mathbf v=\mathbf 0")
    assert first < second < third


def test_lambda_two_example_connects_to_previous_line() -> None:
    text = source()
    assert r"A-2I=\begin{bmatrix}3&3\\3&3\end{bmatrix}" in text
    assert r"x+y=0" in text
    assert r"E_2=\operatorname{Null}(A-2I)" in text


def test_final_card_shows_both_eigenspaces() -> None:
    text = source()
    assert r"E_8=\operatorname{Null}(A-8I)" in text
    assert r"E_2=\operatorname{Null}(A-2I)" in text
    assert "Each eigenvalue has its own eigenspace." in text


def test_scene_does_not_jump_to_characteristic_equation() -> None:
    text = source().lower()
    assert "characteristic" not in text
    assert "det(" not in text


def test_math_columns_use_bounding_box_spacing() -> None:
    text = source()
    assert "family_note.next_to(relation" in text
    assert "equation.next_to(shifted" in text
    assert "conclusion.next_to(equation" in text
    assert "slow_label.next_to(fast_label" in text


def test_student_facing_scene_contains_no_checkpoint_number() -> None:
    assert "CP170" not in source()
