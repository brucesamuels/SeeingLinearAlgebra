from pathlib import Path

SCENE_PATH = Path("scenes/qr_factorization_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_header_and_revision() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "QR Factorization: Gram-Schmidt in Matrix Form"' in source
    assert 'SCENE_REVISION = "cp160_r4_right_title_clearance"' in source
    assert 'class QRFactorizationPresentation(Scene)' in source


def test_scene_has_seven_cards() -> None:
    source = scene_source()
    for helper in (
        '_original_columns_card',
        '_orthonormal_columns_card',
        '_first_column_coefficients_card',
        '_second_column_coefficients_card',
        '_assemble_qr_card',
        '_inverse_trick_for_r_card',
        '_why_qr_helps_card',
    ):
        assert f'self.{helper}()' in source
        assert f'def {helper}' in source


def test_graphic_cards_use_emphasized_coordinate_grid() -> None:
    source = scene_source()
    assert 'background_line_style={"stroke_opacity": 0.34, "stroke_width": 1.6}' in source
    assert 'axis_config={"stroke_opacity": 0.72, "stroke_width": 2.2}' in source
    assert source.count('plane = self._plane()') >= 3
    assert 'plane = self._plane(closeup=True)' in source


def test_scene_connects_gram_schmidt_to_q() -> None:
    source = scene_source()
    for token in (
        r'\mathbf q_1=\frac1{\sqrt5}(1,2)',
        r'\mathbf q_2=\frac1{\sqrt5}(2,-1)',
        r'Q=\begin{bmatrix}\vert&\vert\\\mathbf q_1&\mathbf q_2\\\vert&\vert\end{bmatrix}',
        'self.lesson.Q_ORTHONORMAL',
    ):
        assert token in source
    assert 'def _right_angle_marker' in source


def test_scene_builds_r_from_column_coordinates() -> None:
    source = scene_source()
    for token in (
        r'\mathbf a_1=\sqrt5\,\mathbf q_1+0\,\mathbf q_2',
        r'\mathbf a_2=2\sqrt5\,\mathbf q_1+\sqrt5\,\mathbf q_2',
        r'R=\begin{bmatrix}\sqrt5&2\sqrt5\\0&\sqrt5\end{bmatrix}',
        'self.lesson.QR_FACTORIZATION',
    ):
        assert token in source


def test_second_column_card_uses_head_to_tail_decomposition() -> None:
    source = scene_source()
    assert 'a2_q1 = Arrow(' in source
    assert 'a2_q2 = Arrow(' in source
    assert 'start=plane.c2p(*first_end)' not in source  # positional args keep Manim 0.20 compatibility
    assert 'plane.c2p(*first_end),' in source
    assert 'plane.c2p(*self.snapshot.a2),' in source


def test_scene_bridges_qr_to_triangular_solve_and_least_squares_question() -> None:
    source = scene_source()
    assert 'self.lesson.R_FROM_QA' in source
    assert r'R\mathbf x=Q^T\mathbf b' in source
    assert 'self.lesson.bridge_prompt' in source


def test_scene_includes_inverse_trick_for_r() -> None:
    source = scene_source()
    for token in (
        'A computational shortcut for R',
        r'Q^{-1}A=Q^{-1}QR',
        r'Q^{-1}A=R',
        'self.lesson.Q_INVERSE_TRANSPOSE',
        'self.lesson.R_FROM_QA',
        r'\begin{bmatrix}5&10\\0&5\end{bmatrix}',
        'Because this Q is square and orthogonal, its inverse is its transpose.',
    ):
        assert token in source


def test_inverse_card_titles_are_raised_above_the_math() -> None:
    source = scene_source()
    assert "LEFT * 3.15 + UP * 1.55" in source
    assert "RIGHT * 3.10 + UP * 1.78" in source


def test_inverse_card_right_math_block_is_lowered_for_clearance() -> None:
    source = scene_source()
    assert "RIGHT * 3.10 + UP * 1.78" in source
    assert ").arrange(DOWN, buff=0.27).move_to(RIGHT * 3.05 + DOWN * 0.42)" in source
