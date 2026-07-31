# Checkpoint 90 — Computing the Cross Product

## Purpose

Teach the coordinate computation of the cross product while preserving the
geometric meaning established in CP89.

The lesson uses the example

\[
\mathbf{u}=
\begin{bmatrix}
2\\
1\\
3
\end{bmatrix},
\qquad
\mathbf{v}=
\begin{bmatrix}
1\\
4\\
2
\end{bmatrix}.
\]

The computed result is

\[
\mathbf{u}\times\mathbf{v}
=
\begin{bmatrix}
-10\\
-1\\
7
\end{bmatrix}.
\]

## Pedagogical sequence

1. Present the two vectors.
2. Ask whether the perpendicular vector can be computed directly.
3. Introduce the formal determinant layout.
4. Expand one basis-vector component at a time.
5. Enlarge each relevant 2×2 minor while dimming the rest.
6. Emphasize the alternating sign on the \(\mathbf{j}\)-component.
7. Assemble the basis-vector form.
8. Transform it into coordinate-vector form.
9. Verify orthogonality with two dot products.
10. Return to the 3D geometry.

## Added files

- `engine/cross_product_computation.py`
- `scenes/cross_product_computation_presentation.py`
- `scripts/check_cp90_cross_product_computation.zsh`
- `scripts/render_cp90_cross_product_computation.zsh`
- `tests/test_cross_product_computation.py`
- `tests/test_cross_product_computation_presentation.py`

## Design principles

- Renderer-independent mathematics.
- Thin Manim presentation layer.
- One minor at a time.
- Geometry before and after computation.
- Standalone visual approval before chapter integration.
