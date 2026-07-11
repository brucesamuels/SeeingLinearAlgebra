# Episode 2: Span, Rank, and Dimension

## Central idea

Rank is the number of independent directions available in the output.
A rank drop appears as a collapse of reachable space.

## R^2

1. Two nonparallel vectors generate `a v_1 + b v_2`.
2. Sweep coefficients to fill the plane.
3. Display rank 2 and dimension 2.
4. Pause and predict.
5. Rotate the second vector until it becomes parallel.
6. Compress the plane into a line.
7. Keep both coefficients varying.
8. Display rank 1 and dimension 1.

## R^3

1. Three independent vectors fill a translucent volume.
2. Display rank 3 and span equal to R^3.
3. Move the third vector into the plane of the first two.
4. Compress the volume into a plane.
5. Keep all three coefficients varying.
6. Display rank 2.
7. Make all three vectors parallel.
8. Fold the plane into a line.
9. Display rank 1.

## Matrix reveal

Transform the vectors into columns of a matrix and show

`Ax = x_1 v_1 + x_2 v_2 + x_3 v_3`.

Reveal:

- `Col(A) = span{columns of A}`
- `dim Col(A) = rank(A)`

## Closing question

What information about the input is lost when the output space loses a dimension?
