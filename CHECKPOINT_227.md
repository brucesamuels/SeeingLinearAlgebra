# Checkpoint 227 — Adjacency and Degree Matrices: From Picture to Array

This checkpoint gives the recurring four-vertex graph its first algebraic
representation. After choosing a common vertex order for rows and columns, the
adjacency matrix records direct connections with zeros and ones. Row sums recover
the vertex degrees, and the degree matrix stores those counts diagonally.

## Numerical spine

For the vertex order `(1,2,3,4)`, use

```text
A = [[0,1,1,0],
     [1,0,1,0],
     [1,1,0,1],
     [0,0,1,0]]

d = [2,2,3,1]

D = [[2,0,0,0],
     [0,2,0,0],
     [0,0,3,0],
     [0,0,0,1]].
```

Because the graph is undirected, `A` is symmetric. Because it is simple and has
no loops, the diagonal entries are zero. The row sums of `A` equal `d`, so
`A*1=d=D*1`.

For the vertex signal `x=(1,2,3,4)`,

```text
A*x = (5,4,7,3).
```

Each output coordinate is the sum of the values at one vertex's neighbors.

## Story

1. Revisit the closing CP226 question: use one for a direct edge and zero otherwise.
2. Choose the same vertex order for the rows and columns.
3. Define `a_ij`, activate each vertex in turn, flash its incident connections,
   and reveal its labeled adjacency row after a short beat.
4. Accumulate all four rows into the completed adjacency matrix, then interpret
   row 3 explicitly.
5. Connect undirected edges to symmetry and the absence of loops to a zero diagonal.
6. Add each row to recover the degree vector `(2,2,3,1)`.
7. Place those degrees on the diagonal of `D`, define the all-ones vector, and
   explain that multiplying by it adds each row before showing `A*1=d=D*1`.
8. Apply `A` to `x=(1,2,3,4)` and interpret the result as neighbor sums.
9. Finish with `A`, `D`, and `A*x` as three readings of the same graph.

## Architecture

`GraphMatrixEncoding` is renderer-independent and composes the CP226
`SimpleUndirectedGraph`. It validates a vertex ordering and provides adjacency
entries, the adjacency matrix, row sums, the degree vector, the degree matrix,
and neighbor-sum multiplication. The scene uses structural Manim `Matrix`
objects for every displayed array.

## Scope boundary

This checkpoint does not introduce powers of the adjacency matrix, walk-counting
theorems, directed or weighted adjacency matrices, incidence matrices, the graph
Laplacian, eigenvalues, or electrical networks. Matrix powers begin in CP228.

## Files

```text
engine/graph_matrix_encoding.py
scenes/graph_matrix_encoding_presentation.py
tests/test_graph_matrix_encoding.py
tests/test_graph_matrix_encoding_presentation.py
scripts/check_cp227_graph_matrix_encoding.zsh
scripts/render_cp227_graph_matrix_encoding.zsh
CHECKPOINT_227.md
apply_checkpoint_227.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp227_graph_matrix_encoding.zsh
scripts/render_cp227_graph_matrix_encoding.zsh
```

The render command produces only an uncached low-quality preview for review.
