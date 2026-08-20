# Checkpoint 174 — An Eigenvector Basis

## Purpose

Continue Chapter 7 from CP173. CP173 found three independent eigenvectors for

\[
A=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix},
\]

with eigenvalues \(1,2,5\). CP174 asks what happens when those eigenvectors are used as a basis for \(\mathbb R^3\).

## Core example

Use

\[
\mathbf v_1=\begin{bmatrix}0\\0\\1\end{bmatrix},\quad
\mathbf v_2=\begin{bmatrix}1\\-2\\0\end{bmatrix},\quad
\mathbf v_3=\begin{bmatrix}1\\1\\0\end{bmatrix}.
\]

Choose

\[
\mathbf x=\mathbf v_1+\mathbf v_2+\mathbf v_3
=\begin{bmatrix}2\\-1\\1\end{bmatrix},
\]

so

\[
[\mathbf x]_{\mathcal B}=\begin{bmatrix}1\\1\\1\end{bmatrix}.
\]

Because

\[
A\mathbf v_1=1\mathbf v_1,\qquad
A\mathbf v_2=2\mathbf v_2,\qquad
A\mathbf v_3=5\mathbf v_3,
\]

we get

\[
[A\mathbf x]_{\mathcal B}=\begin{bmatrix}1\\2\\5\end{bmatrix}.
\]

## Pedagogy

The lesson is geometric first. It shows the three eigenvector directions in 3D, then decomposes one vector into those basis directions. The transformation acts by independent scaling of the three eigenvector coordinates. The lesson deliberately stops before writing the full diagonalization identity \(A=PDP^{-1}\); that belongs to the next checkpoint.

## Layout

The camera is fixed. 3D is used only for the basis geometry. Algebra is placed in fixed-in-frame regions with explicit width control and generous separation from the chapter banner, lesson title, and heading.

## Validation

The focused checker compiles the renderer-independent engine, scene, and tests, then runs the two CP174 test files.


## Revision note

Fixed the Card 4 LaTeX action line so adjacent raw strings retain an explicit space after `\qquad`. This prevents LaTeX from reading `\qquadA` as an undefined control sequence. Added a focused regression test.


## Revision note

This revision keeps the 3D eigenvector graphic centered when it first appears, then shifts the geometry left as the coordinate equations are introduced. The move creates a clearer split-screen layout and prevents collisions between the 3D graphic and the algebra on the right.


## LaTeX row-break correction

Corrected the Card 3 decomposition and eigenbasis-coordinate column vectors so every bmatrix row separator uses a valid double backslash. Added regression coverage for the exact source strings.


## Revision note

This revision attaches the small eigenvector labels directly to the 3D graphic instead of fixing them in the frame. When the algebra enters, the entire geometry cluster, including the labels, now shifts farther viewer-left and slightly downward to create a cleaner split-screen layout.


## Revision note

This revision fixes the orange-vector artifact by creating the example vector directly from the already-shifted axes, rather than shifting the arrow a second time. It also fades the orange example vector out before introducing the yellow transformed vector, so the transition to A x is cleaner.


## Revision note

This revision makes the orange example vector easier to discern by increasing its thickness and adding an attached x label. It also cleans the Card 3 to Card 4 transition by fading and explicitly removing the fixed white decomposition and coordinate equations before the next algebra appears, preventing residual white artifacts.


## Revision note

The Card 2/3 layout move now translates the 3D graph within the camera's screen plane rather than along the scene's ordinary world x/y directions. This keeps the graph at constant camera depth, preserving its apparent size and perspective while it slides viewer-left and slightly downward to make room for the algebra.
