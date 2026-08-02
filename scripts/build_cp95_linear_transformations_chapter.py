#!/usr/bin/env python3
"""Render and concatenate the approved Linear Transformations chapter scenes."""

from __future__ import annotations

import ast
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MEDIA = REPO / "media"
ASSEMBLY_DIR = MEDIA / "videos" / "linear_transformations_chapter"
OUTPUT = ASSEMBLY_DIR / "LinearTransformationsChapter.mp4"


@dataclass(frozen=True)
class SceneSpec:
    label: str
    candidates: tuple[str, ...]
    required_tokens: tuple[str, ...] = ()


SPECS = (
    SceneSpec(
        "Chapter opening",
        ("scenes/linear_transformations_chapter_cards.py",),
        ("LinearTransformationsChapterOpening",),
    ),
    SceneSpec(
        "What a linear transformation does",
        (
            "scenes/what_does_a_linear_transformation_do_presentation.py",
            "scenes/what_does_linear_transformation_do_presentation.py",
            "scenes/linear_transformation_action_presentation.py",
        ),
        ("Linear", "Transformation"),
    ),
    SceneSpec(
        "Which transformations are linear",
        (
            "scenes/which_transformations_are_linear_presentation.py",
            "scenes/linear_transformation_tests_presentation.py",
        ),
        ("Linear",),
    ),
    SceneSpec(
        "Reflection then dilation",
        ("scenes/reflection_then_dilation_presentation.py",),
        ("Reflection", "Dilation"),
    ),
    SceneSpec(
        "Reflection preserves addition",
        (
            "scenes/reflection_preserves_addition_presentation.py",
            "scenes/reflection_addition_presentation.py",
        ),
        ("Reflection",),
    ),
    SceneSpec(
        "Linearity preserves linear combinations",
        ("scenes/linearity_preserves_linear_combinations_presentation.py",),
        ("Linear", "Combination"),
    ),
    SceneSpec(
        "Composition of transformations",
        (
            "scenes/matrix_composition_presentation.py",
        ),
        ("Matrix", "Composition"),
    ),
    SceneSpec(
        "A basis determines the transformation",
        ("scenes/basis_determines_transformation_presentation.py",),
        ("Basis", "Transformation"),
    ),
    SceneSpec(
        "Basis images become matrix columns",
        ("scenes/basis_images_to_matrix_presentation.py",),
        ("Basis", "Matrix"),
    ),
    SceneSpec(
        "Chapter reflection",
        ("scenes/linear_transformations_chapter_cards.py",),
        ("LinearTransformationsChapterReflection",),
    ),
)


def scene_classes(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            bases = {
                base.id
                for base in node.bases
                if isinstance(base, ast.Name)
            }
            if {"Scene", "ThreeDScene", "MovingCameraScene"} & bases:
                names.append(node.name)
    return names


def choose_scene(spec: SceneSpec) -> tuple[Path, str]:
    for candidate in spec.candidates:
        path = REPO / candidate
        if not path.exists():
            continue
        classes = scene_classes(path)
        if not classes:
            continue
        for class_name in classes:
            if all(token.lower() in class_name.lower() for token in spec.required_tokens):
                return path, class_name
        if len(classes) == 1:
            return path, classes[0]

    searched = "\n  ".join(spec.candidates)
    raise FileNotFoundError(
        f"Could not resolve scene for: {spec.label}\n"
        f"Searched:\n  {searched}"
    )


def render_scene(path: Path, class_name: str) -> Path:
    command = [
        "manim",
        "--disable_caching",
        "-qh",
        str(path.relative_to(REPO)),
        class_name,
    ]
    print("+", " ".join(command))
    subprocess.run(command, cwd=REPO, check=True)

    matches = sorted(
        MEDIA.glob(f"videos/**/{class_name}.mp4"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not matches:
        raise FileNotFoundError(f"Rendered video not found for {class_name}")
    return matches[0]


def main() -> int:
    if shutil.which("manim") is None:
        print("manim is not available on PATH", file=sys.stderr)
        return 1
    if shutil.which("ffmpeg") is None:
        print("ffmpeg is not available on PATH", file=sys.stderr)
        return 1

    ASSEMBLY_DIR.mkdir(parents=True, exist_ok=True)

    resolved = []
    print("\nResolved chapter order:")
    for index, spec in enumerate(SPECS, start=1):
        path, class_name = choose_scene(spec)
        resolved.append((spec, path, class_name))
        print(f"{index:2}. {spec.label}: {path.relative_to(REPO)}::{class_name}")

    clips = []
    for index, (spec, path, class_name) in enumerate(resolved, start=1):
        print(f"\n[{index}/{len(resolved)}] Rendering {spec.label}")
        clips.append(render_scene(path, class_name))

    concat_file = ASSEMBLY_DIR / "concat.txt"
    concat_file.write_text(
        "".join(f"file '{clip.resolve()}'\n" for clip in clips),
        encoding="utf-8",
    )

    command = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(OUTPUT),
    ]
    print("\n+", " ".join(command))
    subprocess.run(command, cwd=REPO, check=True)

    print(f"\nComplete chapter written to:\n{OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
