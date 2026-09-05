#!/usr/bin/env python3
"""Render and assemble the Singular Values, Rank, and Approximation preview."""

from __future__ import annotations

import argparse
import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path


CHAPTER_CLIPS = (
    (None, "singular_values_rank_approximation_title_card.py", "SingularValuesRankApproximationTitleCard", "Chapter title"),
    (215, "svd_zero_singular_value_presentation.py", "ZeroSingularValuePresentation", "What Does a Zero Singular Value Mean?"),
    (216, "svd_fundamental_subspaces_presentation.py", "SVDFundamentalSubspacesPresentation", "Full SVD and the Four Fundamental Subspaces"),
    (217, "svd_pseudoinverse_presentation.py", "SVDPseudoinversePresentation", "The Pseudoinverse: Undo What Can Be Undone"),
    (218, "pseudoinverse_least_squares_presentation.py", "PseudoinverseLeastSquaresPresentation", "Least Squares and Minimum-Norm Solutions"),
    (219, "svd_conditioning_presentation.py", "SVDConditioningPresentation", "Small Singular Values and Conditioning"),
    (220, "truncated_svd_approximation_presentation.py", "TruncatedSVDApproximationPresentation", "Truncated SVD and the Best Low-Rank Approximation"),
    (221, "svd_image_compression_presentation.py", "SVDImageCompressionPresentation", "Image Compression with the SVD"),
    (222, "pca_svd_presentation.py", "PCASVDPresentation", "Principal Component Analysis through the SVD"),
    (223, "svd_chapter_synthesis_presentation.py", "SVDChapterSynthesisPresentation", "Singular Values, Rank, and Approximation: The Big Picture"),
)


def detect_scene_class(scene_file: Path) -> str:
    tree = ast.parse(scene_file.read_text(encoding="utf-8"), filename=str(scene_file))
    scene_bases = {"Scene", "ThreeDScene", "MovingCameraScene"}
    candidates: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        bases = {
            base.id if isinstance(base, ast.Name) else base.attr
            for base in node.bases
            if isinstance(base, (ast.Name, ast.Attribute))
        }
        if bases.intersection(scene_bases):
            candidates.append(node.name)
    if len(candidates) != 1:
        raise RuntimeError(
            f"Expected one top-level Manim scene class in {scene_file}; found {candidates}"
        )
    return candidates[0]


def resolve_scenes(repo_root: Path) -> list[tuple[int | None, Path, str, str]]:
    scenes_dir = repo_root / "scenes"
    resolved = []
    missing = []
    for checkpoint, filename, class_name, lesson_name in CHAPTER_CLIPS:
        path = scenes_dir / filename
        if not path.exists():
            prefix = "Title" if checkpoint is None else f"CP{checkpoint}"
            missing.append(f"  - {prefix} — {lesson_name}: {filename}")
            continue
        detected = detect_scene_class(path)
        if detected != class_name:
            raise RuntimeError(
                f"Unexpected scene class in {filename}: found {detected}; expected {class_name}"
            )
        resolved.append((checkpoint, path, class_name, lesson_name))
    if missing:
        raise FileNotFoundError(
            "Missing Singular Values, Rank, and Approximation scenes:\n" + "\n".join(missing)
        )
    return resolved


def run(command: list[str], cwd: Path) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def newest_render(media_root: Path, class_name: str, quality: str = "480p15") -> Path:
    candidates = [
        path
        for path in media_root.rglob(f"{class_name}.mp4")
        if "partial_movie_files" not in path.parts
    ]
    if not candidates:
        raise FileNotFoundError(f"No rendered clip found for {class_name}")
    preferred = [path for path in candidates if quality in path.parts]
    return max(preferred or candidates, key=lambda path: path.stat().st_mtime)


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


def render_scenes(
    repo_root: Path,
    media_root: Path,
    quality: str,
) -> list[tuple[int | None, str, str, Path]]:
    rendered = []
    for index, (checkpoint, scene_file, class_name, lesson_name) in enumerate(
        resolve_scenes(repo_root), start=1
    ):
        prefix = "Title" if checkpoint is None else f"CP{checkpoint}"
        print(f"\nRendering {index}/{len(CHAPTER_CLIPS)}: {prefix} — {lesson_name}")
        run(
            [
                sys.executable,
                "-m", "manim",
                "--disable_caching",
                f"-q{quality}",
                "--media_dir", str(media_root),
                str(scene_file),
                class_name,
            ],
            cwd=repo_root,
        )
        rendered.append(
            (checkpoint, class_name, lesson_name, newest_render(media_root, class_name))
        )
    return rendered


def assemble(
    repo_root: Path,
    media_root: Path,
    output: Path,
    quality: str = "l",
) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if ffmpeg is None or ffprobe is None:
        raise RuntimeError("ffmpeg and ffprobe are required to assemble the preview")

    rendered = render_scenes(repo_root, media_root, quality)
    clips = [entry[3] for entry in rendered]
    expected_duration = validate_compatible_clips(ffprobe, clips)
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = media_root / "svd_chapter_preview.concat.txt"
    write_concat_manifest(clips, manifest)
    run(
        [
            ffmpeg, "-y", "-v", "warning", "-f", "concat", "-safe", "0",
            "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(output),
        ],
        cwd=repo_root,
    )

    assembled_duration = float(probe_clip(ffprobe, output)["format"]["duration"])
    if abs(assembled_duration - expected_duration) > 0.75:
        raise RuntimeError(
            f"Assembled duration {assembled_duration:.3f} differs from source total "
            f"{expected_duration:.3f}"
        )

    print("\nSingular Values, Rank, and Approximation preview order:")
    for index, (checkpoint, _, lesson_name, clip) in enumerate(rendered, start=1):
        prefix = "Title" if checkpoint is None else f"CP{checkpoint}"
        print(f"{index:2d}. {prefix} — {lesson_name}: {clip}")
    print(f"Expected duration from source clips: {expected_duration:.3f} seconds")
    print(f"Assembled duration: {assembled_duration:.3f} seconds")
    print(f"Preview chapter: {output.resolve()}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quality", choices=("l", "m", "h", "p", "k"), default="l")
    parser.add_argument(
        "--media-root",
        type=Path,
        default=Path("media/cp224_svd_chapter_preview_segments"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "media/videos/singular_values_rank_approximation_assembly/"
            "SingularValuesRankApproximation_preview.mp4"
        ),
    )
    args = parser.parse_args()
    assemble(Path.cwd().resolve(), args.media_root.resolve(), args.output.resolve(), args.quality)


if __name__ == "__main__":
    main()
