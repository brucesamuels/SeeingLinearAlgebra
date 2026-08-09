# Checkpoint 143 — Determinants of Products

## Central theorem

For square matrices of the same size,
\[
\det(AB)=\det(A)\det(B).
\]

## Proof strategy

The proof is built from elementary row operations.

### Step 1: elementary left factor
If \(E\) is elementary, then left multiplication \(EB\) performs the corresponding row operation on \(B\).

- Row interchange gives \(\det(E)=-1\) and \(\det(EB)=-\det(B)\).
- Row scaling by \(c\) gives \(\det(E)=c\) and \(\det(EB)=c\det(B)\).
- Row replacement gives \(\det(E)=1\) and \(\det(EB)=\det(B)\).

Therefore in all three cases,
\[
\det(EB)=\det(E)\det(B).
\]

### Step 2: invertible A
If \(A\) is invertible, then
\[
A=E_mE_{m-1}\cdots E_1.
\]
Hence
\[
AB=E_mE_{m-1}\cdots E_1B.
\]
Repeatedly applying the elementary-matrix result gives
\[
\det(AB)=\det(E_m)\cdots\det(E_1)\det(B).
\]
But
\[
\det(A)=\det(E_m)\cdots\det(E_1),
\]
so
\[
\det(AB)=\det(A)\det(B).
\]

### Step 3: singular A
If \(A\) is singular, then \(\det(A)=0\). Also,
\[
\operatorname{rank}(AB)\leq\operatorname{rank}(A)<n,
\]
so \(AB\) is singular and \(\det(AB)=0\). Thus
\[
\det(AB)=0=\det(A)\det(B).
\]

## Consequences

\[
\det(A^{-1})=\frac{1}{\det(A)},
\qquad
\det(A^k)=\det(A)^k,
\]
and
\[
\det(A_1A_2\cdots A_m)
=
\det(A_1)\det(A_2)\cdots\det(A_m).
\]

## Files

- `engine/determinant_product_rule.py`
- `scenes/determinant_product_rule_presentation.py`
- `tests/test_determinant_product_rule.py`
- `tests/test_determinant_product_rule_presentation.py`
- `tests/test_cp143_scripts.py`
- `scripts/check_cp143_determinant_products.zsh`
- `scripts/render_cp143_determinant_products.zsh`


## Layout refinement R2

This refinement reduces text collisions across several cards in the determinant product lesson. The elementary-matrix card uses smaller row entries and tighter spacing, the invertible-case card reduces formula sizes and separates the top and bottom bands more clearly, the singular-case card uses a slightly more compact stack, and the consequences card is redesigned from a side-by-side layout into a vertically stacked layout to give the long many-factors formula more room. The closing takeaway card also uses slightly smaller note text and a slightly higher theorem position.


## Layout refinement R3

This refinement targets the cards most prone to persistent collisions in preview renders: the invertible case, the singular case, and the consequences card. On the invertible-case card, the title and formula lines are reduced slightly and the two text bands are separated more clearly. On the singular-case card, all four lines are reduced and the body stack is moved lower. On the consequences card, the content is split into three separate vertical blocks -- inverse, powers, and many factors -- so each consequence gets its own dedicated space without crowding.


## Layout refinement R4

This refinement targets the persistent collisions on the invertible-matrix card around the mid-20-second mark in preview renders. The yellow title is reduced again, the two upper factorization lines are reduced slightly and kept in a tighter top band, and the long determinant-chain step is split across two separate green lines so the product of determinant factors no longer runs through the right edge or into neighboring text.


## Proof-structure redesign R5

This refinement rebuilds the invertible-matrix portion of the proof into three separate cards so the logic is readable rather than compressed into one dense screen. The first new card states the factorization of an invertible matrix into elementary matrices and then applies it to AB. The second card peels off one elementary matrix at a time to show how determinant factors accumulate. The third card identifies the accumulated product with det(A) and then concludes det(AB)=det(A)det(B). This matches the pedagogical proof structure discussed in chat and is intended to eliminate the visual clutter on the former invertible-matrix card.


## Layout refinement R6

This refinement raises the subheading on the first invertible-matrix proof card so the line "Now suppose A is invertible" clears the formulas below it more comfortably. The mathematical content is unchanged; only the vertical placement of that subheading is adjusted upward.


## Layout refinement R7

This refinement raises the subheading on the first invertible-matrix proof card even further so the line "Now suppose A is invertible" sits more comfortably above the formulas. The mathematical content is unchanged; only the subheading position is adjusted upward again.
