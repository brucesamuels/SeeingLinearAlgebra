# Checkpoint 230 — The Graph Laplacian: Differences Return

This checkpoint introduces the graph Laplacian as a vertex-to-edge-to-vertex
composition. The incidence matrix sends vertex values to oriented edge
differences, and its transpose gathers those signed differences back at the
vertices. Their composition is independent of the temporary edge orientations
and agrees with degrees minus adjacency:

```text
L = B^T B = D - A.
```

## Numerical spine

For the recurring graph,

```text
L = [[ 2,-1,-1, 0],
     [-1, 2,-1, 0],
     [-1,-1, 3,-1],
     [ 0, 0,-1, 1]].
```

The diagonal entries are the vertex degrees. An off-diagonal entry is `-1`
when its two vertices share an edge and zero otherwise.

For `x=(1,2,3,4)`,

```text
B*x       = ( 1,1,2,1)
B^T*(B*x) = (-3,0,2,1)
L*x       = (-3,0,2,1).
```

Each coordinate is a local neighbor-difference sum. At vertex 1,

```text
(L*x)_1 = (x1-x2)+(x1-x3) = -3.
```

Reversing one edge negates its incidence row and its oriented difference. The
matching signs in the transpose also reverse, so `B^T B` and `L*x` do not
change. Every row of `L` sums to zero, giving `L*1=0`.

## Story

1. Recall that `B*x` sends the familiar vertex values to four oriented edge
   differences.
2. Apply `B^T` to those edge values and interpret the signed return at vertex 1.
3. Compose the two maps and name `L=B^T B` as the graph Laplacian.
4. Multiply the structural matrices to obtain the exact vertex-by-vertex `L`.
5. Read its diagonal and off-diagonal pattern and identify `L=D-A`.
6. Interpret `(L*x)_1` as the sum of vertex 1's comparisons with its neighbors.
7. Compute the full vector `L*x=(-3,0,2,1)` and explain that a zero coordinate
   can mean local balance rather than globally constant values.
8. Reverse edge `e3` and show why the paired sign changes cancel in `B^T B`.
9. Synthesize the three views of `L`, show `L*1=0`, and preview total variation
   across edges.

## Architecture

`GraphLaplacianOperator` is renderer-independent and composes CP229's
`GraphIncidenceEncoding`. It constructs the Laplacian from both `B^T B` and
`D-A`, validates their equality, maps vertex values to edge differences,
returns edge values through `B^T`, evaluates the full Laplacian action, computes
individual local neighbor-difference sums, and supports orientation-reversal
checks. The scene uses structural matrices and black numerals inside colored
vertices for strong contrast.

## Scope boundary

This checkpoint defines and interprets the Laplacian operator, but it does not
yet derive Laplacian energy, prove positive semidefiniteness, characterize the
full null space through connected components, introduce Laplacian eigenvalues,
or discuss electrical networks. The quadratic energy identity begins in CP231.

## Files

```text
engine/graph_laplacian_operator.py
scenes/graph_laplacian_operator_presentation.py
tests/test_graph_laplacian_operator.py
tests/test_graph_laplacian_operator_presentation.py
scripts/check_cp230_graph_laplacian_operator.zsh
scripts/render_cp230_graph_laplacian_operator.zsh
CHECKPOINT_230.md
apply_checkpoint_230.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp230_graph_laplacian_operator.zsh
scripts/render_cp230_graph_laplacian_operator.zsh
```

The render command produces only an uncached low-quality preview for review.
