/* Curated conceptual / multiple-choice / justify / applied items.
   These cover topics (especially in Units 7-9) where a fully general
   numeric generator would either be intractable by hand or would hide
   the underlying idea. Computational generators (generators.js) cover
   every topic too, so the engine can always fall back to those. */

const QUESTION_BANK = [
  // ---------------- Unit 1: Vectors & Vector Spaces ----------------
  { unitId: "vectors", topicId: "vec-ops", type: "conceptual", difficulty: 1,
    prompt: "True or False: Vector addition is commutative, i.e. u + v = v + u for all vectors u, v.",
    answer: "True", explanation: "Addition is componentwise real-number addition, which is commutative." },
  { unitId: "vectors", topicId: "vec-ops", type: "multiplechoice", difficulty: 1,
    prompt: "Which of the following is the zero vector's role in R^n?",
    choices: ["It is the only vector with no direction", "It is the additive identity: v + 0 = v for all v", "It has length 1", "It is undefined in R^n"],
    answer: "It is the additive identity: v + 0 = v for all v" },

  { unitId: "vectors", topicId: "vec-dot", type: "conceptual", difficulty: 2,
    prompt: "True or False: If u . v = 0 for nonzero vectors u and v, then u and v point in exactly opposite directions.",
    answer: "False", explanation: "u . v = 0 means u and v are orthogonal (perpendicular), not opposite." },
  { unitId: "vectors", topicId: "vec-dot", type: "justify", difficulty: 2,
    prompt: "Explain why the Cauchy-Schwarz inequality |u . v| <= |u||v| implies the triangle inequality |u + v| <= |u| + |v|.",
    answer: "Expand |u+v|^2 = |u|^2 + 2(u.v) + |v|^2 <= |u|^2 + 2|u||v| + |v|^2 = (|u|+|v|)^2 using Cauchy-Schwarz, then take square roots.",
    explanation: "Standard proof using Cauchy-Schwarz on the cross term." },

  { unitId: "vectors", topicId: "vec-cross", type: "multiplechoice", difficulty: 1,
    prompt: "The cross product u x v is defined for vectors in which space?",
    choices: ["R^2 only", "R^3 only", "R^n for any n", "Only for unit vectors"],
    answer: "R^3 only" },
  { unitId: "vectors", topicId: "vec-cross", type: "conceptual", difficulty: 2,
    prompt: "True or False: u x v is always orthogonal to both u and v.",
    answer: "True", explanation: "This is the defining geometric property of the cross product." },

  { unitId: "vectors", topicId: "vec-span", type: "conceptual", difficulty: 1,
    prompt: "True or False: The span of a single nonzero vector v in R^3 is a plane through the origin.",
    answer: "False", explanation: "span{v} for a single nonzero vector is a LINE through the origin, not a plane." },
  { unitId: "vectors", topicId: "vec-span", type: "justify", difficulty: 3,
    prompt: "If v1, v2, v3 are three vectors in R^3 and v3 = 2v1 - v2, explain why span{v1, v2, v3} = span{v1, v2}.",
    answer: "Any combination involving v3 can be rewritten in terms of v1 and v2 since v3 is already a combination of them, so adding v3 introduces no new directions.",
    explanation: "v3 is redundant because it lies in span{v1, v2}." },

  { unitId: "vectors", topicId: "vec-subspace", type: "multiplechoice", difficulty: 2,
    prompt: "Which of the following subsets of R^2 is a subspace?",
    choices: ["{(x,y) : x + y = 1}", "{(x,y) : x >= 0}", "{(x,y) : x = 2y}", "{(x,y) : x^2 + y^2 = 1}"],
    answer: "{(x,y) : x = 2y}" },
  { unitId: "vectors", topicId: "vec-subspace", type: "justify", difficulty: 2,
    prompt: "Explain why the union of two distinct lines through the origin in R^2 is NOT a subspace of R^2.",
    answer: "Pick a nonzero vector from each line and add them; the sum generally lies off both lines, so the set fails closure under addition.",
    explanation: "Closure under addition fails even though both individual lines are subspaces." },

  { unitId: "vectors", topicId: "vec-colnullrow", type: "conceptual", difficulty: 2,
    prompt: "True or False: Row(A) and Col(A) always have the same dimension, even though they may be subsets of different spaces.",
    answer: "True", explanation: "Both equal rank(A) in dimension, since row rank = column rank." },
  { unitId: "vectors", topicId: "vec-colnullrow", type: "multiplechoice", difficulty: 1,
    prompt: "The null space of a matrix A consists of all vectors x such that:",
    choices: ["Ax = 0", "xA = 0", "A = 0", "x is a row of A"],
    answer: "Ax = 0" },

  { unitId: "vectors", topicId: "vec-basis", type: "conceptual", difficulty: 1,
    prompt: "True or False: Every basis of a given vector space has the same number of vectors.",
    answer: "True", explanation: "This common size is the dimension of the space." },
  { unitId: "vectors", topicId: "vec-basis", type: "justify", difficulty: 2,
    prompt: "Explain why 4 vectors in R^3 can never be linearly independent.",
    answer: "Any linearly independent set in R^3 has at most 3 vectors, since R^3 has dimension 3; a 4th vector must be a combination of the others.",
    explanation: "Dimension bounds the size of any independent set." },

  { unitId: "vectors", topicId: "vec-rank", type: "applied", difficulty: 2,
    prompt: "A 5x7 matrix A represents 5 sensor readings as combinations of 7 unknown signal sources. If rank(A) = 4, how many independent directions of signal can NOT be recovered from the sensor data, and why?",
    answer: "3 directions (the nullity, 7 - 4 = 3); those directions of signal produce no change in the sensor readings, so they are invisible to this sensor array.",
    explanation: "Nullity = n - rank measures the 'blind directions' of the linear map." },
  { unitId: "vectors", topicId: "vec-rank", type: "multiplechoice", difficulty: 1,
    prompt: "For an m x n matrix A, the Rank-Nullity Theorem states:",
    choices: ["rank(A) + nullity(A) = m", "rank(A) + nullity(A) = n", "rank(A) * nullity(A) = n", "rank(A) - nullity(A) = m"],
    answer: "rank(A) + nullity(A) = n" },

  { unitId: "vectors", topicId: "vec-fourspaces", type: "conceptual", difficulty: 3,
    prompt: "True or False: Col(A) and Null(A^T) are orthogonal complements of each other in R^m.",
    answer: "True", explanation: "This is one of the two orthogonality relations among the four fundamental subspaces." },
  { unitId: "vectors", topicId: "vec-fourspaces", type: "justify", difficulty: 3,
    prompt: "Explain why Row(A) and Null(A) are orthogonal complements in R^n.",
    answer: "Every row of A is orthogonal to every vector in Null(A) by definition of Ax = 0, and dimension counting (rank + nullity = n) shows these subspaces fill out all of R^n as complements.",
    explanation: "Direct consequence of the definition of the null space plus rank-nullity." },

  // ---------------- Unit 2: Linear Transformations & Matrix Algebra ----------------
  { unitId: "matrices", topicId: "mat-lintrans", type: "conceptual", difficulty: 1,
    prompt: "True or False: A function T is linear if T(u+v) = T(u)+T(v) and T(cu) = cT(u) for all vectors u, v and scalars c.",
    answer: "True", explanation: "This is the definition of linearity." },
  { unitId: "matrices", topicId: "mat-lintrans", type: "multiplechoice", difficulty: 2,
    prompt: "Which transformation of R^2 is NOT linear?",
    choices: ["T(x,y) = (2x, -y)", "T(x,y) = (x+y, x-y)", "T(x,y) = (x+1, y)", "T(x,y) = (0, 0)"],
    answer: "T(x,y) = (x+1, y)" },

  { unitId: "matrices", topicId: "mat-repr", type: "justify", difficulty: 2,
    prompt: "Explain why the standard matrix of a linear transformation T: R^n -> R^m is uniquely determined by the images T(e1), ..., T(en) of the standard basis vectors.",
    answer: "Every vector x is a combination of the e_i, so linearity forces T(x) to be the same combination of the T(e_i); those images become exactly the columns of the matrix.",
    explanation: "Linearity plus the standard basis pins down the whole map from finitely many values." },

  { unitId: "matrices", topicId: "mat-addsub", type: "conceptual", difficulty: 1,
    prompt: "True or False: (A + B)^T = A^T + B^T for any two matrices of the same size.",
    answer: "True", explanation: "Transpose distributes over addition." },

  { unitId: "matrices", topicId: "mat-mult", type: "conceptual", difficulty: 1,
    prompt: "True or False: Matrix multiplication is commutative in general, i.e. AB = BA.",
    answer: "False", explanation: "In general AB != BA; commutativity only holds for special pairs of matrices." },
  { unitId: "matrices", topicId: "mat-mult", type: "justify", difficulty: 2,
    prompt: "Explain, using dimensions, why AB can be defined even when BA is not.",
    answer: "AB requires the number of columns of A to equal the number of rows of B; if A is m x n and B is n x p with p != m, then BA (p x n times m x n) is undefined unless p = m.",
    explanation: "Matrix multiplication compatibility depends on matching inner dimensions." },

  { unitId: "matrices", topicId: "mat-elim", type: "conceptual", difficulty: 1,
    prompt: "True or False: Row operations (swap, scale, add a multiple of one row to another) never change the solution set of a linear system.",
    answer: "True", explanation: "Each elementary row operation is reversible and preserves the system's solutions." },

  { unitId: "matrices", topicId: "mat-inverse", type: "multiplechoice", difficulty: 2,
    prompt: "A square matrix A is invertible if and only if:",
    choices: ["det(A) = 0", "A has a row of zeros", "det(A) != 0", "A is symmetric"],
    answer: "det(A) != 0" },
  { unitId: "matrices", topicId: "mat-inverse", type: "applied", difficulty: 2,
    prompt: "A simple encryption scheme multiplies a numeric message vector m by an invertible matrix A to get the ciphertext c = Am. Explain how the recipient decodes c, and why A must be invertible for this scheme to work at all.",
    answer: "The recipient computes m = A^-1 c; if A were not invertible, different messages could map to the same ciphertext (or some ciphertexts would have no valid message), so decoding would be impossible or ambiguous.",
    explanation: "Invertibility is exactly what guarantees a unique, recoverable decoding." },

  { unitId: "matrices", topicId: "mat-lu", type: "conceptual", difficulty: 2,
    prompt: "True or False: In an LU factorization A = LU, U is exactly the row echelon form produced by forward elimination on A (without row swaps).",
    answer: "True", explanation: "L records the elimination multipliers used to reach that echelon form U." },

  { unitId: "matrices", topicId: "mat-axb", type: "multiplechoice", difficulty: 1,
    prompt: "If, after elimination, a system Ax = b produces a row [0 0 0 | 5], the system is:",
    choices: ["Consistent with a unique solution", "Consistent with infinitely many solutions", "Inconsistent (no solution)", "Impossible to determine"],
    answer: "Inconsistent (no solution)" },

  { unitId: "matrices", topicId: "mat-rect", type: "applied", difficulty: 3,
    prompt: "A survey collects 10 equations (one per respondent) in 4 unknown preference scores. Explain why this overdetermined system typically has no exact solution, and what is usually done instead.",
    answer: "With more independent equations than unknowns, the system is generically inconsistent; in practice one finds the least-squares solution that minimizes the total squared error instead of demanding an exact fit.",
    explanation: "This previews the least-squares topic in Unit 4." },

  // ---------------- Unit 3: Determinants ----------------
  { unitId: "determinants", topicId: "det-area", type: "conceptual", difficulty: 1,
    prompt: "True or False: If det(A) = 0 for a 2x2 matrix A, the columns of A are linearly dependent.",
    answer: "True", explanation: "A zero determinant means the parallelogram spanned by the columns has zero area, i.e. the columns are collinear (dependent)." },

  { unitId: "determinants", topicId: "det-props", type: "multiplechoice", difficulty: 2,
    prompt: "If you multiply a single row of an n x n matrix A by a scalar k, the determinant of the new matrix is:",
    choices: ["det(A)", "k * det(A)", "k^n * det(A)", "det(A) + k"],
    answer: "k * det(A)" },
  { unitId: "determinants", topicId: "det-props", type: "justify", difficulty: 3,
    prompt: "Use the scaling property of determinants to explain why det(kA) = k^n det(A) for an n x n matrix A.",
    answer: "Scaling A by k scales every one of the n rows by k; each row scaling multiplies the determinant by k once, so the total factor is k^n.",
    explanation: "Apply the single-row scaling rule n times, once per row." },

  { unitId: "determinants", topicId: "det-cofactor", type: "conceptual", difficulty: 2,
    prompt: "True or False: Cofactor expansion gives the same value for det(A) no matter which row or column you expand along.",
    answer: "True", explanation: "The determinant is a single well-defined number; any row/column expansion computes it." },

  { unitId: "determinants", topicId: "det-invert", type: "conceptual", difficulty: 1,
    prompt: "True or False: A matrix with a full row of zeros always has determinant 0.",
    answer: "True", explanation: "Cofactor expansion along the zero row gives a sum of zero terms." },

  { unitId: "determinants", topicId: "det-cramer", type: "justify", difficulty: 3,
    prompt: "Explain why Cramer's Rule fails to give a solution formula when det(A) = 0, even if the system Ax = b happens to be consistent.",
    answer: "Cramer's Rule divides by det(A); when det(A) = 0 this division is undefined, even though the system may still have infinitely many solutions found by other methods (elimination).",
    explanation: "Cramer's Rule only applies to square systems with a nonzero determinant." },

  { unitId: "determinants", topicId: "det-products", type: "multiplechoice", difficulty: 2,
    prompt: "For square matrices A and B of the same size, det(AB) equals:",
    choices: ["det(A) + det(B)", "det(A) * det(B)", "det(A + B)", "det(A)^det(B)"],
    answer: "det(A) * det(B)" },

  // ---------------- Unit 4: Orthogonality & Least Squares ----------------
  { unitId: "orthogonality", topicId: "orth-sets", type: "conceptual", difficulty: 1,
    prompt: "True or False: An orthonormal set is automatically also an orthogonal set.",
    answer: "True", explanation: "Orthonormal requires orthogonality plus unit length, so it's a stronger condition." },

  { unitId: "orthogonality", topicId: "orth-proj", type: "multiplechoice", difficulty: 2,
    prompt: "The vector b - proj_a(b) is always:",
    choices: ["Parallel to a", "Orthogonal to a", "Equal to b", "The zero vector"],
    answer: "Orthogonal to a" },

  { unitId: "orthogonality", topicId: "orth-complement", type: "justify", difficulty: 2,
    prompt: "Explain why W and W^perp only share the zero vector, for any subspace W of R^n.",
    answer: "If v is in both W and W^perp, then v . v = 0 (since v is orthogonal to itself as an element of W^perp acting on the element v of W), forcing v = 0.",
    explanation: "Self-orthogonality of a nonzero vector is impossible since |v|^2 > 0." },

  { unitId: "orthogonality", topicId: "orth-gramschmidt", type: "conceptual", difficulty: 2,
    prompt: "True or False: The Gram-Schmidt process converts any linearly independent set of vectors into an orthogonal set spanning the same subspace.",
    answer: "True", explanation: "That is precisely the purpose and guarantee of Gram-Schmidt." },

  { unitId: "orthogonality", topicId: "orth-qr", type: "multiplechoice", difficulty: 2,
    prompt: "In a QR factorization A = QR, the matrix R is:",
    choices: ["Orthogonal", "Diagonal", "Upper triangular", "Lower triangular"],
    answer: "Upper triangular" },

  { unitId: "orthogonality", topicId: "orth-leastsquares", type: "applied", difficulty: 2,
    prompt: "A scientist has 8 noisy measurements that should fit a line y = mx + b (2 unknowns). Explain why she solves the normal equations A^T A x = A^T b instead of trying to solve Ax = b directly.",
    answer: "With 8 equations and only 2 unknowns, Ax = b is overdetermined and generally has no exact solution; the normal equations instead give the x that minimizes the total squared residual, the best-fit line.",
    explanation: "Least squares turns an inconsistent system into a solvable minimization problem." },

  // ---------------- Unit 5: Eigenvalues & Eigenvectors ----------------
  { unitId: "eigen", topicId: "eig-charpoly", type: "conceptual", difficulty: 1,
    prompt: "True or False: The eigenvalues of A are exactly the roots of det(A - lambda I) = 0.",
    answer: "True", explanation: "This is the definition of the characteristic equation." },

  { unitId: "eigen", topicId: "eig-vectors", type: "multiplechoice", difficulty: 2,
    prompt: "An eigenvector corresponding to eigenvalue lambda is any nonzero vector v satisfying:",
    choices: ["Av = lambda", "Av = lambda v", "A = lambda v", "v = lambda A"],
    answer: "Av = lambda v" },

  { unitId: "eigen", topicId: "eig-diag", type: "justify", difficulty: 3,
    prompt: "Explain why an n x n matrix with n distinct eigenvalues is guaranteed to be diagonalizable.",
    answer: "Eigenvectors corresponding to distinct eigenvalues are automatically linearly independent, so n distinct eigenvalues produce n independent eigenvectors, which form a basis and diagonalize A.",
    explanation: "Distinctness of eigenvalues rules out repeated-eigenvalue deficiencies that can block diagonalization." },

  { unitId: "eigen", topicId: "eig-powers", type: "applied", difficulty: 2,
    prompt: "A matrix A modeling a population has eigenvalues 1.05 and 0.9. Explain what happens to the population's long-term growth rate and structure as time increases.",
    answer: "The eigenvalue 1.05 dominates because |1.05| > |0.9|, so the population eventually grows by about 5% per period and its distribution converges to (a multiple of) the corresponding eigenvector.",
    explanation: "Long-term behavior of A^k x is governed by the eigenvalue of largest absolute value." },

  { unitId: "eigen", topicId: "eig-symmetric", type: "conceptual", difficulty: 2,
    prompt: "True or False: A symmetric matrix always has real eigenvalues.",
    answer: "True", explanation: "This is a consequence of the Spectral Theorem for real symmetric matrices." },

  { unitId: "eigen", topicId: "eig-apps", type: "justify", difficulty: 2,
    prompt: "For the Fibonacci recurrence F(n+1) = F(n) + F(n-1), explain (without computing exact values) why writing it as a matrix power [[1,1],[1,0]]^n lets you find a closed-form formula for F(n).",
    answer: "Diagonalizing the matrix as PDP^-1 lets you compute the nth power as PD^nP^-1, replacing repeated matrix multiplication with just raising the (scalar) eigenvalues to the nth power.",
    explanation: "Diagonalization turns hard matrix powers into easy scalar powers." },

  // ---------------- Unit 6: Change of Basis ----------------
  { unitId: "changeofbasis", topicId: "cob-coords", type: "conceptual", difficulty: 1,
    prompt: "True or False: The coordinate vector [v]_B of v relative to a basis B depends on the order in which the basis vectors are listed.",
    answer: "True", explanation: "Reordering the basis vectors permutes the entries of the coordinate vector accordingly." },

  { unitId: "changeofbasis", topicId: "cob-matrix", type: "multiplechoice", difficulty: 2,
    prompt: "If P is the change-of-basis matrix converting B1-coordinates to B2-coordinates, then P^-1 converts:",
    choices: ["B2-coordinates to B1-coordinates", "Standard coordinates to B1-coordinates", "B1-coordinates to standard coordinates", "Nothing meaningful"],
    answer: "B2-coordinates to B1-coordinates" },

  { unitId: "changeofbasis", topicId: "cob-transform", type: "justify", difficulty: 3,
    prompt: "Explain why A and B^-1AB (for invertible B) represent the same linear transformation, just in different bases.",
    answer: "B^-1AB describes what A does to a vector after first converting to the new basis (via B), applying A, then converting back (via B^-1) — the underlying map is unchanged, only its matrix description changes.",
    explanation: "This is the similarity relation that underlies change of basis for linear maps." },

  // ---------------- Unit 7: Positive Definite Matrices ----------------
  { unitId: "posdef", topicId: "pd-eigtest", type: "conceptual", difficulty: 1,
    prompt: "True or False: A symmetric matrix is positive definite exactly when all of its eigenvalues are positive.",
    answer: "True", explanation: "This is the eigenvalue test for positive definiteness." },

  { unitId: "posdef", topicId: "pd-elimtest", type: "multiplechoice", difficulty: 2,
    prompt: "In the pivot (elimination) test for positive definiteness, a symmetric matrix is positive definite exactly when:",
    choices: ["All entries are positive", "All pivots produced by elimination are positive", "The determinant is positive", "The trace is positive"],
    answer: "All pivots produced by elimination are positive" },

  { unitId: "posdef", topicId: "pd-ldl", type: "justify", difficulty: 3,
    prompt: "Explain how the Cholesky factorization A = LL^T follows from the LDL^T factorization when A is positive definite.",
    answer: "Since D has strictly positive diagonal entries, we can write D = sqrt(D) sqrt(D), so A = L sqrt(D) sqrt(D) L^T = (L sqrt(D))(L sqrt(D))^T, giving a single triangular factor L' = L sqrt(D) with A = L'L'^T.",
    explanation: "Positive pivots are exactly what let you take a real square root of D." },

  { unitId: "posdef", topicId: "pd-ata", type: "applied", difficulty: 2,
    prompt: "In statistics, a covariance matrix is always of the form (1/n) X^T X for a data matrix X. Explain why this guarantees the covariance matrix is at least positive semidefinite.",
    answer: "For any vector v, v^T(X^TX)v = (Xv)^T(Xv) = |Xv|^2 >= 0, so X^TX (and hence the covariance matrix) is positive semidefinite by definition.",
    explanation: "A^T A is always positive semidefinite because the associated quadratic form is a sum of squares." },

  // ---------------- Unit 8: Singular Value Decomposition ----------------
  { unitId: "svd", topicId: "svd-basics", type: "conceptual", difficulty: 1,
    prompt: "True or False: Every matrix (square or rectangular) has a singular value decomposition, unlike eigen-decomposition which requires a square matrix.",
    answer: "True", explanation: "The SVD exists for any real (or complex) m x n matrix." },

  { unitId: "svd", topicId: "svd-compute", type: "multiplechoice", difficulty: 2,
    prompt: "The singular values of A are computed as:",
    choices: ["The eigenvalues of A", "The square roots of the eigenvalues of A^T A", "The diagonal entries of A", "The rows of A"],
    answer: "The square roots of the eigenvalues of A^T A" },

  { unitId: "svd", topicId: "svd-pseudoinv", type: "justify", difficulty: 3,
    prompt: "Explain why the pseudoinverse A+ = V Sigma+ U^T reduces to the ordinary inverse A^-1 when A is square and invertible.",
    answer: "When A is invertible all singular values are nonzero, so Sigma+ = Sigma^-1 exactly, and V Sigma^-1 U^T equals A^-1 because A = U Sigma V^T implies A^-1 = V Sigma^-1 U^T.",
    explanation: "The pseudoinverse construction specializes to the true inverse whenever one exists." },

  { unitId: "svd", topicId: "svd-lowrank", type: "applied", difficulty: 2,
    prompt: "An image is stored as a matrix with singular values 120, 45, 10, 2, 0.5, .... Explain why keeping only the top 2 singular values (a rank-2 approximation) can compress the image with little visible loss.",
    answer: "Because the singular values drop off quickly, most of the 'energy' (Frobenius norm) of the matrix is captured by the largest ones; the Eckart-Young theorem guarantees the truncated SVD is the best possible low-rank approximation, so little information is lost.",
    explanation: "This is the mathematical basis of SVD-based image compression." },

  // ---------------- Unit 9: Graphs, Networks & Markov Chains ----------------
  { unitId: "graphs", topicId: "gr-adjacency", type: "conceptual", difficulty: 1,
    prompt: "True or False: For an undirected graph, the adjacency matrix is always symmetric.",
    answer: "True", explanation: "Each edge {i,j} contributes to both A[i][j] and A[j][i] equally." },

  { unitId: "graphs", topicId: "gr-incidence", type: "multiplechoice", difficulty: 2,
    prompt: "For a connected graph's incidence matrix B, Null(B) is spanned by:",
    choices: ["The zero vector only", "The all-ones vector", "The rows of B", "The standard basis vectors"],
    answer: "The all-ones vector" },

  { unitId: "graphs", topicId: "gr-spectral", type: "justify", difficulty: 3,
    prompt: "Explain why the all-ones vector is always an eigenvector of any graph Laplacian L, with eigenvalue 0.",
    answer: "Each row of L sums to zero (degree on the diagonal minus 1's for each neighbor), so L times the all-ones vector gives the zero vector, i.e. L*1 = 0*1.",
    explanation: "Row sums of zero are built into the Laplacian's definition L = D - A." },

  { unitId: "graphs", topicId: "gr-electrical", type: "applied", difficulty: 2,
    prompt: "In a resistor network modeled by Lx = b (Kirchhoff's Laws), explain why at least one node's potential must be fixed (grounded) before the system can be solved uniquely.",
    answer: "The Laplacian L is singular (it has the all-ones vector in its null space), so without fixing a reference potential the system has infinitely many solutions that differ by a constant shift; grounding one node removes that ambiguity.",
    explanation: "This mirrors why absolute electrical potential is only meaningful relative to a reference point." },

  { unitId: "graphs", topicId: "gr-markov", type: "conceptual", difficulty: 2,
    prompt: "True or False: For a Markov chain's transition matrix, the steady-state distribution is always an eigenvector of the transition matrix with eigenvalue 1.",
    answer: "True", explanation: "The steady state pi satisfies P*pi = pi, which is exactly the eigenvector equation for eigenvalue 1." },
  { unitId: "graphs", topicId: "gr-markov", type: "applied", difficulty: 3,
    prompt: "Explain, in terms of eigenvalues, why PageRank's random-walk model on the web graph converges to a single steady-state ranking regardless of the starting distribution.",
    answer: "The (damped) transition matrix has 1 as its largest eigenvalue with a unique corresponding eigenvector (the steady state), and all other eigenvalues are strictly smaller in absolute value, so repeated multiplication drives any starting distribution toward that dominant eigenvector.",
    explanation: "This is the linear-algebra engine behind PageRank's convergence guarantee." }
];
