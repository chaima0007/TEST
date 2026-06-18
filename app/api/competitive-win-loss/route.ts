import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCompetitors = [
  {
    competitor: "Salesforce",
    total_deals: 28,
    wins: 20,
    losses: 6,
    no_decisions: 2,
    win_rate_pct: 71.4,
    avg_deal_size_eur: 85000,
    avg_cycle_days: 92.0,
    position: "dominant",
    action: "replicate",
    top_loss_reasons: [
      "Relation établie avec le concurrent (3 deals)",
      "Pricing trop élevé vs. concurrent (2 deals)",
      "Gap fonctionnel identifié par le prospect (1 deal)",
    ],
    win_patterns: [
      "POC systématique — 75% des deals gagnés incluaient un POC",
      "Références clients clés — 65% avec références fournies",
      "Engagement C-level — 80% avec sponsor exécutif engagé",
      "Taille moyenne des deals gagnés: 90,000€",
    ],
    loss_patterns: [
      "Cycle de vente moyen des défaites: 140j",
    ],
    battlecard_priorities: [
      "Documenter le playbook gagnant vs. Salesforce pour l'équipe",
    ],
    arr_won_eur: 1800000,
    arr_lost_eur: 510000,
    net_arr_eur: 1290000,
  },
  {
    competitor: "HubSpot",
    total_deals: 22,
    wins: 14,
    losses: 7,
    no_decisions: 1,
    win_rate_pct: 63.6,
    avg_deal_size_eur: 52000,
    avg_cycle_days: 68.0,
    position: "strong",
    action: "defend",
    top_loss_reasons: [
      "Pricing trop élevé vs. concurrent (4 deals)",
      "Gap fonctionnel identifié par le prospect (2 deals)",
      "Décision reportée — mauvais timing (1 deal)",
    ],
    win_patterns: [
      "POC systématique — 64% des deals gagnés incluaient un POC",
      "Engagement C-level — 71% avec sponsor exécutif engagé",
      "Taille moyenne des deals gagnés: 58,000€",
    ],
    loss_patterns: [
      "Objection prix fréquente — 71% des défaites liées au prix",
      "Sponsor exécutif absent — 71% des défaites sans C-level engagé",
      "Cycle de vente moyen des défaites: 95j",
    ],
    battlecard_priorities: [
      "Préparer la justification ROI vs. HubSpot — contrer l'argument prix",
      "Maintenir l'avantage — surveiller les évolutions produit du concurrent",
    ],
    arr_won_eur: 812000,
    arr_lost_eur: 364000,
    net_arr_eur: 448000,
  },
  {
    competitor: "Pipedrive",
    total_deals: 18,
    wins: 10,
    losses: 7,
    no_decisions: 1,
    win_rate_pct: 55.6,
    avg_deal_size_eur: 31000,
    avg_cycle_days: 55.0,
    position: "strong",
    action: "defend",
    top_loss_reasons: [
      "Pricing trop élevé vs. concurrent (5 deals)",
      "Gap fonctionnel identifié par le prospect (1 deal)",
      "Raison non identifiée — debriefing manquant (1 deal)",
    ],
    win_patterns: [
      "Références clients clés — 60% avec références fournies",
      "Taille moyenne des deals gagnés: 36,000€",
    ],
    loss_patterns: [
      "Objection prix fréquente — 71% des défaites liées au prix",
      "Cycle de vente moyen des défaites: 78j",
    ],
    battlecard_priorities: [
      "Préparer la justification ROI vs. Pipedrive — contrer l'argument prix",
      "Maintenir l'avantage — surveiller les évolutions produit du concurrent",
    ],
    arr_won_eur: 360000,
    arr_lost_eur: 217000,
    net_arr_eur: 143000,
  },
  {
    competitor: "Monday.com",
    total_deals: 15,
    wins: 7,
    losses: 7,
    no_decisions: 1,
    win_rate_pct: 46.7,
    avg_deal_size_eur: 38000,
    avg_cycle_days: 72.0,
    position: "competitive",
    action: "differentiate",
    top_loss_reasons: [
      "Gap fonctionnel identifié par le prospect (3 deals)",
      "Pricing trop élevé vs. concurrent (2 deals)",
      "Relation établie avec le concurrent (2 deals)",
    ],
    win_patterns: [
      "POC systématique — 71% des deals gagnés incluaient un POC",
      "Taille moyenne des deals gagnés: 42,000€",
    ],
    loss_patterns: [
      "Gap produit mentionné — 43% des défaites avec gap fonctionnel",
      "Sponsor exécutif absent — 71% des défaites sans C-level engagé",
      "Cycle de vente moyen des défaites: 95j",
    ],
    battlecard_priorities: [
      "Documenter les fonctionnalités différenciantes vs. Monday.com",
      "Renforcer la discovery pour détecter Monday.com tôt",
      "Préparer des références clients dans le même secteur",
    ],
    arr_won_eur: 294000,
    arr_lost_eur: 266000,
    net_arr_eur: 28000,
  },
  {
    competitor: "Zoho CRM",
    total_deals: 12,
    wins: 4,
    losses: 8,
    no_decisions: 0,
    win_rate_pct: 33.3,
    avg_deal_size_eur: 22000,
    avg_cycle_days: 61.0,
    position: "competitive",
    action: "differentiate",
    top_loss_reasons: [
      "Pricing trop élevé vs. concurrent (6 deals)",
      "Gap fonctionnel identifié par le prospect (1 deal)",
      "Raison non identifiée — debriefing manquant (1 deal)",
    ],
    win_patterns: [
      "Taille moyenne des deals gagnés: 28,000€",
    ],
    loss_patterns: [
      "Objection prix fréquente — 75% des défaites liées au prix",
      "Cycle de vente moyen des défaites: 72j",
    ],
    battlecard_priorities: [
      "Préparer la justification ROI vs. Zoho CRM — contrer l'argument prix",
      "Renforcer la discovery pour détecter Zoho CRM tôt",
      "Préparer des références clients dans le même secteur",
    ],
    arr_won_eur: 112000,
    arr_lost_eur: 176000,
    net_arr_eur: -64000,
  },
  {
    competitor: "Dynamics 365",
    total_deals: 10,
    wins: 2,
    losses: 7,
    no_decisions: 1,
    win_rate_pct: 20.0,
    avg_deal_size_eur: 120000,
    avg_cycle_days: 145.0,
    position: "weak",
    action: "battlecard",
    top_loss_reasons: [
      "Relation établie avec le concurrent (4 deals)",
      "Gap fonctionnel identifié par le prospect (2 deals)",
      "Pricing trop élevé vs. concurrent (1 deal)",
    ],
    win_patterns: [
      "Taille moyenne des deals gagnés: 135,000€",
    ],
    loss_patterns: [
      "Gap produit mentionné — 43% des défaites avec gap fonctionnel",
      "Sponsor exécutif absent — 71% des défaites sans C-level engagé",
      "Cycle de vente moyen des défaites: 168j",
    ],
    battlecard_priorities: [
      "Documenter les fonctionnalités différenciantes vs. Dynamics 365",
      "Win story urgente — 3 cas clients gagnés vs. Dynamics 365 à documenter",
      "Définir le terrain de jeu idéal — éviter les deals où le concurrent est fort",
    ],
    arr_won_eur: 270000,
    arr_lost_eur: 840000,
    net_arr_eur: -570000,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const position = searchParams.get("position");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/competitive-win-loss`);
      if (position) url.searchParams.set("position", position);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let competitors = [...mockCompetitors];
  if (position) competitors = competitors.filter((c) => c.position === position);
  if (action) competitors = competitors.filter((c) => c.action === action);

  const position_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_deals = 0;
  let total_won = 0;
  let total_arr_won = 0;
  let total_arr_lost = 0;

  for (const c of mockCompetitors) {
    position_counts[c.position] = (position_counts[c.position] || 0) + 1;
    action_counts[c.action] = (action_counts[c.action] || 0) + 1;
    total_deals += c.total_deals;
    total_won += c.wins;
    total_arr_won += c.arr_won_eur;
    total_arr_lost += c.arr_lost_eur;
  }

  return NextResponse.json({
    competitors,
    summary: {
      total_competitors: mockCompetitors.length,
      total_deals,
      overall_win_rate_pct: total_deals > 0 ? Math.round((total_won / total_deals) * 1000) / 10 : 0,
      total_arr_won_eur: total_arr_won,
      total_arr_lost_eur: total_arr_lost,
      net_arr_eur: total_arr_won - total_arr_lost,
      position_counts,
      action_counts,
      needs_battlecard_count: mockCompetitors.filter((c) => c.action === "battlecard").length,
      most_common_loss_reason: "price",
    },
  });
}
