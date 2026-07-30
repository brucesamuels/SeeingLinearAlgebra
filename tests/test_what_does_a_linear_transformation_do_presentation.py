from pathlib import Path

from engine.planar_affine_transformation import CANDIDATE_TRANSFORMATIONS


SCENE = Path("scenes/what_does_a_linear_transformation_do_presentation.py")


def test_candidate_sequence_contains_required_geometric_actions() -> None:
    names = tuple(name for name, _ in CANDIDATE_TRANSFORMATIONS)
    assert names == ("Rotation", "Reflection", "Shear", "Projection", "Translation")


def test_only_translation_moves_origin() -> None:
    fixed = {name: transform.fixes_origin for name, transform in CANDIDATE_TRANSFORMATIONS}
    assert fixed == {
        "Rotation": True,
        "Reflection": True,
        "Shear": True,
        "Projection": True,
        "Translation": False,
    }


def test_scene_asks_for_structure_without_introducing_matrix_notation() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "Which of these preserve the linear structure?" in source
    assert "A linear transformation must fix the origin." in source
    assert "What additional properties must it preserve?" in source
    assert "Matrix(" not in source
    assert r"T(c" not in source
    assert r"T(u" not in source


def test_scene_deforms_grid_basis_vectors_and_figure() -> None:
    source = SCENE.read_text(encoding="utf-8")
    for token in (
        "grid_lines",
        "e1_arrow",
        "e2_arrow",
        "vector_arrow",
        "figure",
        "origin_dot",
        "update_from_snapshot",
    ):
        assert token in source
