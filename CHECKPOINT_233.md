# Checkpoint 233 — Laplacian Eigenvalues and the Spectral Gap

This checkpoint moves from the Laplacian null space to the low end of the full
Laplacian spectrum. For a connected graph, the constant direction has
eigenvalue zero. The next eigenvalue,

```text
lambda_2 = min over nonzero x perpendicular to 1 of (x^T L x)/(x^T x),
```

is the spectral gap, also called the algebraic connectivity. It is positive
exactly when the graph is connected.

## Numerical spine

The recurring triangle-with-a-tail graph has exact ordered spectrum

```text
lambda_1, lambda_2, lambda_3, lambda_4 = 0, 1, 3, 4.
```

Exact eigenvectors may be chosen as

```text
lambda_1 = 0:  ( 1,  1,  1,  1)^T
lambda_2 = 1:  ( 1,  1,  0, -2)^T
lambda_3 = 3:  ( 1, -1,  0,  0)^T
lambda_4 = 4:  ( 1,  1, -3,  1)^T.
```

For the second mode `v_2=(1,1,0,-2)^T`,

```text
v_2^T L v_2 = 0 + 1 + 1 + 4 = 6,
v_2^T v_2 = 1 + 1 + 0 + 4 = 6,
R(v_2) = 6/6 = 1 = lambda_2.
```

Deleting the bridge `{3,4}` changes the spectrum to `(0,0,3,3)`, so the
spectral gap closes from one to zero as the graph separates.

## Story

1. Recall that the constant null vector is an eigenvector with eigenvalue zero.
2. Order the four real, nonnegative Laplacian eigenvalues and reveal the exact
   spectrum `(0,1,3,4)` on a number line.
3. Verify the exact second eigenpair `L(1,1,0,-2)^T=1(1,1,0,-2)^T` and note that
   it is perpendicular to the constant vector.
4. Place the second mode on the graph. Its largest squared change occurs on the
   lone edge leading to vertex 4.
5. Introduce the Rayleigh quotient as energy divided by squared vector length
   and compute the exact value one.
6. Exclude the constant direction and characterize `lambda_2` as the least
   normalized nonconstant variation.
7. Define the spectral gap and establish `lambda_2>0` for connected graphs and
   `lambda_2=0` for disconnected graphs.
8. Compare the bridge-present spectrum `(0,1,3,4)` with the bridge-removed
   spectrum `(0,0,3,3)`.
9. Synthesize zero multiplicity, the gap, and the second mode; name the second
   eigenvector as a Fiedler vector and preview using its signs.

## Architecture

`GraphLaplacianSpectrum` is renderer-independent and composes the established
graph, incidence, Laplacian, and energy models. It returns ordered orthonormal
eigenpairs with a deterministic sign convention, the second eigenvalue and
mode, zero multiplicity, the spectral connectivity test, Rayleigh quotients,
orthogonality to constants, and eigenpair residuals.

The scene retains the chapter's banner, title, heading, color, spacing, and
pacing conventions. It uses a structural matrix product, a spectral number
line, prominent edge flashes, legible fractions, and black numerals inside
colored vertices.

## Scope boundary

This checkpoint names the Fiedler vector only on its final card. It does not yet
turn its signs or coordinates into a graph partition, optimize a cut, introduce
normalized Laplacians, or model electrical networks. Spectral partitioning
begins in CP234.

## Files

```text
engine/graph_laplacian_spectrum.py
scenes/graph_laplacian_spectrum_presentation.py
tests/test_graph_laplacian_spectrum.py
tests/test_graph_laplacian_spectrum_presentation.py
scripts/check_cp233_graph_laplacian_spectrum.zsh
scripts/render_cp233_graph_laplacian_spectrum.zsh
CHECKPOINT_233.md
apply_checkpoint_233.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp233_graph_laplacian_spectrum.zsh
scripts/render_cp233_graph_laplacian_spectrum.zsh
```

The render command produces only an uncached low-quality preview for review.
