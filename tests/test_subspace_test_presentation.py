from pathlib import Path

SCENE = Path("scenes/subspace_test_presentation.py")


def test_scene_uses_renderer_independent_model() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "from engine.subspace_test import SubspaceTest" in source
    assert "class SubspaceTestPresentation(ThreeDScene)" in source


def test_scene_contrasts_origin_plane_and_shifted_plane() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'PASS_HEADING = "A plane through the origin"' in source
    assert 'FAIL_HEADING = "The same plane, shifted"' in source
    assert "good = model.through_origin" in source
    assert "bad = model.shifted" in source


def test_scene_demonstrates_both_closure_operations() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\mathbf u+\mathbf v\in W" in source
    assert r"c\mathbf u\in W" in source
    assert r"\mathbf p+\mathbf q\notin S" in source
    assert r"2\mathbf p\notin S" in source


def test_scene_ends_with_three_part_subspace_test() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"1.\quad \mathbf 0\in W" in source
    assert r"2.\quad \mathbf u,\mathbf v\in W" in source
    assert r"3.\quad \mathbf u\in W,\ c\in\mathbb R" in source
    assert "A subspace contains 0 and is closed under addition and scalar multiplication." in source
