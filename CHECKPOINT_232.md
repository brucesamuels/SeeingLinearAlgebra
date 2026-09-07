# Checkpoint 232 — Connected Components and the Laplacian Null Space

This checkpoint proves that the null space of a graph Laplacian records the
graph's connected components. A vector lies in `Null(L)` exactly when its vertex
values are constant on each connected component. Consequently,

```text
dim Null(L) = number of connected components.
```

## Numerical spine

Start with the recurring triangle-with-a-tail graph and remove the bridge
`{3,4}`. The remaining graph has components

```text
C1 = {1,2,3},    C2 = {4}
```

and Laplacian

```text
L_split = [ 2 -1 -1  0
           -1  2 -1  0
           -1 -1  2  0
            0  0  0  0 ].
```

Every componentwise-constant signal has the form

```text
x = (a,a,a,b)^T
  = a(1,1,1,0)^T + b(0,0,0,1)^T,
```

so the two component indicators form a basis for `Null(L_split)`. The original
connected graph has only the all-ones indicator and therefore nullity one.

## Story

1. Recall that zero energy on the connected recurring graph forces one global
   constant and gives `Null(L)=span{1}`.
2. Remove the bridge `{3,4}` and recover the two connected components first
   introduced in CP226.
3. Put value `a` on the triangle and `b` on the isolated vertex. Every remaining
   edge difference is zero even when `a` and `b` differ.
4. Multiply the block Laplacian structurally by `(a,a,a,b)^T` and obtain zero.
5. Build one indicator vector for each component.
6. Scale and add those indicators to produce every componentwise-constant null
   vector and identify a null-space basis.
7. Prove both directions of the general theorem using the energy identity and
   `L=B^T B`.
8. Compare the connected graph's nullity one with the split graph's nullity two.
9. State the component-nullity theorem and preview the first positive Laplacian
   eigenvalue.

## Architecture

`GraphLaplacianNullSpace` is renderer-independent. It composes the established
simple-graph, matrix-encoding, incidence, Laplacian, and energy models. It
exposes the ordered connected components, their indicator vectors, the
indicator matrix, componentwise-constant signals, and both sides of the
null-space characterization.

The scene continues the chapter's banner, title, heading, color, spacing, and
pacing conventions. Matrices are rendered structurally, and vertex numerals are
black for high contrast inside colored vertices.

## Scope boundary

This checkpoint characterizes the zero eigenspace without yet developing the
ordered Laplacian eigenvalues, spectral gap, Fiedler vector, spectral
partitioning, or electrical networks. The final card only previews the first
positive eigenvalue.

## Files

```text
engine/graph_laplacian_null_space.py
scenes/graph_laplacian_null_space_presentation.py
tests/test_graph_laplacian_null_space.py
tests/test_graph_laplacian_null_space_presentation.py
scripts/check_cp232_graph_laplacian_null_space.zsh
scripts/render_cp232_graph_laplacian_null_space.zsh
CHECKPOINT_232.md
apply_checkpoint_232.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp232_graph_laplacian_null_space.zsh
scripts/render_cp232_graph_laplacian_null_space.zsh
```

The render command produces only an uncached low-quality preview for review.
