/**
 * Converts the Precalc Problem Generator's ASCII pseudo-math notation into
 * KaTeX-renderable LaTeX, wrapping individual math tokens in \( ... \)
 * (NOT $...$, since several generators emit literal "$" currency signs).
 * Applied to prompt/choice/answer/solution strings at render time, so none
 * of the generator functions need to change.
 *
 * Every conversion goes through protect(), which replaces the LaTeX with an
 * opaque placeholder token wrapped in control characters that can never
 * appear in generated worksheet text (so it can never collide with a plain
 * number already in that text). That guarantees later rules in this same
 * pass can never re-scan, re-wrap, or reach inside and corrupt text a prior
 * rule already converted: each token is touched exactly once, in a fixed
 * priority order (most specific structures first).
 */

function mathify(text) {
  if (typeof text !== "string" || !text) return text;

  let s = text;
  const placeholders = [];
  function protect(latex) {
    const token = `\u0001${placeholders.length}\u0002`;
    placeholders.push(`\\(${latex}\\)`);
    return token;
  }

  // Fixes safe to apply to text captured *inside* a structure (sqrt/frac/
  // binom argument) before that structure is wrapped and protected: LaTeX
  // needs braced exponents, and these commands render fine unprotected
  // since they never contain top-level \( \) of their own.
  function bodyify(inner) {
    let b = inner;
    b = b.replace(/\^\(([^()]*)\)/g, (_, e) => `^{${e.replace(/\*/g, "\\cdot ")}}`);
    b = b.replace(/(?<=[a-zA-Z0-9)\]}])\^(-?[a-zA-Z0-9]+)/g, (_, e) => `^{${e}}`);
    b = b.replace(/\btheta\b/g, "\\theta");
    b = b.replace(/\bpi\b/g, "\\pi");
    b = b.replace(/\*/g, "\\cdot ");
    return b;
  }

  // 1. sqrt(N)/D  ->  \(\frac{\sqrt{N}}{D}\)   (exact trig values etc.)
  s = s.replace(/sqrt\(((?:[^()]|\([^()]*\))*)\)\/(-?\d+)/g, (_, inner, den) => protect(`\\frac{\\sqrt{${bodyify(inner)}}}{${den}}`));

  // 2. remaining sqrt(EXPR) -> \(\sqrt{EXPR}\), one level of nested parens allowed
  s = s.replace(/sqrt\(((?:[^()]|\([^()]*\))*)\)/g, (_, inner) => protect(`\\sqrt{${bodyify(inner)}}`));

  // 3. C(n, k) binomial coefficient notation -> \(\binom{n}{k}\)
  s = s.replace(/\bC\(([a-zA-Z0-9]+),\s*([a-zA-Z0-9]+)\)/g, (_, a, b) => protect(`\\binom{${a}}{${b}}`));

  // 4. 2x2 matrix literal [[a, b], [c, d]] -> bmatrix
  s = s.replace(
    /\[\[\s*(-?[\w.]+)\s*,\s*(-?[\w.]+)\s*\]\s*,\s*\[\s*(-?[\w.]+)\s*,\s*(-?[\w.]+)\s*\]\]/g,
    (_, a, b, c, d) => protect(`\\begin{bmatrix} ${a} & ${b} \\\\ ${c} & ${d} \\end{bmatrix}`)
  );

  // 4b. 2x2 determinant bars |a b; c d| (Cramer's Rule notation) -> vmatrix.
  //     Must run before the generic absolute-value-bars rule below.
  s = s.replace(
    /\|(-?[\w.]+)\s+(-?[\w.]+);\s*(-?[\w.]+)\s+(-?[\w.]+)\|/g,
    (_, a, b, c, d) => protect(`\\begin{vmatrix} ${a} & ${b} \\\\ ${c} & ${d} \\end{vmatrix}`)
  );

  // 5. vectors: <a, b, c> (3-component) then <a, b> (2-component)
  s = s.replace(/<\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*>/g, (_, a, b, c) => protect(`\\langle ${a},\\ ${b},\\ ${c} \\rangle`));
  s = s.replace(/<\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*>/g, (_, a, b) => protect(`\\langle ${a},\\ ${b} \\rangle`));

  // 6. relational operators (word-boundary safe: these are always used as ASCII digraphs here)
  s = s.replace(/<=/g, () => protect("\\leq"));
  s = s.replace(/>=/g, () => protect("\\geq"));
  s = s.replace(/!=/g, () => protect("\\neq"));

  // 7. limit / approach arrow
  s = s.replace(/->/g, () => protect("\\to"));

  // 8. exponents: parenthesized group first, then bare token
  s = s.replace(/\^\(([^()]*)\)/g, (_, inner) => protect(`^{${inner.replace(/\*/g, "\\cdot ")}}`));
  s = s.replace(/(?<=[a-zA-Z0-9)\]}])\^(-?[a-zA-Z0-9]+)/g, (_, exp) => protect(`^{${exp}}`));

  // 9. trig / log / inverse-trig function names. Only the name is protected;
  //    the literal "(" that follows is left as plain text so the argument
  //    inside is still visible to the rules below (fractions, theta, ...).
  s = s.replace(/\b(arcsin|arccos|arctan|sin|cos|tan|csc|sec|cot|log|ln)(?=\()/g, (_, fn) => protect("\\" + fn));

  // 10. greek letters (word-boundary bare words); a leading digit run like
  //     "2theta" has no word boundary before "theta", so handle that
  //     coefficient-prefixed form first (common in double-angle formulas).
  s = s.replace(/(\d+)theta\b/g, (_, n) => protect(`${n}\\theta`));
  s = s.replace(/\bpi\b/g, () => protect("\\pi"));
  s = s.replace(/\btheta\b/g, () => protect("\\theta"));
  s = s.replace(/\bphi\b/g, () => protect("\\phi"));

  // 11. infinity
  s = s.replace(/\binfinity\b/g, () => protect("\\infty"));

  // 12. dot product, restricted to the small set of variable names this generator
  //     actually uses for vectors/matrices, to avoid false positives in prose.
  s = s.replace(/\b([uvwAB])\s\.\s([uvwAB])\b/g, (_, a, b) => protect(`${a} \\cdot ${b}`));

  // 13. bare integer fractions (e.g. "7/6", "-1/2"), but never when either side
  //     is actually part of a decimal number (e.g. skip inside "0.05/12").
  s = s.replace(/(?<![\d.])(-?\d+)\/(-?\d+)(?![\d.])/g, (_, n, d) => protect(`\\frac{${n}}{${d}}`));

  // 14. absolute value bars |EXPR| (simple, non-nested)
  s = s.replace(/\|([^|]+)\|/g, (_, inner) => protect(`\\left|${inner}\\right|`));

  // Restore placeholders. The sentinel wrapper (\u0001 ... \u0002) guarantees
  // this only ever matches a real placeholder token, never a plain number
  // already present in the text.
  s = s.replace(/\u0001(\d+)\u0002/g, (_, i) => placeholders[Number(i)]);

  return s;
}
