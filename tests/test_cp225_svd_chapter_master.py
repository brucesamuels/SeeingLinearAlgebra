import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
MODULE_PATH = SCRIPTS / "build_cp225_svd_chapter_master.py"
SPEC = importlib.util.spec_from_file_location("svd_chapter_master_builder", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_master_reuses_approved_cp224_order():
    checkpoints = [checkpoint for checkpoint, *_ in MODULE.CHAPTER_CLIPS if checkpoint is not None]
    assert checkpoints == list(range(215, 224))
    assert MODULE.CHAPTER_CLIPS[0][2] == "SingularValuesRankApproximationTitleCard"
    assert MODULE.CHAPTER_CLIPS[-1][2] == "SVDChapterSynthesisPresentation"


def test_master_requires_exact_1080p60_signature():
    assert MODULE.EXPECTED_SIGNATURE == ("h264", 1920, 1080, "yuv420p", "60/1")


def test_builder_renders_current_sources_at_high_quality():
    source = MODULE_PATH.read_text()
    assert 'render_scenes(repo_root, media_root, "h")' in source
    assert "validate_compatible_clips" in source
    assert "High-definition segment" in source


def test_builder_stream_copies_without_global_retiming():
    source = MODULE_PATH.read_text()
    assert '"-c", "copy"' in source
    assert "setpts" not in source
    assert "DEFAULT_SPEED" not in source
    assert "SingularValuesRankApproximation_1080p60.mp4" in source


def test_builder_verifies_output_duration_and_signature():
    source = MODULE_PATH.read_text()
    assert "abs(duration - source_duration) > 0.75" in source
    assert "Final master has" in source
    assert "Final 1080p60 master" in source
