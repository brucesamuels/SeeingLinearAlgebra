#!/usr/bin/env python3
"""Render Chapter 7 at 1080p60 and create the approved 85%-speed master."""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path


LESSONS = [
    (168, ("eigenvector_special_directions_presentation.py",), "Special directions"),
    (169, ("eigenvectors_and_eigenvalues_presentation.py", "eigenvectors_eigenvalues_presentation.py"), "Eigenvectors and eigenvalues"),
    (170, ("eigenspaces_presentation.py",), "Eigenspaces"),
    (171, ("characteristic_equation_presentation.py", "characteristic_equation_derivation_presentation.py", "why_characteristic_equation_presentation.py"), "Characteristic equation"),
    (172, ("computing_eigenvalues_presentation.py", "eigenvalue_computation_presentation.py"), "Computing eigenvalues"),
    (173, ("computing_eigenvectors_presentation.py",), "Computing eigenvectors"),
    (174, ("eigenvector_basis_presentation.py",), "An eigenvector basis"),
    (175, ("diagonalization_presentation.py",), "Diagonalization"),
    (176, ("powers_of_diagonalizable_matrix_presentation.py",), "Powers of a diagonalizable matrix"),
    (177, ("repeated_eigenvalues_presentation.py",), "Repeated eigenvalues and diagonalizability"),
    (178, ("symmetric_orthogonal_eigenvectors_presentation.py",), "Symmetric matrices and orthogonal eigenvectors"),
    (179, ("spectral_theorem_presentation.py",), "Spectral theorem"),
    (180, ("dominant_eigenvector_presentation.py",), "Dynamics and the dominant eigenvector"),
    (181, ("first_order_system_eigenvectors_presentation.py",), "First-order differential systems"),
    (182, ("fibonacci_difference_equation_presentation.py",), "Fibonacci and difference equations"),
    (183, ("eigenvalues_chapter_review_presentation.py",), "Chapter review"),
]

SPEED = 0.85


def detect_scene_class(scene_file: Path) -> str:
    tree = ast.parse(scene_file.read_text(encoding="utf-8"), filename=str(scene_file))
    scene_bases = {"Scene", "ThreeDScene", "MovingCameraScene"}
    candidates: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        base_names: list[str] = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_names.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_names.append(base.attr)
        if scene_bases.intersection(base_names):
            candidates.append(node.name)
    if len(candidates) != 1:
        raise RuntimeError(
            f"Expected exactly one top-level Manim scene class in {scene_file}; found {candidates}"
        )
    return candidates[0]


def resolve_scene(scenes_dir: Path, checkpoint: int, candidates: tuple[str, ...]) -> Path:
    for name in candidates:
        path = scenes_dir / name
        if path.exists():
            return path

    checkpoint_tokens = {
        169: ("eigen", "value"),
        171: ("characteristic",),
        172: ("eigen", "comput"),
    }.get(checkpoint, ())
    if checkpoint_tokens:
        matches = [
            p for p in scenes_dir.glob("*_presentation.py")
            if all(token in p.stem.lower() for token in checkpoint_tokens)
        ]
        if len(matches) == 1:
            return matches[0]

    expected = ", ".join(candidates)
    raise FileNotFoundError(
        f"CP{checkpoint}: could not find the approved scene. Expected one of: {expected}"
    )


def run(command: list[str], cwd: Path) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def newest_render(media_dir: Path, class_name: str) -> Path:
    matches = list(media_dir.rglob(f"{class_name}.mp4"))
    if not matches:
        raise FileNotFoundError(f"Could not locate rendered MP4 for {class_name} under {media_dir}")
    return max(matches, key=lambda p: p.stat().st_mtime)


def main() -> int:
    repo_root = Path.cwd().resolve()
    scenes_dir = repo_root / "scenes"
    title_file = scenes_dir / "chapter_seven_title_card.py"
    if not title_file.exists():
        raise FileNotFoundError(
            f"Missing {title_file}. Install the Chapter 7 assembly checkpoint first."
        )

    ordered: list[tuple[str, Path, str]] = [
        ("Chapter 7 title", title_file, detect_scene_class(title_file))
    ]
    for checkpoint, candidates, label in LESSONS:
        scene_file = resolve_scene(scenes_dir, checkpoint, candidates)
        ordered.append((f"CP{checkpoint} — {label}", scene_file, detect_scene_class(scene_file)))

    print("\nChapter 7 final-master order:")
    for index, (label, scene_file, class_name) in enumerate(ordered, start=1):
        print(f"  {index:02d}. {label}: {scene_file.name} :: {class_name}")

    media_dir = repo_root / "media" / "cp186_chapter_seven_master_segments"
    media_dir.mkdir(parents=True, exist_ok=True)
    segments: list[Path] = []

    for index, (label, scene_file, class_name) in enumerate(ordered, start=1):
        print(f"\nRendering {index}/{len(ordered)} at 1080p60: {label}")
        run(
            [
                "manim",
                "-qh",
                "--media_dir",
                str(media_dir),
                str(scene_file),
                class_name,
            ],
            cwd=repo_root,
        )
        segments.append(newest_render(media_dir, class_name))

    output_dir = repo_root / "media" / "videos" / "chapter_seven_assembly"
    output_dir.mkdir(parents=True, exist_ok=True)
    concat_file = media_dir / "chapter_seven_master_concat.txt"
    concat_file.write_text(
        "".join(f"file '{p.as_posix()}'\n" for p in segments),
        encoding="utf-8",
    )

    fullspeed = output_dir / "ChapterSeven_EigenvaluesAndEigenvectors_1080p60_fullspeed.mp4"
    run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_file), "-c", "copy", str(fullspeed),
        ],
        cwd=repo_root,
    )

    slowed = output_dir / "ChapterSeven_EigenvaluesAndEigenvectors_1080p60_85pct.mp4"
    run(
        [
            "ffmpeg", "-y", "-i", str(fullspeed),
            "-vf", f"setpts=PTS/{SPEED},fps=60",
            "-an",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "16",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(slowed),
        ],
        cwd=repo_root,
    )

    print(f"\nFull-speed 1080p60 assembly:\n{fullspeed}")
    print(f"\nFinal 85% speed 1080p60 master:\n{slowed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
