# Checkpoint 133 - Consequences of the Determinant Properties

## Purpose

Continue the running determinant sequence by deriving consequences from the foundational properties established in CP132.
Every screen remains clearly inside the context:

**Properties of the Determinant**

This checkpoint adds four consequences:

4. Equal rows imply determinant zero.
5. A zero row implies determinant zero.
6. Adding a multiple of one row to another leaves the determinant unchanged.
7. Dependent rows imply determinant zero.

The lesson ends with a summary card connecting these facts to elimination, triangular matrices, and invertibility.

## Mathematical narrative

### Property 4
If two rows are equal, swapping them changes the sign of the determinant but not the matrix itself. Therefore the determinant equals its own negative, so it must be zero.

### Property 5
A zero row implies determinant zero because additivity gives

`D(0,r2)=D(0+0,r2)=D(0,r2)+D(0,r2)`.

### Property 6
Adding a multiple of one row to another leaves the determinant unchanged because

`D(r1+kr2,r2)=D(r1,r2)+kD(r2,r2)=D(r1,r2)`.

### Property 7
If one row depends on the other, the matrix cannot create two-dimensional area, so the determinant is zero.

## Files

- `engine/determinant_consequences.py`
- `scenes/determinant_consequences_presentation.py`
- `tests/test_determinant_consequences.py`
- `tests/test_determinant_consequences_presentation.py`
- `scripts/check_cp133_determinant_consequences.zsh`
- `scripts/render_cp133_determinant_consequences.zsh`
- `CHECKPOINT_133.md`

## Install

Assuming Safari unzips automatically, run from the repository root:

```zsh
cd "/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
zsh ~/Downloads/seeing_linear_algebra_cp133/apply_checkpoint_133.zsh
```

## Check

```zsh
zsh scripts/check_cp133_determinant_consequences.zsh
```

## Render

Preview:

```zsh
zsh scripts/render_cp133_determinant_consequences.zsh -pql
```

High quality after approval:

```zsh
zsh scripts/render_cp133_determinant_consequences.zsh -pqh
```


## Layout refinement

This revision focuses on Property 6. The long yellow property title is split into two lines and raised slightly. The two matrix displays and the row-operation label are moved upward, while the determinant readouts and derivation are repositioned lower to reduce collisions with the graphics.


## Layout refinement v2

This second refinement makes more visible changes. Property 4 redistributes the right-side matrix and symbolic statements vertically across the frame. Property 6 is restructured more aggressively: the matrices sit farther apart, the graphs are smaller and lower, the determinant readouts sit directly under each graph, and the derivation is compressed into two centered lines at the bottom.


## Focused spacing refinement

This revision lowers the matrix and determinant statements on Property 4 to clear the yellow property heading more comfortably. It also raises the yellow Property 6 title so it no longer crowds the two matrix displays.
