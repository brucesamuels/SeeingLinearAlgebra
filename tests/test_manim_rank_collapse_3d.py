from pathlib import Path

SOURCE = Path("engine/manim_rank_collapse_3d.py")


def test_adapter_uses_flat_geometry_to_prevent_axial_spinning() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    assert "from manim import Arrow, Dot3D, Line, VGroup" in source
    assert "Arrow3D" not in source.split("from manim import", 1)[1].split("\n", 1)[0]
    assert "Line3D" not in source.split("from manim import", 1)[1].split("\n", 1)[0]
    assert "Arrow(origin, self._point(vector), **style)" in source
    assert "Line(" in source


def test_adapter_preserves_in_place_motion() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    assert "arrow.put_start_and_end_on" in source
    assert "dot.move_to" in source
    assert "edge.put_start_and_end_on" in source


def test_adapter_translates_3d_style_parameters_for_flat_objects() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    assert "def _flat_arrow_style" in source
    assert "def _flat_edge_style" in source
    assert '"stroke_width"' in source
