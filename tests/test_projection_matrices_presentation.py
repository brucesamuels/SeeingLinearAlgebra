from pathlib import Path

SCENE_PATH = Path("scenes/projection_matrices_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_header_and_revision() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Projection Matrices: Symmetric and Idempotent"' in source
    assert 'SCENE_REVISION = "cp164_r2_general_to_orthonormal_projection"' in source
    assert 'class ProjectionMatricesPresentation(Scene)' in source


def test_scene_has_eight_cards_in_order() -> None:
    source = scene_source()
    construct = source.split("def construct", 1)[1].split("def _header", 1)[0]
    helpers = (
        '_from_basis_to_matrix_card',
        '_general_to_orthonormal_card',
        '_geometry_of_projection_card',
        '_idempotent_card',
        '_symmetric_card',
        '_concrete_example_card',
        '_subspace_complement_card',
        '_projection_vs_orthogonal_card',
    )
    positions = []
    for helper in helpers:
        assert f'self.{helper}()' in construct
        assert f'def {helper}' in source
        positions.append(construct.index(f'self.{helper}()'))
    assert positions == sorted(positions)


def test_graphic_cards_use_emphasized_grid() -> None:
    source = scene_source()
    assert 'background_line_style={"stroke_opacity": 0.34, "stroke_width": 1.6}' in source
    assert 'axis_config={"stroke_opacity": 0.72, "stroke_width": 2.2}' in source
    assert source.count('self._plane(') >= 4


def test_first_card_connects_orthonormal_basis_to_projection_matrix() -> None:
    source = scene_source()
    card = source.split('def _from_basis_to_matrix_card', 1)[1].split('def _geometry_of_projection_card', 1)[0]
    assert r'Q^TQ=I' in card
    assert 'self.lesson.GENERAL_PROJECTION' in card
    assert 'self.lesson.GENERAL_ACTION' in card
    assert 'W = span(q)' in card


def test_new_card_derives_qqt_from_general_projection_formula() -> None:
    source = scene_source()
    card = source.split('def _general_to_orthonormal_card', 1)[1].split('def _geometry_of_projection_card', 1)[0]
    for token in (
        'self.lesson.FULL_COLUMN_PROJECTION',
        r'P=Q(Q^TQ)^{-1}Q^T',
        r'Q^TQ=I',
        r'P=QI^{-1}Q^T',
        r'P=QQ^T',
        'Orthonormal columns make the Gram matrix Q^TQ equal to the identity',
    ):
        assert token in card


def test_geometry_card_shows_orthogonal_residual() -> None:
    source = scene_source()
    card = source.split('def _geometry_of_projection_card', 1)[1].split('def _idempotent_card', 1)[0]
    assert r'\mathbf v=P\mathbf v+\mathbf r' in card
    assert r'\mathbf r\perp W' in card
    assert 'self._right_angle_marker(' in card
    assert 'residual = self._segment(' in card


def test_idempotent_card_explicitly_projects_twice() -> None:
    source = scene_source()
    card = source.split('def _idempotent_card', 1)[1].split('def _symmetric_card', 1)[0]
    assert r'P(P\mathbf v)=P\mathbf v' in card
    assert 'self.lesson.IDEMPOTENT_RULE' in card
    assert 'TransformFromCopy(p_arrow, second_arrow)' in card


def test_symmetric_card_derives_transpose_rule() -> None:
    source = scene_source()
    card = source.split('def _symmetric_card', 1)[1].split('def _concrete_example_card', 1)[0]
    assert r'P^T=(QQ^T)^T' in card
    assert r'\phantom{P^T}=QQ^T' in card
    assert 'self.lesson.SYMMETRY_RULE' in card


def test_concrete_example_uses_q_outer_product_and_specific_vector() -> None:
    source = scene_source()
    card = source.split('def _concrete_example_card', 1)[1].split('def _subspace_complement_card', 1)[0]
    for token in (
        r'\mathbf q=\frac1{\sqrt5}\begin{bmatrix}1\\2\end{bmatrix}',
        r'P=\frac15\begin{bmatrix}1&2\\2&4\end{bmatrix}',
        r'\mathbf v=\begin{bmatrix}4\\1\end{bmatrix}',
        r'P\mathbf v=\begin{bmatrix}6/5\\12/5\end{bmatrix}',
        r'\mathbf r=\begin{bmatrix}14/5\\-7/5\end{bmatrix}',
    ):
        assert token in card


def test_subspace_complement_card_shows_identity_and_collapse_directions() -> None:
    source = scene_source()
    card = source.split('def _subspace_complement_card', 1)[1].split('def _projection_vs_orthogonal_card', 1)[0]
    assert r'P\mathbf q=\mathbf q' in card
    assert r'P\mathbf n=\mathbf 0' in card
    assert r'\operatorname{range}(P)=W' in card
    assert r'\operatorname{null}(P)=W^\perp' in card


def test_final_card_distinguishes_projection_from_orthogonal_matrix() -> None:
    source = scene_source()
    card = source.split('def _projection_vs_orthogonal_card', 1)[1]
    assert 'self.lesson.IDEMPOTENT_RULE' in card
    assert 'self.lesson.SYMMETRY_RULE' in card
    assert 'self.lesson.ORTHOGONAL_MATRIX_RULE' in card
    assert 'moves vectors toward a subspace' in card
    assert 'preserves lengths and angles' in card
    assert 'does not collapse dimension' in card
    assert 'self.lesson.CLOSING_IDEA' in card
    assert 'comparison_mid_y = 0.5 * (self.lesson_title_mobject.get_bottom()[1] + title_band.get_top()[1])' in card
    assert ').move_to(np.array([0.0, comparison_mid_y, 0.0]))' in card


def test_graphic_cards_keep_math_in_reserved_right_column() -> None:
    source = scene_source()
    assert 'def _right_math(*mobjects)' in source
    assert ').move_to(RIGHT * 3.30 + DOWN * 0.10)' in source
    assert source.count('equations = self._right_math(') == 4
