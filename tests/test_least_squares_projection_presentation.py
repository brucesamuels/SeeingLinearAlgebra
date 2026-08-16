from pathlib import Path

SCENE_PATH = Path("scenes/least_squares_projection_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_header_and_revision() -> None:
    source = scene_source()
    assert 'LESSON_TITLE = "Least Squares: Projection and the Normal Equation"' in source
    assert 'SCENE_REVISION = "cp161_r14_lower_penultimate_math_blocks"' in source
    assert 'class LeastSquaresProjectionPresentation(ThreeDScene)' in source


def test_scene_has_seven_cards() -> None:
    source = scene_source()
    for helper in (
        '_no_exact_solution_card',
        '_closest_point_card',
        '_residual_orthogonality_card',
        '_matrix_orthogonality_card',
        '_normal_equation_card',
        '_solve_normal_equation_card',
        '_qr_route_card',
    ):
        assert f'self.{helper}()' in source
        assert f'def {helper}' in source


def test_geometry_cards_show_column_space_projection_and_residual() -> None:
    source = scene_source()
    assert 'Polygon(' in source
    assert 'Arrow3D(' in source
    assert r'\operatorname{Col}(A)' in source
    assert r'A\widehat{\mathbf x}=\operatorname{proj}_{\operatorname{Col}(A)}\mathbf b' in source
    assert r'\mathbf r=\mathbf b-A\widehat{\mathbf x}' in source
    assert 'def _right_angle_marker' in source


def test_scene_turns_perpendicularity_into_transpose_equation() -> None:
    source = scene_source()
    assert r'\mathbf a_1^T\mathbf r=0,\qquad \mathbf a_2^T\mathbf r=0' in source
    assert r'\begin{bmatrix}\mathbf a_1^T\\\mathbf a_2^T\end{bmatrix}\mathbf r=\mathbf 0' in source
    assert 'self.lesson.RESIDUAL_ORTHOGONALITY' in source


def test_normal_equation_gets_dedicated_highlight_card() -> None:
    source = scene_source()
    assert 'Text("THE NORMAL EQUATION"' in source
    assert 'normal_equation = MathTex(self.lesson.NORMAL_EQUATION, font_size=57, color=YELLOW)' in source
    assert 'SurroundingRectangle(' in source
    assert r'A^T(\mathbf b-A\widehat{\mathbf x})=\mathbf 0' in source
    assert r'A^T\mathbf b-A^TA\widehat{\mathbf x}=\mathbf 0' in source
    assert 'self.wait(self.HOLD_TIME + 0.8)' in source


def test_scene_computes_normal_equation_example() -> None:
    source = scene_source()
    for token in (
        r'A^TA=\begin{bmatrix}2&1\\1&2\end{bmatrix}',
        r'A^T\mathbf b=\begin{bmatrix}3\\3\end{bmatrix}',
        r'\widehat{\mathbf x}=\begin{bmatrix}1\\1\end{bmatrix}',
        r'A\widehat{\mathbf x}=\begin{bmatrix}1\\1\\2\end{bmatrix}',
        r'\mathbf r=\mathbf b-A\widehat{\mathbf x}=\begin{bmatrix}1\\1\\-1\end{bmatrix}',
    ):
        assert token in source


def test_scene_connects_normal_equation_to_qr_route() -> None:
    source = scene_source()
    assert 'Normal equation' in source
    assert 'QR route' in source
    assert 'self.lesson.NORMAL_EQUATION' in source
    assert 'self.lesson.QR_LEAST_SQUARES' in source
    assert 'without forming A^T A' in source



def test_projection_cards_use_one_consistent_camera_view() -> None:
    source = scene_source()
    assert "def _set_projection_geometry_view(self) -> None:" in source
    assert "phi=111.42 * np.pi / 180" in source
    assert "theta=101.31 * np.pi / 180" in source
    assert "gamma=-118.71 * np.pi / 180" in source
    assert "zoom=0.88" in source
    construct = source.split("def construct", 1)[1].split("def _set_projection_geometry_view", 1)[0]
    assert construct.count("self._set_projection_geometry_view()") == 1
    assert "_set_projection_right_angle_view" not in source


def test_opening_axes_use_equal_coordinate_scale() -> None:
    source = scene_source()
    assert "x_range=(-1.5, 3.0, 1)" in source
    assert "y_range=(-1.5, 3.0, 1)" in source
    assert "z_range=(-2.0, 4.5, 1)" in source
    assert "x_length=4.5" in source
    assert "y_length=4.5" in source
    assert "z_length=6.5" in source
    assert ").shift(LEFT * 0.907 + DOWN * 1.041 + IN * 2.149)" in source


def test_cards_two_and_three_preserve_same_visual_language() -> None:
    source = scene_source()
    card2 = source.split("def _closest_point_card", 1)[1].split("def _residual_orthogonality_card", 1)[0]
    card3 = source.split("def _residual_orthogonality_card", 1)[1].split("def _matrix_orthogonality_card", 1)[0]
    for card in (card2, card3):
        assert "axes = self._axes3d()" in card
        assert "plane = self._column_space_patch(axes)" in card
        assert "FadeIn(axes)" in card
        assert "-self.snapshot.projection" in card
        assert "Create(marker)" in card
        assert "marker_a1" not in card
        assert "marker_a2" not in card
        assert "_column_space_projection_patch" not in card
        assert "_in_plane_guide" not in card


def test_card2_projection_and_residual_form_clean_right_angle_at_projection_point() -> None:
    source = scene_source()
    card2 = source.split("def _closest_point_card", 1)[1].split("def _residual_orthogonality_card", 1)[0]
    assert "p_arrow = self._origin_arrow(axes, self.snapshot.projection, GREEN)" in card2
    assert "axes.c2p(*self.snapshot.projection)" in card2
    assert "axes.c2p(*self.snapshot.b)" in card2
    assert "-self.snapshot.projection" in card2
    assert "self.snapshot.residual" in card2
    assert "size=0.42" in card2
    assert "The closest point is where the perpendicular from b meets the column space." in card2


def test_card3_uses_single_clean_right_angle_marker_and_projection_label() -> None:
    source = scene_source()
    card3 = source.split("def _residual_orthogonality_card", 1)[1].split("def _matrix_orthogonality_card", 1)[0]
    assert "marker = self._right_angle_marker(" in card3
    assert "size=0.40" in card3
    assert "marker_a1" not in card3
    assert "marker_a2" not in card3
    assert 'r"A\\widehat{\\mathbf x}"' in card3
    assert "self.remove_fixed_orientation_mobjects(p_label, r_label)" in card3


def test_opening_axes_fade_in_without_isolated_arrowhead() -> None:
    source = scene_source()
    assert source.count("FadeIn(axes)") == 3
    assert "Create(axes)" not in source


def test_default_view_is_restored_after_geometry_cards() -> None:
    source = scene_source()
    assert "self._residual_orthogonality_card()" in source
    assert "self._set_default_view()" in source
    assert "self.set_camera_orientation(phi=67 * np.pi / 180, theta=-48 * np.pi / 180, zoom=0.86)" in source


def test_projection_axes_disable_tips_to_avoid_stray_arrowhead_artifact() -> None:
    source = scene_source()
    assert "axis_config={\"stroke_opacity\": 0.28, \"stroke_width\": 1.5, \"include_tip\": False}" in source


def test_penultimate_card_lowers_math_blocks_to_clear_heading() -> None:
    source = scene_source()
    card = source.split("def _solve_normal_equation_card", 1)[1].split("def _qr_route_card", 1)[0]
    assert ").arrange(DOWN, buff=0.28).move_to(LEFT * 1.8 + DOWN * 0.34)" in card
    assert ").arrange(DOWN, buff=0.30).move_to(RIGHT * 3.20 + DOWN * 0.38)" in card
    assert "divider = Line(UP * 1.22, DOWN * 2.33, color=GREY_B, stroke_opacity=0.45)" in card
