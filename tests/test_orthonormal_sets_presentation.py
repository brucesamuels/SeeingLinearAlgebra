from pathlib import Path

SCENE_PATH = Path("scenes/orthonormal_sets_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_uses_chapter_header_and_3d_scene() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Orthonormal Sets"' in source
    assert "class OrthonormalSetsPresentation(ThreeDScene)" in source
    assert 'SCENE_REVISION = "cp152_r2_slower_transitions"' in source


def test_scene_has_six_cards() -> None:
    source = scene_source()
    for helper in (
        "_from_orthogonal_to_orthonormal",
        "_definition_card",
        "_normalization_card",
        "_gram_matrix_card",
        "_coordinates_card",
        "_projection_bridge_card",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_normalization_card_uses_approved_3d_camera_family() -> None:
    source = scene_source()
    assert "ThreeDAxes(" in source
    assert "Arrow3D" in source
    assert "theta=-15 * DEGREES" in source
    assert "theta=28 * DEGREES" in source
    assert "ReplacementTransform(old, new)" in source


def test_scene_defines_orthonormality_and_kronecker_form() -> None:
    source = scene_source()
    assert "self.lesson.DEFINITION" in source
    assert "self.lesson.KRONECKER" in source
    assert "Different vectors are perpendicular; each vector has unit length." in source


def test_scene_includes_qtq_identity() -> None:
    source = scene_source()
    assert "self.lesson.MATRIX_IDENTITY" in source
    assert 'r"Q^TQ="' in source
    assert "Orthonormal columns have identity as their Gram matrix." in source


def test_scene_derives_coordinates_from_dot_products() -> None:
    source = scene_source()
    assert "self.lesson.COORDINATE_RULE" in source
    assert r"\mathbf{q}_j\cdot\mathbf{x}" in source
    assert r"=c_j" in source
    assert "dot products read off the coordinates directly" in source


def test_scene_bridges_to_projection_without_giving_full_projection_formula() -> None:
    source = scene_source()
    assert "How much of a vector points in one chosen direction?" in source
    assert r"\mathbf{q}\cdot\mathbf{x}" in source
    assert "leads to projection" in source
    assert r"(\mathbf{q}\cdot\mathbf{x})\mathbf{q}" not in source


def test_scene_does_not_reference_checkpoint_numbers_to_students() -> None:
    source = scene_source()
    student_strings = (
        "Orthogonality separates directions.",
        "What changes if every vector also has length 1?",
        "Normalize without changing direction",
        "All pairwise dot products at once",
        "Why unit length is so useful",
        "Next question",
    )
    for text in student_strings:
        assert text in source
    assert 'Text("CP151' not in source
    assert 'Text("CP152' not in source


def test_scene_uses_slower_deliberate_pacing() -> None:
    source = scene_source()
    assert "TRANSITION_TIME = 1.35" in source
    assert "EMPHASIS_TIME = 1.15" in source
    assert "HOLD_TIME = 2.6" in source
    assert "LONG_HOLD_TIME = 3.0" in source
    assert "run_time=3.4" in source
    assert "run_time=0.95" in source
