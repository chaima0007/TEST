// ─── Agent RÉSOLVEUR (premium) — déblocage ───────────────────────────────────
//
// Détecte les frictions de la flotte, en diagnostique la cause, et propose
// (ou applique) le correctif en s'appuyant sur les mécanismes existants :
// reprise de run (resumeRun), boucle de rétroaction (seuil budget), etc.

export type Signal =
  | { type: "run_failed"; runId: string; failedStep?: string }
  | { type: "low_reply_rate"; rate: number; channel: string }
  | { type: "deploy_failed"; message?: string }
  | { type: "no_matches"; runId: string }
  | { type: "non_compliant_plan"; violations: string[] };

export interface Remediation {
  cause: string;
  fix: string;
  agent: string; // agent qui exécute le correctif
  autoApplicable: boolean; // peut-on l'appliquer sans validation humaine ?
}

export function diagnose(signal: Signal): Remediation {
  switch (signal.type) {
    case "run_failed":
      return {
        cause: `Le run ${signal.runId} a échoué${signal.failedStep ? ` à l'étape « ${signal.failedStep} »` : ""}.`,
        fix: "Reprendre le run depuis l'étape fautive (resumeRun) ; si l'extraction LLM échoue, repli heuristique automatique.",
        agent: "FORGE",
        autoApplicable: true,
      };
    case "low_reply_rate":
      return {
        cause: `Taux de réponse ${Math.round(signal.rate * 100)} % sur ${signal.channel} — ciblage ou message à revoir.`,
        fix: "Réduire le volume et resserrer le ciblage ; A/B tester l'accroche via HERMES, ajouter une preuve sociale (portfolio).",
        agent: "HERMES",
        autoApplicable: false,
      };
    case "deploy_failed":
      return {
        cause: `Déploiement en échec${signal.message ? ` : ${signal.message}` : ""}.`,
        fix: "Relancer le build, vérifier les variables d'environnement et la config Cloudflare Pages.",
        agent: "FORGE",
        autoApplicable: false,
      };
    case "no_matches":
      return {
        cause: `Aucune opportunité retenue sur le run ${signal.runId} — seuil trop strict ou profils trop étroits.`,
        fix: "Abaisser le seuil budget (boucle de rétroaction) ou élargir les compétences des profils.",
        agent: "ORACLE",
        autoApplicable: true,
      };
    case "non_compliant_plan":
      return {
        cause: `Plan non conforme : ${signal.violations.join(" ; ")}.`,
        fix: "Retirer les actions interdites (scraping, plafond dépassé, encaissement prématuré) avant exécution.",
        agent: "SENTINEL",
        autoApplicable: false,
      };
  }
}

export function diagnoseAll(signals: Signal[]): Remediation[] {
  return signals.map(diagnose);
}
