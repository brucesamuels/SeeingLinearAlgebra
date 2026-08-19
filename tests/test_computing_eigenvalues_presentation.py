from pathlib import Path

SCENE_PATH = Path("scenes/computing_eigenvalues_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_is_fixed_2d_and_explicitly_3x3() -> None:
    text = source()
    assert "class ComputingEigenvaluesPresentation(Scene):" in text
    assert 'LESSON_TITLE = "Computing Eigenvalues in a 3×3 Example"' in text
    assert r"A=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}" in text
    assert "ThreeDScene" not in text
    assert "NumberPlane(" not in text


def test_lambda_identity_subtraction_is_built_for_all_three_diagonal_entries() -> None:
    text = source()
    assert r"\lambda I=\begin{bmatrix}\lambda&0&0\\0&\lambda&0\\0&0&\lambda\end{bmatrix}" in text
    assert r"\begin{bmatrix}4-\lambda&1&0\\2&3-\lambda&0\\0&0&1-\lambda\end{bmatrix}" in text
    assert "Only the diagonal entries change." in text


def test_full_3x3_determinant_is_displayed_before_reduction() -> None:
    text = source()
    assert r"4-\lambda&1&0" in text
    assert r"2&3-\lambda&0" in text
    assert r"0&0&1-\lambda" in text
    assert "The third column has two zeros" in text


def test_cofactor_expansion_reduces_to_2x2() -> None:
    text = source()
    assert r"(1-\lambda)" in text
    assert r"\begin{vmatrix}4-\lambda&1\\2&3-\lambda\end{vmatrix}=0" in text
    assert "Only the (3,3) entry contributes" in text


def test_remaining_2x2_determinant_uses_ad_minus_bc() -> None:
    text = source()
    assert r"\begin{vmatrix}a&b\\c&d\end{vmatrix}=ad-bc" in text
    assert r"(4-\lambda)(3-\lambda)" in text
    assert r"1\cdot2" in text
    assert r"(1-\lambda)\big((4-\lambda)(3-\lambda)-2\big)=0" in text


def test_polynomial_simplification_and_factoring_are_animated_in_order() -> None:
    text = source()
    stages = [
        r"(1-\lambda)\big((4-\lambda)(3-\lambda)-2\big)=0",
        r"(1-\lambda)(12-7\lambda+\lambda^2-2)=0",
        r"(1-\lambda)(\lambda^2-7\lambda+10)=0",
        r"(1-\lambda)(\lambda-5)(\lambda-2)=0",
        r"\boxed{\lambda=1,\qquad \lambda=2,\qquad \lambda=5}",
    ]
    positions = [text.index(stage) for stage in stages]
    assert positions == sorted(positions)


def test_final_card_states_3x3_workflow() -> None:
    text = source()
    for phrase in [
        "1. Form  A − λI",
        "2. Compute  det(A − λI)",
        "3. Use zeros or cofactors strategically",
        "4. Factor and solve for λ",
    ]:
        assert phrase in text


def test_student_facing_scene_contains_no_checkpoint_number() -> None:
    assert "CP172" not in source()
