/**
 * AP Precalculus curriculum structure (College Board Course and Exam
 * Description, Units 1-4) and the mapping from each topic to the
 * generator function that produces practice problems for it.
 */

const CURRICULUM = [
  {
    id: "U1",
    title: "Unit 1: Polynomial and Rational Functions",
    topics: [
      { id: "1.1", title: "Change in Tandem", gen: "changeInTandem" },
      { id: "1.2", title: "Rates of Change", gen: "rateOfChange" },
      { id: "1.3", title: "Rates of Change in Linear and Quadratic Functions", gen: "rateOfChange" },
      { id: "1.4", title: "Polynomial Functions and Rates of Change", gen: "polynomialZeros" },
      { id: "1.5", title: "Polynomial Functions and Complex Zeros", gen: "polynomialZeros" },
      { id: "1.6", title: "Polynomial Functions and End Behavior", gen: "polynomialEndBehavior" },
      { id: "1.7", title: "Rational Functions and End Behavior", gen: "rationalEndBehavior" },
      { id: "1.8", title: "Rational Functions and Zeros", gen: "rationalZeros" },
      { id: "1.9", title: "Rational Functions and Vertical Asymptotes", gen: "rationalAsymptotes" },
      { id: "1.10", title: "Rational Functions and Holes", gen: "rationalHoles" },
      { id: "1.11", title: "Equivalent Representations of Polynomial and Rational Expressions", gen: "equivalentExpressions" },
      { id: "1.12", title: "Transformations of Functions", gen: "functionTransformations" },
      { id: "1.13", title: "Function Model Selection and Assumptions", gen: "modelSelection" },
    ],
  },
  {
    id: "U2",
    title: "Unit 2: Exponential and Logarithmic Functions",
    topics: [
      { id: "2.1", title: "Change in Arithmetic and Geometric Sequences", gen: "sequences" },
      { id: "2.2", title: "Change in Linear and Exponential Functions", gen: "linearVsExponential" },
      { id: "2.3", title: "Exponential Functions", gen: "exponentialFunctions" },
      { id: "2.4", title: "Exponential Function Manipulation", gen: "exponentialManipulation" },
      { id: "2.5", title: "Exponential Function Context and Data Modeling", gen: "exponentialModeling" },
      { id: "2.6", title: "Competing Function Model Validation", gen: "modelSelection" },
      { id: "2.7", title: "Composition of Functions", gen: "compositionOfFunctions" },
      { id: "2.8", title: "Inverse Functions", gen: "inverseFunctions" },
      { id: "2.9", title: "Logarithmic Expressions", gen: "logarithmExpressions" },
      { id: "2.10", title: "Inverses of Exponential Functions", gen: "inverseFunctions" },
      { id: "2.11", title: "Logarithmic Functions", gen: "logFunctions" },
      { id: "2.12", title: "Logarithmic Function Manipulation", gen: "logarithmExpressions" },
      { id: "2.13", title: "Exponential and Logarithmic Equations and Inequalities", gen: "expLogEquations" },
      { id: "2.14", title: "Logarithmic Function Context and Data Modeling", gen: "exponentialModeling" },
      { id: "2.15", title: "Semi-log Plots", gen: "semiLogPlots" },
    ],
  },
  {
    id: "U3",
    title: "Unit 3: Trigonometric and Polar Functions",
    topics: [
      { id: "3.1", title: "Periodic Phenomena", gen: "periodicPhenomena" },
      { id: "3.2", title: "Sine, Cosine, and Tangent", gen: "trigValues" },
      { id: "3.3", title: "Sine and Cosine Function Values", gen: "trigValues" },
      { id: "3.4", title: "Sine and Cosine Function Graphs", gen: "trigGraphs" },
      { id: "3.5", title: "Sinusoidal Functions", gen: "trigGraphs" },
      { id: "3.6", title: "Sinusoidal Function Context and Data Modeling", gen: "trigModeling" },
      { id: "3.7", title: "The Tangent Function", gen: "tangentFunction" },
      { id: "3.8", title: "Inverse Trigonometric Functions", gen: "inverseTrig" },
      { id: "3.9", title: "Trigonometric Equations and Inequalities", gen: "trigEquations" },
      { id: "3.10", title: "The Secant, Cosecant, and Cotangent Functions", gen: "reciprocalTrig" },
      { id: "3.11", title: "Equivalent Representations of Trigonometric Functions", gen: "trigIdentities" },
      { id: "3.12", title: "Trigonometry and Polar Coordinates", gen: "polarCoordinates" },
      { id: "3.13", title: "Polar Function Graphs", gen: "polarGraphs" },
      { id: "3.14", title: "Rates of Change in Polar Functions", gen: "polarGraphs" },
    ],
  },
  {
    id: "U4",
    title: "Unit 4: Functions Involving Parameters, Vectors, and Matrices",
    topics: [
      { id: "4.1", title: "Parametric Functions", gen: "parametricFunctions" },
      { id: "4.2", title: "Parametric Functions and Rates of Change", gen: "parametricFunctions" },
      { id: "4.3", title: "Parametrically Defined Circles and Lines", gen: "parametricCirclesLines" },
      { id: "4.4", title: "Parametrization of Implicitly Defined Functions", gen: "parametricFunctions" },
      { id: "4.5", title: "Parametric Functions and Motion", gen: "parametricMotion" },
      { id: "4.6", title: "Vectors", gen: "vectors" },
      { id: "4.7", title: "Vector-Valued Functions", gen: "vectorValuedFunctions" },
      { id: "4.8", title: "Matrices", gen: "matrices" },
      { id: "4.9", title: "The Inverse and Determinant of a Matrix", gen: "matrixInverseDeterminant" },
      { id: "4.10", title: "Linear Transformations and Matrices", gen: "linearTransformations" },
      { id: "4.11", title: "Matrices as Functions", gen: "matrices" },
      { id: "4.12", title: "Matrices Modeling Contexts", gen: "matrixModeling" },
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
