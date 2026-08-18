from pathlib import Path

SCENE_PATH = Path("scenes/eigenvectors_eigenvalues_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_is_fixed_2d_with_clear_coordinate_grid() -> None:
    text = source()
    assert "class EigenvectorsEigenvaluesPresentation(Scene):" in text
    assert "NumberPlane(" in text
    assert "ThreeDScene" not in text


def test_scene_reuses_cp168_matrix_and_special_direction_first() -> None:
    text = source()
    assert r'A=\begin{bmatrix}5&3\\3&5\end{bmatrix}' in text
    assert r'\mathbf v=\begin{bmatrix}1\\-1\end{bmatrix}' in text
    assert r'A\mathbf v=\begin{bmatrix}2\\-2\end{bmatrix}=2\mathbf v' in text


def test_defining_equation_is_revealed_after_numeric_example() -> None:
    text = source()
    numeric = text.index(r'A\mathbf v=\begin{bmatrix}2\\-2\end{bmatrix}=2\mathbf v')
    definition = text.index(r'A\mathbf v=\lambda\mathbf v,\qquad \mathbf v\ne\mathbf 0')
    assert numeric < definition


def test_scene_explicitly_separates_direction_and_scaling() -> None:
    text = source()
    assert "An eigenvector stays on its line; the eigenvalue tells how it scales." in text
    assert "λ is the scale factor along the eigenvector line." in text
    assert "v: the special direction" in text
    assert "λ: the scale factor" in text


def test_scene_includes_second_eigenvalue_from_same_transformation() -> None:
    text = source()
    assert r'A\mathbf w=8\mathbf w' in text
    assert "EIGENVECTOR_FAST" in text


def test_scene_classifies_five_lambda_behaviors() -> None:
    text = source()
    for phrase in ("stretch", "shrink", "reverse", "fixed", "collapse to the origin"):
        assert phrase in text


def test_scene_does_not_jump_ahead_to_characteristic_polynomial() -> None:
    text = source().lower()
    assert "characteristic" not in text
    assert "det(" not in text
    assert "eigenspace" not in text


def test_student_facing_scene_contains_no_checkpoint_number() -> None:
    assert "CP169" not in source()


def test_worked_example_matrix_blocks_use_bounding_box_spacing() -> None:
    text = source()
    assert "vector_tex.next_to(matrix_tex" in text
    assert "buff=0.48" in text
    assert "image_tex.next_to(vector_tex" in text
    assert "buff=0.62" in text
    assert "image_tex.move_to(np.array([3.8, -1.05, 0.0]))" not in text
