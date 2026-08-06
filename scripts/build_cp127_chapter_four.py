#!/usr/bin/env python3
"""Assemble Chapter 4 from the approved Manim lesson renders."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_QUALITY = "1080p60"
OUTPUT_FILENAME = "ChapterFourSolvingLinearSystems.mp4"
MANIM_QUALITY_FLAGS = {
    "480p15": "-ql",
    "720p30": "-qm",
    "1080p60": "-qh",
    "2160p60": "-qk",
}


@dataclass(frozen=True)
class ChapterClip:
    """One approved lesson render in chapter order."""

    lesson: str
    scene_stem: str
    scene_class: str
    render_script: str

    def relative_video_path(self, quality: str) -> Path:
        return Path("media/videos") / self.scene_stem / quality / f"{self.scene_class}.mp4"

    def relative_scene_path(self) -> Path:
        return Path("scenes") / f"{self.scene_stem}.py"


CHAPTER_CLIPS: tuple[ChapterClip, ...] = (
    ChapterClip(
        "Chapter 4 title",
        "chapter_four_title_card",
        "ChapterFourTitleCard",
        "scripts/build_cp127_chapter_four.zsh",
    ),
    ChapterClip(
        "What it means to solve A x = b",
        "linear_system_meaning_presentation",
        "LinearSystemMeaningPresentation",
        "scripts/render_cp105_linear_system_meaning.zsh",
    ),
    ChapterClip(
        "Equations to an augmented matrix",
        "augmented_matrix_encoding_presentation",
        "AugmentedMatrixEncodingPresentation",
        "scripts/render_cp106_augmented_matrix_encoding.zsh",
    ),
    ChapterClip(
        "Elementary row operations",
        "elementary_row_operations_presentation",
        "ElementaryRowOperationsPresentation",
        "scripts/render_cp107_elementary_row_operations.zsh",
    ),
    ChapterClip(
        "Why row replacement preserves solutions",
        "row_replacement_preserves_solutions_presentation",
        "RowReplacementPreservesSolutionsPresentation",
        "scripts/render_cp108_row_replacement_preserves_solutions.zsh",
    ),
    ChapterClip(
        "Gaussian elimination to echelon form",
        "gaussian_elimination_to_echelon_presentation",
        "GaussianEliminationToEchelonPresentation",
        "scripts/render_cp109_gaussian_elimination_to_echelon.zsh",
    ),
    ChapterClip(
        "Back substitution",
        "back_substitution_presentation",
        "BackSubstitutionPresentation",
        "scripts/render_cp110_back_substitution.zsh",
    ),
    ChapterClip(
        "The elimination algorithm",
        "elimination_algorithm_presentation",
        "EliminationAlgorithmPresentation",
        "scripts/render_cp111_elimination_algorithm.zsh",
    ),
    ChapterClip(
        "Gauss-Jordan elimination and RREF",
        "gauss_jordan_rref_presentation",
        "GaussJordanRREFPresentation",
        "scripts/render_cp112_gauss_jordan_rref.zsh",
    ),
    ChapterClip(
        "Reading solution sets from RREF",
        "rref_solution_sets_presentation",
        "RREFSolutionSetsPresentation",
        "scripts/render_cp113_rref_solution_sets.zsh",
    ),
    ChapterClip(
        "Pivot and free variables",
        "pivot_and_free_variables_presentation",
        "PivotAndFreeVariablesPresentation",
        "scripts/render_cp114_pivot_and_free_variables.zsh",
    ),
    ChapterClip(
        "Homogeneous systems and the null space",
        "homogeneous_null_space_presentation",
        "HomogeneousNullSpacePresentation",
        "scripts/render_cp115_homogeneous_null_space.zsh",
    ),
    ChapterClip(
        "A basis for the null space",
        "null_space_basis_presentation",
        "NullSpaceBasisPresentation",
        "scripts/render_cp116_null_space_basis.zsh",
    ),
    ChapterClip(
        "The complete solution",
        "complete_solution_presentation",
        "CompleteSolutionPresentation",
        "scripts/render_cp117_complete_solution.zsh",
    ),
    ChapterClip(
        "Rank, pivots, and consistency",
        "rank_pivots_consistency_presentation",
        "RankPivotsConsistencyPresentation",
        "scripts/render_cp118_rank_pivots_consistency.zsh",
    ),
    ChapterClip(
        "Rectangular matrices and the geometry of A x = b",
        "rectangular_matrices_presentation",
        "RectangularMatricesPresentation",
        "scripts/render_cp125_rectangular_matrices.zsh",
    ),
    ChapterClip(
        "Solvability of overdetermined and underdetermined systems",
        "rectangular_system_solvability_presentation",
        "RectangularSystemSolvabilityPresentation",
        "scripts/render_cp126_rectangular_system_solvability.zsh",
    ),
    ChapterClip(
        "Elementary matrices",
        "elementary_matrices_presentation",
        "ElementaryMatricesPresentation",
        "scripts/render_cp119_elementary_matrices.zsh",
    ),
    ChapterClip(
        "Elimination as matrix multiplication",
        "elimination_matrix_multiplication_presentation",
        "EliminationMatrixMultiplicationPresentation",
        "scripts/render_cp120_elimination_matrix_multiplication.zsh",
    ),
    ChapterClip(
        "Multiple right-hand sides",
        "multiple_right_hand_sides_presentation",
        "MultipleRightHandSidesPresentation",
        "scripts/render_cp121_multiple_right_hand_sides.zsh",
    ),
    ChapterClip(
        "Inverse by Gauss-Jordan elimination",
        "gauss_jordan_inverse_presentation",
        "GaussJordanInversePresentation",
        "scripts/render_cp122_gauss_jordan_inverse.zsh",
    ),
    ChapterClip(
        "Why some matrices are not invertible",
        "noninvertible_matrix_presentation",
        "NoninvertibleMatrixPresentation",
        "scripts/render_cp123_noninvertible_matrix.zsh",
    ),
    ChapterClip(
        "Pivoting and PA = LU",
        "pivoting_pa_lu_presentation",
        "PivotingPALUPresentation",
        "scripts/render_cp124_pivoting_pa_lu.zsh",
    ),
)


class AssemblyError(RuntimeError):
    """Raised when approved chapter clips cannot be assembled safely."""


def command_path(name: str) -> str:
    resolved = shutil.which(name)
    if resolved is None:
        raise AssemblyError(f"Required command is not installed or not on PATH: {name}")
    return resolved


def manim_quality_flag(quality: str) -> str:
    try:
        return MANIM_QUALITY_FLAGS[quality]
    except KeyError as error:
        supported = ", ".join(MANIM_QUALITY_FLAGS)
        raise AssemblyError(
            f"Unsupported Manim quality directory: {quality}. Supported values: {supported}"
        ) from error


def inspect_clip_paths(
    repo_root: Path,
    quality: str,
) -> tuple[list[Path], list[tuple[ChapterClip, Path]]]:
    paths: list[Path] = []
    missing: list[tuple[ChapterClip, Path]] = []
    for clip in CHAPTER_CLIPS:
        path = repo_root / clip.relative_video_path(quality)
        if path.is_file():
            paths.append(path)
        else:
            missing.append((clip, path))
    return paths, missing


def manual_render_command(clip: ChapterClip, quality: str) -> str:
    flag = manim_quality_flag(quality)
    return (
        f"python -m manim --disable_caching {flag} "
        f"{clip.relative_scene_path()} {clip.scene_class}"
    )


def collect_clip_paths(repo_root: Path, quality: str) -> list[Path]:
    paths, missing = inspect_clip_paths(repo_root, quality)
    if missing:
        lines = [
            "The chapter cannot be assembled because these approved renders are missing:",
        ]
        for clip, path in missing:
            lines.append(f"  - {clip.lesson}")
            lines.append(f"    expected: {path}")
            lines.append(f"    render:   {manual_render_command(clip, quality)}")
        lines.append(
            "Run ./scripts/build_cp127_chapter_four.zsh to render missing clips automatically."
        )
        raise AssemblyError("\n".join(lines))
    return paths


def render_clip(repo_root: Path, quality: str, clip: ChapterClip) -> Path:
    scene_path = repo_root / clip.relative_scene_path()
    if not scene_path.is_file():
        raise AssemblyError(f"Scene source is missing for {clip.lesson}: {scene_path}")

    output_path = repo_root / clip.relative_video_path(quality)
    environment = os.environ.copy()
    existing_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        f"{repo_root}{os.pathsep}{existing_pythonpath}"
        if existing_pythonpath
        else str(repo_root)
    )
    command = [
        sys.executable,
        "-m",
        "manim",
        "--disable_caching",
        manim_quality_flag(quality),
        str(clip.relative_scene_path()),
        clip.scene_class,
    ]
    try:
        subprocess.run(command, cwd=repo_root, env=environment, check=True)
    except subprocess.CalledProcessError as error:
        raise AssemblyError(
            f"Manim could not render {clip.lesson}.\n"
            f"Command: {' '.join(command)}"
        ) from error

    if not output_path.is_file():
        raise AssemblyError(
            f"Manim completed, but the expected render was not created for {clip.lesson}: "
            f"{output_path}"
        )
    return output_path


def render_missing_clips(repo_root: Path, quality: str) -> list[Path]:
    _, missing = inspect_clip_paths(repo_root, quality)
    if not missing:
        print(f"All {len(CHAPTER_CLIPS)} chapter clips already exist at {quality}.")
        return []

    print(f"Rendering {len(missing)} missing chapter clip(s) at {quality}...")
    rendered: list[Path] = []
    for index, (clip, _) in enumerate(missing, start=1):
        print(f"[{index}/{len(missing)}] {clip.lesson}")
        rendered.append(render_clip(repo_root, quality, clip))
    return rendered


def probe_video(ffprobe: str, path: Path) -> dict[str, object]:
    command = [
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate:format=duration",
        "-of",
        "json",
        str(path),
    ]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    payload = json.loads(completed.stdout)
    streams = payload.get("streams", [])
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    if len(video_streams) != 1:
        raise AssemblyError(f"Expected exactly one video stream in {path}; found {len(video_streams)}")
    stream = video_streams[0]
    duration = float(payload.get("format", {}).get("duration", 0.0))
    return {
        "codec_name": stream.get("codec_name"),
        "width": stream.get("width"),
        "height": stream.get("height"),
        "pix_fmt": stream.get("pix_fmt"),
        "r_frame_rate": stream.get("r_frame_rate"),
        "duration": duration,
    }


def compatibility_signature(metadata: dict[str, object]) -> tuple[object, ...]:
    return (
        metadata["codec_name"],
        metadata["width"],
        metadata["height"],
        metadata["pix_fmt"],
        metadata["r_frame_rate"],
    )


def validate_compatible_clips(ffprobe: str, paths: Sequence[Path]) -> float:
    baseline_path = paths[0]
    baseline = probe_video(ffprobe, baseline_path)
    baseline_signature = compatibility_signature(baseline)
    total_duration = float(baseline["duration"])

    mismatches: list[str] = []
    for path in paths[1:]:
        metadata = probe_video(ffprobe, path)
        total_duration += float(metadata["duration"])
        signature = compatibility_signature(metadata)
        if signature != baseline_signature:
            mismatches.append(
                f"  - {path}\n"
                f"    expected {baseline_signature}\n"
                f"    found    {signature}"
            )

    if mismatches:
        raise AssemblyError(
            "The lesson renders do not share one stream-copy format. "
            "Re-render every lesson with the same Manim quality setting.\n"
            + "\n".join(mismatches)
        )
    return total_duration


def write_concat_manifest(paths: Iterable[Path], manifest_path: Path) -> None:
    lines: list[str] = ["ffconcat version 1.0"]
    for path in paths:
        absolute = str(path.resolve())
        if "'" in absolute:
            raise AssemblyError(f"A clip path contains an unsupported apostrophe: {absolute}")
        lines.append(f"file '{absolute}'")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_duration(seconds: float) -> str:
    rounded = max(0, int(round(seconds)))
    hours, remainder = divmod(rounded, 3600)
    minutes, seconds_part = divmod(remainder, 60)
    return f"{hours:d}:{minutes:02d}:{seconds_part:02d}"


def assemble(
    repo_root: Path,
    quality: str,
    *,
    dry_run: bool = False,
    render_missing: bool = False,
) -> tuple[Path, Path, float]:
    ffmpeg = command_path("ffmpeg")
    ffprobe = command_path("ffprobe")
    if render_missing and not dry_run:
        render_missing_clips(repo_root, quality)
    paths = collect_clip_paths(repo_root, quality)
    total_duration = validate_compatible_clips(ffprobe, paths)

    assembly_dir = repo_root / "media/videos/chapter_four_assembly" / quality
    assembly_dir.mkdir(parents=True, exist_ok=True)
    archive_output = assembly_dir / OUTPUT_FILENAME
    convenient_output = repo_root / "media" / OUTPUT_FILENAME

    if dry_run:
        return archive_output, convenient_output, total_duration

    temporary_output = assembly_dir / f".{OUTPUT_FILENAME}.tmp.mp4"
    temporary_output.unlink(missing_ok=True)

    with tempfile.TemporaryDirectory(prefix="cp127-chapter-four-") as temporary_directory:
        manifest = Path(temporary_directory) / "chapter_four.ffconcat"
        write_concat_manifest(paths, manifest)
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(manifest),
            "-map",
            "0:v:0",
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(temporary_output),
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as error:
            temporary_output.unlink(missing_ok=True)
            raise AssemblyError("ffmpeg could not concatenate the approved lesson renders.") from error

    temporary_output.replace(archive_output)
    convenient_output.parent.mkdir(parents=True, exist_ok=True)
    temporary_copy = convenient_output.with_name(f".{OUTPUT_FILENAME}.tmp")
    temporary_copy.unlink(missing_ok=True)
    shutil.copy2(archive_output, temporary_copy)
    temporary_copy.replace(convenient_output)
    return archive_output, convenient_output, total_duration


def parse_arguments(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="SeeingLinearAlgebra repository root (default: inferred from this script)",
    )
    parser.add_argument(
        "--quality",
        default=DEFAULT_QUALITY,
        help=f"Manim quality directory (default: {DEFAULT_QUALITY})",
    )
    parser.add_argument(
        "--render-missing",
        action="store_true",
        help="Render any missing chapter clips at the selected quality before assembly",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate every source clip without writing the assembled video",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    repo_root = arguments.repo_root.expanduser().resolve()
    try:
        archive_output, convenient_output, duration = assemble(
            repo_root,
            arguments.quality,
            dry_run=arguments.dry_run,
            render_missing=arguments.render_missing,
        )
    except (AssemblyError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"CP127 assembly failed:\n{error}", file=sys.stderr)
        return 1

    action = "Validated" if arguments.dry_run else "Assembled"
    print(f"{action} {len(CHAPTER_CLIPS)} chapter clips.")
    print(f"Approximate chapter duration: {format_duration(duration)}")
    print(f"Archive output: {archive_output}")
    print(f"Convenient copy: {convenient_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
