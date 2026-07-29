from pathlib import Path

RENDER_SCRIPT = Path("scripts/render_vector_spaces_chapter.zsh")
ASSEMBLER = Path("scripts/assemble_vector_spaces_chapter.py")


def test_render_script_falls_back_to_pyav_when_ffmpeg_is_missing() -> None:
    source = RENDER_SCRIPT.read_text(encoding="utf-8")
    assert "if command -v ffmpeg >/dev/null 2>&1; then" in source
    assert "System ffmpeg not found; using the Python/PyAV assembler." in source
    assert 'python scripts/assemble_vector_spaces_chapter.py "$CONCAT_FILE" "$OUTPUT_FILE"' in source


def test_python_assembler_reads_concat_file_and_encodes_video() -> None:
    source = ASSEMBLER.read_text(encoding="utf-8")
    assert "import av" in source
    assert "def read_concat_file" in source
    assert "def assemble" in source
    assert 'output.add_stream("libx264", rate=rate)' in source
    assert 'output.add_stream("mpeg4", rate=rate)' in source


def test_assembler_reports_missing_segments() -> None:
    source = ASSEMBLER.read_text(encoding="utf-8")
    assert "Rendered segment not found" in source
    assert "No rendered segments were listed for assembly" in source
