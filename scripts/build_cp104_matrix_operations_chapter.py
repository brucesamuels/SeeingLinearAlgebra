"""Build the complete Matrix Operations chapter video.

The builder renders the opening card, all chapter lessons, and the closing
reflection, then concatenates the resulting MP4 files with ffmpeg.

The CP94 scene is discovered by content because its exact historical filename
may differ across repository revisions.
"""

from __future__ import annotations

import argparse
import ast
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SceneSpec:
    label: str
    scene_file: str | None
    scene_class: str | None
    discovery_terms: tuple[str, ...] = ()


CHAPTER_SCENES = (
    SceneSpec(
        "Opening card",
        "scenes/matrix_operations_chapter_cards.py",
        "MatrixOperationsChapterTitleCard",
    ),
    SceneSpec(
        "Matrix addition and subtraction",
        "scenes/matrix_addition_subtraction_presentation.py",
        "MatrixAdditionSubtractionPresentation",
    ),
    SceneSpec(
        "Scalar multiplication of matrices",
        "scenes/matrix_scalar_multiplication_presentation.py",
        "MatrixScalarMultiplicationPresentation",
    ),
    SceneSpec(
        "Matrix-vector multiplication as a column combination",
        None,
        None,
        (
            "column combination",
            "matrix-vector",
            "matrix vector",
        ),
    ),
    SceneSpec(
        "The row-column rule",
        "scenes/row_column_rule_presentation.py",
        "RowColumnRulePresentation",
    ),
    SceneSpec(
        "Matrix-matrix multiplication",
        "scenes/matrix_matrix_multiplication_presentation.py",
        "MatrixMatrixMultiplicationPresentation",
    ),
    SceneSpec(
        "Matrix multiplication as composition",
        "scenes/matrix_multiplication_composition_presentation.py",
        "MatrixMultiplicationCompositionPresentation",
    ),
    SceneSpec(
        "The trace of a matrix",
        "scenes/matrix_trace_presentation.py",
        "MatrixTracePresentation",
    ),
    SceneSpec(
        "Matrix transposition",
        "scenes/matrix_transposition_presentation.py",
        "MatrixTranspositionPresentation",
    ),
    SceneSpec(
        "Order, identity, and undoing",
        "scenes/matrix_order_identity_undoing_presentation.py",
        "MatrixOrderIdentityUndoingPresentation",
    ),
    SceneSpec(
        "Closing reflection",
        "scenes/matrix_operations_chapter_cards.py",
        "MatrixOperationsChapterReflectionCard",
    ),
)


def scene_classes(source_path: Path) -> tuple[str, ...]:
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    classes: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        base_names = {
            base.id
            for base in node.bases
            if isinstance(base, ast.Name)
        }
        if "Scene" in base_names:
            classes.append(node.name)
    return tuple(classes)


def discover_scene(
    repo_root: Path,
    spec: SceneSpec,
) -> tuple[Path, str]:
    if spec.scene_file and spec.scene_class:
        scene_path = repo_root / spec.scene_file
        if not scene_path.exists():
            raise FileNotFoundError(
                f"{spec.label}: missing scene file {scene_path}"
            )
        classes = scene_classes(scene_path)
        if spec.scene_class not in classes:
            raise ValueError(
                f"{spec.label}: class {spec.scene_class} was not found "
                f"in {scene_path}"
            )
        return scene_path, spec.scene_class

    scenes_dir = repo_root / "scenes"
    candidates: list[tuple[int, Path, str]] = []

    for path in sorted(scenes_dir.glob("*.py")):
        source = path.read_text(encoding="utf-8")
        lowered = source.lower()
        score = sum(term in lowered for term in spec.discovery_terms)
        if score == 0:
            continue

        for class_name in scene_classes(path):
            class_score = score
            name_lower = class_name.lower()
            if "column" in name_lower:
                class_score += 2
            if "combination" in name_lower:
                class_score += 2
            if "matrix" in name_lower and "vector" in name_lower:
                class_score += 2
            candidates.append((class_score, path, class_name))

    if not candidates:
        raise FileNotFoundError(
            f"{spec.label}: could not discover a matching scene. "
            "Search terms were "
            f"{', '.join(spec.discovery_terms)}"
        )

    candidates.sort(
        key=lambda item: (item[0], item[1].name, item[2]),
        reverse=True,
    )
    _, path, class_name = candidates[0]
    return path, class_name


def run(command: list[str], *, cwd: Path) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def newest_render(media_dir: Path, class_name: str) -> Path:
    matches = list(media_dir.rglob(f"{class_name}.mp4"))
    if not matches:
        raise FileNotFoundError(
            f"No rendered MP4 was found for {class_name} under {media_dir}"
        )
    return max(matches, key=lambda path: path.stat().st_mtime)


def render_scene(
    repo_root: Path,
    media_dir: Path,
    scene_path: Path,
    class_name: str,
    quality: str,
) -> Path:
    quality_flags = {
        "low": "-ql",
        "medium": "-qm",
        "high": "-qh",
    }
    run(
        [
            sys.executable,
            "-m",
            "manim",
            quality_flags[quality],
            str(scene_path.relative_to(repo_root)),
            class_name,
        ],
        cwd=repo_root,
    )
    return newest_render(media_dir, class_name)


def concat_videos(
    videos: list[Path],
    output_path: Path,
    work_dir: Path,
) -> None:
    concat_file = work_dir / "matrix_operations_concat.txt"
    lines = []
    for video in videos:
        escaped = str(video.resolve()).replace("'", "'\\''")
        lines.append(f"file '{escaped}'")
    concat_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    copy_command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(output_path),
    ]

    try:
        run(copy_command, cwd=work_dir)
    except subprocess.CalledProcessError:
        # Re-encode if stream parameters differ across older scene renders.
        run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-an",
                str(output_path),
            ],
            cwd=work_dir,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quality",
        choices=("low", "medium", "high"),
        default="low",
    )
    parser.add_argument(
        "--output",
        default=(
            "media/videos/matrix_operations_chapter/"
            "MatrixOperationsChapter.mp4"
        ),
    )
    parser.add_argument(
        "--reuse-existing",
        action="store_true",
        help="Reuse existing scene MP4 files when available.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    media_dir = repo_root / "media"
    output_path = repo_root / args.output
    work_dir = repo_root / ".cp104_build"
    work_dir.mkdir(exist_ok=True)

    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required but was not found on PATH")

    rendered: list[Path] = []

    print("\nMatrix Operations chapter order:\n")
    for index, spec in enumerate(CHAPTER_SCENES, start=1):
        scene_path, class_name = discover_scene(repo_root, spec)
        print(
            f"{index:2d}. {spec.label}\n"
            f"    {scene_path.relative_to(repo_root)} :: {class_name}"
        )

        existing: Path | None = None
        always_rerender = class_name in {
            "MatrixOperationsChapterTitleCard",
            "MatrixOperationsChapterReflectionCard",
        }
        if args.reuse_existing and not always_rerender:
            try:
                existing = newest_render(media_dir, class_name)
            except FileNotFoundError:
                existing = None

        if existing is not None:
            print(f"    Reusing {existing.relative_to(repo_root)}")
            rendered.append(existing)
        else:
            rendered.append(
                render_scene(
                    repo_root,
                    media_dir,
                    scene_path,
                    class_name,
                    args.quality,
                )
            )

    concat_videos(rendered, output_path, work_dir)

    print("\nComplete chapter created:")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
