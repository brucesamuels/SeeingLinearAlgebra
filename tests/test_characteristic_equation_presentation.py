from pathlib import Path

SCENE_PATH = Path("scenes/characteristic_equation_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_is_fixed_2d_and_algebra_first() -> None:
    text = source()
    assert "class CharacteristicEquationPresentation(Scene):" in text
    assert "NumberPlane(" not in text
    assert "ThreeDScene" not in text


def test_definition_appears_before_identity_matrix_step() -> None:
    text = source()
    definition = text.index(r"A\mathbf v=\lambda\mathbf v,\qquad \mathbf v\neq\mathbf 0")
    identity = text.index(r"I\mathbf v=\mathbf v")
    with_identity = text.index(r"A\mathbf v=\lambda I\mathbf v")
    assert definition < identity < with_identity


def test_identity_matrix_is_explained_not_merely_inserted() -> None:
    text = source()
    assert r"I=\begin{bmatrix}1&0\\0&1\end{bmatrix}" in text
    assert "inserting I changes nothing" in text
    assert "A and λI can be subtracted" in text


def test_matrix_subtraction_and_factoring_are_animated_in_order() -> None:
    text = source()
    subtraction = text.index(r"A\mathbf v-\lambda I\mathbf v=\mathbf 0")
    factored = text.index(r"(A-\lambda I)\mathbf v=\mathbf 0")
    assert subtraction < factored
    assert "The common factor is the vector v." in text


def test_singularity_logic_precedes_characteristic_equation() -> None:
    text = source()
    singular = text.index(r"A-\lambda I\ \text{is singular}")
    determinant = text.index(r"\boxed{\det(A-\lambda I)=0}")
    assert singular < determinant
    assert "This is the characteristic equation." in text


def test_example_builds_lambda_identity_and_subtracts_matrices() -> None:
    text = source()
    assert r"A=\begin{bmatrix}5&3\\3&5\end{bmatrix}" in text
    assert r"\lambda I=\begin{bmatrix}\lambda&0\\0&\lambda\end{bmatrix}" in text
    assert r"A-\lambda I=\begin{bmatrix}5-\lambda&3\\3&5-\lambda\end{bmatrix}" in text
    assert "Only the diagonal entries change" in text


def test_two_by_two_determinant_rule_is_shown_explicitly() -> None:
    text = source()
    assert r"\begin{vmatrix}a&b\\c&d\end{vmatrix}=ad-bc" in text
    assert r"(5-\lambda)(5-\lambda)" in text
    assert r"3\cdot3" in text
    assert r"(5-\lambda)^2-9" in text
    assert "Multiply the main diagonal" in text


def test_characteristic_polynomial_is_expanded_factored_and_solved() -> None:
    text = source()
    stages = [
        r"(5-\lambda)^2-9=0",
        r"25-10\lambda+\lambda^2-9=0",
        r"\lambda^2-10\lambda+16=0",
        r"(\lambda-2)(\lambda-8)=0",
        r"\boxed{\lambda=2\qquad\text{or}\qquad\lambda=8}",
    ]
    positions = [text.index(stage) for stage in stages]
    assert positions == sorted(positions)


def test_final_synthesis_repeats_complete_algebraic_bridge() -> None:
    text = source()
    assert "The characteristic equation is the bridge from the definition to computation." in text
    assert "Solve this equation to find the eigenvalues." in text


def test_student_facing_scene_contains_no_checkpoint_number() -> None:
    assert "CP171" not in source()
