/* Curriculum structure for Seeing Linear Algebra Problem Set Generator.
   Units/topics are derived from this project's own course checkpoints
   (CHECKPOINT_1.md - CHECKPOINT_239.md), which document the full Brooklyn
   Technical High School Linear Algebra course sequence (a Strang-style
   "Introduction to Linear Algebra" syllabus). No separate syllabus/textbook
   file was attached to this session, so this list was built directly from
   the repository's own chapter checkpoints rather than an external upload. */

const CURRICULUM = [
  {
    id: "vectors",
    title: "Unit 1: Vectors & Vector Spaces",
    topics: [
      { id: "vec-ops", title: "Vector addition, subtraction & scalar multiplication" },
      { id: "vec-dot", title: "Dot product, length, and unit vectors" },
      { id: "vec-cross", title: "Cross product in R^3" },
      { id: "vec-span", title: "Linear combinations & span" },
      { id: "vec-subspace", title: "Subspaces & the subspace test" },
      { id: "vec-colnullrow", title: "Column space, null space & row space" },
      { id: "vec-basis", title: "Basis and dimension" },
      { id: "vec-rank", title: "Rank & nullity (Rank-Nullity Theorem)" },
      { id: "vec-fourspaces", title: "The four fundamental subspaces" }
    ]
  },
  {
    id: "matrices",
    title: "Unit 2: Linear Transformations & Matrix Algebra",
    topics: [
      { id: "mat-lintrans", title: "Linear transformations & linearity" },
      { id: "mat-repr", title: "Matrix representation of a transformation" },
      { id: "mat-addsub", title: "Matrix addition, scalar multiplication, transpose, trace" },
      { id: "mat-mult", title: "Matrix multiplication (row-column rule, composition)" },
      { id: "mat-elim", title: "Elimination & row echelon form" },
      { id: "mat-inverse", title: "Gauss-Jordan elimination & matrix inverses" },
      { id: "mat-lu", title: "LU factorization (PA = LU)" },
      { id: "mat-axb", title: "Solving Ax = b: existence & uniqueness" },
      { id: "mat-rect", title: "Rectangular systems (over-/under-determined)" }
    ]
  },
  {
    id: "determinants",
    title: "Unit 3: Determinants",
    topics: [
      { id: "det-area", title: "Determinant as area/volume scale factor" },
      { id: "det-props", title: "Properties of determinants" },
      { id: "det-cofactor", title: "Cofactor expansion" },
      { id: "det-invert", title: "Determinants & invertibility" },
      { id: "det-cramer", title: "Cramer's Rule" },
      { id: "det-products", title: "Determinants of products & transposes" }
    ]
  },
  {
    id: "orthogonality",
    title: "Unit 4: Orthogonality & Least Squares",
    topics: [
      { id: "orth-sets", title: "Orthogonal & orthonormal sets" },
      { id: "orth-proj", title: "Projection onto a vector or subspace" },
      { id: "orth-complement", title: "Orthogonal complements" },
      { id: "orth-gramschmidt", title: "Gram-Schmidt process" },
      { id: "orth-qr", title: "QR factorization" },
      { id: "orth-leastsquares", title: "Least squares approximation" }
    ]
  },
  {
    id: "eigen",
    title: "Unit 5: Eigenvalues & Eigenvectors",
    topics: [
      { id: "eig-charpoly", title: "Characteristic polynomial & eigenvalues" },
      { id: "eig-vectors", title: "Computing eigenvectors & eigenspaces" },
      { id: "eig-diag", title: "Diagonalization" },
      { id: "eig-powers", title: "Powers of a matrix & dynamical systems" },
      { id: "eig-symmetric", title: "Symmetric matrices & the Spectral Theorem" },
      { id: "eig-apps", title: "Applications: Fibonacci & difference equations" }
    ]
  },
  {
    id: "changeofbasis",
    title: "Unit 6: Change of Basis",
    topics: [
      { id: "cob-coords", title: "Coordinates relative to a basis" },
      { id: "cob-matrix", title: "The change-of-basis matrix" },
      { id: "cob-transform", title: "Matrix of a transformation in another basis" }
    ]
  },
  {
    id: "posdef",
    title: "Unit 7: Positive Definite Matrices",
    topics: [
      { id: "pd-eigtest", title: "Definition & the eigenvalue test" },
      { id: "pd-elimtest", title: "The elimination/pivot test" },
      { id: "pd-ldl", title: "LDL^T and Cholesky factorization" },
      { id: "pd-ata", title: "A^T A, covariance, and least squares connections" }
    ]
  },
  {
    id: "svd",
    title: "Unit 8: Singular Value Decomposition",
    topics: [
      { id: "svd-basics", title: "The SVD and singular values" },
      { id: "svd-compute", title: "Computing the SVD" },
      { id: "svd-pseudoinv", title: "Pseudoinverse & minimum-norm solutions" },
      { id: "svd-lowrank", title: "Low-rank approximation & applications (PCA, compression)" }
    ]
  },
  {
    id: "graphs",
    title: "Unit 9: Graphs, Networks & Markov Chains",
    topics: [
      { id: "gr-adjacency", title: "Adjacency & degree matrices" },
      { id: "gr-incidence", title: "Incidence matrix & the graph Laplacian" },
      { id: "gr-spectral", title: "Laplacian eigenvalues & spectral partitioning" },
      { id: "gr-electrical", title: "Electrical networks" },
      { id: "gr-markov", title: "Random walks, Markov chains & PageRank" }
    ]
  }
];

const QUESTION_TYPES = [
  { id: "computation", title: "Computation" },
  { id: "conceptual", title: "Conceptual (short answer / true-false)" },
  { id: "multiplechoice", title: "Multiple choice" },
  { id: "justify", title: "Justify / prove" },
  { id: "applied", title: "Applied / word problem" }
];

const DIFFICULTIES = [
  { id: 1, title: "Foundational" },
  { id: 2, title: "Standard" },
  { id: 3, title: "Challenge" }
];
