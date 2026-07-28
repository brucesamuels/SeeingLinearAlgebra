from pathlib import Path

SCENE = Path("scenes/pivot_columns_presentation.py")


def test_scene_uses_pivot_columns_model() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "from engine.pivot_columns import PivotColumns" in source
    assert "class PivotColumnsPresentation(ThreeDScene)" in source


def test_scene_displays_both_a_and_r_as_fixed_matrices() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'label_a = MathTex(r"A=", font_size=34, color=TEXT)' in source
    assert 'label_r = MathTex(r"R=", font_size=34, color=TEXT)' in source
    assert 'self.add_fixed_in_frame_mobjects(title, matrix_a_group, matrix_r_group)' in source


def test_scene_color_codes_matrix_columns_to_match_vectors() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'matrix_a_columns[0].set_color(A1_COLOR)' in source
    assert 'matrix_a_columns[1].set_color(A2_COLOR)' in source
    assert 'matrix_a_columns[2].set_color(A3_COLOR)' in source
    assert 'matrix_r_columns[0].set_color(A1_COLOR)' in source
    assert 'matrix_r_columns[1].set_color(A2_COLOR)' in source


def test_spatial_vector_labels_face_the_viewer() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'self.add_fixed_orientation_mobjects(*labels)' in source
    assert 'label.set_stroke(color=BACKGROUND, width=8, background=True)' in source


def test_scene_removes_uninformative_dot_field() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'Dot3D' not in source
    assert 'space_points' not in source
    assert 'dots = VGroup' not in source
    assert 'self.play(FadeIn(plane), run_time=1.7)' in source


def test_matrix_highlights_and_guides_are_fixed_in_frame() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'a_pivot_boxes, r_pivot_boxes, nonpivot_box, guides, pivot_caption, nonpivot_caption' in source
    assert 'self.add_fixed_in_frame_mobjects(' in source


def test_scene_explicitly_explains_pivot_and_nonpivot_highlights() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'pivot_caption = Text("Pivot columns in R"' in source
    assert 'nonpivot_caption = Text("The third column is nonpivot, so it is redundant."' in source


def test_scene_concludes_basis_comes_from_original_matrix() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\{\mathbf a_1,\mathbf a_2\}\text{ is a basis for }\operatorname{col}(A)" in source
    assert "Pivot positions come from R, but the basis columns come from A." in source
