import { describe, it, expect } from "vitest";
import { HeuristicWriter, type WriterInput } from "../writer";

const input: WriterInput = {
  jobTitle: "API Next.js",
  jobDescription: "Mission de 3 mois",
  budget: 12000,
  freelanceName: "Alice Martin",
  freelanceBio: "Dev full-stack TS, 8 ans d'XP.",
  commonSkills: ["Next.js", "TypeScript"],
};

describe("HeuristicWriter", () => {
  it("rédige une proposition personnalisée (nom, mission, compétences, budget)", async () => {
    const d = await new HeuristicWriter().prepare(input);
    expect(d.proposal).toContain("Alice Martin");
    expect(d.proposal).toContain("API Next.js");
    expect(d.proposal).toContain("Next.js");
    expect(d.proposal).toMatch(/12\s?000\s?€/u); // l'espace milliers FR est insécable
    expect(d.generatedBy).toBe("heuristic");
  });

  it("prépare des réponses de suivi (Négociateur)", async () => {
    const d = await new HeuristicWriter().prepare(input);
    expect(d.followups.length).toBe(3);
    expect(d.followups.every((f) => f.question && f.answer)).toBe(true);
  });

  it("gère un budget inconnu sans planter", async () => {
    const d = await new HeuristicWriter().prepare({ ...input, budget: null });
    expect(d.proposal).toContain("Alice Martin");
    expect(d.followups.length).toBe(3);
  });
});
