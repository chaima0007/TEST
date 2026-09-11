import { describe, it, expect } from "vitest";
import { HeuristicPacte, type LeadBrief } from "../pacte";
import { CAELUM_OFFER } from "../hermes";

const lead: LeadBrief = {
  firstName: "Sophie",
  company: "Cabinet Durand",
  sector: "cabinet d'avocats",
  need: "avoir un site vitrine clair avec un formulaire de contact",
  city: "Bruxelles",
};

describe("PACTE (heuristique)", () => {
  it("personnalise l'objet et l'accroche avec le prospect", async () => {
    const p = await new HeuristicPacte().draft(lead);
    expect(p.subject).toContain("Cabinet Durand");
    expect(p.greeting).toContain("Sophie");
    expect(p.generatedBy).toBe("heuristic");
  });

  it("affiche le prix de l'offre (500 €)", async () => {
    const p = await new HeuristicPacte().draft(lead);
    expect(p.priceLine).toMatch(/500\s?€/u);
    expect(p.terms.join("\n")).toMatch(/500\s?€/u);
  });

  it("liste des livrables ET un hors-périmètre (honnêteté)", async () => {
    const p = await new HeuristicPacte().draft(lead);
    expect(p.scope.length).toBeGreaterThan(0);
    expect(p.outOfScope.length).toBeGreaterThan(0);
  });

  it("laisse la facturation À CONFIRMER et ne promet aucun paiement en ligne", async () => {
    const p = await new HeuristicPacte().draft(lead);
    const terms = p.terms.join("\n");
    expect(terms).toMatch(/À CONFIRMER/);
    const all = [p.subject, p.understanding, p.timeline, p.priceLine, p.nextStep, ...p.scope, ...p.outOfScope, terms].join("\n");
    expect(all).not.toMatch(/paiement en ligne|carte bancaire|stripe/i);
  });

  it("ne contient aucune survente invérifiable", async () => {
    const p = await new HeuristicPacte().draft(lead);
    const all = [p.subject, p.understanding, p.timeline, p.priceLine, p.nextStep, ...p.scope, ...p.outOfScope, ...p.terms].join("\n");
    expect(all).not.toMatch(/garanti|certifi|meilleur|n[°o]\s?1|100\s?%/i);
  });

  it("fonctionne sans secteur ni besoin (champs optionnels)", async () => {
    const p = await new HeuristicPacte().draft({ firstName: "Marc", company: "Studio K" });
    expect(p.understanding).toContain("Studio K");
    expect(p.scope.length).toBeGreaterThan(0);
  });

  it("respecte une offre personnalisée (prix 1500 €)", async () => {
    const p = await new HeuristicPacte().draft(lead, { ...CAELUM_OFFER, service: "automatisation IA", price: 1500 });
    expect(p.priceLine).toMatch(/1\s?500\s?€/u);
    expect(p.subject).toContain("automatisation IA");
  });
});
