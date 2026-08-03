from pathlib import Path

SOURCE_PATH = Path(
    "scenes/matrix_order_identity_undoing_presentation.py"
)


def source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_scene_and_title_are_present() -> None:
    text = source()
    assert "class MatrixOrderIdentityUndoingPresentation(Scene)" in text
    assert 'TITLE = "Order, Identity, and Undoing"' in text


def test_scene_shows_noncommutativity() -> None:
    text = source()
    assert "Same two transformations, different order" in text
    assert r"BA\neq AB" in text
    assert r"BA\mathbf{x}=(-3,1)" in text
    assert r"AB\mathbf{x}=(-1,1)" in text
    assert "A = shear,  B = reflect across the y-axis" in text


def test_scene_shows_identity_matrix() -> None:
    text = source()
    assert "The identity matrix changes nothing" in text
    assert r"I\mathbf{x}=\mathbf{x}" in text
    assert "do-nothing transformation" in text
    assert r"IA=A,\qquad AI=A" in text


def test_scene_shows_undoing_and_noninvertible_case() -> None:
    text = source()
    assert "Some transformations can be undone" in text
    assert r"A^{-1}A=I,\qquad AA^{-1}=I" in text
    assert "projection collapses information" in text
    assert "cannot be undone" in text


def test_scene_defers_full_inverse_study() -> None:
    text = source()
    assert "study inverses more fully with linear systems" in text


def test_scene_includes_pause_predict_and_assembly_bridge() -> None:
    text = source()
    assert "Pause and Predict" in text
    assert "Which matrix acts first in ACBx?" in text
    assert "B acts first." in text
    assert "assemble the Matrix Operations chapter" in text


def test_key_groups_fit_within_frame() -> None:
    text = source()
    assert "equation.scale_to_fit_width(8.8)" in text
    assert "top_line.scale_to_fit_width(7.7)" in text
    assert "projection_line.scale_to_fit_width(6.5)" in text


def test_scene_uses_revised_spacing_to_avoid_collisions() -> None:
    text = source()
    assert "move_to(RIGHT * 4.1 + UP * 1.0)" in text
    assert "formulas.move_to(RIGHT * 3.95 + DOWN * 1.02)" in text
    assert ").scale(0.94).move_to(DOWN * 0.82)" in text
    assert ").scale(0.42).move_to(DOWN * 1.55)" in text
    assert ").scale(0.82).move_to(DOWN * 2.22)" in text
    assert "top_line.move_to(UP * 0.96)" in text
    assert ").scale(0.35).move_to(DOWN * 0.02)" in text
    assert ").scale(0.72).move_to(DOWN * 0.76)" in text
    assert "projection_line.move_to(DOWN * 1.98)" in text
    assert ").scale(0.32).move_to(DOWN * 3.04)" in text
