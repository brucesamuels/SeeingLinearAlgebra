from pathlib import Path

SCENE_PATH = Path("scenes/rotations_reflections_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_header_and_revision() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Rotations and Reflections: Orthogonal Transformations"' in source
    assert 'SCENE_REVISION = "cp163_r6_final_spacing_cleanup"' in source
    assert 'class RotationsReflectionsPresentation(Scene)' in source


def test_scene_has_eight_cards_in_order() -> None:
    source = scene_source()
    construct = source.split("def construct", 1)[1].split("def _header", 1)[0]
    helpers = (
        '_rotation_from_basis_card',
        '_rotation_in_motion_card',
        '_inverse_rotation_card',
        '_reflection_geometry_card',
        '_reflection_inverse_card',
        '_why_orthogonal_card',
        '_specific_examples_orthogonal_card',
        '_compare_orientation_card',
    )
    positions = []
    for helper in helpers:
        assert f'self.{helper}()' in construct
        assert f'def {helper}' in source
        positions.append(construct.index(f'self.{helper}()'))
    assert positions == sorted(positions)


def test_graphic_cards_use_consistent_emphasized_grid() -> None:
    source = scene_source()
    assert 'background_line_style={"stroke_opacity": 0.34, "stroke_width": 1.6}' in source
    assert 'axis_config={"stroke_opacity": 0.72, "stroke_width": 2.2}' in source
    assert 'x_length=width' in source
    assert 'y_length=height' in source


def test_rotation_card_builds_matrix_from_basis_images() -> None:
    source = scene_source()
    for token in (
        r'R_\theta\mathbf e_1=(\cos\theta,\sin\theta)',
        r'R_\theta\mathbf e_2=(-\sin\theta,\cos\theta)',
        'self.lesson.ROTATION_MATRIX',
        'theta_arc = Angle(',
    ):
        assert token in source


def test_rotation_is_animated_as_rigid_motion() -> None:
    source = scene_source()
    card = source.split('def _rotation_in_motion_card', 1)[1].split('def _inverse_rotation_card', 1)[0]
    assert 'Rotate(moving, angle=self.snapshot.theta' in card
    assert 'Rotate(moving_v, angle=self.snapshot.theta' in card
    assert r'\theta=60^\circ' in card
    assert r'R_{60^\circ}' in card


def test_inverse_rotation_card_connects_transpose_and_opposite_angle() -> None:
    source = scene_source()
    card = source.split('def _inverse_rotation_card', 1)[1].split('def _reflection_geometry_card', 1)[0]
    assert r'R_{-\theta}R_\theta=I' in card
    assert 'self.lesson.ROTATION_INVERSE' in card
    assert r'R_\theta^TR_\theta=I' in card
    assert 'angle=-self.snapshot.theta' in card


def test_reflection_card_shows_fixed_and_reversed_directions() -> None:
    source = scene_source()
    card = source.split('def _reflection_geometry_card', 1)[1].split('def _reflection_inverse_card', 1)[0]
    assert r'H\mathbf e_1=\mathbf e_1' in card
    assert r'H\mathbf e_2=-\mathbf e_2' in card
    assert 'self.lesson.REFLECTION_MATRIX' in card
    assert 'mirror line' in card


def test_reflection_is_its_own_inverse() -> None:
    source = scene_source()
    card = source.split('def _reflection_inverse_card', 1)[1].split('def _why_orthogonal_card', 1)[0]
    assert r'H(H\mathbf v)=\mathbf v' in card
    assert r'H^2=I' in card
    assert 'self.lesson.REFLECTION_INVERSE' in card


def test_general_orthogonality_card_states_the_criterion_cleanly() -> None:
    source = scene_source()
    card = source.split('def _why_orthogonal_card', 1)[1].split('def _specific_examples_orthogonal_card', 1)[0]
    for token in (
        'self.lesson.ORTHOGONAL_CRITERION',
        'Text("Its two columns are perpendicular", font_size=22, color=WHITE)',
        'Text("and each column has length 1.", font_size=22, color=WHITE)',
        r'R_\theta=[R_\theta\mathbf e_1\;R_\theta\mathbf e_2]',
        r'\Rightarrow R_\theta^TR_\theta=I',
        r'H=[H\mathbf e_1\;H\mathbf e_2]',
        r'\Rightarrow H^TH=I',
    ):
        assert token in card


def test_specific_examples_card_checks_orthonormal_columns_in_actual_matrices() -> None:
    source = scene_source()
    card = source.split('def _specific_examples_orthogonal_card', 1)[1].split('def _compare_orientation_card', 1)[0]
    for token in (
        r'R_{60^\circ}=\begin{bmatrix}\frac12&-\frac{\sqrt3}{2}',
        r'\mathbf q_1^T\mathbf q_2=-\frac{\sqrt3}{4}+\frac{\sqrt3}{4}=0',
        r'\|\mathbf q_1\|^2=\frac14+\frac34=1,\quad \|\mathbf q_2\|^2=\frac34+\frac14=1',
        'The Pythagorean identity gives unit-length columns.',
        'max_note_width = left_box.width - 0.50',
        'pythagorean_note.scale_to_fit_width(max_note_width)',
        r'H=\begin{bmatrix}1&0\\0&-1\end{bmatrix}',
        r'\mathbf h_1^T\mathbf h_2=(1)(0)+(0)(-1)=0',
        r'\|\mathbf h_1\|=1,\quad \|\mathbf h_2\|=1',
        'Here the arithmetic is immediate.',
    ):
        assert token in card


def test_closing_card_distinguishes_orientation_by_determinant() -> None:
    source = scene_source()
    card = source.split('def _compare_orientation_card', 1)[1]
    assert 'Orientation distinguishes them' in card
    assert 'self.lesson_title_mobject, DOWN, buff=0.12' in card
    assert 'Rotation and reflection are both orthogonal' in card
    assert r'\det R_\theta=+1' in card
    assert r'\det H=-1' in card
    assert 'orientation preserved' in card
    assert 'orientation reversed' in card
    assert 'LEFT * 3.25 + DOWN * 0.62' in card
    assert 'RIGHT * 3.25 + DOWN * 0.62' in card
    assert 'gap_mid_y = 0.5 * (heading.get_bottom()[1] + title_band.get_top()[1])' in card
    assert 'orthogonal_text = Text(' in card


def test_main_geometry_cards_keep_math_in_right_column() -> None:
    source = scene_source()
    assert 'def _right_math(*mobjects)' in source
    assert ').move_to(RIGHT * 3.25 + DOWN * 0.20)' in source
    assert source.count('equations = self._right_math(') == 5
