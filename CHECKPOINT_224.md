# Checkpoint 224 — Singular Values, Rank, and Approximation Preview Assembly

This checkpoint creates the unnumbered chapter title card and assembles a fresh
low-quality preview of the completed **Singular Values, Rank, and
Approximation** chapter.

## Preview order

1. Singular Values, Rank, and Approximation title card
2. CP215 — What Does a Zero Singular Value Mean?
3. CP216 — Full SVD and the Four Fundamental Subspaces
4. CP217 — The Pseudoinverse: Undo What Can Be Undone
5. CP218 — Least Squares and Minimum-Norm Solutions
6. CP219 — Small Singular Values and Conditioning
7. CP220 — Truncated SVD and the Best Low-Rank Approximation
8. CP221 — Image Compression with the SVD
9. CP222 — Principal Component Analysis through the SVD
10. CP223 — Singular Values, Rank, and Approximation: The Big Picture

CP208 and CP209 remain in the preceding Positive Definite Matrices chapter,
where they introduce and compute the SVD through Gram matrices. CP215 opens
this chapter by extending that bridge to rank loss.

## Build behavior

The builder:

1. Requires Python 3.12, Manim Community 0.21.0, ffmpeg, and ffprobe.
2. Detects and verifies the expected scene class in every source file.
3. Renders the title and all nine lessons fresh at `480p15` by default.
4. Verifies codec, dimensions, pixel format, and frame rate compatibility.
5. Concatenates by stream copy without recompressing approved frames.
6. Verifies that the assembled duration matches the sum of its source clips.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp224_svd_chapter_preview.zsh
scripts/render_cp224_svd_chapter_preview.zsh
```

Default output:

```text
media/videos/singular_values_rank_approximation_assembly/SingularValuesRankApproximation_preview.mp4
```

This is a review assembly, not the final high-definition master. Review the
complete chapter for transitions, pacing, terminology, and visual consistency
before creating the final render checkpoint.
