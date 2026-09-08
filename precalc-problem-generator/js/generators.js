/**
 * Problem generators for the Brooklyn Tech Precalculus problem set
 * generator, aligned to the department's 11-unit curriculum map.
 *
 * Every generator has the signature (difficulty, type) -> problem, where
 * difficulty is 1 (Easy), 2 (Medium), or 3 (Hard), and type is 'mc' or
 * 'fr'. A problem object looks like:
 *   {
 *     type: 'mc' | 'fr',
 *     prompt: string,
 *     choices: string[]        // mc only
 *     correctIndex: number     // mc only
 *     answer: string,
 *     solution: string[]
 *   }
 *
 * Plain-ASCII math notation is used throughout (x^2, sqrt(x), pi, theta,
 * deg) instead of Unicode symbols that are not renderable in the client
 * side PDF font, so the same text is safe on screen and in the PDF. The
 * exceptions are the handful of Latin-1 symbols (deg, +/- as ±,
 * middle dot, times, division sign) that the PDF's standard font does
 * support.
 */

/* ----------------------------- utilities ------------------------------ */

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
function randNonZero(min, max) {
  let n;
  do {
    n = randInt(min, max);
  } while (n === 0);
  return n;
}
function choice(arr) {
  return arr[randInt(0, arr.length - 1)];
}
function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = randInt(0, i);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function gcd(a, b) {
  a = Math.abs(a);
  b = Math.abs(b);
  while (b) {
    [a, b] = [b, a % b];
  }
  return a || 1;
}
function fracStr(num, den) {
  if (den < 0) {
    num = -num;
    den = -den;
  }
  const g = gcd(num, den) || 1;
  num /= g;
  den /= g;
  if (den === 1) return `${num}`;
  return `${num}/${den}`;
}
function round2(n) {
  return Math.round(n * 100) / 100;
}
function round4(n) {
  return Math.round(n * 10000) / 10000;
}
function fmtNum(n) {
  if (Number.isInteger(n)) return `${n}`;
  return round2(n).toString();
}
function fmt4(n) {
  if (Number.isInteger(n)) return `${n}`;
  return round4(n).toString();
}

function polyStr(coeffs) {
  const deg = coeffs.length - 1;
  const terms = [];
  coeffs.forEach((c, i) => {
    if (c === 0) return;
    const power = deg - i;
    const absC = Math.abs(c);
    let term;
    if (power === 0) term = `${absC}`;
    else if (power === 1) term = (absC === 1 ? "" : `${absC}`) + "x";
    else term = (absC === 1 ? "" : `${absC}`) + `x^${power}`;
    terms.push({ c, term });
  });
  if (terms.length === 0) return "0";
  let s = (terms[0].c < 0 ? "-" : "") + terms[0].term;
  for (let i = 1; i < terms.length; i++) {
    s += terms[i].c < 0 ? ` - ${terms[i].term}` : ` + ${terms[i].term}`;
  }
  return s;
}
function linearFactorStr(root) {
  if (root === 0) return "x";
  return root > 0 ? `(x - ${root})` : `(x + ${Math.abs(root)})`;
}
/** "x - h" or "x + |h|", sign-aware (h may be 0 or negative). */
function xMinus(h) {
  return h >= 0 ? `x - ${h}` : `x + ${Math.abs(h)}`;
}
function yMinus(k) {
  return k >= 0 ? `y - ${k}` : `y + ${Math.abs(k)}`;
}
function expandTwoFactors(r1, r2) {
  // (x - r1)(x - r2) = x^2 - (r1+r2)x + r1*r2
  return [1, -(r1 + r2), r1 * r2];
}
function expandThreeFactors(r1, r2, r3) {
  const [b2, c2] = [-(r1 + r2), r1 * r2];
  const b3 = b2 - r3;
  const c3 = c2 - r3 * b2;
  const d3 = -r3 * c2;
  return [1, b3, c3, d3];
}
function factorial(n) {
  let r = 1;
  for (let i = 2; i <= n; i++) r *= i;
  return r;
}
function nPr(n, r) {
  let result = 1;
  for (let i = 0; i < r; i++) result *= n - i;
  return result;
}
function nCr(n, r) {
  return Math.round(nPr(n, r) / factorial(r));
}
function factorsOf(n) {
  n = Math.abs(n);
  const result = [];
  for (let i = 1; i <= n; i++) if (n % i === 0) result.push(i);
  return result;
}
/** Synthetic division of a polynomial (descending coeffs) by (x - c). */
function syntheticDivide(coeffs, c) {
  const quotient = [coeffs[0]];
  for (let i = 1; i < coeffs.length; i++) {
    quotient.push(coeffs[i] + quotient[i - 1] * c);
  }
  const remainder = quotient.pop();
  return { quotient, remainder };
}
/** Format a complex number a + bi (integers) as a plain-ASCII string. */
function fmtComplex(re, im) {
  const r = Number.isInteger(re) ? re : round2(re);
  const i = Number.isInteger(im) ? im : round2(im);
  if (i === 0) return `${r}`;
  const sign = i < 0 ? "-" : "+";
  const absI = Math.abs(i);
  const iPart = absI === 1 ? "i" : `${absI}i`;
  if (r === 0) return i < 0 ? `-${iPart}` : `${iPart}`;
  return `${r} ${sign} ${iPart}`;
}
/** Format a complex number whose parts are exact fractions num/den (den > 0). */
function fmtComplexFrac(reNum, den, imNum, imDen) {
  const rePart = fracStr(reNum, den);
  const imAbs = fracStr(Math.abs(imNum), imDen);
  if (imAbs === "0") return rePart;
  const sign = imNum < 0 ? "-" : "+";
  const imPart = imAbs === "1" ? "i" : `${imAbs}i`;
  return `${rePart} ${sign} ${imPart}`;
}

/** Build a multiple-choice problem from a correct value + distractor values. */
function buildMC(prompt, correctVal, formatter, solution, distractorVals) {
  const seen = new Set([formatter(correctVal)]);
  const distinctDistractors = [];
  for (const d of distractorVals) {
    const s = formatter(d);
    if (!seen.has(s)) {
      seen.add(s);
      distinctDistractors.push(d);
    }
    if (distinctDistractors.length >= 3) break;
  }
  if (distinctDistractors.length === 0 && distractorVals.length > 0) {
    // All candidates collapsed to duplicates of the correct answer (rare) --
    // fall back to the first candidate rather than leave no wrong option.
    distinctDistractors.push(distractorVals[0]);
  }
  if (typeof correctVal === "number") {
    while (distinctDistractors.length < 3) {
      const filler = correctVal + randNonZero(-5, 5);
      const s = formatter(filler);
      if (!seen.has(s)) {
        seen.add(s);
        distinctDistractors.push(filler);
      }
    }
  }
  const options = shuffle([correctVal, ...distinctDistractors]);
  const choices = options.map(formatter);
  const correctIndex = options.indexOf(correctVal);
  return {
    type: "mc",
    prompt,
    choices,
    correctIndex,
    answer: formatter(correctVal),
    solution,
  };
}
function buildFR(prompt, answer, solution) {
  return { type: "fr", prompt, answer, solution };
}

/* ============================ UNIT 1: FUNCTIONS ========================= */

function domainOfComposition(difficulty, type) {
  const kind = difficulty === 1 ? "rational" : choice(["rational", "radical"]);
  const A = randInt(-6, 6);
  const B = randNonZero(-6, 6);
  const gStr = `g(x) = x ${B >= 0 ? "+" : "-"} ${Math.abs(B)}`;
  if (kind === "rational") {
    const excluded = A - B;
    const prompt = `Let f(x) = 1/(x - (${A})) and ${gStr}. Find the domain of f(g(x)).`;
    const answer = `all real numbers except x = ${excluded}`;
    const solution = [
      `f(g(x)) is undefined when g(x) = ${A}, i.e. x ${B >= 0 ? "+" : "-"} ${Math.abs(B)} = ${A}.`,
      `Solve: x = ${A} ${B >= 0 ? "-" : "+"} ${Math.abs(B)} = ${excluded}.`,
      `Domain: ${answer}`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, answer, (v) => v, solution, [
      `all real numbers except x = ${excluded + 1}`,
      `all real numbers except x = ${A + B}`,
      `all real numbers except x = ${-excluded}`,
    ]);
  } else {
    const bound = A - B;
    const prompt = `Let f(x) = sqrt(x - (${A})) and ${gStr}. Find the domain of f(g(x)).`;
    const answer = `x >= ${bound}`;
    const solution = [
      `f(g(x)) requires g(x) >= ${A}, i.e. x ${B >= 0 ? "+" : "-"} ${Math.abs(B)} >= ${A}.`,
      `Solve: x >= ${A} ${B >= 0 ? "-" : "+"} ${Math.abs(B)} = ${bound}.`,
      `Domain: ${answer}`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, answer, (v) => v, solution, [`x <= ${bound}`, `x >= ${bound + 1}`, `x >= ${-bound}`]);
  }
}

function compositionOfFunctions(difficulty, type) {
  const a1 = randNonZero(-4, 4);
  const b1 = randInt(-6, 6);
  const a2 = randNonZero(-4, 4);
  const b2 = randInt(-6, 6);
  const f = (x) => a1 * x + b1;
  const g = (x) => a2 * x + b2;
  const forward = Math.random() < 0.5;
  const x0 = randInt(-5, 5);
  const val = forward ? f(g(x0)) : g(f(x0));
  const prompt = `Let f(x) = ${a1}x ${b1 >= 0 ? "+" : "-"} ${Math.abs(b1)} and g(x) = ${a2}x ${b2 >= 0 ? "+" : "-"} ${Math.abs(b2)}. Find ${forward ? `f(g(${x0}))` : `g(f(${x0}))`}.`;
  const inner = forward ? g(x0) : f(x0);
  const solution = forward
    ? [`g(${x0}) = ${a2}(${x0}) ${b2 >= 0 ? "+" : "-"} ${Math.abs(b2)} = ${inner}`, `f(${inner}) = ${a1}(${inner}) ${b1 >= 0 ? "+" : "-"} ${Math.abs(b1)} = ${val}`]
    : [`f(${x0}) = ${a1}(${x0}) ${b1 >= 0 ? "+" : "-"} ${Math.abs(b1)} = ${inner}`, `g(${inner}) = ${a2}(${inner}) ${b2 >= 0 ? "+" : "-"} ${Math.abs(b2)} = ${val}`];
  if (type === "fr") return buildFR(prompt, `${val}`, solution);
  return buildMC(prompt, val, fmtNum, solution, [inner, val + 1, -val]);
}

function piecewiseFunctions(difficulty, type) {
  const c = randInt(-4, 4);
  const m1 = randNonZero(-4, 4), b1 = randInt(-5, 5);
  const m2 = randNonZero(-4, 4), b2 = randInt(-5, 5);
  const useFirst = Math.random() < 0.5;
  const x0 = useFirst ? c - randInt(1, 3 + difficulty) : c + randInt(0, 3 + difficulty);
  const val = useFirst ? m1 * x0 + b1 : m2 * x0 + b2;
  const prompt = `f(x) = { ${m1}x ${b1 >= 0 ? "+" : "-"} ${Math.abs(b1)}  if x < ${c}\n         ${m2}x ${b2 >= 0 ? "+" : "-"} ${Math.abs(b2)}  if x >= ${c} }\nFind f(${x0}).`;
  const solution = [
    `Since ${x0} ${useFirst ? "<" : ">="} ${c}, use the ${useFirst ? "first" : "second"} piece.`,
    `f(${x0}) = ${useFirst ? m1 : m2}(${x0}) ${(useFirst ? b1 : b2) >= 0 ? "+" : "-"} ${Math.abs(useFirst ? b1 : b2)} = ${val}`,
  ];
  if (type === "fr") return buildFR(prompt, `${val}`, solution);
  return buildMC(prompt, val, fmtNum, solution, [useFirst ? m2 * x0 + b2 : m1 * x0 + b1, val + 1, val - 1]);
}

function absoluteValueFunctions(difficulty, type) {
  const a = randNonZero(-5, 5);
  const b = randInt(-6, 6);
  const allowZero = difficulty === 3 && Math.random() < 0.3;
  const c = allowZero ? 0 : randInt(1, 8);
  const prompt = `Solve for x: |${a}x ${b >= 0 ? "+" : "-"} ${Math.abs(b)}| = ${c}`;
  if (c === 0) {
    const x = fracStr(-b, a);
    const answer = `x = ${x}`;
    const solution = [`|${a}x ${b >= 0 ? "+" : "-"} ${Math.abs(b)}| = 0 means ${a}x ${b >= 0 ? "+" : "-"} ${Math.abs(b)} = 0`, `x = ${x}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, answer, (v) => v, solution, [`x = ${fracStr(b, a)}`, `x = ${fracStr(-b, -a)}`, `x = ${fracStr(-b + a, a)}`]);
  }
  const x1 = fracStr(c - b, a);
  const x2 = fracStr(-c - b, a);
  const answer = `x = ${x1} or x = ${x2}`;
  const solution = [
    `${a}x ${b >= 0 ? "+" : "-"} ${Math.abs(b)} = ${c}  or  ${a}x ${b >= 0 ? "+" : "-"} ${Math.abs(b)} = ${-c}`,
    `x = ${x1}  or  x = ${x2}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [`x = ${x1} or x = ${fracStr(c + b, a)}`, `x = ${fracStr(c - b, -a)} or x = ${x2}`, `x = ${x1}`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function intuitiveLimit(difficulty, type) {
  const useHole = difficulty >= 2 && Math.random() < 0.6;
  if (!useHole) {
    const a = randInt(-3, 3), b = randInt(-3, 3), c = randInt(-5, 5);
    const k = randInt(-4, 4);
    const val = a * k * k + b * k + c;
    const fx = polyStr([a, b, c]);
    const prompt = `Find lim(x -> ${k}) of f(x) = ${fx}.`;
    const answer = `${val}`;
    const solution = [`f is a polynomial, so it is continuous everywhere; the limit equals f(${k}).`, `f(${k}) = ${val}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, val, fmtNum, solution, [val + 1, val - 1, -val]);
  } else {
    const k = randNonZero(-6, 6);
    const prompt = `Find lim(x -> ${k}) of f(x) = (x^2 - ${k * k}) / (${xMinus(k)}).`;
    const answer = `${2 * k}`;
    const solution = [
      `Factor the numerator: x^2 - ${k * k} = (${xMinus(k)})(x ${k >= 0 ? "+" : "-"} ${Math.abs(k)})`,
      `f(x) = (${xMinus(k)})(x ${k >= 0 ? "+" : "-"} ${Math.abs(k)}) / (${xMinus(k)}) = x ${k >= 0 ? "+" : "-"} ${Math.abs(k)}, for x != ${k}`,
      `lim(x -> ${k}) f(x) = ${k} + ${k} = ${2 * k}`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, 2 * k, fmtNum, solution, [k, -2 * k, 2 * k + 2]);
  }
}

function intermediateValueTheorem(difficulty, type) {
  let a1, b1, c1, lo, hi, f, flo, fhi;
  do {
    a1 = randNonZero(-3, 3);
    b1 = randInt(-4, 4);
    c1 = randInt(-6, 6);
    lo = randInt(-4, 0);
    hi = lo + randInt(1, 3 + difficulty);
    f = (x) => a1 * x * x + b1 * x + c1;
    flo = f(lo);
    fhi = f(hi);
  } while (flo === 0 || fhi === 0);
  const fx = polyStr([a1, b1, c1]);
  const guarantees = (flo < 0 && fhi > 0) || (flo > 0 && fhi < 0);
  const prompt = `Let f(x) = ${fx}. Given f(${lo}) = ${flo} and f(${hi}) = ${fhi}, does the Intermediate Value Theorem guarantee a zero of f on [${lo}, ${hi}]?`;
  const pool = [
    "Yes -- f changes sign on the interval, so IVT guarantees a zero.",
    "No -- f(a) and f(b) have the same sign, so IVT does not guarantee a zero.",
    "Yes -- because f is a polynomial, IVT always guarantees a zero regardless of sign.",
    "No -- IVT never applies to polynomial functions.",
  ];
  const answer = guarantees ? pool[0] : pool[1];
  const solution = [
    `f(${lo}) = ${flo}, f(${hi}) = ${fhi}`,
    guarantees
      ? `f(${lo}) and f(${hi}) have opposite signs, so IVT guarantees at least one zero in (${lo}, ${hi}).`
      : `f(${lo}) and f(${hi}) have the same sign, so IVT does not guarantee a zero on this interval.`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, answer, (v) => v, solution, pool.filter((p) => p !== answer));
}

function rateOfChange(difficulty, type) {
  const useQuadratic = difficulty >= 2 && Math.random() < 0.6;
  const a = useQuadratic ? randNonZero(-3, 3) : 0;
  const b = randNonZero(-5, 5);
  const c = randInt(-6, 6);
  const x1 = randInt(-4, 2);
  const x2 = x1 + randInt(1, difficulty + 2);
  const f = (x) => a * x * x + b * x + c;
  const y1 = f(x1);
  const y2 = f(x2);
  const rate = (y2 - y1) / (x2 - x1);
  const fx = useQuadratic ? polyStr([a, b, c]) : polyStr([b, c]);
  const prompt = `Let f(x) = ${fx}. Find the average rate of change of f on the interval [${x1}, ${x2}].`;
  const solution = [
    `f(${x1}) = ${y1}, f(${x2}) = ${y2}`,
    `Average rate of change = (f(${x2}) - f(${x1})) / (${x2} - ${x1}) = (${y2} - ${y1}) / (${x2 - x1}) = ${fracStr(y2 - y1, x2 - x1)}`,
  ];
  const rateStr = fracStr(y2 - y1, x2 - x1);
  if (type === "fr") return buildFR(prompt, rateStr, solution);
  return buildMC(
    prompt,
    rate,
    (v) => (Number.isInteger(v) ? `${v}` : fracStr(round2(v * 1000), 1000)),
    solution,
    [rate + 1, rate - 1, -rate, rate * 2]
  );
}

function functionTransformations(difficulty, type) {
  const base = choice(["x^2", "sqrt(x)", "|x|", "x^3"]);
  const h = randNonZero(-5, 5);
  const k = randNonZero(-5, 5);
  const a = difficulty === 1 ? choice([1, -1]) : choice([-3, -2, -1, 1, 2, 3]);
  const hSign = h >= 0 ? "-" : "+";
  const inner = `(x ${hSign} ${Math.abs(h)})`;
  const baseWithInner = base.replace(/x/g, inner);
  const aTerm = a === 1 ? "" : a === -1 ? "-" : `${a}`;
  const kSign = k >= 0 ? "+" : "-";
  const gStr = `g(x) = ${aTerm}${baseWithInner} ${kSign} ${Math.abs(k)}`;
  const prompt = `The graph of g is obtained by transforming the graph of f(x) = ${base}. Given ${gStr}, describe the transformations applied to f, in order.`;
  const parts = [];
  if (Math.abs(a) !== 1) parts.push(`vertical stretch/compression by a factor of ${Math.abs(a)}`);
  if (a < 0) parts.push("reflection over the x-axis");
  parts.push(`horizontal shift ${h > 0 ? "right" : "left"} by ${Math.abs(h)}`);
  parts.push(`vertical shift ${k > 0 ? "up" : "down"} by ${Math.abs(k)}`);
  const answer = parts.join("; ");
  const solution = [
    `Compare g(x) = ${aTerm || "1"}*f(x ${hSign} ${Math.abs(h)}) ${kSign} ${Math.abs(k)} to f(x).`,
    `The value inside the parentheses shifts horizontally opposite its sign; the value outside shifts vertically with its sign.`,
    `Transformations: ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    parts.map((p) => p.replace("right", "TEMP").replace("left", "right").replace("TEMP", "left")).join("; "),
    parts.map((p) => p.replace("up", "TEMP").replace("down", "up").replace("TEMP", "down")).join("; "),
    [...parts].reverse().join("; "),
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function inverseFunctions(difficulty, type) {
  const a = randNonZero(-6, 6);
  const b = randInt(-8, 8);
  const prompt = `Find the inverse of f(x) = ${a}x ${b >= 0 ? "+" : "-"} ${Math.abs(b)}.`;
  const answer = `f^-1(x) = (x ${b >= 0 ? "-" : "+"} ${Math.abs(b)}) / ${a}`;
  const solution = [`y = ${a}x ${b >= 0 ? "+" : "-"} ${Math.abs(b)}`, `Solve for x: x = (y ${b >= 0 ? "-" : "+"} ${Math.abs(b)}) / ${a}`, `Swap x and y: ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [`f^-1(x) = ${a}x ${b >= 0 ? "-" : "+"} ${Math.abs(b)}`, `f^-1(x) = (x ${b >= 0 ? "+" : "-"} ${Math.abs(b)}) / ${a}`, `f^-1(x) = (${a}x ${b >= 0 ? "-" : "+"} ${Math.abs(b)})`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

/* ============================ UNIT 2: POLYNOMIALS ======================= */

function polynomialDivision(difficulty, type) {
  const degree = difficulty === 1 ? 3 : 4;
  const coeffs = [randNonZero(-4, 4), ...Array.from({ length: degree }, () => randInt(-6, 6))];
  const c = randNonZero(-4, 4);
  const { quotient, remainder } = syntheticDivide(coeffs, c);
  const fx = polyStr(coeffs);
  const qStr = polyStr(quotient);
  const prompt = `Use synthetic division to divide f(x) = ${fx} by (x - ${c}). Give the quotient and remainder.`;
  const answer = `quotient = ${qStr}, remainder = ${remainder}`;
  const solution = [
    `Synthetic division by c = ${c} on coefficients [${coeffs.join(", ")}]:`,
    `Quotient coefficients: [${quotient.join(", ")}], remainder = ${remainder}`,
    `f(x) = (x - ${c})(${qStr}) ${remainder >= 0 ? "+" : "-"} ${Math.abs(remainder)}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `quotient = ${qStr}, remainder = ${-remainder}`,
    `quotient = ${polyStr(quotient.map((x) => x + 1))}, remainder = ${remainder}`,
    `quotient = ${qStr}, remainder = ${remainder + 1}`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function remainderFactorTheorem(difficulty, type) {
  const degree = difficulty === 1 ? 2 : 3;
  const coeffs = [randNonZero(-3, 3), ...Array.from({ length: degree }, () => randInt(-6, 6))];
  const c = randInt(-3, 3);
  const fx = polyStr(coeffs);
  const val = coeffs.reduce((acc, coef) => acc * c + coef, 0);
  const askFactor = Math.random() < 0.5;
  if (!askFactor) {
    const prompt = `By the Remainder Theorem, find the remainder when f(x) = ${fx} is divided by (x - ${c}).`;
    const answer = `${val}`;
    const solution = [`By the Remainder Theorem, the remainder equals f(${c}).`, `f(${c}) = ${val}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, val, fmtNum, solution, [val + 1, val - 1, -val]);
  } else {
    const isFactor = val === 0;
    const prompt = `Is (x - ${c}) a factor of f(x) = ${fx}?`;
    const answer = isFactor ? `Yes, since f(${c}) = 0.` : `No, since f(${c}) = ${val} != 0.`;
    const solution = [`By the Factor Theorem, (x - ${c}) is a factor of f if and only if f(${c}) = 0.`, `f(${c}) = ${val}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const pool = [
      `Yes, since f(${c}) = 0.`,
      `No, since f(${c}) = ${val} != 0.`,
      `Yes, every linear expression is a factor of every polynomial.`,
      `No, (x - ${c}) can never be a factor of a polynomial.`,
    ];
    return buildMC(prompt, answer, (v) => v, solution, pool.filter((p) => p !== answer));
  }
}

function polynomialZeros(difficulty, type) {
  const withMultiplicity = difficulty >= 2 && Math.random() < 0.5;
  if (!withMultiplicity) {
    const nRoots = difficulty === 1 ? 2 : 3;
    const roots = [];
    while (roots.length < nRoots) {
      const r = randInt(-6, 6);
      if (!roots.includes(r)) roots.push(r);
    }
    const coeffs = nRoots === 2 ? expandTwoFactors(...roots) : expandThreeFactors(...roots);
    const fx = polyStr(coeffs);
    const factored = roots.map(linearFactorStr).join("");
    const sortedRoots = [...roots].sort((a, b) => a - b);
    const prompt = `A polynomial function is given by f(x) = ${fx}, which factors as f(x) = ${factored}. List the real zeros of f.`;
    const answer = sortedRoots.join(", ");
    const solution = [`Set each factor equal to 0: ${roots.map((r) => `x - (${r}) = 0`).join(", ")}`, `Zeros: x = ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [
      sortedRoots.map((r) => r + 1).join(", "),
      sortedRoots.map((r) => -r).join(", "),
      [...sortedRoots].reverse().map((r) => r * -1).join(", "),
    ];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  } else {
    const repeated = randInt(-5, 5);
    let other;
    do {
      other = randInt(-5, 5);
    } while (other === repeated);
    const coeffs = expandThreeFactors(repeated, repeated, other);
    const fx = polyStr(coeffs);
    const factored = `${linearFactorStr(repeated)}^2${linearFactorStr(other)}`;
    const answer = `x = ${repeated} (multiplicity 2), x = ${other} (multiplicity 1)`;
    const prompt = `A polynomial function is given by f(x) = ${fx}, which factors as f(x) = ${factored}. List the real zeros of f and their multiplicities.`;
    const solution = [`Set each factor equal to 0.`, `The factor (x - (${repeated})) is squared, so x = ${repeated} has multiplicity 2.`, `x = ${other} has multiplicity 1.`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [
      `x = ${repeated} (multiplicity 1), x = ${other} (multiplicity 2)`,
      `x = ${repeated} (multiplicity 2), x = ${other} (multiplicity 2)`,
      `x = ${other} (multiplicity 2), x = ${repeated} (multiplicity 1)`,
    ];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  }
}

function complexNumberArithmetic(difficulty, type) {
  const a = randInt(-6, 6), b = randNonZero(-6, 6);
  const c = randInt(-6, 6), d = randNonZero(-6, 6);
  const op = difficulty === 1 ? choice(["add", "subtract"]) : choice(["add", "subtract", "multiply", "divide"]);
  const z1 = fmtComplex(a, b), z2 = fmtComplex(c, d);
  if (op === "add" || op === "subtract") {
    const sign = op === "add" ? 1 : -1;
    const re = a + sign * c, im = b + sign * d;
    const prompt = `${op === "add" ? "Add" : "Subtract"}: (${z1}) ${op === "add" ? "+" : "-"} (${z2})`;
    const answer = fmtComplex(re, im);
    const solution = [
      `Combine real parts: ${a} ${sign > 0 ? "+" : "-"} ${c} = ${re}`,
      `Combine imaginary parts: ${b} ${sign > 0 ? "+" : "-"} ${d} = ${im}`,
      `Result: ${answer}`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, answer, (v) => v, solution, [fmtComplex(re + 2, im), fmtComplex(re, -im), fmtComplex(-re, im)]);
  } else if (op === "multiply") {
    const re = a * c - b * d, im = a * d + b * c;
    const prompt = `Multiply: (${z1})(${z2})`;
    const answer = fmtComplex(re, im);
    const solution = [
      `(${z1})(${z2}) = ${a * c} + ${a * d}i + ${b * c}i + ${b * d}i^2`,
      `Since i^2 = -1: = (${a * c} - ${b * d}) + (${a * d} + ${b * c})i`,
      `Result: ${answer}`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, answer, (v) => v, solution, [fmtComplex(re + 2 * b * d, im), fmtComplex(re, -im), fmtComplex(-re, -im)]);
  } else {
    const den = c * c + d * d;
    const reNum = a * c + b * d, imNum = b * c - a * d;
    const prompt = `Divide: (${z1}) / (${z2})`;
    const answer = fmtComplexFrac(reNum, den, imNum, den);
    const solution = [
      `Multiply numerator and denominator by the conjugate of the denominator, ${fmtComplex(c, -d)}.`,
      `Denominator: ${c}^2 + ${d}^2 = ${den}`,
      `Numerator: (${z1})(${fmtComplex(c, -d)}) = ${reNum} + ${imNum}i`,
      `Result: ${answer}`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [
      fmtComplexFrac(reNum + den, den, imNum, den),
      fmtComplexFrac(reNum, den, -imNum, den),
      fmtComplexFrac(-reNum, den, imNum, den),
    ];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  }
}

function fundamentalTheoremAlgebra(difficulty, type) {
  const n = difficulty === 1 ? randInt(2, 3) : randInt(4, 6);
  const lead = randNonZero(-4, 4);
  const rest = Array.from({ length: n }, () => randInt(-6, 6));
  const fx = polyStr([lead, ...rest]);
  const prompt = `By the Fundamental Theorem of Algebra, how many zeros (counted with multiplicity, including complex zeros) does f(x) = ${fx} have?`;
  const answer = `${n}`;
  const solution = [`f has degree ${n}.`, `By the Fundamental Theorem of Algebra, a degree-${n} polynomial has exactly ${n} zeros, counted with multiplicity, over the complex numbers.`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, n, fmtNum, solution, [n + 1, n - 1, n * 2]);
}

function rationalRootTheorem(difficulty, type) {
  const lead = choice(difficulty === 1 ? [1, 2] : [1, 2, 3, 4]);
  const c0 = randNonZero(-12, 12);
  const pFactors = factorsOf(c0);
  const qFactors = factorsOf(lead);
  const ratios = new Set();
  pFactors.forEach((p) => qFactors.forEach((q) => ratios.add(fracStr(p, q))));
  const sorted = [...ratios].sort((a, b) => parseFloat(a) - parseFloat(b));
  const answer = sorted.map((r) => `±${r}`).join(", ");
  const degree = difficulty === 1 ? 2 : 3;
  const middle = Array.from({ length: degree - 1 }, () => randInt(-6, 6));
  const coeffs = [lead, ...middle, c0];
  const fx = polyStr(coeffs);
  const prompt = `List all possible rational roots of f(x) = ${fx}, according to the Rational Root Theorem.`;
  const solution = [
    `Factors of the constant term (${c0}): ${pFactors.join(", ")}`,
    `Factors of the leading coefficient (${lead}): ${qFactors.join(", ")}`,
    `Possible rational roots (p/q): ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    sorted.join(", "),
    [...sorted.map((r) => `±${r}`), `±${fracStr(c0 + 1, lead)}`].join(", "),
    pFactors.map((p) => `±${p}`).join(", "),
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function conjugateZerosTheorem(difficulty, type) {
  const a = randInt(-5, 5);
  const b = randNonZero(1, 6) * choice([1, -1]);
  const prompt = `A polynomial f(x) with real coefficients has ${fmtComplex(a, b)} as one of its zeros. By the Conjugate Zeros Theorem, what other complex number must also be a zero of f?`;
  const answer = fmtComplex(a, -b);
  const solution = [`Since f has real coefficients, non-real zeros occur in conjugate pairs.`, `The conjugate of ${fmtComplex(a, b)} is ${answer}.`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, answer, (v) => v, solution, [fmtComplex(-a, b), fmtComplex(-a, -b), fmtComplex(a, b)]);
}

function sumProductRoots(difficulty, type) {
  const useCubic = difficulty === 3 && Math.random() < 0.5;
  if (!useCubic) {
    const a = randNonZero(-4, 4), b = randInt(-8, 8), c = randInt(-8, 8);
    const fx = polyStr([a, b, c]);
    const sum = fracStr(-b, a), prod = fracStr(c, a);
    const prompt = `For ${fx} = 0, find the sum and product of the roots without solving for the roots directly.`;
    const answer = `sum = ${sum}, product = ${prod}`;
    const solution = [`For ax^2 + bx + c = 0: sum of roots = -b/a, product of roots = c/a.`, `sum = -(${b})/(${a}) = ${sum}`, `product = ${c}/(${a}) = ${prod}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, answer, (v) => v, solution, [
      `sum = ${fracStr(b, a)}, product = ${prod}`,
      `sum = ${sum}, product = ${fracStr(-c, a)}`,
      `sum = ${fracStr(-b, a)}, product = ${fracStr(a, c)}`,
    ]);
  } else {
    const a = randNonZero(-3, 3), b = randInt(-6, 6), c = randInt(-6, 6), d = randInt(-6, 6);
    const fx = polyStr([a, b, c, d]);
    const sum = fracStr(-b, a), prod = fracStr(-d, a);
    const prompt = `For ${fx} = 0, find the sum and product of the roots without solving for the roots directly.`;
    const answer = `sum = ${sum}, product = ${prod}`;
    const solution = [`For ax^3 + bx^2 + cx + d = 0: sum of roots = -b/a, product of roots = -d/a.`, `sum = -(${b})/(${a}) = ${sum}`, `product = -(${d})/(${a}) = ${prod}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, answer, (v) => v, solution, [
      `sum = ${fracStr(b, a)}, product = ${prod}`,
      `sum = ${sum}, product = ${fracStr(d, a)}`,
      `sum = ${fracStr(-c, a)}, product = ${prod}`,
    ]);
  }
}

function permutationsCombinations(difficulty, type) {
  const n = difficulty === 1 ? randInt(4, 7) : randInt(6, 10);
  const r = randInt(2, Math.min(n - 1, 5));
  const isCombo = Math.random() < 0.5;
  const val = isCombo ? nCr(n, r) : nPr(n, r);
  const prompt = isCombo
    ? `Evaluate: C(${n}, ${r}) (the number of ways to choose ${r} items from ${n})`
    : `Evaluate: P(${n}, ${r}) (the number of ways to arrange ${r} items from ${n})`;
  const answer = `${val}`;
  const solution = isCombo
    ? [`C(n, r) = n! / (r!(n-r)!)`, `C(${n}, ${r}) = ${n}! / (${r}! * ${n - r}!) = ${val}`]
    : [`P(n, r) = n! / (n-r)!`, `P(${n}, ${r}) = ${n}! / ${n - r}! = ${val}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, val, fmtNum, solution, [isCombo ? nPr(n, r) : nCr(n, r), val + r, Math.max(1, val - r)]);
}

function binomialExpansion(difficulty, type) {
  const n = difficulty === 1 ? randInt(4, 5) : randInt(5, 7);
  const c = randNonZero(-3, 3);
  const k = randInt(1, n - 1);
  const coeff = nCr(n, k) * Math.pow(c, n - k);
  const prompt = `In the binomial expansion of (x + ${c})^${n}, find the coefficient of the x^${k} term.`;
  const answer = `${coeff}`;
  const solution = [
    `The general term is C(n, k) x^k c^(n-k) = C(${n}, ${k}) x^${k} (${c})^${n - k}.`,
    `C(${n}, ${k}) = ${nCr(n, k)}`,
    `Coefficient = ${nCr(n, k)} * (${c})^${n - k} = ${coeff}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, coeff, fmtNum, solution, [nCr(n, k), coeff * c, -coeff]);
}

function binomialProbability(difficulty, type) {
  const n = difficulty === 1 ? randInt(4, 6) : randInt(6, 10);
  const k = randInt(0, n);
  const p = choice([0.5, 0.25, 0.75, 0.2, 0.8, 0.4, 0.6]);
  const prob = nCr(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k);
  const rounded = round4(prob);
  const prompt = `A binomial experiment has n = ${n} trials with success probability p = ${p}. Find P(X = ${k}), rounded to 4 decimal places.`;
  const answer = `${rounded}`;
  const solution = [`P(X = k) = C(n, k) p^k (1-p)^(n-k)`, `P(X = ${k}) = C(${n}, ${k})(${p})^${k}(${round4(1 - p)})^${n - k} ~ ${rounded}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, rounded, fmt4, solution, [round4(rounded + 0.05), round4(Math.max(0, rounded - 0.05)), round4(1 - rounded)]);
}

/* ========================= UNIT 3: RATIONAL FUNCTIONS ==================== */

function makeRational(difficulty) {
  const numRoots = [];
  const denRoots = [];
  const nNum = difficulty === 1 ? 1 : 2;
  const nDen = difficulty === 1 ? 1 : 2;
  const used = new Set();
  const pick = () => {
    let r;
    do {
      r = randInt(-6, 6);
    } while (used.has(r));
    used.add(r);
    return r;
  };
  for (let i = 0; i < nNum; i++) numRoots.push(pick());
  for (let i = 0; i < nDen; i++) denRoots.push(pick());
  return { numRoots, denRoots };
}

function verticalHorizontalAsymptotes(difficulty, type) {
  const { numRoots, denRoots } = makeRational(difficulty);
  const k = difficulty >= 2 ? choice([1, 1, 1, 2, 3, -1, -2]) : 1;
  const numStr = numRoots.map(linearFactorStr).join("");
  const denStr = denRoots.map(linearFactorStr).join("");
  const kPrefix = k === 1 ? "" : k === -1 ? "-" : `${k}`;
  const prompt = `Let f(x) = ${kPrefix}[${numStr}] / [${denStr}]. Find the vertical asymptote(s) and horizontal asymptote of f.`;
  const vaSorted = [...denRoots].sort((a, b) => a - b);
  const va = vaSorted.map((r) => `x = ${r}`).join(", ");
  const degNum = numRoots.length, degDen = denRoots.length;
  let ha;
  if (degNum < degDen) ha = "y = 0";
  else if (degNum === degDen) ha = `y = ${k}`;
  else ha = "none";
  const answer = `vertical: ${va}; horizontal: ${ha}`;
  const solution = [
    `Vertical asymptotes occur where the denominator is 0 (and the numerator is not): x = ${vaSorted.join(", ")}.`,
    degNum < degDen
      ? `Numerator degree (${degNum}) < denominator degree (${degDen}), so the horizontal asymptote is y = 0.`
      : degNum === degDen
      ? `Numerator and denominator degrees are equal (${degNum}), so the horizontal asymptote is the ratio of leading coefficients: y = ${k}.`
      : `Numerator degree (${degNum}) > denominator degree (${degDen}), so there is no horizontal asymptote.`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `vertical: ${numRoots.sort((a, b) => a - b).map((r) => `x = ${r}`).join(", ")}; horizontal: ${ha}`,
    `vertical: ${va}; horizontal: y = 0`,
    `vertical: ${va}; horizontal: none`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function slantAsymptotes(difficulty, type) {
  const d = randInt(-5, 5);
  let r1, r2;
  do {
    r1 = randInt(-6, 6);
    r2 = randInt(-6, 6);
  } while (r1 === r2);
  const numCoeffs = expandTwoFactors(r1, r2);
  const { quotient, remainder } = syntheticDivide(numCoeffs, d);
  const slantStr = polyStr(quotient);
  const prompt = `Let f(x) = [${linearFactorStr(r1)}${linearFactorStr(r2)}] / [${linearFactorStr(d)}]. Find the equation of the slant asymptote of f.`;
  const answer = `y = ${slantStr}`;
  const solution = [
    `Since the numerator's degree (2) is exactly one more than the denominator's degree (1), f has a slant asymptote.`,
    `Divide the numerator by (x - ${d}) using synthetic division: quotient = ${slantStr}, remainder = ${remainder}.`,
    `The slant asymptote is the quotient (ignoring the remainder): ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [`y = ${polyStr([1, quotient[1] + 1])}`, `y = ${polyStr([1, -quotient[1]])}`, `y = ${remainder}`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function rationalHoles(difficulty, type) {
  const shared = randInt(-6, 6);
  const usedRoots = new Set([shared]);
  const pick = () => {
    let r;
    do {
      r = randInt(-6, 6);
    } while (usedRoots.has(r));
    usedRoots.add(r);
    return r;
  };
  const extraNum = difficulty === 1 ? [] : [pick()];
  const extraDen = difficulty === 1 ? [] : [pick()];
  const numRoots = [shared, ...extraNum];
  const denRoots = [shared, ...extraDen];
  const numStr = numRoots.map(linearFactorStr).join("");
  const denStr = denRoots.map(linearFactorStr).join("");
  const prompt = `Let f(x) = [${numStr}] / [${denStr}]. This function has a removable discontinuity (a hole). Give its x-coordinate.`;
  const answer = `x = ${shared}`;
  const solution = [
    `The factor (x - (${shared})) appears in both the numerator and denominator, so it cancels.`,
    `This creates a hole at x = ${shared} (rather than a vertical asymptote).`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const others = [...numRoots, ...denRoots].filter((r) => r !== shared);
  const distractors = others.slice(0, 3).map((r) => `x = ${r}`);
  while (distractors.length < 3) distractors.push(`x = ${shared + distractors.length + 1}`);
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function oneSidedInfiniteLimits(difficulty, type) {
  const k = randInt(-5, 5);
  const signMult = choice([1, -1]);
  const fromRight = Math.random() < 0.5;
  const prompt = `Let f(x) = ${signMult === 1 ? "" : "-"}1 / (x - ${k}). Find lim(x -> ${k}${fromRight ? "+" : "-"}) f(x).`;
  const baseSign = fromRight ? 1 : -1;
  const resultSign = baseSign * signMult;
  const answer = resultSign > 0 ? "infinity" : "-infinity";
  const solution = [
    `As x -> ${k}${fromRight ? "+" : "-"}, (x - ${k}) approaches 0 from the ${fromRight ? "positive" : "negative"} side.`,
    `So 1/(x-${k}) -> ${baseSign > 0 ? "infinity" : "-infinity"}` + (signMult === -1 ? `, and the negative sign flips this to ${answer}.` : `.`),
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const pool = ["infinity", "-infinity", "0", "the limit does not exist"];
  return buildMC(prompt, answer, (v) => v, solution, pool.filter((p) => p !== answer));
}

function rationalInequalities(difficulty, type) {
  let a, b;
  do {
    a = randInt(-6, 6);
    b = randInt(-6, 6);
  } while (a === b);
  const wantPositive = Math.random() < 0.5;
  const ineqSymbol = wantPositive ? ">" : "<";
  const lo = Math.min(a, b), hi = Math.max(a, b);
  const prompt = `Solve the inequality: (x - ${a}) / (x - ${b}) ${ineqSymbol} 0`;
  const answer = wantPositive ? `x < ${lo} or x > ${hi}` : `${lo} < x < ${hi}`;
  const solution = [
    `The expression is undefined at x = ${b} and equal to 0 at x = ${a}; these are the critical points ${lo} and ${hi}.`,
    `Testing a point in each interval shows the expression is ${wantPositive ? "positive" : "negative"} ${wantPositive ? "outside" : "between"} the critical points.`,
    `Solution: ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [wantPositive ? `${lo} < x < ${hi}` : `x < ${lo} or x > ${hi}`, `x < ${lo}`, `x > ${hi}`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function partialFractions(difficulty, type) {
  let a, b;
  do {
    a = randInt(-6, 6);
    b = randInt(-6, 6);
  } while (a === b);
  const p = randNonZero(-5, 5), q = randNonZero(-6, 6);
  const A = fracStr(p * a + q, a - b);
  const B = fracStr(p * b + q, b - a);
  const numStr = `${p}x ${q >= 0 ? "+" : "-"} ${Math.abs(q)}`;
  const prompt = `Decompose into partial fractions: (${numStr}) / [${linearFactorStr(a)}${linearFactorStr(b)}]`;
  const answer = `${A}/${linearFactorStr(a)} + ${B}/${linearFactorStr(b)}`;
  const solution = [
    `Write (${numStr})/[(x-${a})(x-${b})] = A/(x-${a}) + B/(x-${b}).`,
    `Cover-up method: A = (${p}(${a}) ${q >= 0 ? "+" : "-"} ${Math.abs(q)}) / (${a} - ${b}) = ${A}`,
    `B = (${p}(${b}) ${q >= 0 ? "+" : "-"} ${Math.abs(q)}) / (${b} - ${a}) = ${B}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `${B}/${linearFactorStr(a)} + ${A}/${linearFactorStr(b)}`,
    `${A}/${linearFactorStr(a)} - ${B}/${linearFactorStr(b)}`,
    `${fracStr(-(p * a + q), a - b)}/${linearFactorStr(a)} + ${B}/${linearFactorStr(b)}`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function rationalEquations(difficulty, type) {
  const a = randInt(-6, 6);
  const k = randNonZero(-8, 8);
  const c = randNonZero(-6, 6);
  const answerNum = k + c * a;
  const answer = `x = ${fracStr(answerNum, c)}`;
  const prompt = `Solve for x: ${k} / (x - ${a}) = ${c}`;
  const solution = [
    `Multiply both sides by (x - ${a}): ${k} = ${c}(x - ${a})`,
    `${k} = ${c}x - ${c * a}`,
    `x = (${k} + ${c * a}) / ${c} = ${fracStr(answerNum, c)}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [`x = ${fracStr(k - c * a, c)}`, `x = ${fracStr(answerNum, -c)}`, `x = ${a}`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

/* =============== UNIT 4: EXPONENTIAL AND LOGARITHMIC FUNCTIONS =========== */

function logarithmExpressions(difficulty, type) {
  const expand = Math.random() < 0.5;
  const base = choice([2, 10]);
  if (expand) {
    const p = randInt(2, 5);
    const q = randInt(2, 5);
    const prompt = `Expand as a sum/difference of logarithms: log_${base}(x^${p} / y^${q})`;
    const answer = `${p}*log_${base}(x) - ${q}*log_${base}(y)`;
    const solution = [`log_${base}(x^${p}/y^${q}) = log_${base}(x^${p}) - log_${base}(y^${q})`, `= ${p}log_${base}(x) - ${q}log_${base}(y)`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [`${p}*log_${base}(x) + ${q}*log_${base}(y)`, `log_${base}(x)^${p} / log_${base}(y)^${q}`, `${q}*log_${base}(x) - ${p}*log_${base}(y)`];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  } else {
    const p = randInt(2, 5);
    const q = randInt(2, 5);
    const prompt = `Condense into a single logarithm: ${p}log_${base}(x) + ${q}log_${base}(y)`;
    const answer = `log_${base}(x^${p} * y^${q})`;
    const solution = [`${p}log_${base}(x) = log_${base}(x^${p})`, `${q}log_${base}(y) = log_${base}(y^${q})`, `Sum of logs = log of product: ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [`log_${base}(x^${p} + y^${q})`, `log_${base}(x^${p} / y^${q})`, `log_${base}(x^${q} * y^${p})`];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  }
}

function expLogEquations(difficulty, type) {
  const isExp = Math.random() < 0.5;
  if (isExp) {
    const a = randInt(2, 6);
    const base = choice([2, 3, 5, 10]);
    const c = a * Math.pow(base, randInt(1, 2 + difficulty));
    const prompt = `Solve for x: ${a} * ${base}^x = ${c}`;
    const xVal = Math.log(c / a) / Math.log(base);
    const answer = Number.isInteger(round2(xVal)) ? `${Math.round(xVal)}` : `x = log_${base}(${fracStr(c, a)}) ~ ${round2(xVal)}`;
    const solution = [`Divide both sides by ${a}: ${base}^x = ${fracStr(c, a)}`, `Take log base ${base} of both sides: x = log_${base}(${fracStr(c, a)})`, `x ~ ${round2(xVal)}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, round2(xVal), fmtNum, solution, [round2(xVal) + 1, round2(xVal) - 1, round2(xVal * 2)]);
  } else {
    const base = choice([2, 3, 5, 10]);
    const xVal = randInt(2, 6 + difficulty);
    const rhs = randInt(1, 3);
    const c = Math.pow(base, xVal + rhs);
    const prompt = `Solve for x: log_${base}(${c}) = x + ${rhs}`;
    const answer = `${xVal}`;
    const solution = [`log_${base}(${c}) = ${xVal + rhs}, since ${base}^${xVal + rhs} = ${c}`, `So x + ${rhs} = ${xVal + rhs}`, `x = ${xVal}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, xVal, fmtNum, solution, [xVal + rhs, xVal - 1, xVal + 1]);
  }
}

function compoundInterest(difficulty, type) {
  const P = randInt(500, 5000);
  const ratePct = choice([2, 3, 4, 5, 6, 8]);
  const r = ratePct / 100;
  const n = choice([1, 2, 4, 12]);
  const t = randInt(2, 5 + difficulty);
  const A = P * Math.pow(1 + r / n, n * t);
  const rounded = round2(A);
  const compoundName = { 1: "annually", 2: "semiannually", 4: "quarterly", 12: "monthly" }[n];
  const prompt = `$${P} is invested at an annual rate of ${ratePct}% compounded ${compoundName} for ${t} years. Use A = P(1 + r/n)^(nt) to find the value of the investment, rounded to the nearest cent.`;
  const answer = `$${rounded.toFixed(2)}`;
  const solution = [`A = ${P}(1 + ${r}/${n})^(${n}*${t})`, `A = ${P}(${round4(1 + r / n)})^${n * t} ~ ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, rounded, (v) => `$${v.toFixed(2)}`, solution, [round2(P * (1 + r * t)), round2(rounded * 1.1), round2(rounded * 0.9)]);
}

function exponentialModeling(difficulty, type) {
  const P0 = randInt(100, 900) * 10;
  const rate = choice([0.03, 0.05, 0.08, 0.1, -0.04, -0.06]);
  const t = randInt(2, 4 + difficulty);
  const val = P0 * Math.pow(1 + rate, t);
  const growth = rate > 0 ? "grows" : "decays";
  const prompt = `A population is P0 = ${P0} and ${growth} at ${Math.abs(rate) * 100}% per year. Find the population after ${t} years, rounded to the nearest whole number.`;
  const answer = Math.round(val).toString();
  const solution = [`P(t) = ${P0}(1 ${rate > 0 ? "+" : "-"} ${Math.abs(rate)})^t`, `P(${t}) = ${P0}(${1 + rate})^${t} ~ ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const v = Math.round(val);
  return buildMC(prompt, v, (n) => `${Math.round(n)}`, solution, [Math.round(P0 * (1 + rate) * t), Math.round(P0 + rate * t * P0), Math.round(val * (1 + rate))]);
}

/* ========================= UNIT 5: CONIC SECTIONS ========================= */

function parabolas(difficulty, type) {
  const h = randInt(-5, 5), k = randInt(-5, 5);
  const p = randNonZero(-4, 4);
  const coeff = 4 * p;
  const prompt = `A parabola has equation (${xMinus(h)})^2 = ${coeff}(${yMinus(k)}). Find the vertex, focus, and directrix.`;
  const vertex = `(${h}, ${k})`;
  const focus = `(${h}, ${k + p})`;
  const directrix = `y = ${k - p}`;
  const answer = `vertex = ${vertex}, focus = ${focus}, directrix: ${directrix}`;
  const solution = [
    `This is of the form (x-h)^2 = 4p(y-k) with h = ${h}, k = ${k}, and 4p = ${coeff}, so p = ${p}.`,
    `Vertex: (h, k) = ${vertex}`,
    `Focus: (h, k+p) = ${focus}`,
    `Directrix: y = k - p = ${k - p}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `vertex = ${vertex}, focus = (${h}, ${k - p}), directrix: y = ${k + p}`,
    `vertex = (${k}, ${h}), focus = ${focus}, directrix: ${directrix}`,
    `vertex = ${vertex}, focus = (${h + p}, ${k}), directrix: x = ${h - p}`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function ellipses(difficulty, type) {
  const h = randInt(-5, 5), k = randInt(-5, 5);
  const bb = randInt(2, 5);
  const aa = bb + randInt(1, 4);
  const c = round2(Math.sqrt(aa * aa - bb * bb));
  const prompt = `An ellipse has equation (${xMinus(h)})^2/${aa * aa} + (${yMinus(k)})^2/${bb * bb} = 1. Find the center, vertices, and foci.`;
  const center = `(${h}, ${k})`;
  const vertices = `(${h - aa}, ${k}) and (${h + aa}, ${k})`;
  const foci = `(${round2(h - c)}, ${k}) and (${round2(h + c)}, ${k})`;
  const answer = `center = ${center}, vertices = ${vertices}, foci = ${foci}`;
  const solution = [
    `Since ${aa * aa} > ${bb * bb}, the major axis is horizontal: a = ${aa}, b = ${bb}.`,
    `Center: (h, k) = ${center}`,
    `Vertices: (h +/- a, k) = ${vertices}`,
    `c = sqrt(a^2 - b^2) = sqrt(${aa * aa} - ${bb * bb}) = ${c}`,
    `Foci: (h +/- c, k) = ${foci}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const farC = round2(Math.sqrt(aa * aa + bb * bb));
  const distractors = [
    `center = ${center}, vertices = (${h}, ${k - aa}) and (${h}, ${k + aa}), foci = ${foci}`,
    `center = ${center}, vertices = ${vertices}, foci = (${round2(h - farC)}, ${k}) and (${round2(h + farC)}, ${k})`,
    `center = (${k}, ${h}), vertices = ${vertices}, foci = ${foci}`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function hyperbolas(difficulty, type) {
  const h = randInt(-5, 5), k = randInt(-5, 5);
  const aa = randInt(2, 5), bb = randInt(2, 5);
  const c = round2(Math.sqrt(aa * aa + bb * bb));
  const slope = fracStr(bb, aa);
  const prompt = `A hyperbola has equation (${xMinus(h)})^2/${aa * aa} - (${yMinus(k)})^2/${bb * bb} = 1. Find the center, vertices, foci, and equations of the asymptotes.`;
  const center = `(${h}, ${k})`;
  const vertices = `(${h - aa}, ${k}) and (${h + aa}, ${k})`;
  const foci = `(${round2(h - c)}, ${k}) and (${round2(h + c)}, ${k})`;
  const asymptotes = `${yMinus(k)} = ±(${slope})(${xMinus(h)})`;
  const answer = `center = ${center}, vertices = ${vertices}, foci = ${foci}, asymptotes: ${asymptotes}`;
  const solution = [
    `a = ${aa}, b = ${bb}; the transverse axis is horizontal.`,
    `Center: ${center}`,
    `Vertices: (h +/- a, k) = ${vertices}`,
    `c = sqrt(a^2 + b^2) = sqrt(${aa * aa} + ${bb * bb}) = ${c}`,
    `Foci: (h +/- c, k) = ${foci}`,
    `Asymptotes: y - k = +/-(b/a)(x - h) = ${asymptotes}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const nearC = round2(Math.sqrt(Math.abs(aa * aa - bb * bb)));
  const distractors = [
    `center = ${center}, vertices = (${h}, ${k - aa}) and (${h}, ${k + aa}), foci = ${foci}, asymptotes: ${asymptotes}`,
    `center = ${center}, vertices = ${vertices}, foci = (${round2(h - nearC)}, ${k}) and (${round2(h + nearC)}, ${k}), asymptotes: ${asymptotes}`,
    `center = ${center}, vertices = ${vertices}, foci = ${foci}, asymptotes: ${yMinus(k)} = ±(${fracStr(aa, bb)})(${xMinus(h)})`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function classifyConics(difficulty, type) {
  const kind = choice(["circle", "ellipse", "hyperbola", "parabola"]);
  let A, C;
  if (kind === "circle") {
    A = C = randNonZero(1, 4);
  } else if (kind === "ellipse") {
    A = randNonZero(1, 4);
    do {
      C = randNonZero(1, 4);
    } while (C === A);
    if (Math.sign(A) !== Math.sign(C)) C = Math.abs(C) * Math.sign(A);
  } else if (kind === "hyperbola") {
    A = randNonZero(1, 4) * choice([1, -1]);
    C = randNonZero(1, 4) * -Math.sign(A);
  } else {
    if (Math.random() < 0.5) {
      A = randNonZero(1, 4);
      C = 0;
    } else {
      A = 0;
      C = randNonZero(1, 4);
    }
  }
  const D = randInt(-6, 6), E = randInt(-6, 6), F = randInt(-8, 8);
  const terms = [];
  if (A !== 0) terms.push(`${A === 1 ? "" : A}x^2`);
  if (C !== 0) terms.push(`${C > 0 ? "+" : "-"}${Math.abs(C) === 1 ? "" : Math.abs(C)}y^2`);
  if (D !== 0) terms.push(`${D > 0 ? "+" : "-"}${Math.abs(D)}x`);
  if (E !== 0) terms.push(`${E > 0 ? "+" : "-"}${Math.abs(E)}y`);
  if (F !== 0) terms.push(`${F > 0 ? "+" : "-"}${Math.abs(F)}`);
  const eq = terms.join(" ").replace(/^\+/, "");
  const prompt = `Classify the conic section: ${eq} = 0`;
  const answer = kind;
  const solution = [
    A === 0 || C === 0
      ? `Exactly one of the squared terms is present, so this is a parabola.`
      : A === C
      ? `The coefficients of x^2 and y^2 are equal, so this is a circle (a special ellipse).`
      : Math.sign(A) === Math.sign(C)
      ? `The coefficients of x^2 and y^2 have the same sign but different magnitude, so this is an ellipse.`
      : `The coefficients of x^2 and y^2 have opposite signs, so this is a hyperbola.`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const pool = ["circle", "ellipse", "hyperbola", "parabola"];
  return buildMC(prompt, answer, (v) => v, solution, pool.filter((p) => p !== answer));
}

/* ======================= UNIT 6: TRIGONOMETRIC FUNCTIONS ================= */

const NICE_ANGLES_DEG = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360];
const TRIG_TABLE = {
  0: { sin: "0", cos: "1", tan: "0" },
  30: { sin: "1/2", cos: "sqrt(3)/2", tan: "sqrt(3)/3" },
  45: { sin: "sqrt(2)/2", cos: "sqrt(2)/2", tan: "1" },
  60: { sin: "sqrt(3)/2", cos: "1/2", tan: "sqrt(3)" },
  90: { sin: "1", cos: "0", tan: "undefined" },
  120: { sin: "sqrt(3)/2", cos: "-1/2", tan: "-sqrt(3)" },
  135: { sin: "sqrt(2)/2", cos: "-sqrt(2)/2", tan: "-1" },
  150: { sin: "1/2", cos: "-sqrt(3)/2", tan: "-sqrt(3)/3" },
  180: { sin: "0", cos: "-1", tan: "0" },
  210: { sin: "-1/2", cos: "-sqrt(3)/2", tan: "sqrt(3)/3" },
  225: { sin: "-sqrt(2)/2", cos: "-sqrt(2)/2", tan: "1" },
  240: { sin: "-sqrt(3)/2", cos: "-1/2", tan: "sqrt(3)" },
  270: { sin: "-1", cos: "0", tan: "undefined" },
  300: { sin: "-sqrt(3)/2", cos: "1/2", tan: "-sqrt(3)" },
  315: { sin: "-sqrt(2)/2", cos: "sqrt(2)/2", tan: "-1" },
  330: { sin: "-1/2", cos: "sqrt(3)/2", tan: "-sqrt(3)/3" },
  360: { sin: "0", cos: "1", tan: "0" },
};

function trigValues(difficulty, type) {
  const angles = difficulty === 1 ? [0, 30, 45, 60, 90, 180, 270, 360] : NICE_ANGLES_DEG;
  const deg = choice(angles);
  const func = choice(["sin", "cos", "tan"]);
  const prompt = `Evaluate exactly: ${func}(${deg} deg)`;
  const answer = TRIG_TABLE[deg][func];
  const solution = [`${deg} deg is a standard unit-circle angle.`, `${func}(${deg} deg) = ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const otherFuncsVals = ["sin", "cos", "tan"].map((f) => TRIG_TABLE[deg][f]).filter((v) => v !== answer);
  const neighborDeg = choice(angles.filter((a) => a !== deg));
  const distractors = [...otherFuncsVals, TRIG_TABLE[neighborDeg][func]];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function reciprocalTrig(difficulty, type) {
  const angles = [0, 30, 45, 60, 120, 135, 150, 180, 210, 225, 240, 300, 315, 330];
  const deg = choice(angles.filter((a) => TRIG_TABLE[a].sin !== "0" && TRIG_TABLE[a].cos !== "0"));
  const func = choice(["sec", "csc", "cot"]);
  const recipOf = { sec: "cos", csc: "sin", cot: "tan" };
  const base = TRIG_TABLE[deg][recipOf[func]];
  const RECIP_MAP = {
    "1": "1", "-1": "-1",
    "1/2": "2", "-1/2": "-2",
    "sqrt(2)/2": "sqrt(2)", "-sqrt(2)/2": "-sqrt(2)",
    "sqrt(3)/2": "2sqrt(3)/3", "-sqrt(3)/2": "-2sqrt(3)/3",
    "sqrt(3)": "sqrt(3)/3", "-sqrt(3)": "-sqrt(3)/3",
    "sqrt(3)/3": "sqrt(3)", "-sqrt(3)/3": "-sqrt(3)",
  };
  const answer = RECIP_MAP[base] ?? `1/(${base})`;
  const prompt = `Evaluate exactly: ${func}(${deg} deg)`;
  const solution = [`${func} is the reciprocal of ${recipOf[func]}.`, `${recipOf[func]}(${deg} deg) = ${base}`, `${func}(${deg} deg) = 1/(${base}) = ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, answer, (v) => v, solution, [base, `-${answer}`, TRIG_TABLE[deg][recipOf[func] === "cos" ? "sin" : "cos"]]);
}

function trigValuesReciprocal(difficulty, type) {
  return Math.random() < 0.6 ? trigValues(difficulty, type) : reciprocalTrig(difficulty, type);
}

function expressTrigUsingOthers(difficulty, type) {
  const triples = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25]];
  const [o, a, h] = choice(triples);
  const givenSin = Math.random() < 0.5;
  const quadrant = choice([1, 2, 3, 4]);
  const sinSign = quadrant === 1 || quadrant === 2 ? 1 : -1;
  const cosSign = quadrant === 1 || quadrant === 4 ? 1 : -1;
  const tanSign = sinSign * cosSign;
  const sinVal = `${sinSign < 0 ? "-" : ""}${o}/${h}`;
  const cosVal = `${cosSign < 0 ? "-" : ""}${a}/${h}`;
  const tanVal = `${tanSign < 0 ? "-" : ""}${o}/${a}`;
  const findTan = difficulty >= 2 && Math.random() < 0.5;
  let prompt, answer, solution;
  if (givenSin) {
    prompt = `Given sin(theta) = ${sinVal} and theta is in Quadrant ${quadrant}, find ${findTan ? "tan(theta)" : "cos(theta)"}.`;
    answer = findTan ? tanVal : cosVal;
    solution = [
      `Use sin^2(theta) + cos^2(theta) = 1 with the ${o}-${a}-${h} triple.`,
      `In Quadrant ${quadrant}, cos(theta) is ${cosSign < 0 ? "negative" : "positive"}${findTan ? ` and tan(theta) is ${tanSign < 0 ? "negative" : "positive"}` : ""}.`,
      `${findTan ? "tan(theta)" : "cos(theta)"} = ${answer}`,
    ];
  } else {
    prompt = `Given cos(theta) = ${cosVal} and theta is in Quadrant ${quadrant}, find ${findTan ? "tan(theta)" : "sin(theta)"}.`;
    answer = findTan ? tanVal : sinVal;
    solution = [
      `Use sin^2(theta) + cos^2(theta) = 1 with the ${o}-${a}-${h} triple.`,
      `In Quadrant ${quadrant}, sin(theta) is ${sinSign < 0 ? "negative" : "positive"}${findTan ? ` and tan(theta) is ${tanSign < 0 ? "negative" : "positive"}` : ""}.`,
      `${findTan ? "tan(theta)" : "sin(theta)"} = ${answer}`,
    ];
  }
  if (type === "fr") return buildFR(prompt, answer, solution);
  const flipSign = answer.startsWith("-") ? answer.slice(1) : `-${answer}`;
  return buildMC(prompt, answer, (v) => v, solution, [flipSign, sinVal === answer ? cosVal : sinVal, tanVal === answer ? sinVal : tanVal]);
}

function trigGraphs(difficulty, type) {
  const a = randInt(1, 5 + difficulty);
  const b = choice([1, 2, 3, 0.5]);
  const d = randInt(-5, 5);
  const func = choice(["sin", "cos"]);
  const prompt = `For y = ${a}${func}(${b}x) ${d >= 0 ? "+" : "-"} ${Math.abs(d)}, find the amplitude, period, and midline.`;
  const answer = `amplitude = ${a}, period = ${b === 1 ? "2pi" : `2pi/${b}`}, midline y = ${d}`;
  const solution = [`Amplitude = |a| = ${a}`, `Period = 2pi / |b| = 2pi / ${b}`, `Midline: y = d = ${d}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `amplitude = ${a}, period = ${b}pi, midline y = ${d}`,
    `amplitude = ${b}, period = 2pi/${a}, midline y = ${d}`,
    `amplitude = ${a}, period = ${b === 1 ? "2pi" : `2pi/${b}`}, midline y = ${-d}`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function tanSecCscCotGraphs(difficulty, type) {
  const func = choice(["tan", "cot", "sec", "csc"]);
  const a = randInt(1, 4);
  const b = choice([1, 2, 3]);
  const isTanCot = func === "tan" || func === "cot";
  const periodStr = isTanCot ? (b === 1 ? "pi" : `pi/${b}`) : b === 1 ? "2pi" : `2pi/${b}`;
  let firstAsymptote;
  if (func === "tan" || func === "sec") firstAsymptote = b === 1 ? "x = pi/2" : `x = pi/${2 * b}`;
  else firstAsymptote = b === 1 ? "x = pi" : `x = pi/${b}`;
  const prompt = `For y = ${a}${func}(${b === 1 ? "x" : `${b}x`}), find the period and the first positive vertical asymptote.`;
  const answer = `period = ${periodStr}, first positive asymptote: ${firstAsymptote}`;
  const solution = [
    isTanCot
      ? `${func}(theta) has period pi, so ${func}(${b === 1 ? "x" : `${b}x`}) has period pi/${b}${b === 1 ? " = pi" : ""}.`
      : `${func}(theta) has period 2pi, so ${func}(${b === 1 ? "x" : `${b}x`}) has period 2pi/${b}${b === 1 ? " = 2pi" : ""}.`,
    `Vertical asymptotes occur where ${func === "tan" || func === "sec" ? "cos" : "sin"}(${b === 1 ? "x" : `${b}x`}) = 0.`,
    `The first positive one is ${firstAsymptote}.`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `period = ${periodStr}, first positive asymptote: x = ${b === 1 ? "pi" : `${b}pi`}`,
    `period = ${b === 1 ? "2pi" : `2pi/${b}`}, first positive asymptote: ${firstAsymptote}`,
    `period = ${periodStr}, first positive asymptote: x = 0`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function inverseTrig(difficulty, type) {
  const table = [
    { func: "arcsin", x: "1/2", ans: "30 deg" },
    { func: "arcsin", x: "sqrt(2)/2", ans: "45 deg" },
    { func: "arcsin", x: "sqrt(3)/2", ans: "60 deg" },
    { func: "arccos", x: "1/2", ans: "60 deg" },
    { func: "arccos", x: "sqrt(2)/2", ans: "45 deg" },
    { func: "arccos", x: "sqrt(3)/2", ans: "30 deg" },
    { func: "arctan", x: "1", ans: "45 deg" },
    { func: "arctan", x: "sqrt(3)", ans: "60 deg" },
    { func: "arctan", x: "sqrt(3)/3", ans: "30 deg" },
  ];
  const item = choice(table);
  const prompt = `Evaluate: ${item.func}(${item.x})`;
  const answer = item.ans;
  const solution = [`This asks for the angle in the range of ${item.func} whose ${item.func === "arcsin" ? "sine" : item.func === "arccos" ? "cosine" : "tangent"} is ${item.x}.`, `Answer: ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = table.filter((t) => t.ans !== answer).map((t) => t.ans);
  return buildMC(prompt, answer, (v) => v, solution, shuffle(distractors));
}

function rightTriangleTrig(difficulty, type) {
  const angleDeg = choice([20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]);
  const side = randInt(5, 20);
  const findFunc = choice(["sin", "cos", "tan"]);
  const rad = (angleDeg * Math.PI) / 180;
  let prompt, answer, solution, unknownVal;
  if (findFunc === "tan") {
    unknownVal = round2(side * Math.tan(rad));
    prompt = `In a right triangle, one acute angle measures ${angleDeg} deg and the side adjacent to it has length ${side}. Find the length of the side opposite this angle, rounded to 2 decimals.`;
    solution = [`tan(${angleDeg} deg) = opposite / adjacent`, `opposite = ${side} * tan(${angleDeg} deg) ~ ${unknownVal}`];
  } else if (findFunc === "sin") {
    unknownVal = round2(side * Math.sin(rad));
    prompt = `In a right triangle, one acute angle measures ${angleDeg} deg and the hypotenuse has length ${side}. Find the length of the side opposite this angle, rounded to 2 decimals.`;
    solution = [`sin(${angleDeg} deg) = opposite / hypotenuse`, `opposite = ${side} * sin(${angleDeg} deg) ~ ${unknownVal}`];
  } else {
    unknownVal = round2(side * Math.cos(rad));
    prompt = `In a right triangle, one acute angle measures ${angleDeg} deg and the hypotenuse has length ${side}. Find the length of the side adjacent to this angle, rounded to 2 decimals.`;
    solution = [`cos(${angleDeg} deg) = adjacent / hypotenuse`, `adjacent = ${side} * cos(${angleDeg} deg) ~ ${unknownVal}`];
  }
  answer = `${unknownVal}`;
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, unknownVal, fmtNum, solution, [round2(unknownVal + 1), round2(unknownVal - 1), round2(side - unknownVal)]);
}

/* ======================= UNIT 7: ANALYTIC TRIGONOMETRY ==================== */

function trigIdentities(difficulty, type) {
  const identities = [
    { lhs: "sin^2(theta) + cos^2(theta)", rhs: "1" },
    { lhs: "1 + tan^2(theta)", rhs: "sec^2(theta)" },
    { lhs: "1 + cot^2(theta)", rhs: "csc^2(theta)" },
    { lhs: "sin(theta)/cos(theta)", rhs: "tan(theta)" },
    { lhs: "sin(-theta)", rhs: "-sin(theta)" },
    { lhs: "cos(-theta)", rhs: "cos(theta)" },
  ];
  const item = choice(identities);
  const prompt = `Which expression is equivalent to ${item.lhs}?`;
  const answer = item.rhs;
  const solution = [`This is a standard Pythagorean/reciprocal/odd-even identity: ${item.lhs} = ${item.rhs}.`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const others = identities.filter((i) => i.rhs !== answer).map((i) => i.rhs);
  const choices = shuffle([answer, ...shuffle(others).slice(0, 3)]);
  return { type: "mc", prompt, choices, correctIndex: choices.indexOf(answer), answer, solution };
}

function sumDifferenceFormulas(difficulty, type) {
  const useSum = Math.random() < 0.5;
  const func = choice(["sin", "cos"]);
  const resultDeg = useSum ? 75 : 15;
  const EXACT = {
    75: { sin: "(sqrt(6)+sqrt(2))/4", cos: "(sqrt(6)-sqrt(2))/4" },
    15: { sin: "(sqrt(6)-sqrt(2))/4", cos: "(sqrt(6)+sqrt(2))/4" },
  };
  const answer = EXACT[resultDeg][func];
  const prompt = `Use a sum or difference formula to find the exact value of ${func}(${resultDeg} deg). (Hint: ${resultDeg} = 45 ${useSum ? "+" : "-"} 30)`;
  const formulaName =
    func === "sin"
      ? useSum
        ? "sin(A+B) = sinA cosB + cosA sinB"
        : "sin(A-B) = sinA cosB - cosA sinB"
      : useSum
      ? "cos(A+B) = cosA cosB - sinA sinB"
      : "cos(A-B) = cosA cosB + sinA sinB";
  const solution = [
    `${resultDeg} deg = 45 deg ${useSum ? "+" : "-"} 30 deg`,
    formulaName,
    `Substituting sin45 = sqrt(2)/2, cos45 = sqrt(2)/2, sin30 = 1/2, cos30 = sqrt(3)/2 gives ${func}(${resultDeg} deg) = ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const otherFunc = func === "sin" ? "cos" : "sin";
  const otherDeg = resultDeg === 75 ? 15 : 75;
  const distractors = [EXACT[resultDeg][otherFunc], EXACT[otherDeg][func], EXACT[otherDeg][otherFunc]];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function doubleHalfAngle(difficulty, type) {
  const triples = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25]];
  const [o, a, h] = choice(triples);
  const quadrant = choice([1, 2, 3, 4]);
  const sinSign = quadrant === 1 || quadrant === 2 ? 1 : -1;
  const cosSign = quadrant === 1 || quadrant === 4 ? 1 : -1;
  const useSin2 = Math.random() < 0.5;
  const prompt = `Given sin(theta) = ${sinSign < 0 ? "-" : ""}${o}/${h} and theta is in Quadrant ${quadrant}, find ${useSin2 ? "sin(2theta)" : "cos(2theta)"}.`;
  let answer, solution, distractors;
  if (useSin2) {
    const num = 2 * sinSign * cosSign * o * a;
    const den = h * h;
    answer = fracStr(num, den);
    solution = [
      `cos(theta) = ${cosSign < 0 ? "-" : ""}${a}/${h} (Quadrant ${quadrant})`,
      `sin(2theta) = 2 sin(theta) cos(theta) = 2(${sinSign < 0 ? "-" : ""}${o}/${h})(${cosSign < 0 ? "-" : ""}${a}/${h})`,
      `= ${answer}`,
    ];
    distractors = [fracStr(a * a - o * o, h * h), fracStr(o * o, h * h)];
  } else {
    const num = a * a - o * o;
    const den = h * h;
    answer = fracStr(num, den);
    solution = [`cos(2theta) = cos^2(theta) - sin^2(theta) = (${a}^2 - ${o}^2)/${h}^2`, `= ${answer}`];
    distractors = [fracStr(2 * o * a, h * h), fracStr(o * o, h * h)];
  }
  const flip = answer.startsWith("-") ? answer.slice(1) : `-${answer}`;
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, answer, (v) => v, solution, [flip, ...distractors]);
}

function trigEquations(difficulty, type) {
  const func = choice(["sin", "cos"]);
  const val = choice(["1/2", "sqrt(2)/2", "sqrt(3)/2", "-1/2", "-sqrt(2)/2"]);
  const solutionsByFunc = {
    sin: { "1/2": [30, 150], "sqrt(2)/2": [45, 135], "sqrt(3)/2": [60, 120], "-1/2": [210, 330], "-sqrt(2)/2": [225, 315] },
    cos: { "1/2": [60, 300], "sqrt(2)/2": [45, 315], "sqrt(3)/2": [30, 330], "-1/2": [120, 240], "-sqrt(2)/2": [135, 225] },
  };
  const sols = solutionsByFunc[func][val];
  const prompt = `Solve on the interval [0 deg, 360 deg): ${func}(theta) = ${val}`;
  const answer = sols.map((d) => `${d} deg`).join(", ");
  const solution = [`${val} is a standard value of ${func}.`, `Reference angle and quadrant analysis give theta = ${answer}.`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [sols.map((d) => `${360 - d} deg`).join(", "), sols.map((d) => `${d + 10} deg`).join(", "), `${sols[0]} deg`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function harmonicMotion(difficulty, type) {
  const A = randNonZero(-8, 8);
  const B = randNonZero(-8, 8);
  const R = round2(Math.sqrt(A * A + B * B));
  const phiDeg = round2((Math.atan2(B, A) * 180) / Math.PI);
  const prompt = `Write ${A}sin(x) + ${B}cos(x) in the form R sin(x + phi). Find R (rounded to 2 decimals) and phi in degrees (rounded to 1 decimal).`;
  const answer = `R = ${R}, phi = ${phiDeg} deg`;
  const solution = [`R = sqrt(A^2 + B^2) = sqrt(${A}^2 + ${B}^2) = ${R}`, `phi = arctan(B/A), adjusted for the quadrant of (A, B) ~ ${phiDeg} deg`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, answer, (v) => v, solution, [
    `R = ${R}, phi = ${round2(-phiDeg)} deg`,
    `R = ${round2(Math.abs(A) + Math.abs(B))}, phi = ${phiDeg} deg`,
    `R = ${R}, phi = ${round2(90 - phiDeg)} deg`,
  ]);
}

/* ================ UNIT 8: ADDITIONAL TOPICS OF TRIGONOMETRY =============== */

function lawOfSines(difficulty, type) {
  const ambiguous = difficulty >= 2 && Math.random() < 0.4;
  if (!ambiguous) {
    const A = choice([30, 40, 50, 60, 70, 80, 100, 110, 120]);
    const B = choice([20, 30, 40, 50, 60].filter((x) => x + A < 180));
    const a = randInt(8, 25);
    const bVal = round2((a * Math.sin((B * Math.PI) / 180)) / Math.sin((A * Math.PI) / 180));
    const prompt = `In triangle ABC, angle A = ${A} deg, angle B = ${B} deg, and side a = ${a}. Find side b, rounded to 2 decimals.`;
    const answer = `${bVal}`;
    const solution = [`Law of Sines: a/sin(A) = b/sin(B)`, `b = a*sin(B)/sin(A) = ${a}*sin(${B} deg)/sin(${A} deg) ~ ${bVal}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, bVal, fmtNum, solution, [
      round2(bVal + 1),
      round2(bVal - 1),
      round2((a * Math.sin((A * Math.PI) / 180)) / Math.sin((B * Math.PI) / 180)),
    ]);
  } else {
    const A = choice([25, 30, 35, 40, 45, 50]);
    const b = randInt(10, 20);
    const h = round2(b * Math.sin((A * Math.PI) / 180));
    const outcome = choice(["none", "one-right", "two", "one-large"]);
    let a;
    if (outcome === "none") a = round2(h - randInt(1, 3));
    else if (outcome === "one-right") a = h;
    else if (outcome === "two") a = round2(h + randInt(1, Math.max(1, Math.floor((b - h) / 2))));
    else a = round2(b + randInt(1, 5));
    const prompt = `In triangle ABC, angle A = ${A} deg, side a = ${a}, and side b = ${b}. How many distinct triangles satisfy these conditions?`;
    let answer, reason;
    if (a < h) {
      answer = "0 (no triangle)";
      reason = `a (${a}) < b*sin(A) (${h}), so no triangle exists.`;
    } else if (a === h) {
      answer = "1 (a right triangle)";
      reason = `a (${a}) = b*sin(A) (${h}), so exactly one right triangle exists.`;
    } else if (a < b) {
      answer = "2 (the ambiguous case)";
      reason = `b*sin(A) (${h}) < a (${a}) < b (${b}), so two distinct triangles exist.`;
    } else {
      answer = "1";
      reason = `a (${a}) >= b (${b}), so exactly one triangle exists.`;
    }
    const solution = [`h = b*sin(A) = ${b}*sin(${A} deg) = ${h}`, reason];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const pool = ["0 (no triangle)", "1 (a right triangle)", "2 (the ambiguous case)", "1"];
    return buildMC(prompt, answer, (v) => v, solution, pool.filter((p) => p !== answer));
  }
}

function lawOfCosines(difficulty, type) {
  const a = randInt(5, 20), b = randInt(5, 20);
  const C = choice([40, 50, 60, 70, 80, 100, 110, 120, 130]);
  const c = round2(Math.sqrt(a * a + b * b - 2 * a * b * Math.cos((C * Math.PI) / 180)));
  const prompt = `In triangle ABC, side a = ${a}, side b = ${b}, and the included angle C = ${C} deg. Find side c, rounded to 2 decimals.`;
  const answer = `${c}`;
  const solution = [`Law of Cosines: c^2 = a^2 + b^2 - 2ab*cos(C)`, `c^2 = ${a}^2 + ${b}^2 - 2(${a})(${b})cos(${C} deg)`, `c ~ ${c}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, c, fmtNum, solution, [round2(c + 1), round2(c - 1), round2(Math.sqrt(a * a + b * b))]);
}

function heronsFormula(difficulty, type) {
  let a, b, c;
  do {
    a = randInt(5, 15);
    b = randInt(5, 15);
    c = randInt(5, 15);
  } while (a + b <= c || a + c <= b || b + c <= a);
  const s = (a + b + c) / 2;
  const area = round2(Math.sqrt(s * (s - a) * (s - b) * (s - c)));
  const prompt = `A triangle has sides a = ${a}, b = ${b}, c = ${c}. Use Heron's Formula to find its area, rounded to 2 decimals.`;
  const answer = `${area}`;
  const solution = [`s = (a+b+c)/2 = (${a}+${b}+${c})/2 = ${s}`, `Area = sqrt(s(s-a)(s-b)(s-c)) = sqrt(${s}(${s - a})(${s - b})(${s - c})) ~ ${area}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, area, fmtNum, solution, [round2(area + 2), round2(area - 2), round2(s)]);
}

function trigFormComplex(difficulty, type) {
  const examples = [
    { aStr: "1", bStr: "sqrt(3)", rStr: "2", deg: 60 },
    { aStr: "sqrt(3)", bStr: "1", rStr: "2", deg: 30 },
    { aStr: "-1", bStr: "sqrt(3)", rStr: "2", deg: 120 },
    { aStr: "1", bStr: "1", rStr: "sqrt(2)", deg: 45 },
    { aStr: "-1", bStr: "1", rStr: "sqrt(2)", deg: 135 },
    { aStr: "-sqrt(3)", bStr: "1", rStr: "2", deg: 150 },
    { aStr: "-1", bStr: "-1", rStr: "sqrt(2)", deg: 225 },
    { aStr: "1", bStr: "-1", rStr: "sqrt(2)", deg: 315 },
  ];
  const ex = choice(examples);
  const prompt = `Write z = ${ex.aStr} + ${ex.bStr}i in trigonometric (polar) form, r(cos theta + i sin theta).`;
  const answer = `${ex.rStr}(cos(${ex.deg} deg) + i sin(${ex.deg} deg))`;
  const solution = [`r = sqrt(a^2 + b^2) = ${ex.rStr}`, `theta = reference angle from (a, b) = ${ex.deg} deg`, `z = ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const others = examples.filter((e) => e !== ex);
  const distractors = shuffle(others)
    .slice(0, 3)
    .map((e) => `${ex.rStr}(cos(${e.deg} deg) + i sin(${e.deg} deg))`);
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function deMoivresTheorem(difficulty, type) {
  const r = choice([1, 2, 3]);
  const deg = choice([15, 30, 36, 45, 60, 90]);
  const n = difficulty === 1 ? randInt(2, 3) : randInt(2, 5);
  const resultDeg = (deg * n) % 360;
  const resultR = Math.pow(r, n);
  const prompt = `Let z = ${r}(cos(${deg} deg) + i sin(${deg} deg)). Use De Moivre's Theorem to find z^${n}.`;
  const answer = `${resultR}(cos(${resultDeg} deg) + i sin(${resultDeg} deg))`;
  const solution = [
    `De Moivre's Theorem: z^n = r^n (cos(n*theta) + i sin(n*theta))`,
    `r^${n} = ${r}^${n} = ${resultR}`,
    `n*theta = ${n}*${deg} deg = ${deg * n} deg, coterminal with ${resultDeg} deg`,
    `z^${n} = ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const flipDeg = (360 - resultDeg) % 360;
  const distractors = [
    `${r * n}(cos(${resultDeg} deg) + i sin(${resultDeg} deg))`,
    `${resultR}(cos(${deg} deg) + i sin(${deg} deg))`,
    `${resultR}(cos(${flipDeg} deg) + i sin(${flipDeg} deg))`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function rootsOfComplex(difficulty, type) {
  const examples = [
    { r: 8, deg: 90, n: 3 },
    { r: 16, deg: 60, n: 4 },
    { r: 4, deg: 180, n: 2 },
    { r: 27, deg: 270, n: 3 },
  ];
  const ex = choice(examples);
  const rootR = Math.round(Math.pow(ex.r, 1 / ex.n) * 1000) / 1000;
  const rootDeg = round2(ex.deg / ex.n);
  const prompt = `Find the principal nth root (k = 0) of z = ${ex.r}(cos(${ex.deg} deg) + i sin(${ex.deg} deg)), where n = ${ex.n}.`;
  const answer = `${fmtNum(rootR)}(cos(${rootDeg} deg) + i sin(${rootDeg} deg))`;
  const solution = [
    `The nth roots of r(cos theta + i sin theta) are r^(1/n)(cos((theta + 360k)/n) + i sin((theta + 360k)/n)) for k = 0, 1, ..., n-1.`,
    `r^(1/${ex.n}) = ${ex.r}^(1/${ex.n}) = ${fmtNum(rootR)}`,
    `For k = 0: angle = ${ex.deg}/${ex.n} = ${rootDeg} deg`,
    `Principal root: ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `${fmtNum(rootR)}(cos(${round2(ex.deg)} deg) + i sin(${round2(ex.deg)} deg))`,
    `${fmtNum(ex.r)}(cos(${rootDeg} deg) + i sin(${rootDeg} deg))`,
    `${fmtNum(rootR)}(cos(${round2(rootDeg + 360 / ex.n)} deg) + i sin(${round2(rootDeg + 360 / ex.n)} deg))`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

/* ============ UNIT 9: PARAMETRIC EQUATIONS AND POLAR COORDINATES ========= */

function parametricFunctions(difficulty, type) {
  const ax = randNonZero(-4, 4);
  const bx = randInt(-6, 6);
  const ay = randNonZero(-4, 4);
  const by = randInt(-6, 6);
  const t0 = randInt(-3, 3);
  const xt = `${ax}t ${bx >= 0 ? "+" : "-"} ${Math.abs(bx)}`;
  const yt = `${ay}t ${by >= 0 ? "+" : "-"} ${Math.abs(by)}`;
  const xVal = ax * t0 + bx;
  const yVal = ay * t0 + by;
  const prompt = `A curve is defined parametrically by x(t) = ${xt}, y(t) = ${yt}. Find the point (x, y) when t = ${t0}.`;
  const answer = `(${xVal}, ${yVal})`;
  const solution = [`x(${t0}) = ${ax}(${t0}) ${bx >= 0 ? "+" : "-"} ${Math.abs(bx)} = ${xVal}`, `y(${t0}) = ${ay}(${t0}) ${by >= 0 ? "+" : "-"} ${Math.abs(by)} = ${yVal}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, answer, (v) => v, solution, [`(${yVal}, ${xVal})`, `(${xVal + 1}, ${yVal})`, `(${xVal}, ${yVal + 1})`]);
}

function parametricMotion(difficulty, type) {
  const x0 = randInt(-5, 5), y0 = randInt(-5, 5);
  const vx = randNonZero(-6, 6), vy = randNonZero(-6, 6);
  const t1 = randInt(0, 2), t2 = t1 + randInt(1, 3 + difficulty);
  const pos = (t) => [x0 + vx * t, y0 + vy * t];
  const [x1, y1] = pos(t1);
  const [x2, y2] = pos(t2);
  const dist = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
  const speed = round2(dist / (t2 - t1));
  const prompt = `An object's position is given by x(t) = ${x0} ${vx >= 0 ? "+" : "-"} ${Math.abs(vx)}t, y(t) = ${y0} ${vy >= 0 ? "+" : "-"} ${Math.abs(vy)}t (position in meters, t in seconds). Find the object's average speed between t = ${t1} and t = ${t2}, rounded to 2 decimals.`;
  const answer = `${speed} m/s`;
  const solution = [
    `Position at t=${t1}: (${x1}, ${y1}); position at t=${t2}: (${x2}, ${y2})`,
    `Distance = sqrt((${x2}-${x1})^2 + (${y2}-${y1})^2) ~ ${round2(dist)}`,
    `Average speed = distance / time = ${round2(dist)} / ${t2 - t1} ~ ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, speed, (v) => `${v} m/s`, solution, [round2(speed + 1), round2(speed - 1), round2(dist)]);
}

function eliminateParameter(difficulty, type) {
  const a = randNonZero(-4, 4), b = randInt(-6, 6);
  const c = randNonZero(-4, 4), d = randInt(-6, 6);
  const prompt = `A curve is defined parametrically by x(t) = ${a}t ${b >= 0 ? "+" : "-"} ${Math.abs(b)}, y(t) = ${c}t ${d >= 0 ? "+" : "-"} ${Math.abs(d)}. Eliminate the parameter to write y as a function of x.`;
  const slope = fracStr(c, a);
  const intercept = fracStr(a * d - c * b, a);
  const answer = `y = (${slope})x + (${intercept})`;
  const solution = [
    `Solve x(t) for t: t = (${xMinus(b)}) / ${a}`,
    `Substitute into y(t) = ${c}t ${d >= 0 ? "+" : "-"} ${Math.abs(d)}.`,
    `Simplify: ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `y = (${fracStr(a, c)})x + (${intercept})`,
    `y = (${slope})x + (${fracStr(c * b - a * d, a)})`,
    `y = (${fracStr(-c, a)})x + (${intercept})`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function parametricCurves(difficulty, type) {
  const r = Math.random();
  if (r < 0.4) return eliminateParameter(difficulty, type);
  if (r < 0.7) return parametricFunctions(difficulty, type);
  return parametricMotion(difficulty, type);
}

function parametricCirclesLines(difficulty, type) {
  const wantLine = Math.random() < 0.5;
  if (!wantLine) {
    const r = randInt(2, 8), h = randInt(-5, 5), k = randInt(-5, 5);
    const prompt = `Write parametric equations for a circle of radius ${r} centered at (${h}, ${k}), using parameter t in [0, 2pi).`;
    const answer = `x(t) = ${h} + ${r}cos(t), y(t) = ${k} + ${r}sin(t)`;
    const solution = [`A circle of radius r centered at (h, k) is x(t) = h + r*cos(t), y(t) = k + r*sin(t).`, `Substitute h = ${h}, k = ${k}, r = ${r}: ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [
      `x(t) = ${r} + ${h}cos(t), y(t) = ${r} + ${k}sin(t)`,
      `x(t) = ${h} + ${r}sin(t), y(t) = ${k} + ${r}cos(t)`,
      `x(t) = ${h} + ${r}t, y(t) = ${k} + ${r}t`,
    ];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  } else {
    const x0 = randInt(-6, 6), y0 = randInt(-6, 6);
    const dx = randNonZero(-5, 5), dy = randNonZero(-5, 5);
    const prompt = `Write parametric equations for the line through (${x0}, ${y0}) with direction vector <${dx}, ${dy}>.`;
    const answer = `x(t) = ${x0} ${dx >= 0 ? "+" : "-"} ${Math.abs(dx)}t, y(t) = ${y0} ${dy >= 0 ? "+" : "-"} ${Math.abs(dy)}t`;
    const solution = [`A line through (x0, y0) with direction <dx, dy> is x(t) = x0 + dx*t, y(t) = y0 + dy*t.`, `Substitute: ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [
      `x(t) = ${y0} ${dx >= 0 ? "+" : "-"} ${Math.abs(dx)}t, y(t) = ${x0} ${dy >= 0 ? "+" : "-"} ${Math.abs(dy)}t`,
      `x(t) = ${x0} ${dy >= 0 ? "+" : "-"} ${Math.abs(dy)}t, y(t) = ${y0} ${dx >= 0 ? "+" : "-"} ${Math.abs(dx)}t`,
      `x(t) = ${x0} ${dx >= 0 ? "+" : "-"} ${Math.abs(dx)}t^2, y(t) = ${y0} ${dy >= 0 ? "+" : "-"} ${Math.abs(dy)}t^2`,
    ];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  }
}

function polarCoordinates(difficulty, type) {
  const toRect = Math.random() < 0.5;
  if (toRect) {
    const r = randInt(2, 10);
    const deg = choice([0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]);
    const cosv = TRIG_TABLE[deg].cos;
    const sinv = TRIG_TABLE[deg].sin;
    const prompt = `Convert the polar point (r, theta) = (${r}, ${deg} deg) to rectangular coordinates.`;
    const answer = `(${r}*(${cosv}), ${r}*(${sinv}))`;
    const solution = [`x = r*cos(theta) = ${r}*(${cosv})`, `y = r*sin(theta) = ${r}*(${sinv})`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [`(${r}*(${sinv}), ${r}*(${cosv}))`, `(${r}, ${deg})`, `(-${r}*(${cosv}), ${r}*(${sinv}))`];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  } else {
    const x = choice([3, 4, 6, 8, 5]);
    const y = choice([4, 3, 8, 6, 12]);
    const r = round2(Math.sqrt(x * x + y * y));
    const prompt = `Convert the rectangular point (x, y) = (${x}, ${y}) to polar coordinates. Give r (exact or rounded to 2 decimals) and theta in degrees (rounded to 1 decimal).`;
    const thetaDeg = round2((Math.atan2(y, x) * 180) / Math.PI);
    const answer = `r = ${r}, theta ~ ${thetaDeg} deg`;
    const solution = [`r = sqrt(x^2 + y^2) = sqrt(${x}^2 + ${y}^2) = ${r}`, `theta = arctan(y/x) = arctan(${y}/${x}) ~ ${thetaDeg} deg`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [`r = ${r}, theta ~ ${round2(90 - thetaDeg)} deg`, `r = ${x + y}, theta ~ ${thetaDeg} deg`, `r = ${r}, theta ~ ${round2(thetaDeg + 90)} deg`];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  }
}

function polarGraphs(difficulty, type) {
  const shapes = [
    { eq: "r = a", answer: "a circle centered at the pole with radius a" },
    { eq: "r = a*cos(theta)", answer: "a circle through the pole, centered on the x-axis" },
    { eq: "r = a*sin(theta)", answer: "a circle through the pole, centered on the y-axis" },
    { eq: "r = a + b*cos(theta), with a = b", answer: "a cardioid" },
    { eq: "r = a*cos(k*theta), k an integer >= 2", answer: "a rose curve" },
    { eq: "r = a + b*cos(theta), with a > b > 0", answer: "a limacon without an inner loop" },
    { eq: "r = ed / (1 + e*cos(theta)), with e = 1", answer: "a parabola (a conic in polar form)" },
  ];
  const item = choice(shapes);
  const prompt = `Identify the type of polar curve described by ${item.eq} (a, b, d > 0 constants).`;
  const answer = item.answer;
  const solution = [`This is the standard classification for a polar equation of the form ${item.eq}.`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const others = shapes.filter((s) => s.answer !== answer).map((s) => s.answer);
  const choices = shuffle([answer, ...shuffle(others).slice(0, 3)]);
  return { type: "mc", prompt, choices, correctIndex: choices.indexOf(answer), answer, solution };
}

/* ========================= UNIT 10: VECTORS AND MATRICES ================= */

function vectors(difficulty, type) {
  const op = choice(["magnitude", "sum", "scalar"]);
  const vx = randNonZero(-8, 8);
  const vy = randNonZero(-8, 8);
  if (op === "magnitude") {
    const mag = round2(Math.sqrt(vx * vx + vy * vy));
    const prompt = `Find the magnitude of vector v = <${vx}, ${vy}>, rounded to 2 decimals.`;
    const answer = `${mag}`;
    const solution = [`|v| = sqrt(${vx}^2 + ${vy}^2) = sqrt(${vx * vx + vy * vy}) ~ ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, mag, fmtNum, solution, [Math.abs(vx) + Math.abs(vy), round2(mag + 1), round2(mag - 1)]);
  } else if (op === "sum") {
    const wx = randNonZero(-8, 8);
    const wy = randNonZero(-8, 8);
    const prompt = `Let v = <${vx}, ${vy}> and w = <${wx}, ${wy}>. Find v + w.`;
    const answer = `<${vx + wx}, ${vy + wy}>`;
    const solution = [`v + w = <${vx} + ${wx}, ${vy} + ${wy}> = ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [`<${vx - wx}, ${vy - wy}>`, `<${vx * wx}, ${vy * wy}>`, `<${wx - vx}, ${wy - vy}>`];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  } else {
    const k = randNonZero(-4, 4);
    const prompt = `Let v = <${vx}, ${vy}>. Find ${k}v.`;
    const answer = `<${k * vx}, ${k * vy}>`;
    const solution = [`${k}v = <${k}*${vx}, ${k}*${vy}> = ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [`<${k + vx}, ${k + vy}>`, `<${vx}, ${vy}>`, `<${k * vy}, ${k * vx}>`];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  }
}

function dotProduct(difficulty, type) {
  const a = randNonZero(-8, 8), b = randNonZero(-8, 8);
  const c = randNonZero(-8, 8), d = randNonZero(-8, 8);
  const dot = a * c + b * d;
  const prompt = `Let u = <${a}, ${b}> and v = <${c}, ${d}>. Find u . v (the dot product).`;
  const answer = `${dot}`;
  const solution = [`u . v = (${a})(${c}) + (${b})(${d}) = ${a * c} + ${b * d} = ${dot}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, dot, fmtNum, solution, [a * c - b * d, a * d + b * c, dot + 2]);
}

function perpendicularAngleBetween(difficulty, type) {
  const checkPerp = Math.random() < 0.6;
  if (checkPerp) {
    const perp = Math.random() < 0.5;
    const a = randNonZero(-8, 8), b = randNonZero(-8, 8);
    let c, d;
    if (perp) {
      const flip = Math.random() < 0.5;
      c = flip ? -b : b;
      d = flip ? a : -a;
      const scale = randNonZero(1, 3);
      c *= scale;
      d *= scale;
    } else {
      do {
        c = randNonZero(-8, 8);
        d = randNonZero(-8, 8);
      } while (a * c + b * d === 0);
    }
    const dot = a * c + b * d;
    const prompt = `Are u = <${a}, ${b}> and v = <${c}, ${d}> perpendicular?`;
    const answer = dot === 0 ? `Yes, since u . v = 0.` : `No, since u . v = ${dot} != 0.`;
    const solution = [
      `u . v = (${a})(${c}) + (${b})(${d}) = ${dot}`,
      dot === 0 ? `Since the dot product is 0, u and v are perpendicular.` : `Since the dot product is not 0, u and v are not perpendicular.`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const pool = [
      `Yes, since u . v = 0.`,
      `No, since u . v = ${dot} != 0.`,
      `Yes, all vectors in the plane are perpendicular.`,
      `No, perpendicularity cannot be determined from components.`,
    ];
    return buildMC(prompt, answer, (v) => v, solution, pool.filter((p) => p !== answer));
  } else {
    const angles = [30, 45, 60, 90, 120, 135, 150];
    const deg = choice(angles);
    const mag1 = randInt(2, 6);
    const mag2 = randInt(2, 6);
    const rad = (deg * Math.PI) / 180;
    const u = [mag1, 0];
    const v = [round2(mag2 * Math.cos(rad)), round2(mag2 * Math.sin(rad))];
    const dot = round2(u[0] * v[0] + u[1] * v[1]);
    const prompt = `Let u = <${u[0]}, ${u[1]}> and v = <${v[0]}, ${v[1]}>. Find the angle between u and v, rounded to the nearest degree.`;
    const answer = `${deg} deg`;
    const solution = [`cos(theta) = (u . v)/(|u||v|)`, `u . v = ${dot}, |u| = ${mag1}, |v| = ${mag2}`, `theta = arccos(${round2(dot / (mag1 * mag2))}) ~ ${deg} deg`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, deg, (n) => `${n} deg`, solution, [deg + 15, deg - 15, 180 - deg]);
  }
}

function distancePointToPlane(difficulty, type) {
  const A = randNonZero(-5, 5), B = randNonZero(-5, 5), C = randNonZero(-5, 5), D = randInt(-10, 10);
  const x0 = randInt(-6, 6), y0 = randInt(-6, 6), z0 = randInt(-6, 6);
  const numRaw = A * x0 + B * y0 + C * z0 - D;
  const denom = round2(Math.sqrt(A * A + B * B + C * C));
  const dist = round2(Math.abs(numRaw) / denom);
  const prompt = `Find the distance from the point (${x0}, ${y0}, ${z0}) to the plane ${A}x ${B >= 0 ? "+" : "-"} ${Math.abs(B)}y ${C >= 0 ? "+" : "-"} ${Math.abs(C)}z = ${D}, rounded to 2 decimals.`;
  const answer = `${dist}`;
  const solution = [
    `distance = |Ax0 + By0 + Cz0 - D| / sqrt(A^2 + B^2 + C^2)`,
    `= |${A}(${x0}) + ${B}(${y0}) + ${C}(${z0}) - ${D}| / sqrt(${A}^2 + ${B}^2 + ${C}^2)`,
    `= |${numRaw}| / ${denom} ~ ${dist}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, dist, fmtNum, solution, [round2(dist + 1), round2(Math.abs(numRaw)), round2(dist / 2)]);
}

function randMatrix2() {
  return [
    [randInt(-5, 5), randInt(-5, 5)],
    [randInt(-5, 5), randInt(-5, 5)],
  ];
}
function matStr(M) {
  return `[[${M[0][0]}, ${M[0][1]}], [${M[1][0]}, ${M[1][1]}]]`;
}

function matrices(difficulty, type) {
  const op = choice(["add", "multiply", "apply"]);
  const A = randMatrix2();
  if (op === "add") {
    const B = randMatrix2();
    const C = [[A[0][0] + B[0][0], A[0][1] + B[0][1]], [A[1][0] + B[1][0], A[1][1] + B[1][1]]];
    const prompt = `Let A = ${matStr(A)} and B = ${matStr(B)}. Find A + B.`;
    const answer = matStr(C);
    const solution = [`Add corresponding entries: ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const D1 = [[A[0][0] - B[0][0], A[0][1] - B[0][1]], [A[1][0] - B[1][0], A[1][1] - B[1][1]]];
    return buildMC(prompt, answer, (v) => v, solution, [matStr(D1), matStr(B), matStr(A)]);
  } else if (op === "multiply") {
    const B = randMatrix2();
    const C = [
      [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
      [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ];
    const prompt = `Let A = ${matStr(A)} and B = ${matStr(B)}. Find AB.`;
    const answer = matStr(C);
    const solution = [
      `Row 1 of A times columns of B: [${A[0][0]}*${B[0][0]}+${A[0][1]}*${B[1][0]}, ${A[0][0]}*${B[0][1]}+${A[0][1]}*${B[1][1]}]`,
      `Row 2 of A times columns of B: [${A[1][0]}*${B[0][0]}+${A[1][1]}*${B[1][0]}, ${A[1][0]}*${B[0][1]}+${A[1][1]}*${B[1][1]}]`,
      `AB = ${answer}`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const wrongOrder = [
      [B[0][0] * A[0][0] + B[0][1] * A[1][0], B[0][0] * A[0][1] + B[0][1] * A[1][1]],
      [B[1][0] * A[0][0] + B[1][1] * A[1][0], B[1][0] * A[0][1] + B[1][1] * A[1][1]],
    ];
    return buildMC(prompt, answer, (v) => v, solution, [matStr(wrongOrder), matStr(B), matStr(A)]);
  } else {
    const vx = randInt(-6, 6), vy = randInt(-6, 6);
    const rx = A[0][0] * vx + A[0][1] * vy;
    const ry = A[1][0] * vx + A[1][1] * vy;
    const prompt = `Let A = ${matStr(A)} act on the point (x, y) = (${vx}, ${vy}) as a linear function. Find A(${vx}, ${vy}).`;
    const answer = `(${rx}, ${ry})`;
    const solution = [`A*[x,y] = [${A[0][0]}*${vx} + ${A[0][1]}*${vy}, ${A[1][0]}*${vx} + ${A[1][1]}*${vy}] = ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, answer, (v) => v, solution, [`(${ry}, ${rx})`, `(${vx}, ${vy})`, `(${rx + 1}, ${ry})`]);
  }
}

function matrixInverseDeterminant(difficulty, type) {
  let A;
  do {
    A = randMatrix2();
  } while (A[0][0] * A[1][1] - A[0][1] * A[1][0] === 0);
  const det = A[0][0] * A[1][1] - A[0][1] * A[1][0];
  const wantInverse = difficulty >= 2 && Math.random() < 0.6;
  if (!wantInverse) {
    const prompt = `Find the determinant of A = ${matStr(A)}.`;
    const answer = `${det}`;
    const solution = [`det(A) = (${A[0][0]})(${A[1][1]}) - (${A[0][1]})(${A[1][0]}) = ${det}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    return buildMC(prompt, det, fmtNum, solution, [det + 1, det - 1, -det]);
  } else {
    const prompt = `Find the inverse of A = ${matStr(A)}.`;
    const answer = `(1/${det}) * [[${A[1][1]}, ${-A[0][1]}], [${-A[1][0]}, ${A[0][0]}]]`;
    const solution = [
      `det(A) = (${A[0][0]})(${A[1][1]}) - (${A[0][1]})(${A[1][0]}) = ${det}`,
      `A^-1 = (1/det(A)) * [[d, -b], [-c, a]] where A = [[a,b],[c,d]]`,
      `A^-1 = ${answer}`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [
      `(1/${det}) * [[${A[0][0]}, ${A[0][1]}], [${A[1][0]}, ${A[1][1]}]]`,
      `(1/${-det}) * [[${A[1][1]}, ${-A[0][1]}], [${-A[1][0]}, ${A[0][0]}]]`,
      `(1/${det}) * [[${A[1][1]}, ${A[0][1]}], [${A[1][0]}, ${A[0][0]}]]`,
    ];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  }
}

function linearTransformations(difficulty, type) {
  const types = [
    { M: [[1, 0], [0, -1]], name: "reflection over the x-axis" },
    { M: [[-1, 0], [0, 1]], name: "reflection over the y-axis" },
    { M: [[0, -1], [1, 0]], name: "rotation by 90 deg counterclockwise" },
    { M: [[-1, 0], [0, -1]], name: "rotation by 180 deg" },
    { M: [[2, 0], [0, 2]], name: "a scaling by a factor of 2" },
    { M: [[0, 1], [1, 0]], name: "reflection over the line y = x" },
  ];
  const item = choice(types);
  const prompt = `The matrix M = ${matStr(item.M)} represents which linear transformation?`;
  const answer = item.name;
  const solution = [`Applying M to (1,0) and (0,1) reveals the transformation: ${answer}.`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const others = types.filter((t) => t.name !== answer).map((t) => t.name);
  const choices = shuffle([answer, ...shuffle(others).slice(0, 3)]);
  return { type: "mc", prompt, choices, correctIndex: choices.indexOf(answer), answer, solution };
}

function cramersRule(difficulty, type) {
  let a1, b1, a2, b2, D;
  do {
    a1 = randNonZero(-6, 6);
    b1 = randNonZero(-6, 6);
    a2 = randNonZero(-6, 6);
    b2 = randNonZero(-6, 6);
    D = a1 * b2 - a2 * b1;
  } while (D === 0);
  const xVal = randInt(-5, 5), yVal = randInt(-5, 5);
  const c1 = a1 * xVal + b1 * yVal, c2 = a2 * xVal + b2 * yVal;
  const Dx = c1 * b2 - c2 * b1, Dy = a1 * c2 - a2 * c1;
  const prompt = `Use Cramer's Rule to solve the system:\n${a1}x ${b1 >= 0 ? "+" : "-"} ${Math.abs(b1)}y = ${c1}\n${a2}x ${b2 >= 0 ? "+" : "-"} ${Math.abs(b2)}y = ${c2}`;
  const answer = `x = ${fracStr(Dx, D)}, y = ${fracStr(Dy, D)}`;
  const solution = [
    `D = |${a1} ${b1}; ${a2} ${b2}| = ${a1}(${b2}) - ${a2}(${b1}) = ${D}`,
    `Dx = |${c1} ${b1}; ${c2} ${b2}| = ${Dx}`,
    `Dy = |${a1} ${c1}; ${a2} ${c2}| = ${Dy}`,
    `x = Dx/D = ${fracStr(Dx, D)}, y = Dy/D = ${fracStr(Dy, D)}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [`x = ${fracStr(Dy, D)}, y = ${fracStr(Dx, D)}`, `x = ${fracStr(Dx, -D)}, y = ${fracStr(Dy, D)}`, `x = ${xVal + 1}, y = ${yVal}`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

/* ========================= UNIT 11: SEQUENCES AND SERIES ================== */

function sequences(difficulty, type) {
  const isArithmetic = Math.random() < 0.5;
  const a1 = randInt(-8, 8);
  const n = randInt(4, 5 + difficulty);
  if (isArithmetic) {
    const d = randNonZero(-6, 6);
    const terms = Array.from({ length: 4 }, (_, i) => a1 + d * i);
    const an = a1 + d * (n - 1);
    const prompt = `An arithmetic sequence begins ${terms.join(", ")}, ... Find the ${n}th term.`;
    const solution = [`Common difference d = ${d}.`, `a_n = a_1 + (n-1)d = ${a1} + (${n}-1)(${d}) = ${an}`];
    if (type === "fr") return buildFR(prompt, `${an}`, solution);
    return buildMC(prompt, an, fmtNum, solution, [an + d, an - d, an + 1]);
  } else {
    const r = choice([2, 3, -2, 0.5, -0.5]);
    const first = randInt(1, 6) * (r === 0.5 || r === -0.5 ? 4 : 1);
    const terms = Array.from({ length: 4 }, (_, i) => first * Math.pow(r, i));
    const an = first * Math.pow(r, n - 1);
    const prompt = `A geometric sequence begins ${terms.map(fmtNum).join(", ")}, ... Find the ${n}th term.`;
    const solution = [`Common ratio r = ${r}.`, `a_n = a_1 * r^(n-1) = ${first} * (${r})^${n - 1} = ${fmtNum(an)}`];
    if (type === "fr") return buildFR(prompt, fmtNum(an), solution);
    return buildMC(prompt, an, fmtNum, solution, [an * r, an / r, -an]);
  }
}

function recursiveFibonacci(difficulty, type) {
  const a1 = randInt(1, 6), a2 = randInt(1, 6);
  const n = randInt(5, 7 + difficulty);
  const seq = [a1, a2];
  for (let i = 2; i < n; i++) seq.push(seq[i - 1] + seq[i - 2]);
  const val = seq[n - 1];
  const prompt = `A sequence is defined recursively by a1 = ${a1}, a2 = ${a2}, and a_n = a_(n-1) + a_(n-2) for n >= 3. Find a_${n}.`;
  const answer = `${val}`;
  const solution = [`Terms: ${seq.map((v, i) => `a_${i + 1}=${v}`).join(", ")}`, `a_${n} = ${val}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, val, fmtNum, solution, [seq[n - 2], val + seq[n - 2], val - 1]);
}

function infiniteGeometricSeries(difficulty, type) {
  const asRepeatingDecimal = difficulty >= 2 && Math.random() < 0.5;
  if (!asRepeatingDecimal) {
    const R_CHOICES = [[1, 2], [-1, 2], [1, 3], [-1, 3], [1, 4], [-1, 4], [2, 3], [-2, 3], [1, 5], [-1, 5]];
    const [rp, rq] = choice(R_CHOICES);
    const a = randInt(2, 12);
    const answer = fracStr(a * rq, rq - rp);
    const rStr = fracStr(rp, rq);
    const prompt = `Find the sum of the infinite geometric series with first term a = ${a} and common ratio r = ${rStr}.`;
    const solution = [`Since |r| < 1, S = a / (1 - r)`, `S = ${a} / (1 - ${rStr}) = ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [fracStr(a * rq, rq + rp), fracStr(a, rq - rp), fracStr(a * rq, -(rq - rp))];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  } else {
    const REPEATS = [
      { digits: "7", num: 7, denPow: 1 },
      { digits: "3", num: 3, denPow: 1 },
      { digits: "45", num: 45, denPow: 2 },
      { digits: "27", num: 27, denPow: 2 },
      { digits: "18", num: 18, denPow: 2 },
    ];
    const rep = choice(REPEATS);
    const den = Math.pow(10, rep.denPow) - 1;
    const answer = fracStr(rep.num, den);
    const prompt = `Convert the repeating decimal 0.${rep.digits}${rep.digits}${rep.digits}... (repeating block "${rep.digits}") to a fraction in lowest terms.`;
    const solution = [
      `Let x = 0.${rep.digits} repeating (block length ${rep.digits.length}).`,
      `${den + 1}x - x = ${rep.num} (shift by the block length and subtract), so ${den}x = ${rep.num}`,
      `x = ${rep.num}/${den} = ${answer}`,
    ];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [fracStr(rep.num, den + 2), fracStr(rep.num + 1, den), fracStr(den, rep.num)];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  }
}

function financialApplications(difficulty, type) {
  const PMT = randInt(50, 500) * 10;
  const ratePct = choice([3, 4, 5, 6, 8]);
  const i = ratePct / 100;
  const n = randInt(5, 10 + difficulty * 2);
  const FV = PMT * ((Math.pow(1 + i, n) - 1) / i);
  const rounded = round2(FV);
  const prompt = `An ordinary annuity has payments of $${PMT} at the end of each year for ${n} years, earning ${ratePct}% annual interest. Use FV = PMT * [((1+i)^n - 1)/i] to find the future value, rounded to the nearest cent.`;
  const answer = `$${rounded.toFixed(2)}`;
  const solution = [`FV = ${PMT} * [((1+${i})^${n} - 1)/${i}]`, `FV ~ ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, rounded, (v) => `$${v.toFixed(2)}`, solution, [round2(PMT * n), round2(rounded * 1.1), round2(rounded * 0.9)]);
}

function mathematicalInduction(difficulty, type) {
  const formulas = [
    { name: "sum of the first n positive integers", closed: (n) => (n * (n + 1)) / 2, formulaStr: "n(n+1)/2" },
    { name: "sum of the first n odd positive integers", closed: (n) => n * n, formulaStr: "n^2" },
    { name: "sum of the first n squares", closed: (n) => (n * (n + 1) * (2 * n + 1)) / 6, formulaStr: "n(n+1)(2n+1)/6" },
  ];
  const f = choice(formulas);
  const n = randInt(4, 8 + difficulty);
  const val = f.closed(n);
  const prompt = `The formula for the ${f.name} is S(n) = ${f.formulaStr}. Verify this formula by computing S(${n}).`;
  const answer = `${val}`;
  const solution = [`S(${n}) = ${f.formulaStr.replace(/n/g, `(${n})`)}`, `S(${n}) = ${val}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, val, fmtNum, solution, [val + n, val - n, f.closed(n - 1)]);
}

function telescopingSeries(difficulty, type) {
  const n = randInt(4, 10 + difficulty);
  const answer = fracStr(n, n + 1);
  const prompt = `Find the sum: sum_(k=1)^(${n}) [1/k - 1/(k+1)]`;
  const solution = [`This telescopes: the sum collapses to 1/1 - 1/(${n}+1).`, `= 1 - 1/${n + 1} = ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, answer, (v) => v, solution, [fracStr(1, n + 1), fracStr(n + 1, n), fracStr(n, n - 1)]);
}

function limitsOfSequences(difficulty, type) {
  const degNum = difficulty === 1 ? 1 : randInt(1, 2);
  const degDen = difficulty === 1 ? 1 : randInt(1, 2);
  const leadNum = randNonZero(-6, 6);
  let leadDen = randNonZero(1, 6);
  if (leadDen === leadNum) leadDen = leadNum + 1;
  const prompt = `Find lim(n -> infinity) of a_n = (${leadNum}n^${degNum} + ...) / (${leadDen}n^${degDen} + ...)`;
  let answer, reasoning;
  if (degNum < degDen) {
    answer = "0";
    reasoning = `The denominator grows faster (higher degree), so the limit is 0.`;
  } else if (degNum === degDen) {
    answer = fracStr(leadNum, leadDen);
    reasoning = `The degrees are equal, so the limit is the ratio of leading coefficients.`;
  } else {
    answer = "infinity (does not converge)";
    reasoning = `The numerator grows faster (higher degree), so the sequence diverges.`;
  }
  const solution = [reasoning, `Answer: ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const pool = ["0", fracStr(leadNum, leadDen), "infinity (does not converge)", fracStr(leadDen, leadNum)];
  return buildMC(prompt, answer, (v) => v, solution, pool.filter((p) => p !== answer));
}

/* ============================ dispatcher =============================== */

const GENERATORS = {
  domainOfComposition,
  compositionOfFunctions,
  piecewiseFunctions,
  absoluteValueFunctions,
  intuitiveLimit,
  intermediateValueTheorem,
  rateOfChange,
  functionTransformations,
  inverseFunctions,
  polynomialDivision,
  remainderFactorTheorem,
  polynomialZeros,
  complexNumberArithmetic,
  fundamentalTheoremAlgebra,
  rationalRootTheorem,
  conjugateZerosTheorem,
  sumProductRoots,
  permutationsCombinations,
  binomialExpansion,
  binomialProbability,
  verticalHorizontalAsymptotes,
  slantAsymptotes,
  rationalHoles,
  oneSidedInfiniteLimits,
  rationalInequalities,
  partialFractions,
  rationalEquations,
  logarithmExpressions,
  expLogEquations,
  compoundInterest,
  exponentialModeling,
  parabolas,
  ellipses,
  hyperbolas,
  classifyConics,
  trigValuesReciprocal,
  expressTrigUsingOthers,
  trigGraphs,
  tanSecCscCotGraphs,
  inverseTrig,
  rightTriangleTrig,
  trigIdentities,
  sumDifferenceFormulas,
  doubleHalfAngle,
  trigEquations,
  harmonicMotion,
  lawOfSines,
  lawOfCosines,
  heronsFormula,
  trigFormComplex,
  deMoivresTheorem,
  rootsOfComplex,
  parametricCurves,
  parametricCirclesLines,
  polarCoordinates,
  polarGraphs,
  vectors,
  dotProduct,
  perpendicularAngleBetween,
  distancePointToPlane,
  matrices,
  linearTransformations,
  matrixInverseDeterminant,
  cramersRule,
  sequences,
  recursiveFibonacci,
  infiniteGeometricSeries,
  financialApplications,
  mathematicalInduction,
  telescopingSeries,
  limitsOfSequences,
};

function generateProblem(topicId, difficulty, questionType) {
  const topic = TOPIC_INDEX[topicId];
  if (!topic) throw new Error(`Unknown topic id: ${topicId}`);
  const fn = GENERATORS[topic.gen];
  if (!fn) throw new Error(`No generator registered for: ${topic.gen}`);
  let effectiveType = questionType;
  if (questionType === "mixed") effectiveType = Math.random() < 0.5 ? "mc" : "fr";
  const q = fn(difficulty, effectiveType);
  return Object.assign(
    {
      topicId,
      topicTitle: topic.title,
      unitTitle: topic.unitTitle,
    },
    q
  );
}
