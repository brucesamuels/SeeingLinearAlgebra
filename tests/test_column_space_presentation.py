from pathlib import Path

SCENE = Path("scenes/column_space_presentation.py")


def test_scene_uses_column_space_model() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "from engine.column_space import ColumnSpace" in source
    assert "class ColumnSpacePresentation(ThreeDScene)" in source


def test_scene_builds_matrix_from_three_columns() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\mathbf a_1&\mathbf a_2&\mathbf a_3" in source
    assert r"\mathbf a_3=\mathbf a_1+\mathbf a_2" in source
    assert "column_arrows = VGroup(" in source


def test_scene_shows_matrix_vector_product_as_linear_combination() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"A\mathbf x=x_1\mathbf a_1+x_2\mathbf a_2+x_3\mathbf a_3" in source
    assert "UpdateFromAlphaFunc(output_group, sweep_output)" in source
    assert "run_time=7.5" in source


def test_scene_reveals_column_plane_with_sampled_outputs() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "coefficient_samples = np.array" in source
    assert "outputs = model.sample_outputs(coefficient_samples)" in source
    assert "plane = Polygon(" in source
    assert "FadeIn(plane), FadeIn(field)" in source


def test_scene_connects_column_space_to_span_and_subspace_test() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\operatorname{col}(A)=" in source
    assert r"\operatorname{span}\{\mathbf a_1,\mathbf a_2,\mathbf a_3\}" in source
    assert r"\mathbf 0=A\mathbf 0\in\operatorname{col}(A)" in source
    assert r"A\mathbf x+A\mathbf y=A(\mathbf x+\mathbf y)" in source
    assert r"c(A\mathbf x)=A(c\mathbf x)" in source
