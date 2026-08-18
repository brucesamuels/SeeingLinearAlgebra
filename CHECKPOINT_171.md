# Checkpoint 171 — Why the Characteristic Equation Appears

## Purpose

Rebuild the lesson around the algebra that connects the eigenvector definition to the characteristic equation. The identity matrix is introduced explicitly so students can see why matrix subtraction is legitimate, and the familiar 2x2 determinant rule is then animated rather than skipped.

## Student-facing arc

1. Start from the definition
   `A v = lambda v`, with `v != 0`.
2. Use `I v = v` to rewrite the right side as
   `lambda I v`.
3. Move both matrix terms to one side:
   `A v - lambda I v = 0`.
4. Factor the common vector:
   `(A - lambda I)v = 0`.
5. Recall that a nonzero solution of a homogeneous system requires the coefficient matrix to be singular, hence
   `det(A - lambda I) = 0`.
6. Name this determinant equation as the characteristic equation.
7. For `A=[[5,3],[3,5]]`, build
   `lambda I=[[lambda,0],[0,lambda]]`
   and subtract entry-by-entry to get
   `A-lambda I=[[5-lambda,3],[3,5-lambda]]`.
8. Review the ordinary 2x2 determinant rule `ad-bc` and animate the two diagonal products:
   `(5-lambda)(5-lambda) - 3*3`.
9. Simplify, expand, factor, and solve:
   `(5-lambda)^2-9=0`
   -> `lambda^2-10lambda+16=0`
   -> `(lambda-2)(lambda-8)=0`
   -> `lambda=2,8`.
10. Close with the full bridge:
    `Av=lambda v -> (A-lambda I)v=0 -> det(A-lambda I)=0`.

## Pedagogical intent

The lesson no longer relies on geometric rank-collapse imagery as its primary explanation. Instead, every algebraic move is motivated and animated. In particular, the role of the identity matrix is made explicit, and the 2x2 determinant is computed using the same `ad-bc` procedure students already know from the determinant chapter.

## Layout discipline

- Fixed 2D camera with no coordinate grid; this is an algebra-focused lesson.
- One conceptual move per card.
- The identity-matrix explanation gets its own card rather than being hidden inside a formula.
- Matrix subtraction is shown before the simplified shifted matrix.
- The determinant rule `ad-bc` appears beside the concrete determinant before simplification.
- Long equation stacks use deliberate vertical spacing and generous safety margins.
- Bottom captions remain short and separate from the main mathematics.

## Files

- `engine/characteristic_equation.py`
- `scenes/characteristic_equation_presentation.py`
- `tests/test_characteristic_equation.py`
- `tests/test_characteristic_equation_presentation.py`
- `scripts/check_cp171_characteristic_equation.zsh`
- `scripts/render_cp171_characteristic_equation.zsh`
- `CHECKPOINT_171.md`

## Commands

```zsh
zsh scripts/check_cp171_characteristic_equation.zsh
zsh scripts/render_cp171_characteristic_equation.zsh
```
