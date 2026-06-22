import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[objection-intelligence] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "obj_001",
    deal_name: "NexaCloud — Platform Expansion",
    account_name: "NexaCloud Enterprise",
    arr_eur: 240000,
    stage: "closing",
    objection_burden: "clear",
    objection_action: "advance",
    burden_score: 8.0,
    total_active_objections: 0,
    resolution_score: 100.0,
    primary_objection_type: "none",
    deal_impact_eur: 19200.0,
    risk_factors: [],
    mitigating_factors: [
      "Budget confirmé — objections prix partiellement levées",
      "Champion a explicitement soutenu la solution en interne",
      "POC complété — preuves techniques établies",
      "Sponsor exécutif engagé — niveau décisionnel couvert",
      "Business case partagé — ROI démontré",
      "Références clients fournies — crédibilité renforcée",
      "Timeline convenu — objections de timing levées",
    ],
    recommended_tactics: [
      "Aucune objection active — proposer les prochaines étapes contractuelles",
    ],
  },
  {
    deal_id: "obj_002",
    deal_name: "FinEdge — Suite Entreprise",
    account_name: "FinEdge Solutions",
    arr_eur: 180000,
    stage: "negotiation",
    objection_burden: "moderate",
    objection_action: "address",
    burden_score: 28.0,
    total_active_objections: 2,
    resolution_score: 74.0,
    primary_objection_type: "price",
    deal_impact_eur: 50400.0,
    risk_factors: [
      "Objection prix active (1x) — budget non confirmé",
      "Objection de timing — deal bloqué temporellement (1x)",
    ],
    mitigating_factors: [
      "Champion a explicitement soutenu la solution en interne",
      "POC complété — preuves techniques établies",
      "Sponsor exécutif engagé — niveau décisionnel couvert",
      "Business case partagé — ROI démontré",
      "2 objection(s) traitée(s) lors de la dernière session",
    ],
    recommended_tactics: [
      "Clarifier la valeur ROI et confirmer l'enveloppe budgétaire disponible",
      "Co-construire un business case urgency avec le champion pour débloquer le timing",
    ],
  },
  {
    deal_id: "obj_003",
    deal_name: "RetailPro — Analytics Module",
    account_name: "RetailPro International",
    arr_eur: 96000,
    stage: "proposal",
    objection_burden: "moderate",
    objection_action: "address",
    burden_score: 38.5,
    total_active_objections: 3,
    resolution_score: 42.0,
    primary_objection_type: "competitor",
    deal_impact_eur: 36960.0,
    risk_factors: [
      "Concurrent nommé en évaluation (2 alternative(s) évaluée(s))",
      "Objection d'autorité — 1 partie(s) prenante(s) non engagée(s)",
      "Inquiétudes d'implémentation actives (1x)",
    ],
    mitigating_factors: [
      "Champion a explicitement soutenu la solution en interne",
      "1 objection(s) traitée(s) lors de la dernière session",
    ],
    recommended_tactics: [
      "Préparer une battle card comparative pour le concurrent identifié",
      "Activer le sponsor exécutif pour atteindre les décideurs finaux",
      "Proposer un POC ou workshop technique pour lever les inquiétudes d'implémentation",
      "Demander les critères de sélection et positionner l'avantage concurrentiel différenciant",
    ],
  },
  {
    deal_id: "obj_004",
    deal_name: "ManuGroup — Opérations Suite",
    account_name: "ManuGroup France",
    arr_eur: 144000,
    stage: "proposal",
    objection_burden: "heavy",
    objection_action: "address",
    burden_score: 52.0,
    total_active_objections: 4,
    resolution_score: 22.0,
    primary_objection_type: "price",
    deal_impact_eur: 74880.0,
    risk_factors: [
      "Objection prix active (2x) — budget non confirmé",
      "Objection de timing — deal bloqué temporellement (1x)",
      "Inquiétudes d'implémentation actives (1x)",
      "Objection persistante depuis 8j sans résolution",
    ],
    mitigating_factors: [
      "Business case partagé — ROI démontré",
    ],
    recommended_tactics: [
      "Clarifier la valeur ROI et confirmer l'enveloppe budgétaire disponible",
      "Co-construire un business case urgency avec le champion pour débloquer le timing",
      "Proposer un POC ou workshop technique pour lever les inquiétudes d'implémentation",
      "Planifier un appel de suivi dédié pour résoudre l'objection persistante (8j)",
    ],
  },
  {
    deal_id: "obj_005",
    deal_name: "HealthCo — Compliance Platform",
    account_name: "HealthCo Belgium",
    arr_eur: 72000,
    stage: "demo",
    objection_burden: "heavy",
    objection_action: "escalate",
    burden_score: 63.5,
    total_active_objections: 5,
    resolution_score: 8.0,
    primary_objection_type: "price",
    deal_impact_eur: 45720.0,
    risk_factors: [
      "Objection prix active (2x) — budget non confirmé",
      "Concurrent identifié en évaluation (2 alternative(s) évaluée(s))",
      "Objection d'autorité — 1 partie(s) prenante(s) non engagée(s)",
      "Objection de timing — deal bloqué temporellement (1x)",
      "Confiance insuffisante — 1 objection(s) de crédibilité",
      "Forte concurrence — 3 alternatives en évaluation",
    ],
    mitigating_factors: [
      "1 objection(s) traitée(s) lors de la dernière session",
    ],
    recommended_tactics: [
      "Clarifier la valeur ROI et confirmer l'enveloppe budgétaire disponible",
      "Identifier le concurrent et positionner les différenciateurs clés",
      "Activer le sponsor exécutif pour atteindre les décideurs finaux",
      "Co-construire un business case urgency avec le champion pour débloquer le timing",
      "Fournir des références clients du même secteur et organiser des peer calls",
      "Partager un business case de référence avec ROI mesurable",
      "Demander les critères de sélection et positionner l'avantage concurrentiel différenciant",
    ],
  },
  {
    deal_id: "obj_006",
    deal_name: "EduTech — Learning Management",
    account_name: "EduTech Learn GmbH",
    arr_eur: 60000,
    stage: "qualification",
    objection_burden: "heavy",
    objection_action: "escalate",
    burden_score: 68.0,
    total_active_objections: 5,
    resolution_score: 0.0,
    primary_objection_type: "authority",
    deal_impact_eur: 40800.0,
    risk_factors: [
      "Objection prix active (1x) — budget non confirmé",
      "Concurrent nommé en évaluation (2 alternative(s) évaluée(s))",
      "Objection d'autorité — 2 partie(s) prenante(s) non engagée(s)",
      "Inquiétudes d'implémentation actives (1x)",
      "Confiance insuffisante — 1 objection(s) de crédibilité",
      "Forte concurrence — 3 alternatives en évaluation",
      "Sponsor exécutif non activé — deal en situation critique",
    ],
    mitigating_factors: [],
    recommended_tactics: [
      "Clarifier la valeur ROI et confirmer l'enveloppe budgétaire disponible",
      "Préparer une battle card comparative pour le concurrent identifié",
      "Activer le sponsor exécutif pour atteindre les décideurs finaux",
      "Proposer un POC ou workshop technique pour lever les inquiétudes d'implémentation",
      "Fournir des références clients du même secteur et organiser des peer calls",
      "Partager un business case de référence avec ROI mesurable",
      "Demander les critères de sélection et positionner l'avantage concurrentiel différenciant",
    ],
  },
  {
    deal_id: "obj_007",
    deal_name: "PropTech — Portfolio Analytics",
    account_name: "PropTech Venture",
    arr_eur: 48000,
    stage: "demo",
    objection_burden: "critical",
    objection_action: "reassess",
    burden_score: 82.5,
    total_active_objections: 7,
    resolution_score: 0.0,
    primary_objection_type: "price",
    deal_impact_eur: 39600.0,
    risk_factors: [
      "Objection prix active (2x) — budget non confirmé",
      "Concurrent nommé en évaluation (3 alternative(s) évaluée(s))",
      "Objection d'autorité — 1 partie(s) prenante(s) non engagée(s)",
      "Objection de timing — deal bloqué temporellement (1x)",
      "Inquiétudes d'implémentation actives (1x)",
      "Confiance insuffisante — 1 objection(s) de crédibilité",
      "Objection non résolue depuis 21j — risque de stagnation",
      "Forte concurrence — 4 alternatives en évaluation",
      "Sponsor exécutif non activé — deal en situation critique",
    ],
    mitigating_factors: [],
    recommended_tactics: [
      "Clarifier la valeur ROI et confirmer l'enveloppe budgétaire disponible",
      "Préparer une battle card comparative pour le concurrent identifié",
      "Activer le sponsor exécutif pour atteindre les décideurs finaux",
      "Co-construire un business case urgency avec le champion pour débloquer le timing",
      "Proposer un POC ou workshop technique pour lever les inquiétudes d'implémentation",
      "Fournir des références clients du même secteur et organiser des peer calls",
      "Partager un business case de référence avec ROI mesurable",
      "Planifier un appel de suivi dédié pour résoudre l'objection persistante (21j)",
      "Demander les critères de sélection et positionner l'avantage concurrentiel différenciant",
      "Evaluer si le deal répond aux critères ICP — envisager une pause stratégique",
    ],
  },
  {
    deal_id: "obj_008",
    deal_name: "LogiChain — Supply Intelligence",
    account_name: "LogiChain Systems",
    arr_eur: 36000,
    stage: "qualification",
    objection_burden: "critical",
    objection_action: "reassess",
    burden_score: 91.0,
    total_active_objections: 8,
    resolution_score: 0.0,
    primary_objection_type: "price",
    deal_impact_eur: 32760.0,
    risk_factors: [
      "Objection prix active (2x) — budget non confirmé",
      "Concurrent identifié en évaluation (4 alternative(s) évaluée(s))",
      "Objection d'autorité — 2 partie(s) prenante(s) non engagée(s)",
      "Objection de timing — deal bloqué temporellement (2x)",
      "Inquiétudes d'implémentation actives (2x)",
      "Confiance insuffisante — 2 objection(s) de crédibilité",
      "Objection non résolue depuis 30j — risque de stagnation",
      "Forte concurrence — 4 alternatives en évaluation",
      "Sponsor exécutif non activé — deal en situation critique",
    ],
    mitigating_factors: [],
    recommended_tactics: [
      "Clarifier la valeur ROI et confirmer l'enveloppe budgétaire disponible",
      "Identifier le concurrent et positionner les différenciateurs clés",
      "Activer le sponsor exécutif pour atteindre les décideurs finaux",
      "Co-construire un business case urgency avec le champion pour débloquer le timing",
      "Proposer un POC ou workshop technique pour lever les inquiétudes d'implémentation",
      "Fournir des références clients du même secteur et organiser des peer calls",
      "Partager un business case de référence avec ROI mesurable",
      "Planifier un appel de suivi dédié pour résoudre l'objection persistante (30j)",
      "Demander les critères de sélection et positionner l'avantage concurrentiel différenciant",
      "Evaluer si le deal répond aux critères ICP — envisager une pause stratégique",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const burden = searchParams.get("burden");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/objection-intelligence`);
      if (burden) url.searchParams.set("burden", burden);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (burden) deals = deals.filter((d) => d.objection_burden === burden);
  if (action) deals = deals.filter((d) => d.objection_action === action);

  const burden_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_score = 0;
  let total_resolution = 0;
  let total_impact = 0;
  let total_at_risk_arr = 0;
  let critical_count = 0;
  let escalation_count = 0;
  let advance_count = 0;

  for (const d of mockDeals) {
    burden_counts[d.objection_burden] = (burden_counts[d.objection_burden] || 0) + 1;
    action_counts[d.objection_action] = (action_counts[d.objection_action] || 0) + 1;
    total_score += d.burden_score;
    total_resolution += d.resolution_score;
    total_impact += d.deal_impact_eur;
    if (d.objection_burden === "critical" || d.objection_burden === "heavy") total_at_risk_arr += d.arr_eur;
    if (d.objection_burden === "critical") critical_count++;
    if (d.objection_action === "escalate" || d.objection_action === "reassess") escalation_count++;
    if (d.objection_action === "advance") advance_count++;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json(sealResponse({
    deals,
    summary: {
      total: n,
      burden_counts,
      action_counts,
      avg_burden_score: Math.round((total_score / n) * 10) / 10,
      avg_resolution_score: Math.round((total_resolution / n) * 10) / 10,
      total_arr_impacted_eur: Math.round(total_impact * 100) / 100,
      total_arr_at_risk_eur: total_at_risk_arr,
      critical_count,
      escalation_count,
      advance_ready_count: advance_count,
    },
  } as Record<string,unknown>)));
}
