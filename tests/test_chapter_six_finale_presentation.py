from pathlib import Path

SCENE_PATH = Path("scenes/chapter_six_finale_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_header_and_revision() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Orthogonality and Projection: The Big Picture"' in source
    assert 'SCENE_REVISION = "cp165_r2_center_matrix_families_heading"' in source
    assert 'class ChapterSixFinalePresentation(Scene)' in source


def test_scene_has_eight_cards_in_order() -> None:
    source = scene_source()
    construct = source.split("def construct", 1)[1].split("def _header", 1)[0]
    helpers = (
        '_perpendicularity_card',
        '_projection_decomposition_card',
        '_orthonormal_coordinates_card',
        '_gram_schmidt_qr_card',
        '_least_squares_card',
        '_two_matrix_families_card',
        '_recognition_card',
        '_closing_card',
    )
    positions = []
    for helper in helpers:
        assert f'self.{helper}()' in construct
        assert f'def {helper}' in source
        positions.append(construct.index(f'self.{helper}()'))
    assert positions == sorted(positions)


def test_graphic_cards_use_emphasized_grid_and_right_angle_markers() -> None:
    source = scene_source()
    assert 'background_line_style={"stroke_opacity": 0.34, "stroke_width": 1.6}' in source
    assert 'axis_config={"stroke_opacity": 0.72, "stroke_width": 2.2}' in source
    assert source.count('self._plane(') >= 3
    assert source.count('self._right_angle_marker(') >= 3


def test_perpendicularity_card_returns_to_zero_dot_product() -> None:
    source = scene_source()
    card = source.split('def _perpendicularity_card', 1)[1].split('def _projection_decomposition_card', 1)[0]
    assert r'\mathbf u^T\mathbf v=2-2=0' in card
    assert 'self.lesson.DOT_RULE' in card
    assert 'Perpendicular geometry becomes a zero dot product' in card


def test_projection_card_synthesizes_decomposition_and_projection_matrix() -> None:
    source = scene_source()
    card = source.split('def _projection_decomposition_card', 1)[1].split('def _orthonormal_coordinates_card', 1)[0]
    assert 'self.lesson.DECOMPOSITION_RULE' in card
    assert r'P\mathbf v\in W' in card
    assert r'\mathbf r\in W^\perp' in card
    assert r'P=QQ^T' in card


def test_orthonormal_coordinates_card_connects_coordinates_and_projection() -> None:
    source = scene_source()
    card = source.split('def _orthonormal_coordinates_card', 1)[1].split('def _gram_schmidt_qr_card', 1)[0]
    assert r'Q^TQ=I' in card
    assert r'\mathbf c=Q^T\mathbf v' in card
    assert r'P\mathbf v=Q\mathbf c=QQ^T\mathbf v' in card


def test_gram_schmidt_card_builds_toward_qr() -> None:
    source = scene_source()
    card = source.split('def _gram_schmidt_qr_card', 1)[1].split('def _least_squares_card', 1)[0]
    assert 'Gram-Schmidt' in card
    assert 'subtract projections' in card
    assert 'then normalize' in card
    assert 'self.lesson.QR_RULE' in card


def test_least_squares_card_connects_geometry_normal_equation_and_qr() -> None:
    source = scene_source()
    card = source.split('def _least_squares_card', 1)[1].split('def _two_matrix_families_card', 1)[0]
    assert r'\mathbf r\perp\operatorname{Col}(A)' in card
    assert 'self.lesson.LEAST_SQUARES_RULE' in card
    assert 'self.lesson.NORMAL_EQUATION' in card
    assert 'self.lesson.QR_LEAST_SQUARES' in card


def test_matrix_families_card_keeps_projection_and_orthogonal_matrix_distinct() -> None:
    source = scene_source()
    card = source.split('def _two_matrix_families_card', 1)[1].split('def _recognition_card', 1)[0]
    assert 'Projection matrix P' in card
    assert 'Square orthogonal matrix U' in card
    assert 'self.lesson.PROJECTION_SIGNATURE' in card
    assert 'self.lesson.ORTHOGONAL_SIGNATURE' in card
    assert 'can collapse dimension' in card
    assert 'preserves lengths and angles' in card
    assert 'title_band = VGroup(left_title, right_title)' in card
    assert 'heading_mid_y = 0.5 * (self.lesson_title_mobject.get_bottom()[1] + title_band.get_top()[1])' in card
    assert ').move_to(np.array([0.0, heading_mid_y, 0.0]))' in card


def test_recognition_card_has_four_chapter_signatures() -> None:
    source = scene_source()
    card = source.split('def _recognition_card', 1)[1].split('def _closing_card', 1)[0]
    for token in (
        r'\mathbf u^T\mathbf v=0',
        r'Q^TQ=I',
        r'P^T=P,\ P^2=P',
        r'A^T(\mathbf b-A\hat{\mathbf x})=0',
        'perpendicular vectors',
        'orthonormal columns',
        'orthogonal projection',
        'least-squares residual',
    ):
        assert token in card


def test_closing_card_is_sparse_and_ends_on_the_chapter_idea() -> None:
    source = scene_source()
    card = source.split('def _closing_card', 1)[1]
    assert 'The chapter in one sentence' in card
    assert 'self.lesson.CLOSING_IDEA' in card
    assert 'perpendicularity' in card
    assert 'projection' in card
    assert 'orthonormal bases' in card
    assert 'QR and least squares' in card
    assert 'Geometry tells us what is true; orthogonality gives us an efficient way to compute it.' in card
