# Checkpoint 182 — Fibonacci and Difference Equations

## Lesson purpose

Use the Fibonacci recurrence as a discrete-dynamics application of eigenvalues, eigenvectors, diagonalization, matrix powers, and dominant eigenvalue behavior.

## Mathematical arc

1. Start with `F_{n+1}=F_n+F_{n-1}` and `F_0=0, F_1=1`.
2. Define the state vector `x_n=[F_{n+1},F_n]^T`.
3. Derive `x_{n+1}=Ax_n` for `A=[[1,1],[1,0]]`.
4. Conclude `x_n=A^n x_0`.
5. Compute the eigenvalues `phi=(1+sqrt(5))/2` and `psi=(1-sqrt(5))/2`.
6. Use eigenvectors `[phi,1]^T` and `[psi,1]^T` to diagonalize `A`.
7. Use `A^n=PD^nP^{-1}`.
8. Derive Binet's formula `F_n=(phi^n-psi^n)/sqrt(5)`.
9. Verify `F_8=21`.
10. Use the dominant eigenvalue to explain `F_{n+1}/F_n -> phi`.

## Pedagogical role

This lesson is the discrete analogue of CP181's first-order ODE system. Together they show that an eigenvector basis decouples both continuous and discrete linear dynamics.


## Revision note

This revision replaces the Card 4 subheading with a mixed text/math heading so A^n renders properly, and lowers the Card 5 eigenvector/diagonalization block to prevent the orange diagonalization expression from colliding with the subheading.


## Revision note

This revision renders the Card 7 subheading's F_n with MathTex so the subscript is displayed properly instead of appearing as raw LaTeX.
