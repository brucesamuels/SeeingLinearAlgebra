# Checkpoint 89 — The Cross Product

## Purpose

Introduce the cross product as a geometric operation on two vectors in
\(\mathbb{R}^3\) that produces a third vector perpendicular to both.

The lesson emphasizes three linked ideas:

1. Direction — the cross product points perpendicular to the plane containing
   the input vectors.
2. Magnitude — its length equals the area of the parallelogram spanned by the
   input vectors.
3. Orientation — reversing the order reverses the resulting vector.

## Pedagogical sequence

1. Begin with two vectors in a common plane.
2. Ask what kind of vector could describe both of them at once.
3. Reveal the parallelogram and its area.
4. Grow a perpendicular vector from the origin.
5. Rotate the camera so perpendicularity becomes visually unmistakable.
6. Reveal
   \[
   \|\mathbf{u}\times\mathbf{v}\|
   =
   \|\mathbf{u}\|\,\|\mathbf{v}\|\sin\theta.
   \]
7. Reverse the vector order and show
   \[
   \mathbf{v}\times\mathbf{u}
   =
   -(\mathbf{u}\times\mathbf{v}).
   \]
8. Conclude that the cross product measures oriented area.

## Added files

- `engine/cross_product.py`
- `scenes/cross_product_presentation.py`
- `scripts/check_cp89_cross_product.zsh`
- `scripts/render_cp89_cross_product.zsh`
- `tests/test_cross_product.py`
- `tests/test_cross_product_presentation.py`

## Design principles

- Renderer-independent mathematical engine.
- Thin Manim presentation layer.
- Geometry before formula.
- Standalone visual approval before chapter integration.
