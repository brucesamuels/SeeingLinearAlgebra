# Checkpoint 239 — The Fundamental Subspaces of a Graph

This checkpoint focuses exclusively on what the four fundamental subspaces of
the recurring graph's incidence matrix reveal about graph structure. It does
not revisit general matrix tests for consistency, uniqueness, one-to-one maps,
onto maps, invertibility, or least squares.

With the established edge-by-vertex convention,

```text
B : R^V -> R^E
```

sends vertex values to oriented edge differences. Its input-side subspaces
describe vertex structure; its output-side subspaces describe edge structure:

```text
Row(B)       balanced vertex contrasts
Null(B)      values constant on connected components
Col(B)       compatible edge differences (gradients)
Null(B^T)    conserved circulations around cycles.
```

## Exact incidence spine

Retain the recurring orientation

```text
e1: 1 -> 2
e2: 2 -> 3
e3: 1 -> 3
e4: 3 -> 4
```

and incidence matrix

```text
    [-1  1  0  0]
B = [ 0 -1  1  0]
    [-1  0  1  0]
    [ 0  0 -1  1].
```

The graph has `n=4` vertices, `m=4` edges, and `c=1` connected component, so

```text
rank(B)        = n-c     = 3
dim Null(B)    = c       = 1
dim Null(B^T)  = m-n+c   = 1.
```

The vertex null space is

```text
Null(B)=span{(1,1,1,1)^T}.
```

Deleting the bridge `{3,4}` creates two components and gives the two component
indicators `(1,1,1,0)^T` and `(0,0,0,1)^T`. Thus the nullity rises from one to
two while the triangle cycle remains.

The row space is the orthogonal complement of the component constants. For the
connected graph,

```text
Row(B)=1^perp={z in R^4 : z1+z2+z3+z4=0}.
```

## Edge space: gradients and cycles

For the familiar vertex values `x=(1,2,3,4)^T`,

```text
Bx=(1,1,2,1)^T.
```

The first three coordinates satisfy the triangle consistency condition

```text
(x2-x1)+(x3-x2)-(x3-x1)=0,
```

so every vector in `Col(B)` has `y1+y2-y3=0`. These are compatible edge
differences: they can be obtained from a set of vertex values.

The vector

```text
q=(1,1,-1,0)^T
```

satisfies `B^T q=0`. Relative to the stored edge orientations, it sends one unit
around the triangle and creates no net accumulation at any vertex. Therefore

```text
Null(B^T)=span{q}
```

is the one-dimensional cycle space for the recurring graph. Deleting a triangle
edge leaves a connected tree, so the component nullity remains one while the
left nullity—and the independent cycle count—falls to zero.

## Laplacian consequence

Because `L=B^T B` is symmetric,

```text
Null(L) = Null(B),
Col(L)  = Row(B).
```

For the connected recurring graph,

```text
Null(L)=span{1},
Col(L)=1^perp.
```

Consequently,

```text
Lv=b is solvable  iff  1^T b=0.
```

This is the balanced-injection condition from the electrical-network lesson.
If one solution exists, adding a constant multiple of `1` gives another, which
explains the need to ground one vertex.

## Story

1. Place the four subspaces around `B:R^V -> R^E` and identify which describe
   vertex data and which describe edge data.
2. Interpret `Null(B)` as values constant on the connected graph.
3. Delete the bridge and show one null direction per connected component.
4. Interpret `Row(B)=Null(B)^perp` as balanced vertex contrasts.
5. Interpret `Col(B)` as cycle-consistent edge differences.
6. Interpret `Null(B^T)` as conserved circulation around the triangle.
7. Use the incidence dimension formulas to compare the recurring graph, the
   split graph, and a connected tree.
8. Decompose vertex data into contrasts plus component constants and edge data
   into gradients plus circulations.
9. Show how `L=B^T B` inherits the vertex-side incidence subspaces.
10. Use those spaces to explain solvability and nonuniqueness of `Lv=b`.

## Architecture

`GraphFundamentalSubspaces` is renderer-independent and composes the established
graph, incidence, and Laplacian models. It computes incidence rank, nullities,
component count, cycle rank, component indicators, edge differences, vertex
accumulations, component balance, edge-difference compatibility, gradient and
circulation components, edge-deletion comparisons, and Laplacian reachability.

The Manim scene retains the chapter's banner, title, heading, colors, spacing,
and pacing. Temporary incidence orientations remain bookkeeping devices, cycle
arrows are visually distinguished, matrices are structural, and vertex numerals
remain black inside yellow vertices.

## Scope boundary

This lesson uses only the recurring unweighted undirected graph and its incidence
and Laplacian matrices. It does not repeat the earlier general fundamental-
subspaces lesson, introduce weighted graphs, develop a full cut-space theory,
or add homology terminology. The next checkpoint will synthesize the complete
graph chapter.

## Files

```text
engine/graph_fundamental_subspaces.py
scenes/graph_fundamental_subspaces_presentation.py
tests/test_graph_fundamental_subspaces.py
tests/test_graph_fundamental_subspaces_presentation.py
scripts/check_cp239_graph_fundamental_subspaces.zsh
scripts/render_cp239_graph_fundamental_subspaces.zsh
CHECKPOINT_239.md
apply_checkpoint_239.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp239_graph_fundamental_subspaces.zsh
scripts/render_cp239_graph_fundamental_subspaces.zsh
```

The render command produces only an uncached low-quality preview for review.
