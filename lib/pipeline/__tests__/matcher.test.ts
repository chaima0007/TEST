import { describe, it, expect } from "vitest";
import { scoreMatch } from "../matcher";

describe("scoreMatch", () => {
  it("renvoie une confiance forte quand compétences, budget et lieu correspondent", () => {
    const r = scoreMatch(
      { skills: ["Next.js", "TypeScript"], budget: 12000, location: "remote" },
      { skills: ["Next.js", "TypeScript", "React"], minBudget: 8000, locations: ["remote"] },
    );
    expect(r.confidence).toBeGreaterThan(0.8);
  });

  it("force la confiance à 0 sans aucune compétence commune", () => {
    const r = scoreMatch(
      { skills: ["Python"], budget: 99999, location: "remote" },
      { skills: ["React"], minBudget: 0, locations: ["remote"] },
    );
    expect(r.confidence).toBe(0);
  });

  it("dégrade le score quand le budget est sous le minimum du freelance", () => {
    const high = scoreMatch(
      { skills: ["SQL"], budget: 20000, location: null },
      { skills: ["SQL"], minBudget: 15000, locations: ["remote"] },
    );
    const low = scoreMatch(
      { skills: ["SQL"], budget: 3000, location: null },
      { skills: ["SQL"], minBudget: 15000, locations: ["remote"] },
    );
    expect(low.confidence).toBeLessThan(high.confidence);
  });

  it("pénalise un lieu incompatible (pas de remote)", () => {
    const r = scoreMatch(
      { skills: ["React"], budget: 5000, location: "Lyon" },
      { skills: ["React"], minBudget: 0, locations: ["Paris"] },
    );
    expect(r.breakdown.location).toBe(0);
  });
});
