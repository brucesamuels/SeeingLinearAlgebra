import importlib.util
import os
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_cp213_positive_definite_preview.py"
SPEC = importlib.util.spec_from_file_location("positive_definite_preview_builder", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def checkpoints():
    return [checkpoint for checkpoint, _, _ in MODULE.CHAPTER_CLIPS if checkpoint is not None]


def scene_names():
    return [scene_name for _, scene_name, _ in MODULE.CHAPTER_CLIPS]


def test_assembly_contains_cp199_through_cp212_in_order():
    assert checkpoints() == list(range(199, 213))


def test_title_precedes_lessons_and_summary_closes_chapter():
    assert MODULE.CHAPTER_CLIPS[0][1] == "PositiveDefiniteMatricesTitleCard"
    assert MODULE.CHAPTER_CLIPS[-1][1] == "PositiveDefinitenessSummaryPresentation"


def test_every_scene_name_is_unique():
    assert len(scene_names()) == len(set(scene_names()))


def test_svd_minimum_principle_and_finite_elements_keep_approved_order():
    names = scene_names()
    assert names.index("SingularValueDecompositionIntroductionPresentation") < names.index(
        "SingularValueDecompositionComputationPresentation"
    )
    assert names.index("SingularValueDecompositionComputationPresentation") < names.index(
        "MinimumPrinciplePresentation"
    )
    assert names.index("MinimumPrinciplePresentation") < names.index(
        "FiniteElementEnergyPresentation"
    )


def test_find_rendered_clip_prefers_requested_quality_and_newest(tmp_path):
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
    assert MODULE.find_rendered_clip(tmp_path, "ExamplePresentation", "480p15") == newer


def test_collect_clips_reports_incomplete_assembly(tmp_path):
    with pytest.raises(FileNotFoundError, match="Missing rendered Positive Definite Matrices clips"):
        MODULE.collect_clips(tmp_path)


def test_video_signature_uses_stream_copy_compatibility_fields():
    metadata = {
        "streams": [{
            "codec_type": "video", "codec_name": "h264", "width": 854,
            "height": 480, "pix_fmt": "yuv420p", "r_frame_rate": "15/1",
        }],
        "format": {"duration": "2.5"},
    }
    assert MODULE.video_signature(metadata) == ("h264", 854, 480, "yuv420p", "15/1")


def test_builder_uses_ffprobe_validation_and_stream_copy_concat():
    source = MODULE_PATH.read_text()
    assert "validate_compatible_clips" in source
    assert '"concat"' in source
    assert '"-c", "copy"' in source
    assert "PositiveDefiniteMatrices_preview.mp4" in source
