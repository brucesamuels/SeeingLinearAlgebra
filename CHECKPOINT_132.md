# Checkpoint 132 - Foundational Properties of the Determinant

## Purpose

Continue the determinant chapter by **enumerating the determinant properties** in a clearly labeled sequence.
Every screen stays inside the same running context:

**Properties of the Determinant**

This checkpoint presents four screens inside that sequence:

1. `det(I)=1`
2. Swapping two rows changes the sign.
3. Scaling one row scales the determinant.
4. The determinant is additive in one row.

The lesson ends with a summary card that gathers the properties so far and points ahead to further consequences.

## Mathematical narrative

### Property 1
The identity matrix leaves the unit square unchanged, so

`det(I)=1`.

### Property 2
A row swap preserves area magnitude but reverses orientation, so the determinant changes sign.

### Property 3a
Multiplying one row by `k` multiplies the determinant by `k`.

### Property 3b
If one row splits as `u+s`, then the determinant splits as a sum:

`D(u+s,r2)=D(u,r2)+D(s,r2)`, illustrated numerically by `2+1=3`.

## Files

- `engine/determinant_properties.py`
- `scenes/determinant_properties_presentation.py`
- `tests/test_determinant_properties.py`
- `tests/test_determinant_properties_presentation.py`
- `scripts/check_cp132_determinant_properties.zsh`
- `scripts/render_cp132_determinant_properties.zsh`
- `CHECKPOINT_132.md`

## Install

Assuming Safari unzips automatically, run from the repository root:

```zsh
cd "/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
zsh ~/Downloads/seeing_linear_algebra_cp132/apply_checkpoint_132.zsh
```

## Check

```zsh
zsh scripts/check_cp132_determinant_properties.zsh
```

## Render

Preview:

```zsh
zsh scripts/render_cp132_determinant_properties.zsh -pql
```

High quality after approval:

```zsh
zsh scripts/render_cp132_determinant_properties.zsh -pqh
```


## Refinement notes

This refinement removes the persistent subtitle after the opening context card to create more vertical space. Property 2 now shows the row-swap effect as a reflected parallelogram, with a dashed `y=x` reflection guide.


## Property-card refinement

This revision separates the determinant formulas beneath Properties 2 and 3a into left and right cards under the corresponding graphics, reducing bottom overlap. Property 3b increases the size of the additivity formulas and explicitly shows the concluding `2+1=3` line.


## Visual refinement

This refinement changes the red determinant under Property 2 to a side-by-side layout, separating the determinant expression from the value `=-3` to reduce crowding. It also increases the formula sizes in Property 3b substantially so the additivity rule reads more clearly on screen.


## Focused layout adjustment

This refinement moves the small red determinant display in Property 2 lower on the card to avoid collision. It also increases the font size of the smaller introductory formulas in Property 3b (`r_1=u+s`, `u=(1,0), s=(1,1)`, and `r_2=(1,2)`).


## Verified R3 refinement

This refinement lowers the left determinant display in Property 2 to match the successful right-side placement. It also nudges the Property 3a yellow heading upward and moves both scaling matrices upward to improve clearance above the graphics.
