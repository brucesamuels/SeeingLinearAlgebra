from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "change_of_basis_review_presentation.py"
TEXT = SOURCE.read_text()


def test_fixed_vector_is_not_transformed_with_grid():
    assert "Transform(grid_b, grid_c, rate_func=smooth)" in TEXT
    segment = TEXT.split("Transform(grid_b, grid_c, rate_func=smooth)", 1)[1].split("run_time=4.0", 1)[0]
    assert "Transform(vector" not in segment


def test_review_contains_all_core_formulas():
    assert r"Q_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal C}^{-1}P_{\mathcal B}" in TEXT
    assert r"[\mathbf v]_{\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}[\mathbf v]_{\mathcal B}" in TEXT
    assert r"[T]_{\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}[T]_{\mathcal B}Q_{\mathcal B\leftarrow\mathcal C}" in TEXT


def test_transition_matrix_is_grounded_in_linear_combinations():
    assert r"\mathbf b_1=1\mathbf c_1+0\mathbf c_2" in TEXT
    assert r"\mathbf b_2=-\mathbf c_1+\mathbf c_2" in TEXT
    assert "how do I build this old basis vector from the new basis?" in TEXT


def test_scene_uses_structural_matrices():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_has_no_checkpoint_number_in_student_content():
    assert "CP196" not in TEXT
    assert "Checkpoint 196" not in TEXT

