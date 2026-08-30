/*
 * compositional.js — generator variants built on the expr.js symbolic
 * engine instead of one hand-picked function shape per topic. These are
 * ADDED to the existing GENERATORS registry (generators.js) as extra
 * entries for topics 2.2, 2.3, 2.4, 3.2, 6.1, 6.3, and 8.1 — the original
 * hand-written generators for those topics stay registered too, so
 * generateProblem() now picks at random among all variants for a topic.
 *
 * Every derivative here is produced by expr.js's diff(), which is exact
 * by construction and verified against finite differences across
 * thousands of random trees (see the property-based test used during
 * development). Integration problems use the same "build the
 * antiderivative, then differentiate it" trick as the original
 * u-substitution generator, generalized to more outer-function shapes —
 * no general symbolic integration is attempted anywhere.
 */

/** Reconstruct an exact Frac from an evalSmart() result string ("n" or
 * "n/d") — needed because evalResult.value is a lossy float and Frac.of()
 * would round it (e.g. 0.5 -> 1), silently corrupting the fraction. */
function parseFracStr(str) {
  if (str.includes('/')) { const [n, d] = str.split('/').map(Number); return F(n, d); }
  return F(Number(str));
}

/* ---- Shared distractor builders ---- */

function buildSymbolicDerivativeDistractors(f, correctNode) {
  const correctHTML = toHTML(correctNode);
  const candidates = [
    diffBuggy(f, { noChain: true }),
    diffBuggy(f, { cosSign: true }),
    flipRandomTermSign(correctNode),
  ];
  const seen = new Set([correctHTML]);
  const out = [];
  for (const c of candidates) {
    const html = toHTML(c);
    if (!seen.has(html)) { seen.add(html); out.push(html); }
  }
  let guard = 0;
  while (out.length < 3 && guard < 20) {
    guard++;
    const jittered = scaleLeadingCoef(correctNode, F(choice([2, -1, 3, -2])));
    const html = toHTML(jittered);
    if (!seen.has(html)) { seen.add(html); out.push(html); }
  }
  return out.slice(0, 3);
}

function buildAntiderivativeDistractors(F_, correctHTML) {
  const candidates = [
    scaleLeadingCoef(F_, F(-1)),
    scaleLeadingCoef(F_, F(2)),
    scaleLeadingCoef(F_, F(1, 2)),
  ];
  const seen = new Set([correctHTML]);
  const out = [];
  for (const c of candidates) {
    const html = `${toHTML(c)} + C`;
    if (!seen.has(html)) { seen.add(html); out.push(html); }
  }
  let guard = 0;
  while (out.length < 3 && guard < 20) {
    guard++;
    const factor = F(choice([3, -2, 4, -3]), choice([1, 2]));
    const html = `${toHTML(scaleLeadingCoef(F_, factor))} + C`;
    if (!seen.has(html)) { seen.add(html); out.push(html); }
  }
  return out.slice(0, 3);
}

/* ---- 2.2 — Derivatives of Trig, Exponential & Log Sums (composed variant) ---- */

function genComposedDerivativeSum(difficulty) {
  const f = randomExpr(difficulty);
  const fp = simplify(diff(f));
  const correctHTML = toHTML(fp);
  const stem = `Let f(x) = ${toHTML(f)}. Find f&prime;(x).`;
  const steps = [
    `Differentiate term by term, applying the chain rule to any composite terms (an inner linear function contributes a constant multiplier).`,
    `f&prime;(x) = ${correctHTML}.`,
  ];
  return { unit: 2, topic: '2.2', topicName: 'Derivatives of Trig, Exponential & Log Sums', difficulty, stem, answerHTML: correctHTML, solution: steps, wrongHTML: buildSymbolicDerivativeDistractors(f, fp) };
}

/* ---- 3.2 — The Chain Rule, Symbolic Derivative (deep composition variant) ---- */

function genDeepChainRule(difficulty) {
  const f = randomComposedSingle(difficulty);
  const fp = simplify(diff(f));
  const correctHTML = toHTML(fp);
  const stem = `Let f(x) = ${toHTML(f)}. Find f&prime;(x).`;
  const steps = [
    `Apply the chain rule at each layer of composition, working from the outside in and multiplying by the derivative of each inner function.`,
    `f&prime;(x) = ${correctHTML}.`,
  ];
  return { unit: 3, topic: '3.2', topicName: 'The Chain Rule (Symbolic Derivative)', difficulty, stem, answerHTML: correctHTML, solution: steps, wrongHTML: buildSymbolicDerivativeDistractors(f, fp) };
}

/* ---- 2.3 / 2.4 — Product & Quotient Rule with mixed factor types ---- */

const SIMPLE_FACTOR_KINDS = ['poly', 'sin', 'cos', 'exp', 'pow'];

function genProductRuleMixed(difficulty) {
  const range = difficulty === 1 ? 4 : difficulty === 2 ? 6 : 8;
  const u = randomAtomicTerm(difficulty, { kinds: SIMPLE_FACTOR_KINDS, coeffRange: range });
  const v = randomAtomicTerm(difficulty, { kinds: SIMPLE_FACTOR_KINDS, coeffRange: range });
  const f = mulN(u, v);
  const fp = simplify(diff(f));
  const x0 = randInt(-2, 2);
  const evalResult = evalSmart(fp, x0);
  const stem = `Let f(x) = (${toHTML(u)})(${toHTML(v)}). Use the product rule to find f&prime;(${x0})${evalResult.exact ? '' : ' (round to three decimal places)'}.`;
  const steps = [
    `Product rule: f&prime;(x) = u&prime;(x)v(x) + u(x)v&prime;(x), where u(x) = ${toHTML(u)} and v(x) = ${toHTML(v)}.`,
    `f&prime;(x) = ${toHTML(fp)}.`,
    `f&prime;(${x0}) ${evalResult.exact ? '=' : '≈'} ${evalResult.str}.`,
  ];
  const wrongHTML = evalResult.exact ? makeNumericDistractors(parseFracStr(evalResult.str)) : makeDecimalDistractors(evalResult.value, 3);
  return { unit: 2, topic: '2.3', topicName: 'The Product Rule', difficulty, stem, answerHTML: evalResult.str, solution: steps, wrongHTML };
}

function genQuotientRuleMixed(difficulty) {
  const range = difficulty === 1 ? 4 : difficulty === 2 ? 6 : 8;
  let u, v, x0, denAt;
  do {
    u = randomAtomicTerm(difficulty, { kinds: SIMPLE_FACTOR_KINDS, coeffRange: range });
    v = randomAtomicTerm(difficulty, { kinds: SIMPLE_FACTOR_KINDS, coeffRange: range });
    x0 = randInt(-2, 2);
    denAt = evalNum(v, x0);
  } while (!Number.isFinite(denAt) || Math.abs(denAt) < 0.2);
  const f = divN(u, v);
  const fp = simplify(diff(f));
  const evalResult = evalSmart(fp, x0);
  const stem = `Let f(x) = (${toHTML(u)}) / (${toHTML(v)}). Use the quotient rule to find f&prime;(${x0})${evalResult.exact ? '' : ' (round to three decimal places)'}.`;
  const steps = [
    `Quotient rule: f&prime;(x) = [u&prime;(x)v(x) − u(x)v&prime;(x)] / [v(x)]<sup>2</sup>, where u(x) = ${toHTML(u)} and v(x) = ${toHTML(v)}.`,
    `f&prime;(x) = ${toHTML(fp)}.`,
    `f&prime;(${x0}) ${evalResult.exact ? '=' : '≈'} ${evalResult.str}.`,
  ];
  const wrongHTML = evalResult.exact ? makeNumericDistractors(parseFracStr(evalResult.str)) : makeDecimalDistractors(evalResult.value, 3);
  return { unit: 2, topic: '2.4', topicName: 'The Quotient Rule', difficulty, stem, answerHTML: evalResult.str, solution: steps, wrongHTML };
}

/* ---- 6.3 — Antiderivatives by u-Substitution (generalized outer function) ---- */

function genUSubGeneral(difficulty) {
  const { F: F_, f } = randomAntiderivative(difficulty);
  const correctHTML = `${toHTML(F_)} + C`;
  const stem = `Find the indefinite integral:<br><span class="mathblock">∫ ${toHTML(f)} dx</span>`;
  const steps = [
    `Recognize this as a chain-rule derivative in reverse: the integrand is of the form g&prime;(x)·h&prime;(g(x)) for some inner function g.`,
    `An antiderivative is F(x) = ${toHTML(F_)}, since differentiating F confirms F&prime;(x) = ${toHTML(f)}.`,
    `∫ ${toHTML(f)} dx = ${correctHTML}.`,
  ];
  return { unit: 6, topic: '6.3', topicName: 'Antiderivatives by u-Substitution', difficulty, stem, answerHTML: correctHTML, solution: steps, wrongHTML: buildAntiderivativeDistractors(F_, correctHTML) };
}

/* ---- 6.1 — Definite Integrals via antiderivative-first construction ---- */

function genDefiniteIntegralGeneral(difficulty) {
  const { F: F_, f } = randomAntiderivative(difficulty);
  const a = randInt(0, 2);
  const b = randInt(a + 1, a + 3);
  const Fb = evalSmart(F_, b), Fa = evalSmart(F_, a);
  const exact = Fb.exact && Fa.exact;
  const value = Fb.value - Fa.value;
  const resultStr = exact ? fracFromEvalResults(Fb, Fa).toString() : value.toFixed(3);
  const stem = `Evaluate the definite integral:<br><span class="mathblock">∫<sub>${a}</sub><sup>${b}</sup> (${toHTML(f)}) dx</span>`;
  const steps = [
    `Find an antiderivative: F(x) = ${toHTML(F_)} (check: F&prime;(x) = ${toHTML(f)}).`,
    `By the Fundamental Theorem of Calculus: F(${b}) − F(${a}) = ${Fb.str} − (${Fa.str}) ${exact ? '=' : '≈'} ${resultStr}.`,
  ];
  const wrongHTML = exact ? makeNumericDistractors(fracFromEvalResults(Fb, Fa)) : makeDecimalDistractors(value, 3);
  return { unit: 6, topic: '6.1', topicName: 'Definite Integrals (FTC)', difficulty, stem, answerHTML: resultStr, solution: steps, wrongHTML };
}

/* ---- 8.1 — Average Value via antiderivative-first construction ---- */

function genAverageValueGeneral(difficulty) {
  const { F: F_, f } = randomAntiderivative(difficulty);
  const a = randInt(0, 2);
  const b = randInt(a + 1, a + 3);
  const Fb = evalSmart(F_, b), Fa = evalSmart(F_, a);
  const exact = Fb.exact && Fa.exact;
  const integral = exact ? fracFromEvalResults(Fb, Fa) : null;
  const value = exact ? integral.toFloat() / (b - a) : (Fb.value - Fa.value) / (b - a);
  const resultStr = exact ? integral.div(F(b - a)).toString() : value.toFixed(3);
  const stem = `Find the average value of f(x) = ${toHTML(f)} on the interval [${a}, ${b}].`;
  const steps = [
    `Average value formula: f<sub>avg</sub> = (1/(b−a)) ∫<sub>a</sub><sup>b</sup> f(x) dx.`,
    `An antiderivative is F(x) = ${toHTML(F_)}, so ∫<sub>${a}</sub><sup>${b}</sup> f(x) dx = F(${b}) − F(${a}) = ${Fb.str} − (${Fa.str}).`,
    `f<sub>avg</sub> ${exact ? '=' : '≈'} ${resultStr}.`,
  ];
  const wrongHTML = exact ? makeNumericDistractors(integral.div(F(b - a))) : makeDecimalDistractors(value, 3);
  return { unit: 8, topic: '8.1', topicName: 'Average Value of a Function', difficulty, stem, answerHTML: resultStr, solution: steps, wrongHTML };
}

function fracFromEvalResults(rb, ra) { return parseFracStr(rb.str).sub(parseFracStr(ra.str)); }

/* ---- Register alongside the existing hand-written generators ---- */

GENERATORS.push(
  { topic: '2.2', fn: genComposedDerivativeSum },
  { topic: '3.2', fn: genDeepChainRule },
  { topic: '2.3', fn: genProductRuleMixed },
  { topic: '2.4', fn: genQuotientRuleMixed },
  { topic: '6.3', fn: genUSubGeneral },
  { topic: '6.1', fn: genDefiniteIntegralGeneral },
  { topic: '8.1', fn: genAverageValueGeneral },
);

if (typeof module !== 'undefined') {
  module.exports = {
    genComposedDerivativeSum, genDeepChainRule, genProductRuleMixed, genQuotientRuleMixed,
    genUSubGeneral, genDefiniteIntegralGeneral, genAverageValueGeneral,
  };
}
