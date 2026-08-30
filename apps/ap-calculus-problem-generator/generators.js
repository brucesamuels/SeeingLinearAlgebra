/*
 * generators.js — randomized AP Calculus problem generators.
 *
 * Every generator takes a difficulty level (1 = easy, 2 = medium, 3 = hard)
 * and returns a plain object:
 *   {
 *     unit, topic, topicName, difficulty,
 *     stem: HTML string of the question prompt,
 *     answerHTML: HTML string of the final answer,
 *     solution: [HTML strings], step-by-step teacher-key explanation,
 *     wrongHTML: [3 HTML strings], plausible multiple-choice distractors
 *   }
 *
 * All numeric work uses the exact Frac/polynomial helpers in core.js so
 * answers are exact fractions wherever the underlying math is rational.
 * Genuinely transcendental (calculator-active) results are rounded, which
 * matches how the AP exam itself scores those items.
 */

/* ---------------------------------------------------------------------- *
 * Unit 1 — Limits and Continuity
 * ---------------------------------------------------------------------- */

function genLimitFactor(difficulty) {
  const range = difficulty === 1 ? [-6, 6] : difficulty === 2 ? [-8, 8] : [-10, 10];
  const r = randNonZero(range[0], range[1]);
  let s; do { s = randNonZero(range[0], range[1]); } while (s === r);
  const a = difficulty === 1 ? 1 : randNonZero(-3, 3);

  let numHTML, denHTML, answer, steps;
  if (difficulty < 3) {
    const num = polyScale(polyMul([F(-r), F(1)], [F(-s), F(1)]), a);
    const den = [F(-r), F(1)];
    numHTML = polyToHTML(num); denHTML = polyToHTML(den);
    answer = F(a).mul(F(r - s));
    steps = [
      `Factor the numerator: ${a === 1 ? '' : a + '·'}(x − (${r}))(x − (${s})).`,
      `Cancel the common factor (x − (${r})) from numerator and denominator (valid since x ≠ ${r}).`,
      `The simplified function is ${a === 1 ? '' : a + '·'}(x − (${s})).`,
      `Substitute x = ${r}: ${a === 1 ? '' : a + '·'}(${r} − (${s})) = ${answer.toString()}.`,
    ];
  } else {
    let t; do { t = randNonZero(range[0], range[1]); } while (t === r || t === s);
    const num = polyScale(polyMul([F(-r), F(1)], [F(-s), F(1)]), a);
    const den = polyMul([F(-r), F(1)], [F(-t), F(1)]);
    numHTML = polyToHTML(num); denHTML = polyToHTML(den);
    answer = F(a).mul(F(r - s)).div(F(r - t));
    steps = [
      `Factor: numerator = ${a === 1 ? '' : a + '·'}(x−(${r}))(x−(${s})), denominator = (x−(${r}))(x−(${t})).`,
      `Cancel the common factor (x − (${r})).`,
      `The simplified function is ${a === 1 ? '' : a + '·'}(x−(${s})) / (x−(${t})).`,
      `Substitute x = ${r}: answer = ${answer.toString()}.`,
    ];
  }
  const stem = `Evaluate the limit:<br><span class="mathblock">lim<sub>x→${r}</sub> [ (${numHTML}) / (${denHTML}) ]</span>`;
  return {
    unit: 1, topic: '1.1', topicName: 'Evaluating Limits by Factoring', difficulty, stem,
    answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer),
  };
}

function genLimitInfinity(difficulty) {
  const maxDeg = difficulty === 1 ? 2 : difficulty === 2 ? 3 : 4;
  const numDeg = randInt(1, maxDeg);
  const denDeg = randInt(1, maxDeg);
  const coeffMax = difficulty === 1 ? 6 : difficulty === 2 ? 9 : 12;
  const numLead = randNonZero(-coeffMax, coeffMax);
  const denLead = randNonZero(-coeffMax, coeffMax);
  const num = randPoly(numDeg, numDeg, -coeffMax, coeffMax); num[numDeg] = F(numLead);
  const den = randPoly(denDeg, denDeg, -coeffMax, coeffMax); den[denDeg] = F(denLead);
  const toNegInf = difficulty === 3 && Math.random() < 0.5;
  const arrow = toNegInf ? '−∞' : '∞';

  let answerHTML, steps, wrongHTML;
  if (numDeg < denDeg) {
    answerHTML = '0';
    steps = [
      `Compare degrees: the numerator's degree (${numDeg}) is less than the denominator's degree (${denDeg}).`,
      `When the denominator grows faster, the fraction shrinks to 0 as x → ${arrow}.`,
    ];
    wrongHTML = ['∞', '−∞', F(numLead).div(F(denLead)).toString()];
  } else if (numDeg === denDeg) {
    const val = F(numLead).div(F(denLead));
    answerHTML = val.toString();
    steps = [
      `Both polynomials have the same degree (${numDeg}), so the limit equals the ratio of leading coefficients.`,
      `Leading coefficients: ${numLead} (numerator), ${denLead} (denominator).`,
      `Limit = ${numLead}/${denLead} = ${val.toString()}.`,
    ];
    wrongHTML = makeNumericDistractors(val);
  } else {
    const diff = numDeg - denDeg;
    let sign = Math.sign(numLead / denLead);
    if (toNegInf && diff % 2 === 1) sign = -sign;
    answerHTML = sign > 0 ? '∞' : '−∞';
    steps = [
      `The numerator's degree (${numDeg}) is greater than the denominator's degree (${denDeg}), so the limit is infinite.`,
      `The sign is determined by the ratio of leading coefficients (${numLead}/${denLead})${toNegInf ? ` and the parity of x<sup>${diff}</sup> as x → −∞` : ''}.`,
      `Limit = ${answerHTML}.`,
    ];
    wrongHTML = [sign > 0 ? '−∞' : '∞', '0', F(numLead).div(F(denLead)).toString()];
  }
  const stem = `Evaluate the limit:<br><span class="mathblock">lim<sub>x→${arrow}</sub> [ (${polyToHTML(num)}) / (${polyToHTML(den)}) ]</span>`;
  return { unit: 1, topic: '1.2', topicName: 'Limits at Infinity (End Behavior)', difficulty, stem, answerHTML, solution: steps, wrongHTML };
}

function genContinuityK(difficulty) {
  const range = difficulty === 1 ? [-5, 5] : difficulty === 2 ? [-7, 7] : [-9, 9];
  const c = randNonZero(difficulty === 1 ? 1 : 2, difficulty === 1 ? 4 : 6) * choice([1, -1]);
  const A = randNonZero(range[0], range[1]);
  const B = randInt(range[0], range[1]);
  const M = randInt(range[0], range[1]);
  const left = F(A).mul(F(c)).add(F(B));
  const K = left.sub(F(M)).div(F(c * c));
  const stem = `The function f is defined by<br>` +
    `<span class="mathblock">f(x) = ${polyToHTML(linear(A, B))}, &nbsp; x &lt; ${c}<br>` +
    `f(x) = kx<sup>2</sup> ${M >= 0 ? '+' : '−'} ${Math.abs(M)}, &nbsp; x ≥ ${c}</span><br>` +
    `For what value of k is f continuous at x = ${c}?`;
  const steps = [
    `For continuity at x = ${c}, the two pieces must agree: ${A}(${c}) + ${B} = k(${c})<sup>2</sup> + ${M}.`,
    `Simplify the left side: ${left.toString()}.`,
    `Solve for k: k = (${left.toString()} − ${M}) / ${c * c} = ${K.toString()}.`,
  ];
  return { unit: 1, topic: '1.3', topicName: 'Continuity: Solving for a Constant', difficulty, stem, answerHTML: K.toString(), solution: steps, wrongHTML: makeNumericDistractors(K) };
}

/* ---------------------------------------------------------------------- *
 * Unit 2 — Differentiation: Basic Rules
 * ---------------------------------------------------------------------- */

function genPowerRule(difficulty) {
  const maxDeg = difficulty === 1 ? 3 : difficulty === 2 ? 4 : 5;
  const p = randPoly(2, maxDeg, -9, 9);
  const D = polyDeriv(p);
  const correctHTML = polyToHTML(D);

  const wrong1 = polyTrim(p.map((c, i) => (i === 0 ? F(0) : c.mul(F(i))))); // forgot to decrement exponent
  let wrong2 = D.slice();
  for (let i = 0; i < wrong2.length; i++) { if (!wrong2[i].isZero()) { wrong2[i] = F(0); break; } } // dropped a term
  wrong2 = polyTrim(wrong2);
  let wrong3 = D.slice();
  const nzIdx = wrong3.map((c, i) => (c.isZero() ? -1 : i)).filter((i) => i >= 0);
  if (nzIdx.length) { const idx = choice(nzIdx); wrong3[idx] = wrong3[idx].neg(); } // sign error
  wrong3 = polyTrim(wrong3);

  const seen = new Set([correctHTML]);
  const wrongHTML = [];
  for (const w of [wrong1, wrong2, wrong3].map((w) => polyToHTML(w))) { if (!seen.has(w)) { seen.add(w); wrongHTML.push(w); } }
  let guard = 0;
  while (wrongHTML.length < 3 && guard < 20) {
    guard++;
    const jitter = D.slice();
    const i = randInt(0, jitter.length - 1);
    jitter[i] = jitter[i].add(F(choice([1, -1, 2, -2])));
    const h = polyToHTML(polyTrim(jitter));
    if (!seen.has(h)) { seen.add(h); wrongHTML.push(h); }
  }

  const stem = `Let f(x) = ${polyToHTML(p)}. Find f&prime;(x).`;
  const steps = [
    `Apply the power rule term by term: d/dx[x<sup>n</sup>] = n·x<sup>n−1</sup>.`,
    `f&prime;(x) = ${correctHTML}.`,
  ];
  return { unit: 2, topic: '2.1', topicName: 'The Power Rule', difficulty, stem, answerHTML: correctHTML, solution: steps, wrongHTML };
}

function genBasicRulesSum(difficulty) {
  const A = randNonZero(-6, 6);
  const n = randInt(2, 4);
  const B = randNonZero(-6, 6);
  const C = randNonZero(-6, 6);
  const includeExp = difficulty >= 2;
  const includeLn = difficulty >= 3;
  const D = includeExp ? randNonZero(-5, 5) : 0;
  const E = includeLn ? randNonZero(-5, 5) : 0;

  const joinTerms = (terms) => {
    let html = (terms[0].sign < 0 ? '−' : '') + terms[0].text;
    for (let i = 1; i < terms.length; i++) html += terms[i].sign < 0 ? ` − ${terms[i].text}` : ` + ${terms[i].text}`;
    return html;
  };
  // Coefficient magnitude for display: omit a bare "1" (e.g. "x", not "1x").
  const c1 = (v) => (Math.abs(v) === 1 ? '' : `${Math.abs(v)}`);

  const termsStem = [
    { sign: A < 0 ? -1 : 1, text: `${c1(A)}x<sup>${n}</sup>` },
    { sign: B < 0 ? -1 : 1, text: `${c1(B)}sin x` },
    { sign: C < 0 ? -1 : 1, text: `${c1(C)}cos x` },
  ];
  if (includeExp) termsStem.push({ sign: D < 0 ? -1 : 1, text: `${c1(D)}e<sup>x</sup>` });
  if (includeLn) termsStem.push({ sign: E < 0 ? -1 : 1, text: `${c1(E)}ln x` });
  const stemExpr = joinTerms(termsStem);

  const coefAn = A * n;
  const derivTerms = [
    { sign: coefAn < 0 ? -1 : 1, text: n - 1 === 1 ? `${c1(coefAn)}x` : `${c1(coefAn)}x<sup>${n - 1}</sup>` },
    { sign: B < 0 ? -1 : 1, text: `${c1(B)}cos x` },
    { sign: C < 0 ? 1 : -1, text: `${c1(C)}sin x` }, // d/dx[C cos x] = -C sin x
  ];
  if (includeExp) derivTerms.push({ sign: D < 0 ? -1 : 1, text: `${c1(D)}e<sup>x</sup>` });
  if (includeLn) derivTerms.push({ sign: E < 0 ? -1 : 1, text: `${Math.abs(E)}/x` });
  const derivExpr = joinTerms(derivTerms);

  const stem = `Let f(x) = ${stemExpr}. Find f&prime;(x).`;
  const steps = [
    `Differentiate term by term using the power, sine, and cosine rules${includeExp ? ', plus d/dx[e<sup>x</sup>] = e<sup>x</sup>' : ''}${includeLn ? ', and d/dx[ln x] = 1/x' : ''}.`,
    `d/dx[sin x] = cos x, &nbsp; d/dx[cos x] = −sin x.`,
    `f&prime;(x) = ${derivExpr}.`,
  ];

  const wrong1Terms = derivTerms.map((t) => ({ ...t }));
  wrong1Terms[2] = { sign: C < 0 ? -1 : 1, text: `${Math.abs(C)}sin x` }; // dropped the negative on cos'
  const wrong2Terms = derivTerms.map((t) => ({ ...t }));
  wrong2Terms[0] = { sign: A < 0 ? -1 : 1, text: n === 2 ? `${Math.abs(A)}x` : `${Math.abs(A)}x<sup>${n}</sup>` }; // forgot power rule
  const wrong3Terms = derivTerms.map((t) => ({ ...t }));
  const flipIdx = randInt(0, wrong3Terms.length - 1);
  wrong3Terms[flipIdx] = { ...wrong3Terms[flipIdx], sign: -wrong3Terms[flipIdx].sign };

  const seen = new Set([derivExpr]);
  const wrongHTML = [];
  for (const t of [wrong1Terms, wrong2Terms, wrong3Terms]) {
    const w = joinTerms(t);
    if (!seen.has(w)) { seen.add(w); wrongHTML.push(w); }
  }
  let guard = 0;
  while (wrongHTML.length < 3 && guard < 20) {
    guard++;
    const idx = randInt(0, derivTerms.length - 1);
    const t = derivTerms.map((x) => ({ ...x }));
    t[idx].sign = -t[idx].sign;
    const w = joinTerms(t);
    if (!seen.has(w)) { seen.add(w); wrongHTML.push(w); }
  }

  return { unit: 2, topic: '2.2', topicName: 'Derivatives of Trig, Exponential & Log Sums', difficulty, stem, answerHTML: derivExpr, solution: steps, wrongHTML };
}

function genProductRule(difficulty) {
  const range = difficulty === 1 ? [-4, 4] : difficulty === 2 ? [-6, 6] : [-8, 8];
  const a = randNonZero(range[0], range[1]), b = randInt(range[0], range[1]);
  const c = randNonZero(range[0], range[1]), d = randInt(range[0], range[1]), e = randInt(range[0], range[1]);
  const x0 = randInt(-3, 3);
  const u = linear(a, b), v = [F(e), F(d), F(c)];
  const uAt = polyEval(u, x0), vAt = polyEval(v, x0);
  const uP = F(a), vPPoly = polyDeriv(v), vPAt = polyEval(vPPoly, x0);
  const answer = uP.mul(vAt).add(uAt.mul(vPAt));
  const stem = `Let f(x) = (${polyToHTML(u)})(${polyToHTML(v)}). Use the product rule to find f&prime;(${x0}).`;
  const steps = [
    `Product rule: f&prime;(x) = u&prime;(x)v(x) + u(x)v&prime;(x), where u(x) = ${polyToHTML(u)} and v(x) = ${polyToHTML(v)}.`,
    `u&prime;(x) = ${a}, &nbsp; v&prime;(x) = ${polyToHTML(vPPoly)}.`,
    `At x = ${x0}: u = ${uAt}, v = ${vAt}, u&prime; = ${uP}, v&prime; = ${vPAt}.`,
    `f&prime;(${x0}) = (${uP})(${vAt}) + (${uAt})(${vPAt}) = ${answer.toString()}.`,
  ];
  return { unit: 2, topic: '2.3', topicName: 'The Product Rule', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

function genQuotientRule(difficulty) {
  const range = difficulty === 1 ? [-4, 4] : difficulty === 2 ? [-6, 6] : [-8, 8];
  let a, b, c, d, e, x0, vAtNum;
  do {
    a = randNonZero(range[0], range[1]); b = randInt(range[0], range[1]);
    c = randNonZero(range[0], range[1]); d = randInt(range[0], range[1]); e = randInt(range[0], range[1]);
    x0 = randInt(-3, 3);
    vAtNum = c * x0 * x0 + d * x0 + e;
  } while (vAtNum === 0);
  const u = linear(a, b), v = [F(e), F(d), F(c)];
  const uAt = polyEval(u, x0), vAt = polyEval(v, x0);
  const uP = F(a), vP = polyDeriv(v), vPAt = polyEval(vP, x0);
  const answer = uP.mul(vAt).sub(uAt.mul(vPAt)).div(vAt.mul(vAt));
  const stem = `Let f(x) = (${polyToHTML(u)}) / (${polyToHTML(v)}). Use the quotient rule to find f&prime;(${x0}).`;
  const steps = [
    `Quotient rule: f&prime;(x) = [u&prime;(x)v(x) − u(x)v&prime;(x)] / [v(x)]<sup>2</sup>, where u(x) = ${polyToHTML(u)} and v(x) = ${polyToHTML(v)}.`,
    `u&prime;(x) = ${a}, &nbsp; v&prime;(x) = ${polyToHTML(vP)}.`,
    `At x = ${x0}: u = ${uAt}, v = ${vAt}, u&prime; = ${uP}, v&prime; = ${vPAt}.`,
    `f&prime;(${x0}) = [(${uP})(${vAt}) − (${uAt})(${vPAt})] / (${vAt})<sup>2</sup> = ${answer.toString()}.`,
  ];
  return { unit: 2, topic: '2.4', topicName: 'The Quotient Rule', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

/* ---------------------------------------------------------------------- *
 * Unit 3 — Composite, Implicit & Inverse Functions
 * ---------------------------------------------------------------------- */

function genChainNumeric(difficulty) {
  const n = difficulty === 1 ? randInt(2, 3) : difficulty === 2 ? randInt(3, 4) : randInt(4, 5);
  const a = randNonZero(-3, 3);
  const b = randInt(-4, 4);
  const x0 = randInt(-2, 2);
  const innerHTML = polyToHTML(linear(a, b));
  const inner = a * x0 + b;
  const answer = F(n).mul(F(inner).pow(n - 1)).mul(F(a));
  const stem = `Let f(x) = (${innerHTML})<sup>${n}</sup>. Use the chain rule to find f&prime;(${x0}).`;
  const steps = [
    `Chain rule: d/dx[(g(x))<sup>${n}</sup>] = ${n}(g(x))<sup>${n - 1}</sup>·g&prime;(x), where g(x) = ${innerHTML}.`,
    `g(${x0}) = ${inner}, &nbsp; g&prime;(x) = ${a}.`,
    `f&prime;(${x0}) = ${n}(${inner})<sup>${n - 1}</sup>(${a}) = ${answer.toString()}.`,
  ];
  return { unit: 3, topic: '3.1', topicName: 'The Chain Rule (Evaluate Numerically)', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

function genChainSymbolic(difficulty) {
  const p = randNonZero(-4, 4);
  const q = randInt(-5, 5);
  const innerHTML = polyToHTML(linear(p, q));
  const kinds = difficulty === 1 ? ['sin', 'cos', 'exp'] : difficulty === 2 ? ['sin', 'cos', 'exp', 'ln'] : ['sin', 'cos', 'exp', 'ln', 'pow'];
  const kind = choice(kinds);
  const trig = (coef, name) => {
    const c = coef === 1 ? '' : coef === -1 ? '−' : `${coef}`;
    return `${c}${name}(${innerHTML})`;
  };

  let stemFunc, derivExpr, wrongCandidates;
  if (kind === 'sin') {
    stemFunc = `sin(${innerHTML})`;
    derivExpr = trig(p, 'cos');
    wrongCandidates = [trig(1, 'cos'), trig(p, 'sin'), trig(-p, 'cos'), trig(p + 2, 'cos'), trig(p - 2, 'cos')];
  } else if (kind === 'cos') {
    stemFunc = `cos(${innerHTML})`;
    derivExpr = trig(-p, 'sin');
    wrongCandidates = [trig(1, 'sin'), trig(p, 'sin'), trig(-p, 'cos'), trig(-p + 2, 'sin'), trig(-p - 2, 'sin')];
  } else if (kind === 'exp') {
    stemFunc = `e<sup>${innerHTML}</sup>`;
    derivExpr = `${p === 1 ? '' : p === -1 ? '−' : p}e<sup>${innerHTML}</sup>`;
    wrongCandidates = [
      `e<sup>${innerHTML}</sup>`, `${p * p}e<sup>${innerHTML}</sup>`, `${p}·(${innerHTML})·e<sup>${innerHTML}</sup>`,
      `${p + 2}e<sup>${innerHTML}</sup>`, `${p - 2}e<sup>${innerHTML}</sup>`,
    ];
  } else if (kind === 'ln') {
    stemFunc = `ln(${innerHTML})`;
    derivExpr = p === 1 ? `1/(${innerHTML})` : `${p}/(${innerHTML})`;
    wrongCandidates = [`1/(${innerHTML})`, `${p}/x`, `${p}·ln(${innerHTML})`, `${p + 2}/(${innerHTML})`, `${p - 2}/(${innerHTML})`];
  } else {
    const n = randInt(2, 4);
    stemFunc = `(${innerHTML})<sup>${n}</sup>`;
    const coefProduct = n * p;
    derivExpr = `${coefProduct}(${innerHTML})<sup>${n - 1}</sup>`;
    wrongCandidates = [
      `${n}(${innerHTML})<sup>${n - 1}</sup>`, `${coefProduct}(${innerHTML})<sup>${n}</sup>`, `${p}(${innerHTML})<sup>${n - 1}</sup>`,
      `${coefProduct + 2}(${innerHTML})<sup>${n - 1}</sup>`, `${coefProduct - 2}(${innerHTML})<sup>${n - 1}</sup>`,
    ];
  }

  const stem = `Let f(x) = ${stemFunc}. Find f&prime;(x).`;
  const steps = [
    `Apply the chain rule: differentiate the outer function, then multiply by the derivative of the inner function g(x) = ${innerHTML}, where g&prime;(x) = ${p}.`,
    `f&prime;(x) = ${derivExpr}.`,
  ];
  const seen = new Set([derivExpr]);
  const wrongHTML = [];
  for (const w of wrongCandidates) {
    if (!seen.has(w)) { seen.add(w); wrongHTML.push(w); }
    if (wrongHTML.length === 3) break;
  }
  return { unit: 3, topic: '3.2', topicName: 'The Chain Rule (Symbolic Derivative)', difficulty, stem, answerHTML: derivExpr, solution: steps, wrongHTML };
}

function genImplicit(difficulty) {
  if (difficulty < 3) {
    const [p, q, r] = choice(PYTHAGOREAN_TRIPLES);
    const swap = Math.random() < 0.5;
    const x0 = swap ? q : p, y0 = swap ? p : q;
    const rr = r * r;
    const answer = F(-x0, y0);
    const stem = `The point (${x0}, ${y0}) lies on the curve x<sup>2</sup> + y<sup>2</sup> = ${rr}. Find dy/dx at this point.`;
    const steps = [
      `Differentiate implicitly: 2x + 2y·(dy/dx) = 0.`,
      `Solve for dy/dx: dy/dx = −x/y.`,
      `At (${x0}, ${y0}): dy/dx = −${x0}/${y0} = ${answer.toString()}.`,
    ];
    return { unit: 3, topic: '3.3', topicName: 'Implicit Differentiation', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
  }
  let x0, y0, A;
  do { x0 = randNonZero(-4, 4); y0 = randNonZero(-4, 4); A = randNonZero(-3, 3); } while (y0 === 0);
  const C = A * x0 * x0 + y0 * y0 * y0;
  const answer = F(-2 * A * x0).div(F(3 * y0 * y0));
  const stem = `The point (${x0}, ${y0}) lies on the curve ${A}x<sup>2</sup> + y<sup>3</sup> = ${C}. Find dy/dx at this point.`;
  const steps = [
    `Differentiate implicitly: ${2 * A}x + 3y<sup>2</sup>·(dy/dx) = 0.`,
    `Solve for dy/dx: dy/dx = −${2 * A}x / (3y<sup>2</sup>).`,
    `At (${x0}, ${y0}): dy/dx = −${2 * A * x0} / ${3 * y0 * y0} = ${answer.toString()}.`,
  ];
  return { unit: 3, topic: '3.3', topicName: 'Implicit Differentiation', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

function genInverseDeriv(difficulty) {
  const a = randInt(-5, 5);
  const b = randInt(-5, 5);
  const range = difficulty === 1 ? [2, 6] : difficulty === 2 ? [2, 9] : [2, 12];
  const mN = randNonZero(-range[1], range[1]);
  const mD = difficulty === 3 ? randInt(2, 4) : 1;
  const m = F(mN, mD);
  const answer = F(1).div(m);
  const stem = `Suppose f is differentiable and invertible, with f(${a}) = ${b} and f&prime;(${a}) = ${m.toString()}. Find (f<sup>−1</sup>)&prime;(${b}).`;
  const steps = [
    `Use the inverse function derivative formula: (f<sup>−1</sup>)&prime;(b) = 1 / f&prime;(f<sup>−1</sup>(b)).`,
    `Since f(${a}) = ${b}, we know f<sup>−1</sup>(${b}) = ${a}.`,
    `(f<sup>−1</sup>)&prime;(${b}) = 1 / f&prime;(${a}) = 1 / (${m.toString()}) = ${answer.toString()}.`,
  ];
  return { unit: 3, topic: '3.4', topicName: 'Derivatives of Inverse Functions', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

/* ---------------------------------------------------------------------- *
 * Unit 4 — Contextual Applications of Differentiation
 * ---------------------------------------------------------------------- */

function genMotion(difficulty) {
  const maxCoeff = difficulty === 1 ? 5 : difficulty === 2 ? 7 : 9;
  const s = randPoly(3, 3, -maxCoeff, maxCoeff);
  const v = polyDeriv(s);
  const acc = polyDeriv(v);
  const t0 = randInt(1, 3);
  const mode = choice(['velocity', 'acceleration', 'speed']);
  const vAt = polyEval(v, t0), aAt = polyEval(acc, t0);
  let stem, answerHTML, steps, wrongHTML;
  if (mode === 'velocity') {
    stem = `The position of a particle moving along a line is given by s(t) = ${polyToHTML(s)} (t in seconds, s in meters). Find the particle's velocity at t = ${t0}.`;
    answerHTML = `${vAt.toString()} m/s`;
    steps = [
      `Velocity is the derivative of position: v(t) = s&prime;(t) = ${polyToHTML(v)}.`,
      `v(${t0}) = ${vAt.toString()} m/s.`,
    ];
    wrongHTML = makeNumericDistractors(vAt).map((w) => `${w} m/s`);
  } else if (mode === 'acceleration') {
    stem = `The position of a particle moving along a line is given by s(t) = ${polyToHTML(s)} (t in seconds, s in meters). Find the particle's acceleration at t = ${t0}.`;
    answerHTML = `${aAt.toString()} m/s²`;
    steps = [
      `Velocity: v(t) = s&prime;(t) = ${polyToHTML(v)}. Acceleration: a(t) = v&prime;(t) = ${polyToHTML(acc)}.`,
      `a(${t0}) = ${aAt.toString()} m/s².`,
    ];
    wrongHTML = makeNumericDistractors(aAt).map((w) => `${w} m/s²`);
  } else {
    const speedingUp = vAt.toFloat() * aAt.toFloat() > 0;
    answerHTML = vAt.isZero() ? 'momentarily at rest' : (speedingUp ? 'speeding up' : 'slowing down');
    stem = `The position of a particle moving along a line is given by s(t) = ${polyToHTML(s)} (t in seconds, s in meters). Is the particle speeding up or slowing down at t = ${t0}? Justify your answer.`;
    steps = [
      `v(t) = ${polyToHTML(v)}, so v(${t0}) = ${vAt.toString()}. a(t) = ${polyToHTML(acc)}, so a(${t0}) = ${aAt.toString()}.`,
      `A particle speeds up when v(t) and a(t) have the same sign, and slows down when they have opposite signs.`,
      `Since v(${t0}) = ${vAt.toString()} and a(${t0}) = ${aAt.toString()}, the particle is ${answerHTML} at t = ${t0}.`,
    ];
    wrongHTML = ['speeding up', 'slowing down', 'momentarily at rest', 'moving at constant velocity'].filter((x) => x !== answerHTML).slice(0, 3);
  }
  return { unit: 4, topic: '4.1', topicName: 'Motion: Position, Velocity & Acceleration', difficulty, stem, answerHTML, solution: steps, wrongHTML };
}

function genRelatedRates(difficulty) {
  const kind = choice(['ladder', 'sphere']);
  if (kind === 'ladder') {
    const [p, q, L] = choice(PYTHAGOREAN_TRIPLES);
    const dxdt = randNonZero(1, difficulty === 1 ? 3 : difficulty === 2 ? 5 : 8);
    const answer = F(-p * dxdt, q);
    const stem = `A ${L}-foot ladder leans against a vertical wall. The bottom of the ladder is being pulled away from the wall at a rate of ${dxdt} ft/s. How fast is the top of the ladder sliding down the wall at the moment the bottom of the ladder is ${p} ft from the wall?`;
    const steps = [
      `Let x = distance from the wall to the base, y = height of the top of the ladder. Then x<sup>2</sup> + y<sup>2</sup> = ${L}<sup>2</sup>.`,
      `Differentiate with respect to t: 2x(dx/dt) + 2y(dy/dt) = 0, so dy/dt = −(x/y)(dx/dt).`,
      `When x = ${p}: y = √(${L}<sup>2</sup> − ${p}<sup>2</sup>) = ${q}.`,
      `dy/dt = −(${p}/${q})(${dxdt}) = ${answer.toString()} ft/s (negative means the top is sliding down).`,
    ];
    return { unit: 4, topic: '4.2', topicName: 'Related Rates', difficulty, stem, answerHTML: `${answer.toString()} ft/s`, solution: steps, wrongHTML: makeNumericDistractors(answer).map((w) => `${w} ft/s`) };
  }
  const r0 = randInt(2, difficulty === 1 ? 4 : difficulty === 2 ? 6 : 9);
  const dVdt = randNonZero(1, 6) * choice([4, 8, 12]);
  const coeff = F(dVdt, 4 * r0 * r0);
  const overPi = (c) => (c.d === 1 ? `${c.n}/π` : `${c.n}/(${c.d}π)`);
  const stem = `Air is pumped into a spherical balloon so that its volume increases at a rate of ${dVdt} cubic inches per second. How fast is the radius increasing when the radius is ${r0} inches? (Leave your answer in terms of π.)`;
  const steps = [
    `V = (4/3)πr<sup>3</sup>. Differentiate with respect to t: dV/dt = 4πr<sup>2</sup>(dr/dt).`,
    `Solve for dr/dt: dr/dt = (dV/dt) / (4πr<sup>2</sup>).`,
    `dr/dt = ${dVdt} / (4π(${r0})<sup>2</sup>) = ${overPi(coeff)} in/s.`,
  ];
  const wrongCoeffs = [coeff.neg(), coeff.add(F(1)), coeff.sub(F(1)), coeff.mul(F(2)), coeff.div(F(2))];
  const seenPi = new Set([coeff.toString()]);
  const wrongHTML = [];
  for (const c of wrongCoeffs) { if (!seenPi.has(c.toString())) { seenPi.add(c.toString()); wrongHTML.push(`${overPi(c)} in/s`); } if (wrongHTML.length === 3) break; }
  return { unit: 4, topic: '4.2', topicName: 'Related Rates', difficulty, stem, answerHTML: `${overPi(coeff)} in/s`, solution: steps, wrongHTML };
}

function genLinearApprox(difficulty) {
  const maxCoeff = difficulty === 1 ? 4 : difficulty === 2 ? 6 : 8;
  const p = randPoly(2, 2, -maxCoeff, maxCoeff);
  const x0 = randInt(-3, 3);
  const dx = choice([1, -1, 2, -2]);
  const x1 = x0 + dx;
  const fAt = polyEval(p, x0);
  const fP = polyDeriv(p);
  const fPAt = polyEval(fP, x0);
  const answer = fAt.add(fPAt.mul(F(dx)));
  const stem = `Let f(x) = ${polyToHTML(p)}. Use the line tangent to f at x = ${x0} to approximate f(${x1}).`;
  const steps = [
    `f(${x0}) = ${fAt.toString()}, and f&prime;(x) = ${polyToHTML(fP)}, so f&prime;(${x0}) = ${fPAt.toString()}.`,
    `Tangent line (linear approximation): L(x) = f(${x0}) + f&prime;(${x0})(x − ${x0}).`,
    `L(${x1}) = ${fAt.toString()} + (${fPAt.toString()})(${x1} − ${x0}) = ${answer.toString()}.`,
  ];
  return { unit: 4, topic: '4.3', topicName: 'Local Linearization (Tangent Line Approximation)', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

function genLHopital(difficulty) {
  const range = difficulty === 1 ? [-5, 5] : difficulty === 2 ? [-7, 7] : [-9, 9];
  const a = randInt(Math.max(range[0], -3), 3);
  let s; do { s = randNonZero(range[0], range[1]); } while (s === a);
  let t; do { t = randNonZero(range[0], range[1]); } while (t === a || t === s);
  const A = randNonZero(-3, 3), B = randNonZero(-3, 3);
  const p = polyScale(polyMul([F(-a), F(1)], [F(-s), F(1)]), A);
  const q = polyScale(polyMul([F(-a), F(1)], [F(-t), F(1)]), B);
  const pP = polyDeriv(p), qP = polyDeriv(q);
  const pPAt = polyEval(pP, a), qPAt = polyEval(qP, a);
  const answer = pPAt.div(qPAt);
  const stem = `Evaluate using L'Hôpital's Rule:<br><span class="mathblock">lim<sub>x→${a}</sub> [ (${polyToHTML(p)}) / (${polyToHTML(q)}) ]</span>`;
  const steps = [
    `Direct substitution gives the indeterminate form 0/0, since x = ${a} is a root of both the numerator and denominator.`,
    `L'Hôpital's Rule: the limit equals lim<sub>x→${a}</sub> [p&prime;(x)/q&prime;(x)], where p&prime;(x) = ${polyToHTML(pP)} and q&prime;(x) = ${polyToHTML(qP)}.`,
    `Substitute x = ${a}: ${pPAt.toString()} / ${qPAt.toString()} = ${answer.toString()}.`,
  ];
  return { unit: 4, topic: '4.4', topicName: "L'Hôpital's Rule", difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

/* ---------------------------------------------------------------------- *
 * Unit 5 — Analytical Applications of Differentiation
 * ---------------------------------------------------------------------- */

function genFirstDerivTest(difficulty) {
  const range = difficulty === 1 ? [-6, 6] : difficulty === 2 ? [-8, 8] : [-10, 10];
  let p = randInt(range[0], range[1]);
  let q; do { q = randInt(range[0], range[1]); } while (q === p);
  if (p > q) [p, q] = [q, p];
  const A = randNonZero(-3, 3);
  const fP = polyScale(polyMul([F(-p), F(1)], [F(-q), F(1)]), A);
  const f = polyAntideriv(fP);
  const askMin = Math.random() < 0.5;
  const minLoc = A > 0 ? q : p;
  const maxLoc = A > 0 ? p : q;
  const answer = askMin ? minLoc : maxLoc;
  const otherLoc = askMin ? maxLoc : minLoc;
  const stem = `Let f be a function with f(x) = ${polyToHTML(f)} and f&prime;(x) = ${polyToHTML(fP)}. At what x-value does f have a local ${askMin ? 'minimum' : 'maximum'}?`;
  const steps = [
    `f&prime;(x) = 0 at x = ${p} and x = ${q}. These are the critical points.`,
    `The leading coefficient of f&prime; is ${A} (${A > 0 ? 'positive: opens upward' : 'negative: opens downward'}), so f&prime; is ${A > 0 ? 'negative between the roots and positive outside' : 'positive between the roots and negative outside'}.`,
    `By the First Derivative Test, f has a local ${A > 0 ? 'maximum' : 'minimum'} at x = ${p} and a local ${A > 0 ? 'minimum' : 'maximum'} at x = ${q}.`,
    `So the local ${askMin ? 'minimum' : 'maximum'} occurs at x = ${answer}.`,
  ];
  const wl = [`${otherLoc}`, `${answer + 1}`, `${answer - 1}`];
  const seen = new Set([`${answer}`]);
  const wrongHTML = [];
  for (const w of wl) { if (!seen.has(w)) { seen.add(w); wrongHTML.push(w); } }
  let guard = 0;
  while (wrongHTML.length < 3 && guard < 20) { guard++; const v = `${answer + randNonZero(-4, 4)}`; if (!seen.has(v)) { seen.add(v); wrongHTML.push(v); } }
  return { unit: 5, topic: '5.1', topicName: 'Increasing/Decreasing & the First Derivative Test', difficulty, stem, answerHTML: `x = ${answer}`, solution: steps, wrongHTML: wrongHTML.map((w) => `x = ${w}`) };
}

function genConcavity(difficulty) {
  const range = difficulty === 1 ? [-5, 5] : difficulty === 2 ? [-7, 7] : [-9, 9];
  const xInf = randInt(range[0], range[1]);
  const a = randNonZero(-3, 3);
  const b = -3 * a * xInf;
  const c = randInt(range[0], range[1]);
  const d = randInt(range[0], range[1]);
  const f = [F(d), F(c), F(b), F(a)];
  const fP = polyDeriv(f);
  const fPP = polyDeriv(fP);
  const stem = `Let f(x) = ${polyToHTML(f)}. Find the x-coordinate of the point of inflection of f.`;
  const steps = [
    `f&prime;(x) = ${polyToHTML(fP)}, and f&Prime;(x) = ${polyToHTML(fPP)}.`,
    `Set f&Prime;(x) = 0 and solve: ${polyToHTML(fPP)} = 0 → x = ${xInf}.`,
    `f&Prime; changes sign at x = ${xInf} (it is linear with nonzero slope), so this is a point of inflection.`,
  ];
  const answer = F(xInf);
  return { unit: 5, topic: '5.2', topicName: 'Concavity & the Second Derivative Test', difficulty, stem, answerHTML: `x = ${answer.toString()}`, solution: steps, wrongHTML: makeNumericDistractors(answer).map((w) => `x = ${w}`) };
}

function genOptimization(difficulty) {
  const kind = choice(['fence', 'wall']);
  const base = difficulty === 1 ? [8, 16] : difficulty === 2 ? [12, 24] : [16, 32];
  if (kind === 'fence') {
    let P; do { P = randInt(base[0], base[1]); } while (P % 4 !== 0);
    const x = P / 4;
    const area = x * x;
    const stem = `A rectangular garden is to be enclosed by ${P} feet of fencing. What dimensions maximize the enclosed area, and what is that maximum area?`;
    const steps = [
      `Let x and y be the side lengths. The perimeter constraint gives 2x + 2y = ${P}, so y = ${P / 2} − x.`,
      `Area: A(x) = x(${P / 2} − x) = ${P / 2}x − x<sup>2</sup>.`,
      `A&prime;(x) = ${P / 2} − 2x. Set A&prime;(x) = 0: x = ${x}.`,
      `A&Prime;(x) = −2 &lt; 0, confirming a maximum. Since y = ${P / 2} − ${x} = ${x}, the maximum-area rectangle is a ${x} ft × ${x} ft square with area ${area} ft².`,
    ];
    const answerHTML = `${x} ft × ${x} ft (area = ${area} ft²)`;
    const candidates = [
      [x - 1, x + 1], [x + 2, x - 2], [P / 2, 0], [x + 1, x - 1], [1, P / 2 - 1],
    ].filter(([w, h]) => w >= 0 && h >= 0);
    const seenOpt = new Set([answerHTML]);
    const wrongHTML = [];
    for (const [w, h] of candidates) {
      const txt = `${w} ft × ${h} ft (area = ${w * h} ft²)`;
      if (!seenOpt.has(txt)) { seenOpt.add(txt); wrongHTML.push(txt); }
      if (wrongHTML.length === 3) break;
    }
    return { unit: 5, topic: '5.3', topicName: 'Optimization Problems', difficulty, stem, answerHTML, solution: steps, wrongHTML };
  }
  let Ftot; do { Ftot = randInt(base[0], base[1]); } while (Ftot % 4 !== 0);
  const x = Ftot / 4, y = Ftot / 2;
  const area = x * y;
  const stem = `A farmer has ${Ftot} feet of fencing to enclose a rectangular pen that uses an existing straight wall as one side (no fencing needed along the wall). Find the dimensions that maximize the enclosed area.`;
  const steps = [
    `Let x = the length of each side perpendicular to the wall, and y = the length parallel to the wall. Fencing constraint: 2x + y = ${Ftot}, so y = ${Ftot} − 2x.`,
    `Area: A(x) = xy = x(${Ftot} − 2x) = ${Ftot}x − 2x<sup>2</sup>.`,
    `A&prime;(x) = ${Ftot} − 4x. Set A&prime;(x) = 0: x = ${x}.`,
    `A&Prime;(x) = −4 &lt; 0, confirming a maximum. y = ${Ftot} − 2(${x}) = ${y}. Maximum area = ${x} × ${y} = ${area} ft².`,
  ];
  const answerHTML = `x = ${x} ft, y = ${y} ft (area = ${area} ft²)`;
  const wallCandidates = [
    [y, x], [x + 1, Ftot - 2 * (x + 1)], [x - 1, Ftot - 2 * (x - 1)], [Ftot / 2, 0], [x + 2, Ftot - 2 * (x + 2)],
  ].filter(([cx, cy]) => cx >= 0 && cy >= 0);
  const seenWall = new Set([answerHTML]);
  const wrongHTML = [];
  for (const [cx, cy] of wallCandidates) {
    const txt = `x = ${cx} ft, y = ${cy} ft (area = ${cx * cy} ft²)`;
    if (!seenWall.has(txt)) { seenWall.add(txt); wrongHTML.push(txt); }
    if (wrongHTML.length === 3) break;
  }
  return { unit: 5, topic: '5.3', topicName: 'Optimization Problems', difficulty, stem, answerHTML, solution: steps, wrongHTML };
}

/* ---------------------------------------------------------------------- *
 * Unit 6 — Integration and Accumulation of Change
 * ---------------------------------------------------------------------- */

function genDefiniteIntegral(difficulty) {
  const maxDeg = difficulty === 1 ? 2 : difficulty === 2 ? 3 : 4;
  const p = randPoly(1, maxDeg, -6, 6);
  const a = randInt(-3, 2);
  const b = randInt(a + 1, a + 4);
  const P = polyAntideriv(p);
  const Pb = polyEval(P, b), Pa = polyEval(P, a);
  const answer = Pb.sub(Pa);
  const stem = `Evaluate the definite integral:<br><span class="mathblock">∫<sub>${a}</sub><sup>${b}</sup> (${polyToHTML(p)}) dx</span>`;
  const steps = [
    `Find an antiderivative: F(x) = ${polyToHTML(P)}.`,
    `By the Fundamental Theorem of Calculus: F(${b}) − F(${a}) = ${Pb.toString()} − (${Pa.toString()}) = ${answer.toString()}.`,
  ];
  return { unit: 6, topic: '6.1', topicName: 'Definite Integrals (FTC)', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

function genFTCAccum(difficulty) {
  const f = randPoly(1, 2, -6, 6);
  const a = randInt(-3, 3);
  const x0 = randInt(-2, 3);
  if (difficulty === 1) {
    const val = polyEval(f, x0);
    const stem = `Let g(x) = ∫<sub>${a}</sub><sup>x</sup> (${polyToHTML(f, 't')}) dt. Find g&prime;(${x0}).`;
    const steps = [
      `By the Fundamental Theorem of Calculus (Part 1), g&prime;(x) = f(x), where f(t) = ${polyToHTML(f, 't')}.`,
      `g&prime;(${x0}) = f(${x0}) = ${val.toString()}.`,
    ];
    return { unit: 6, topic: '6.2', topicName: 'Accumulation Functions (FTC Part 1)', difficulty, stem, answerHTML: val.toString(), solution: steps, wrongHTML: makeNumericDistractors(val) };
  }
  const k = difficulty === 2 ? choice([2, 3]) : choice([2, 3, -2]);
  const hx0 = k * x0;
  const fAtH = polyEval(f, hx0);
  const answer = fAtH.mul(F(k));
  const upper = `${k === 1 ? '' : k}x`;
  const stem = `Let g(x) = ∫<sub>${a}</sub><sup>${upper}</sup> (${polyToHTML(f, 't')}) dt. Find g&prime;(${x0}).`;
  const steps = [
    `By the Fundamental Theorem of Calculus with the chain rule: g&prime;(x) = f(${upper})·${k}, where f(t) = ${polyToHTML(f, 't')}.`,
    `At x = ${x0}: ${upper.replace('x', `(${x0})`)} = ${hx0}, so f(${hx0}) = ${fAtH.toString()}.`,
    `g&prime;(${x0}) = ${fAtH.toString()} × ${k} = ${answer.toString()}.`,
  ];
  return { unit: 6, topic: '6.2', topicName: 'Accumulation Functions (FTC Part 1)', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

function genUSub(difficulty) {
  const k = randNonZero(-4, 4);
  const m = randInt(-5, 5);
  const n = difficulty === 1 ? randInt(2, 3) : difficulty === 2 ? randInt(3, 5) : randInt(2, 6);
  const a = randNonZero(-3, 3);
  const innerHTML = polyToHTML(linear(k, m));
  const coef = F(a).div(F(k * (n + 1)));
  const coefPrefix = coef.equals(F(1)) ? '' : coef.equals(F(-1)) ? '−' : coef.toString();
  const answerHTML = `${coefPrefix}(${innerHTML})<sup>${n + 1}</sup> + C`;
  const stem = `Find the indefinite integral:<br><span class="mathblock">∫ ${a === 1 ? '' : a}(${innerHTML})<sup>${n}</sup> dx</span>`;
  const steps = [
    `Let u = ${innerHTML}, so du = ${k} dx, i.e. dx = du/${k}.`,
    `The integral becomes ∫ ${a} u<sup>${n}</sup> (du/${k}) = (${a}/${k}) ∫ u<sup>${n}</sup> du = (${a}/${k}) · u<sup>${n + 1}</sup>/${n + 1} + C.`,
    `Substitute back u = ${innerHTML}: ${answerHTML}`,
  ];
  const wrong1 = `${F(a, k).toString()}(${innerHTML})<sup>${n + 1}</sup> + C`; // forgot to divide by (n+1)
  const wrong2 = `${coefPrefix}(${innerHTML})<sup>${n}</sup> + C`; // forgot to raise the exponent
  const wrong3 = `${F(a, n + 1).toString()}(${innerHTML})<sup>${n + 1}</sup> + C`; // forgot to divide by k
  const seen = new Set([answerHTML]);
  const wrongHTML = [];
  for (const w of [wrong1, wrong2, wrong3]) { if (!seen.has(w)) { seen.add(w); wrongHTML.push(w); } }
  while (wrongHTML.length < 3) wrongHTML.push(`${coef.add(F(1)).toString()}(${innerHTML})<sup>${n + 1}</sup> + C`);
  return { unit: 6, topic: '6.3', topicName: 'Antiderivatives by u-Substitution', difficulty, stem, answerHTML, solution: steps, wrongHTML: wrongHTML.slice(0, 3) };
}

/* ---------------------------------------------------------------------- *
 * Unit 7 — Differential Equations
 * ---------------------------------------------------------------------- */

function genSeparableDE(difficulty) {
  const pool = difficulty === 1 ? PYTHAGOREAN_TRIPLES.filter((t) => t[2] <= 13)
    : difficulty === 2 ? PYTHAGOREAN_TRIPLES.filter((t) => t[2] <= 25)
    : PYTHAGOREAN_TRIPLES;
  const [m, x1, y1] = choice(pool.length ? pool : PYTHAGOREAN_TRIPLES);
  const stem = `Solve the differential equation dy/dx = x/y with initial condition y(0) = ${m}, y &gt; 0. Find y(${x1}).`;
  const steps = [
    `Separate variables: y dy = x dx.`,
    `Integrate both sides: y<sup>2</sup>/2 = x<sup>2</sup>/2 + C.`,
    `Apply the initial condition y(0) = ${m}: ${m}<sup>2</sup>/2 = 0 + C, so C = ${(m * m) / 2}.`,
    `General solution: y<sup>2</sup> = x<sup>2</sup> + ${m * m}, so y = √(x<sup>2</sup> + ${m * m}) (positive root, since y &gt; 0).`,
    `y(${x1}) = √(${x1}<sup>2</sup> + ${m * m}) = √${x1 * x1 + m * m} = ${y1}.`,
  ];
  const answer = F(y1);
  return { unit: 7, topic: '7.1', topicName: 'Separable Differential Equations', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

function genGrowthDecay(difficulty) {
  const P0 = randInt(50, 400);
  const grow = Math.random() < 0.5;
  const span = difficulty === 1 ? 2 : difficulty === 2 ? 4 : 6;
  const ratio = grow ? 1 + randInt(1, span) / 10 : 1 - randInt(1, span) / 10;
  const t1 = randInt(2, 6);
  const t2 = t1 + randInt(1, 5);
  const k = Math.log(ratio) / t1;
  const P1 = Math.round(P0 * ratio);
  const answer = P0 * Math.exp(k * t2);
  const stem = `A population grows or decays at a rate proportional to its size. At time t = 0 the population is ${P0}. At time t = ${t1}, the population is ${P1}. Assuming exponential growth/decay, find the population at time t = ${t2}. Round to the nearest whole number.`;
  const steps = [
    `The model is P(t) = P<sub>0</sub>e<sup>kt</sup> with P<sub>0</sub> = ${P0}.`,
    `Use P(${t1}) = ${P1}: ${P0}e<sup>${t1}k</sup> = ${P1}, so k = ln(${P1}/${P0}) / ${t1} ≈ ${k.toFixed(5)}.`,
    `P(${t2}) = ${P0}e<sup>${(k * t2).toFixed(5)}</sup> ≈ ${answer.toFixed(0)}.`,
  ];
  return { unit: 7, topic: '7.2', topicName: 'Exponential Growth and Decay', difficulty, stem, answerHTML: `${answer.toFixed(0)}`, solution: steps, wrongHTML: makeDecimalDistractors(answer, 0) };
}

/* ---------------------------------------------------------------------- *
 * Unit 8 — Applications of Integration
 * ---------------------------------------------------------------------- */

function genAverageValue(difficulty) {
  const maxDeg = difficulty === 1 ? 2 : difficulty === 2 ? 3 : 4;
  const p = randPoly(1, maxDeg, -6, 6);
  const a = randInt(-3, 1);
  const b = randInt(a + 1, a + 5);
  const P = polyAntideriv(p);
  const integral = polyEval(P, b).sub(polyEval(P, a));
  const answer = integral.div(F(b - a));
  const stem = `Find the average value of f(x) = ${polyToHTML(p)} on the interval [${a}, ${b}].`;
  const steps = [
    `Average value formula: f<sub>avg</sub> = (1/(b−a)) ∫<sub>a</sub><sup>b</sup> f(x) dx.`,
    `∫<sub>${a}</sub><sup>${b}</sup> (${polyToHTML(p)}) dx = ${integral.toString()} (using F(x) = ${polyToHTML(P)}).`,
    `f<sub>avg</sub> = ${integral.toString()} / (${b} − (${a})) = ${answer.toString()}.`,
  ];
  return { unit: 8, topic: '8.1', topicName: 'Average Value of a Function', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

function genAreaBetween(difficulty) {
  const maxDeg = difficulty === 3 ? 2 : 1;
  let f, g, a, b, diff, ok = false, tries = 0;
  while (!ok && tries < 200) {
    tries++;
    f = polyAdd(randPoly(1, maxDeg, -5, 5), [F(randInt(4, 10))]); // biased upward
    g = randPoly(0, 1, -5, 5);
    a = randInt(-2, 0); b = randInt(a + 2, a + 4);
    diff = polySub(f, g);
    ok = true;
    for (let i = 0; i <= 40; i++) {
      const x = a + ((b - a) * i) / 40;
      if (polyEvalFloat(diff, x) <= 0) { ok = false; break; }
    }
  }
  if (!ok) { // guaranteed-safe fallback
    g = randPoly(0, 1, -5, 5);
    const c = randInt(3, 9);
    f = polyAdd(g, [F(c)]);
    a = randInt(-2, 0); b = randInt(a + 2, a + 4);
    diff = [F(c)];
  }
  const D = polyAntideriv(diff);
  const Db = polyEval(D, b), Da = polyEval(D, a);
  const area = Db.sub(Da);
  const stem = `Let R be the region bounded by f(x) = ${polyToHTML(f)} and g(x) = ${polyToHTML(g)} between x = ${a} and x = ${b}. Find the area of R.`;
  const steps = [
    `On [${a}, ${b}], f(x) ≥ g(x), so Area = ∫<sub>${a}</sub><sup>${b}</sup> [f(x) − g(x)] dx.`,
    `f(x) − g(x) = ${polyToHTML(diff)}.`,
    `Antiderivative: ${polyToHTML(D)}.`,
    `Area = ${Db.toString()} − (${Da.toString()}) = ${area.toString()}.`,
  ];
  return { unit: 8, topic: '8.2', topicName: 'Area Between Two Curves', difficulty, stem, answerHTML: area.toString(), solution: steps, wrongHTML: makeNumericDistractors(area) };
}

function genVolume(difficulty) {
  const maxDeg = difficulty === 1 ? 1 : 2;
  const f = randPoly(1, maxDeg, -4, 4);
  const a = randInt(0, 2);
  const b = randInt(a + 1, a + 3);
  const sq = polyMul(f, f);
  const S = polyAntideriv(sq);
  const coeff = polyEval(S, b).sub(polyEval(S, a));
  const stem = `The region bounded by y = ${polyToHTML(f)}, the x-axis, x = ${a}, and x = ${b} is revolved about the x-axis. Find the volume of the resulting solid.`;
  const steps = [
    `Disk method: V = π∫<sub>${a}</sub><sup>${b}</sup> [f(x)]<sup>2</sup> dx, where [f(x)]<sup>2</sup> = ${polyToHTML(sq)}.`,
    `Antiderivative: ${polyToHTML(S)}.`,
    `V = π[${polyEval(S, b).toString()} − (${polyEval(S, a).toString()})] = ${coeff.toString()}π.`,
  ];
  return { unit: 8, topic: '8.3', topicName: 'Volumes of Revolution (Disk/Washer)', difficulty, stem, answerHTML: fracPiHTML(coeff), solution: steps, wrongHTML: piDistractorsHTML(coeff) };
}

/* ---------------------------------------------------------------------- *
 * Unit 9 (BC) — Parametric, Polar & Vector-Valued Functions
 * ---------------------------------------------------------------------- */

function genParametricDeriv(difficulty) {
  const maxDeg = difficulty === 1 ? 1 : 2;
  let x, y, t0, xP, xPAt;
  do {
    x = randPoly(1, maxDeg, -5, 5);
    y = randPoly(1, maxDeg, -5, 5);
    t0 = randInt(-2, 2);
    xP = polyDeriv(x);
    xPAt = polyEval(xP, t0);
  } while (xPAt.isZero());
  const yP = polyDeriv(y);
  const yPAt = polyEval(yP, t0);
  const answer = yPAt.div(xPAt);
  const stem = `A curve is defined parametrically by x(t) = ${polyToHTML(x, 't')} and y(t) = ${polyToHTML(y, 't')}. Find dy/dx at t = ${t0}.`;
  const steps = [
    `dy/dx = [dy/dt] / [dx/dt] = y&prime;(t) / x&prime;(t).`,
    `x&prime;(t) = ${polyToHTML(xP, 't')}, so x&prime;(${t0}) = ${xPAt.toString()}.`,
    `y&prime;(t) = ${polyToHTML(yP, 't')}, so y&prime;(${t0}) = ${yPAt.toString()}.`,
    `dy/dx = ${yPAt.toString()} / ${xPAt.toString()} = ${answer.toString()}.`,
  ];
  return { unit: 9, topic: '9.1', topicName: 'Derivatives of Parametric Equations', difficulty, stem, answerHTML: answer.toString(), solution: steps, wrongHTML: makeNumericDistractors(answer) };
}

function piDistractorsHTML(coeff) {
  const candidates = [coeff.neg(), coeff.add(F(1)), coeff.sub(F(1)), coeff.mul(F(2)), coeff.div(F(2))];
  const seen = new Set([coeff.toString()]);
  const out = [];
  for (const c of candidates) { if (!seen.has(c.toString())) { seen.add(c.toString()); out.push(fracPiHTML(c)); } if (out.length === 3) break; }
  return out;
}

function genPolarArea(difficulty) {
  const kind = difficulty === 1 ? 'circle' : choice(['circle', 'rose']);
  const k = randInt(2, 6);
  if (kind === 'circle') {
    const half = difficulty >= 2 && Math.random() < 0.5;
    const answerCoeff = half ? F(k * k, 2) : F(k * k);
    const stem = `Find the area enclosed by the polar curve r = ${k} for θ from ${half ? '0 to π' : '0 to 2π'}.`;
    const steps = [
      `Polar area formula: A = (1/2)∫ r<sup>2</sup> dθ.`,
      `A = (1/2)∫<sub>0</sub><sup>${half ? 'π' : '2π'}</sup> ${k * k} dθ = (1/2)(${k * k})(${half ? 'π' : '2π'}) = ${answerCoeff.toString()}π.`,
    ];
    return { unit: 9, topic: '9.2', topicName: 'Area of a Polar Region', difficulty, stem, answerHTML: fracPiHTML(answerCoeff), solution: steps, wrongHTML: piDistractorsHTML(answerCoeff) };
  }
  const n = choice([2, 3]);
  const areaCoeff = F(k * k, 4 * n);
  const stem = `Find the area of one petal of the polar rose r = ${k} sin(${n}θ).`;
  const steps = [
    `For a rose r = k sin(nθ), the area of one petal is A = πk<sup>2</sup>/(4n).`,
    `A = π(${k})<sup>2</sup> / (4·${n}) = ${areaCoeff.toString()}π.`,
  ];
  return { unit: 9, topic: '9.2', topicName: 'Area of a Polar Region', difficulty, stem, answerHTML: fracPiHTML(areaCoeff), solution: steps, wrongHTML: piDistractorsHTML(areaCoeff) };
}

/* ---------------------------------------------------------------------- *
 * Unit 10 (BC) — Infinite Sequences and Series
 * ---------------------------------------------------------------------- */

function genGeometricSeries(difficulty) {
  const a = randNonZero(-9, 9);
  const denomChoices = difficulty === 1 ? [2, 3, 4] : difficulty === 2 ? [2, 3, 4, 5] : [2, 3, 4, 5, 6];
  const rd = choice(denomChoices);
  const rn = randNonZero(1, rd - 1) * choice([1, -1]);
  const r = F(rn, rd);
  const sum = F(a).div(F(1).sub(r));
  const stem = `Find the sum of the geometric series: ${a} + ${a}(${r.toString()}) + ${a}(${r.toString()})<sup>2</sup> + ⋯`;
  const steps = [
    `This is a geometric series with first term a = ${a} and common ratio r = ${r.toString()}.`,
    `Since |r| = |${r.toString()}| &lt; 1, the series converges.`,
    `Sum = a/(1 − r) = ${a} / (1 − (${r.toString()})) = ${sum.toString()}.`,
  ];
  return { unit: 10, topic: '10.1', topicName: 'Geometric Series', difficulty, stem, answerHTML: sum.toString(), solution: steps, wrongHTML: makeNumericDistractors(sum) };
}

function factorial(k) { let r = 1; for (let i = 2; i <= k; i++) r *= i; return r; }

function genMaclaurin(difficulty) {
  const kind = choice(['exp', 'sin', 'cos', 'geom']);
  const n = difficulty === 1 ? 3 : difficulty === 2 ? 4 : 5;
  const terms = [];
  if (kind === 'exp') {
    for (let i = 0; i <= n; i++) terms.push({ power: i, coef: F(1, factorial(i)) });
  } else if (kind === 'geom') {
    for (let i = 0; i <= n; i++) terms.push({ power: i, coef: F(1) });
  } else if (kind === 'sin') {
    for (let i = 1; i <= n; i += 2) { const k = (i - 1) / 2; terms.push({ power: i, coef: F(k % 2 === 0 ? 1 : -1, factorial(i)) }); }
  } else {
    for (let i = 0; i <= n; i += 2) { const k = i / 2; terms.push({ power: i, coef: F(k % 2 === 0 ? 1 : -1, factorial(i)) }); }
  }
  const label = { exp: 'e<sup>x</sup>', sin: 'sin x', cos: 'cos x', geom: '1/(1−x)' }[kind];
  const html = terms.map((t) => {
    const c = t.coef, cAbs = c.abs();
    const coefStr = cAbs.equals(F(1)) && t.power !== 0 ? '' : cAbs.toString();
    const varStr = t.power === 0 ? '' : t.power === 1 ? 'x' : `x<sup>${t.power}</sup>`;
    return { neg: c.isNeg(), text: coefStr + varStr };
  });
  const joinHtml = (parts) => {
    let s = (parts[0].neg ? '−' : '') + parts[0].text;
    for (let i = 1; i < parts.length; i++) s += parts[i].neg ? ` − ${parts[i].text}` : ` + ${parts[i].text}`;
    return s;
  };
  const poly = joinHtml(html);
  const stem = `Find the degree-${n} Maclaurin polynomial for f(x) = ${label}.`;
  const steps = [
    `Maclaurin series: f(x) ≈ Σ [f<sup>(k)</sup>(0)/k!] x<sup>k</sup>.`,
    `P<sub>${n}</sub>(x) = ${poly}.`,
  ];

  const droppedParts = html.slice(0, -1);
  const wrongDrop = droppedParts.length ? joinHtml(droppedParts) : '0';
  const flippedParts = html.map((t) => ({ ...t, neg: !t.neg }));
  const wrongFlip = joinHtml(flippedParts);
  const wrongExtra = `${poly} + C`;
  const seen = new Set([poly]);
  const wrongHTML = [];
  for (const w of [wrongDrop, wrongFlip, wrongExtra]) { if (!seen.has(w)) { seen.add(w); wrongHTML.push(w); } }
  while (wrongHTML.length < 3) wrongHTML.push(`${poly} (all terms doubled)`);
  return { unit: 10, topic: '10.2', topicName: 'Maclaurin Polynomials', difficulty, stem, answerHTML: poly, solution: steps, wrongHTML: wrongHTML.slice(0, 3) };
}

function genRadiusConvergence(difficulty) {
  const c = randInt(-4, 4);
  const b = difficulty === 1 ? randInt(2, 4) : difficulty === 2 ? randInt(2, 6) : randInt(2, 9);
  const includeN = difficulty >= 2 && Math.random() < 0.5;
  const stemSeries = includeN
    ? `Σ<sub>n=1</sub><sup>∞</sup> [ n(x − ${c})<sup>n</sup> / ${b}<sup>n</sup> ]`
    : `Σ<sub>n=1</sub><sup>∞</sup> [ (x − ${c})<sup>n</sup> / ${b}<sup>n</sup> ]`;
  const stem = `Find the radius of convergence of the power series:<br><span class="mathblock">${stemSeries}</span>`;
  const steps = [
    `Apply the Ratio Test: compute L = lim<sub>n→∞</sub> |a<sub>n+1</sub>/a<sub>n</sub>|·|x − ${c}|.`,
    includeN
      ? `|a<sub>n+1</sub>/a<sub>n</sub>| = [(n+1)/n]·(1/${b}) → 1/${b} as n→∞.`
      : `|a<sub>n+1</sub>/a<sub>n</sub>| = 1/${b}.`,
    `So L = |x − ${c}|/${b}. The series converges when L &lt; 1, i.e. |x − ${c}| &lt; ${b}.`,
    `Radius of convergence: R = ${b}.`,
  ];
  const answer = F(b);
  return { unit: 10, topic: '10.3', topicName: 'Radius of Convergence (Ratio Test)', difficulty, stem, answerHTML: `R = ${answer.toString()}`, solution: steps, wrongHTML: makeNumericDistractors(answer).map((w) => `R = ${w}`) };
}

/* ---------------------------------------------------------------------- *
 * Registry
 * ---------------------------------------------------------------------- */

const GENERATORS = [
  { topic: '1.1', fn: genLimitFactor },
  { topic: '1.2', fn: genLimitInfinity },
  { topic: '1.3', fn: genContinuityK },
  { topic: '2.1', fn: genPowerRule },
  { topic: '2.2', fn: genBasicRulesSum },
  { topic: '2.3', fn: genProductRule },
  { topic: '2.4', fn: genQuotientRule },
  { topic: '3.1', fn: genChainNumeric },
  { topic: '3.2', fn: genChainSymbolic },
  { topic: '3.3', fn: genImplicit },
  { topic: '3.4', fn: genInverseDeriv },
  { topic: '4.1', fn: genMotion },
  { topic: '4.2', fn: genRelatedRates },
  { topic: '4.3', fn: genLinearApprox },
  { topic: '4.4', fn: genLHopital },
  { topic: '5.1', fn: genFirstDerivTest },
  { topic: '5.2', fn: genConcavity },
  { topic: '5.3', fn: genOptimization },
  { topic: '6.1', fn: genDefiniteIntegral },
  { topic: '6.2', fn: genFTCAccum },
  { topic: '6.3', fn: genUSub },
  { topic: '7.1', fn: genSeparableDE },
  { topic: '7.2', fn: genGrowthDecay },
  { topic: '8.1', fn: genAverageValue },
  { topic: '8.2', fn: genAreaBetween },
  { topic: '8.3', fn: genVolume },
  { topic: '9.1', fn: genParametricDeriv },
  { topic: '9.2', fn: genPolarArea },
  { topic: '10.1', fn: genGeometricSeries },
  { topic: '10.2', fn: genMaclaurin },
  { topic: '10.3', fn: genRadiusConvergence },
];

function generateProblem(topicCode, difficulty) {
  // Topics may have more than one generator registered (e.g. a hand-written
  // template plus a compositional-engine variant from compositional.js,
  // which pushes extra entries onto GENERATORS after this file loads) —
  // pick uniformly at random among whichever are registered for this topic.
  const entries = GENERATORS.filter((g) => g.topic === topicCode);
  if (!entries.length) return null;
  return choice(entries).fn(difficulty);
}

if (typeof module !== 'undefined') {
  module.exports = { GENERATORS, generateProblem };
}
