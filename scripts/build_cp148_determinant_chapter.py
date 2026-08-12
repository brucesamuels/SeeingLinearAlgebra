#!/usr/bin/env python3
"""Build the Chapter 5 determinant assembly from the newest rendered scene videos."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


SCENE_ORDER: tuple[tuple[str, str], ...] = (
    ("DeterminantChapterTitleCard", "Chapter 5 title card"),
    ("WhyDeterminantsPresentation", "Why Do We Need Determinants?"),
    ("DeterminantAreaScalePresentation", "Determinant as Area Scale Factor"),
    ("DeterminantOrientationPresentation", "Determinant Sign and Orientation"),
    ("DeterminantFormulaGeometryPresentation", "Geometric Derivation of the 2 x 2 Formula"),
    ("DeterminantGeometryPresentation", "Determinant as Signed Area and Volume Scaling"),
    ("DeterminantPropertiesPresentation", "Foundational Determinant Properties"),
    ("DeterminantConsequencesPresentation", "Derived Determinant Consequences"),
    ("DeterminantProductRulePresentation", "Determinants of Products"),
    ("DeterminantTransposeRulePresentation", "Determinant of a Transpose"),
    ("DeterminantEliminationPresentation", "Determinants and Elimination"),
    ("DeterminantBigFormulaPresentation", "The Big Formula"),
    ("DeterminantBigFormulaDerivationPresentation", "From Permutations to the 3 x 3 Formula"),
    ("DeterminantCofactorExpansionPresentation", "Cofactor Expansion"),
    ("DeterminantCofactorEfficiencyPresentation", "Using Cofactor Expansion Efficiently"),
    ("DeterminantTriangularPresentation", "Triangular and Block-Triangular Matrices"),
    ("DeterminantInvertibilityPresentation", "Determinant and Invertibility"),
    ("DeterminantCramersRulePresentation", "Cramer's Rule"),
    ("DeterminantAdjugateInversePresentation", "The Adjugate and the Inverse Formula"),
    ("DeterminantJacobianPreviewPresentation", "Determinants and Change of Variables / Jacobian Preview"),
    ("DeterminantChapterSynthesisPresentation", "Determinant Chapter Synthesis"),
)


def newest_render(media_root: Path, scene_class: str, quality_dir: str | None = None) -> Path | None:
    candidates = [
        path
        for path in media_root.rglob(f"{scene_class}.mp4")
        if "partial_movie_files" not in path.parts
        and (quality_dir is None or quality_dir in path.parts)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def quote_concat_path(path: Path) -> str:
    # ffmpeg concat files use single-quoted paths; escape any embedded quote.
    return "'" + str(path.resolve()).replace("'", "'\\''") + "'"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("media/chapter_five_determinants/Chapter5_Determinants_Assembly.mp4"),
    )
    parser.add_argument(
        "--quality-dir",
        default=None,
        help="Require renders from a Manim quality directory such as 1080p60.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    media_root = repo_root / "media"
    if not media_root.exists():
        print(f"Missing media directory: {media_root}", file=sys.stderr)
        return 2

    if shutil.which("ffmpeg") is None:
        print("ffmpeg is required but was not found on PATH.", file=sys.stderr)
        return 2

    selected: list[tuple[str, str, Path]] = []
    missing: list[tuple[str, str]] = []
    for scene_class, lesson_title in SCENE_ORDER:
        path = newest_render(media_root, scene_class, args.quality_dir)
        if path is None:
            missing.append((scene_class, lesson_title))
        else:
            selected.append((scene_class, lesson_title, path))

    if missing:
        print("Cannot assemble Chapter 5. Missing rendered videos:", file=sys.stderr)
        for scene_class, lesson_title in missing:
            print(f"  - {scene_class}: {lesson_title}", file=sys.stderr)
        return 3

    output = args.output
    if not output.is_absolute():
        output = repo_root / output
    output.parent.mkdir(parents=True, exist_ok=True)

    concat_file = output.parent / "chapter5_concat_list.txt"
    concat_file.write_text(
        "".join(f"file {quote_concat_path(path)}\n" for _, _, path in selected),
        encoding="utf-8",
    )

    print("Chapter 5 assembly order:")
    for index, (_, lesson_title, path) in enumerate(selected, start=1):
        print(f"{index:2d}. {lesson_title}")
        print(f"    {path.relative_to(repo_root)}")

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "18",
        "-preset",
        "medium",
        "-movflags",
        "+faststart",
        str(output),
    ]
    subprocess.run(command, check=True)
    print(f"\nAssembled chapter: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
