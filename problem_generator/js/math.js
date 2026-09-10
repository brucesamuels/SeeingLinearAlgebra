/* Small exact-arithmetic linear algebra toolkit used by the generators.
   Everything is fraction-based so answers come out as clean numbers
   (or simple fractions) instead of floating-point noise. */

function gcd(a, b) {
  a = Math.abs(a); b = Math.abs(b);
  while (b) { [a, b] = [b, a % b]; }
  return a || 1;
}

class Frac {
  constructor(n, d = 1) {
    if (d === 0) throw new Error("Division by zero in Frac");
    if (d < 0) { n = -n; d = -d; }
    const g = gcd(n, d);
    this.n = g ? n / g : 0;
    this.d = g ? d / g : 1;
  }
  static of(x) { return x instanceof Frac ? x : new Frac(x, 1); }
  add(o) { o = Frac.of(o); return new Frac(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { o = Frac.of(o); return new Frac(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { o = Frac.of(o); return new Frac(this.n * o.n, this.d * o.d); }
  div(o) { o = Frac.of(o); return new Frac(this.n * o.d, this.d * o.n); }
  neg() { return new Frac(-this.n, this.d); }
  abs() { return new Frac(Math.abs(this.n), this.d); }
  isZero() { return this.n === 0; }
  eq(o) { o = Frac.of(o); return this.n === o.n && this.d === o.d; }
  toFloat() { return this.n / this.d; }
  cmp(o) { o = Frac.of(o); return this.n * o.d - o.n * this.d; }
  toString() {
    if (this.d === 1) return String(this.n);
    return `${this.n}/${this.d}`;
  }
}

function F(n, d = 1) { return new Frac(n, d); }

// ---- Matrix helpers (matrices are arrays of arrays of Frac) ----

function matFromInts(rows) {
  return rows.map(r => r.map(x => F(x)));
}

function vecFromInts(v) { return v.map(x => F(x)); }

function matDims(A) { return [A.length, A[0] ? A[0].length : 0]; }

function matMul(A, B) {
  const [ar, ac] = matDims(A);
  const [br, bc] = matDims(B);
  if (ac !== br) throw new Error("Dimension mismatch in matMul");
  const out = [];
  for (let i = 0; i < ar; i++) {
    const row = [];
    for (let j = 0; j < bc; j++) {
      let s = F(0);
      for (let k = 0; k < ac; k++) s = s.add(A[i][k].mul(B[k][j]));
      row.push(s);
    }
    out.push(row);
  }
  return out;
}

function matVec(A, v) {
  return A.map(row => row.reduce((s, a, j) => s.add(a.mul(v[j])), F(0)));
}

function matAdd(A, B, sign = 1) {
  return A.map((row, i) => row.map((a, j) => sign === 1 ? a.add(B[i][j]) : a.sub(B[i][j])));
}

function matScale(A, k) {
  k = Frac.of(k);
  return A.map(row => row.map(a => a.mul(k)));
}

function transpose(A) {
  const [r, c] = matDims(A);
  const out = [];
  for (let j = 0; j < c; j++) {
    const row = [];
    for (let i = 0; i < r; i++) row.push(A[i][j]);
    out.push(row);
  }
  return out;
}

function trace(A) {
  let s = F(0);
  for (let i = 0; i < A.length; i++) s = s.add(A[i][i]);
  return s;
}

function identity(n) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const row = [];
    for (let j = 0; j < n; j++) row.push(F(i === j ? 1 : 0));
    out.push(row);
  }
  return out;
}

function cloneMat(A) { return A.map(row => row.map(a => new Frac(a.n, a.d))); }

function det2(A) {
  return A[0][0].mul(A[1][1]).sub(A[0][1].mul(A[1][0]));
}

function det3(A) {
  const a = A;
  return a[0][0].mul(a[1][1].mul(a[2][2]).sub(a[1][2].mul(a[2][1])))
    .sub(a[0][1].mul(a[1][0].mul(a[2][2]).sub(a[1][2].mul(a[2][0]))))
    .add(a[0][2].mul(a[1][0].mul(a[2][1]).sub(a[1][1].mul(a[2][0]))));
}

function determinant(A) {
  const n = A.length;
  if (n === 1) return A[0][0];
  if (n === 2) return det2(A);
  if (n === 3) return det3(A);
  // General cofactor expansion along row 0 (fine for the small matrices used here).
  let s = F(0);
  for (let j = 0; j < n; j++) {
    const minor = A.slice(1).map(row => row.filter((_, k) => k !== j));
    const cof = determinant(minor).mul(F((j % 2 === 0) ? 1 : -1));
    s = s.add(A[0][j].mul(cof));
  }
  return s;
}

function cofactorMatrix(A) {
  const n = A.length;
  const out = [];
  for (let i = 0; i < n; i++) {
    const row = [];
    for (let j = 0; j < n; j++) {
      const minor = A.filter((_, r) => r !== i).map(r => r.filter((_, c) => c !== j));
      const sign = ((i + j) % 2 === 0) ? 1 : -1;
      row.push(determinant(minor).mul(F(sign)));
    }
    out.push(row);
  }
  return out;
}

function adjugate(A) { return transpose(cofactorMatrix(A)); }

function inverse(A) {
  const d = determinant(A);
  if (d.isZero()) return null;
  const adj = adjugate(A);
  return matScale(adj, F(1).div(d));
}

// Gauss-Jordan reduction to RREF with step tracking (for teacher keys).
function rref(Ain, steps) {
  const A = cloneMat(Ain);
  const rows = A.length, cols = A[0].length;
  let pivotRow = 0;
  const pivotCols = [];
  for (let col = 0; col < cols && pivotRow < rows; col++) {
    let sel = -1;
    for (let r = pivotRow; r < rows; r++) if (!A[r][col].isZero()) { sel = r; break; }
    if (sel === -1) continue;
    if (sel !== pivotRow) {
      [A[sel], A[pivotRow]] = [A[pivotRow], A[sel]];
      if (steps) steps.push(`Swap R${sel + 1} and R${pivotRow + 1}`);
    }
    const pv = A[pivotRow][col];
    if (!pv.eq(F(1))) {
      A[pivotRow] = A[pivotRow].map(x => x.div(pv));
      if (steps) steps.push(`R${pivotRow + 1} -> R${pivotRow + 1} / (${pv.toString()})`);
    }
    for (let r = 0; r < rows; r++) {
      if (r === pivotRow) continue;
      const factor = A[r][col];
      if (!factor.isZero()) {
        A[r] = A[r].map((x, j) => x.sub(factor.mul(A[pivotRow][j])));
        if (steps) steps.push(`R${r + 1} -> R${r + 1} - (${factor.toString()})*R${pivotRow + 1}`);
      }
    }
    pivotCols.push(col);
    pivotRow++;
  }
  return { R: A, pivotCols, rank: pivotCols.length };
}

function solveLinearSystem(A, b) {
  const n = A.length;
  const aug = A.map((row, i) => [...row, b[i]]);
  const { R, pivotCols, rank } = rref(aug);
  const cols = A[0].length;
  if (rank < cols) {
    // Check consistency (a fully-zero row on the LHS with nonzero RHS => no solution).
    for (let r = rank; r < R.length; r++) {
      const allZero = R[r].slice(0, cols).every(x => x.isZero());
      if (allZero && !R[r][cols].isZero()) return { type: "none" };
    }
    return { type: "infinite", R, pivotCols };
  }
  const x = new Array(cols).fill(F(0));
  for (let i = 0; i < pivotCols.length; i++) x[pivotCols[i]] = R[i][cols];
  return { type: "unique", x };
}

// Null space basis of A (solves Ax = 0) via free-variable back substitution on the RREF.
function nullSpaceBasis(A) {
  const { R, pivotCols, rank } = rref(A);
  const cols = A[0].length;
  const freeCols = [];
  for (let c = 0; c < cols; c++) if (!pivotCols.includes(c)) freeCols.push(c);
  const basis = [];
  for (const fc of freeCols) {
    const v = new Array(cols).fill(F(0));
    v[fc] = F(1);
    for (let i = 0; i < pivotCols.length; i++) {
      v[pivotCols[i]] = R[i][fc].neg();
    }
    basis.push(v);
  }
  return basis;
}

// Column space basis: the original columns at the pivot positions of RREF(A).
function colSpaceBasis(A) {
  const { pivotCols } = rref(A);
  return pivotCols.map(c => A.map(row => row[c]));
}

// Row space basis: the nonzero rows of RREF(A).
function rowSpaceBasis(A) {
  const { R, rank } = rref(A);
  return R.slice(0, rank);
}

function fmtVec(v) { return `(${v.map(x => x.toString()).join(", ")})`; }

function fmtMatText(A) {
  return A.map(row => "[ " + row.map(x => x.toString()).join(", ") + " ]").join("\n");
}

// Small helper RNG so problem sets can (optionally) be reproduced from a seed.
function makeRng(seed) {
  let s = seed >>> 0 || 0xC0FFEE;
  return function () {
    s ^= s << 13; s >>>= 0;
    s ^= s >> 17;
    s ^= s << 5; s >>>= 0;
    return (s >>> 0) / 4294967296;
  };
}

function randInt(rng, lo, hi) { return lo + Math.floor(rng() * (hi - lo + 1)); }
function randNonZeroInt(rng, lo, hi) {
  let v = 0;
  do { v = randInt(rng, lo, hi); } while (v === 0);
  return v;
}
function pick(rng, arr) { return arr[Math.floor(rng() * arr.length)]; }
function shuffle(rng, arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
