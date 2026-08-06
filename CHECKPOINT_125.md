# Checkpoint 125: Rectangular Matrices and the Geometry of `Ax = b`

## Purpose

Extend the linear-systems chapter from square matrices to the general map

\[
A:\mathbb{R}^n\longrightarrow\mathbb{R}^m.
\]

The lesson distinguishes the number of equations from the number of unknowns,
then connects matrix shape, rank, column space, null space, reachability, and
uniqueness.

## Central dimension statement

\[
A_{m\times n}\mathbf{x}_{n\times1}=\mathbf{b}_{m\times1}.
\]

Thus:

- the `m` rows represent `m` equations and output coordinates;
- the `n` columns represent `n` unknowns and input coordinates;
- `A` maps inputs in \(\mathbb R^n\) to outputs in \(\mathbb R^m\).

## Three matrix shapes

The presentation compares:

\[
m=n \quad\text{(square)},
\qquad
m>n \quad\text{(tall or overdetermined)},
\qquad
m<n \quad\text{(wide or underdetermined)}.
\]

Shape alone does not determine consistency.

## Column-space criterion

Writing the product by columns gives

\[
A\mathbf{x}
=x_1\mathbf{a}_1+\cdots+x_n\mathbf{a}_n.
\]

Therefore

\[
A\mathbf{x}=\mathbf{b}
\text{ is solvable}
\iff
\mathbf{b}\in\operatorname{Col}(A).
\]

The row-reduction version of the same condition is

\[
\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b]).
\]

## Rank and nullity

\[
r=\operatorname{rank}(A)\le\min(m,n),
\qquad
\dim N(A)=n-r.
\]

Rank counts independent reachable directions in the output space.  Nullity
counts input directions that collapse to zero.

## Full-rank geometry

### Tall matrix

For a full-column-rank map \(\mathbb R^2\to\mathbb R^3\):

- the image is a plane in the three-dimensional output space;
- the map may be one-to-one;
- it cannot be onto;
- a reachable right-hand side has at most one solution.

### Wide matrix

For a full-row-rank map \(\mathbb R^3\to\mathbb R^2\):

- every output can be reached;
- the null space has positive dimension;
- several inputs differing by a null vector map to the same output;
- a consistent system cannot have a unique solution.

### Square matrix

A full-rank square map can be both onto and one-to-one, so every right-hand
side has exactly one solution.

## Important cautions

- Overdetermined does not automatically mean inconsistent.
- Underdetermined does not automatically mean consistent.
- The shape gives rank limits; the actual rank and the position of \(\mathbf b\)
  determine the solution set.

## Replacing the former assembly checkpoint

The earlier, uncommitted CP125 assembly source is intentionally removed by the
installer.  The rendered chapter media is left untouched, and the assembly work
will return after the two rectangular-system lessons.

## Files

- `engine/rectangular_matrices.py`
- `scenes/rectangular_matrices_presentation.py`
- `tests/test_rectangular_matrices.py`
- `tests/test_rectangular_matrices_presentation.py`
- `scripts/check_cp125_rectangular_matrices.zsh`
- `scripts/render_cp125_rectangular_matrices.zsh`

## Run focused checks

```zsh
./scripts/check_cp125_rectangular_matrices.zsh
```

## Render

```zsh
./scripts/render_cp125_rectangular_matrices.zsh
```

## Visual review

Check especially:

- the square/tall/wide matrix cards;
- the column-space diagram and its reachable and unreachable points;
- the rank/nullity panel;
- the tall-map image plane;
- the wide-map null-space family;
- the final full-rank comparison.

## Revised package note

The rectangular-matrices revised package removes an invalid repository test that
looked for the package-only installer in the repository root. It also fixes the
zsh rollback handler by avoiding the read-only `status` variable and disabling
traps before restoration.


## Revised 2

Explicitly fades all red, green, and yellow highlight rectangles with their associated panels so they do not persist over later scenes. Added regression tests for highlight lifecycle.


## Revised 3

Replaces the custom two-line arrowhead, which could resemble an `x`, with a standard Manim arrow. Each map arrow is now constructed directly between the facing edges of its input and output boxes, so it remains centered even when the boxes have different widths. The arrow is labeled `A` and `x maps to b`. The square full-rank statement now says in words that every output has exactly one input instead of using the less familiar symbol `exists!`.
