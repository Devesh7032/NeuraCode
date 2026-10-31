// @vitest-environment jsdom
import { describe, it, expect, vi, beforeEach } from "vitest";
import React from "react";
import { BRAND_CONFIG } from "./config/brand";

// Mock Monaco Editor as it uses canvas and browser APIs not supported in jsdom
vi.mock("@monaco-editor/react", () => ({
  default: () => <textarea data-testid="mock-monaco-editor" />
}));

describe("Branding Configuration", () => {
  it("uses the correct project title", () => {
    expect(BRAND_CONFIG.name).toBe("NeuraCode");
  });

  it("has custom navigation menu entries", () => {
    expect(BRAND_CONFIG.navigation.length).toBeGreaterThan(0);
    expect(BRAND_CONFIG.navigation[0].label).toBe("Dashboard");
  });
});

describe("AI/ML Challenge Tags Mappings", () => {
  const challengeTags: Record<string, string[]> = {
    "sigmoid-activation": ["math", "activation", "neural-networks"],
    "mean-squared-error": ["loss-functions", "regression", "metrics"],
    "single-step-gradient-descent": ["optimization", "gradient-descent", "math"],
    "self-attention-weights": ["transformers", "attention-weights", "nlp"]
  };

  it("assigns matching mathematical tags for sigmoid", () => {
    const tags = challengeTags["sigmoid-activation"];
    expect(tags).toContain("activation");
    expect(tags).toContain("math");
  });

  it("assigns matching transformer tags for attention weights", () => {
    const tags = challengeTags["self-attention-weights"];
    expect(tags).toContain("transformers");
    expect(tags).toContain("nlp");
  });
});

describe("Code Draft localStorage Simulation", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("reads default template if no draft exists in localStorage", () => {
    const slug = "sigmoid-activation";
    const starterCode = "def sigmoid(z): pass";
    const savedDraft = localStorage.getItem(`neuracode_draft_${slug}`);
    
    expect(savedDraft).toBeNull();
    const activeCode = savedDraft || starterCode;
    expect(activeCode).toBe(starterCode);
  });

  it("retrieves saved draft from localStorage successfully", () => {
    const slug = "sigmoid-activation";
    const userDraft = "def sigmoid(z):\n    return 1 / (1 + math.exp(-z))";
    
    localStorage.setItem(`neuracode_draft_${slug}`, userDraft);
    const savedDraft = localStorage.getItem(`neuracode_draft_${slug}`);
    
    expect(savedDraft).toBe(userDraft);
  });
});

describe("Problems Filter Search Utility Simulation", () => {
  const sampleChallenges = [
    { title: "Sigmoid Activation Function", category: "Mathematics", difficulty: "Easy" },
    { title: "Mean Squared Error (MSE)", category: "Machine Learning", difficulty: "Easy" },
    { title: "Single-Step Gradient Descent", category: "Machine Learning", difficulty: "Medium" }
  ];

  it("filters challenges by search query correctly", () => {
    const query = "gradient";
    const filtered = sampleChallenges.filter(c => 
      c.title.toLowerCase().includes(query.toLowerCase())
    );
    expect(filtered.length).toBe(1);
    expect(filtered[0].title).toBe("Single-Step Gradient Descent");
  });

  it("filters challenges by category correctly", () => {
    const category = "Machine Learning";
    const filtered = sampleChallenges.filter(c => c.category === category);
    expect(filtered.length).toBe(2);
  });
});
