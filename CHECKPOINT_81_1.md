# Checkpoint 81.1 — Chapter Assembly Without a System FFmpeg Command

## Problem
The CP81 chapter renderer successfully rendered the individual scenes, but failed during concatenation because the shell could not find a system-wide `ffmpeg` executable.

## Fix
- Keep `ffmpeg` as the fast path when it is available.
- Add a Python/PyAV fallback assembler when `ffmpeg` is not installed as a shell command.
- Read the same generated concat list.
- Decode each rendered segment and encode the complete chapter as one MP4.
- Verify that every expected segment exists before assembly.

## Output
The assembled chapter remains:

`media/videos/vector_spaces_chapter/480p15/VectorSpacesAndSubspacesChapter.mp4`

## Files added or updated
- `scripts/render_vector_spaces_chapter.zsh`
- `scripts/assemble_vector_spaces_chapter.py`
- `tests/test_vector_spaces_chapter_assembly.py`
- `CHECKPOINT_81_1.md`
