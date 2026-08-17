# Checkpoint 166 - Chapter 6 Preview Assembly

## Purpose

Assemble the approved Chapter 6 lessons into a single low-quality preview video without changing lesson content.

## Preview sequence

1. CP149 - Why Orthogonality?
2. CP150 - Dot Product and Perpendicularity
3. CP151 - Orthogonal Sets
4. CP152 - Orthonormal Sets
5. CP153 - Projection onto a Vector
6. CP154 - Orthogonal Decomposition
7. CP155 - Projection onto a Subspace
8. CP156 - Orthogonal Complements
9. CP157 - Gram-Schmidt with Two Vectors
10. CP159 - Gram-Schmidt in R^3
11. CP158 - From Orthogonal to Orthonormal
12. CP160 - QR Factorization: Gram-Schmidt in Matrix Form
13. CP161 - Least Squares: Projection and the Normal Equation
14. CP162 - Orthogonal Matrices Preserve Geometry
15. CP163 - Rotations and Reflections: Orthogonal Transformations
16. CP164 - Projection Matrices: Symmetric and Idempotent
17. CP165 - Orthogonality and Projection: The Big Picture

CP159 is placed before CP158 so the orthonormalization lesson's explicit `Q^TQ=I` / `A=QR` bridge leads directly into QR.

## Assembly behavior

- Reuses approved `480p15` lesson renders when they are already present.
- Renders only missing clips at Manim low quality (`-ql`).
- `--fresh` forces all 17 lesson clips to be rerendered at `480p15`.
- Uses FFprobe to verify that all clips have matching codec, dimensions, frame rate, and pixel format before concatenation.
- Uses FFmpeg stream-copy concatenation after validation.

## Output

`media/ChapterSixOrthogonalityAndProjection_preview.mp4`

## Commands

```zsh
zsh scripts/check_cp166_chapter_six_assembly.zsh
zsh scripts/assemble_cp166_chapter_six_preview.zsh
open media/ChapterSixOrthogonalityAndProjection_preview.mp4
```

If the existing low-quality renders are not mutually compatible:

```zsh
zsh scripts/assemble_cp166_chapter_six_preview.zsh --fresh
```
