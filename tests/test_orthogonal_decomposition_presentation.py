from pathlib import Path

SCENE_PATH = Path("scenes/orthogonal_decomposition_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_uses_chapter_header_and_scene_class() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Orthogonal Decomposition"' in source
    assert "class OrthogonalDecompositionPresentation(Scene)" in source
    assert 'SCENE_REVISION = "cp154_r2_labeled_geometry"' in source


def test_scene_has_six_cards() -> None:
    source = scene_source()
    for helper in (
        "_projection_becomes_split_card",
        "_where_parts_live_card",
        "_uniqueness_card",
        "_worked_example_card",
        "_pythagorean_card",
        "_bridge_to_subspaces_card",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_geometry_visually_builds_parallel_and_perpendicular_parts() -> None:
    source = scene_source()
    assert "_residual_arrow" in source
    assert "_right_angle_marker" in source
    assert "self.snapshot.parallel" in source
    assert "snapshot.perpendicular" in source
    assert r"\mathbf{x}=\mathbf{p}+\mathbf{r}" in source


def test_scene_places_parts_in_W_and_orthogonal_complement() -> None:
    source = scene_source()
    assert r"\mathbf{p}\in W" in source
    assert r"\mathbf{r}=\mathbf{x}-\mathbf{p}\in W^\perp" in source
    assert r"\mathbf{p}\cdot\mathbf{r}=0" in source


def test_scene_includes_short_uniqueness_argument() -> None:
    source = scene_source()
    assert r"W\cap W^\perp=\{\mathbf{0}\}" in source
    assert r"\mathbf{p}=\mathbf{p}',\qquad \mathbf{r}=\mathbf{r}'" in source


def test_worked_example_uses_clean_hand_friendly_data() -> None:
    source = scene_source()
    assert r"\mathbf{x}=(4,2),\quad W=\operatorname{span}(1,1)" in source
    assert r"\mathbf{p}=(3,3)" in source
    assert r"\mathbf{r}=\mathbf{x}-\mathbf{p}=(1,-1)" in source
    assert r"(3,3)\cdot(1,-1)=0" in source


def test_scene_makes_pythagorean_payoff_explicit() -> None:
    source = scene_source()
    assert "self.lesson.PYTHAGOREAN" in source
    assert r"20=18+2" in source


def test_final_card_bridges_to_projection_onto_a_subspace() -> None:
    source = scene_source()
    assert "How do we find p when W has several basis vectors?" in source
    assert "projection onto a subspace" in source


def test_scene_keeps_approved_deliberate_pacing() -> None:
    source = scene_source()
    assert "TRANSITION_TIME = 1.35" in source
    assert "EMPHASIS_TIME = 1.15" in source
    assert "HOLD_TIME = 2.6" in source
    assert "LONG_HOLD_TIME = 3.0" in source


def test_scene_imports_all_direction_constants_it_uses() -> None:
    source = scene_source()
    import_block = source.split("from manim import (", 1)[1].split(")", 1)[0]
    for name in ("LEFT,", "RIGHT,", "UP,", "DOWN,"):
        assert name in import_block


def test_diagrams_label_vectors_and_subspace_directly() -> None:
    source = scene_source()
    assert source.count("w_diagram_label") >= 3
    assert "x_diagram_label" in source
    assert source.count("p_diagram_label") >= 2
    assert source.count("r_diagram_label") >= 2
    assert r'W=\operatorname{span}(1,1)' in source


def test_worked_example_fades_in_W_label_with_geometry() -> None:
    source = scene_source()
    worked = source.split("def _worked_example_card", 1)[1].split("def _pythagorean_card", 1)[0]
    assert "FadeIn(w_diagram_label)" in worked
    assert "FadeIn(x_diagram_label)" in worked
    assert "FadeIn(p_diagram_label)" in worked
    assert "FadeIn(r_diagram_label)" in worked
