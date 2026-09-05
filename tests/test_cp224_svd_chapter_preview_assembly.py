import importlib.util
import os
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_cp224_svd_chapter_preview.py"
SPEC = importlib.util.spec_from_file_location("svd_chapter_preview_builder", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def checkpoints():
    return [checkpoint for checkpoint, *_ in MODULE.CHAPTER_CLIPS if checkpoint is not None]


def scene_classes():
    return [class_name for _, _, class_name, _ in MODULE.CHAPTER_CLIPS]


def test_assembly_contains_cp215_through_cp223_in_order():
    assert checkpoints() == list(range(215, 224))


def test_title_precedes_lessons_and_synthesis_closes_chapter():
    assert MODULE.CHAPTER_CLIPS[0][2] == "SingularValuesRankApproximationTitleCard"
    assert MODULE.CHAPTER_CLIPS[-1][2] == "SVDChapterSynthesisPresentation"


def test_cp208_and_cp209_are_not_repeated_from_previous_chapter():
    assert 208 not in checkpoints()
    assert 209 not in checkpoints()


def test_every_scene_class_and_filename_is_unique():
    filenames = [filename for _, filename, _, _ in MODULE.CHAPTER_CLIPS]
    assert len(filenames) == len(set(filenames))
    assert len(scene_classes()) == len(set(scene_classes()))


def test_all_scene_files_resolve_and_classes_match_project_source():
    resolved = MODULE.resolve_scenes(Path(__file__).parents[1])
    assert len(resolved) == 10
    assert [entry[2] for entry in resolved] == scene_classes()


def test_newest_render_prefers_requested_quality_and_newest(tmp_path):
    low = tmp_path / "videos" / "lesson" / "480p15"
    high = tmp_path / "videos" / "lesson" / "1080p60"
    low.mkdir(parents=True)
    high.mkdir(parents=True)
    old = low / "ExamplePresentation.mp4"
    newer = low / "nested" / "ExamplePresentation.mp4"
    other_quality = high / "ExamplePresentation.mp4"
    old.write_bytes(b"old")
    newer.parent.mkdir()
    newer.write_bytes(b"new")
    other_quality.write_bytes(b"high")
    os.utime(old, (100, 100))
    os.utime(newer, (200, 200))
    os.utime(other_quality, (300, 300))
    assert MODULE.newest_render(tmp_path, "ExamplePresentation", "480p15") == newer


def test_video_signature_uses_stream_copy_compatibility_fields():
    metadata = {
        "streams": [{
            "codec_type": "video", "codec_name": "h264", "width": 854,
            "height": 480, "pix_fmt": "yuv420p", "r_frame_rate": "15/1",
        }],
        "format": {"duration": "2.5"},
    }
    assert MODULE.video_signature(metadata) == ("h264", 854, 480, "yuv420p", "15/1")


def test_resolve_scenes_reports_incomplete_chapter(tmp_path):
    (tmp_path / "scenes").mkdir()
    with pytest.raises(FileNotFoundError, match="Missing Singular Values"):
        MODULE.resolve_scenes(tmp_path)


def test_builder_renders_fresh_validates_and_uses_stream_copy():
    source = MODULE_PATH.read_text()
    assert "render_scenes" in source
    assert "validate_compatible_clips" in source
    assert '"--disable_caching"' in source
    assert '"-c", "copy"' in source
    assert "SingularValuesRankApproximation_preview.mp4" in source
