# Checkpoint 188 - Coordinates Relative to a Basis

This checkpoint develops the second lesson of the unnumbered **Change of Basis** chapter.

It continues the fixed example from CP187:

\[
\mathbf v=\begin{bmatrix}4\\2\end{bmatrix},
\qquad
\mathcal B=(\mathbf b_1,\mathbf b_2),
\qquad
\mathbf b_1=\begin{bmatrix}1\\1\end{bmatrix},
\quad
\mathbf b_2=\begin{bmatrix}1\\-1\end{bmatrix}.
\]

The geometry first constructs

\[
\mathbf v=3\mathbf b_1+\mathbf b_2
\]

with three green copies of \(\mathbf b_1\) and one blue copy of \(\mathbf b_2\). Only afterward are the ordered coefficients placed into

\[
[\mathbf v]_{\mathcal B}=\begin{bmatrix}3\\1\end{bmatrix}.
\]

The lesson then distinguishes the geometric vector from its coordinate column and demonstrates that reversing the ordered basis reverses the coordinates:

\[
\mathcal B'=(\mathbf b_2,\mathbf b_1)
\quad\Longrightarrow\quad
[\mathbf v]_{\mathcal B'}=\begin{bmatrix}1\\3\end{bmatrix}.
\]

All right-hand content panels use explicit width and height constraints to preserve frame margins.

Revision 1 enlarges the mathematical expressions on Cards 4 and 5. Card 5 separates each ordered basis and its coordinate column onto two lines so the larger type remains legible without being reduced by the safe-width fitting.

Revision 2 gives Card 5 the full content width. The graph fades after Card 4, the two ordered-basis descriptions appear side by side at 54 points, and no height-based scaling is applied. The concluding card is also centered in the resulting full-width layout.

## Installation and preview

From the repository root:

```zsh
zsh /path/to/seeing_linear_algebra_cp188_coordinates_relative_to_basis/apply_checkpoint_188.zsh
zsh scripts/check_cp188_coordinates_relative_to_basis.zsh
zsh scripts/render_cp188_coordinates_relative_to_basis.zsh
```
