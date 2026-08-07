# Checkpoint 134 - Determinants and Elimination

## Purpose

Build the next determinant lesson around **elimination as a determinant-computation tool**.
The scene remains connected to the running determinant sequence by keeping the banner:

**Properties of the Determinant**

but now uses those properties to compute a determinant through elimination.

## Mathematical narrative

We first recall four key rules:

1. swapping two rows changes the sign;
2. scaling a row multiplies the determinant by the scale factor;
3. adding a multiple of one row to another leaves the determinant unchanged;
4. the determinant of a triangular matrix is the product of the diagonal entries.

We then apply elimination to

\[
A=\begin{bmatrix}
0&2&1\\
1&1&0\\
2&3&4
\end{bmatrix}
\]

with the sequence

- `r1 <-> r2`
- `r2 -> (1/2) r2`
- `r3 -> r3 - 2r1`
- `r3 -> r3 - r2`

This produces an upper triangular matrix

\[
U=\begin{bmatrix}
1&1&0\\
0&1&\tfrac12\\
0&0&\tfrac72
\end{bmatrix}
\]

so

\[
\det(U)=1\cdot 1\cdot \tfrac72=\tfrac72.
\]

Because the cumulative determinant factor is `-1/2`,

\[
\det(U)=-\tfrac12\det(A),
\]

and therefore

\[
\det(A)=-7.
\]

## Files

- `engine/determinant_elimination.py`
- `scenes/determinant_elimination_presentation.py`
- `tests/test_determinant_elimination.py`
- `tests/test_determinant_elimination_presentation.py`
- `scripts/check_cp134_determinant_elimination.zsh`
- `scripts/render_cp134_determinant_elimination.zsh`
- `CHECKPOINT_134.md`

## Install

Assuming Safari unzips automatically, run from the repository root:

```zsh
cd "/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
zsh ~/Downloads/seeing_linear_algebra_cp134/apply_checkpoint_134.zsh
```

## Check

```zsh
zsh scripts/check_cp134_determinant_elimination.zsh
```

## Render

Preview:

```zsh
zsh scripts/render_cp134_determinant_elimination.zsh -pql
```

High quality after approval:

```zsh
zsh scripts/render_cp134_determinant_elimination.zsh -pqh
```


## Refinement notes

This revision clarifies that the product of the pivots gives the determinant of the resulting triangular matrix `U`, not immediately the determinant of the original matrix `A`. The scene now explicitly states that row swaps and row scalings must be undone to recover `det(A)`.

It also resolves layout crowding by giving the opening rule card more breathing room and by reorganizing the elimination snapshots into a two-row layout so the matrices do not overlap each other.


## Focused spacing refinement

This revision addresses two previewed collisions: on the example setup card, the matrix is moved further left and the Goal block further right; on the step-by-step elimination card, the first three step snapshots are raised and the last two lowered slightly so the two rows of matrices do not collide.


## Focused title/text refinement

This revision raises the "Step-by-step elimination" title to clear the upper row of matrices more comfortably. It also increases the font size of the symbolic row-operation lines at the bottom of that card as much as possible while preserving separation from the matrix layouts.


## Verified step-title revision R2

The prior package accidentally raised the overview title rather than the Step-by-step elimination title. This revision corrects the specific step-card title to y=2.75 and visibly enlarges the three symbolic lines to font sizes 28, 28, and 26.


## Matrix-label refinement

This revision nudges the step labels ("Start", "Step 1", etc.) upward on the step-by-step elimination card so they clear the matrix entries more comfortably.


## Step-card redesign

This revision redesigns the step-by-step elimination card. Each condensed 3x3 matrix is now immediately followed by the symbolic elimination step and then by a note describing the determinant change. The five stages are arranged in a three-over-two layout so the viewer can read each local elimination move in sequence without a separate bottom legend.


## Flow-diagram redesign

This revision converts the step-by-step elimination card into a true flow diagram. The symbolic row operation and the determinant effect now live in the gaps between successive matrices, with arrows indicating the direction of the elimination sequence. To make room, the matrices are tightened internally using reduced matrix buffers, and the row-operation fonts are made larger for easier reading.


## Flow-diagram spacing refinement

This refinement pulls the symbolic row-operation blocks farther away from the matrices so the flow diagram reads cleanly. The successive matrices are spaced farther apart, the transition annotations are split into more compact stacks, and every visible element is made slightly larger so the card is better filled without crowding.


## Balanced flow-diagram redesign

This refinement spreads the matrices farther apart and restructures the step card into an alternating flow: matrix, arrow, symbolic row reduction, arrow, next matrix. The path now runs across the top row, down the right side, and back across the bottom row, creating a balanced snake-style diagram that uses the full card more effectively.


## Single-arrow flow redesign

This refinement restructures the step card into a clearer alternating sequence: matrix, arrow, symbolic row reduction, next matrix. Only one arrow is used for each transition, and the matrices are spread farther apart so the reduction text has more room to breathe. The overall path still runs across the top, down the right, and back across the bottom.


## Title and arrow refinement

This refinement raises the step-card title slightly, lowers the transition from Step 2 to Step 3, and extends the transition arrows so the flow between stages reads more clearly. The vertical transition annotation is also nudged down to stay centered on the longer arrow.


## Arrow-position refinement

This refinement shifts both top horizontal transition arrows to the right so they sit more clearly between the matrices, lowers the vertical Step 2 to Step 3 transition to clear the symbolic text, and shifts the Step 3 to Step 4 transition left while moving Step 4 slightly right to close the lower gap.


## Symmetry and readability refinement

This refinement rebuilds the step-by-step card around a more symmetric layout: the top and bottom row matrices are evenly spaced, the lower row mirrors the upper row, and the transition annotations are offset from the arrows rather than sitting directly on top of them. The symbolic row-operation text and determinant notes are also enlarged for easier reading while preserving clearance from the matrices.


## Step-card relayout after video review

After inspecting the rendered preview, this revision re-lays out the step-by-step card more aggressively. The matrices are reduced slightly and spread more evenly, and each row-operation text block is separated from its arrow and from nearby matrices so the symbolic text remains readable. The lower row is aligned symmetrically with the upper row, and the vertical transition is pushed to the right of the matrices to prevent direct overlap.


## R13 spacing nudges

This refinement nudges the two top-row symbolic row-reduction blocks and their determinant notes to the left to clear the matrices, while nudging the bottom-row symbolic row-reduction block and determinant note to the right. The vertical transition and all arrows remain unchanged.


## R14 larger spacing nudges

The same directional adjustment is repeated more strongly so it is visually obvious: both top-row row-operation/determinant blocks move farther left, while the bottom-row row-operation/determinant block moves farther right. The arrows and vertical transition remain unchanged.


## R15 larger-elements refinement

This revision preserves the R14 spacing and positions while enlarging all visible elements on the step-by-step card: title, step labels, matrices, row-operation text, determinant notes, and arrow weight.


## R16 step-2 right nudge

This refinement nudges the Step 2 matrix and its label to the right, and moves the associated vertical row-reduction text and determinant note to the right as well, to reduce collisions with the left-side elements. Arrow positions remain unchanged.
