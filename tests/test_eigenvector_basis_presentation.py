from pathlib import Path

SCENE_PATH = Path("scenes/eigenvector_basis_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_title_and_basis_are_explicit() -> None:
    text = source()
    assert 'LESSON_TITLE = "An Eigenvector Basis"' in text
    assert r"\mathbf v_1=\begin{bmatrix}0\\0\\1\end{bmatrix}" in text
    assert r"\mathbf v_2=\begin{bmatrix}1\\-2\\0\end{bmatrix}" in text
    assert r"\mathbf v_3=\begin{bmatrix}1\\1\\0\end{bmatrix}" in text


def test_generic_vector_is_decomposed_in_eigenbasis() -> None:
    text = source()
    assert r"\mathbf x=\mathbf v_1+\mathbf v_2+\mathbf v_3" in text
    assert r"[\mathbf x]_{\mathcal B}=\begin{bmatrix}1\\1\\1\end{bmatrix}" in text


def test_transformation_scales_components_independently() -> None:
    text = source()
    assert r"A\mathbf v_1=1\mathbf v_1" in text
    assert r"A\mathbf v_2=2\mathbf v_2" in text
    assert r"A\mathbf v_3=5\mathbf v_3" in text
    assert r"[A\mathbf x]_{\mathcal B}=\begin{bmatrix}1\\2\\5\end{bmatrix}" in text


def test_diagonal_coordinate_action_is_shown_without_full_diagonalization() -> None:
    text = source()
    assert r"\begin{bmatrix}1&0&0\\0&2&0\\0&0&5\end{bmatrix}" in text
    assert "PDP" not in text
    assert "P^{-1}" not in text


def test_3d_is_used_without_camera_animation() -> None:
    text = source()
    assert "class EigenvectorBasisPresentation(ThreeDScene):" in text
    assert "ThreeDAxes" in text
    assert "Arrow3D" in text
    assert "begin_ambient_camera_rotation" not in text


def test_student_facing_scene_omits_checkpoint_number() -> None:
    assert "CP174" not in source()


def test_action_tex_separators_do_not_merge_with_next_A() -> None:
    text = source()
    assert r"\qquadA" not in text
    assert r"\qquad " in text


def test_card3_vectors_keep_valid_latex_row_breaks() -> None:
    text = source()
    assert r"\begin{bmatrix}2\\-1\\1\end{bmatrix}" in text
    assert r"[\mathbf x]_{\mathcal B}=\begin{bmatrix}1\\1\\1\end{bmatrix}" in text
    assert r"\begin{bmatrix}2\-1\1\end{bmatrix}" not in text


def test_labels_are_attached_to_3d_geometry_and_shift_with_it() -> None:
    text = source()
    assert 'move_to(axes.c2p(0.12, 0.05, 1.28))' in text
    assert 'move_to(axes.c2p(1.25, -2.2, 0.12))' in text
    assert 'move_to(axes.c2p(1.18, 1.18, 0.10))' in text
    assert 'self.add_fixed_in_frame_mobjects(*labels)' not in text
    assert 'geometry_group = VGroup(axes, v1, v2, v3, *labels)' in text
    assert 'layout_shift = self._screen_plane_shift(left=2.6, down=0.45)' in text
    assert 'geometry_group.animate.shift(layout_shift)' in text
    assert 'x_arrow.shift(LEFT * 2.6 + DOWN * 0.45)' not in text

def test_example_vector_is_not_double_shifted_and_fades_before_Ax() -> None:
    text = source()
    assert 'x_arrow = Arrow3D(start=axes.c2p(0,0,0), end=axes.c2p(*example.standard_vector), color=ORANGE, thickness=0.055)' in text
    assert 'x_arrow.shift(' not in text
    assert 'self.play(FadeOut(x_arrow), run_time=0.4)' in text
    assert 'self.play(FadeIn(ax_arrow), run_time=0.55)' in text



def test_card3_orange_vector_is_emphasized_and_white_fixed_text_is_cleaned_up() -> None:
    text = source()
    assert 'color=ORANGE, thickness=0.055' in text
    assert 'x_label = MathTex(r"\\mathbf x", font_size=34, color=ORANGE)' in text
    assert 'self.play(FadeOut(decomposition), FadeOut(coords), FadeOut(x_label), run_time=0.5)' in text
    assert 'self.remove(decomposition, coords, x_label)' in text
    assert 'self.play(FadeOut(algebra), FadeIn(action))' not in text

def test_repositioning_stays_in_camera_screen_plane() -> None:
    text = source()
    assert 'screen_right = np.array([-np.sin(theta), np.cos(theta), 0.0])' in text
    assert 'screen_up = np.array([' in text
    assert 'return -left * screen_right - down * screen_up' in text
    assert 'geometry_group.animate.shift(LEFT * 2.6 + DOWN * 0.45)' not in text
    assert 'set_camera_orientation(phi=self.CAMERA_PHI, theta=self.CAMERA_THETA, zoom=0.82)' in text

