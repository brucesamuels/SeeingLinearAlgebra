# Checkpoint 231 — Laplacian Energy: Variation Across Edges

This checkpoint turns the graph Laplacian into a single global measure of
variation. Factoring the quadratic form through the incidence matrix gives

```text
x^T L x = x^T B^T B x = ||B x||^2
          = sum over edges {i,j} of (x_i-x_j)^2.
```

Because this is a sum of squares, it is nonnegative for every vertex vector.
The Laplacian is therefore positive semidefinite.

## Numerical spine

For the recurring values `x=(1,2,3,4)`,

```text
L*x = (-3,0,2,1)
x^T L x = -3+0+6+4 = 7

B*x = (1,1,2,1)
||B*x||^2 = 1^2+1^2+2^2+1^2 = 7.
```

The four undirected-edge contributions are

```text
{1,2}: (1-2)^2 = 1
{2,3}: (2-3)^2 = 1
{1,3}: (1-3)^2 = 4
{3,4}: (3-4)^2 = 1.
```

Reversing an incidence orientation changes the sign of one edge difference but
not its square. A constant vector has zero difference on every edge and hence
zero energy. On the recurring connected graph, zero energy also forces equality
to propagate along edges, so the vector must be constant.

## Story

1. Recall the four local coordinates in `L*x` and ask for one global measure of
   variation.
2. Form the quadratic scalar `x^T L x=7` structurally.
3. Substitute `L=B^T B` and regroup to obtain `||B*x||^2`.
4. Square the four familiar incidence differences and add them to get 7.
5. Attach each squared contribution to its undirected graph edge.
6. State the general edge-sum identity and explain both one-count-per-edge and
   orientation independence.
7. Recall the quadratic-form definition of positive semidefiniteness and apply
   it immediately to the sum of squares.
8. On this connected graph, show that zero energy forces equality along every
   edge and hence a constant vertex vector.
9. Distinguish a zero local Laplacian coordinate from zero total energy, then
   preview the role of connected components.

## Architecture

`GraphLaplacianEnergy` is renderer-independent and composes CP230's
`GraphLaplacianOperator`. It evaluates the quadratic form, incidence norm, and
direct graph-edge sum; exposes oriented differences and squared edge
contributions; verifies the three energy routes; and supports edge-orientation
reversal. The scene uses structural matrices, prominent edge flashes, and black
numerals inside colored vertices.

## Scope boundary

This checkpoint proves positive semidefiniteness through the energy identity and
characterizes zero energy only on the recurring connected graph. It does not yet
derive the full null-space/component theorem, introduce Laplacian eigenvalues or
the spectral gap, define the Fiedler vector, partition a graph, or model an
electrical network. Connected components and the Laplacian null space begin in
CP232.

## Files

```text
engine/graph_laplacian_energy.py
scenes/graph_laplacian_energy_presentation.py
tests/test_graph_laplacian_energy.py
tests/test_graph_laplacian_energy_presentation.py
scripts/check_cp231_graph_laplacian_energy.zsh
scripts/render_cp231_graph_laplacian_energy.zsh
CHECKPOINT_231.md
apply_checkpoint_231.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp231_graph_laplacian_energy.zsh
scripts/render_cp231_graph_laplacian_energy.zsh
```

The render command produces only an uncached low-quality preview for review.
