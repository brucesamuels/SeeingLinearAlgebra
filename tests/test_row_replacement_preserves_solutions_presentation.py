from __future__ import annotations

from pathlib import Path


SCENE_PATH = Path("scenes/row_replacement_preserves_solutions_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_has_expected_title_and_subtitle() -> None:
    source = scene_source()
    assert "Why Does Row Replacement Preserve Solutions?" in source
    assert "loses no information" in source


def test_scene_uses_forward_row_replacement() -> None:
    source = scene_source()
    assert r"R_2\leftarrow R_2-2R_1" in source
    assert r"(2x-y)-2(x+y)=1-2(2)" in source
    assert r"-3y=-3" in source


def test_scene_states_forward_implication() -> None:
    source = scene_source()
    assert "Every original solution satisfies the replacement equation" in source
    assert "Subtracting equal quantities from equal quantities preserves equality." in source


def test_scene_verifies_the_common_solution() -> None:
    source = scene_source()
    assert r"(x,y)=(1,1)" in source
    assert r"1+1=2" in source
    assert r"-3(1)=-3" in source


def test_scene_asks_about_lost_solutions() -> None:
    source = scene_source()
    assert "But did we lose any solutions?" in source
    assert "Can the original second equation be recovered?" in source


def test_scene_shows_inverse_row_replacement() -> None:
    source = scene_source()
    assert r"R_2\leftarrow R_2+2R_1" in source
    assert r"(-3y)+2(x+y)=-3+2(2)" in source
    assert r"2x-y=1" in source


def test_scene_connects_equations_and_augmented_matrices() -> None:
    source = scene_source()
    assert "The same reversible move in the augmented matrix" in source
    assert "snapshot.original_augmented" in source
    assert "snapshot.transformed_augmented" in source


def test_scene_concludes_with_general_inverse_pair() -> None:
    source = scene_source()
    assert r"R_i\leftarrow R_i+cR_j" in source
    assert r"R_i\leftarrow R_i-cR_j" in source
    assert "exactly the same solutions" in source
