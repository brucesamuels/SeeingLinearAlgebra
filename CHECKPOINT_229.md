# Checkpoint 229 — The Incidence Matrix: Edges Meet Vertices

This checkpoint introduces an edge-by-vertex incidence matrix for the recurring
undirected graph. A temporary orientation assigns each edge a tail and a head
without turning the graph into a directed graph. Each incidence row records
`-1` at its tail, `+1` at its head, and zero at every other vertex. Acting on
vertex values, `B*x` returns head-minus-tail differences along the oriented
edges.

## Numerical spine

Use the vertex order `(1,2,3,4)` and oriented edge order

```text
e1: 1 -> 2
e2: 2 -> 3
e3: 1 -> 3
e4: 3 -> 4.
```

Then

```text
B = [[-1, 1, 0, 0],
     [ 0,-1, 1, 0],
     [-1, 0, 1, 0],
     [ 0, 0,-1, 1]].
```

For the recurring vertex values `x=(1,2,3,4)`,

```text
B*x = (1,1,2,1).
```

Reversing `e3` negates only row 3 of `B` and changes its edge difference from
`2` to `-2`. The undirected edge and the magnitude of its difference do not
change. Because every row sums to zero, `B*1=0`.

## Story

1. Add temporary arrows to the undirected graph and emphasize that they are
   bookkeeping choices rather than new directed edges.
2. Choose an edge order for rows and retain the vertex order for columns;
   explain that an incidence matrix is generally `m` edges by `n` vertices.
3. Build the first row from the tail, head, and non-endpoints of `e1`.
4. Activate each oriented edge and reveal `B` one structural row at a time.
5. Read a row as one edge and a column as one vertex's roles across all edges.
6. Attach the familiar values `(1,2,3,4)` to the vertices and derive
   `(B*x)_3=x_3-x_1=2` as a concrete endpoint comparison.
7. Compute all four oriented edge differences in one matrix-vector product.
8. Reverse `e3` and show that its row and output difference change sign while
   the underlying graph remains fixed.
9. Synthesize the matrix shape and action, show `B*1=0`, and ask what happens
   when `B^T` sends edge differences back to vertices.

## Architecture

`GraphIncidenceEncoding` is renderer-independent and composes CP227's
`GraphMatrixEncoding`. It validates that every undirected edge receives exactly
one orientation, constructs the edge-by-vertex incidence matrix, extracts
individual edge rows, computes oriented edge differences, and returns a new
encoding with one chosen edge reversed. The scene owns all rendering, labels,
arrows, and layout. Vertex numerals use black against yellow, orange, and teal
vertex fills for strong contrast at preview resolution.

## Scope boundary

This checkpoint does not reinterpret the graph as directed, introduce weighted
incidence matrices, define the graph Laplacian, prove orientation independence
of `B^T B`, or discuss energy, connected components, spectra, or electrical
networks. The incidence-transpose composition begins in CP230.

## Files

```text
engine/graph_incidence_encoding.py
scenes/graph_incidence_encoding_presentation.py
tests/test_graph_incidence_encoding.py
tests/test_graph_incidence_encoding_presentation.py
scripts/check_cp229_graph_incidence_encoding.zsh
scripts/render_cp229_graph_incidence_encoding.zsh
CHECKPOINT_229.md
apply_checkpoint_229.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp229_graph_incidence_encoding.zsh
scripts/render_cp229_graph_incidence_encoding.zsh
```

The render command produces only an uncached low-quality preview for review.
