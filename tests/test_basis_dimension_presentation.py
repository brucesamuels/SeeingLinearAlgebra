from pathlib import Path

SCENE = Path("scenes/basis_dimension_presentation.py")


def test_scene_uses_basis_dimension_model() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "from engine.basis_dimension import BasisDimension" in source
    assert "class BasisDimensionPresentation(ThreeDScene)" in source


def test_scene_uses_redundant_third_vector_relation() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\mathbf v_3={relation[0]:.0f}\mathbf v_1+{relation[1]:.0f}\mathbf v_2" in source
    assert "V3 = V1 + V2" in source


def test_scene_asks_if_all_three_vectors_are_needed() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "If three vectors generate this plane, do we really need all three?" in source


def test_scene_reveals_same_span_after_fading_redundant_vector() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "arrows[2].animate.set_opacity(0.18)" in source
    assert "FadeOut(arrows[2])" in source
    assert r"\operatorname{span}\{\mathbf v_1,\mathbf v_2,\mathbf v_3\}=" in source
    assert r"\operatorname{span}\{\mathbf v_1,\mathbf v_2\}" in source


def test_scene_concludes_with_basis_and_dimension() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\{\mathbf v_1,\mathbf v_2\}\text{ is a basis}" in source
    assert r"\dim(W)=2" in source
    assert "A basis spans the space, with no redundant vectors." in source
    assert "The dimension is the number of vectors in a basis." in source


def test_scene_uses_plane_patch_and_sample_points() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "plane = Polygon(" in source
    assert "Dot3D(axes.c2p(*point), radius=0.032" in source
    assert "snapshot.endpoints_basis" in source


def test_scene_imports_all_direction_constants_it_uses() -> None:
    source = SCENE.read_text(encoding="utf-8")
    import_block = source.split("from manim import (", 1)[1].split(")", 1)[0]
    assert "DOWN," in import_block
    assert ".to_edge(DOWN" in source


def test_basis_caption_is_separated_from_key_idea() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert ").to_edge(DOWN, buff=1.02)" in source
    assert "key_idea = Text(KEY_IDEA, font_size=25, color=MUTED).to_edge(DOWN, buff=0.24)" in source
