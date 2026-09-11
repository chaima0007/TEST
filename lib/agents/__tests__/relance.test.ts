import { describe, it, expect } from "vitest";
import { HeuristicRelance, type PendingQuote } from "../relance";
import { CAELUM_OFFER } from "../hermes";

const quote: PendingQuote = { firstName: "Sophie", company: "Cabinet Durand" };

describe("RELANCE (heuristique)", () => {
  it("produit une séquence de 3 messages personnalisés, dont une clôture", async () => {
    const s = await new HeuristicRelance().draft(quote);
    expect(s.messages).toHaveLength(3);
    expect(s.messages.every((m) => m.body.includes("Sophie"))).toBe(true);
    expect(s.messages[2].label).toMatch(/clôture/i);
    expect(s.messages[2].body).toContain("Cabinet Durand");
    expect(s.generatedBy).toBe("heuristic");
  });

  it("adapte le message J+7 à l'objection prix (propose de réduire le périmètre)", async () => {
    const s = await new HeuristicRelance().draft({ ...quote, objection: "price" });
    expect(s.messages[1].body).toMatch(/périmètre|budget|enveloppe/i);
  });

  it("adapte le message J+7 à l'objection timing (garde au chaud)", async () => {
    const s = await new HeuristicRelance().draft({ ...quote, objection: "timing" });
    expect(s.messages[1].body).toMatch(/moment|chaud|revien/i);
  });

  it("ne contient aucune fausse urgence ni survente invérifiable", async () => {
    const s = await new HeuristicRelance().draft({ ...quote, objection: "trust" });
    const all = s.messages.map((m) => m.body).join("\n");
    expect(all).not.toMatch(/garanti|certifi|meilleur|n[°o]\s?1|100\s?%|dernière chance|offre expire/i);
  });

  it("utilise le service de l'offre par défaut", async () => {
    const s = await new HeuristicRelance().draft(quote);
    expect(s.messages[0].body).toContain(CAELUM_OFFER.service);
  });

  it("respecte un service personnalisé", async () => {
    const s = await new HeuristicRelance().draft({ ...quote, service: "automatisation IA" });
    expect(s.messages[0].body).toContain("automatisation IA");
  });
});
