import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockContracts = [
  {
    contract_id: "cr_001",
    account_name: "NexaCloud Enterprise",
    segment: "enterprise",
    arr_eur: 240000,
    days_to_renewal: 120,
    renewal_risk: "green",
    renewal_action: "early_renew",
    uplift_potential: "high",
    renewal_score: 88.5,
    uplift_score: 82.0,
    recommended_uplift_pct: 10.0,
    churn_signals: [],
    retention_levers: [
      "Capitaliser sur la bonne santé compte — présenter les ROI atteints",
      "Référencer l'historique d'expansion — client qui croit avec nous",
      "Négocier un engagement pluriannuel — sécuriser et offrir visibilité tarifaire",
      "Utilisation sièges à 94% — démontrer la valeur business générée",
      "QBR récent — continuer sur la dynamique établie",
      "4 parties prenantes engagées — base de support étendue",
      "3 nouveau(x) cas d'usage identifié(s) — expansion naturelle du ROI",
      "Alignement exécutif actif — mobiliser pour signature",
    ],
    negotiation_tactics: [
      "Défendre la hausse tarifaire avec des données ROI quantifiées",
      "Proposer un palier tarifaire pluriannuel — protection prix contre engagement long terme",
      "Structurer un deal 2 ou 3 ans avec visibilité tarifaire pour le client",
      "Budget confirmé — accélérer vers la signature sans délai",
    ],
    timeline_steps: [
      "Initier la conversation de renouvellement anticipé maintenant",
      "QBR de valeur — présenter les ROI et les gains futurs",
      "Proposer une offre pluriannuelle avec avantage tarifaire",
      "Signature avant la fenêtre de renouvellement officielle",
    ],
  },
  {
    contract_id: "cr_002",
    account_name: "FinEdge Solutions",
    segment: "enterprise",
    arr_eur: 180000,
    days_to_renewal: 75,
    renewal_risk: "green",
    renewal_action: "close_renewal",
    uplift_potential: "high",
    renewal_score: 79.0,
    uplift_score: 71.0,
    recommended_uplift_pct: 9.0,
    churn_signals: [
      "1 offre concurrente reçue — surveiller le processus de décision",
    ],
    retention_levers: [
      "Capitaliser sur la bonne santé compte — présenter les ROI atteints",
      "Utilisation sièges à 88% — démontrer la valeur business générée",
      "QBR récent — continuer sur la dynamique établie",
      "3 parties prenantes engagées — base de support étendue",
      "2 nouveau(x) cas d'usage identifié(s) — expansion naturelle du ROI",
      "Alignement exécutif actif — mobiliser pour signature",
    ],
    negotiation_tactics: [
      "Défendre la hausse tarifaire avec des données ROI quantifiées",
      "Proposer un palier tarifaire pluriannuel — protection prix contre engagement long terme",
      "Préparer un briefing concurrentiel — argumentaire ROI vs alternatives",
      "Quantifier le coût de migration — switching cost à présenter en réunion",
      "Budget confirmé — accélérer vers la signature sans délai",
    ],
    timeline_steps: [
      "Préparer et envoyer la proposition de renouvellement sous 5 jours",
      "Réunion de closing — aligner budget, termes et signataires",
      "Signature dans les 30 jours",
    ],
  },
  {
    contract_id: "cr_003",
    account_name: "RetailPro International",
    segment: "mid_market",
    arr_eur: 144000,
    days_to_renewal: 60,
    renewal_risk: "yellow",
    renewal_action: "accelerate",
    uplift_potential: "medium",
    renewal_score: 62.0,
    uplift_score: 52.0,
    recommended_uplift_pct: 6.0,
    churn_signals: [
      "NPS faible (12) — satisfaction fragile",
      "Hausse de prix proposée (12%) — résistance budget attendue",
    ],
    retention_levers: [
      "Utilisation sièges à 75% — démontrer la valeur business générée",
      "QBR récent — continuer sur la dynamique établie",
      "1 nouveau(x) cas d'usage identifié(s) — expansion naturelle du ROI",
    ],
    negotiation_tactics: [
      "Limiter la hausse à 5-8% — priorité renouvellement sur marge",
      "Budget confirmé — accélérer vers la signature sans délai",
    ],
    timeline_steps: [
      "Qualifier le renouvellement — budget et décideur confirmés",
      "Préparer la proposition de renouvellement avec uplift justifié",
      "Réunion de présentation — sponsor exécutif impliqué",
      "Closing et signature avant J-30",
    ],
  },
  {
    contract_id: "cr_004",
    account_name: "ManuGroup France",
    segment: "enterprise",
    arr_eur: 120000,
    days_to_renewal: 45,
    renewal_risk: "yellow",
    renewal_action: "accelerate",
    uplift_potential: "medium",
    renewal_score: 55.0,
    uplift_score: 45.0,
    recommended_uplift_pct: 5.0,
    churn_signals: [
      "1 escalade(s) support — à résoudre avant renouvellement",
      "Sponsor exécutif non engagé — décision de renouvellement incertaine",
      "Budget non confirmé à moins de 60j du renouvellement — risque de glissement",
    ],
    retention_levers: [
      "Utilisation sièges à 72% — démontrer la valeur business générée",
    ],
    negotiation_tactics: [
      "Limiter la hausse à 5-8% — priorité renouvellement sur marge",
      "Qualifier et confirmer le budget avant d'envoyer la proposition",
    ],
    timeline_steps: [
      "Qualifier le renouvellement — budget et décideur confirmés",
      "Préparer la proposition de renouvellement avec uplift justifié",
      "Réunion de présentation — sponsor exécutif impliqué",
      "Closing et signature avant J-30",
    ],
  },
  {
    contract_id: "cr_005",
    account_name: "HealthCo Belgium",
    segment: "mid_market",
    arr_eur: 72000,
    days_to_renewal: 30,
    renewal_risk: "orange",
    renewal_action: "intervene",
    uplift_potential: "low",
    renewal_score: 38.5,
    uplift_score: 25.0,
    recommended_uplift_pct: 0.0,
    churn_signals: [
      "2 offres concurrentes reçues — risque de départ élevé",
      "NPS négatif (-18) — client détracteur, churn imminent",
      "Champion faible ou absent — pas de défenseur interne",
      "Adoption produit faible (35/100) — valeur non perçue",
    ],
    retention_levers: [
      "Champion encore engagé — activer pour contre-attaque interne",
    ],
    negotiation_tactics: [
      "Présenter un plan de remédiation formel — montrer l'engagement et la roadmap",
      "Préparer un briefing concurrentiel — argumentaire ROI vs alternatives",
      "Reconduire au prix actuel — concentrer sur le renouvellement ferme",
      "Quantifier le coût de migration — switching cost à présenter en réunion",
      "Qualifier et confirmer le budget avant d'envoyer la proposition",
    ],
    timeline_steps: [
      "J-30 : Analyse des risques — plan d'intervention priorisé",
      "J+7 : Résolution des escalades techniques et relationnelles",
      "J+14 : QBR de santé — remettre la relation sur les rails",
      "J+21 : Envoi de la proposition de renouvellement",
      "J+30 : Closing et signature",
    ],
  },
  {
    contract_id: "cr_006",
    account_name: "EduTech Learn GmbH",
    segment: "smb",
    arr_eur: 48000,
    days_to_renewal: 20,
    renewal_risk: "orange",
    renewal_action: "intervene",
    uplift_potential: "low",
    renewal_score: 32.0,
    uplift_score: 18.0,
    recommended_uplift_pct: 0.0,
    churn_signals: [
      "1 offre concurrente reçue — surveiller le processus de décision",
      "NPS faible (8) — satisfaction fragile",
      "Champion faible ou absent — pas de défenseur interne",
      "Adoption produit faible (32/100) — valeur non perçue",
      "Budget non confirmé à moins de 60j du renouvellement — risque de glissement",
    ],
    retention_levers: [],
    negotiation_tactics: [
      "Présenter un plan de remédiation formel — montrer l'engagement et la roadmap",
      "Préparer un briefing concurrentiel — argumentaire ROI vs alternatives",
      "Reconduire au prix actuel — concentrer sur le renouvellement ferme",
      "Quantifier le coût de migration — switching cost à présenter en réunion",
      "Qualifier et confirmer le budget avant d'envoyer la proposition",
    ],
    timeline_steps: [
      "J-20 : Analyse des risques — plan d'intervention priorisé",
      "J+7 : Résolution des escalades techniques et relationnelles",
      "J+14 : QBR de santé — remettre la relation sur les rails",
      "J+21 : Envoi de la proposition de renouvellement",
      "J+30 : Closing et signature",
    ],
  },
  {
    contract_id: "cr_007",
    account_name: "PropTech Ventures",
    segment: "mid_market",
    arr_eur: 36000,
    days_to_renewal: 10,
    renewal_risk: "red",
    renewal_action: "save",
    uplift_potential: "low",
    renewal_score: 18.0,
    uplift_score: 10.0,
    recommended_uplift_pct: 0.0,
    churn_signals: [
      "3 escalades support actives — insatisfaction critique",
      "2 offres concurrentes reçues — risque de départ élevé",
      "NPS négatif (-35) — client détracteur, churn imminent",
      "Champion faible ou absent — pas de défenseur interne",
      "Sponsor exécutif non engagé — décision de renouvellement incertaine",
      "Adoption produit faible (22/100) — valeur non perçue",
    ],
    retention_levers: [],
    negotiation_tactics: [
      "Présenter un plan de remédiation formel — montrer l'engagement et la roadmap",
      "Résoudre les escalades avant toute discussion commerciale",
      "Préparer un briefing concurrentiel — argumentaire ROI vs alternatives",
      "Reconduire au prix actuel — concentrer sur le renouvellement ferme",
      "Quantifier le coût de migration — switching cost à présenter en réunion",
      "Qualifier et confirmer le budget avant d'envoyer la proposition",
    ],
    timeline_steps: [
      "J-0 : Appel de sauvegarde immédiat — senior leadership impliqué",
      "J+2 : Plan de remédiation formalisé — résoudre les blocages identifiés",
      "J+7 : QBR de récupération — ROI, roadmap, valeur démontrée",
      "J+14 : Proposition de renouvellement avec concessions si nécessaire",
      "J+21 : Signature ou escalade finale C-level vs C-level",
    ],
  },
  {
    contract_id: "cr_008",
    account_name: "LogiChain Systems",
    segment: "smb",
    arr_eur: 24000,
    days_to_renewal: 5,
    renewal_risk: "red",
    renewal_action: "save",
    uplift_potential: "low",
    renewal_score: 8.0,
    uplift_score: 5.0,
    recommended_uplift_pct: 0.0,
    churn_signals: [
      "3 escalades support actives — insatisfaction critique",
      "2 offres concurrentes reçues — risque de départ élevé",
      "NPS négatif (-55) — client détracteur, churn imminent",
      "Champion faible ou absent — pas de défenseur interne",
      "Sponsor exécutif non engagé — décision de renouvellement incertaine",
      "Adoption produit faible (18/100) — valeur non perçue",
      "Budget non confirmé à moins de 60j du renouvellement — risque de glissement",
    ],
    retention_levers: [],
    negotiation_tactics: [
      "Présenter un plan de remédiation formel — montrer l'engagement et la roadmap",
      "Résoudre les escalades avant toute discussion commerciale",
      "Préparer un briefing concurrentiel — argumentaire ROI vs alternatives",
      "Reconduire au prix actuel — concentrer sur le renouvellement ferme",
      "Quantifier le coût de migration — switching cost à présenter en réunion",
      "Qualifier et confirmer le budget avant d'envoyer la proposition",
    ],
    timeline_steps: [
      "J-0 : Appel de sauvegarde immédiat — senior leadership impliqué",
      "J+2 : Plan de remédiation formalisé — résoudre les blocages identifiés",
      "J+7 : QBR de récupération — ROI, roadmap, valeur démontrée",
      "J+14 : Proposition de renouvellement avec concessions si nécessaire",
      "J+21 : Signature ou escalade finale C-level vs C-level",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk = searchParams.get("risk");
  const action = searchParams.get("action");
  const uplift = searchParams.get("uplift");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/contract-renewal`);
      if (risk) url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      if (uplift) url.searchParams.set("uplift", uplift);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let contracts = [...mockContracts];
  if (risk) contracts = contracts.filter((c) => c.renewal_risk === risk);
  if (action) contracts = contracts.filter((c) => c.renewal_action === action);
  if (uplift) contracts = contracts.filter((c) => c.uplift_potential === uplift);

  const risk_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const uplift_counts: Record<string, number> = {};
  let total_score = 0;
  let arr_at_risk = 0;
  let arr_total = 0;
  let total_uplift = 0;

  for (const c of mockContracts) {
    risk_counts[c.renewal_risk] = (risk_counts[c.renewal_risk] || 0) + 1;
    action_counts[c.renewal_action] = (action_counts[c.renewal_action] || 0) + 1;
    uplift_counts[c.uplift_potential] = (uplift_counts[c.uplift_potential] || 0) + 1;
    total_score += c.renewal_score;
    arr_total += c.arr_eur;
    if (c.renewal_risk === "orange" || c.renewal_risk === "red") arr_at_risk += c.arr_eur;
    total_uplift += c.arr_eur * c.recommended_uplift_pct / 100;
  }

  const n = mockContracts.length;

  return NextResponse.json({
    contracts,
    summary: {
      total: n,
      risk_counts,
      action_counts,
      uplift_counts,
      avg_renewal_score: Math.round((total_score / n) * 10) / 10,
      total_arr_at_risk_eur: arr_at_risk,
      total_arr_renewing_eur: arr_total,
      total_potential_uplift_eur: Math.round(total_uplift * 100) / 100,
      needs_save_count: mockContracts.filter((c) => c.renewal_action === "save").length,
      high_uplift_count: mockContracts.filter((c) => c.uplift_potential === "high").length,
    },
  });
}
