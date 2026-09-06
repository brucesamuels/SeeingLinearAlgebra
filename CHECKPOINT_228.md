# Checkpoint 228 — Matrix Powers Count Walks

This checkpoint turns adjacency-matrix multiplication into a graph operation.
One factor of `A` records one edge-step. Matrix multiplication sums over the
possible intermediate vertex, so each additional factor appends one step to a
walk. The entry `(A^k)_ij` therefore counts walks of exactly length `k` from
vertex `i` to vertex `j`.

## Numerical spine

For the recurring graph and vertex order `(1,2,3,4)`,

```text
A^2 = [[2,1,1,1],
       [1,2,1,1],
       [1,1,3,0],
       [1,1,0,1]]

A^3 = [[2,3,4,1],
       [3,2,4,1],
       [4,4,2,3],
       [1,1,3,0]].
```

The entry `(A^2)_11=2` counts the walks `1-2-1` and `1-3-1`.
The entry `(A^2)_14=1` counts the unique walk `1-3-4`. The entry
`(A^3)_13=4` counts four walks, several of which revisit a vertex. These are
walk counts, not counts of paths or shortest routes.

## Story

1. Recall that a walk follows edges, may repeat vertices, and has an exact
   length measured in edge-steps.
2. Interpret entries of `A` as counts of one-step walks.
3. Animate the two length-two return walks from vertex 1 through intermediate
   vertices 2 and 3.
4. Compute `(A^2)_11` as a structural row-column product and match its two
   nonzero products to those two walks.
5. Compute `(A^2)_14=1` and animate the unique walk `1-3-4`.
6. Reveal the complete matrix `A^2` and interpret several entries, including a
   zero count.
7. Form `A^3=A^2 A` and list the four length-three walks from vertex 1 to
   vertex 3, explicitly retaining repeated vertices.
8. State the general walk-counting rule only after the exact examples explain
   why multiplication appends an edge-step.
9. Synthesize graph edges, `A`, and `A^k`, then preview oriented incidence data.

## Architecture

`GraphWalkCounting` is renderer-independent and composes CP227's
`GraphMatrixEncoding`. It validates exact nonnegative walk lengths and known
vertices, computes integer matrix powers, returns endpoint counts, and
enumerates small exact walk sets for visual verification. The Manim scene owns
all layout and animation decisions and uses structural `Matrix` objects.

## Scope boundary

This checkpoint counts walks, for which repeated vertices and edges are
allowed. It does not count simple paths, introduce directed or weighted graphs,
develop incidence matrices, define the graph Laplacian, or discuss spectral or
electrical applications. Choosing edge orientations begins in CP229.

## Files

```text
engine/graph_walk_counting.py
scenes/graph_walk_counting_presentation.py
tests/test_graph_walk_counting.py
tests/test_graph_walk_counting_presentation.py
scripts/check_cp228_graph_walk_counting.zsh
scripts/render_cp228_graph_walk_counting.zsh
CHECKPOINT_228.md
apply_checkpoint_228.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp228_graph_walk_counting.zsh
scripts/render_cp228_graph_walk_counting.zsh
```

The render command produces only an uncached low-quality preview for review.
