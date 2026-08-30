/*
 * curriculum.js — AP Calculus AB/BC units and topics used to populate the
 * Unit/Topic selector. Every topic listed here has a matching generator in
 * generators.js (see the `topic` field on each generator's output).
 */

const AP_CALC_CURRICULUM = [
  {
    unit: 1, course: 'both', name: 'Limits and Continuity',
    topics: [
      { code: '1.1', name: 'Evaluating Limits by Factoring' },
      { code: '1.2', name: 'Limits at Infinity (End Behavior)' },
      { code: '1.3', name: 'Continuity: Solving for a Constant' },
    ],
  },
  {
    unit: 2, course: 'both', name: 'Differentiation: Basic Rules',
    topics: [
      { code: '2.1', name: 'The Power Rule' },
      { code: '2.2', name: 'Derivatives of Trig, Exponential & Log Sums' },
      { code: '2.3', name: 'The Product Rule' },
      { code: '2.4', name: 'The Quotient Rule' },
    ],
  },
  {
    unit: 3, course: 'both', name: 'Composite, Implicit & Inverse Functions',
    topics: [
      { code: '3.1', name: 'The Chain Rule (Evaluate Numerically)' },
      { code: '3.2', name: 'The Chain Rule (Symbolic Derivative)' },
      { code: '3.3', name: 'Implicit Differentiation' },
      { code: '3.4', name: 'Derivatives of Inverse Functions' },
    ],
  },
  {
    unit: 4, course: 'both', name: 'Contextual Applications of Differentiation',
    topics: [
      { code: '4.1', name: 'Motion: Position, Velocity & Acceleration' },
      { code: '4.2', name: 'Related Rates' },
      { code: '4.3', name: 'Local Linearization (Tangent Line Approximation)' },
      { code: '4.4', name: "L'Hôpital's Rule" },
    ],
  },
  {
    unit: 5, course: 'both', name: 'Analytical Applications of Differentiation',
    topics: [
      { code: '5.1', name: 'Increasing/Decreasing & the First Derivative Test' },
      { code: '5.2', name: 'Concavity & the Second Derivative Test' },
      { code: '5.3', name: 'Optimization Problems' },
    ],
  },
  {
    unit: 6, course: 'both', name: 'Integration and Accumulation of Change',
    topics: [
      { code: '6.1', name: 'Definite Integrals (FTC)' },
      { code: '6.2', name: 'Accumulation Functions (FTC Part 1)' },
      { code: '6.3', name: 'Antiderivatives by u-Substitution' },
    ],
  },
  {
    unit: 7, course: 'both', name: 'Differential Equations',
    topics: [
      { code: '7.1', name: 'Separable Differential Equations' },
      { code: '7.2', name: 'Exponential Growth and Decay' },
    ],
  },
  {
    unit: 8, course: 'both', name: 'Applications of Integration',
    topics: [
      { code: '8.1', name: 'Average Value of a Function' },
      { code: '8.2', name: 'Area Between Two Curves' },
      { code: '8.3', name: 'Volumes of Revolution (Disk/Washer)' },
    ],
  },
  {
    unit: 9, course: 'bc', name: 'Parametric, Polar & Vector-Valued Functions',
    topics: [
      { code: '9.1', name: 'Derivatives of Parametric Equations' },
      { code: '9.2', name: 'Area of a Polar Region' },
    ],
  },
  {
    unit: 10, course: 'bc', name: 'Infinite Sequences and Series',
    topics: [
      { code: '10.1', name: 'Geometric Series' },
      { code: '10.2', name: 'Maclaurin Polynomials' },
      { code: '10.3', name: 'Radius of Convergence (Ratio Test)' },
    ],
  },
];

if (typeof module !== 'undefined') {
  module.exports = { AP_CALC_CURRICULUM };
}
