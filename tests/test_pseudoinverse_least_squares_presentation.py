from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "pseudoinverse_least_squares_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_chapter_banner_and_structural_matrices():
    assert "SINGULAR VALUES, RANK, AND APPROXIMATION" in TEXT
    assert "Least Squares and Minimum-Norm Solutions" in TEXT
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_starts_with_target_outside_image_and_no_preimage():
    assert '[["1", "1"], ["1", "1"], ["0", "0"]]' in TEXT
    assert r"A(x_1,x_2)=(s,s,0)" in TEXT
    assert '["3", "1", "2"]' in TEXT
    assert r"\mathbf b\notin\mathcal R(A)" in TEXT
    assert "No input maps exactly to b." in TEXT


def test_scene_separates_closest_output_from_selected_preimage():
    assert "CLOSEST REACHABLE OUTPUT" in TEXT
    assert r"\widehat{\mathbf b}=AA^+\mathbf b" in TEXT
    assert "SELECTED PRE-IMAGE" in TEXT
    assert r"\widehat{\mathbf x}=A^+\mathbf b" in TEXT
    assert "project b onto the image" in TEXT
    assert "return to the row space" in TEXT


def test_scene_computes_projection_and_orthogonal_residual():
    assert '["2", "2", "0"]' in TEXT
    assert r"\widehat{\mathbf b}=(2,2,0)\in\mathcal R(A)" in TEXT
    assert r"\mathbf r=\mathbf b-\widehat{\mathbf b}=(1,-1,2)" in TEXT
    assert r"A^T\mathbf r=0" in TEXT
    assert "No reachable output is closer to b." in TEXT


def test_scene_computes_pseudoinverse_solution_and_full_family():
    assert r"\frac14" in TEXT
    assert r"A\widehat{\mathbf x}=(2,2,0)=\widehat{\mathbf b}" in TEXT
    assert r"\mathbf x_t=(1,1)+t(1,-1)=(1+t,1-t)" in TEXT
    assert "for every }t" in TEXT
    assert "Null-space motion changes the pre-image" in TEXT


def test_scene_proves_minimum_norm_choice():
    assert r"\|\mathbf x_t\|^2=(1+t)^2+(1-t)^2" in TEXT
    assert r"=2+2t^2\ge 2" in TEXT
    assert r"t=0\quad\Longrightarrow\quad\widehat{\mathbf x}=(1,1)" in TEXT
    assert "Equality occurs only at the pseudoinverse solution." in TEXT


def test_scene_uses_function_language_and_concludes_with_two_properties():
    assert "one-to-one and onto" in TEXT
    assert r"A:\mathcal R(A^T)" in TEXT
    assert r"A^+:\mathcal R(A)" in TEXT
    assert "genuine inverses" in TEXT
    assert "LEAST SQUARES" in TEXT
    assert "MINIMUM NORM" in TEXT
    assert r"\boxed{\widehat{\mathbf x}=A^+\mathbf b}" in TEXT


def test_scene_preserves_later_chapter_scope_and_has_no_checkpoint_labels():
    forbidden = ("condition number", "Eckart", "compression", "PCA")
    assert not any(term.lower() in TEXT.lower() for term in forbidden)
    assert "CP218" not in TEXT
    assert "CP217" not in TEXT
    assert "checkpoint" not in TEXT.lower()
