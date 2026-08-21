# Checkpoint 187 - Why Change Basis?

This checkpoint begins the unnumbered **Change of Basis** chapter.

The lesson establishes its central visual idea:

\[
\boxed{\text{The geometric vector remains fixed while its coordinate description changes.}}
\]

The fixed vector is

\[
\mathbf v=\begin{bmatrix}4\\2\end{bmatrix}.
\]

Relative to the standard basis, its coordinate column is

\[
[\mathbf v]_{\mathcal E}=\begin{bmatrix}4\\2\end{bmatrix}.
\]

For

\[
\mathcal B=\left(
\begin{bmatrix}1\\1\end{bmatrix},
\begin{bmatrix}1\\-1\end{bmatrix}
\right),
\]

the same vector satisfies

\[
\mathbf v=3\mathbf b_1+\mathbf b_2,
\qquad
[\mathbf v]_{\mathcal B}=\begin{bmatrix}3\\1\end{bmatrix}.
\]

The presentation creates the vector arrow once and never transforms it. The standard grid is replaced by the oblique basis lattice while the arrow and endpoint remain fixed.

The two bases are also introduced as two coordinate **languages** for the same geometry. This provides an intuitive bridge from the visual distinction to the later change-of-coordinate formulas.

Revision 1 wraps the final yellow takeaway into a balanced two-line block so that it remains within the right-hand panel and the frame margins.

Revision 2 constrains and centers the complete final panel - coordinate columns and takeaway together - within an explicit right-hand safe area. This corrects both horizontal and vertical overflow.

## Installation and preview

From the repository root:

```zsh
zsh /path/to/seeing_linear_algebra_cp187_why_change_basis/apply_checkpoint_187.zsh
zsh scripts/check_cp187_why_change_basis.zsh
zsh scripts/render_cp187_why_change_basis.zsh
```
