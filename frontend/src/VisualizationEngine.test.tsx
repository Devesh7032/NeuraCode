// @vitest-environment jsdom
import { describe, it, expect, vi } from "vitest";
import React from "react";
import { render, screen } from "@testing-library/react";
import { VisualizationEngine } from "./components/VisualizationEngine";

describe("VisualizationEngine Trace Rendering Tests", () => {
  const dummyOnRun = vi.fn();

  it("renders idle state message when visualizationData is null but visualization_type exists", () => {
    const challenge = {
      id: "ch1",
      title: "Gradient Descent Step",
      slug: "single-step-gradient-descent",
      description: "Perform single update step",
      difficulty: "Easy",
      category: "Machine Learning",
      starter_code: "def gradient_update(w, dw, learning_rate): pass",
      visualization_type: "GRADIENT_DESCENT",
      visualization_config: '{"learning_rate_default": 0.1}',
      tests: [],
      hints: []
    };

    render(
      <VisualizationEngine
        challenge={challenge}
        visualizationData={null}
        onRunExperiment={dummyOnRun}
        running={false}
      />
    );

    expect(screen.getByText("Visual Experiment Idle")).toBeDefined();
    expect(screen.getByText(/Run your solution first to generate real data-driven trace representations/i)).toBeDefined();
  });

  it("renders empty message when challenge has no visualization_type", () => {
    const challenge = {
      id: "ch2",
      title: "No Vis Challenge",
      slug: "no-vis",
      description: "No vis",
      difficulty: "Easy",
      category: "Python",
      starter_code: "pass",
      tests: [],
      hints: []
    };

    render(
      <VisualizationEngine
        challenge={challenge}
        visualizationData={null}
        onRunExperiment={dummyOnRun}
        running={false}
      />
    );

    expect(screen.getByText("No visualization configuration is defined for this challenge.")).toBeDefined();
  });

  it("renders Gradient Descent visualization with real trace data", () => {
    const challenge = {
      id: "ch-gd",
      title: "Gradient Descent Step",
      slug: "single-step-gradient-descent",
      difficulty: "Easy",
      category: "Machine Learning",
      starter_code: "def gradient_update(w, dw, learning_rate): return w - learning_rate * dw",
      visualization_type: "GRADIENT_DESCENT",
      visualization_config: '{}',
      tests: [],
      hints: []
    };

    const visData = {
      type: "GRADIENT_DESCENT",
      learning_rate: 0.1,
      target_weight: 2.0,
      steps: [
        { epoch: 0, loss: 4.0, weight: 0.0, derivative: -4.0, w_new: 0.4 },
        { epoch: 1, loss: 2.56, weight: 0.4, derivative: -3.2, w_new: 0.72 }
      ]
    };

    render(
      <VisualizationEngine
        challenge={challenge}
        visualizationData={visData}
        onRunExperiment={dummyOnRun}
        running={false}
      />
    );

    expect(screen.getByText("📉 Iterative Gradient Descent Convergence")).toBeDefined();
    expect(screen.getByText("Mathematical Update Relationship")).toBeDefined();
    expect(screen.getByText("w_new = w - (learning_rate × dw)")).toBeDefined();
    expect(screen.getByText("Visual Parameter Movement Track (w → w_new)")).toBeDefined();
  });

  it("renders Sigmoid Function visualization with trace data", () => {
    const challenge = {
      id: "ch-sig",
      title: "Sigmoid Activation Function",
      slug: "sigmoid-activation",
      difficulty: "Easy",
      category: "Machine Learning",
      starter_code: "def sigmoid(z): pass",
      visualization_type: "FUNCTION",
      tests: [],
      hints: []
    };

    const visData = {
      type: "FUNCTION",
      x: [-2.0, 0.0, 2.0],
      y: [0.1192, 0.5, 0.8808],
      custom_x: 2.0,
      custom_y: 0.8808
    };

    render(
      <VisualizationEngine
        challenge={challenge}
        visualizationData={visData}
        onRunExperiment={dummyOnRun}
        running={false}
      />
    );

    expect(screen.getByText(/Mathematical Function Trace/i)).toBeDefined();
  });

  it("renders Matrix Multiplication visualization with trace data", () => {
    const challenge = {
      id: "ch-mm",
      title: "Matrix Multiplication",
      slug: "matrix-multiplication",
      difficulty: "Easy",
      category: "Mathematics",
      starter_code: "def matrix_multiply(A, B): pass",
      visualization_type: "MATRIX_MULTIPLICATION",
      tests: [],
      hints: []
    };

    const visData = {
      type: "MATRIX_MULTIPLICATION",
      matrix_a: [[1, 2], [3, 4]],
      matrix_b: [[2, 0], [1, 2]],
      matrix_c: [[4, 4], [10, 8]]
    };

    render(
      <VisualizationEngine
        challenge={challenge}
        visualizationData={visData}
        onRunExperiment={dummyOnRun}
        running={false}
      />
    );

    expect(screen.getByText(/Matrix Multiplication \(A × B = C\)/i)).toBeDefined();
  });
});
