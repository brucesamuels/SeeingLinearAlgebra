# Checkpoint 214 — Positive Definite Matrices Final Master

This checkpoint renders the approved Positive Definite Matrices chapter from
current source at 1080p60, assembles the lessons in CP213 order, and creates a
final viewing master at 80% of the animation speed. The slower presentation
provides more time to absorb the chapter's denser arguments.

## Master order

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

## Narration

`POSITIVE_DEFINITE_MATRICES_NARRATION.md` is a proposed, time-aligned narration
for the 80%-speed master. It explains “quadratic energy” at the outset: the
term is literal for stored energy in physical systems and interpretive when the
quadratic form represents variance, squared size, or cost.

The script targets a final duration of approximately 18 minutes 37 seconds.
No narration audio is generated or embedded at this checkpoint.

## Build behavior

The render process:

1. Requires Python 3.12, Manim Community 0.21.0, ffmpeg, and ffprobe.
2. Renders the title and every CP199–CP212 lesson from current source at
   1920x1080, 60 frames per second.
3. Verifies the codec, dimensions, pixel format, frame rate, and duration of
   every segment.
4. Creates a lossless stream-copy assembly at the original animation speed.
5. Retimes the assembly to 80% speed and encodes it as high-quality H.264,
   yuv420p, with fast-start metadata.
6. Verifies the final master signature and expected slowed duration.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp214_positive_definite_master.zsh
scripts/render_cp214_positive_definite_master.zsh
```

Outputs:

```text
media/videos/positive_definite_matrices_assembly/PositiveDefiniteMatrices_1080p60_fullspeed.mp4
media/videos/positive_definite_matrices_assembly/PositiveDefiniteMatrices_1080p60_80pct.mp4
```

Rendered media remains outside source control.

## Files

```text
scripts/build_cp214_positive_definite_master.py
tests/test_cp214_positive_definite_master.py
scripts/check_cp214_positive_definite_master.zsh
scripts/render_cp214_positive_definite_master.zsh
POSITIVE_DEFINITE_MATRICES_NARRATION.md
CHECKPOINT_214.md
apply_checkpoint_214.zsh
```
