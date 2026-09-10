/* Converts the plain-ASCII math notation used throughout the generators and
   question bank (sqrt(...), lambda, dot/cross products) into real LaTeX,
   wrapped in \( \) so KaTeX's auto-render (see js/app.js) can typeset it.
   Matrices already arrive pre-wrapped in \( \) from js/render.js -- this
   only has to handle the ASCII math that appears in ordinary prose lines.

   Each rule below immediately replaces its match with an opaque placeholder
   token before moving to the next rule, so no later rule can ever re-match
   or nest inside text an earlier rule already converted. */
function mathify(str) {
  if (typeof str !== "string" || str.indexOf === undefined) return str;

  const placeholders = [];
  function protect(latex) {
    placeholders.push(latex);
    return "\x01" + (placeholders.length - 1) + "\x02";
  }

  let s = str;

  // Fix up a rare inline "sigma_2^2" style subscript+exponent so it reads
  // correctly once wrapped in real math mode below.
  s = s.replace(/\bsigma_(\d+)\^(\d+)/g, (_m, i, p) => `\\sigma_{${i}}^{${p}}`);

  // Bars around a cross product, e.g. "|u x v|" (norm of a cross product).
  s = s.replace(/\|([uvw]\d?)\s+x\s+([uvw]\d?)\|/g, (_m, a, b) => protect(`\\(\\|${a} \\times ${b}\\|\\)`));

  // Bars around a single vector, e.g. "|u|" (a vector's length/norm).
  s = s.replace(/\|([uvw]\d?)\|/g, (_m, a) => protect(`\\(\\|${a}\\|\\)`));

  // Cross product: u x v (only single-letter vector names u/v/w).
  s = s.replace(/\b([uvw]\d?)\s+x\s+([uvw]\d?)\b/g, (_m, a, b) => protect(`\\(${a} \\times ${b}\\)`));

  // Dot product: u . v (only single-letter vector names u/v/w).
  s = s.replace(/\b([uvw]\d?)\s+\.\s+([uvw]\d?)\b/g, (_m, a, b) => protect(`\\(${a} \\cdot ${b}\\)`));

  // sqrt(...) -- arguments here are always a single flat expression (no
  // nested parens), so a simple non-nested match is safe.
  s = s.replace(/sqrt\(([^()]*)\)/g, (_m, inner) => protect(`\\(\\sqrt{${inner}}\\)`));

  // The characteristic-polynomial equation built by charPoly2Text():
  // "lambda^2 - (A)*lambda + (B) = 0".
  s = s.replace(/lambda\^2 - \(([^()]*)\)\*lambda \+ \(([^()]*)\) = 0/g,
    (_m, a, b) => protect(`\\(\\lambda^2 - (${a})\\lambda + (${b}) = 0\\)`));

  // "lambda = N" / "lambda1 = N" assignments.
  s = s.replace(/\blambda(\d?)\s*=\s*(-?\d+(?:\/\d+)?)/g,
    (_m, sub, val) => protect(`\\(\\lambda${sub ? "_{" + sub + "}" : ""} = ${val}\\)`));

  // Any remaining bare "lambda" (as a symbol in prose, e.g. "eigenvalue lambda").
  s = s.replace(/\blambda\b/g, () => protect("\\(\\lambda\\)"));

  s = s.replace(/\x01(\d+)\x02/g, (_m, i) => placeholders[Number(i)]);
  return s;
}

if (typeof module !== "undefined") module.exports = { mathify };
