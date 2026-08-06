# Checkpoint 127: Assemble Chapter 4

## Purpose

Assemble the complete chapter

\[
\text{Chapter 4: Solving Linear Systems},
\qquad
A\mathbf{x}=\mathbf{b}.
\]

The chapter now contains the twenty lessons from Checkpoints 105 through 124,
followed by the two rectangular-system lessons developed in Checkpoints 125 and
126. Pedagogically, the rectangular lessons are inserted immediately after the
rank-and-consistency lesson and before elementary matrices.

## Chapter order

1. What it means to solve \(A\mathbf{x}=\mathbf b\)
2. Equations to an augmented matrix
3. Elementary row operations
4. Why row replacement preserves solutions
5. Gaussian elimination to echelon form
6. Back substitution
7. The elimination algorithm
8. Gauss-Jordan elimination and RREF
9. Reading solution sets from RREF
10. Pivot and free variables
11. Homogeneous systems and the null space
12. A basis for the null space
13. The complete solution
14. Rank, pivots, and consistency
15. Rectangular matrices and the geometry of \(A\mathbf{x}=\mathbf b\)
16. Solvability of overdetermined and underdetermined systems
17. Elementary matrices
18. Elimination as matrix multiplication
19. Multiple right-hand sides
20. Inverse by Gauss-Jordan elimination
21. Why some matrices are not invertible
22. Pivoting and \(PA=LU\)

## Assembly behavior

The builder assembles the chapter at Manim's `1080p60` quality. It checks every
expected render before concatenation. Any missing high-quality render is created
automatically with `python -m manim --disable_caching -qh`.

Existing compatible clips are reused without re-rendering or re-encoding. After
validating codec, resolution, pixel format, and frame rate with FFprobe, the
builder uses FFmpeg stream-copy concatenation.

The completed chapter is written to:

- `media/videos/chapter_four_assembly/1080p60/ChapterFourSolvingLinearSystems.mp4`
- `media/ChapterFourSolvingLinearSystems.mp4`

## Files

- `scenes/chapter_four_title_card.py`
- `scripts/build_cp127_chapter_four.py`
- `scripts/build_cp127_chapter_four.zsh`
- `scripts/check_cp127_chapter_four_assembly.zsh`
- `tests/test_cp127_chapter_four_assembly.py`

## Run focused checks

```zsh
./scripts/check_cp127_chapter_four_assembly.zsh
```

## Build and preview the chapter

```zsh
./scripts/build_cp127_chapter_four.zsh --preview
```

The first build may render the title card or any lesson that is not already
available at `1080p60`. Later builds reuse those clips.

## Visual review

Check especially:

- the opening title card and transition into the first lesson;
- that all twenty-two lessons appear exactly once;
- the transition from rank and consistency into rectangular matrices;
- the transition from rectangular solvability into elementary matrices;
- consistent resolution and frame rate across all clips;
- the final transition into `Pivoting and PA = LU`;
- the convenient chapter copy at `media/ChapterFourSolvingLinearSystems.mp4`.
