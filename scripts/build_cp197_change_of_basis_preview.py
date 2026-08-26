#!/usr/bin/env python3
"""Assemble the rendered Change of Basis lessons into one preview video."""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


CHAPTER_CLIPS = (
    ("ChangeOfBasisTitleCard", "Chapter title"),
    ("WhyChangeBasisPresentation", "Why Change Basis"),
    ("CoordinatesRelativeToBasisPresentation", "Coordinates Relative to a Basis"),
    ("CoordinateLinearCombinationsPresentation", "Coordinates as Linear-Combination Recipes"),
    ("BasisMatrixPresentation", "The Basis Matrix"),
    ("StandardToBasisCoordinatesPresentation", "Standard to Basis Coordinates"),
    ("TwoBasisCoordinatesPresentation", "Changing Between Two Nonstandard Bases"),
    ("TransformationMatrixBasisPresentation", "Matrix of a Transformation in Another Basis"),
    ("TransformationBetweenBasesPresentation", "Changing a Transformation Between Two Bases"),
    ("GoodBasisPresentation", "Why a Good Basis Matters"),
    ("ChangeOfBasisReviewPresentation", "One Object, Many Descriptions"),
)


def find_rendered_clip(media_root: Path, scene_name: str, quality: str = "480p15") -> Path:
    """Return the newest exact scene render, preferring the requested quality."""
    candidates = [path for path in media_root.rglob(f"{scene_name}.mp4") if "partial_movie_files" not in path.parts]
    if not candidates:
        raise FileNotFoundError(f"No rendered clip found for {scene_name}")
    preferred = [path for path in candidates if quality in path.parts]
    pool = preferred or candidates
    return max(pool, key=lambda path: path.stat().st_mtime)


def collect_clips(media_root: Path, quality: str = "480p15") -> list[Path]:
    missing = []
    clips = []
    for scene_name, lesson_name in CHAPTER_CLIPS:
        try:
            clips.append(find_rendered_clip(media_root, scene_name, quality))
        except FileNotFoundError:
            missing.append(f"  - {lesson_name}: {scene_name}.mp4")
    if missing:
        details = "\n".join(missing)
        raise FileNotFoundError(f"Missing rendered chapter clips:\n{details}")
    return clips


def _ffmpeg_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "'\\''")


def write_concat_manifest(clips: list[Path], manifest: Path) -> None:
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("".join(f"file '{_ffmpeg_path(clip)}'\n" for clip in clips))


def assemble(media_root: Path, output: Path, quality: str = "480p15") -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required to assemble the preview chapter")
    clips = collect_clips(media_root, quality)
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = output.with_suffix(".concat.txt")
    write_concat_manifest(clips, manifest)
    command = [
        ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(manifest),
        "-c", "copy", "-movflags", "+faststart", str(output),
    ]
    subprocess.run(command, check=True)
    print("Assembled lessons in this order:")
    for index, ((_, lesson_name), clip) in enumerate(zip(CHAPTER_CLIPS, clips), start=1):
        print(f"{index:2d}. {lesson_name}: {clip}")
    print(f"Preview chapter: {output.resolve()}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--media-root", type=Path, default=Path("media"))
    parser.add_argument("--quality", default="480p15")
    parser.add_argument("--output", type=Path, default=Path("media/change_of_basis_preview.mp4"))
    args = parser.parse_args()
    assemble(args.media_root, args.output, args.quality)


if __name__ == "__main__":
    main()

