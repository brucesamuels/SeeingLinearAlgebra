from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "coordinate_linear_combinations_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_keeps_vector_fixed_during_grid_change():
    assert "Transform(standard_grid, basis_grid, rate_func=smooth)" in TEXT
    animation = TEXT.split("Transform(standard_grid, basis_grid, rate_func=smooth)", 1)[1].split("run_time=4.0", 1)[0]
    assert "Transform(vector" not in animation


def test_scene_explicitly_connects_linear_combinations_to_columns():
    assert r"\mathbf v=1\mathbf b_1+2\mathbf b_2" in TEXT
    assert r"[\mathbf b_1]_{\mathcal E}" in TEXT
    assert r"[\mathbf b_2]_{\mathcal E}" in TEXT
    assert "The columns store the two substitution recipes." in TEXT


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_previews_general_transition_matrix():
    assert r"Q_{\mathcal C\leftarrow\mathcal B}" in TEXT
    assert "Write each old basis vector as a linear combination of the new basis vectors." in TEXT


def test_scene_has_no_checkpoint_number_in_student_content():
    assert "CP195" not in TEXT
    assert "Checkpoint 195" not in TEXT

