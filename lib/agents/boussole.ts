// ─── Agent BOUSSOLE — qualification / triage de leads (Caelum) ───────────────
//
// BOUSSOLE situe un prospect dans l'entonnoir : ce lead vaut-il ton temps, et
// quelles questions poser avant de rédiger un devis (PACTE) ? Il RECOMMANDE une
// prochaine action ; Chaima décide (§10). Il ne contacte, n'écarte et n'engage
// personne.
//
// CHOIX DE CONCEPTION ASSUMÉ : 100 % déterministe, AUCUN LLM. La qualification
// doit être transparente et auditable — un score de règles explicites, jamais
// une intuition boîte-noire (§10 « aucun agent n'invente un chiffre » ; §13
// « pas de certitude inventée »). Chaque point du score est justifié dans
// `reasons`. Pas de pourcentage (§13) : un score entier borné + un mot de
// confiance (FAIBLE / MODÉRÉE / ÉLEVÉE).

export type Timing = "now" | "soon" | "later" | "unknown";
export type WebsiteState = "none" | "outdated" | "recent" | "unknown";

export interface Lead {
  firstName: string;
  company: string;
  sector?: string;
  /** Texte libre du prospect (mail / message LinkedIn). Sert d'indice quand les
   *  drapeaux explicites ne sont pas fournis. */
  reply?: string;
  needClear?: boolean; // besoin exprimé clairement ?
  budgetSignal?: boolean; // a évoqué un budget / une volonté de payer ?
  timing?: Timing;
  decisionMaker?: boolean; // interlocuteur = décideur ?
  hasWebsite?: WebsiteState;
}

export type Fit = "ÉLEVÉE" | "MODÉRÉE" | "FAIBLE";
export type Priority = "haute" | "moyenne" | "basse";

export interface Qualification {
  fit: Fit;
  priority: Priority;
  score: number; // entier transparent (pas un pourcentage)
  maxScore: number;
  reasons: string[]; // ce qui a fait le score (le « PARCE QUE » du §14)
  questions: string[]; // questions de découverte ciblées sur les manques
  recommendation: string; // prochaine action — l'humain décide (§10)
}

export const MAX_SCORE = 8;

// Mots-clés simples pour dériver un signal quand le drapeau explicite est absent.
// Volontairement conservateur : n'écrase jamais un drapeau fourni.
const RE_BUDGET = /\b(budget|prix|tarif|co[ûu]t|combien|devis)\b/i;
const RE_NEED = /\b(besoin|je veux|j'aimerais|nous voulons|objectif|refaire|cr[ée]er|site)\b/i;
const RE_NOW = /\b(urgent|rapidement|au plus vite|d[èe]s que possible|cette semaine|maintenant)\b/i;
const RE_SOON = /\b(bient[ôo]t|ce mois|prochainement|dans les semaines)\b/i;

// Complète les drapeaux absents à partir du texte libre, de façon déterministe.
function deriveSignals(l: Lead): Lead {
  const r = l.reply ?? "";
  const timing: Timing =
    l.timing ?? (RE_NOW.test(r) ? "now" : RE_SOON.test(r) ? "soon" : "unknown");
  return {
    ...l,
    needClear: l.needClear ?? (r ? RE_NEED.test(r) : undefined),
    budgetSignal: l.budgetSignal ?? (r ? RE_BUDGET.test(r) : undefined),
    timing,
  };
}

export function qualify(input: Lead): Qualification {
  const l = deriveSignals(input);
  let score = 0;
  const reasons: string[] = [];

  if (l.needClear) {
    score += 2;
    reasons.push("Besoin exprimé clairement (+2).");
  } else {
    reasons.push("Besoin encore flou (+0).");
  }

  if (l.budgetSignal) {
    score += 2;
    reasons.push("Signal de budget / volonté de payer (+2).");
  } else {
    reasons.push("Aucun signal de budget (+0).");
  }

  if (l.timing === "now") {
    score += 2;
    reasons.push("Échéance immédiate (+2).");
  } else if (l.timing === "soon") {
    score += 1;
    reasons.push("Échéance proche (+1).");
  } else {
    reasons.push("Échéance vague ou inconnue (+0).");
  }

  if (l.decisionMaker) {
    score += 1;
    reasons.push("Interlocuteur décideur (+1).");
  }

  if (l.hasWebsite === "none" || l.hasWebsite === "outdated") {
    score += 1;
    reasons.push("Site absent ou daté = besoin réel (+1).");
  }

  const fit: Fit = score >= 6 ? "ÉLEVÉE" : score >= 3 ? "MODÉRÉE" : "FAIBLE";
  const priority: Priority = fit === "ÉLEVÉE" ? "haute" : fit === "MODÉRÉE" ? "moyenne" : "basse";

  const questions: string[] = [];
  if (!l.needClear)
    questions.push("Quel résultat concret attendez-vous du site (plus de contacts, crédibilité, prise de RDV) ?");
  if (!l.budgetSignal) questions.push("Avez-vous un budget en tête pour ce projet ?");
  if (l.timing === "unknown" || l.timing === "later")
    questions.push("À quelle échéance aimeriez-vous être en ligne ?");
  if (l.decisionMaker === undefined || l.decisionMaker === false)
    questions.push("Êtes-vous la personne qui décide, ou faut-il impliquer quelqu'un d'autre ?");
  if (questions.length === 0)
    questions.push("Avez-vous des exemples de sites que vous aimez, pour cadrer le style ?");
  const topQuestions = questions.slice(0, 3);

  const recommendation =
    fit === "ÉLEVÉE"
      ? "Prospect prioritaire : propose un appel de 15 min, puis un devis (PACTE). L'envoi reste ta décision (§10)."
      : fit === "MODÉRÉE"
        ? "À creuser : pose les questions ci-dessus avant de t'engager sur un devis."
        : "Faible priorité : réponds poliment et garde le contact, sans y consacrer de temps maintenant.";

  return { fit, priority, score, maxScore: MAX_SCORE, reasons, questions: topQuestions, recommendation };
}
