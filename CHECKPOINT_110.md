# Seeing Linear Algebra — Checkpoint 110

## Topic
Back substitution from row echelon form.

## Goal
Start from the echelon matrix produced in CP109 and solve the system by
working upward from the bottom row. Then verify the resulting solution in the
original system.

## Mathematical content
Begin with the row echelon augmented matrix

\[
\left[
\begin{array}{ccc|c}
1&1&1&3\\
0&1&-2&-1\\
0&0&-7&-7
\end{array}
\right].
\]

Back substitution proceeds upward:

\[
-7z=-7 \Longrightarrow z=1,
\]

\[
y-2(1)=-1 \Longrightarrow y=1,
\]

\[
x+1+1=3 \Longrightarrow x=1.
\]

So the solution is

\[
(x,y,z)=(1,1,1).
\]

Verify this in the original system

\[
\begin{aligned}
x+y+z&=3,\\
2x-y+z&=2,\\
x+2y-z&=2.
\end{aligned}
\]

## Pedagogical sequence
1. Display the echelon form obtained in CP109.
2. Explain that the bottom row contains only one unknown.
3. Solve for \(z\).
4. Substitute \(z=1\) into the second row and solve for \(y\).
5. Substitute \(y=1\) and \(z=1\) into the first row and solve for \(x\).
6. Summarize the solution \((1,1,1)\).
7. Verify the solution in the original system.

## Files
```text
engine/back_substitution.py
scenes/back_substitution_presentation.py
tests/test_back_substitution.py
tests/test_back_substitution_presentation.py
scripts/check_cp110_back_substitution.zsh
scripts/render_cp110_back_substitution.zsh
CHECKPOINT_110.md
```

## Visual review targets
- The echelon matrix remains comfortably separated from the value panel.
- Each highlighted row is obvious before its algebra appears.
- The algebra panels sit low enough to avoid the matrix and high enough to stay on screen.
- The known-values panel updates clearly after each step.
- The verification screen is readable and uncluttered.
- All student-facing text stays within the frame.

## Revision 2
- Remove the Known values panel before the final verification screen.
- Add a compact solution badge above the verification panels.
- Separate the outgoing and incoming bottom captions to prevent a brief crossfade collision.
