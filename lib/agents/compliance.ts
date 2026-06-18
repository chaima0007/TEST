// ─── Module « Respect » (compliance) — Caelum Partners ───────────────────────
//
// Règles dures que tout plan d'action doit respecter. Le COMMANDANT élimine
// d'office les plans non conformes, AVANT toute optimisation de succès ou de ROI.
// (Voir STATUT LÉGAL : inscription indépendante en attente, pas de Stripe encore.)

export interface PlanAction {
  agent: string;
  channel?: "linkedin" | "email" | "web" | "internal";
  /** Messages sortants par jour (prospection). */
  outboundPerDay?: number;
  /** Utilise de l'automatisation/scraping sur une plateforme tierce ? */
  automatedScraping?: boolean;
  /** Encaisse un paiement ? */
  collectsPayment?: boolean;
  /** Données personnelles de tiers traitées avec base légale (RGPD) ? */
  gdprLawfulBasis?: boolean;
}

export interface ComplianceResult {
  compliant: boolean;
  violations: string[];
}

// Plafond de prospection manuelle "raisonnable" pour rester dans les usages
// acceptables de LinkedIn (au-delà → comportement de bot / risque de ban).
const LINKEDIN_MANUAL_DAILY_CAP = 25;

export function checkAction(a: PlanAction): string[] {
  const v: string[] = [];
  if (a.automatedScraping) {
    v.push(`${a.agent} : scraping/automatisation tierce interdit (CGU + RGPD).`);
  }
  if (a.channel === "linkedin" && (a.outboundPerDay ?? 0) > LINKEDIN_MANUAL_DAILY_CAP) {
    v.push(`${a.agent} : ${a.outboundPerDay} msg/jour dépasse le plafond manuel (${LINKEDIN_MANUAL_DAILY_CAP}).`);
  }
  if (a.collectsPayment) {
    v.push(`${a.agent} : encaissement impossible avant inscription légale (Stripe non activé).`);
  }
  if ((a.channel === "linkedin" || a.channel === "email") && (a.outboundPerDay ?? 0) > 0 && a.gdprLawfulBasis === false) {
    v.push(`${a.agent} : prospection sans base légale RGPD.`);
  }
  return v;
}

export function checkPlan(actions: PlanAction[]): ComplianceResult {
  const violations = actions.flatMap(checkAction);
  return { compliant: violations.length === 0, violations };
}
