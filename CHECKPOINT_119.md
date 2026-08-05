# Seeing Linear Algebra — Checkpoint 119

## Topic
Elementary matrices, inverse elementary operations, and complete row reduction.

## Goal
Represent each elementary row operation as left multiplication, explicitly
reverse each operation with an inverse elementary matrix, and combine a full
sequence of elementary matrices into one row-reduction matrix.

## Individual operations and their inverses
For each elementary matrix \(E\), the lesson now animates both

\[
EA=A'
\]

and

\[
E^{-1}A'=A.
\]

The three examples are:

- \(R_1\leftrightarrow R_2\), whose elementary matrix is its own inverse;
- \(R_2\leftarrow -2R_2\), reversed by
  \(R_2\leftarrow -\tfrac12R_2\);
- \(R_3\leftarrow R_3+2R_1\), reversed by
  \(R_3\leftarrow R_3-2R_1\).

## Complete row-reduction example

\[
A=
\begin{bmatrix}
1&2&1\\
0&1&3\\
0&0&2
\end{bmatrix}.
\]

The lesson performs four elementary operations:

\[
E_1:\ R_3\leftarrow \tfrac12R_3,
\]

\[
E_2:\ R_2\leftarrow R_2-3R_3,
\]

\[
E_3:\ R_1\leftarrow R_1-R_3,
\]

\[
E_4:\ R_1\leftarrow R_1-2R_2.
\]

At every stage the animation displays

\[
E_kA_{k-1}=A_k.
\]

The final result is

\[
E_4E_3E_2E_1A=I.
\]

## Entire row-reduction matrix
The cumulative products are displayed one at a time:

\[
P_1=E_1,
\qquad
P_2=E_2E_1,
\qquad
P_3=E_3E_2E_1,
\qquad
P_4=E_4E_3E_2E_1.
\]

They multiply out to

\[
P_4=
\begin{bmatrix}
1&-2&\tfrac52\\
0&1&-\tfrac32\\
0&0&\tfrac12
\end{bmatrix}.
\]

Since \(P_4A=I\),

\[
P_4=A^{-1}.
\]

## Reverse sequence
Starting from \(I\), the animation applies the inverse elementary matrices in
reverse chronological order:

\[
E_4^{-1},\quad E_3^{-1},\quad E_2^{-1},\quad E_1^{-1}.
\]

This rebuilds \(A\) and yields

\[
A=E_1^{-1}E_2^{-1}E_3^{-1}E_4^{-1}.
\]

Thus the lesson explicitly presents both factorizations:

\[
A^{-1}=E_4E_3E_2E_1,
\]

and

\[
A=E_1^{-1}E_2^{-1}E_3^{-1}E_4^{-1}.
\]

## Pedagogical sequence
1. Construct an elementary matrix from the identity.
2. Review the three elementary operation types.
3. Animate each forward product \(EA\).
4. Animate the corresponding inverse product \(E^{-1}(EA)=A\).
5. Explain why elementary matrices multiply on the left.
6. Carry out a complete four-step row reduction.
7. Accumulate the products \(P_k=E_k\cdots E_1\).
8. Identify the entire row-reduction matrix as \(A^{-1}\).
9. Reverse the process with inverse elementary matrices.
10. Compare the forward and reverse factorizations.

## Future chapter relationship
This expanded checkpoint now contains the inverse-sequence lesson that was
originally going to be deferred. CP120 can therefore focus on elimination
matrices, general elimination products, and factorization rather than repeating
these foundational examples.

## Visual review targets
- Each forward multiplication and inverse multiplication should be readable.
- Matrix labels must remain attached to the correct matrices.
- Changed rows should be highlighted only after the product appears.
- The four reduction steps should proceed slowly enough for hand verification.
- The cumulative-product grid must fit inside its outer panel.
- Fractions in the final reduction matrix must remain legible.
- The reverse sequence must clearly begin at \(I\) and end at \(A\).


## Revised visual layout

- Explanatory text now uses one consistent 21-point size and is only shrunk, never enlarged to fill a panel.
- Fractional matrix entries use compact fractions with additional row spacing.
- Tall panels are lowered and headings raised to maintain a clear gap throughout the expanded lesson.

## Revised 5 visual correction

- Reverse-step headings now separate prose from mathematics.
- `Text` renders “Reverse step k: apply,” while `MathTex` renders `E_j^{-1}` with a true subscript and superscript.
- Removed the stale literal underscore notation from all four reverse-step headings.
