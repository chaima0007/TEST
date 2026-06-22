import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[competitor-intelligence] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCompetitors = [
  {
    competitor_id: "comp_001",
    competitor_name: "SalesForce AI",
    competitor_type: "direct",
    threat_score: 82.4,
    threat_level: "critical",
    market_score: 88.5,
    product_score: 79.2,
    gtm_score: 84.1,
    weakness_score: 18.0,
    recommended_action: "preempt",
    win_probability_vs_this: 20.3,
    threat_signals: [
      "Ils gagnent 58% des deals face à nous",
      "Croissance rapide (42% YoY) — expansion agressive",
      "Lancement produit récent — nouvelles fonctionnalités à analyser",
      "Fort chevauchement fonctionnel (78%)",
      "Financement récent (120M€ il y a 4 mois)",
    ],
    opportunity_signals: [
      "Pricing nettement plus élevé — argument prix en notre faveur",
    ],
    battle_card_tips: [
      "Mettre en avant nos fonctionnalités différenciantes — faire une démo comparative",
      "Valoriser le ROI et le TCO plutôt que le prix unitaire",
      "Sécuriser le champion interne avant la phase de comparaison",
      "Impliquer un exec sponsor tôt dans le cycle de vente",
    ],
  },
  {
    competitor_id: "comp_002",
    competitor_name: "HubSpot Pro",
    competitor_type: "direct",
    threat_score: 71.8,
    threat_level: "high",
    market_score: 76.3,
    product_score: 72.5,
    gtm_score: 68.4,
    weakness_score: 22.0,
    recommended_action: "respond",
    win_probability_vs_this: 31.5,
    threat_signals: [
      "Ils gagnent 48% des deals face à nous",
      "Budget marketing supérieur au nôtre — pression sur l'acquisition",
      "2 partenariats stratégiques récents",
    ],
    opportunity_signals: [
      "22% d'avis négatifs — insatisfaction clients",
      "Insatisfaction produit visible — prospects ouverts à changer",
    ],
    battle_card_tips: [
      "Mettre en avant nos fonctionnalités différenciantes — faire une démo comparative",
      "Sécuriser le champion interne avant la phase de comparaison",
      "Partager les références clients et les témoignages G2/Capterra",
      "Impliquer un exec sponsor tôt dans le cycle de vente",
    ],
  },
  {
    competitor_id: "comp_003",
    competitor_name: "OutreachMax",
    competitor_type: "emerging",
    threat_score: 64.2,
    threat_level: "high",
    market_score: 58.0,
    product_score: 68.8,
    gtm_score: 62.1,
    weakness_score: 12.0,
    recommended_action: "differentiate",
    win_probability_vs_this: 37.6,
    threat_signals: [
      "Lancement produit récent — nouvelles fonctionnalités à analyser",
      "Croissance rapide (38% YoY) — expansion agressive",
    ],
    opportunity_signals: [
      "Faible trésorerie probable — investissements ralentis",
    ],
    battle_card_tips: [
      "Mettre en avant nos fonctionnalités différenciantes — faire une démo comparative",
      "Sécuriser le champion interne avant la phase de comparaison",
      "Impliquer un exec sponsor tôt dans le cycle de vente",
    ],
  },
  {
    competitor_id: "comp_004",
    competitor_name: "SalesLegacy CRM",
    competitor_type: "legacy",
    threat_score: 48.6,
    threat_level: "medium",
    market_score: 62.0,
    product_score: 44.2,
    gtm_score: 55.8,
    weakness_score: 38.0,
    recommended_action: "monitor",
    win_probability_vs_this: 56.3,
    threat_signals: [
      "Fort chevauchement fonctionnel (65%)",
    ],
    opportunity_signals: [
      "3 départs C-suite — instabilité interne",
      "28% d'avis négatifs — insatisfaction clients",
      "Ralentissement des embauches — capacité d'exécution réduite",
      "Insatisfaction produit visible — prospects ouverts à changer",
    ],
    battle_card_tips: [
      "Mettre en avant nos fonctionnalités différenciantes — faire une démo comparative",
      "Soulever la question de la stabilité et de la roadmap long-terme",
      "Partager les références clients et les témoignages G2/Capterra",
    ],
  },
  {
    competitor_id: "comp_005",
    competitor_name: "NicheSales AI",
    competitor_type: "niche",
    threat_score: 38.4,
    threat_level: "medium",
    market_score: 32.5,
    product_score: 45.8,
    gtm_score: 35.2,
    weakness_score: 15.0,
    recommended_action: "monitor",
    win_probability_vs_this: 64.0,
    threat_signals: [
      "Lancement produit récent — nouvelles fonctionnalités à analyser",
    ],
    opportunity_signals: [
      "Pricing nettement plus élevé — argument prix en notre faveur",
    ],
    battle_card_tips: [
      "Valoriser le ROI et le TCO plutôt que le prix unitaire",
    ],
  },
  {
    competitor_id: "comp_006",
    competitor_name: "IndirectPlatform",
    competitor_type: "indirect",
    threat_score: 24.8,
    threat_level: "low",
    market_score: 28.0,
    product_score: 22.5,
    gtm_score: 30.1,
    weakness_score: 10.0,
    recommended_action: "monitor",
    win_probability_vs_this: 77.5,
    threat_signals: [],
    opportunity_signals: [
      "Faible trésorerie probable — investissements ralentis",
    ],
    battle_card_tips: [],
  },
  {
    competitor_id: "comp_007",
    competitor_name: "MiniTool Sales",
    competitor_type: "niche",
    threat_score: 14.2,
    threat_level: "minimal",
    market_score: 12.0,
    product_score: 18.5,
    gtm_score: 15.4,
    weakness_score: 45.0,
    recommended_action: "ignore",
    win_probability_vs_this: 89.0,
    threat_signals: [],
    opportunity_signals: [
      "4 départs C-suite — instabilité interne",
      "35% d'avis négatifs — insatisfaction clients",
      "Ralentissement des embauches — capacité d'exécution réduite",
    ],
    battle_card_tips: [],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const level = searchParams.get("level");
  const type = searchParams.get("type");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/competitor-intelligence`);
      if (level) url.searchParams.set("level", level);
      if (type) url.searchParams.set("type", type);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let competitors = [...mockCompetitors];
  if (level) competitors = competitors.filter((c) => c.threat_level === level);
  if (type) competitors = competitors.filter((c) => c.competitor_type === type);

  const level_counts: Record<string, number> = {
    critical: 0, high: 0, medium: 0, low: 0, minimal: 0,
  };
  const type_counts: Record<string, number> = {};
  let total_threat = 0;
  let total_win = 0;

  for (const c of mockCompetitors) {
    level_counts[c.threat_level] = (level_counts[c.threat_level] || 0) + 1;
    type_counts[c.competitor_type] = (type_counts[c.competitor_type] || 0) + 1;
    total_threat += c.threat_score;
    total_win += c.win_probability_vs_this;
  }

  const n = mockCompetitors.length;

  return sealResponse(NextResponse.json(sealResponse({
    competitors,
    summary: {
      total: n,
      level_counts,
      type_counts,
      avg_threat_score: Math.round((total_threat / n) * 10) / 10,
      avg_win_probability: Math.round((total_win / n) * 10) / 10,
    },
  } as Record<string,unknown>)));
}
