/* Computational problem generators, one (or more) per topic.
   Every generator has the signature (rng, difficulty) -> Question, where
   Question = {
     unitId, topicId, type: "computation", difficulty,
     title: string,
     statement: [textLine|monoLines...],
     answer:    [textLine|monoLines...]
   }
   All arithmetic is exact (Frac), so answers never show floating point noise. */

const GENERATORS = {};

function Q(unitId, topicId, title, statement, answer) {
  return { unitId, topicId, type: "computation", title, statement, answer };
}

// ---------- shared construction helpers ----------

function elementaryShear(n, rng, maxOff) {
  const M = identity(n);
  let i = randInt(rng, 0, n - 1), j;
  do { j = randInt(rng, 0, n - 1); } while (j === i);
  M[i][j] = F(randNonZeroInt(rng, -maxOff, maxOff));
  return M;
}

function unimodular(n, rng, count) {
  let P = identity(n);
  for (let k = 0; k < count; k++) P = matMul(P, elementaryShear(n, rng, 2));
  return P;
}

// Builds an integer matrix A = P D P^-1 with prescribed eigenvalues (via a
// unimodular integer change of basis, so A always comes out integer-valued).
function similarEigenMatrix(rng, n, eigenvalues) {
  const D = identity(n);
  for (let i = 0; i < n; i++) D[i][i] = F(eigenvalues[i]);
  const P = unimodular(n, rng, n === 2 ? 3 : 5);
  const Pinv = inverse(P);
  const A = matMul(matMul(P, D), Pinv);
  return { A, P, D, Pinv };
}

const PY_TRIPLES = [[3, 4, 5], [6, 8, 10], [5, 12, 13], [8, 15, 17]];

// Builds a symmetric 2x2 integer matrix with prescribed integer eigenvalues
// lo = center - r*k, hi = center + r*k, using a scaled Pythagorean triple so
// the discriminant of the characteristic polynomial is a perfect square.
function symmetricFromEigenGap(rng, center, k) {
  const [p, q, r] = pick(rng, PY_TRIPLES);
  const a = center + p * k, d = center - p * k, b = q * k;
  const A = matFromInts([[a, b], [b, d]]);
  return { A, lo: center - r * k, hi: center + r * k, p, q, r, k };
}

function eigenvector2(A, lam) {
  // Solve (A - lam I) v = 0 for a 2x2 matrix.
  const a = A[0][0].sub(lam), b = A[0][1], c = A[1][0], d = A[1][1].sub(lam);
  if (!a.isZero() || !b.isZero()) {
    if (!b.isZero()) return [b.neg(), a];
    return [d.neg(), c];
  }
  if (!c.isZero() || !d.isZero()) {
    if (!d.isZero()) return [d.neg(), c];
    return [b.neg(), a];
  }
  return [F(1), F(0)];
}

function charPoly2Text(A) {
  // det(A - lambda I) = lambda^2 - trace*lambda + det
  const tr = trace(A), dt = determinant(A);
  return `lambda^2 - (${tr.toString()})*lambda + (${dt.toString()}) = 0`;
}

// ---------- Unit 1: Vectors & Vector Spaces ----------

GENERATORS["vec-ops"] = (rng, diff) => {
  const dim = diff === 1 ? 2 : 3;
  const rangeMax = 4 + diff * 2;
  const u = vecFromInts(Array.from({ length: dim }, () => randInt(rng, -rangeMax, rangeMax)));
  const v = vecFromInts(Array.from({ length: dim }, () => randInt(rng, -rangeMax, rangeMax)));
  const c1 = randNonZeroInt(rng, -3, 3), c2 = diff >= 2 ? randNonZeroInt(rng, -3, 3) : 1;
  const result = u.map((ui, i) => ui.mul(F(c1)).add(v[i].mul(F(c2))));
  const statement = [
    textLine(`Let u = ${tupleStr(u)} and v = ${tupleStr(v)}.`),
    textLine(diff >= 2
      ? `Compute the linear combination w = ${c1}u + ${c2}v.`
      : `Compute w = u + v and w' = u - v.`)
  ];
  const answer = diff >= 2
    ? [textLine(`w = ${tupleStr(result)}`)]
    : [
        textLine(`u + v = ${tupleStr(u.map((ui, i) => ui.add(v[i])))}`),
        textLine(`u - v = ${tupleStr(u.map((ui, i) => ui.sub(v[i])))}`)
      ];
  return Q("vectors", "vec-ops", "Vector arithmetic", statement, answer);
};

GENERATORS["vec-dot"] = (rng, diff) => {
  const dim = diff === 3 ? 3 : 2;
  const u = vecFromInts(Array.from({ length: dim }, () => randInt(rng, -6, 6)));
  const v = vecFromInts(Array.from({ length: dim }, () => randInt(rng, -6, 6)));
  const dot = u.reduce((s, ui, i) => s.add(ui.mul(v[i])), F(0));
  const statement = [textLine(`Let u = ${tupleStr(u)} and v = ${tupleStr(v)}.`)];
  const answer = [];
  if (diff === 1) {
    statement.push(textLine("Compute u . v."));
    answer.push(textLine(`u . v = ${dot.toString()}`));
  } else if (diff === 2) {
    statement.push(textLine("Compute u . v and the length |u|."));
    const lenSqU = u.reduce((s, ui) => s.add(ui.mul(ui)), F(0));
    answer.push(textLine(`u . v = ${dot.toString()}`));
    answer.push(textLine(`|u| = sqrt(${lenSqU.toString()})`));
  } else {
    statement.push(textLine("Compute u . v, then state whether u and v are orthogonal, and find a unit vector in the direction of u."));
    const lenSqU = u.reduce((s, ui) => s.add(ui.mul(ui)), F(0));
    answer.push(textLine(`u . v = ${dot.toString()} -> ${dot.isZero() ? "orthogonal" : "not orthogonal"}`));
    answer.push(textLine(`|u| = sqrt(${lenSqU.toString()})`));
    answer.push(textLine(`unit vector = (1/sqrt(${lenSqU.toString()})) * ${tupleStr(u)}`));
  }
  return Q("vectors", "vec-dot", "Dot product & length", statement, answer);
};

GENERATORS["vec-cross"] = (rng, diff) => {
  const u = vecFromInts(Array.from({ length: 3 }, () => randInt(rng, -4 - diff, 4 + diff)));
  const v = vecFromInts(Array.from({ length: 3 }, () => randInt(rng, -4 - diff, 4 + diff)));
  const cross = [
    u[1].mul(v[2]).sub(u[2].mul(v[1])),
    u[2].mul(v[0]).sub(u[0].mul(v[2])),
    u[0].mul(v[1]).sub(u[1].mul(v[0]))
  ];
  const statement = [
    textLine(`Let u = ${tupleStr(u)} and v = ${tupleStr(v)}.`),
    textLine(diff >= 3
      ? "Compute u x v and the area of the parallelogram spanned by u and v (as |u x v|, left in simplified radical form)."
      : "Compute the cross product u x v.")
  ];
  const answer = [textLine(`u x v = ${tupleStr(cross)}`)];
  if (diff >= 3) {
    const lenSq = cross.reduce((s, c) => s.add(c.mul(c)), F(0));
    answer.push(textLine(`area = |u x v| = sqrt(${lenSq.toString()})`));
  }
  return Q("vectors", "vec-cross", "Cross product", statement, answer);
};

GENERATORS["vec-span"] = (rng, diff) => {
  const dim = diff === 1 ? 2 : 3;
  const nvecs = diff === 3 ? 3 : 2;
  const cols = [];
  for (let i = 0; i < nvecs; i++) cols.push(vecFromInts(Array.from({ length: dim }, () => randInt(rng, -4, 4))));
  const coeffs = Array.from({ length: nvecs }, () => randInt(rng, -2, 2) || 1);
  const target = Array.from({ length: dim }, (_, i) => cols.reduce((s, c, j) => s.add(c[i].mul(F(coeffs[j]))), F(0)));
  const A = [];
  for (let i = 0; i < dim; i++) A.push(cols.map(c => c[i]));
  const statement = [
    ...cols.map((c, i) => textLine(`v${i + 1} = ${tupleStr(c)}`)),
    textLine(`b = ${tupleStr(target)}`),
    textLine(`Determine whether b is in span{${cols.map((_, i) => "v" + (i + 1)).join(", ")}}. If so, write b as a linear combination of the v_i.`)
  ];
  const res = solveLinearSystem(A, target);
  const answer = [monoLines(labeledMatrix("A", A)), textLine("Row reduce [A | b]:")];
  if (res.type === "unique") {
    answer.push(textLine(`b IS in the span. b = ${res.x.map((c, i) => `${c.toString()}*v${i + 1}`).join(" + ")}`));
  } else if (res.type === "infinite") {
    answer.push(textLine("b IS in the span (infinitely many ways to write it as a combination)."));
  } else {
    answer.push(textLine("b is NOT in the span (the system Ax = b is inconsistent)."));
  }
  return Q("vectors", "vec-span", "Linear combinations & span", statement, answer);
};

GENERATORS["vec-subspace"] = (rng, diff) => {
  const forms = [
    { desc: (a, b) => `W = {(x, y, z) in R^3 : ${a}x + ${b}y - z = 0}`, isSub: true, coef: [1, 1] },
    { desc: (a, b) => `W = {(x, y) in R^2 : xy = 0}`, isSub: false },
    { desc: (a, b) => `W = {(x, y, z) in R^3 : x + y + z = ${a}}`, isSub: false, coef: [1] },
    { desc: (a, b) => `W = {(x, y) in R^2 : y = ${a}x^2}`, isSub: false, coef: [1] }
  ];
  const shape = diff === 1 ? forms[0] : pick(rng, forms);
  const a = randInt(rng, 1, 3), b = randInt(rng, 1, 3);
  const statement = [
    textLine(shape.desc(a, b)),
    textLine("Determine whether W is a subspace of the ambient vector space. Justify by checking: (i) 0 in W, (ii) closure under addition, (iii) closure under scalar multiplication.")
  ];
  const answer = [];
  if (shape.isSub) {
    answer.push(textLine("W IS a subspace."));
    answer.push(textLine(`0 = (0,0,0) satisfies ${a}(0)+${b}(0)-0=0. ✓`));
    answer.push(textLine(`If ${a}x1+${b}y1-z1=0 and ${a}x2+${b}y2-z2=0, adding gives ${a}(x1+x2)+${b}(y1+y2)-(z1+z2)=0. ✓`));
    answer.push(textLine(`Scaling by k: ${a}(kx)+${b}(ky)-(kz)=k(${a}x+${b}y-z)=0. ✓`));
  } else {
    answer.push(textLine("W is NOT a subspace."));
    answer.push(textLine("A specific counterexample (closure under addition or the zero vector) fails; e.g. two elements of W can be found whose sum leaves W, or 0 is not in W when the defining equation is inhomogeneous or nonlinear."));
  }
  return Q("vectors", "vec-subspace", "The subspace test", statement, answer);
};

function matrixSizeForDiff(diff) {
  if (diff === 1) return [2, 3];
  if (diff === 2) return [3, 3];
  return [3, 4];
}

GENERATORS["vec-colnullrow"] = (rng, diff) => {
  const [m, n] = matrixSizeForDiff(diff);
  let A;
  do {
    A = matFromInts(Array.from({ length: m }, () => Array.from({ length: n }, () => randInt(rng, -3, 3))));
  } while (rref(A).rank === 0);
  const statement = [
    monoLines(labeledMatrix("A", A)),
    textLine("Find a basis for Col(A), a basis for Null(A), and a basis for Row(A).")
  ];
  const colB = colSpaceBasis(A), nullB = nullSpaceBasis(A), rowB = rowSpaceBasis(A);
  const answer = [
    textLine(`rank(A) = ${colB.length}`),
    monoLines(colB.length ? colB.map((v, i) => labeledColVector("c" + (i + 1), v)).flat() : ["Col(A) = {0}"]),
    textLine(""),
    monoLines(nullB.length ? nullB.map((v, i) => labeledColVector("n" + (i + 1), v)).flat() : ["Null(A) = {0}"]),
    textLine(""),
    monoLines(rowB.length ? rowB.map((v, i) => "r" + (i + 1) + " = " + tupleStr(v)) : ["Row(A) = {0}"])
  ];
  return Q("vectors", "vec-colnullrow", "Column, null & row space", statement, answer);
};

GENERATORS["vec-basis"] = (rng, diff) => {
  const dim = diff === 1 ? 2 : 3;
  const count = diff === 3 ? 4 : 3;
  const cols = Array.from({ length: count }, () => vecFromInts(Array.from({ length: dim }, () => randInt(rng, -3, 3))));
  const A = [];
  for (let i = 0; i < dim; i++) A.push(cols.map(c => c[i]));
  const { pivotCols, rank } = rref(A);
  const statement = [
    ...cols.map((c, i) => textLine(`v${i + 1} = ${tupleStr(c)}`)),
    textLine("Find a basis for span{v1, ..., v" + count + "} and state its dimension.")
  ];
  const answer = [
    textLine(`dim(span) = rank = ${rank}`),
    textLine(`A basis is {${pivotCols.map(c => "v" + (c + 1)).join(", ")}} (the other vectors are linear combinations of these).`)
  ];
  return Q("vectors", "vec-basis", "Basis & dimension", statement, answer);
};

GENERATORS["vec-rank"] = (rng, diff) => {
  const [m, n] = matrixSizeForDiff(diff);
  const A = matFromInts(Array.from({ length: m }, () => Array.from({ length: n }, () => randInt(rng, -3, 3))));
  const { rank } = rref(A);
  const statement = [monoLines(labeledMatrix("A", A)), textLine(`A is ${m}x${n}. Find rank(A) and nullity(A), and verify the Rank-Nullity Theorem.`)];
  const answer = [
    textLine(`rank(A) = ${rank}`),
    textLine(`nullity(A) = n - rank(A) = ${n} - ${rank} = ${n - rank}`),
    textLine(`Check: rank + nullity = ${rank} + ${n - rank} = ${n} = number of columns. ✓`)
  ];
  return Q("vectors", "vec-rank", "Rank & nullity", statement, answer);
};

GENERATORS["vec-fourspaces"] = (rng, diff) => {
  const [m, n] = diff === 1 ? [2, 3] : diff === 2 ? [3, 3] : [3, 4];
  let A;
  do {
    A = matFromInts(Array.from({ length: m }, () => Array.from({ length: n }, () => randInt(rng, -3, 3))));
  } while (rref(A).rank < 1);
  const AT = transpose(A);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Find a basis for each of the four fundamental subspaces: Col(A), Null(A), Row(A), Null(A^T).")];
  const col = colSpaceBasis(A), nul = nullSpaceBasis(A), row = rowSpaceBasis(A), nulT = nullSpaceBasis(AT);
  const answer = [
    textLine(`rank(A) = ${col.length}`),
    textLine("Col(A) basis: " + (col.length ? col.map(v => tupleStr(v)).join(", ") : "{0}")),
    textLine("Null(A) basis: " + (nul.length ? nul.map(v => tupleStr(v)).join(", ") : "{0}")),
    textLine("Row(A) basis: " + (row.length ? row.map(v => tupleStr(v)).join(", ") : "{0}")),
    textLine("Null(A^T) basis: " + (nulT.length ? nulT.map(v => tupleStr(v)).join(", ") : "{0}"))
  ];
  return Q("vectors", "vec-fourspaces", "Four fundamental subspaces", statement, answer);
};

// ---------- Unit 2: Linear Transformations & Matrix Algebra ----------

const T2 = {
  rotation90: [[0, -1], [1, 0]],
  reflectX: [[1, 0], [0, -1]],
  reflectY: [[-1, 0], [0, 1]],
  projX: [[1, 0], [0, 0]],
  dilate: (k) => [[k, 0], [0, k]]
};

GENERATORS["mat-lintrans"] = (rng, diff) => {
  const names = ["rotation90", "reflectX", "reflectY"];
  const name = diff === 3 ? "dilate" : pick(rng, names);
  const k = randInt(rng, 2, 3);
  const M = matFromInts(name === "dilate" ? T2.dilate(k) : T2[name]);
  const v = vecFromInts([randInt(rng, -4, 4), randInt(rng, -4, 4)]);
  const label = name === "rotation90" ? "a 90-degree counterclockwise rotation"
    : name === "reflectX" ? "a reflection across the x-axis"
    : name === "reflectY" ? "a reflection across the y-axis"
    : `a dilation by factor ${k}`;
  const statement = [
    textLine(`T : R^2 -> R^2 is ${label}, with standard matrix A.`),
    textLine(`Let v = ${tupleStr(v)}. Compute A and T(v) = Av.`)
  ];
  const Tv = matVec(M, v);
  const answer = [monoLines(labeledMatrix("A", M)), textLine(`T(v) = ${tupleStr(Tv)}`)];
  if (diff >= 2) {
    const u = vecFromInts([randInt(rng, -4, 4), randInt(rng, -4, 4)]);
    const lhs = matVec(M, u.map((ui, i) => ui.add(v[i])));
    const rhs = matVec(M, u).map((x, i) => x.add(matVec(M, v)[i]));
    statement.push(textLine(`Also let u = ${tupleStr(u)}. Verify T(u+v) = T(u) + T(v).`));
    answer.push(textLine(`T(u+v) = ${tupleStr(lhs)}, T(u)+T(v) = ${tupleStr(rhs)} -> equal, confirming linearity.`));
  }
  return Q("matrices", "mat-lintrans", "Linear transformations", statement, answer);
};

GENERATORS["mat-repr"] = (rng, diff) => {
  const dim = diff === 3 ? 3 : 2;
  const images = Array.from({ length: dim }, () => vecFromInts(Array.from({ length: dim }, () => randInt(rng, -4, 4))));
  const A = [];
  for (let i = 0; i < dim; i++) A.push(images.map(im => im[i]));
  const basisNames = dim === 2 ? ["e1", "e2"] : ["e1", "e2", "e3"];
  const statement = [
    textLine(`A linear transformation T satisfies:`),
    ...images.map((im, i) => textLine(`T(${basisNames[i]}) = ${tupleStr(im)}`)),
    textLine("Find the standard matrix A of T.")
  ];
  const answer = [monoLines(labeledMatrix("A", A)), textLine("(Each T(e_i) becomes column i of A.)")];
  return Q("matrices", "mat-repr", "Matrix of a transformation", statement, answer);
};

GENERATORS["mat-addsub"] = (rng, diff) => {
  const n = diff === 1 ? 2 : 3;
  const A = matFromInts(Array.from({ length: n }, () => Array.from({ length: n }, () => randInt(rng, -5, 5))));
  const B = matFromInts(Array.from({ length: n }, () => Array.from({ length: n }, () => randInt(rng, -5, 5))));
  const k = randNonZeroInt(rng, -3, 3);
  const statement = [monoLines(labeledMatrix("A", A)), monoLines(labeledMatrix("B", B)), textLine(`Compute A + B, ${k}A, A^T, and trace(A).`)];
  const answer = [
    monoLines(labeledMatrix("A+B", matAdd(A, B))),
    monoLines(labeledMatrix(`${k}A`, matScale(A, k))),
    monoLines(labeledMatrix("A^T", transpose(A))),
    textLine(`trace(A) = ${trace(A).toString()}`)
  ];
  return Q("matrices", "mat-addsub", "Matrix addition, transpose & trace", statement, answer);
};

GENERATORS["mat-mult"] = (rng, diff) => {
  const n = diff === 1 ? 2 : 3;
  const A = matFromInts(Array.from({ length: n }, () => Array.from({ length: n }, () => randInt(rng, -4, 4))));
  const B = matFromInts(Array.from({ length: n }, () => Array.from({ length: n }, () => randInt(rng, -4, 4))));
  const statement = [monoLines(labeledMatrix("A", A)), monoLines(labeledMatrix("B", B)), textLine("Compute AB. " + (diff >= 2 ? "Then compute BA and state whether matrix multiplication is commutative here." : ""))];
  const answer = [monoLines(labeledMatrix("AB", matMul(A, B)))];
  if (diff >= 2) {
    const BA = matMul(B, A);
    answer.push(monoLines(labeledMatrix("BA", BA)));
    const same = A.every((row, i) => row.every((_, j) => matMul(A, B)[i][j].eq(BA[i][j])));
    answer.push(textLine(same ? "Here AB = BA." : "AB != BA, so matrix multiplication is not commutative in general."));
  }
  return Q("matrices", "mat-mult", "Matrix multiplication", statement, answer);
};

GENERATORS["mat-elim"] = (rng, diff) => {
  const [m, n] = diff === 1 ? [2, 3] : diff === 2 ? [3, 3] : [3, 4];
  const A = matFromInts(Array.from({ length: m }, () => Array.from({ length: n }, () => randInt(rng, -4, 4))));
  const steps = [];
  const { R } = rref(A, steps);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Use elimination (Gauss-Jordan) to reduce A to reduced row echelon form. Show your row operations.")];
  const answer = [textLine("Row operations:"), ...steps.map(s => textLine("  " + s)), textLine(""), monoLines(labeledMatrix("rref(A)", R))];
  return Q("matrices", "mat-elim", "Elimination & row echelon form", statement, answer);
};

GENERATORS["mat-inverse"] = (rng, diff) => {
  const n = diff === 1 ? 2 : 3;
  let A, singular = diff === 3 && rng() < 0.35;
  if (singular) {
    const row1 = Array.from({ length: n }, () => randInt(rng, -3, 3));
    const k = randNonZeroInt(rng, -2, 2);
    const row2 = row1.map(x => x * k);
    const rest = Array.from({ length: n - 2 }, () => Array.from({ length: n }, () => randInt(rng, -3, 3)));
    A = matFromInts([row1, row2, ...rest]);
  } else {
    do {
      A = matFromInts(Array.from({ length: n }, () => Array.from({ length: n }, () => randInt(rng, -3, 3))));
    } while (determinant(A).isZero());
  }
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Find A^-1 using Gauss-Jordan elimination on [A | I], or explain why A is not invertible.")];
  const inv = inverse(A);
  const answer = inv
    ? [monoLines(labeledMatrix("A^-1", inv)), textLine(`(det(A) = ${determinant(A).toString()} != 0, so A is invertible.)`)]
    : [textLine(`det(A) = 0 (row 2 is a scalar multiple of row 1), so A has no inverse.`)];
  return Q("matrices", "mat-inverse", "Matrix inverses", statement, answer);
};

GENERATORS["mat-lu"] = (rng, diff) => {
  const n = diff === 1 ? 2 : 3;
  // Build A as L*U directly (guarantees no row swaps are needed).
  const L = identity(n);
  for (let i = 1; i < n; i++) for (let j = 0; j < i; j++) L[i][j] = F(randInt(rng, -2, 2));
  const U = identity(n);
  for (let i = 0; i < n; i++) U[i][i] = F(randNonZeroInt(rng, 1, 3));
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) U[i][j] = F(randInt(rng, -3, 3));
  const A = matMul(L, U);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Factor A = LU using elimination, where L is lower triangular with 1's on the diagonal.")];
  const answer = [monoLines(labeledMatrix("L", L)), monoLines(labeledMatrix("U", U))];
  return Q("matrices", "mat-lu", "LU factorization", statement, answer);
};

GENERATORS["mat-axb"] = (rng, diff) => {
  const n = diff === 1 ? 2 : 3;
  let A, b, x;
  if (diff === 3 && rng() < 0.5) {
    // Force a dependent system for infinite/no-solution practice.
    const row1 = Array.from({ length: n }, () => randInt(rng, -3, 3));
    const k = randNonZeroInt(rng, -2, 2);
    A = matFromInts([row1, row1.map(v => v * k), ...(n > 2 ? [Array.from({ length: n }, () => randInt(rng, -3, 3))] : [])]);
    b = vecFromInts(Array.from({ length: n }, () => randInt(rng, -5, 5)));
  } else {
    do {
      A = matFromInts(Array.from({ length: n }, () => Array.from({ length: n }, () => randInt(rng, -4, 4))));
    } while (determinant(A).isZero());
    x = vecFromInts(Array.from({ length: n }, () => randInt(rng, -3, 3)));
    b = matVec(A, x);
  }
  const statement = [monoLines(labeledMatrix("A", A)), textLine(`b = ${tupleStr(b)}`), textLine("Solve Ax = b. State whether the solution is unique, there are infinitely many, or there is no solution.")];
  const res = solveLinearSystem(A, b);
  const answer = [];
  if (res.type === "unique") answer.push(textLine(`Unique solution: x = ${tupleStr(res.x)}`));
  else if (res.type === "none") answer.push(textLine("No solution: the reduced system has a row like [0 0 ... 0 | c] with c != 0."));
  else answer.push(textLine("Infinitely many solutions (a free variable remains after elimination)."));
  return Q("matrices", "mat-axb", "Solving Ax = b", statement, answer);
};

GENERATORS["mat-rect"] = (rng, diff) => {
  const overdetermined = diff !== 3;
  const [m, n] = overdetermined ? [3, 2] : [2, 3];
  const A = matFromInts(Array.from({ length: m }, () => Array.from({ length: n }, () => randInt(rng, -3, 3))));
  let b;
  if (overdetermined) {
    const x = vecFromInts(Array.from({ length: n }, () => randInt(rng, -3, 3)));
    b = matVec(A, x);
    if (diff === 2) b = b.map(v => v.add(F(randInt(rng, 1, 2))));
  } else {
    b = vecFromInts(Array.from({ length: m }, () => randInt(rng, -4, 4)));
  }
  const statement = [monoLines(labeledMatrix("A", A)), textLine(`b = ${tupleStr(b)}`), textLine(overdetermined
    ? "This is an overdetermined system (more equations than unknowns). Determine whether Ax = b is consistent."
    : "This is an underdetermined system (fewer equations than unknowns). Describe the solution set of Ax = b using a free parameter.")];
  const res = solveLinearSystem(A, b);
  const answer = [];
  if (res.type === "unique") answer.push(textLine(`Consistent, unique solution x = ${tupleStr(res.x)}.`));
  else if (res.type === "none") answer.push(textLine("Inconsistent: no x satisfies Ax = b."));
  else answer.push(textLine("Consistent with infinitely many solutions; express the free variable(s) as parameter(s) and back-substitute for the rest."));
  return Q("matrices", "mat-rect", "Rectangular systems", statement, answer);
};

// ---------- Unit 3: Determinants ----------

GENERATORS["det-area"] = (rng, diff) => {
  const A = matFromInts([[randInt(rng, -5, 5), randInt(rng, -5, 5)], [randInt(rng, -5, 5), randInt(rng, -5, 5)]]);
  const d = det2(A);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("The columns of A span a parallelogram. Find det(A), the area of the parallelogram, and state the orientation (same or reversed) of the basis.")];
  const answer = [
    textLine(`det(A) = ${d.toString()}`),
    textLine(`area = |det(A)| = ${d.abs().toString()}`),
    textLine(d.cmp(0) >= 0 ? "Orientation preserved (det > 0)." : "Orientation reversed (det < 0).")
  ];
  return Q("determinants", "det-area", "Determinant as area", statement, answer);
};

GENERATORS["det-props"] = (rng, diff) => {
  const n = diff === 1 ? 2 : 3;
  const d0 = randNonZeroInt(rng, 2, 9);
  const ops = [
    { text: "swapping two rows", factor: -1 },
    { text: `scaling one row by ${randNonZeroInt(rng, -3, 3)}`, factor: null },
    { text: "adding a multiple of one row to another", factor: 1 }
  ];
  const op = pick(rng, ops);
  let k = 0;
  if (op.factor === null) { k = randNonZeroInt(rng, -3, 3); }
  const statement = [
    textLine(`A is a ${n}x${n} matrix with det(A) = ${d0}.`),
    textLine(`Matrix B is obtained from A by ${op.text}. Find det(B).`)
  ];
  let newDet;
  if (op.text.startsWith("swapping")) newDet = -d0;
  else if (op.text.startsWith("scaling")) newDet = d0 * k;
  else newDet = d0;
  const answer = [textLine(`det(B) = ${newDet}`), textLine(op.text.startsWith("swapping") ? "(A row swap negates the determinant.)"
    : op.text.startsWith("scaling") ? `(Scaling a single row by k multiplies det by k: ${d0} * ${k} = ${newDet}.)`
    : "(Adding a multiple of one row to another leaves det unchanged.)")];
  return Q("determinants", "det-props", "Properties of determinants", statement, answer);
};

GENERATORS["det-cofactor"] = (rng, diff) => {
  const A = matFromInts(Array.from({ length: 3 }, () => Array.from({ length: 3 }, () => randInt(rng, -4, 4))));
  const row = diff === 3 ? randInt(rng, 0, 2) : 0;
  const statement = [monoLines(labeledMatrix("A", A)), textLine(`Compute det(A) by cofactor expansion along row ${row + 1}.`)];
  const terms = [];
  let total = F(0);
  for (let j = 0; j < 3; j++) {
    const minor = A.filter((_, r) => r !== row).map(r => r.filter((_, c) => c !== j));
    const m = determinant(minor);
    const sign = ((row + j) % 2 === 0) ? 1 : -1;
    const term = A[row][j].mul(m).mul(F(sign));
    total = total.add(term);
    terms.push(`(${sign === 1 ? "+" : "-"}) (${A[row][j].toString()}) * (${m.toString()}) = ${term.toString()}`);
  }
  const answer = [...terms.map(t => textLine(t)), textLine(`det(A) = ${total.toString()}`)];
  return Q("determinants", "det-cofactor", "Cofactor expansion", statement, answer);
};

GENERATORS["det-invert"] = (rng, diff) => {
  const n = diff === 1 ? 2 : 3;
  const A = matFromInts(Array.from({ length: n }, () => Array.from({ length: n }, () => randInt(rng, -3, 3))));
  const d = determinant(A);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Compute det(A) and determine whether A is invertible.")];
  const answer = [textLine(`det(A) = ${d.toString()}`), textLine(d.isZero() ? "A is NOT invertible (det = 0)." : "A IS invertible (det != 0).")];
  return Q("determinants", "det-invert", "Determinants & invertibility", statement, answer);
};

GENERATORS["det-cramer"] = (rng, diff) => {
  const n = diff === 3 ? 3 : 2;
  let A;
  do { A = matFromInts(Array.from({ length: n }, () => Array.from({ length: n }, () => randInt(rng, -3, 3)))); } while (determinant(A).isZero());
  const x = vecFromInts(Array.from({ length: n }, () => randInt(rng, -3, 3)));
  const b = matVec(A, x);
  const d = determinant(A);
  const statement = [monoLines(labeledMatrix("A", A)), textLine(`b = ${tupleStr(b)}`), textLine("Solve Ax = b using Cramer's Rule.")];
  const answer = [textLine(`det(A) = ${d.toString()}`)];
  for (let i = 0; i < n; i++) {
    const Ai = A.map((row, r) => row.map((v, c) => c === i ? b[r] : v));
    const di = determinant(Ai);
    answer.push(textLine(`det(A_${i + 1}) = ${di.toString()}  ->  x${i + 1} = ${di.toString()}/${d.toString()} = ${di.div(d).toString()}`));
  }
  return Q("determinants", "det-cramer", "Cramer's Rule", statement, answer);
};

GENERATORS["det-products"] = (rng, diff) => {
  const n = diff === 1 ? 2 : 3;
  const detA = randNonZeroInt(rng, -5, 5), detB = randNonZeroInt(rng, -5, 5);
  const k = randNonZeroInt(rng, -3, 3);
  const statement = [
    textLine(`A and B are ${n}x${n} matrices with det(A) = ${detA} and det(B) = ${detB}.`),
    textLine(`Find det(AB), det(A^T), det(${k}A), and det(A^-1).`)
  ];
  const answer = [
    textLine(`det(AB) = det(A)*det(B) = ${detA}*${detB} = ${detA * detB}`),
    textLine(`det(A^T) = det(A) = ${detA}`),
    textLine(`det(${k}A) = ${k}^${n} * det(A) = ${Math.pow(k, n)} * ${detA} = ${Math.pow(k, n) * detA}`),
    textLine(`det(A^-1) = 1/det(A) = 1/${detA}`)
  ];
  return Q("determinants", "det-products", "Determinants of products", statement, answer);
};

// ---------- Unit 4: Orthogonality & Least Squares ----------

GENERATORS["orth-sets"] = (rng, diff) => {
  const orthogonal = rng() < 0.6;
  let u, v;
  if (orthogonal) {
    const a = randNonZeroInt(rng, -4, 4), b = randNonZeroInt(rng, -4, 4);
    u = vecFromInts([a, b]); v = vecFromInts([-b, a]);
  } else {
    u = vecFromInts([randInt(rng, -4, 4), randInt(rng, -4, 4)]);
    v = vecFromInts([randInt(rng, -4, 4), randInt(rng, -4, 4)]);
  }
  const dot = u[0].mul(v[0]).add(u[1].mul(v[1]));
  const statement = [textLine(`u = ${tupleStr(u)}, v = ${tupleStr(v)}`), textLine("Determine whether {u, v} is an orthogonal set. If it is, also state whether it is orthonormal.")];
  const nu = u[0].mul(u[0]).add(u[1].mul(u[1])), nv = v[0].mul(v[0]).add(v[1].mul(v[1]));
  const answer = [textLine(`u . v = ${dot.toString()}`)];
  if (dot.isZero()) {
    answer.push(textLine("Orthogonal set. ✓"));
    answer.push(textLine(`|u|^2 = ${nu.toString()}, |v|^2 = ${nv.toString()} -> ${nu.eq(F(1)) && nv.eq(F(1)) ? "also orthonormal." : "not orthonormal (lengths are not 1)."}`));
  } else {
    answer.push(textLine("Not an orthogonal set (u . v != 0)."));
  }
  return Q("orthogonality", "orth-sets", "Orthogonal & orthonormal sets", statement, answer);
};

GENERATORS["orth-proj"] = (rng, diff) => {
  const dim = diff === 3 ? 3 : 2;
  const b = vecFromInts(Array.from({ length: dim }, () => randInt(rng, -5, 5)));
  const a = vecFromInts(Array.from({ length: dim }, () => randNonZeroInt(rng, -4, 4)));
  const dot = a.reduce((s, ai, i) => s.add(ai.mul(b[i])), F(0));
  const normSq = a.reduce((s, ai) => s.add(ai.mul(ai)), F(0));
  const scalar = dot.div(normSq);
  const proj = a.map(ai => ai.mul(scalar));
  const statement = [textLine(`a = ${tupleStr(a)}, b = ${tupleStr(b)}`), textLine("Find the orthogonal projection of b onto a, proj_a(b) = ((a.b)/(a.a)) a.")];
  const answer = [
    textLine(`a . b = ${dot.toString()}, a . a = ${normSq.toString()}`),
    textLine(`scalar = ${scalar.toString()}`),
    textLine(`proj_a(b) = ${tupleStr(proj)}`)
  ];
  return Q("orthogonality", "orth-proj", "Projection onto a vector", statement, answer);
};

GENERATORS["orth-complement"] = (rng, diff) => {
  const n = diff === 1 ? 2 : 3;
  const count = diff === 3 ? 2 : 1;
  const vecs = Array.from({ length: count }, () => vecFromInts(Array.from({ length: n }, () => randInt(rng, -3, 3))));
  const A = vecs.map(v => v.slice());
  const statement = [...vecs.map((v, i) => textLine(`v${i + 1} = ${tupleStr(v)}`)), textLine(`Let W = span{${vecs.map((_, i) => "v" + (i + 1)).join(", ")}} in R^${n}. Find a basis for W^perp (solve v_i . x = 0 for all i).`)];
  const basis = nullSpaceBasis(A);
  const answer = [monoLines(basis.length ? basis.map((v, i) => "w" + (i + 1) + " = " + tupleStr(v)) : ["W^perp = {0}"])];
  return Q("orthogonality", "orth-complement", "Orthogonal complements", statement, answer);
};

GENERATORS["orth-gramschmidt"] = (rng, diff) => {
  const dim = diff === 3 ? 3 : 2;
  const count = diff === 3 ? 3 : 2;
  const dotp = (a, b) => a.reduce((s, ai, i) => s.add(ai.mul(b[i])), F(0));
  // Retry if the random vectors turn out linearly dependent (or a stray
  // all-zero draw), which would divide by zero partway through Gram-Schmidt.
  function isDegenerate(candidateVecs) {
    const built = [];
    for (let i = 0; i < candidateVecs.length; i++) {
      let u = candidateVecs[i].slice();
      for (let j = 0; j < built.length; j++) {
        if (dotp(built[j], built[j]).isZero()) return true;
        const scalar = dotp(built[j], candidateVecs[i]).div(dotp(built[j], built[j]));
        u = u.map((c, k) => c.sub(built[j][k].mul(scalar)));
      }
      if (u.every(c => c.isZero())) return true;
      built.push(u);
    }
    return false;
  }
  let vecs;
  do {
    vecs = Array.from({ length: count }, () => vecFromInts(Array.from({ length: dim }, () => randInt(rng, -3, 3))));
  } while (isDegenerate(vecs));
  const statement = [...vecs.map((v, i) => textLine(`v${i + 1} = ${tupleStr(v)}`)), textLine("Apply the Gram-Schmidt process to produce an orthogonal basis {u1, u2" + (count === 3 ? ", u3" : "") + "}.")];
  const us = [];
  const answer = [];
  for (let i = 0; i < count; i++) {
    let u = vecs[i].slice();
    const parts = [];
    for (let j = 0; j < us.length; j++) {
      const scalar = dotp(us[j], vecs[i]).div(dotp(us[j], us[j]));
      u = u.map((c, k) => c.sub(us[j][k].mul(scalar)));
      parts.push(`proj_{u${j + 1}}(v${i + 1})`);
    }
    us.push(u);
    answer.push(textLine(`u${i + 1} = v${i + 1}` + (parts.length ? " - " + parts.join(" - ") : "") + ` = ${tupleStr(u)}`));
  }
  return Q("orthogonality", "orth-gramschmidt", "Gram-Schmidt process", statement, answer);
};

GENERATORS["orth-qr"] = (rng, diff) => {
  // Build A with two independent integer columns; run Gram-Schmidt for Q's directions (left un-normalized to stay exact), then R = Q^T A style relation is described conceptually.
  const dim = 2;
  const v1 = vecFromInts([randNonZeroInt(rng, -4, 4), randInt(rng, -4, 4)]);
  const v2 = vecFromInts([randInt(rng, -4, 4), randNonZeroInt(rng, -4, 4)]);
  const A = [[v1[0], v2[0]], [v1[1], v2[1]]];
  const dotp = (a, b) => a[0].mul(b[0]).add(a[1].mul(b[1]));
  const u1 = v1;
  const scalar = dotp(u1, v2).div(dotp(u1, u1));
  const u2 = v2.map((c, k) => c.sub(u1[k].mul(scalar)));
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Using Gram-Schmidt on the columns of A, find an orthogonal basis {u1, u2} for Col(A), then write the (unnormalized) QR-style relation A = [u1 u2] R for upper triangular R.")];
  const r11 = dotp(u1, u1).div(dotp(u1,u1)); // 1, since u1=v1
  const r12 = scalar;
  const answer = [
    textLine(`u1 = v1 = ${tupleStr(u1)}`),
    textLine(`u2 = v2 - (${scalar.toString()})u1 = ${tupleStr(u2)}`),
    textLine(`So v2 = u2 + (${scalar.toString()})u1, giving R = [[1, ${scalar.toString()}], [0, 1]] with A = [u1 u2] R.`)
  ];
  return Q("orthogonality", "orth-qr", "QR factorization", statement, answer);
};

GENERATORS["orth-leastsquares"] = (rng, diff) => {
  const m = diff === 3 ? 4 : 3, n = 2;
  const A = matFromInts(Array.from({ length: m }, () => [randInt(rng, -3, 3) || 1, randInt(rng, 0, 3)]));
  const b = vecFromInts(Array.from({ length: m }, () => randInt(rng, -5, 5)));
  const AT = transpose(A);
  const ATA = matMul(AT, A);
  const ATb = matVec(AT, b);
  const res = solveLinearSystem(ATA, ATb);
  const statement = [monoLines(labeledMatrix("A", A)), textLine(`b = ${tupleStr(b)}`), textLine("Ax = b has no exact solution. Find the least-squares solution x-hat by solving the normal equations A^T A x = A^T b.")];
  const answer = [
    monoLines(labeledMatrix("A^T A", ATA)),
    textLine(`A^T b = ${tupleStr(ATb)}`),
    textLine(res.type === "unique" ? `x-hat = ${tupleStr(res.x)}` : "Solve the resulting 2x2 (or larger) system for x-hat.")
  ];
  return Q("orthogonality", "orth-leastsquares", "Least squares", statement, answer);
};

// ---------- Unit 5: Eigenvalues & Eigenvectors ----------

GENERATORS["eig-charpoly"] = (rng, diff) => {
  const n = diff === 3 ? 3 : 2;
  const eigenvalues = n === 2 ? shuffle(rng, [randInt(rng, -3, 3), randInt(rng, -3, 3)]) : [randInt(rng, -3, 3), randInt(rng, -3, 3), randInt(rng, -3, 3)];
  const { A } = similarEigenMatrix(rng, n, eigenvalues);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Find the characteristic polynomial of A and its eigenvalues.")];
  const answer = n === 2
    ? [textLine(`trace(A) = ${trace(A).toString()}, det(A) = ${determinant(A).toString()}`), textLine(`Characteristic equation: ${charPoly2Text(A)}`), textLine(`Eigenvalues: ${eigenvalues.join(", ")}`)]
    : [textLine(`By construction A = PDP^-1 with D = diag(${eigenvalues.join(", ")}), so these are the eigenvalues of A.`), textLine(`Verify: trace(A) = ${trace(A).toString()} = sum of eigenvalues = ${eigenvalues.reduce((a,b)=>a+b,0)}; det(A) = ${determinant(A).toString()} = product of eigenvalues = ${eigenvalues.reduce((a,b)=>a*b,1)}.`)];
  return Q("eigen", "eig-charpoly", "Characteristic polynomial & eigenvalues", statement, answer);
};

GENERATORS["eig-vectors"] = (rng, diff) => {
  const eigenvalues = shuffle(rng, [randInt(rng, -3, 3), randNonZeroInt(rng, -3, 3)]);
  while (eigenvalues[0] === eigenvalues[1]) eigenvalues[1] = randNonZeroInt(rng, -3, 3);
  const { A } = similarEigenMatrix(rng, 2, eigenvalues);
  const statement = [monoLines(labeledMatrix("A", A)), textLine(`A has eigenvalues ${eigenvalues[0]} and ${eigenvalues[1]}. Find a basis eigenvector for each eigenspace.`)];
  const answer = eigenvalues.map(lam => {
    const v = eigenvector2(A, F(lam));
    return textLine(`lambda = ${lam}: solve (A - ${lam}I)v = 0  ->  v = ${tupleStr(v)}`);
  });
  return Q("eigen", "eig-vectors", "Eigenvectors & eigenspaces", statement, answer);
};

GENERATORS["eig-diag"] = (rng, diff) => {
  const eigenvalues = shuffle(rng, [randInt(rng, -3, 3), randNonZeroInt(rng, -3, 3)]);
  while (eigenvalues[0] === eigenvalues[1]) eigenvalues[1] = randNonZeroInt(rng, -3, 3);
  const { A } = similarEigenMatrix(rng, 2, eigenvalues);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Diagonalize A: find an invertible P and diagonal D with A = PDP^-1.")];
  const P = [];
  const answer = [];
  for (const lam of eigenvalues) {
    const v = eigenvector2(A, F(lam));
    P.push(v);
    answer.push(textLine(`lambda = ${lam} -> eigenvector ${tupleStr(v)}`));
  }
  const Pmat = [[P[0][0], P[1][0]], [P[0][1], P[1][1]]];
  const D = [[F(eigenvalues[0]), F(0)], [F(0), F(eigenvalues[1])]];
  answer.push(monoLines(labeledMatrix("P", Pmat)));
  answer.push(monoLines(labeledMatrix("D", D)));
  return Q("eigen", "eig-diag", "Diagonalization", statement, answer);
};

GENERATORS["eig-powers"] = (rng, diff) => {
  const eigenvalues = [randInt(rng, 1, 3), randInt(rng, -2, 2)];
  while (eigenvalues[0] === eigenvalues[1]) eigenvalues[1] = randInt(rng, -2, 2);
  const { A } = similarEigenMatrix(rng, 2, eigenvalues);
  const power = diff === 1 ? 2 : diff === 2 ? 3 : 5;
  const statement = [monoLines(labeledMatrix("A", A)), textLine(`A has eigenvalues ${eigenvalues[0]} and ${eigenvalues[1]}. Using diagonalization, describe A^${power} in terms of P, D^${power}, P^-1, and state which eigen-direction dominates as the exponent grows.`)];
  const dominant = Math.abs(eigenvalues[0]) > Math.abs(eigenvalues[1]) ? eigenvalues[0] : eigenvalues[1];
  const answer = [
    textLine(`A^${power} = P D^${power} P^-1, where D^${power} = diag(${eigenvalues[0]}^${power}, ${eigenvalues[1]}^${power}) = diag(${Math.pow(eigenvalues[0], power)}, ${Math.pow(eigenvalues[1], power)}).`),
    textLine(`Since |${dominant}| is the larger eigenvalue in absolute value, the eigenvector for lambda = ${dominant} dominates the long-run behavior of A^k v for most starting vectors v.`)
  ];
  return Q("eigen", "eig-powers", "Powers of a matrix & dynamics", statement, answer);
};

GENERATORS["eig-symmetric"] = (rng, diff) => {
  const center = randInt(rng, -2, 2);
  const k = diff === 3 ? randInt(rng, 2, 3) : 1;
  const { A, lo, hi } = symmetricFromEigenGap(rng, center, k);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("A is symmetric. Find its eigenvalues, and verify that the eigenvectors for distinct eigenvalues are orthogonal.")];
  const v1 = eigenvector2(A, F(lo)), v2 = eigenvector2(A, F(hi));
  const dot = v1[0].mul(v2[0]).add(v1[1].mul(v2[1]));
  const answer = [
    textLine(`Eigenvalues: ${lo}, ${hi}`),
    textLine(`Eigenvector for ${lo}: ${tupleStr(v1)}`),
    textLine(`Eigenvector for ${hi}: ${tupleStr(v2)}`),
    textLine(`Dot product = ${dot.toString()} -> ${dot.isZero() ? "orthogonal, as guaranteed by the Spectral Theorem for symmetric matrices." : "check arithmetic."}`)
  ];
  return Q("eigen", "eig-symmetric", "Symmetric matrices & Spectral Theorem", statement, answer);
};

GENERATORS["eig-apps"] = (rng, diff) => {
  const eigenvalues = [randInt(rng, 2, 3), randInt(rng, -1, 1)];
  while (eigenvalues[0] === eigenvalues[1]) eigenvalues[1] = randInt(rng, -1, 1);
  const { A, P, D, Pinv } = similarEigenMatrix(rng, 2, eigenvalues);
  const x0 = vecFromInts([randInt(rng, 1, 4), randInt(rng, 1, 4)]);
  const statement = [
    textLine(`A population model follows x_{k+1} = A x_k with`),
    monoLines(labeledMatrix("A", A)),
    textLine(`and initial state x_0 = ${tupleStr(x0)}.`),
    textLine("Find x_1 and x_2, and describe the long-term behavior using the eigenvalues of A.")
  ];
  const x1 = matVec(A, x0);
  const x2 = matVec(A, x1);
  const dominant = Math.abs(eigenvalues[0]) > Math.abs(eigenvalues[1]) ? eigenvalues[0] : eigenvalues[1];
  const answer = [
    textLine(`x1 = A x0 = ${tupleStr(x1)}`),
    textLine(`x2 = A x1 = ${tupleStr(x2)}`),
    textLine(`Eigenvalues of A are ${eigenvalues.join(" and ")}; since |${dominant}| dominates, x_k grows/shrinks like ${dominant}^k along that eigen-direction for large k.`)
  ];
  return Q("eigen", "eig-apps", "Difference equations", statement, answer);
};

// ---------- Unit 6: Change of Basis ----------

GENERATORS["cob-coords"] = (rng, diff) => {
  const dim = diff === 3 ? 3 : 2;
  let B;
  do { B = matFromInts(Array.from({ length: dim }, () => Array.from({ length: dim }, () => randInt(rng, -3, 3)))); } while (determinant(B).isZero());
  const coords = vecFromInts(Array.from({ length: dim }, () => randInt(rng, -3, 3)));
  const v = matVec(B, coords);
  const statement = [monoLines(labeledMatrix("B", B)), textLine(`Let B's columns be a basis for R^${dim}, and let v = ${tupleStr(v)}.`), textLine("Find the coordinate vector [v]_B such that v = B[v]_B.")];
  const res = solveLinearSystem(B, v);
  const answer = [textLine(`Solve B x = v.`), textLine(`[v]_B = ${tupleStr(res.x)}`)];
  return Q("changeofbasis", "cob-coords", "Coordinates relative to a basis", statement, answer);
};

GENERATORS["cob-matrix"] = (rng, diff) => {
  let B1, B2;
  do { B1 = matFromInts(Array.from({ length: 2 }, () => Array.from({ length: 2 }, () => randInt(rng, -3, 3)))); } while (determinant(B1).isZero());
  do { B2 = matFromInts(Array.from({ length: 2 }, () => Array.from({ length: 2 }, () => randInt(rng, -3, 3)))); } while (determinant(B2).isZero());
  const statement = [monoLines(labeledMatrix("B1", B1)), monoLines(labeledMatrix("B2", B2)), textLine("B1 and B2 are two bases of R^2 (columns = basis vectors). Find the change-of-basis matrix P from B1-coordinates to B2-coordinates, i.e. P = B2^-1 B1.")];
  const B2inv = inverse(B2);
  const P = matMul(B2inv, B1);
  const answer = [monoLines(labeledMatrix("B2^-1", B2inv)), monoLines(labeledMatrix("P = B2^-1 B1", P))];
  return Q("changeofbasis", "cob-matrix", "Change-of-basis matrix", statement, answer);
};

GENERATORS["cob-transform"] = (rng, diff) => {
  const A = matFromInts(Array.from({ length: 2 }, () => Array.from({ length: 2 }, () => randInt(rng, -3, 3))));
  let B;
  do { B = matFromInts(Array.from({ length: 2 }, () => Array.from({ length: 2 }, () => randInt(rng, -2, 2)))); } while (determinant(B).isZero());
  const Binv = inverse(B);
  const Aprime = matMul(matMul(Binv, A), B);
  const statement = [monoLines(labeledMatrix("A", A)), monoLines(labeledMatrix("B", B)), textLine("A is the standard matrix of T. B's columns form a new basis. Find the matrix A' representing T in the B-basis: A' = B^-1 A B.")];
  const answer = [monoLines(labeledMatrix("B^-1", Binv)), monoLines(labeledMatrix("A' = B^-1 A B", Aprime))];
  return Q("changeofbasis", "cob-transform", "Transformation in another basis", statement, answer);
};

// ---------- Unit 7: Positive Definite Matrices ----------

GENERATORS["pd-eigtest"] = (rng, diff) => {
  const center = randInt(rng, 3, 6);
  const k = diff === 3 ? randInt(rng, 1, 2) : 1;
  const { A, lo, hi } = symmetricFromEigenGap(rng, center, k);
  const forcePD = diff !== 3 || rng() < 0.6;
  const useA = forcePD ? A : matScale(A, -1);
  const useLo = forcePD ? lo : -hi, useHi = forcePD ? hi : -lo;
  const statement = [monoLines(labeledMatrix("A", useA)), textLine("Use the eigenvalue test to determine whether A is positive definite.")];
  const answer = [textLine(`Eigenvalues: ${useLo}, ${useHi}`), textLine((useLo > 0 && useHi > 0) ? "Both eigenvalues are positive, so A IS positive definite." : "Not all eigenvalues are positive, so A is NOT positive definite.")];
  return Q("posdef", "pd-eigtest", "The eigenvalue test", statement, answer);
};

function pivotsOfSymmetric2(A) {
  const p1 = A[0][0];
  const p2 = A[1][1].sub(A[1][0].mul(A[0][1]).div(p1));
  return [p1, p2];
}

GENERATORS["pd-elimtest"] = (rng, diff) => {
  const a = randInt(rng, 2, 6);
  const b = randInt(rng, -3, 3);
  const dMin = Math.ceil((b * b) / a) + 1;
  const forcePD = diff !== 3 || rng() < 0.6;
  const d = forcePD ? dMin + randInt(rng, 0, 3) : Math.max(1, Math.floor((b * b) / a) - randInt(rng, 0, 2));
  const A = matFromInts([[a, b], [b, d]]);
  const [p1, p2] = pivotsOfSymmetric2(A);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Use the elimination (pivot) test to determine whether A is positive definite: eliminate to find the pivots and check that they are all positive.")];
  const answer = [
    textLine(`Pivot 1 = a11 = ${p1.toString()}`),
    textLine(`Pivot 2 = a22 - (a21*a12)/a11 = ${A[1][1].toString()} - (${A[1][0].toString()}*${A[0][1].toString()})/${A[0][0].toString()} = ${p2.toString()}`),
    textLine((p1.cmp(0) > 0 && p2.cmp(0) > 0) ? "Both pivots are positive, so A IS positive definite." : "Not all pivots are positive, so A is NOT positive definite.")
  ];
  return Q("posdef", "pd-elimtest", "The elimination/pivot test", statement, answer);
};

GENERATORS["pd-ldl"] = (rng, diff) => {
  const a = randInt(rng, 2, 5);
  const b = randInt(rng, -3, 3);
  const d = Math.ceil((b * b) / a) + randInt(rng, 1, 3);
  const A = matFromInts([[a, b], [b, d]]);
  const [p1, p2] = pivotsOfSymmetric2(A);
  const l21 = A[1][0].div(p1);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Find the LDL^T factorization of the symmetric positive definite matrix A (L unit lower triangular, D diagonal of pivots).")];
  const L = [[F(1), F(0)], [l21, F(1)]];
  const D = [[p1, F(0)], [F(0), p2]];
  const answer = [monoLines(labeledMatrix("L", L)), monoLines(labeledMatrix("D", D)), textLine("(Check: L D L^T reconstructs A.)")];
  return Q("posdef", "pd-ldl", "LDL^T factorization", statement, answer);
};

GENERATORS["pd-ata"] = (rng, diff) => {
  const m = diff === 3 ? 3 : 2, n = 2;
  // Retry if A's first column comes up all-zero (rare), which would make
  // the first pivot -- and so the pivot-test division -- zero.
  let A, ATA;
  do {
    A = matFromInts(Array.from({ length: m }, () => Array.from({ length: n }, () => randInt(rng, -3, 3))));
    ATA = matMul(transpose(A), A);
  } while (ATA[0][0].isZero());
  const [p1, p2] = pivotsOfSymmetric2(ATA);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Compute A^T A and use the pivot test to determine whether A^T A is positive definite (vs. only positive semidefinite).")];
  const answer = [
    monoLines(labeledMatrix("A^T A", ATA)),
    textLine(`Pivots: ${p1.toString()}, ${p2.toString()}`),
    textLine((p1.cmp(0) > 0 && p2.cmp(0) > 0)
      ? "Both pivots are positive: A^T A is positive definite (this happens exactly when A's columns are linearly independent)."
      : "A pivot is zero or negative: A^T A is only positive semidefinite (A's columns are dependent).")
  ];
  return Q("posdef", "pd-ata", "A^T A and least squares", statement, answer);
};

// ---------- Unit 8: Singular Value Decomposition ----------
// (Symmetric matrices are used throughout so that eigenvalues double as
// singular values, keeping every computation exact.)

GENERATORS["svd-basics"] = (rng, diff) => {
  const center = 0;
  const k = diff === 3 ? 2 : 1;
  const { A, lo, hi } = symmetricFromEigenGap(rng, center, k);
  const s1 = Math.abs(hi), s2 = Math.abs(lo);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("A is symmetric, so its singular values equal the absolute values of its eigenvalues. Find the singular values of A and order them sigma_1 >= sigma_2 >= 0.")];
  const answer = [textLine(`Eigenvalues: ${lo}, ${hi}`), textLine(`Singular values: sigma_1 = ${Math.max(s1, s2)}, sigma_2 = ${Math.min(s1, s2)}`)];
  return Q("svd", "svd-basics", "The SVD and singular values", statement, answer);
};

GENERATORS["svd-compute"] = (rng, diff) => {
  const center = randInt(rng, 2, 4);
  const k = 1;
  const { A, lo, hi } = symmetricFromEigenGap(rng, center, k);
  const v1 = eigenvector2(A, F(lo)), v2 = eigenvector2(A, F(hi));
  const statement = [monoLines(labeledMatrix("A", A)), textLine("Find the full SVD A = U Sigma V^T, using the fact that A is symmetric (so U = V = the eigenvector matrix, up to sign, and Sigma = |eigenvalues|).")];
  const answer = [
    textLine(`Eigenpairs: lambda1 = ${lo}, v1 = ${tupleStr(v1)};  lambda2 = ${hi}, v2 = ${tupleStr(v2)}`),
    textLine(`Sigma = diag(${Math.max(Math.abs(lo), Math.abs(hi))}, ${Math.min(Math.abs(lo), Math.abs(hi))})`),
    textLine(`U = V = [v1 v2] (normalize each column, and flip the sign of a column where its eigenvalue was negative).`)
  ];
  return Q("svd", "svd-compute", "Computing the SVD", statement, answer);
};

GENERATORS["svd-pseudoinv"] = (rng, diff) => {
  const s1 = randInt(rng, 2, 5);
  const A = matFromInts([[s1, 0], [0, 0]]);
  const statement = [monoLines(labeledMatrix("A", A)), textLine("A is already in the form U Sigma V^T with U = V = I. Find the Moore-Penrose pseudoinverse A+ (invert each nonzero singular value; leave zero singular values as zero).")];
  const Aplus = matFromInts([[Math.round(1e6 / s1) / 1e6, 0], [0, 0]]);
  const answer = [textLine(`Sigma = diag(${s1}, 0)  ->  Sigma+ = diag(1/${s1}, 0)`), monoLines(labeledMatrix("A+", [[F(1, s1), F(0)], [F(0), F(0)]]))];
  return Q("svd", "svd-pseudoinv", "Pseudoinverse", statement, answer);
};

GENERATORS["svd-lowrank"] = (rng, diff) => {
  const [p, q, r] = pick(rng, PY_TRIPLES);
  const k = diff === 1 ? 1 : diff === 2 ? 1 : 2;
  const sigmas = [r * k, q * k, p * k].sort((a, b) => b - a);
  const statement = [
    textLine(`A matrix A has singular values sigma_1 = ${sigmas[0]}, sigma_2 = ${sigmas[1]}, sigma_3 = ${sigmas[2]}.`),
    textLine("By the Eckart-Young theorem, find the Frobenius-norm error ||A - A_1||_F of the best rank-1 approximation A_1.")
  ];
  const errSq = sigmas[1] * sigmas[1] + sigmas[2] * sigmas[2];
  const answer = [
    textLine(`||A - A_1||_F = sqrt(sigma_2^2 + sigma_3^2) = sqrt(${sigmas[1]}^2 + ${sigmas[2]}^2) = sqrt(${errSq})`),
    textLine(Number.isInteger(Math.sqrt(errSq)) ? `= ${Math.sqrt(errSq)}` : "(leave in simplified radical form)")
  ];
  return Q("svd", "svd-lowrank", "Low-rank approximation", statement, answer);
};

// ---------- Unit 9: Graphs, Networks & Markov Chains ----------

function smallGraphEdges(rng, nVerts) {
  const edges = [];
  for (let i = 0; i < nVerts; i++) for (let j = i + 1; j < nVerts; j++) if (rng() < 0.6) edges.push([i, j]);
  if (edges.length === 0) edges.push([0, 1]);
  return edges;
}

GENERATORS["gr-adjacency"] = (rng, diff) => {
  const n = diff === 1 ? 3 : diff === 2 ? 4 : 5;
  const edges = smallGraphEdges(rng, n);
  const A = identity(n).map(row => row.map(() => F(0)));
  for (const [i, j] of edges) { A[i][j] = F(1); A[j][i] = F(1); }
  const degrees = A.map(row => row.reduce((s, x) => s.add(x), F(0)));
  const statement = [
    textLine(`An undirected graph on vertices {1,...,${n}} has edges: ${edges.map(([i, j]) => `${i + 1}-${j + 1}`).join(", ")}.`),
    textLine("Write the adjacency matrix A and the degree matrix D. Then compute A^2 and use it to find the number of length-2 walks between vertex 1 and vertex " + n + ".")
  ];
  const A2 = matMul(A, A);
  const answer = [
    monoLines(labeledMatrix("A", A)),
    textLine("D = diag(" + degrees.map(d => d.toString()).join(", ") + ")"),
    monoLines(labeledMatrix("A^2", A2)),
    textLine(`Number of length-2 walks from vertex 1 to vertex ${n}: (A^2)[1,${n}] = ${A2[0][n - 1].toString()}`)
  ];
  return Q("graphs", "gr-adjacency", "Adjacency & degree matrices", statement, answer);
};

GENERATORS["gr-incidence"] = (rng, diff) => {
  const n = diff === 1 ? 3 : 4;
  const edgesAll = [];
  for (let i = 0; i < n - 1; i++) edgesAll.push([i, i + 1]);
  if (diff >= 2) edgesAll.push([0, n - 1]);
  if (diff === 3 && n > 2) edgesAll.push([0, Math.min(2, n - 1)]);
  const m = edgesAll.length;
  const B = Array.from({ length: m }, () => new Array(n).fill(F(0)));
  edgesAll.forEach(([i, j], e) => { B[e][i] = F(-1); B[e][j] = F(1); });
  const statement = [
    textLine(`A directed graph on vertices {1,...,${n}} has edges (tail -> head): ${edgesAll.map(([i, j]) => `${i + 1}->${j + 1}`).join(", ")}.`),
    textLine("Write the incidence matrix B (rows = edges, -1 at the tail, +1 at the head), then compute the graph Laplacian L = B^T B.")
  ];
  const L = matMul(transpose(B), B);
  const nullB = nullSpaceBasis(B);
  const answer = [
    monoLines(labeledMatrix("B", B)),
    monoLines(labeledMatrix("L = B^T B", L)),
    textLine("Null(B) basis: " + (nullB.length ? nullB.map(v => tupleStr(v)).join(", ") : "{0}") + " (the all-ones vector, since the graph is connected).")
  ];
  return Q("graphs", "gr-incidence", "Incidence matrix & Laplacian", statement, answer);
};

GENERATORS["gr-spectral"] = (rng, diff) => {
  const useComplete = diff !== 3;
  const n = useComplete ? 3 : 4;
  let L, label, eigPairs;
  if (useComplete) {
    L = matFromInts([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]);
    label = "the complete graph K3";
    eigPairs = [{ lam: 0, v: [1, 1, 1] }, { lam: 3, v: [1, -1, 0] }];
  } else {
    L = matFromInts([[3, -1, -1, -1], [-1, 1, 0, 0], [-1, 0, 1, 0], [-1, 0, 0, 1]]);
    label = "the star graph K_{1,3} (vertex 1 is the center)";
    eigPairs = [{ lam: 0, v: [1, 1, 1, 1] }, { lam: 4, v: [3, -1, -1, -1] }];
  }
  const pair = pick(rng, eigPairs);
  const v = vecFromInts(pair.v);
  const statement = [monoLines(labeledMatrix("L", L)), textLine(`L is the Laplacian of ${label}. Verify that v = ${tupleStr(v)} is an eigenvector of L with eigenvalue ${pair.lam} by computing Lv.`)];
  const Lv = matVec(L, v);
  const answer = [monoLines(labeledColVector("Lv", Lv)), textLine(`Lv = ${tupleStr(Lv)} = ${pair.lam} * ${tupleStr(v)}. ✓ (eigenvalue ${pair.lam})`)];
  return Q("graphs", "gr-spectral", "Laplacian eigenvalues", statement, answer);
};

GENERATORS["gr-electrical"] = (rng, diff) => {
  // Path network of 3 nodes: node 0 and node 2 grounded at fixed potentials, solve for node 1.
  const g1 = randInt(rng, 1, 4), g2 = randInt(rng, 1, 4);
  const v0 = randInt(rng, 0, 10), v2 = randInt(rng, 0, 10);
  // KCL at node 1: g1*(v1-v0) + g2*(v1-v2) = 0  ->  (g1+g2) v1 = g1 v0 + g2 v2
  const lhs = g1 + g2;
  const rhs = g1 * v0 + g2 * v2;
  const v1 = F(rhs, lhs);
  const statement = [
    textLine(`Three nodes are connected in a line: node 0 --(conductance g1=${g1})-- node 1 --(conductance g2=${g2})-- node 2.`),
    textLine(`Nodes 0 and 2 are held at fixed potentials v0 = ${v0} and v2 = ${v2}. Use Kirchhoff's Current Law at node 1 to solve for v1, then find the current through each resistor (i = g*(v_a - v_b)).`)
  ];
  const i1 = v1.sub(F(v0)).mul(F(g1));
  const i2 = F(v2).sub(v1).mul(F(g2));
  const answer = [
    textLine(`KCL: ${g1}(v1 - ${v0}) + ${g2}(v1 - ${v2}) = 0  ->  v1 = ${v1.toString()}`),
    textLine(`Current node0->node1: i1 = g1*(v1-v0) = ${i1.toString()}`),
    textLine(`Current node1->node2: i2 = g2*(v2-v1) = ${i2.toString()}`)
  ];
  return Q("graphs", "gr-electrical", "Electrical networks", statement, answer);
};

GENERATORS["gr-markov"] = (rng, diff) => {
  const a = randInt(rng, 1, 3), b = randInt(rng, 1, 3);
  // Column-stochastic 2-state transition matrix with entries a/(a+b) style fractions.
  const p = F(a, a + b), q = F(b, a + b);
  const P = [[F(1).sub(p), q], [p, F(1).sub(q)]];
  const x0 = diff === 1 ? [F(1), F(0)] : [F(a, a + b + 1), F(b + 1, a + b + 1)];
  const steps = diff === 3 ? 2 : 1;
  const statement = [
    monoLines(labeledMatrix("P", P)),
    textLine(`P is the transition matrix of a 2-state Markov chain (columns sum to 1). Starting distribution x0 = ${tupleStr(x0)}.`),
    textLine(`Compute x${steps} = P^${steps} x0, and find the steady-state distribution (solve Px = x with entries summing to 1).`)
  ];
  let x = x0;
  for (let s = 0; s < steps; s++) x = matVec(P, x);
  // Steady state for 2x2 stochastic matrix [[1-p, q],[p, 1-q]]: pi = (q, p)/(p+q)
  const denom = p.add(q);
  const pi = [q.div(denom), p.div(denom)];
  const answer = [
    textLine(`x${steps} = ${tupleStr(x)}`),
    textLine(`Steady state: solve (P - I)x = 0 with x1+x2=1  ->  pi = ${tupleStr(pi)}`)
  ];
  return Q("graphs", "gr-markov", "Markov chains", statement, answer);
};
