from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "svd_introduction_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_reuses_gram_matrix_and_derives_singular_values():
    assert '[["1", "0"], ["1", "1"], ["0", "1"]]' in TEXT
    assert '[["2", "1"], ["1", "2"]]' in TEXT
    assert r"\lambda_1=3" in TEXT
    assert r"\lambda_2=1" in TEXT
    assert r"\boxed{\sigma_i=\sqrt{\lambda_i(A^TA)}}" in TEXT
    assert r"\sigma_1=\sqrt3" in TEXT


def test_scene_has_pause_and_maps_right_to_left_singular_vectors():
    assert "Pause: what stretch factors should A assign to these directions?" in TEXT
    assert r"Av_1=\sqrt3\,u_1" in TEXT
    assert r"Av_2=1\,u_2" in TEXT
    assert r"u_1^Tu_2=0" in TEXT


def test_scene_proves_mapped_directions_are_orthogonal():
    assert r"(Av_i)^T(Av_j)=v_i^TA^TAv_j" in TEXT
    assert r"\lambda_jv_i^Tv_j=0" in TEXT


def test_scene_has_circle_to_ellipse_geometry_and_factor_pipeline():
    assert "Circle(" in TEXT
    assert "Ellipse(" in TEXT
    assert r"\xrightarrow{\ V^T\ }" in TEXT
    assert r"\xrightarrow{\ \Sigma\ }" in TEXT
    assert r"\xrightarrow{\ U\ }" in TEXT


def test_scene_states_svd_and_preserves_later_scope():
    assert "singular value decomposition" in TEXT.lower()
    assert r"\boxed{A=U\Sigma V^T}" in TEXT
    forbidden = ("pseudoinverse", "low-rank", "zero singular value", "minimum principle")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP208" not in TEXT


def test_zero_entry_in_u_is_explicitly_centered_in_its_cell():
    assert "u_entries[3].move_to" in TEXT
    assert "u_entries[1].get_center()[0]" in TEXT
    assert "u_entries[2].get_center()[1]" in TEXT
