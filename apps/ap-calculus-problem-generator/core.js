/*
 * core.js — random helpers, exact fraction arithmetic, and polynomial
 * utilities used by the AP Calculus problem generators.
 */

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
function randNonZero(min, max) {
  let v;
  do { v = randInt(min, max); } while (v === 0);
  return v;
}
function choice(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}
function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function gcd(a, b) {
  a = Math.abs(a); b = Math.abs(b);
  while (b) { [a, b] = [b, a % b]; }
  return a || 1;
}

class Frac {
  constructor(n, d = 1) {
    if (d === 0) throw new Error('Frac: division by zero');
    if (!Number.isInteger(n) || !Number.isInteger(d)) {
      // Allow float rounding safety net (shouldn't normally happen)
      n = Math.round(n); d = Math.round(d);
    }
    if (d < 0) { n = -n; d = -d; }
    const g = gcd(n, d);
    this.n = g ? n / g : 0;
    this.d = g ? d / g : 1;
  }
  add(o) { o = Frac.of(o); return new Frac(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { o = Frac.of(o); return new Frac(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { o = Frac.of(o); return new Frac(this.n * o.n, this.d * o.d); }
  div(o) { o = Frac.of(o); return new Frac(this.n * o.d, this.d * o.n); }
  neg() { return new Frac(-this.n, this.d); }
  abs() { return this.n < 0 ? this.neg() : this; }
  pow(k) {
    if (k === 0) return new Frac(1, 1);
    if (k > 0) return new Frac(Math.round(this.n ** k), Math.round(this.d ** k));
    return new Frac(Math.round(this.d ** (-k)), Math.round(this.n ** (-k)));
  }
  isZero() { return this.n === 0; }
  isNeg() { return this.n < 0; }
  equals(o) { o = Frac.of(o); return this.n * o.d === o.n * this.d; }
  gt(o) { o = Frac.of(o); return this.n * o.d > o.n * this.d; }
  toFloat() { return this.n / this.d; }
  toString() { return this.d === 1 ? `${this.n}` : `${this.n}/${this.d}`; }
  static of(v) { return v instanceof Frac ? v : new Frac(v, 1); }
}
function F(n, d = 1) { return new Frac(n, d); }

// ---- Polynomials: ascending-order arrays of Frac, index = power of x ----

function polyTrim(p) {
  const out = p.slice();
  while (out.length > 1 && out[out.length - 1].isZero()) out.pop();
  return out;
}
function polyAdd(a, b) {
  const len = Math.max(a.length, b.length);
  const out = [];
  for (let i = 0; i < len; i++) out.push((a[i] || F(0)).add(b[i] || F(0)));
  return polyTrim(out);
}
function polySub(a, b) { return polyAdd(a, b.map((c) => c.neg())); }
function polyScale(a, k) { k = Frac.of(k); return polyTrim(a.map((c) => c.mul(k))); }
function polyMul(a, b) {
  const out = new Array(a.length + b.length - 1).fill(null).map(() => F(0));
  for (let i = 0; i < a.length; i++) {
    for (let j = 0; j < b.length; j++) out[i + j] = out[i + j].add(a[i].mul(b[j]));
  }
  return polyTrim(out);
}
function polyDeriv(p) {
  if (p.length <= 1) return [F(0)];
  const out = [];
  for (let i = 1; i < p.length; i++) out.push(p[i].mul(F(i)));
  return polyTrim(out);
}
function polyAntideriv(p, C = F(0)) {
  const out = [C];
  for (let i = 0; i < p.length; i++) out.push(p[i].div(F(i + 1)));
  return polyTrim(out);
}
function polyEval(p, x) {
  x = Frac.of(x);
  let sum = F(0), xp = F(1);
  for (let i = 0; i < p.length; i++) { sum = sum.add(p[i].mul(xp)); xp = xp.mul(x); }
  return sum;
}
function polyEvalFloat(p, xFloat) {
  let sum = 0, xp = 1;
  for (let i = 0; i < p.length; i++) { sum += p[i].toFloat() * xp; xp *= xFloat; }
  return sum;
}
function polyDegree(p) {
  for (let i = p.length - 1; i >= 0; i--) if (!p[i].isZero()) return i;
  return 0;
}
function polyLeadCoeff(p) { return p[polyDegree(p)]; }

function linear(a, b) { return [F(b), F(a)]; } // a*x + b

function randPoly(minDeg, maxDeg, coeffMin, coeffMax) {
  const deg = randInt(minDeg, maxDeg);
  const p = [];
  for (let i = 0; i <= deg; i++) p.push(F(randInt(coeffMin, coeffMax)));
  if (p[deg].isZero()) p[deg] = F(choice([1, -1]) * randInt(1, Math.max(1, coeffMax)));
  return polyTrim(p);
}

// ---- HTML formatting ----

function termParts(c, i, varName) {
  if (c.isZero()) return null;
  const neg = c.isNeg();
  const abs = neg ? c.neg() : c;
  const coefficientIsOne = abs.equals(F(1));
  const coefStr = (coefficientIsOne && i !== 0) ? '' : abs.toString();
  const varStr = i === 0 ? '' : (i === 1 ? varName : `${varName}<sup>${i}</sup>`);
  return { neg, text: coefStr + varStr };
}
function polyToHTML(p, varName = 'x') {
  const terms = [];
  for (let i = p.length - 1; i >= 0; i--) {
    const t = termParts(p[i], i, varName);
    if (t) terms.push(t);
  }
  if (terms.length === 0) return '0';
  let html = (terms[0].neg ? '−' : '') + terms[0].text;
  for (let i = 1; i < terms.length; i++) {
    html += terms[i].neg ? ` − ${terms[i].text}` : ` + ${terms[i].text}`;
  }
  return html;
}
function fracHTML(f) {
  if (f.d === 1) return `${f.n}`;
  return `<span class="frac"><span class="num">${f.n}</span><span class="den">${f.d}</span></span>`;
}
function signed(f) { return f.isNeg() ? `−${f.neg()}` : `${f}`; }
function fracPiHTML(f) {
  if (f.isZero()) return '0';
  const abs = f.abs();
  const coef = abs.equals(F(1)) ? '' : (abs.d === 1 ? abs.toString() : `(${abs.toString()})`);
  return (f.isNeg() ? '−' : '') + coef + 'π';
}

// ---- Distractor helpers for numeric (Frac) answers ----

function makeNumericDistractors(correct) {
  const pool = new Set([correct.toString()]);
  const out = [];
  const candidates = [
    correct.neg(),
    correct.add(F(1)),
    correct.sub(F(1)),
    correct.mul(F(2)),
    correct.mul(F(-1)).add(F(1)),
    correct.add(F(2)),
    correct.sub(F(2)),
  ];
  for (const c of candidates) {
    const s = c.toString();
    if (!pool.has(s)) { pool.add(s); out.push(c.toString()); }
    if (out.length === 3) break;
  }
  let guard = 0;
  while (out.length < 3 && guard < 50) {
    guard++;
    const jitter = F(correct.n * correct.d + randNonZero(-4, 4) * Math.max(1, correct.d), correct.d * correct.d);
    const s = jitter.toString();
    if (!pool.has(s)) { pool.add(s); out.push(s); }
  }
  return out;
}

function makeDecimalDistractors(correctValue, decimals = 3) {
  const fmt = (v) => v.toFixed(decimals);
  const pool = new Set([fmt(correctValue)]);
  const out = [];
  const candidates = [
    -correctValue,
    correctValue + 1,
    correctValue - 1,
    correctValue * 2,
    correctValue / 2,
  ];
  for (const c of candidates) {
    const s = fmt(c);
    if (!pool.has(s)) { pool.add(s); out.push(s); }
    if (out.length === 3) break;
  }
  let guard = 0;
  while (out.length < 3 && guard < 50) {
    guard++;
    const jitter = correctValue + (randNonZero(-5, 5)) * Math.max(0.1, Math.abs(correctValue) * 0.1 || 1);
    const s = fmt(jitter);
    if (!pool.has(s)) { pool.add(s); out.push(s); }
  }
  return out;
}

const PYTHAGOREAN_TRIPLES = [
  [3, 4, 5], [6, 8, 10], [5, 12, 13], [8, 15, 17], [9, 12, 15],
  [7, 24, 25], [20, 21, 29], [9, 40, 41], [12, 16, 20], [10, 24, 26],
];

if (typeof module !== 'undefined') {
  module.exports = {
    randInt, randNonZero, choice, shuffle, gcd, Frac, F,
    polyTrim, polyAdd, polySub, polyScale, polyMul, polyDeriv, polyAntideriv,
    polyEval, polyEvalFloat, polyDegree, polyLeadCoeff, linear, randPoly,
    termParts, polyToHTML, fracHTML, signed, fracPiHTML,
    makeNumericDistractors, makeDecimalDistractors, PYTHAGOREAN_TRIPLES,
  };
}
