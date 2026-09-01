#!/usr/bin/env python3
"""Assemble the approved Positive Definite Matrices lessons into one preview."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


CHAPTER_CLIPS = (
    (None, "PositiveDefiniteMatricesTitleCard", "Chapter title"),
    (199, "PositiveDefiniteWhyPresentation", "Why Positive Definiteness?"),
    (200, "PositiveDefiniteQuadraticSurfacePresentation", "From Directional Energy to a Bowl"),
    (201, "PositiveDefiniteEigenvalueTestPresentation", "The Eigenvalue Test"),
    (202, "PositiveDefiniteEliminationTestPresentation", "The Elimination Test"),
    (203, "PositiveDefiniteLDLTPresentation", "The LDL-Transpose Factorization"),
    (204, "PositiveDefiniteCholeskyPresentation", "Cholesky: A Matrix Square Root"),
    (205, "GramMatrixDefinitenessPresentation", "Why A-Transpose A Is Positive Semidefinite"),
    (206, "LeastSquaresUniquenessPresentation", "Why Least Squares Has a Unique Solution"),
    (207, "CovarianceDefinitenessPresentation", "Why Covariance Is Positive Semidefinite"),
    (208, "SingularValueDecompositionIntroductionPresentation", "Why the Singular Value Decomposition?"),
    (209, "SingularValueDecompositionComputationPresentation", "Computing the SVD from A-Transpose A"),
    (210, "MinimumPrinciplePresentation", "The Minimum Principle"),
    (211, "FiniteElementEnergyPresentation", "Finite Elements: Turning Energy into a Matrix"),
    (212, "PositiveDefinitenessSummaryPresentation", "Positive Definiteness: The Big Picture"),
)


def find_rendered_clip(media_root: Path, scene_name: str, quality: str = "480p15") -> Path:
    candidates = [
        path
        for path in media_root.rglob(f"{scene_name}.mp4")
        if "partial_movie_files" not in path.parts
    ]
    if not candidates:
        raise FileNotFoundError(f"No rendered clip found for {scene_name}")
    preferred = [path for path in candidates if quality in path.parts]
    pool = preferred or candidates
    return max(pool, key=lambda path: path.stat().st_mtime)


def collect_clips(media_root: Path, quality: str = "480p15") -> list[Path]:
    missing = []
    clips = []
    for checkpoint, scene_name, lesson_name in CHAPTER_CLIPS:
        try:
            clips.append(find_rendered_clip(media_root, scene_name, quality))
        except FileNotFoundError:
            prefix = "Title" if checkpoint is None else f"CP{checkpoint}"
            missing.append(f"  - {prefix} — {lesson_name}: {scene_name}.mp4")
    if missing:
        raise FileNotFoundError(
            "Missing rendered Positive Definite Matrices clips:\n" + "\n".join(missing)
        )
    return clips


def probe_clip(ffprobe: str, path: Path) -> dict[str, object]:
    command = [
        ffprobe,
        "-v", "error",
        "-show_entries",
        "stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate:format=duration",
        "-of", "json",
        str(path),
    ]
    return json.loads(subprocess.run(command, check=True, capture_output=True, text=True).stdout)


def video_signature(metadata: dict[str, object]) -> tuple[object, ...]:
    streams = [
        stream for stream in metadata.get("streams", [])
        if stream.get("codec_type") == "video"
    ]
    if len(streams) != 1:
        raise RuntimeError(f"Expected one video stream; found {len(streams)}")
    stream = streams[0]
    return tuple(
        stream.get(key)
        for key in ("codec_name", "width", "height", "pix_fmt", "r_frame_rate")
    )


def validate_compatible_clips(ffprobe: str, clips: list[Path]) -> float:
    baseline = None
    total_duration = 0.0
    for clip in clips:
        metadata = probe_clip(ffprobe, clip)
        signature = video_signature(metadata)
        if baseline is None:
            baseline = signature
        elif signature != baseline:
            raise RuntimeError(
                f"Incompatible preview clip {clip}: {signature}; expected {baseline}"
            )
        total_duration += float(metadata["format"]["duration"])
    return total_duration


def _ffmpeg_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "'\\''")


def write_concat_manifest(clips: list[Path], manifest: Path) -> None:
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "ffconcat version 1.0\n"
        + "".join(f"file '{_ffmpeg_path(clip)}'\n" for clip in clips),
        encoding="utf-8",
    )


def assemble(media_root: Path, output: Path, quality: str = "480p15") -> Path:
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if ffmpeg is None or ffprobe is None:
        raise RuntimeError("ffmpeg and ffprobe are required to assemble the preview")
    clips = collect_clips(media_root, quality)
    total_duration = validate_compatible_clips(ffprobe, clips)
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = output.with_suffix(".concat.txt")
    write_concat_manifest(clips, manifest)
    subprocess.run(
        [
            ffmpeg, "-y", "-v", "warning", "-f", "concat", "-safe", "0",
            "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(output),
        ],
        check=True,
    )
    print("Positive Definite Matrices preview order:")
    for index, ((checkpoint, _, lesson_name), clip) in enumerate(
        zip(CHAPTER_CLIPS, clips), start=1
    ):
        prefix = "Title" if checkpoint is None else f"CP{checkpoint}"
        print(f"{index:2d}. {prefix} — {lesson_name}: {clip}")
    print(f"Expected duration from source clips: {total_duration:.3f} seconds")
    print(f"Preview chapter: {output.resolve()}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--media-root", type=Path, default=Path("media"))
    parser.add_argument("--quality", default="480p15")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "media/videos/positive_definite_matrices_assembly/"
            "PositiveDefiniteMatrices_preview.mp4"
        ),
    )
    args = parser.parse_args()
    assemble(args.media_root, args.output, args.quality)


if __name__ == "__main__":
    main()
