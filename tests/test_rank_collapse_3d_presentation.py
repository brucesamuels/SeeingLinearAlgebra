from pathlib import Path

SCENE = Path("scenes/rank_collapse_3d_presentation.py")


def test_scene_uses_renderer_independent_model_and_thin_adapter() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "class RankCollapse3DPresentation(ThreeDScene)" in source
    assert "from engine.rank_collapse_3d import RankCollapse3D" in source
    assert "from engine.manim_rank_collapse_3d import ManimRankCollapse3D" in source


def test_prediction_focuses_on_yellow_vector_and_the_whole_span() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'PREDICTION = "Watch the yellow vector move.' in source
    assert 'As its direction changes, the whole span changes with it.' in source


def test_transitions_use_explicit_alpha_animations_not_updater_driven_snaps() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "UpdateFromAlphaFunc(adapter.mobject, animate_space_to_plane)" in source
    assert "UpdateFromAlphaFunc(adapter.mobject, animate_plane_to_line)" in source
    assert "add_updater" not in source


def test_pre_motion_pause_is_shortened() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "self.wait(0.5)" in source
    assert "self.wait(1.0)" in source
    assert "self.wait(1.3)" in source


def test_collapses_remain_slow_and_deliberate() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "run_time=9.0" in source
    assert "run_time=9.5" in source
    assert "self.wait(0.8)" in source


def test_parallelepiped_edges_remain_thin_and_faded() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'edge_kwargs={"color": EDGE_COLOR, "thickness": 0.008}' in source
    assert "adapter.edges.set_opacity(0.22)" in source
