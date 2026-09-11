import { describe, it, expect } from "vitest";
import { winProbability, expectedValue, recommendation, simulatePortfolio } from "../simulator";

describe("winProbability", () => {
  it("croît avec la compatibilité", () => {
    const low = winProbability({ confidence: 0.4, seniority: "mid", budget: 1000 });
    const high = winProbability({ confidence: 0.9, seniority: "mid", budget: 1000 });
    expect(high.probability).toBeGreaterThan(low.probability);
  });

  it("avantage les profils seniors", () => {
    const mid = winProbability({ confidence: 0.6, seniority: "mid", budget: 1000 });
    const senior = winProbability({ confidence: 0.6, seniority: "senior", budget: 1000 });
    expect(senior.probability).toBeGreaterThan(mid.probability);
  });

  it("pénalise la concurrence sur les gros budgets", () => {
    const small = winProbability({ confidence: 0.6, seniority: "mid", budget: 1000 });
    const big = winProbability({ confidence: 0.6, seniority: "mid", budget: 40000 });
    expect(big.probability).toBeLessThan(small.probability);
  });

  it("borne la probabilité dans [0.02, 0.95]", () => {
    const p = winProbability({ confidence: 1, seniority: "senior", budget: null }).probability;
    expect(p).toBeLessThanOrEqual(0.95);
    expect(p).toBeGreaterThanOrEqual(0.02);
  });
});

describe("expectedValue", () => {
  it("= budget × probabilité, 0 si budget inconnu", () => {
    expect(expectedValue(10000, 0.3)).toBe(3000);
    expect(expectedValue(null, 0.9)).toBe(0);
  });
});

describe("recommendation", () => {
  it("seuils strong/consider/skip", () => {
    expect(recommendation(0.7)).toBe("strong");
    expect(recommendation(0.4)).toBe("consider");
    expect(recommendation(0.1)).toBe("skip");
  });
});

describe("simulatePortfolio", () => {
  it("est déterministe à seed fixe", () => {
    const items = [{ probability: 0.5, budget: 10000 }, { probability: 0.3, budget: 5000 }];
    const a = simulatePortfolio(items, { trials: 500, seed: 7 });
    const b = simulatePortfolio(items, { trials: 500, seed: 7 });
    expect(a).toEqual(b);
  });

  it("approche l'espérance théorique Σ(p×budget)", () => {
    const items = [{ probability: 0.5, budget: 10000 }, { probability: 0.2, budget: 5000 }];
    const sim = simulatePortfolio(items, { trials: 5000, seed: 1 });
    // théorique = 5000 + 1000 = 6000
    expect(Math.abs(sim.expectedRevenue - 6000)).toBeLessThan(500);
    expect(sim.p10).toBeLessThanOrEqual(sim.p50);
    expect(sim.p50).toBeLessThanOrEqual(sim.p90);
  });
});
