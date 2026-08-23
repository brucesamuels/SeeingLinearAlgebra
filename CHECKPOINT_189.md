# Checkpoint 189 - The Basis Matrix

This checkpoint develops the third lesson of the unnumbered **Change of Basis** chapter.

For

\[
\mathbf b_1=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\mathbf b_2=\begin{bmatrix}1\\-1\end{bmatrix},
\]

the basis matrix is formed by placing the basis vectors into its columns:

\[
P_{\mathcal B}=[\,\mathbf b_1\ \mathbf b_2\,]
=\begin{bmatrix}1&1\\1&-1\end{bmatrix}.
\]

The lesson interprets the coordinate entries as weights on those columns and derives

\[
P_{\mathcal B}
\begin{bmatrix}3\\1\end{bmatrix}
=3\mathbf b_1+\mathbf b_2
=\begin{bmatrix}4\\2\end{bmatrix}.
\]

Thus,

\[
\boxed{\mathbf v=P_{\mathcal B}[\mathbf v]_{\mathcal B}}.
\]

The presentation then treats the basis matrix as a coordinate decoder:

\[
\begin{bmatrix}1\\0\end{bmatrix}_{\mathcal B}\mapsto\mathbf b_1,
\qquad
\begin{bmatrix}0\\1\end{bmatrix}_{\mathcal B}\mapsto\mathbf b_2,
\qquad
\begin{bmatrix}3\\1\end{bmatrix}_{\mathcal B}\mapsto\mathbf v.
\]

Revision 1 removes the reversed-order comparison and replaces it with a detailed numerical conversion:

\[
[\mathbf u]_{\mathcal B}=\begin{bmatrix}2\\-1\end{bmatrix}
\quad\Longrightarrow\quad
[\mathbf u]_{\mathcal E}
=\begin{bmatrix}1&1\\1&-1\end{bmatrix}
\begin{bmatrix}2\\-1\end{bmatrix}
=\begin{bmatrix}1\\3\end{bmatrix}.
\]

The row arithmetic is displayed explicitly. The synthesis now states the conversion as

\[
\boxed{[\mathbf v]_{\mathcal E}=P_{\mathcal B}[\mathbf v]_{\mathcal B}},
\]

with the clarification that \([\mathbf v]_{\mathcal E}=\mathbf v\) when vectors are written as standard coordinate columns. Algebra-heavy cards use large mathematics and a full-width safe layout.

Revision 2 adds an opening problem-setting card before the basis matrix is introduced:

\[
\text{How do we translate }[\mathbf v]_{\mathcal B}
\text{ into }[\mathbf v]_{\mathcal E}\text{?}
\]

The card emphasizes that the two coordinate columns describe the same vector. The remainder of the lesson then presents \(P_{\mathcal B}\) as the answer to that opening question.

Revision 3 makes the coordinate grid and axes more pronounced throughout the geometric cards. During the decoder sequence, the graphical outputs are labeled directly with their standard-basis coordinates:

\[
[\mathbf b_1]_{\mathcal E}=(1,1),
\qquad
[\mathbf b_2]_{\mathcal E}=(1,-1),
\qquad
[\mathbf v]_{\mathcal E}=(4,2).
\]

The labels transform in synchronization with the corresponding output arrows.

## Installation and preview

From the repository root:

```zsh
zsh /path/to/seeing_linear_algebra_cp189_basis_matrix/apply_checkpoint_189.zsh
zsh scripts/check_cp189_basis_matrix.zsh
zsh scripts/render_cp189_basis_matrix.zsh
```
