# Checkpoint 213 — Positive Definite Matrices Preview Assembly

This checkpoint creates the opening title card and assembles the approved
low-quality Positive Definite Matrices chapter preview. It uses the completed
CP199–CP212 lesson renders without altering their internal pacing.

## Final preview order

1. Positive Definite Matrices title card
2. CP199 — Why Positive Definiteness?
3. CP200 — From Directional Energy to a Bowl
4. CP201 — The Eigenvalue Test
5. CP202 — The Elimination Test
6. CP203 — The LDL-Transpose Factorization
7. CP204 — Cholesky: A Matrix Square Root
8. CP205 — Why A-Transpose A Is Positive Semidefinite
9. CP206 — Why Least Squares Has a Unique Solution
10. CP207 — Why Covariance Is Positive Semidefinite
11. CP208 — Why the Singular Value Decomposition?
12. CP209 — Computing the SVD from A-Transpose A
13. CP210 — The Minimum Principle
14. CP211 — Finite Elements: Turning Energy into a Matrix
15. CP212 — Positive Definiteness: The Big Picture

The conceptual arc is:

```text
directional energy
  -> geometry
  -> practical tests
  -> factorizations
  -> Gram-matrix applications
  -> SVD
  -> minimum principles
  -> finite elements
  -> synthesis
```

## Build behavior

The render script:

1. Requires Python 3.12 and Manim Community 0.21.0.
2. Renders only the new title card at low quality.
3. Finds the newest exact `480p15` render for every approved lesson scene.
4. Reports every missing clip instead of building an incomplete chapter.
5. Uses `ffprobe` to require matching codec, dimensions, pixel format, and frame
   rate before concatenation.
6. Uses ffmpeg stream-copy concatenation so the approved lesson renders are not
   recompressed.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp213_positive_definite_preview.zsh
scripts/render_cp213_positive_definite_preview.zsh
```

Output:

```text
media/videos/positive_definite_matrices_assembly/PositiveDefiniteMatrices_preview.mp4
```

This is a review assembly, not the final high-definition master. The full chapter
should be watched for transition, pacing, terminology, and visual-consistency issues
before any final render checkpoint.

## Files

```text
scenes/positive_definite_matrices_title_card.py
scripts/build_cp213_positive_definite_preview.py
tests/test_positive_definite_matrices_title_card.py
tests/test_cp213_positive_definite_preview_assembly.py
scripts/check_cp213_positive_definite_preview.zsh
scripts/render_cp213_positive_definite_preview.zsh
CHECKPOINT_213.md
apply_checkpoint_213.zsh
```
