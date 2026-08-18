# Checkpoint 167 - Chapter 6 HD Master Assembly

## Purpose

Render all 17 approved Chapter 6 scenes fresh at Manim high quality and assemble the final HD chapter master.

## Quality

- Manim `-qh`
- 1920x1080
- 60 fps
- Fresh render of every approved scene; no reuse of old lesson clips

## Final sequence

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

## Output

`media/ChapterSixOrthogonalityAndProjection.mp4`

The approved low-quality preview remains at:

`media/ChapterSixOrthogonalityAndProjection_preview.mp4`

## Commands

```zsh
zsh scripts/check_cp167_chapter_six_hd.zsh
caffeinate -i zsh scripts/assemble_cp167_chapter_six_hd.zsh
open media/ChapterSixOrthogonalityAndProjection.mp4
```

`caffeinate -i` is recommended because a fresh 17-scene 1080p60 render can take substantial time.
