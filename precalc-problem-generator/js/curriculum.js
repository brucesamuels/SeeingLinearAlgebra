/**
 * Brooklyn Tech Precalculus curriculum structure (11 units, per the
 * department's curriculum map) and the mapping from each topic to the
 * generator function that produces practice problems for it.
 */

const CURRICULUM = [
  {
    id: "U1",
    title: "Unit 1: Functions",
    topics: [
      { id: "1.1", title: "Domain of a Function and a Composition", gen: "domainOfComposition" },
      { id: "1.2", title: "Composition of Functions", gen: "compositionOfFunctions" },
      { id: "1.3", title: "Piecewise Functions", gen: "piecewiseFunctions" },
      { id: "1.4", title: "Absolute Value Functions", gen: "absoluteValueFunctions" },
      { id: "1.5", title: "Intuitive Concept of a Limit", gen: "intuitiveLimit" },
      { id: "1.6", title: "Intermediate Value Theorem", gen: "intermediateValueTheorem" },
      { id: "1.7", title: "Average Rate of Change", gen: "rateOfChange" },
      { id: "1.8", title: "Transformations of Functions", gen: "functionTransformations" },
      { id: "1.9", title: "Inverse Functions", gen: "inverseFunctions" },
    ],
  },
  {
    id: "U2",
    title: "Unit 2: Polynomials",
    topics: [
      { id: "2.1", title: "Long and Synthetic Division", gen: "polynomialDivision" },
      { id: "2.2", title: "Remainder and Factor Theorems", gen: "remainderFactorTheorem" },
      { id: "2.3", title: "Linear Factorization Theorem and Multiplicity of Roots", gen: "polynomialZeros" },
      { id: "2.4", title: "Complex Numbers", gen: "complexNumberArithmetic" },
      { id: "2.5", title: "Fundamental Theorem of Algebra", gen: "fundamentalTheoremAlgebra" },
      { id: "2.6", title: "Rational Root Theorem", gen: "rationalRootTheorem" },
      { id: "2.7", title: "Conjugate Zeros Theorem", gen: "conjugateZerosTheorem" },
      { id: "2.8", title: "Sum and Product of the Roots", gen: "sumProductRoots" },
      { id: "2.9", title: "Permutations and Combinations", gen: "permutationsCombinations" },
      { id: "2.10", title: "Binomial Expansion Theorem and Pascal's Triangle", gen: "binomialExpansion" },
      { id: "2.11", title: "Binomial Probability Distribution", gen: "binomialProbability" },
    ],
  },
  {
    id: "U3",
    title: "Unit 3: Rational Functions",
    topics: [
      { id: "3.1", title: "Vertical and Horizontal Asymptotes", gen: "verticalHorizontalAsymptotes" },
      { id: "3.2", title: "Slant Asymptotes", gen: "slantAsymptotes" },
      { id: "3.3", title: "Holes vs. Asymptotes", gen: "rationalHoles" },
      { id: "3.4", title: "One-Sided and Infinite Limits", gen: "oneSidedInfiniteLimits" },
      { id: "3.5", title: "Rational Inequalities", gen: "rationalInequalities" },
      { id: "3.6", title: "Partial Fraction Decomposition", gen: "partialFractions" },
      { id: "3.7", title: "Rational Equations", gen: "rationalEquations" },
    ],
  },
  {
    id: "U4",
    title: "Unit 4: Exponential and Logarithmic Functions",
    topics: [
      { id: "4.1", title: "Properties of Logarithms", gen: "logarithmExpressions" },
      { id: "4.2", title: "Exponential Equations", gen: "expLogEquations" },
      { id: "4.3", title: "Logarithmic Equations", gen: "expLogEquations" },
      { id: "4.4", title: "Compound Interest", gen: "compoundInterest" },
      { id: "4.5", title: "Population Growth and Radioactive Decay", gen: "exponentialModeling" },
    ],
  },
  {
    id: "U5",
    title: "Unit 5: Conic Sections",
    topics: [
      { id: "5.1", title: "Parabolas", gen: "parabolas" },
      { id: "5.2", title: "Ellipses", gen: "ellipses" },
      { id: "5.3", title: "Hyperbolas", gen: "hyperbolas" },
      { id: "5.4", title: "Classifying Conic Sections", gen: "classifyConics" },
    ],
  },
  {
    id: "U6",
    title: "Unit 6: Trigonometric Functions",
    topics: [
      { id: "6.1", title: "The Unit Circle and Six Trig Functions", gen: "trigValuesReciprocal" },
      { id: "6.2", title: "Expressing Trig Functions Using Others", gen: "expressTrigUsingOthers" },
      { id: "6.3", title: "Graphs of Sine and Cosine", gen: "trigGraphs" },
      { id: "6.4", title: "Graphs of Tangent, Secant, Cosecant, Cotangent", gen: "tanSecCscCotGraphs" },
      { id: "6.5", title: "Inverse Trigonometric Functions", gen: "inverseTrig" },
      { id: "6.6", title: "Right Triangle Trigonometry", gen: "rightTriangleTrig" },
    ],
  },
  {
    id: "U7",
    title: "Unit 7: Analytic Trigonometry",
    topics: [
      { id: "7.1", title: "Fundamental Trig Identities", gen: "trigIdentities" },
      { id: "7.2", title: "Sum and Difference Formulas", gen: "sumDifferenceFormulas" },
      { id: "7.3", title: "Double-Angle and Half-Angle Formulas", gen: "doubleHalfAngle" },
      { id: "7.4", title: "Solving Trigonometric Equations", gen: "trigEquations" },
      { id: "7.5", title: "Harmonic Motion (A sin x + B cos x)", gen: "harmonicMotion" },
    ],
  },
  {
    id: "U8",
    title: "Unit 8: Additional Topics of Trigonometry",
    topics: [
      { id: "8.1", title: "Law of Sines", gen: "lawOfSines" },
      { id: "8.2", title: "Law of Cosines", gen: "lawOfCosines" },
      { id: "8.3", title: "Heron's Formula", gen: "heronsFormula" },
      { id: "8.4", title: "The Ambiguous Case (SSA)", gen: "lawOfSines" },
      { id: "8.5", title: "Trigonometric Form of Complex Numbers", gen: "trigFormComplex" },
      { id: "8.6", title: "De Moivre's Theorem", gen: "deMoivresTheorem" },
      { id: "8.7", title: "Roots of a Complex Number", gen: "rootsOfComplex" },
    ],
  },
  {
    id: "U9",
    title: "Unit 9: Parametric Equations and Polar Coordinates",
    topics: [
      { id: "9.1", title: "Parametric Curves and Rectangular Conversion", gen: "parametricCurves" },
      { id: "9.2", title: "Parametric Lines and Conics", gen: "parametricCirclesLines" },
      { id: "9.3", title: "Polar and Rectangular Conversion", gen: "polarCoordinates" },
      { id: "9.4", title: "Polar Equations of Curves", gen: "polarGraphs" },
    ],
  },
  {
    id: "U10",
    title: "Unit 10: Vectors and Matrices",
    topics: [
      { id: "10.1", title: "Vector Operations", gen: "vectors" },
      { id: "10.2", title: "Norm and Dot Product", gen: "dotProduct" },
      { id: "10.3", title: "Perpendicular Vectors and Angle Between Vectors", gen: "perpendicularAngleBetween" },
      { id: "10.4", title: "Distance from a Point to a Plane", gen: "distancePointToPlane" },
      { id: "10.5", title: "Matrix Operations", gen: "matrices" },
      { id: "10.6", title: "Matrices as Transformations", gen: "linearTransformations" },
      { id: "10.7", title: "Inverse Matrix and Determinant", gen: "matrixInverseDeterminant" },
      { id: "10.8", title: "Cramer's Rule", gen: "cramersRule" },
    ],
  },
  {
    id: "U11",
    title: "Unit 11: Sequences and Series",
    topics: [
      { id: "11.1", title: "Arithmetic and Geometric Sequences", gen: "sequences" },
      { id: "11.2", title: "Recursive Sequences and the Fibonacci Sequence", gen: "recursiveFibonacci" },
      { id: "11.3", title: "Infinite Geometric Series", gen: "infiniteGeometricSeries" },
      { id: "11.4", title: "Financial Applications", gen: "financialApplications" },
      { id: "11.5", title: "Mathematical Induction", gen: "mathematicalInduction" },
      { id: "11.6", title: "Telescoping Series", gen: "telescopingSeries" },
      { id: "11.7", title: "Limits of Sequences", gen: "limitsOfSequences" },
    ],
  },
];

// Flat lookup: topic id -> { unitId, unitTitle, title, gen }
const TOPIC_INDEX = {};
CURRICULUM.forEach((unit) => {
  unit.topics.forEach((topic) => {
    TOPIC_INDEX[topic.id] = {
      unitId: unit.id,
      unitTitle: unit.title,
      title: topic.title,
      gen: topic.gen,
    };
  });
});
