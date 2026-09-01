#!/usr/bin/env python3
"""Render and assemble the 1080p60 Positive Definite Matrices master at 80% speed."""
from __future__ import annotations

import argparse
import ast
import json
import shutil
import subprocess
from pathlib import Path


DEFAULT_SPEED = 0.80

MASTER_SCENES = (
    (None, "positive_definite_matrices_title_card.py", "PositiveDefiniteMatricesTitleCard", "Chapter title"),
    (199, "positive_definite_why_presentation.py", "PositiveDefiniteWhyPresentation", "Why Positive Definiteness?"),
    (200, "positive_definite_quadratic_surface_presentation.py", "PositiveDefiniteQuadraticSurfacePresentation", "From Directional Energy to a Bowl"),
    (201, "positive_definite_eigenvalue_test_presentation.py", "PositiveDefiniteEigenvalueTestPresentation", "The Eigenvalue Test"),
    (202, "positive_definite_elimination_test_presentation.py", "PositiveDefiniteEliminationTestPresentation", "The Elimination Test"),
    (203, "positive_definite_ldlt_presentation.py", "PositiveDefiniteLDLTPresentation", "The LDL-Transpose Factorization"),
    (204, "positive_definite_cholesky_presentation.py", "PositiveDefiniteCholeskyPresentation", "Cholesky: A Matrix Square Root"),
    (205, "gram_matrix_definiteness_presentation.py", "GramMatrixDefinitenessPresentation", "Why A-Transpose A Is Positive Semidefinite"),
    (206, "least_squares_uniqueness_presentation.py", "LeastSquaresUniquenessPresentation", "Why Least Squares Has a Unique Solution"),
    (207, "covariance_definiteness_presentation.py", "CovarianceDefinitenessPresentation", "Why Covariance Is Positive Semidefinite"),
    (208, "svd_introduction_presentation.py", "SingularValueDecompositionIntroductionPresentation", "Why the Singular Value Decomposition?"),
    (209, "svd_computation_presentation.py", "SingularValueDecompositionComputationPresentation", "Computing the SVD from A-Transpose A"),
    (210, "minimum_principle_presentation.py", "MinimumPrinciplePresentation", "The Minimum Principle"),
    (211, "finite_element_energy_presentation.py", "FiniteElementEnergyPresentation", "Finite Elements: Turning Energy into a Matrix"),
    (212, "positive_definiteness_summary_presentation.py", "PositiveDefinitenessSummaryPresentation", "Positive Definiteness: The Big Picture"),
)


def validate_speed(speed: float) -> float:
    if not 0.5 <= speed <= 1.0:
        raise ValueError("speed must be between 0.5 and 1.0")
    return float(speed)


def detect_scene_class(scene_file: Path) -> str:
    tree = ast.parse(scene_file.read_text(encoding="utf-8"), filename=str(scene_file))
    scene_bases = {"Scene", "ThreeDScene", "MovingCameraScene"}
    candidates = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        bases = {
            base.id if isinstance(base, ast.Name) else base.attr
            for base in node.bases
            if isinstance(base, (ast.Name, ast.Attribute))
        }
        if scene_bases.intersection(bases):
            candidates.append(node.name)
    if len(candidates) != 1:
        raise RuntimeError(
            f"Expected exactly one top-level Manim scene class in {scene_file}; found {candidates}"
        )
    return candidates[0]


def ordered_scenes(repo_root: Path) -> list[tuple[str, Path, str]]:
    scenes_dir = repo_root / "scenes"
    ordered = []
    for checkpoint, filename, expected_class, lesson in MASTER_SCENES:
        scene_file = scenes_dir / filename
        if not scene_file.is_file():
            raise FileNotFoundError(f"Missing approved scene: {scene_file}")
        detected = detect_scene_class(scene_file)
        if detected != expected_class:
            raise RuntimeError(
                f"Unexpected scene class in {scene_file}: {detected}; expected {expected_class}"
            )
        prefix = "Title" if checkpoint is None else f"CP{checkpoint}"
        ordered.append((f"{prefix} — {lesson}", scene_file, expected_class))
    return ordered


def run(command: list[str], cwd: Path) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def newest_render(media_dir: Path, class_name: str) -> Path:
    matches = [
        path for path in media_dir.rglob(f"{class_name}.mp4")
        if "partial_movie_files" not in path.parts
    ]
    if not matches:
        raise FileNotFoundError(f"Could not locate rendered MP4 for {class_name}")
    return max(matches, key=lambda path: path.stat().st_mtime)


def probe_video(ffprobe: str, path: Path) -> dict[str, object]:
    command = [
        ffprobe, "-v", "error",
        "-show_entries",
        "stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate:format=duration",
        "-of", "json", str(path),
    ]
    return json.loads(subprocess.run(command, check=True, capture_output=True, text=True).stdout)


def video_signature(metadata: dict[str, object]) -> tuple[object, ...]:
    videos = [
        stream for stream in metadata.get("streams", [])
        if stream.get("codec_type") == "video"
    ]
    if len(videos) != 1:
        raise RuntimeError(f"Expected one video stream; found {len(videos)}")
    stream = videos[0]
    return tuple(
        stream.get(key)
        for key in ("codec_name", "width", "height", "pix_fmt", "r_frame_rate")
    )


def validate_segments(ffprobe: str, segments: list[Path]) -> float:
    baseline = None
    total_duration = 0.0
    for segment in segments:
        metadata = probe_video(ffprobe, segment)
        signature = video_signature(metadata)
        if baseline is None:
            baseline = signature
        elif signature != baseline:
            raise RuntimeError(
                f"Incompatible high-definition segment {segment}: {signature}; expected {baseline}"
            )
        total_duration += float(metadata["format"]["duration"])
    expected = ("h264", 1920, 1080, "yuv420p", "60/1")
    if baseline != expected:
        raise RuntimeError(f"High-definition segments have {baseline}; expected {expected}")
    return total_duration


def write_manifest(segments: list[Path], manifest: Path) -> None:
    manifest.write_text(
        "ffconcat version 1.0\n"
        + "".join(f"file '{segment.resolve().as_posix()}'\n" for segment in segments),
        encoding="utf-8",
    )


def build_master(repo_root: Path, speed: float = DEFAULT_SPEED) -> tuple[Path, Path]:
    speed = validate_speed(speed)
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if ffmpeg is None or ffprobe is None:
        raise RuntimeError("ffmpeg and ffprobe are required")

    ordered = ordered_scenes(repo_root)
    print("\nPositive Definite Matrices final-master order:")
    for index, (label, scene_file, class_name) in enumerate(ordered, start=1):
        print(f"  {index:02d}. {label}: {scene_file.name} :: {class_name}")

    segment_media = repo_root / "media" / "cp214_positive_definite_master_segments"
    segment_media.mkdir(parents=True, exist_ok=True)
    segments = []
    for index, (label, scene_file, class_name) in enumerate(ordered, start=1):
        print(f"\nRendering {index}/{len(ordered)} at 1080p60: {label}")
        run(
            [
                "python", "-m", "manim", "--disable_caching", "-qh",
                "--media_dir", str(segment_media), str(scene_file), class_name,
            ],
            repo_root,
        )
        segments.append(newest_render(segment_media, class_name))

    source_duration = validate_segments(ffprobe, segments)
    output_dir = repo_root / "media" / "videos" / "positive_definite_matrices_assembly"
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = segment_media / "positive_definite_master_concat.txt"
    write_manifest(segments, manifest)

    fullspeed = output_dir / "PositiveDefiniteMatrices_1080p60_fullspeed.mp4"
    run(
        [
            ffmpeg, "-y", "-v", "warning", "-f", "concat", "-safe", "0",
            "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(fullspeed),
        ],
        repo_root,
    )

    slowed = output_dir / "PositiveDefiniteMatrices_1080p60_80pct.mp4"
    run(
        [
            ffmpeg, "-y", "-v", "warning", "-i", str(fullspeed),
            "-vf", f"setpts=PTS/{speed:.6f},fps=60", "-an",
            "-c:v", "libx264", "-preset", "slow", "-crf", "16",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(slowed),
        ],
        repo_root,
    )

    full_metadata = probe_video(ffprobe, fullspeed)
    slowed_metadata = probe_video(ffprobe, slowed)
    full_duration = float(full_metadata["format"]["duration"])
    slowed_duration = float(slowed_metadata["format"]["duration"])
    expected_slowed = full_duration / speed
    if abs(full_duration - source_duration) > 0.25:
        raise RuntimeError("Full-speed assembly duration does not match its source segments")
    if abs(slowed_duration - expected_slowed) > 0.25:
        raise RuntimeError("80%-speed master duration does not match the requested slowdown")
    if video_signature(slowed_metadata) != ("h264", 1920, 1080, "yuv420p", "60/1"):
        raise RuntimeError("Slowed master is not 1080p60 H.264 yuv420p")

    print(f"\nFull-speed 1080p60 assembly: {fullspeed}")
    print(f"Final 80% speed 1080p60 master: {slowed}")
    print(f"Full-speed duration: {full_duration:.3f} seconds")
    print(f"80% speed duration: {slowed_duration:.3f} seconds")
    return fullspeed, slowed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED)
    args = parser.parse_args()
    build_master(args.repo_root.resolve(), args.speed)


if __name__ == "__main__":
    main()
