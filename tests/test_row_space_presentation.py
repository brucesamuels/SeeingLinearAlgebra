from pathlib import Path

SCENE = Path("scenes/row_space_presentation.py")


def test_scene_uses_row_space_model() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "from engine.row_space import RowSpace" in source
    assert "class RowSpacePresentation(ThreeDScene)" in source


def test_scene_displays_matrix_and_echelon_form() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"A=\begin{bmatrix}1&2&1\\0&1&1\\1&3&2\end{bmatrix}" in source
    assert r"R=\begin{bmatrix}1&2&1\\0&1&1\\0&0&0\end{bmatrix}" in source


def test_echelon_matrix_is_fixed_in_frame() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "self.add_fixed_in_frame_mobjects(echelon_tex)" in source
    assert "FadeIn(echelon_tex)" in source


def test_scene_asks_whether_row_operations_change_row_space() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "Do row operations change the row space?" in source
    assert r"R_3\leftarrow R_3-R_1" in source
    assert r"R_3\leftarrow R_3-R_2" in source


def test_scene_shows_same_row_space_after_reduction() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\operatorname{row}(A)=\operatorname{row}(R)" in source
    assert "Row reduction changes the rows, but not the row space." in source


def test_scene_concludes_with_pivot_rows_basis_and_rank() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\text{pivot rows of }R\text{ form a basis}" in source
    assert r"\dim(\operatorname{row}(A))=\operatorname{rank}(A)=2" in source
    assert "The pivot rows of echelon form give a basis for the row space." in source


def test_scene_uses_plane_patch_and_sample_points() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "plane = Polygon(" in source
    assert "Dot3D(axes.c2p(*point), radius=0.032" in source
    assert "model.sample_initial_row_space(coefficients)" in source


def test_key_idea_has_its_own_lower_band_to_avoid_collision() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert ').move_to(DOWN * 2.15)' in source
    assert 'key_idea = Text(KEY_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.28)' in source
