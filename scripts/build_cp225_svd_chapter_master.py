#!/usr/bin/env python3
"""Render and assemble the final 1080p60 SVD chapter master."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from build_cp224_svd_chapter_preview import (
    CHAPTER_CLIPS,
    probe_clip,
    render_scenes,
    validate_compatible_clips,
    video_signature,
    write_concat_manifest,
)


EXPECTED_SIGNATURE = ("h264", 1920, 1080, "yuv420p", "60/1")


def run(command: list[str], cwd: Path) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def build_master(repo_root: Path, media_root: Path, output: Path) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if ffmpeg is None or ffprobe is None:
        raise RuntimeError("ffmpeg and ffprobe are required to build the master")

    print("\nRendering final Singular Values, Rank, and Approximation master")
    rendered = render_scenes(repo_root, media_root, "h")
    clips = [entry[3] for entry in rendered]
    source_duration = validate_compatible_clips(ffprobe, clips)
    for clip in clips:
        signature = video_signature(probe_clip(ffprobe, clip))
        if signature != EXPECTED_SIGNATURE:
            raise RuntimeError(
                f"High-definition segment {clip} has {signature}; "
                f"expected {EXPECTED_SIGNATURE}"
            )

    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = media_root / "svd_chapter_master.concat.txt"
    write_concat_manifest(clips, manifest)
    run(
        [
            ffmpeg, "-y", "-v", "warning", "-f", "concat", "-safe", "0",
            "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(output),
        ],
        repo_root,
    )

    metadata = probe_clip(ffprobe, output)
    signature = video_signature(metadata)
    duration = float(metadata["format"]["duration"])
    if signature != EXPECTED_SIGNATURE:
        raise RuntimeError(f"Final master has {signature}; expected {EXPECTED_SIGNATURE}")
    if abs(duration - source_duration) > 0.75:
        raise RuntimeError(
            f"Final duration {duration:.3f} differs from source total {source_duration:.3f}"
        )

    print("\nFinal 1080p60 chapter order:")
    for index, ((checkpoint, _, _, lesson_name), clip) in enumerate(
        zip(CHAPTER_CLIPS, clips), start=1
    ):
        prefix = "Title" if checkpoint is None else f"CP{checkpoint}"
        print(f"{index:2d}. {prefix} — {lesson_name}: {clip}")
    print(f"Source duration: {source_duration:.3f} seconds")
    print(f"Final duration: {duration:.3f} seconds")
    print(f"Final 1080p60 master: {output.resolve()}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--media-root",
        type=Path,
        default=Path("media/cp225_svd_chapter_master_segments"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "media/videos/singular_values_rank_approximation_assembly/"
            "SingularValuesRankApproximation_1080p60.mp4"
        ),
    )
    args = parser.parse_args()
    build_master(
        args.repo_root.resolve(),
        args.media_root.resolve(),
        args.output.resolve(),
    )


if __name__ == "__main__":
    main()
