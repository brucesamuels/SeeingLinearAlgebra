# Positive Definite Matrices — Proposed Narration

This script is timed for the 1080p60 chapter master played at 80% of the
original animation speed. The target duration is approximately **18:37**.
Bracketed text is a performance note, not spoken narration.

## Opening title — 00:00–00:07

Throughout this chapter, we will call the quadratic form \(x^T A x\)
**quadratic energy**. The word “energy” is a unifying interpretation, not a
claim that every matrix describes physics. [Continue without a hard pause.]

## CP199 — Why Positive Definiteness? — 00:07–00:46

In a spring or elastic system, this expression can be literal stored energy.
In other settings it can represent variance, squared size, or cost. The name
is useful because all of these quantities should be nonnegative, and because
their smallest values often identify equilibrium or a best solution.

Start with the symmetric matrix \(A\) having diagonal entries two and
off-diagonal entries one. Let \(x\) move around the unit circle. For every
direction, the scalar \(x^T A x\) remains positive. The number changes with
direction, but it never reaches zero and never becomes negative.

That observation motivates the definition. A symmetric matrix is positive
definite when \(x^T A x\) is greater than zero for every nonzero vector
\(x\). The condition tests every possible direction, not merely the coordinate
axes. What structural facts about \(A\) guarantee this behavior?

## CP200 — From Directional Energy to a Bowl — 00:46–01:49

Any nonzero vector can be written as a length \(r\) times a unit direction
\(u\). Substitution gives \(q(ru)=r^2q(u)\). Direction determines the energy
per squared unit of distance; radius then scales that value by \(r^2\).

Plotting \(q(x)=x^T A x\) above the plane produces a quadratic surface. When
the energy is positive in every direction, the surface rises away from the
origin like a bowl. The origin is its unique minimum.

Now pause and imagine the alternatives. If one direction had zero energy,
the bowl would flatten along that direction. If a direction had negative
energy, the surface would descend there, producing a saddle rather than a
minimum. Positive definiteness is precisely what rules out both failures.

## CP201 — The Eigenvalue Test — 01:49–02:56

Eigenvectors reveal the principal directions of a symmetric matrix. For this
example, one eigenvector points along the line \(x_1=x_2\) and has eigenvalue
three. The perpendicular eigenvector points along \(x_1=-x_2\) and has
eigenvalue one.

Write any vector as \(x=c_1v_1+c_2v_2\). Orthogonality removes the cross
terms, leaving \(x^T A x=3c_1^2+c_2^2\). Every nonzero vector has at least
one nonzero coefficient, so the energy is positive.

In general, a real symmetric matrix is positive definite exactly when all of
its eigenvalues are positive. Zero eigenvalues create flat directions;
negative eigenvalues create descending directions.

## CP202 — The Elimination Test — 02:56–04:10

We can test the same property without first computing eigenvalues. Ordinary
elimination on the two-by-two example produces positive pivots two and
three-halves. Completing the square rewrites the energy as a sum of positive
multiples of squares.

For a symmetric matrix, positive definiteness is equivalent to having all
positive pivots when elimination proceeds without row exchanges.

The closely related Sylvester test uses leading principal minors. These are
the determinants of the upper-left one-by-one, two-by-two, and then
three-by-three blocks. In the displayed three-by-three example, each leading
determinant is positive. Positivity of every leading principal minor is
another complete test for positive definiteness. “Leading” matters: these are
nested blocks beginning in the upper-left corner, not every minor of the
matrix.

## CP203 — The LDL-Transpose Factorization — 04:10–05:21

Symmetric elimination naturally records a factorization
\(A=LDL^T\). The lower triangular matrix \(L\) records the elimination
multipliers, while the diagonal matrix \(D\) contains the pivots.

Insert the factorization into the quadratic form and set \(y=L^Tx\). Then
\(x^TAx=y^TDy\), a weighted sum of squares. Because an invertible triangular
change of coordinates cannot turn a nonzero \(x\) into zero, the signs of the
diagonal entries of \(D\) determine the signs available to the energy.

Thus a symmetric matrix is positive definite exactly when all the entries of
\(D\), equivalently all its elimination pivots, are positive.

## CP204 — Cholesky: A Matrix Square Root — 05:21–06:37

When the diagonal entries of \(D\) are positive, take their positive square
roots and absorb them into the triangular factor. This gives the Cholesky
factorization \(A=R^TR\), with \(R\) upper triangular and a positive diagonal.

Now the energy becomes
\(x^TAx=x^TR^TRx=\lVert Rx\rVert^2\). A positive-definite quadratic form is
therefore an ordinary squared Euclidean length after an invertible change of
coordinates.

The positive diagonal convention makes the Cholesky factor unique. It also
makes the factorization computationally valuable: positive definiteness can be
checked and linear systems can be solved without constructing eigenvectors.

## CP205 — Why A-Transpose A Is Positive Semidefinite — 06:37–07:48

Every matrix \(B\), rectangular or square, creates the symmetric Gram matrix
\(B^TB\). Its quadratic form is
\(x^TB^TBx=\lVert Bx\rVert^2\), which can never be negative. Therefore
\(B^TB\) is always positive semidefinite.

The only remaining question is whether zero is possible for a nonzero
\(x\). That happens exactly when \(Bx=0\), so \(B^TB\) is positive definite
exactly when the nullspace of \(B\) contains only zero—equivalently, when
\(B\) has independent columns.

## CP206 — Why Least Squares Has a Unique Solution — 07:48–09:06

In least squares, we choose \(x\) to minimize the squared residual
\(\lVert Ax-b\rVert^2\). Differentiating this quadratic objective leads to
the normal equations \(A^TAx=A^Tb\).

Geometrically, the best residual is perpendicular to every column of \(A\).
Algebraically, uniqueness depends on the curvature matrix \(A^TA\). If the
columns of \(A\) are independent, then \(A^TA\) is positive definite, the
objective has one strict minimum, and the normal equations have one solution.

If the columns are dependent, different coefficient vectors can produce the
same fitted vector. The residual may still be uniquely determined, but the
coefficients need not be.

## CP207 — Why Covariance Is Positive Semidefinite — 09:06–10:36

A covariance matrix summarizes how measured variables vary together. Begin
with observations, subtract the sample mean from each one, and place the
centered observations into a data matrix \(X\). Up to the conventional scaling
factor, the covariance matrix is \(C=X^TX\).

Choose any direction \(u\) in the space of variables. Project every centered
observation onto that direction. The directional variance is an average of
squared projected values, so
\(u^TCu\) is nonnegative.

That is why every covariance matrix is positive semidefinite. It becomes
positive definite only when no nonzero combination of variables has zero
variation. A zero-energy direction here is not mysterious: it is an exact
linear relation present throughout the data.

## CP208 — Why the Singular Value Decomposition? — 10:36–11:55

The singular value decomposition describes any matrix as three simple actions:
an orthogonal change of input coordinates, independent stretches, and an
orthogonal change of output coordinates.

The right singular vectors are the orthonormal eigenvectors of \(A^TA\).
Their eigenvalues are nonnegative because \(A^TA\) is a Gram matrix. Taking
square roots gives the singular values—the actual stretch factors. Applying
\(A\) to each right singular direction and normalizing gives the corresponding
left singular direction.

Collecting those directions produces \(A=U\Sigma V^T\). Unlike an
eigendecomposition, the SVD works for rectangular matrices and allows the
input and output directions to live in different spaces.

## CP209 — Computing the SVD from A-Transpose A — 11:55–13:32

For the displayed matrix \(B\), first compute the symmetric matrix \(B^TB\).
Its orthonormal eigenvectors become the columns of \(V\), and the square roots
of its eigenvalues become the singular values in \(\Sigma\).

For each nonzero singular value, calculate
\(u_i=Bv_i/\sigma_i\). These vectors have unit length and are mutually
orthogonal, giving the columns of \(U\).

There is a harmless sign choice: changing the signs of both \(u_i\) and
\(v_i\) leaves the product unchanged. The dependable recipe is therefore:
diagonalize \(B^TB\), take nonnegative square roots, construct the left
singular vectors, and verify \(B=U\Sigma V^T\).

## CP210 — The Minimum Principle — 13:32–15:11

The Rayleigh quotient
\(R(x)=x^TAx/(x^Tx)\) removes the effect of scale and keeps only direction.
Expand \(x\) in an orthonormal eigenvector basis. The quotient becomes a
weighted average of the eigenvalues, with nonnegative weights that sum to one.

It can therefore never fall below the smallest eigenvalue or rise above the
largest. Its minimum is achieved in a smallest-eigenvalue direction, and its
maximum in a largest-eigenvalue direction.

After finding one eigenvector, impose orthogonality to it and minimize again.
Successive constrained minima reveal the remaining eigenvalues in order. This
variational viewpoint connects matrix spectra to optimization and to the
continuous energy principles used in differential equations.

## CP211 — Finite Elements: Turning Energy into a Matrix — 15:11–17:13

Consider a stretched string. Let \(u(x)\) denote its downward displacement,
not time, and let the load pull downward. Force balance gives
\(-T u''=q\). The second derivative measures curvature; a downward-deflected
string is concave down, so \(u''\) is negative. The minus sign makes a positive
downward load correspond to positive downward displacement.

With tension and load normalized to one, the equation becomes \(-u''=1\).
The conditions \(u(0)=u(1)=0\) say that both ends are fixed. These are
boundary conditions in space, not initial conditions in time.

The finite-element method replaces the smooth displacement by a combination
of local hat functions. Their coefficients are the unknown nodal
displacements. Integrating the stretching energy and the work of the load
produces a matrix equation \(Kc=f\).

The stiffness matrix \(K\) is positive definite because
\(c^TKc\) measures discrete stretching energy. Zero stretching together with
fixed endpoints forces every displacement to be zero. The minimum of the
discrete energy gives the computed shape of the string.

## CP212 — Positive Definiteness: The Big Picture — 17:13–18:37

We can now recognize one idea in many forms. For a real symmetric matrix,
positive definiteness means positive quadratic energy in every nonzero
direction. It means a bowl with a strict minimum, positive eigenvalues,
positive pivots, positive leading principal minors, and factorizations
\(LDL^T\) with positive \(D\) or \(R^TR\) with invertible \(R\).

Positive semidefinite matrices allow flat directions. Indefinite matrices allow
both positive and negative directions and therefore saddle behavior.

The same structure explains unique least-squares solutions, nonnegative
variance, singular values, minimum principles, and stable finite-element
systems. In physics the word energy can be literal; elsewhere it is a useful
mathematical lens. In every case the central question is the same: what does
the quadratic form do in every direction?

[Let the final equivalence remain on screen before the fade.]
