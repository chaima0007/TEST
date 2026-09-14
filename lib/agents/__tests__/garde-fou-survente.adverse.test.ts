// ─── TESTS ADVERSES — garde-fou anti-survente (PROTOCOLE §13, rôle testeur-adverse)
//
// « Où est le test de non-régression ? Le test qui échoue AVANT le correctif. »
//
// Ces tests ÉCHOUENT volontairement sur le code du 2026-09-14 (`c58a82ee`).
// Ils décrivent un défaut réel, prouvé et reproductible — ils ne décrivent pas
// le comportement souhaité d'un code déjà correct.
//
// DÉFAUT : le filtre `BANNED` n'est appliqué QUE dans les classes `LLM*`
// (hermes.ts:136, relance.ts:145, pacte.ts:148). Les classes `Heuristic*` ne
// filtrent rien — alors qu'elles sont à la fois le repli de la classe LLM ET le
// seul chemin actif tant qu'`ANTHROPIC_API_KEY` est absente (hermes.ts,
// `createHermes()`). Le garde-fou ne protège donc pas le code qui tourne.
//
// NE PAS « corriger » ces tests pour les faire passer : corriger le code.

import { describe, it, expect } from "vitest";
import { HeuristicHermes, CAELUM_OFFER, type Prospect, type Offer } from "../hermes";
import { SurventeDetectee } from "../garde-fou";

// Affirmations « sur nous » que la charte du verificateur-verite désigne comme
// les plus dangereuses. Absentes de BANNED aujourd'hui.
const AFFIRMATIONS_SUR_NOUS = [/\bsécuris/i, /\bconforme\b/i, /\btesté\b/i, /\bbrevet/i];

const prospect: Prospect = {
  firstName: "Alex",
  company: "Acme Conseil",
  sector: "conseil RH",
  signal: "pas de prise de RDV en ligne",
  city: "Bruxelles",
};

async function texteComplet(o?: Offer): Promise<string> {
  const d = await new HeuristicHermes().draft(prospect, o);
  return [d.connectionNote, d.altConnectionNote, d.firstMessage, d.followUp].join("\n");
}

describe("garde-fou anti-survente — chemin heuristique", () => {
  // ✅ CORRIGÉ le 2026-09-14 — ce test passe désormais. Conservé comme test de
  // non-régression : il redeviendrait rouge si le filtre repartait du chemin
  // heuristique. Ne pas le supprimer.
  it("rejette une offre de survente au lieu de l'émettre (ERR-016, volet structurel)", async () => {
    // `draft(p, o)` accepte n'importe quelle Offer : le champ `edge` est injecté
    // verbatim dans firstMessage (hermes.ts, heuristicDraft).
    const offrePiegee: Offer = {
      ...CAELUM_OFFER,
      edge: "résultats garantis, agence certifiée n°1",
    };

    // Comportement attendu : échec BRUYANT. L'heuristique est déjà le repli,
    // elle n'a nulle part où se replier — émettre silencieusement serait pire.
    await expect(new HeuristicHermes().draft(prospect, offrePiegee)).rejects.toThrow(
      SurventeDetectee,
    );

    // L'erreur nomme les termes fautifs, pour que la correction soit évidente.
    await new HeuristicHermes()
      .draft(prospect, offrePiegee)
      .then(() => expect.unreachable("le brouillon n'aurait pas dû être produit"))
      .catch((e: unknown) => {
        expect(e).toBeInstanceOf(SurventeDetectee);
        expect((e as SurventeDetectee).termes.join(" ").toLowerCase()).toContain("garanti");
      });
  });

  it("ÉCHOUE AUJOURD'HUI : l'offre par défaut contient des affirmations « sur nous » non sourçables", async () => {
    const texte = await texteComplet();
    // « hébergement sécurisé inclus » — CAELUM_OFFER.edge, hermes.ts:32.
    const trouvees = AFFIRMATIONS_SUR_NOUS.filter((re) => re.test(texte)).map(
      (re) => texte.match(re)?.[0],
    );
    expect(trouvees).toEqual([]);
  });

  it("ÉCHOUE AUJOURD'HUI : promesse de résultat non étayée (« pensé pour convertir »)", async () => {
    const texte = await texteComplet();
    // Promesse d'effet commercial, invérifiable, émise sans aucune référence
    // client — Caelum n'a aucun client à ce jour.
    expect(/pensé pour convertir/i.test(texte)).toBe(false);
  });

  it("ÉCHOUE AUJOURD'HUI : le prix forfaitaire est annoncé comme un prix plancher", async () => {
    const texte = await texteComplet();
    // CAELUM_OFFER.price est un forfait (500 €). « à partir de » signale au
    // destinataire que la facture sera plus élevée : c'est le « piège » relevé
    // par l'avocat-du-client lors de la réunion du 2026-09-14.
    expect(/à partir de\s*500/i.test(texte)).toBe(false);
  });
});
