/**
 * Problem generators for the AP Precalculus problem set generator.
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
 * side PDF font, so the same text is safe on screen and in the PDF.
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
function fmtNum(n) {
  if (Number.isInteger(n)) return `${n}`;
  return round2(n).toString();
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
  while (distinctDistractors.length < 3) {
    const filler = correctVal + randNonZero(-5, 5);
    const s = formatter(filler);
    if (!seen.has(s)) {
      seen.add(s);
      distinctDistractors.push(filler);
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

const DEG_SCALE = { 1: 1, 2: 1.6, 3: 2.4 };

/* ============================ UNIT 1 =================================== */

function changeInTandem(difficulty, type) {
  const m = randNonZero(-6, 6) * (difficulty === 1 ? 1 : difficulty === 2 ? 1 : 1);
  const b = randInt(-10, 10);
  const start = randInt(-4, 2);
  const xs = [start, start + 1, start + 2, start + 3];
  const ys = xs.map((x) => m * x + b);
  const table = xs.map((x, i) => `x = ${x}: g(x) = ${ys[i]}`).join(",  ");
  const prompt = `A function g changes in tandem with x as shown:\n${table}\nAs x increases by 1, by how much does g(x) change (the constant rate of change)?`;
  const solution = [
    `Consecutive differences: ${ys.slice(1).map((y, i) => y - ys[i]).join(", ")}`,
    `Each difference equals ${m}, so g changes by ${m} for every increase of 1 in x.`,
  ];
  if (type === "fr") return buildFR(prompt, `${m}`, solution);
  return buildMC(prompt, m, fmtNum, solution, [m + 1, m - 1, -m, m * 2]);
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

function polynomialZeros(difficulty, type) {
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
  const solution = [
    `Set each factor equal to 0: ${roots.map((r) => `x - (${r}) = 0`).join(", ")}`,
    `Zeros: x = ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    sortedRoots.map((r) => r + 1).join(", "),
    sortedRoots.map((r) => -r).join(", "),
    [...sortedRoots].reverse().map((r) => r * -1).join(", "),
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function polynomialEndBehavior(difficulty, type) {
  const degree = difficulty === 1 ? randInt(2, 3) : randInt(3, 5);
  const lead = randNonZero(-4, 4);
  const rest = Array.from({ length: degree }, () => randInt(-6, 6));
  const coeffs = [lead, ...rest];
  const fx = polyStr(coeffs);
  const isEvenDeg = degree % 2 === 0;
  const posLead = lead > 0;
  const asXtoInf = posLead ? "infinity" : "-infinity";
  const asXtoNegInf = isEvenDeg ? asXtoInf : posLead ? "-infinity" : "infinity";
  const prompt = `Let f(x) = ${fx}. Describe the end behavior: as x -> infinity, f(x) -> ? and as x -> -infinity, f(x) -> ?`;
  const answer = `As x -> infinity, f(x) -> ${asXtoInf}; as x -> -infinity, f(x) -> ${asXtoNegInf}`;
  const solution = [
    `The leading term is ${lead}x^${degree}, which controls end behavior.`,
    `Degree ${degree} is ${isEvenDeg ? "even" : "odd"} and the leading coefficient is ${posLead ? "positive" : "negative"}.`,
    answer,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const options = [
    "As x -> infinity, f(x) -> infinity; as x -> -infinity, f(x) -> infinity",
    "As x -> infinity, f(x) -> -infinity; as x -> -infinity, f(x) -> -infinity",
    "As x -> infinity, f(x) -> infinity; as x -> -infinity, f(x) -> -infinity",
    "As x -> infinity, f(x) -> -infinity; as x -> -infinity, f(x) -> infinity",
  ];
  const correctStr = answer;
  const others = options.filter((o) => o !== correctStr);
  const choices = shuffle([correctStr, ...shuffle(others).slice(0, 3)]);
  return {
    type: "mc",
    prompt,
    choices,
    correctIndex: choices.indexOf(correctStr),
    answer: correctStr,
    solution,
  };
}

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

function rationalEndBehavior(difficulty, type) {
  const degNum = difficulty === 1 ? randInt(1, 2) : randInt(1, 3);
  const degDen = difficulty === 1 ? randInt(1, 2) : randInt(1, 3);
  const leadNum = randNonZero(-4, 4);
  const leadDen = randNonZero(1, 4);
  const numStr = `${leadNum}x^${degNum}${degNum > 1 ? "" : ""}` + (degNum === 1 ? "" : "");
  const fx = `f(x) = (${leadNum}x^${degNum} + ...) / (${leadDen}x^${degDen} + ...)`;
  let answer, reasoning;
  if (degNum < degDen) {
    answer = "y = 0";
    reasoning = "Since the degree of the numerator is less than the degree of the denominator, the horizontal asymptote is y = 0.";
  } else if (degNum === degDen) {
    const ratio = fracStr(leadNum, leadDen);
    answer = `y = ${ratio}`;
    reasoning = `Since the degrees are equal, the horizontal asymptote is the ratio of leading coefficients: y = ${leadNum}/${leadDen} = ${ratio}.`;
  } else {
    answer = "no horizontal asymptote (end behavior follows the quotient)";
    reasoning = "Since the degree of the numerator is greater than the degree of the denominator, there is no horizontal asymptote.";
  }
  const prompt = `A rational function ${fx} has numerator degree ${degNum} and denominator degree ${degDen}, with leading coefficients ${leadNum} and ${leadDen}. Identify the horizontal asymptote (end behavior) of f.`;
  const solution = [reasoning, `Answer: ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const pool = [
    "y = 0",
    `y = ${fracStr(leadNum, leadDen)}`,
    "no horizontal asymptote (end behavior follows the quotient)",
    `y = ${fracStr(leadDen, leadNum)}`,
    `y = ${fracStr(leadNum + 1, leadDen)}`,
    `y = ${fracStr(leadNum, leadDen + 1)}`,
  ];
  const seen = new Set([answer]);
  const others = [];
  for (const p of pool) {
    if (!seen.has(p)) {
      seen.add(p);
      others.push(p);
    }
    if (others.length >= 3) break;
  }
  const choices = shuffle([answer, ...others]);
  return { type: "mc", prompt, choices, correctIndex: choices.indexOf(answer), answer, solution };
}

function rationalZeros(difficulty, type) {
  const { numRoots, denRoots } = makeRational(difficulty);
  const numStr = numRoots.map(linearFactorStr).join("");
  const denStr = denRoots.map(linearFactorStr).join("");
  const prompt = `Let f(x) = [${numStr}] / [${denStr}]. Find the zero(s) of f.`;
  const sorted = [...numRoots].sort((a, b) => a - b);
  const answer = sorted.join(", ");
  const solution = [
    `The zeros of a rational function are the values that make the numerator 0 (and are not also zeros of the denominator).`,
    `Numerator is 0 when x = ${answer}.`,
    `None of these values also make the denominator 0, so they are valid zeros of f.`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [sorted.map((r) => r + 1).join(", "), denRoots.sort((a, b) => a - b).join(", "), sorted.map((r) => -r).join(", ")];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function rationalAsymptotes(difficulty, type) {
  const { numRoots, denRoots } = makeRational(difficulty);
  const numStr = numRoots.map(linearFactorStr).join("");
  const denStr = denRoots.map(linearFactorStr).join("");
  const prompt = `Let f(x) = [${numStr}] / [${denStr}]. Give the equation(s) of the vertical asymptote(s) of f.`;
  const sorted = [...denRoots].sort((a, b) => a - b);
  const answer = sorted.map((r) => `x = ${r}`).join(", ");
  const solution = [
    `Vertical asymptotes occur where the denominator is 0 and the numerator is not.`,
    `Denominator is 0 when x = ${sorted.join(", ")}, and none of these are also numerator zeros.`,
    `Answer: ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    numRoots.sort((a, b) => a - b).map((r) => `x = ${r}`).join(", "),
    sorted.map((r) => `x = ${r + 1}`).join(", "),
    sorted.map((r) => `x = ${-r}`).join(", "),
  ];
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

function equivalentExpressions(difficulty, type) {
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
  const otherNum = pick();
  const otherDen = pick();
  const numRoots = [shared, otherNum];
  const denRoots = [shared, otherDen];
  const numStr = expandTwoFactors(...numRoots);
  const denStr = expandTwoFactors(...denRoots);
  const prompt = `Simplify to lowest terms: f(x) = (${polyStr(numStr)}) / (${polyStr(denStr)})`;
  const answer = `(x ${otherNum >= 0 ? "-" : "+"} ${Math.abs(otherNum)}) / (x ${otherDen >= 0 ? "-" : "+"} ${Math.abs(otherDen)}),  x != ${shared}`;
  const solution = [
    `Factor numerator: ${linearFactorStr(shared)}${linearFactorStr(otherNum)}`,
    `Factor denominator: ${linearFactorStr(shared)}${linearFactorStr(otherDen)}`,
    `Cancel the common factor (x - (${shared})), noting x != ${shared}.`,
    `Simplified form: ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `(x ${shared >= 0 ? "-" : "+"} ${Math.abs(shared)}) / (x ${otherDen >= 0 ? "-" : "+"} ${Math.abs(otherDen)})`,
    `(x ${otherDen >= 0 ? "-" : "+"} ${Math.abs(otherDen)}) / (x ${otherNum >= 0 ? "-" : "+"} ${Math.abs(otherNum)})`,
    `(x ${otherNum >= 0 ? "+" : "-"} ${Math.abs(otherNum)}) / (x ${otherDen >= 0 ? "-" : "+"} ${Math.abs(otherDen)})`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
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

function modelSelection(difficulty, type) {
  const scenarios = [
    { desc: "Successive outputs share a common difference for equally spaced inputs.", answer: "linear" },
    { desc: "Successive outputs share a common ratio for equally spaced inputs.", answer: "exponential" },
    { desc: "The second differences of the outputs are constant for equally spaced inputs.", answer: "quadratic" },
    { desc: "The output values oscillate between a fixed maximum and minimum on a regular interval.", answer: "sinusoidal (periodic)" },
  ];
  const s = choice(scenarios);
  const prompt = `A table of data has the property: "${s.desc}" Which family of functions best models this data?`;
  const answer = s.answer;
  const solution = [`This pattern is the defining signature of a ${answer} model.`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const all = scenarios.map((x) => x.answer);
  const others = all.filter((a) => a !== answer);
  const choices = shuffle([answer, ...shuffle(others).slice(0, 3)]);
  return { type: "mc", prompt, choices, correctIndex: choices.indexOf(answer), answer, solution };
}

/* ============================ UNIT 2 =================================== */

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

function linearVsExponential(difficulty, type) {
  const b = randInt(2, 10);
  const t = randInt(3, 4 + difficulty);
  const linVal = b * t;
  const base = choice([2, 3]);
  const expVal = b * Math.pow(base, t);
  const prompt = `Function L is linear with L(0) = 0 and grows by ${b} per unit of x. Function E is exponential with E(0) = ${b} and grows by a factor of ${base} per unit of x. Which function is greater at x = ${t}, and what is its value?`;
  const winner = expVal > linVal ? "E" : "L";
  const winVal = Math.max(expVal, linVal);
  const answer = `${winner}(${t}) = ${fmtNum(winVal)}`;
  const solution = [
    `L(${t}) = ${b} * ${t} = ${linVal}`,
    `E(${t}) = ${b} * ${base}^${t} = ${fmtNum(expVal)}`,
    `Exponential growth eventually overtakes linear growth, so ${answer} is greater.`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [`L(${t}) = ${linVal}`, `E(${t}) = ${fmtNum(expVal * base)}`, `L(${t}) = ${linVal * base}`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function exponentialFunctions(difficulty, type) {
  const a = randInt(2, 10);
  const base = choice(difficulty === 1 ? [2, 3, 5] : [2, 3, 5, 1.5, 0.5]);
  const x = randInt(1, 2 + difficulty);
  const val = a * Math.pow(base, x);
  const prompt = `Let f(x) = ${a} * (${base})^x. Find f(${x}).`;
  const answer = fmtNum(val);
  const solution = [`f(${x}) = ${a} * (${base})^${x} = ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, val, fmtNum, solution, [a * Math.pow(base, x - 1), a * Math.pow(base, x + 1), a * x * base]);
}

function exponentialManipulation(difficulty, type) {
  const a = randInt(2, 8);
  const weeklyRate = choice([1.05, 1.1, 1.2, 0.9, 0.85]);
  const prompt = `A quantity is modeled by P(t) = ${a}(${weeklyRate})^t, where t is measured in weeks. Rewrite P as an equivalent function of the form ${a}*b^d, where d is measured in days (t = d/7), and give b rounded to 4 decimal places.`;
  const bDaily = Math.pow(weeklyRate, 1 / 7);
  const answer = bDaily.toFixed(4);
  const solution = [
    `Since t = d/7, P = ${a}(${weeklyRate})^(d/7) = ${a} * [(${weeklyRate})^(1/7)]^d`,
    `(${weeklyRate})^(1/7) ~ ${answer}`,
    `So P(d) = ${a} * (${answer})^d`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [(weeklyRate / 7).toFixed(4), Math.pow(weeklyRate, 7).toFixed(4), (1 + (weeklyRate - 1) / 7).toFixed(4)];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function exponentialModeling(difficulty, type) {
  const P0 = randInt(100, 900) * 10;
  const rate = choice([0.03, 0.05, 0.08, 0.1, -0.04, -0.06]);
  const t = randInt(2, 4 + difficulty);
  const val = P0 * Math.pow(1 + rate, t);
  const growth = rate > 0 ? "grows" : "decays";
  const prompt = `A town's population is P0 = ${P0} and ${growth} at ${Math.abs(rate) * 100}% per year. Find the population after ${t} years, rounded to the nearest whole number.`;
  const answer = Math.round(val).toString();
  const solution = [`P(t) = ${P0}(1 ${rate > 0 ? "+" : "-"} ${Math.abs(rate)})^t`, `P(${t}) = ${P0}(${1 + rate})^${t} ~ ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const v = Math.round(val);
  return buildMC(prompt, v, (n) => `${Math.round(n)}`, solution, [Math.round(P0 * (1 + rate) * t), Math.round(P0 + rate * t * P0), Math.round(val * (1 + rate))]);
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

function inverseFunctions(difficulty, type) {
  const kind = difficulty === 1 ? "linear" : choice(["linear", "exponential"]);
  if (kind === "linear") {
    const a = randNonZero(-6, 6);
    const b = randInt(-8, 8);
    const prompt = `Find the inverse of f(x) = ${a}x ${b >= 0 ? "+" : "-"} ${Math.abs(b)}.`;
    const answer = `f^-1(x) = (x ${b >= 0 ? "-" : "+"} ${Math.abs(b)}) / ${a}`;
    const solution = [`y = ${a}x ${b >= 0 ? "+" : "-"} ${Math.abs(b)}`, `Solve for x: x = (y ${b >= 0 ? "-" : "+"} ${Math.abs(b)}) / ${a}`, `Swap x and y: ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [`f^-1(x) = ${a}x ${b >= 0 ? "-" : "+"} ${Math.abs(b)}`, `f^-1(x) = (x ${b >= 0 ? "+" : "-"} ${Math.abs(b)}) / ${a}`, `f^-1(x) = (${a}x ${b >= 0 ? "-" : "+"} ${Math.abs(b)})`];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  } else {
    const a = randInt(2, 6);
    const base = choice([2, 3, 5]);
    const prompt = `Find the inverse of f(x) = ${a} * ${base}^x.`;
    const answer = `f^-1(x) = log_${base}(x / ${a})`;
    const solution = [`y = ${a} * ${base}^x`, `x / ${a} = ${base}^y`, `Take log base ${base}: y = log_${base}(x/${a})`, `So ${answer}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [`f^-1(x) = log_${base}(x) / ${a}`, `f^-1(x) = ${base}^(x/${a})`, `f^-1(x) = log_${base}(x) - ${a}`];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  }
}

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

function logFunctions(difficulty, type) {
  const base = choice([2, 3, 5, 10]);
  const exp = randInt(1, 3 + difficulty);
  const x = Math.pow(base, exp);
  const prompt = `Evaluate: log_${base}(${x})`;
  const answer = `${exp}`;
  const solution = [`log_${base}(${x}) asks "${base} to what power gives ${x}?"`, `${base}^${exp} = ${x}, so log_${base}(${x}) = ${exp}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, exp, fmtNum, solution, [exp + 1, exp - 1, x]);
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

function semiLogPlots(difficulty, type) {
  const scenarios = [
    { desc: "A plot of log(y) versus x is a straight line.", answer: "y is an exponential function of x" },
    { desc: "A plot of y versus x is a straight line, and a plot of log(y) versus x is curved.", answer: "y is a linear (not exponential) function of x" },
    { desc: "A plot of log(y) versus log(x) is a straight line.", answer: "y is a power function of x" },
    { desc: "Both a plot of y versus x and a plot of log(y) versus x are curved (non-linear).", answer: "y is neither a linear nor an exponential function of x" },
  ];
  const s = choice(scenarios);
  const prompt = `On a data set: "${s.desc}" What does this indicate about the relationship between y and x?`;
  const answer = s.answer;
  const solution = [`A semi-log or log-log plot that is linear reveals the underlying model: ${answer}.`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const others = scenarios.map((x) => x.answer).filter((a) => a !== answer);
  const choices = shuffle([answer, ...others]);
  return { type: "mc", prompt, choices, correctIndex: choices.indexOf(answer), answer, solution };
}

/* ============================ UNIT 3 =================================== */

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

function trigGraphs(difficulty, type) {
  const a = randInt(1, 5 + difficulty);
  const bVals = [1, 2, 3, 0.5];
  const b = choice(bVals);
  const period = round2((2 * Math.PI) / b);
  const d = randInt(-5, 5);
  const func = choice(["sin", "cos"]);
  const prompt = `For y = ${a}${func}(${b}x) ${d >= 0 ? "+" : "-"} ${Math.abs(d)}, find the amplitude, period, and midline.`;
  const answer = `amplitude = ${a}, period = ${a === 1 ? "" : ""}${b === 1 ? "2pi" : `2pi/${b}`}, midline y = ${d}`;
  const solution = [`Amplitude = |a| = ${a}`, `Period = 2pi / |b| = 2pi / ${b}`, `Midline: y = d = ${d}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [
    `amplitude = ${a}, period = ${b}pi, midline y = ${d}`,
    `amplitude = ${b}, period = 2pi/${a}, midline y = ${d}`,
    `amplitude = ${a}, period = ${b === 1 ? "2pi" : `2pi/${b}`}, midline y = ${-d}`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function trigModeling(difficulty, type) {
  const midline = randInt(50, 70);
  const amp = randInt(10, 20 + difficulty * 5);
  const period = choice([12, 24]);
  const b = round2((2 * Math.PI) / period);
  const t = choice([0, period / 4, period / 2]);
  const val = midline + amp * Math.cos((2 * Math.PI * t) / period);
  const prompt = `The temperature T (deg F) t hours after midnight is modeled by T(t) = ${midline} + ${amp}cos((2pi/${period})t). Find T(${t}), the temperature ${t} hours after midnight.`;
  const answer = fmtNum(round2(val));
  const solution = [`T(${t}) = ${midline} + ${amp}cos((2pi/${period})(${t}))`, `= ${midline} + ${amp}cos(${round2((2 * Math.PI * t) / period)}) ~ ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, round2(val), fmtNum, solution, [midline, midline + amp, midline - amp]);
}

function tangentFunction(difficulty, type) {
  const angles = [0, 30, 45, 60, 120, 135, 150, 180, 210, 225, 240, 300, 315, 330];
  const deg = choice(angles);
  const prompt = `Evaluate exactly: tan(${deg} deg)`;
  const answer = TRIG_TABLE[deg].tan;
  const solution = [`tan(theta) = sin(theta)/cos(theta)`, `sin(${deg} deg) = ${TRIG_TABLE[deg].sin}, cos(${deg} deg) = ${TRIG_TABLE[deg].cos}`, `tan(${deg} deg) = ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const other = choice(angles.filter((a) => a !== deg));
  return buildMC(prompt, answer, (v) => v, solution, [TRIG_TABLE[other].tan, TRIG_TABLE[deg].sin, TRIG_TABLE[deg].cos]);
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
  const solution = [`This is asking for the angle in the range of ${item.func} whose ${item.func === "arcsin" ? "sine" : item.func === "arccos" ? "cosine" : "tangent"} is ${item.x}.`, `Answer: ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = table.filter((t) => t.ans !== answer).map((t) => t.ans);
  return buildMC(prompt, answer, (v) => v, solution, shuffle(distractors));
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
  const distractors = [
    sols.map((d) => `${360 - d} deg`).join(", "),
    sols.map((d) => `${d + 10} deg`).join(", "),
    `${sols[0]} deg`,
  ];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

function reciprocalTrig(difficulty, type) {
  const angles = [0, 30, 45, 60, 120, 135, 150, 180, 210, 225, 240, 300, 315, 330];
  const deg = choice(angles.filter((a) => TRIG_TABLE[a].sin !== "0" && TRIG_TABLE[a].cos !== "0"));
  const func = choice(["sec", "csc", "cot"]);
  const recipOf = { sec: "cos", csc: "sin", cot: "tan" };
  const base = TRIG_TABLE[deg][recipOf[func]];
  // Compute reciprocal as a simplified string for common values.
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
  ];
  const item = choice(shapes);
  const prompt = `Identify the type of polar curve described by ${item.eq} (a, b > 0 constants).`;
  const answer = item.answer;
  const solution = [`This is the standard classification for a polar equation of the form ${item.eq}.`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const others = shapes.filter((s) => s.answer !== answer).map((s) => s.answer);
  const choices = shuffle([answer, ...shuffle(others).slice(0, 3)]);
  return { type: "mc", prompt, choices, correctIndex: choices.indexOf(answer), answer, solution };
}

/* ============================ UNIT 4 =================================== */

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

function parametricCirclesLines(difficulty, type) {
  const r = randInt(2, 8);
  const h = randInt(-5, 5);
  const k = randInt(-5, 5);
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
  const prompt = `An object's position is given by x(t) = ${x0} + ${vx}t, y(t) = ${y0} + ${vy}t (position in meters, t in seconds). Find the object's average speed between t = ${t1} and t = ${t2}, rounded to 2 decimals.`;
  const answer = `${speed} m/s`;
  const solution = [
    `Position at t=${t1}: (${x1}, ${y1}); position at t=${t2}: (${x2}, ${y2})`,
    `Distance = sqrt((${x2}-${x1})^2 + (${y2}-${y1})^2) ~ ${round2(dist)}`,
    `Average speed = distance / time = ${round2(dist)} / ${t2 - t1} ~ ${answer}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  return buildMC(prompt, speed, (v) => `${v} m/s`, solution, [round2(speed + 1), round2(speed - 1), round2(dist)]);
}

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

function vectorValuedFunctions(difficulty, type) {
  const ax = randNonZero(-4, 4), bx = randInt(-5, 5);
  const ay = randNonZero(-4, 4), by = randInt(-5, 5);
  const t1 = randInt(0, 3);
  const t2 = t1 + randInt(1, 3 + difficulty);
  const r = (t) => [ax * t + bx, ay * t + by];
  const [x1, y1] = r(t1);
  const [x2, y2] = r(t2);
  const prompt = `A vector-valued function is r(t) = <${ax}t ${bx >= 0 ? "+" : "-"} ${Math.abs(bx)}, ${ay}t ${by >= 0 ? "+" : "-"} ${Math.abs(by)}>. Find the displacement vector from t = ${t1} to t = ${t2}.`;
  const answer = `<${x2 - x1}, ${y2 - y1}>`;
  const solution = [`r(${t1}) = <${x1}, ${y1}>, r(${t2}) = <${x2}, ${y2}>`, `Displacement = r(${t2}) - r(${t1}) = ${answer}`];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [`<${x1}, ${y1}>`, `<${x2}, ${y2}>`, `<${x1 - x2}, ${y1 - y2}>`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
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

function matrixModeling(difficulty, type) {
  const stateA = randInt(100, 500);
  const stateB = randInt(100, 500);
  const keepA = choice([0.7, 0.75, 0.8, 0.85]);
  const keepB = choice([0.6, 0.65, 0.7, 0.75]);
  const toB = round2(1 - keepA);
  const toA = round2(1 - keepB);
  const nextA = round2(keepA * stateA + toA * stateB);
  const nextB = round2(toB * stateA + keepB * stateB);
  const prompt =
    `Each year, ${Math.round(keepA * 100)}% of city A's residents stay and ${Math.round(toB * 100)}% move to city B; ` +
    `${Math.round(keepB * 100)}% of city B's residents stay and ${Math.round(toA * 100)}% move to city A. ` +
    `This year, city A has ${stateA} residents and city B has ${stateB}. Use the transition matrix [[${keepA}, ${toA}], [${toB}, ${keepB}]] to find next year's populations (A, B), rounded to the nearest whole number.`;
  const answer = `(${Math.round(nextA)}, ${Math.round(nextB)})`;
  const solution = [
    `[A', B'] = [[${keepA}, ${toA}], [${toB}, ${keepB}]] * [${stateA}, ${stateB}]`,
    `A' = ${keepA}(${stateA}) + ${toA}(${stateB}) ~ ${Math.round(nextA)}`,
    `B' = ${toB}(${stateA}) + ${keepB}(${stateB}) ~ ${Math.round(nextB)}`,
  ];
  if (type === "fr") return buildFR(prompt, answer, solution);
  const distractors = [`(${Math.round(nextB)}, ${Math.round(nextA)})`, `(${stateA}, ${stateB})`, `(${Math.round(nextA) + 10}, ${Math.round(nextB) - 10})`];
  return buildMC(prompt, answer, (v) => v, solution, distractors);
}

/* ============================ dispatcher =============================== */

const GENERATORS = {
  changeInTandem,
  rateOfChange,
  polynomialZeros,
  polynomialEndBehavior,
  rationalEndBehavior,
  rationalZeros,
  rationalAsymptotes,
  rationalHoles,
  equivalentExpressions,
  functionTransformations,
  modelSelection,
  sequences,
  linearVsExponential,
  exponentialFunctions,
  exponentialManipulation,
  exponentialModeling,
  compositionOfFunctions,
  inverseFunctions,
  logarithmExpressions,
  logFunctions,
  expLogEquations,
  semiLogPlots,
  periodicPhenomena: function periodicPhenomena(difficulty, type) {
    const period = choice([4, 6, 8, 10, 12]);
    const max = randInt(10, 30);
    const min = max - randInt(4, 12) * 2;
    const amp = (max - min) / 2;
    const mid = (max + min) / 2;
    const prompt = `A periodic phenomenon repeats every ${period} hours, reaching a maximum value of ${max} and a minimum value of ${min}. Find the amplitude and midline.`;
    const answer = `amplitude = ${amp}, midline = ${mid}`;
    const solution = [`Amplitude = (max - min)/2 = (${max} - ${min})/2 = ${amp}`, `Midline = (max + min)/2 = (${max} + ${min})/2 = ${mid}`];
    if (type === "fr") return buildFR(prompt, answer, solution);
    const distractors = [`amplitude = ${max}, midline = ${min}`, `amplitude = ${mid}, midline = ${amp}`, `amplitude = ${amp}, midline = ${mid + 2}`];
    return buildMC(prompt, answer, (v) => v, solution, distractors);
  },
  trigValues,
  trigGraphs,
  trigModeling,
  tangentFunction,
  inverseTrig,
  trigEquations,
  reciprocalTrig,
  trigIdentities,
  polarCoordinates,
  polarGraphs,
  parametricFunctions,
  parametricCirclesLines,
  parametricMotion,
  vectors,
  vectorValuedFunctions,
  matrices,
  matrixInverseDeterminant,
  linearTransformations,
  matrixModeling,
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
