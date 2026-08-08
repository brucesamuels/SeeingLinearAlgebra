# Checkpoint 141 — Cramer's Rule

## Purpose

CP141 introduces Cramer's Rule as a consequence of determinant linearity, rather than as a formula to memorize.

## Mathematical narrative

Write

\[
A=[\mathbf a_1\ \mathbf a_2\ \cdots\ \mathbf a_n],
\qquad
A\mathbf x=\mathbf b,
\]

so that

\[
x_1\mathbf a_1+\cdots+x_n\mathbf a_n=\mathbf b.
\]

Let \(A_k\) be the matrix obtained by replacing column \(k\) of \(A\) by \(\mathbf b\). By linearity of the determinant in that column,

\[
\det(A_k)
=
\det(\mathbf a_1,\ldots,\mathbf b,\ldots,\mathbf a_n)
=
\det\left(\mathbf a_1,\ldots,\sum_j x_j\mathbf a_j,\ldots,\mathbf a_n\right).
\]

All terms except the \(x_k\) term have a repeated column and therefore determinant zero. Hence

\[
\det(A_k)=x_k\det(A).
\]

If \(\det(A)\neq0\),

\[
\boxed{x_k=\frac{\det(A_k)}{\det(A)}}.
\]

## Numerical example

\[
\begin{bmatrix}
1&2&0\\
0&1&1\\
2&0&1
\end{bmatrix}
\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix}
=
\begin{bmatrix}0\\2\\7\end{bmatrix}.
\]

Here

\[
\det(A)=5,
\quad
\det(A_1)=10,
\quad
\det(A_2)=-5,
\quad
\det(A_3)=15,
\]

so

\[
(x_1,x_2,x_3)=(2,-1,3).
\]

## Teaching emphasis

- Cramer's Rule depends on \(\det(A)\neq0\), so the system has a unique solution.
- The replacement determinant isolates one coordinate because the other multilinear terms contain repeated columns.
- Cramer's Rule is conceptually elegant and useful for formulas or small systems, but elimination is normally more efficient for large systems.

## R2 visual refinement

The derivation is intentionally split into two successive visual stages so that the long determinant identities never compete with the explanatory text. The final numerical card also uses smaller ratio lines and greater vertical separation between the ratios, solution vector, and closing remarks.

## R3 visual refinement

The presentation now uses one major mathematical object per visual stage. Long determinant identities, explanatory prose, the Cramer's Rule formula, the ratio computations, the solution vector, and the closing remarks are sequenced rather than stacked. A common lower title band also keeps lesson headings clear of the persistent chapter banner.


## Derivation-card layout refinement R4

This refinement reorganizes the derivation card so the yellow title sits clearly on the second line beneath the chapter banner, the white/blue/green determinant equations occupy the middle band of the screen, and the explanatory prose occupies the bottom band. The goal is to separate title, equations, and commentary into distinct vertical regions with no overlap.


## Layout refinement R5

This refinement adjusts two crowded cards. On the second derivation card, the yellow title and the white/blue equation block are moved upward, and the green concluding equation is set to the same displayed scale as the preceding equations. On the 3x3 example card, the system matrix is reduced slightly and moved lower so it no longer collides with the yellow title above or the green determinant line below.


## Layout refinement R6

This refinement further adjusts the derivation and 3x3-example cards. On the derivation card, the green line is explicitly scaled to match the display height of the white line, and the explanatory sentence now renders the symbol $x_k$ in proper mathematical notation. On the 3x3 example card, the title is nudged higher, the displayed system is reduced and moved lower, and the green determinant line and concluding cue are moved farther down to eliminate persistent collisions.


## Theorem-card typography refinement R7

This refinement updates the explanatory line on the Cramer's Rule theorem card so $A_k$ is rendered in mathematical notation rather than as plain text. The entire definition line is now a MathTex object, with $A_k$, $A$, $k$, and $\mathbf b$ displayed consistently in LaTeX style.
