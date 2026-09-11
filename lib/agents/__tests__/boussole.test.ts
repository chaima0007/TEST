import { describe, it, expect } from "vitest";
import { qualify, MAX_SCORE, type Lead } from "../boussole";

const base: Lead = { firstName: "Sophie", company: "Cabinet Durand" };

describe("BOUSSOLE (qualification déterministe)", () => {
  it("note haut un lead complet et chaud (fit ÉLEVÉE, priorité haute)", () => {
    const q = qualify({
      ...base,
      needClear: true,
      budgetSignal: true,
      timing: "now",
      decisionMaker: true,
      hasWebsite: "outdated",
    });
    expect(q.score).toBe(MAX_SCORE);
    expect(q.fit).toBe("ÉLEVÉE");
    expect(q.priority).toBe("haute");
    expect(q.recommendation).toMatch(/prioritaire/i);
  });

  it("note bas un lead vide (fit FAIBLE, priorité basse)", () => {
    const q = qualify(base);
    expect(q.score).toBeLessThanOrEqual(2);
    expect(q.fit).toBe("FAIBLE");
    expect(q.priority).toBe("basse");
  });

  it("classe un lead partiel en MODÉRÉE", () => {
    const q = qualify({ ...base, needClear: true, timing: "soon" });
    expect(q.fit).toBe("MODÉRÉE");
    expect(q.score).toBeGreaterThanOrEqual(3);
    expect(q.score).toBeLessThanOrEqual(5);
  });

  it("justifie chaque point du score (transparence)", () => {
    const q = qualify({ ...base, needClear: true, budgetSignal: true });
    expect(q.reasons.length).toBeGreaterThan(0);
    expect(q.reasons.join("\n")).toMatch(/Besoin exprimé clairement \(\+2\)/);
    expect(q.reasons.join("\n")).toMatch(/budget.*\(\+2\)/i);
  });

  it("cible les questions sur les manques (budget inconnu → demande le budget)", () => {
    const q = qualify({ ...base, needClear: true, timing: "now", decisionMaker: true });
    expect(q.questions.some((x) => /budget/i.test(x))).toBe(true);
    expect(q.questions.length).toBeLessThanOrEqual(3);
  });

  it("dérive les signaux du texte libre quand les drapeaux manquent", () => {
    const q = qualify({ ...base, reply: "Bonjour, j'aimerais refaire mon site, quel est votre tarif ? C'est assez urgent." });
    // besoin + budget + timing 'now' dérivés du message
    expect(q.reasons.join("\n")).toMatch(/Besoin exprimé clairement \(\+2\)/);
    expect(q.reasons.join("\n")).toMatch(/budget.*\(\+2\)/i);
    expect(q.reasons.join("\n")).toMatch(/immédiate \(\+2\)/);
  });

  it("ne contient aucun pourcentage (§13) — score entier borné", () => {
    const q = qualify({ ...base, needClear: true });
    const all = [q.fit, q.priority, q.recommendation, ...q.reasons, ...q.questions].join("\n");
    expect(all).not.toMatch(/\d\s?%/);
    expect(Number.isInteger(q.score)).toBe(true);
    expect(q.maxScore).toBe(MAX_SCORE);
  });

  it("ne prend jamais la décision à la place de l'humain (§10)", () => {
    const q = qualify({ ...base, needClear: true, budgetSignal: true, timing: "now", decisionMaker: true, hasWebsite: "none" });
    expect(q.recommendation).toMatch(/décision|propose|garde le contact/i);
  });
});
