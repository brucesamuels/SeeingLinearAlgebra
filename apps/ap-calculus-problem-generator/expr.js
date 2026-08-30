/*
 * expr.js — a small symbolic expression engine used to compose AP Calculus
 * problems from primitives (polynomials, sin/cos, exp, ln, integer powers)
 * instead of picking a single fixed function shape per topic.
 *
 * A node is a plain object tagged by `op`:
 *   {op:'const', value:Frac}
 *   {op:'x'}
 *   {op:'add', args:[node,...]}
 *   {op:'mul', args:[node,...]}
 *   {op:'pow', base:node, n:int}        base^n, n a non-negative integer literal
 *   {op:'div', num:node, den:node}
 *   {op:'sin'|'cos'|'exp', arg:node}
 *   {op:'ln', arg:node, abs:bool}       abs:true renders ln|arg| (for antiderivatives)
 *
 * diff() applies the standard rules mechanically, so it is exact by
 * construction for any tree built from these primitives — no general
 * symbolic integration is attempted anywhere; see `randomAntiderivative`
 * for how integration problems are generated instead (build the answer,
 * then differentiate it).
 */

function cst(v) { return { op: 'const', value: Frac.of(v) }; }
const X_NODE = { op: 'x' };
function addN(...args) {
  args = args.filter((a) => a); // drop any falsy
  if (args.length === 0) return cst(0);
  if (args.length === 1) return args[0];
  return { op: 'add', args };
}
function mulN(...args) {
  args = args.filter((a) => a);
  if (args.length === 0) return cst(1);
  if (args.length === 1) return args[0];
  return { op: 'mul', args };
}
function powN(base, n) {
  if (n === 0) return cst(1);
  if (n === 1) return base;
  return { op: 'pow', base, n };
}
function divN(num, den) { return { op: 'div', num, den }; }
function sinE(arg) { return { op: 'sin', arg }; }
function cosE(arg) { return { op: 'cos', arg }; }
function expE(arg) { return { op: 'exp', arg }; }
function lnE(arg, abs = false) { return { op: 'ln', arg, abs }; }

/* ---- Differentiation (exact, mechanical, closed-form by construction) ---- */

function diff(node) {
  switch (node.op) {
    case 'const': return cst(0);
    case 'x': return cst(1);
    case 'add': return addN(...node.args.map(diff));
    case 'mul':
      return addN(...node.args.map((_, i) => mulN(diff(node.args[i]), ...node.args.filter((_, j) => j !== i))));
    case 'pow': {
      if (node.n === 0) return cst(0);
      return mulN(cst(node.n), powN(node.base, node.n - 1), diff(node.base));
    }
    case 'div': {
      const { num, den } = node;
      return divN(addN(mulN(diff(num), den), mulN(cst(-1), num, diff(den))), powN(den, 2));
    }
    case 'sin': return mulN(cosE(node.arg), diff(node.arg));
    case 'cos': return mulN(cst(-1), sinE(node.arg), diff(node.arg));
    case 'exp': return mulN(expE(node.arg), diff(node.arg));
    case 'ln': return divN(diff(node.arg), node.arg);
    default: throw new Error(`diff: unknown op ${node.op}`);
  }
}

/*
 * diffBuggy — mirrors diff() but injects one systematic student error, used
 * to generate multiple-choice distractors that are plausible rather than
 * arbitrary. `bug.noChain` skips multiplying by the inner derivative at
 * every chain-rule step; `bug.cosSign` drops the negative sign from
 * d/dx[cos]. Quotient rule (div) is left correct — the bug modes only
 * target chain-rule-style mistakes, which is what the compositional
 * generators actually exercise.
 */
function diffBuggy(node, bug) {
  switch (node.op) {
    case 'const': return cst(0);
    case 'x': return cst(1);
    case 'add': return addN(...node.args.map((a) => diffBuggy(a, bug)));
    case 'mul':
      return addN(...node.args.map((_, i) => mulN(diffBuggy(node.args[i], bug), ...node.args.filter((_, j) => j !== i))));
    case 'pow': {
      if (node.n === 0) return cst(0);
      const inner = bug.noChain ? cst(1) : diffBuggy(node.base, bug);
      return mulN(cst(node.n), powN(node.base, node.n - 1), inner);
    }
    case 'div': return diff(node);
    case 'sin': {
      const inner = bug.noChain ? cst(1) : diffBuggy(node.arg, bug);
      return mulN(cosE(node.arg), inner);
    }
    case 'cos': {
      const inner = bug.noChain ? cst(1) : diffBuggy(node.arg, bug);
      return bug.cosSign ? mulN(sinE(node.arg), inner) : mulN(cst(-1), sinE(node.arg), inner);
    }
    case 'exp': {
      const inner = bug.noChain ? cst(1) : diffBuggy(node.arg, bug);
      return mulN(expE(node.arg), inner);
    }
    case 'ln': {
      const inner = bug.noChain ? cst(1) : diffBuggy(node.arg, bug);
      return divN(inner, node.arg);
    }
    default: throw new Error(`diffBuggy: unknown op ${node.op}`);
  }
}

/* ---- Simplification: constant folding + structural cleanup only.
 * Deliberately does NOT collect like terms across arbitrary subtrees (no
 * general polynomial normal form) — the random builders avoid generating
 * like terms in the first place, which keeps this simple and correct. ---- */

function simplify(node) {
  switch (node.op) {
    case 'const': case 'x': return node;
    case 'add': {
      const flat = [];
      for (const a of node.args.map(simplify)) {
        if (a.op === 'add') flat.push(...a.args); else flat.push(a);
      }
      let constSum = F(0);
      const rest = [];
      for (const a of flat) { if (a.op === 'const') constSum = constSum.add(a.value); else rest.push(a); }
      const parts = constSum.isZero() ? rest : [cst(constSum), ...rest];
      return addN(...parts);
    }
    case 'mul': {
      const flat = [];
      for (const a of node.args.map(simplify)) {
        if (a.op === 'mul') flat.push(...a.args); else flat.push(a);
      }
      let constProd = F(1);
      const rest = [];
      for (const a of flat) { if (a.op === 'const') constProd = constProd.mul(a.value); else rest.push(a); }
      if (constProd.isZero()) return cst(0);
      const parts = constProd.equals(F(1)) ? rest : [cst(constProd), ...rest];
      return mulN(...parts);
    }
    case 'pow': {
      const base = simplify(node.base);
      if (node.n === 0) return cst(1);
      if (node.n === 1) return base;
      if (base.op === 'const') return cst(base.value.pow(node.n));
      return powN(base, node.n);
    }
    case 'div': {
      const num = simplify(node.num), den = simplify(node.den);
      if (num.op === 'const' && num.value.isZero()) return cst(0);
      if (num.op === 'const' && den.op === 'const' && !den.value.isZero()) return cst(num.value.div(den.value));
      if (den.op === 'const') return simplify(mulN(cst(F(1).div(den.value)), num));
      return divN(num, den);
    }
    case 'sin': { const arg = simplify(node.arg); return arg.op === 'const' && arg.value.isZero() ? cst(0) : sinE(arg); }
    case 'cos': { const arg = simplify(node.arg); return arg.op === 'const' && arg.value.isZero() ? cst(1) : cosE(arg); }
    case 'exp': { const arg = simplify(node.arg); return arg.op === 'const' && arg.value.isZero() ? cst(1) : expE(arg); }
    case 'ln': { const arg = simplify(node.arg); return lnE(arg, node.abs); }
    default: throw new Error(`simplify: unknown op ${node.op}`);
  }
}

/* ---- Numeric / exact evaluation ---- */

function evalNum(node, xVal) {
  switch (node.op) {
    case 'const': return node.value.toFloat();
    case 'x': return xVal;
    case 'add': return node.args.reduce((s, a) => s + evalNum(a, xVal), 0);
    case 'mul': return node.args.reduce((p, a) => p * evalNum(a, xVal), 1);
    case 'pow': return Math.pow(evalNum(node.base, xVal), node.n);
    case 'div': return evalNum(node.num, xVal) / evalNum(node.den, xVal);
    case 'sin': return Math.sin(evalNum(node.arg, xVal));
    case 'cos': return Math.cos(evalNum(node.arg, xVal));
    case 'exp': return Math.exp(evalNum(node.arg, xVal));
    case 'ln': return Math.log(Math.abs(evalNum(node.arg, xVal)));
    default: throw new Error(`evalNum: unknown op ${node.op}`);
  }
}

/** Exact (Frac) evaluation. Returns null wherever the subtree is
 * transcendental (sin/cos/exp/ln) or divides by a non-constant, since
 * those are not exact in general. */
function evalExact(node, xFrac) {
  switch (node.op) {
    case 'const': return node.value;
    case 'x': return xFrac;
    case 'add': {
      let s = F(0);
      for (const a of node.args) { const v = evalExact(a, xFrac); if (v === null) return null; s = s.add(v); }
      return s;
    }
    case 'mul': {
      let p = F(1);
      for (const a of node.args) { const v = evalExact(a, xFrac); if (v === null) return null; p = p.mul(v); }
      return p;
    }
    case 'pow': { const b = evalExact(node.base, xFrac); return b === null ? null : b.pow(node.n); }
    case 'div': {
      const n = evalExact(node.num, xFrac), d = evalExact(node.den, xFrac);
      if (n === null || d === null || d.isZero()) return null;
      return n.div(d);
    }
    default: return null; // sin/cos/exp/ln
  }
}

/** Evaluate exactly when possible, else fall back to a rounded decimal
 * (matches how the AP exam treats calculator-active numeric answers). */
function evalSmart(node, x0, decimals = 3) {
  const exact = evalExact(node, F(x0));
  if (exact !== null) return { exact: true, str: exact.toString(), value: exact.toFloat() };
  const value = evalNum(node, x0);
  return { exact: false, str: value.toFixed(decimals), value };
}

/* ---- HTML rendering ---- */

function isNegConst(node) { return node.op === 'const' && node.value.isNeg(); }

/** Split a node into {sign, mag} where mag has a non-negative leading
 * coefficient — used so add() can render "a − b" instead of "a + −b". */
function signSplit(node) {
  if (node.op === 'const') return node.value.isNeg() ? { sign: -1, mag: cst(node.value.neg()) } : { sign: 1, mag: node };
  if (node.op === 'mul' && node.args[0] && node.args[0].op === 'const' && node.args[0].value.isNeg()) {
    const negated = cst(node.args[0].value.neg());
    const restArgs = node.args.slice(1);
    const magArgs = negated.value.equals(F(1)) ? restArgs : [negated, ...restArgs];
    return { sign: -1, mag: mulN(...magArgs) };
  }
  return { sign: 1, mag: node };
}

function wrapIfNeeded(node, context) {
  const html = renderNode(node);
  if (node.op === 'add') return `(${html})`;
  if (context === 'powBase' && (node.op === 'mul' || node.op === 'div')) return `(${html})`;
  return html;
}

function renderNode(node) {
  switch (node.op) {
    case 'const': {
      const v = node.value;
      return v.isNeg() ? `−${fracHTML(v.neg())}` : fracHTML(v);
    }
    case 'x': return 'x';
    case 'add': {
      const parts = node.args.map((a) => signSplit(a));
      let html = (parts[0].sign < 0 ? '−' : '') + renderNode(parts[0].mag);
      for (let i = 1; i < parts.length; i++) {
        html += parts[i].sign < 0 ? ` − ${renderNode(parts[i].mag)}` : ` + ${renderNode(parts[i].mag)}`;
      }
      return html;
    }
    case 'mul': {
      // NOTE: unlike the 'add' case, this does NOT rely on a caller
      // having sign-split the node first — a mul with a negative leading
      // coefficient must render its own '−' whether it appears standalone
      // or nested inside pow/div/sin/etc, since only 'add' terms get
      // pre-split via signSplit() before reaching here.
      let coefHTML = '';
      let neg = false;
      let rest = node.args;
      if (node.args[0] && node.args[0].op === 'const') {
        const c = node.args[0].value;
        rest = node.args.slice(1);
        neg = c.isNeg();
        const absC = neg ? c.neg() : c;
        if (!absC.equals(F(1))) coefHTML = fracHTML(absC);
      }
      const restHTML = rest.map((r) => wrapIfNeeded(r, 'mulFactor')).join('·');
      const body = restHTML ? `${coefHTML}${restHTML}` : (coefHTML || '1');
      return neg ? `−${body}` : body;
    }
    case 'pow': return `${wrapIfNeeded(node.base, 'powBase')}<sup>${node.n}</sup>`;
    case 'div': return `(${renderNode(node.num)}) / (${renderNode(node.den)})`;
    case 'sin': return `sin(${renderNode(node.arg)})`;
    case 'cos': return `cos(${renderNode(node.arg)})`;
    case 'exp': return `e<sup>${renderNode(node.arg)}</sup>`;
    case 'ln': return node.abs ? `ln|${renderNode(node.arg)}|` : `ln(${renderNode(node.arg)})`;
    default: throw new Error(`renderNode: unknown op ${node.op}`);
  }
}

function toHTML(node) { return renderNode(simplify(node)); }

/* ---- Bridge from core.js's Frac-array polynomials ---- */

function polyToNode(poly) {
  const terms = [];
  for (let i = 0; i < poly.length; i++) {
    if (poly[i].isZero()) continue;
    terms.push(mulN(cst(poly[i]), powN(X_NODE, i)));
  }
  return terms.length ? addN(...terms) : cst(0);
}

/* ---- Generic mutation helpers (for distractors) ---- */

function scaleLeadingCoef(node, factor) {
  if (node.op === 'mul' && node.args[0] && node.args[0].op === 'const') {
    return mulN(cst(node.args[0].value.mul(factor)), ...node.args.slice(1));
  }
  return mulN(cst(factor), node);
}
function flipRandomTermSign(node) {
  if (node.op === 'add' && node.args.length > 0) {
    const idx = randInt(0, node.args.length - 1);
    return addN(...node.args.map((a, i) => (i === idx ? mulN(cst(-1), a) : a)));
  }
  return mulN(cst(-1), node);
}

/* ---- Random expression builders ---- */

function randomLinear(coeffRange, opts = {}) {
  const a = opts.forcePositive ? randInt(1, coeffRange) : randNonZero(-coeffRange, coeffRange);
  const b = randInt(-coeffRange, coeffRange);
  return addN(mulN(cst(a), X_NODE), cst(b));
}

/** A linear inner function guaranteed positive for all x >= 0 (positive
 * slope, positive intercept) — used wherever the expression will actually
 * be numerically evaluated at nonnegative bounds through an ln(), so
 * Math.log() never hits zero/negative input. */
function randomPositiveLinear(coeffRange) {
  const a = randInt(1, coeffRange);
  const b = randInt(1, coeffRange);
  return addN(mulN(cst(a), X_NODE), cst(b));
}

const KIND_SETS = {
  1: ['poly', 'sin', 'cos', 'exp'],
  2: ['poly', 'sin', 'cos', 'exp', 'ln', 'pow'],
  3: ['poly', 'sin', 'cos', 'exp', 'ln', 'pow', 'compose'],
};

function randomAtomicTerm(difficulty, opts = {}) {
  const kinds = opts.kinds || KIND_SETS[difficulty] || KIND_SETS[3];
  const kind = choice(kinds);
  const coeff = randNonZero(-6, 6);
  const coeffRange = opts.coeffRange || (difficulty === 1 ? 4 : difficulty === 2 ? 6 : 8);
  switch (kind) {
    case 'poly': {
      const n = randInt(0, 3);
      return n === 0 ? cst(coeff) : mulN(cst(coeff), powN(X_NODE, n));
    }
    case 'sin': return mulN(cst(coeff), sinE(randomLinear(coeffRange)));
    case 'cos': return mulN(cst(coeff), cosE(randomLinear(coeffRange)));
    case 'exp': return mulN(cst(coeff), expE(randomLinear(coeffRange)));
    case 'ln': return mulN(cst(coeff), lnE(randomLinear(coeffRange)));
    case 'pow': {
      const n = randInt(2, 4);
      return mulN(cst(coeff), powN(randomLinear(coeffRange), n));
    }
    case 'compose': {
      const outer = choice(['sin', 'cos', 'exp', 'ln']);
      const innerKind = choice(['sinInner', 'expInner', 'powInner']);
      const inner = innerKind === 'sinInner' ? sinE(randomLinear(3))
        : innerKind === 'expInner' ? expE(randomLinear(3))
          : powN(randomLinear(3), randInt(2, 3));
      const wrapped = outer === 'sin' ? sinE(inner) : outer === 'cos' ? cosE(inner) : outer === 'exp' ? expE(inner) : lnE(inner);
      return mulN(cst(coeff), wrapped);
    }
    default: throw new Error(`randomAtomicTerm: unknown kind ${kind}`);
  }
}

function randomExpr(difficulty) {
  const numTerms = difficulty === 1 ? 2 : difficulty === 2 ? 3 : 4;
  // Retry if the terms happen to cancel (e.g. "−2x + 2x"): not just a
  // distractor-generation headache, it's a degenerate, uninteresting
  // problem ("f'(x) = 0" for no pedagogical reason) that shouldn't be
  // handed to a student.
  for (let attempt = 0; attempt < 15; attempt++) {
    const terms = [];
    for (let i = 0; i < numTerms; i++) terms.push(randomAtomicTerm(difficulty));
    const f = simplify(addN(...terms));
    const fp = simplify(diff(f));
    if (!(fp.op === 'const' && fp.value.isZero())) return f;
  }
  return simplify(addN(randomAtomicTerm(difficulty), mulN(cst(randNonZero(1, 5)), powN(X_NODE, 2))));
}

/** A single (non-sum) composed term guaranteed to need the chain rule —
 * for chain-rule-specific problems, never degenerates to a bare polynomial. */
function randomComposedSingle(difficulty) {
  if (difficulty === 3 && Math.random() < 0.6) {
    return simplify(randomAtomicTerm(difficulty, { kinds: ['compose'] }));
  }
  const kinds = difficulty === 1 ? ['sin', 'cos', 'exp'] : ['sin', 'cos', 'exp', 'ln', 'pow'];
  return simplify(randomAtomicTerm(difficulty, { kinds }));
}

/** Build an antiderivative F and its derivative f = F'(x) (simplified),
 * by constructing F directly and differentiating — guarantees f has a
 * known exact antiderivative without any symbolic integration. */
function randomAntiderivative(difficulty) {
  const outerChoices = difficulty === 1 ? ['pow'] : difficulty === 2 ? ['pow', 'sin', 'cos'] : ['pow', 'sin', 'cos', 'exp', 'ln'];
  const outer = choice(outerChoices);
  const coeffRange = difficulty === 1 ? 3 : difficulty === 2 ? 4 : 5;
  // ln's inner must stay positive across the bounds these antiderivatives
  // get numerically evaluated at (integers roughly in [0, 5] — see the
  // 6.1/8.1 generators), otherwise Math.log() hits zero or a negative
  // input and produces -Infinity/NaN.
  const inner = outer === 'ln' ? randomPositiveLinear(coeffRange) : randomLinear(coeffRange);
  const coef = randNonZero(-4, 4);
  let F_;
  if (outer === 'pow') { const n = randInt(2, difficulty === 1 ? 3 : 5); F_ = mulN(cst(coef), powN(inner, n)); }
  else if (outer === 'sin') F_ = mulN(cst(coef), sinE(inner));
  else if (outer === 'cos') F_ = mulN(cst(coef), cosE(inner));
  else if (outer === 'exp') F_ = mulN(cst(coef), expE(inner));
  else F_ = mulN(cst(coef), lnE(inner, true));
  F_ = simplify(F_);
  const f = simplify(diff(F_));
  return { F: F_, f, inner, outer };
}

if (typeof module !== 'undefined') {
  module.exports = {
    cst, X_NODE, addN, mulN, powN, divN, sinE, cosE, expE, lnE,
    diff, diffBuggy, simplify, evalNum, evalExact, evalSmart,
    toHTML, renderNode, polyToNode, scaleLeadingCoef, flipRandomTermSign,
    randomLinear, randomPositiveLinear, randomAtomicTerm, randomExpr, randomComposedSingle, randomAntiderivative,
  };
}
