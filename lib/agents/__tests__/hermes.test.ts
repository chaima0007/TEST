import { describe, it, expect } from "vitest";
import { HeuristicHermes, CAELUM_OFFER, NOTE_CAP, type Prospect } from "../hermes";

const prospect: Prospect = {
  firstName: "Sophie",
  company: "Cabinet Durand",
  sector: "cabinet d'avocats",
  signal: "site daté et lent sur mobile",
  city: "Bruxelles",
};

describe("HERMES (heuristique)", () => {
  it("personnalise la note de connexion et respecte la borne", async () => {
    const d = await new HeuristicHermes().draft(prospect);
    expect(d.connectionNote).toContain("Sophie");
    expect(d.connectionNote.length).toBeLessThanOrEqual(NOTE_CAP);
    expect(d.altConnectionNote.length).toBeLessThanOrEqual(NOTE_CAP);
    expect(d.generatedBy).toBe("heuristic");
  });

  it("mentionne l'entreprise, le service et le prix dans le 1er message", async () => {
    const d = await new HeuristicHermes().draft(prospect);
    expect(d.firstMessage).toContain("Cabinet Durand");
    expect(d.firstMessage).toContain("site web premium");
    expect(d.firstMessage).toMatch(/500\s?€/u);
  });

  it("propose une relance non vide et polie", async () => {
    const d = await new HeuristicHermes().draft(prospect);
    expect(d.followUp.length).toBeGreaterThan(0);
    expect(d.followUp).toContain("Sophie");
  });

  it("ne contient aucune survente invérifiable (garanti/certifié/meilleur/n°1/100%)", async () => {
    const d = await new HeuristicHermes().draft(prospect);
    const all = [d.connectionNote, d.altConnectionNote, d.firstMessage, d.followUp].join("\n");
    expect(all).not.toMatch(/garanti|certifi|meilleur|n[°o]\s?1|100\s?%/i);
  });

  it("fonctionne sans secteur ni signal (champs optionnels)", async () => {
    const d = await new HeuristicHermes().draft({ firstName: "Marc", company: "Studio K" });
    expect(d.connectionNote).toContain("Marc");
    expect(d.connectionNote.length).toBeLessThanOrEqual(NOTE_CAP);
  });

  it("respecte une offre personnalisée", async () => {
    const d = await new HeuristicHermes().draft(prospect, { ...CAELUM_OFFER, price: 1500 });
    expect(d.firstMessage).toMatch(/1\s?500\s?€/u);
  });
});
