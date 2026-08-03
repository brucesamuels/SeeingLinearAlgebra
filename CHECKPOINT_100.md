# Checkpoint 100 — Matrix Multiplication as Composition

## Chapter role

CP100 follows the row–column computation of matrix products and explains what
the product means geometrically: one transformation followed by another.

## Storyboard

1. Show the sequence
   \[
   \mathbf{x}\xrightarrow{A}A\mathbf{x}
   \xrightarrow{B}B(A\mathbf{x}).
   \]
2. Compress the sequence to
   \[
   B(A\mathbf{x})=(BA)\mathbf{x}.
   \]
3. Animate a vector through a horizontal shear and then a reflection.
4. Display the corresponding matrix sequence.
5. Compute the product matrix \(BA\).
6. Verify that the product matrix gives the same final vector.
7. Explain why the rightmost matrix acts first.
8. Include a Pause-and-Predict prompt.
9. Bridge to noncommutativity.

## Example

\[
A=
\begin{bmatrix}
1&1\\
0&1
\end{bmatrix},
\qquad
B=
\begin{bmatrix}
-1&0\\
0&1
\end{bmatrix},
\qquad
\mathbf{x}=
\begin{bmatrix}
2\\1
\end{bmatrix}.
\]

Then

\[
A\mathbf{x}=
\begin{bmatrix}
3\\1
\end{bmatrix},
\qquad
B(A\mathbf{x})=
\begin{bmatrix}
-3\\1
\end{bmatrix}.
\]

Also,

\[
BA=
\begin{bmatrix}
-1&-1\\
0&1
\end{bmatrix},
\]

so

\[
(BA)\mathbf{x}=
\begin{bmatrix}
-3\\1
\end{bmatrix}.
\]

## Apply

```zsh
chmod +x ~/Downloads/seeing_linear_algebra_cp100/apply_checkpoint_100.zsh
~/Downloads/seeing_linear_algebra_cp100/apply_checkpoint_100.zsh
```

## Check

```zsh
./scripts/check_cp100_matrix_multiplication_composition.zsh
```

## Render

```zsh
./scripts/render_cp100_matrix_multiplication_composition.zsh
```

Do not commit until the render has been reviewed and approved.
