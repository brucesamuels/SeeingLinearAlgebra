# Checkpoint 142 — The Adjugate and the Inverse Formula

## Purpose

CP142 unifies cofactors, invertibility, and Cramer's Rule by introducing the adjugate matrix and deriving the determinant formula
\[
A^{-1}=\frac{1}{\det(A)}\operatorname{adj}(A)
\]
for an invertible square matrix.

## Mathematical narrative

1. Start from the cofactor matrix \(C=[C_{ij}]\) and define the adjugate by
   \[
   \operatorname{adj}(A)=C^T.
   \]

2. Explain the matrix identity
   \[
   A\operatorname{adj}(A)=\det(A)I.
   \]
   The diagonal entries are cofactor expansions of \(\det(A)\). The off-diagonal entries are determinants of matrices with two equal rows, so they are zero.

3. When \(\det(A)\neq 0\), divide by the determinant to obtain
   \[
   A^{-1}=\frac{1}{\det(A)}\operatorname{adj}(A).
   \]

4. Work the concrete 2x2 example
   \[
   A=\begin{bmatrix}2&1\\5&3\end{bmatrix},\qquad \det(A)=1.
   \]
   Its cofactor matrix is
   \[
   \begin{bmatrix}3&-5\\-1&2\end{bmatrix},
   \]
   so
   \[
   \operatorname{adj}(A)=\begin{bmatrix}3&-1\\-5&2\end{bmatrix}
   \]
   and therefore
   \[
   A^{-1}=\begin{bmatrix}3&-1\\-5&2\end{bmatrix}.
   \]

5. Reconnect to Cramer's Rule via
   \[
   \mathbf x=A^{-1}\mathbf b=\frac{1}{\det(A)}\operatorname{adj}(A)\mathbf b.
   \]

## Files

- `engine/determinant_adjugate_inverse.py`
- `scenes/determinant_adjugate_inverse_presentation.py`
- `tests/test_determinant_adjugate_inverse.py`
- `tests/test_determinant_adjugate_inverse_presentation.py`
- `tests/test_cp142_scripts.py`
- `scripts/check_cp142_adjugate_inverse.zsh`
- `scripts/render_cp142_adjugate_inverse.zsh`

## Visual emphasis

The lesson is organized as a sequence of clean cards: define the adjugate, explain the identity, divide to get the inverse formula, verify a 2x2 example, then connect back to Cramer's Rule.


## Layout refinement R2

This refinement addresses crowding on the 2x2 example card and improves the balance of the closing takeaway card. The three matrices on the example card are reduced slightly, spaced more deliberately, and moved higher, while the inverse formula and verification product are reduced and separated into lower bands. On the final takeaway card, the main summary block and closing line are both shifted upward for a more balanced composition.


## Layout refinement R3

This refinement further resolves crowding on the 2x2 example card and raises the closing title on the takeaway card. The example title is raised and slightly reduced, all three 2x2 matrices and their labels are reduced further, the horizontal spacing is tightened in a controlled way, and the formula and product lines are scaled down so each occupies its own vertical band. On the final takeaway card, the yellow title is explicitly raised above the summary block to prevent overlap.


## Layout refinement R4

This refinement raises the yellow title on the 2x2 example card so the heading clears the blue label text below. The mathematical content of the card is unchanged; only the title position is adjusted upward for cleaner separation.


## Layout refinement R5

This refinement raises the yellow title on the 2x2 example card further to create better clearance above the blue label text. It also changes the opening subtitle from a plain Text object to a MathTex subtitle so the notation $A^{-1}$ renders correctly.


## Layout refinement R6

This refinement raises the yellow title on the final takeaway card further so the page has better vertical balance and more clearance above the summary content. The mathematical content is unchanged; only the title position on the closing card is adjusted upward.


## Layout refinement R7

This refinement raises the yellow title on the final takeaway card again so it sits closer to the midpoint between the chapter-banner band and the summary-content band. The mathematical content is unchanged; only the vertical placement of the closing title is adjusted for better visual balance.
