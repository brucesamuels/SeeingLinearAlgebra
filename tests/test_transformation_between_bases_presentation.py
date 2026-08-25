from pathlib import Path


SCENE = Path("scenes/transformation_between_bases_presentation.py")


def source():
    return SCENE.read_text(encoding="utf-8")


def test_scene_identity_and_student_facing_language():
    text = source()
    assert 'CHAPTER_BANNER = "CHANGE OF BASIS"' in text
    assert 'LESSON_TITLE = "Changing a Transformation Between Two Bases"' in text
    assert "CP194" not in text


def test_geometric_vectors_stay_fixed_while_grid_changes():
    text = source()
    assert "Transform(grid_b, grid_c, rate_func=smooth)" in text
    grid_change = text.split("Transform(grid_b, grid_c, rate_func=smooth)", 1)[1].split("run_time=4.0", 1)[0]
    assert "Transform(vector," not in grid_change
    assert "Transform(image," not in grid_change
    assert "geometric vectors did not move" in text


def test_direct_route_avoids_standard_basis():
    text = source()
    assert "No standard-coordinate stage is required." in text
    assert r"Q_{\mathcal B\leftarrow\mathcal C}" in text
    assert r"Q_{\mathcal C\leftarrow\mathcal B}" in text
    assert r"[T]_{\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}" in text


def test_transition_inverse_theorem_and_row_reduction_procedure():
    text = source()
    assert "The two direct transition matrices are inverses." in text
    assert "Go from B to C and back to B" in text
    assert "Reduce the new-basis block to I" in text
    assert r"[P_{\mathcal C}\mid P_{\mathcal B}]" in text
    assert r"R_2\leftarrow R_2-R_1" in text
    assert r"R_2\leftarrow-\tfrac12R_2" in text
    assert r"R_1\leftarrow R_1-2R_2" in text
    assert "self._augmented" in text


def test_transition_matrix_is_derived_from_linear_combinations():
    text = source()
    assert r"\mathbf b_1=1\mathbf c_1+0\mathbf c_2" in text
    assert r"\mathbf b_2=-\mathbf c_1+\mathbf c_2" in text
    assert r"[\mathbf b_1]_{\mathcal C}" in text
    assert r"[\mathbf b_2]_{\mathcal C}" in text
    assert "The coefficient columns of those linear combinations form the transition matrix." in text
    assert r"\mathbf v=x\mathbf b_1+y\mathbf b_2" in text
    assert r"=(x-y)\mathbf c_1+y\mathbf c_2" in text
    assert r"P_{\mathcal C}Q_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal B}" in text
    assert "a consequence of those linear combinations" in text


def test_structural_matrices_and_numerical_verification():
    text = source()
    assert r"\begin{bmatrix}" not in text
    assert "Matrix(" in text
    assert 'self._matrix([["2", "0"], ["0", "3"]]' in text
    assert r"(2,1)_{\mathcal B}\leftrightarrow(1,1)_{\mathcal C}" in text
    assert r"(5,3)_{\mathcal B}\leftrightarrow(2,3)_{\mathcal C}" in text
