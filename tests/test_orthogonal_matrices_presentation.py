from pathlib import Path

SCENE_PATH = Path("scenes/orthogonal_matrices_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_header_and_revision() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Orthogonal Matrices Preserve Geometry"' in source
    assert 'SCENE_REVISION = "cp162_r4_balanced_equation_columns"' in source
    assert 'class OrthogonalMatricesPresentation(Scene)' in source


def test_scene_has_six_cards() -> None:
    source = scene_source()
    for helper in (
        '_orthonormal_columns_card',
        '_length_preservation_card',
        '_angle_preservation_card',
        '_rigid_motion_card',
        '_determinant_card',
        '_closing_card',
    ):
        assert f'self.{helper}()' in source
        assert f'def {helper}' in source


def test_all_graphic_cards_use_the_same_grid_style() -> None:
    source = scene_source()
    assert 'background_line_style={"stroke_opacity": 0.34, "stroke_width": 1.6}' in source
    assert 'axis_config={"stroke_opacity": 0.72, "stroke_width": 2.2}' in source
    assert 'def _plane(center' in source
    assert source.count('self._plane(') >= 8


def test_scene_establishes_orthogonal_matrix_from_orthonormal_columns() -> None:
    source = scene_source()
    for token in (
        r'Q=\begin{bmatrix}\frac{1}{\sqrt2}&-\frac{1}{\sqrt2}\\[4pt]\frac{1}{\sqrt2}&\frac{1}{\sqrt2}\end{bmatrix}',
        'self.lesson.ORTHOGONAL_TEST',
        'self.lesson.INVERSE_RULE',
        'unit_circle = self._circle_for_radius(plane, 1.0, GREEN)',
    ):
        assert token in source


def test_scene_explicitly_shows_length_and_dot_product_preservation() -> None:
    source = scene_source()
    for token in (
        r'\|\mathbf v\|=\sqrt5',
        r'\|Q\mathbf v\|=\sqrt5',
        'self.lesson.LENGTH_RULE',
        r'\mathbf u^T\mathbf v=4',
        r'(Q\mathbf u)^T(Q\mathbf v)=4',
        'self.lesson.DOT_RULE',
    ):
        assert token in source


def test_scene_includes_rigid_motion_and_determinant_distinction() -> None:
    source = scene_source()
    for token in (
        r'Q\text{ sends an orthonormal basis to another orthonormal basis}',
        r'\text{No stretching, no shearing — only rigid motion.}',
        r'\det R=1',
        r'\det H=-1',
        'rotation',
        'reflection',
    ):
        assert token in source


def test_closing_card_summarizes_geometry() -> None:
    source = scene_source()
    assert r'\boxed{\text{Orthogonal matrices preserve lengths and angles.}}' in source
    assert r'\det Q=\pm 1' in source
    assert 'self.lesson.CLOSING_IDEA' in source


def test_cards_two_to_four_use_clear_graph_and_label_layouts() -> None:
    source = scene_source()
    assert 'left_plane = self._plane(LEFT * 4.05 + DOWN * 0.70, width=3.55, height=3.55)' in source
    assert 'right_plane = self._plane(LEFT * 0.55 + DOWN * 0.70, width=3.55, height=3.55)' in source
    assert source.count('left_plane = self._plane(LEFT * 3.35 + DOWN * 0.74)') >= 2
    assert source.count('right_plane = self._plane(RIGHT * 2.05 + DOWN * 0.74)') >= 2
    for token in (
        'v_label = self._label(r"\\mathbf v", left_plane, self.snapshot.v, BLUE, RIGHT * 0.32 + DOWN * 0.04)',
        'qv_label = self._label(r"Q\\mathbf v", right_plane, self.snapshot.Qv, BLUE, RIGHT * 0.40 + DOWN * 0.02)',
        'u_label = self._label(r"\\mathbf u", left_plane, self.snapshot.u, ORANGE, LEFT * 0.42 + DOWN * 0.02)',
        'qu_label = self._label(r"Q\\mathbf u", right_plane, self.snapshot.Qu, ORANGE, RIGHT * 0.60 + DOWN * 0.02)',
        'e2_label = self._label(r"\\mathbf e_2", left_plane, np.array([0.0, 1.0]), PURPLE, LEFT * 0.26 + DOWN * 0.04)',
        'q2_label = self._label(r"Q\\mathbf e_2", right_plane, self.snapshot.q2, PURPLE, LEFT * 0.60 + DOWN * 0.00)',
    ):
        assert token in source


def test_equation_blocks_use_balanced_layout_positions() -> None:
    source = scene_source()
    assert ').arrange(DOWN, buff=0.28).move_to(RIGHT * 3.05 + UP * 0.08)' in source
    assert ').arrange(DOWN, buff=0.24).move_to(RIGHT * 4.55 + DOWN * 0.82)' in source
    assert ').arrange(DOWN, buff=0.24).move_to(RIGHT * 0.10 + DOWN * 2.22)' in source
    assert ').arrange(DOWN, buff=0.25).move_to(RIGHT * 0.12 + DOWN * 2.00)' in source
    assert 'right_plane = self._plane(RIGHT * 0.90 + DOWN * 0.62' in source
    assert ').arrange(DOWN, buff=0.22).move_to(RIGHT * 4.72 + DOWN * 0.78)' in source


def test_construct_progresses_through_all_six_cards_in_order() -> None:
    source = scene_source()
    construct = source.split("def construct", 1)[1].split("def _header", 1)[0]
    helpers = [
        "_orthonormal_columns_card",
        "_length_preservation_card",
        "_angle_preservation_card",
        "_rigid_motion_card",
        "_determinant_card",
        "_closing_card",
    ]
    positions = [construct.index(f"self.{helper}()") for helper in helpers]
    assert positions == sorted(positions)
