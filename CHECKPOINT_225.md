# Checkpoint 225 — Singular Values, Rank, and Approximation Final Master

This checkpoint renders the approved CP224 chapter sequence fresh from current
source at high definition and assembles the final **Singular Values, Rank, and
Approximation** master.

## Master order

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

## Pacing

The high-definition master preserves the approved source timing. No additional
chapter-wide slowdown is applied: CP223 already contains its requested slower
card holds, while the other lessons retain their approved pacing.

## Build behavior

The builder:

1. Reuses the exact CP224 chapter order.
2. Renders the title and all nine lessons fresh at 1920x1080 and 60 fps.
3. Requires H.264, yuv420p, and matching segment signatures.
4. Concatenates the segments by stream copy without recompression or retiming.
5. Verifies the master signature and its duration against the source total.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp225_svd_chapter_master.zsh
scripts/render_cp225_svd_chapter_master.zsh
```

Output:

```text
media/videos/singular_values_rank_approximation_assembly/SingularValuesRankApproximation_1080p60.mp4
```

Rendered media remains outside source control.
