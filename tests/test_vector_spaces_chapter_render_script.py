from pathlib import Path

SCRIPT = Path("scripts/render_vector_spaces_chapter.zsh")


def test_render_script_renders_all_lessons_in_order() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    expected = [
        "RankCollapse3DPresentation",
        "SubspaceTestPresentation",
        "BasisDimensionPresentation",
        "ColumnSpacePresentation",
        "NullSpacePresentation",
        "RowSpacePresentation",
        "PivotColumnsPresentation",
        "RankNullityPresentation",
        "FundamentalSubspacesPresentation",
    ]
    positions = [source.index(name) for name in expected]
    assert positions == sorted(positions)


def test_render_script_uses_low_quality_by_default_and_concatenates() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    assert 'QUALITY="${1:--pql}"' in source
    assert "ffmpeg -y -f concat -safe 0" in source
    assert "VectorSpacesAndSubspacesChapter.mp4" in source


def test_render_script_checks_required_scene_files() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    assert "required_files=(" in source
    assert "Missing chapter scene" in source
