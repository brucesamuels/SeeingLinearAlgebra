# Checkpoint 138 - Using Cofactor Expansion Efficiently

## Goal
Turn cofactor expansion into a practical computational method by teaching students to choose a row or column with many zeros and to apply the method recursively.

## Lesson arc
1. Present a 4x4 matrix and ask which row or column should be used.
2. Highlight row 2, which contains three zeros.
3. Expand along row 2 so that only one cofactor term survives.
4. Reduce to a 3x3 determinant.
5. Expand that determinant again, showing that cofactor expansion is recursive.
6. Finish with 2x2 determinants and obtain det(A)=12.
7. Compare the good choice (one surviving term) with a poorer row choice (two surviving terms).
8. Conclude: choose a row or column with as many zeros as possible.

## Mathematical example

A =
[[2,0,1,0],
 [0,3,0,0],
 [1,0,2,1],
 [0,0,1,2]]

Expanding along row 2 gives

det(A) = 3 det([[2,1,0],[1,2,1],[0,1,2]]).

Expanding the 3x3 determinant along its first row gives

det(B) = 2 det([[2,1],[1,2]]) - det([[1,1],[0,2]]) = 4.

Therefore det(A)=3(4)=12.

## Student-facing key idea
Cofactor expansion works along any row or column. Zeros make terms disappear. Choose a row or column with as many zeros as possible.
