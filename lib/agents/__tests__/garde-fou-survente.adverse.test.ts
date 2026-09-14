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

// Le filtre tel qu'il est déclaré dans hermes.ts:48.
const BANNED = [/\bgaranti/i, /\bcertifi/i, /\bmeilleur\b/i, /\bn[°o]\s?1\b/i, /\b100\s?%/];

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
  it("ÉCHOUE AUJOURD'HUI : une offre de survente traverse le chemin heuristique sans être filtrée", async () => {
    // `draft(p, o)` accepte n'importe quelle Offer : le champ `edge` est injecté
    // verbatim dans firstMessage (hermes.ts, heuristicDraft).
    const offrePiegee: Offer = {
      ...CAELUM_OFFER,
      edge: "résultats garantis, agence certifiée n°1",
    };
    const texte = await texteComplet(offrePiegee);

    // Le filtre du projet reconnaît bien ces termes…
    expect(BANNED.some((re) => re.test(texte))).toBe(true);

    // …mais le code ne l'applique pas ici. Attendu après correctif : le texte
    // émis ne contient AUCUN terme banni (rejet, expurgation, ou erreur levée).
    const termesTrouves = BANNED.filter((re) => re.test(texte)).map(String);
    expect(termesTrouves).toEqual([]);
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
