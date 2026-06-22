import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[win-loss-intelligence] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "wl_001",
    deal_name: "NexaCloud Enterprise Platform",
    account_name: "NexaCloud SA",
    segment: "enterprise",
    arr_eur: 240000,
    outcome: "won",
    execution_quality: "excellent",
    wl_action: "replicate",
    execution_score: 95.0,
    cycle_efficiency_pct: 22.5,
    discount_pressure: "none",
    win_patterns: [
      "Deal champion-led — champion interne a accéléré la décision",
      "Alignement exécutif — sponsor C-level a facilité la signature",
      "POC complété — preuve technique a converti les sceptiques",
      "Deal bien qualifié — budget et décideur confirmés dès le départ",
      "Engagement soutenu — 8 réunions, relation de confiance établie",
      "Victoire sans remise — valeur perçue excellente",
      "Cycle rapide — 23% plus court que prévu",
      "Multi-threading efficace — 4 contacts engagés",
      "Références clients décisives — peer validation convaincante",
      "Business case partagé — ROI démontré avant négociation",
    ],
    loss_factors: [],
    process_gaps: [],
    coaching_insights: [
      "Documenter ce playbook — deal modèle à partager avec l'équipe",
      "Capitaliser sur ce cas — deal sans remise à utiliser en formation pricing",
      "Analyser les facteurs de rapidité (23% sous le cycle cible) — scalabiliser",
    ],
  },
  {
    deal_id: "wl_002",
    deal_name: "FinEdge Solutions Suite",
    account_name: "FinEdge SA",
    segment: "enterprise",
    arr_eur: 180000,
    outcome: "won",
    execution_quality: "good",
    wl_action: "replicate",
    execution_score: 70.0,
    cycle_efficiency_pct: 5.0,
    discount_pressure: "low",
    win_patterns: [
      "Deal champion-led — champion interne a accéléré la décision",
      "Alignement exécutif — sponsor C-level a facilité la signature",
      "POC complété — preuve technique a converti les sceptiques",
      "Deal bien qualifié — budget et décideur confirmés dès le départ",
      "Faible pression prix — seulement 8% de remise accordée",
    ],
    loss_factors: [],
    process_gaps: [],
    coaching_insights: [
      "Documenter ce playbook — deal modèle à partager avec l'équipe",
    ],
  },
  {
    deal_id: "wl_003",
    deal_name: "RetailPro Analytics",
    account_name: "RetailPro International",
    segment: "mid_market",
    arr_eur: 96000,
    outcome: "won",
    execution_quality: "fair",
    wl_action: "coach",
    execution_score: 45.0,
    cycle_efficiency_pct: -15.0,
    discount_pressure: "medium",
    win_patterns: [
      "Deal champion-led — champion interne a accéléré la décision",
    ],
    loss_factors: [],
    process_gaps: [
      "Budget non confirmé — deal insuffisamment qualifié",
      "Décideur jamais rencontré — risque de surprise en fin de cycle",
      "Prochaines étapes non systématiques — momentum fragile",
    ],
    coaching_insights: [
      "Confirmer le budget avant d'aller en proposition",
      "Engager un sponsor exécutif dès le stade démo/proposition",
      "Systématiser les prochaines étapes en fin de chaque réunion",
    ],
  },
  {
    deal_id: "wl_004",
    deal_name: "ManuGroup ERP Migration",
    account_name: "ManuGroup France",
    segment: "enterprise",
    arr_eur: 150000,
    outcome: "lost",
    execution_quality: "good",
    wl_action: "debrief",
    execution_score: 65.0,
    cycle_efficiency_pct: -8.0,
    discount_pressure: "low",
    win_patterns: [],
    loss_factors: [
      "Perdu face à un concurrent (SAP) — différenciation insuffisante",
      "Pas d'engagement exécutif — décision bloquée au niveau opérationnel",
    ],
    process_gaps: [
      "Décideur jamais rencontré — risque de surprise en fin de cycle",
    ],
    coaching_insights: [
      "Renforcer la battle card contre SAP — deal perdu sur différenciation",
      "Engager un sponsor exécutif dès le stade démo/proposition",
    ],
  },
  {
    deal_id: "wl_005",
    deal_name: "HealthCo Patient Platform",
    account_name: "HealthCo Belgium",
    segment: "mid_market",
    arr_eur: 72000,
    outcome: "lost",
    execution_quality: "poor",
    wl_action: "coach",
    execution_score: 20.0,
    cycle_efficiency_pct: -35.0,
    discount_pressure: "high",
    win_patterns: [],
    loss_factors: [
      "Perdu sur le prix — valeur perçue insuffisante par rapport au coût",
      "Aucun champion identifié — manque de support interne critique",
      "Pas d'engagement exécutif — décision bloquée au niveau opérationnel",
      "Forte pression prix (32% remise) — positionnement valeur défaillant",
      "Budget jamais confirmé — qualification incomplète",
    ],
    process_gaps: [
      "Pas de champion identifié — point de contact insuffisant pour influencer",
      "Budget non confirmé — deal insuffisamment qualifié",
      "Décideur jamais rencontré — risque de surprise en fin de cycle",
      "Single-threading détecté — trop dépendant d'un seul contact",
      "Prochaines étapes non systématiques — momentum fragile",
      "POC non proposé sur un deal significatif — opportunité manquée",
    ],
    coaching_insights: [
      "Identifier le champion dès la qualification — ne pas avancer sans",
      "Confirmer le budget avant d'aller en proposition",
      "Travailler le ROI plus tôt — 32% de remise signale une valeur mal perçue",
      "Engager un sponsor exécutif dès le stade démo/proposition",
      "Proposer systématiquement un POC sur les deals à fort enjeu",
      "Systématiser les prochaines étapes en fin de chaque réunion",
      "Développer plusieurs contacts dès la qualification pour éviter le single-threading",
    ],
  },
  {
    deal_id: "wl_006",
    deal_name: "EduTech LMS Upgrade",
    account_name: "EduTech Learn GmbH",
    segment: "smb",
    arr_eur: 36000,
    outcome: "lost",
    execution_quality: "fair",
    wl_action: "coach",
    execution_score: 40.0,
    cycle_efficiency_pct: 0.0,
    discount_pressure: "medium",
    win_patterns: [],
    loss_factors: [
      "Perdu pour gap produit — besoin non couvert par notre offre",
      "Aucun champion identifié — manque de support interne critique",
      "Trop peu de contacts engagés — single-threading risqué",
      "Budget jamais confirmé — qualification incomplète",
    ],
    process_gaps: [
      "Pas de champion identifié — point de contact insuffisant pour influencer",
      "Budget non confirmé — deal insuffisamment qualifié",
      "Single-threading détecté — trop dépendant d'un seul contact",
    ],
    coaching_insights: [
      "Identifier le champion dès la qualification — ne pas avancer sans",
      "Remonter le gap produit à l'équipe produit — impact sur pipeline identique",
      "Développer plusieurs contacts dès la qualification pour éviter le single-threading",
    ],
  },
  {
    deal_id: "wl_007",
    deal_name: "PropTech Portal Migration",
    account_name: "PropTech Ventures",
    segment: "mid_market",
    arr_eur: 84000,
    outcome: "no_decision",
    execution_quality: "fair",
    wl_action: "investigate",
    execution_score: 50.0,
    cycle_efficiency_pct: -45.0,
    discount_pressure: "low",
    win_patterns: [],
    loss_factors: [
      "Pas de décision prise — status quo maintenu ou projet annulé",
      "Perdu par timing — priorité interne non alignée ou budget gelé",
      "Pas d'engagement exécutif — décision bloquée au niveau opérationnel",
    ],
    process_gaps: [
      "Décideur jamais rencontré — risque de surprise en fin de cycle",
      "Prochaines étapes non systématiques — momentum fragile",
    ],
    coaching_insights: [
      "Engager un sponsor exécutif dès le stade démo/proposition",
      "Systématiser les prochaines étapes en fin de chaque réunion",
    ],
  },
  {
    deal_id: "wl_008",
    deal_name: "LogiChain WMS Pilot",
    account_name: "LogiChain Systems",
    segment: "smb",
    arr_eur: 24000,
    outcome: "no_decision",
    execution_quality: "poor",
    wl_action: "investigate",
    execution_score: 15.0,
    cycle_efficiency_pct: -60.0,
    discount_pressure: "none",
    win_patterns: [],
    loss_factors: [
      "Pas de décision prise — status quo maintenu ou projet annulé",
      "Aucun champion identifié — manque de support interne critique",
      "Pas d'engagement exécutif — décision bloquée au niveau opérationnel",
      "Budget jamais confirmé — qualification incomplète",
    ],
    process_gaps: [
      "Pas de champion identifié — point de contact insuffisant pour influencer",
      "Budget non confirmé — deal insuffisamment qualifié",
      "Décideur jamais rencontré — risque de surprise en fin de cycle",
      "Single-threading détecté — trop dépendant d'un seul contact",
      "Prochaines étapes non systématiques — momentum fragile",
      "Peu de réunions (2) — engagement client insuffisant",
    ],
    coaching_insights: [
      "Identifier le champion dès la qualification — ne pas avancer sans",
      "Confirmer le budget avant d'aller en proposition",
      "Systématiser les prochaines étapes en fin de chaque réunion",
      "Développer plusieurs contacts dès la qualification pour éviter le single-threading",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const outcome = searchParams.get("outcome");
  const quality = searchParams.get("quality");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/win-loss-intelligence`);
      if (outcome) url.searchParams.set("outcome", outcome);
      if (quality) url.searchParams.set("quality", quality);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (outcome) deals = deals.filter((d) => d.outcome === outcome);
  if (quality) deals = deals.filter((d) => d.execution_quality === quality);
  if (action) deals = deals.filter((d) => d.wl_action === action);

  const outcome_counts: Record<string, number> = {};
  const quality_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_score = 0;
  let won_arr = 0;
  let lost_arr = 0;
  let won_count = 0;

  for (const d of mockDeals) {
    outcome_counts[d.outcome] = (outcome_counts[d.outcome] || 0) + 1;
    quality_counts[d.execution_quality] = (quality_counts[d.execution_quality] || 0) + 1;
    action_counts[d.wl_action] = (action_counts[d.wl_action] || 0) + 1;
    total_score += d.execution_score;
    if (d.outcome === "won") { won_arr += d.arr_eur; won_count++; }
    if (d.outcome === "lost") lost_arr += d.arr_eur;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json(sealResponse({
    deals,
    summary: {
      total: n,
      outcome_counts,
      quality_counts,
      action_counts,
      win_rate: Math.round((won_count / n) * 1000) / 10,
      avg_execution_score: Math.round((total_score / n) * 10) / 10,
      total_won_arr_eur: won_arr,
      total_lost_arr_eur: lost_arr,
      coaching_needed_count: mockDeals.filter((d) => d.wl_action === "coach").length,
      replicate_count: mockDeals.filter((d) => d.wl_action === "replicate").length,
    },
  } as Record<string,unknown>)));
}
