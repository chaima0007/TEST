import { describe, it, expect } from "vitest";
import { HeuristicAnalyzer } from "../analyzer";

const a = new HeuristicAnalyzer();
const job = (description: string, rawBudget?: string) => ({
  externalId: "t", source: "test", title: "Mission", description, rawBudget,
});

describe("HeuristicAnalyzer", () => {
  it("extrait un budget global en milliers (k)", () => {
    expect(a.extract(job("Mission Next.js. Budget 12k€")).budget).toBe(12000);
  });

  it("extrait un montant explicite en euros", () => {
    expect(a.extract(job("Enveloppe 40 000 € pour 4 mois")).budget).toBe(40000);
  });

  it("calcule un budget total à partir d'un TJM + durée", () => {
    // 450€/jour sur 6 semaines (= 30 jours ouvrés) = 13500
    const r = a.extract(job("TJM 450€/jour pendant 6 semaines"));
    expect(r.budget).toBe(13500);
  });

  it("renvoie budget null quand aucun montant n'est précisé", () => {
    expect(a.extract(job("Besoin d'aide Figma, budget non précisé")).budget).toBeNull();
  });

  it("détecte les compétences canoniques", () => {
    const r = a.extract(job("API en Next.js et TypeScript avec Prisma"));
    expect(r.skills).toEqual(expect.arrayContaining(["Next.js", "TypeScript", "Prisma"]));
  });

  it("détecte le remote et la durée", () => {
    const r = a.extract(job("Mission full remote de 3 mois"));
    expect(r.location).toBe("remote");
    expect(r.durationDays).toBe(63);
  });
});
