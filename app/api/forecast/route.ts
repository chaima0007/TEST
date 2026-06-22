import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[forecast] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

type Stage =
  | "prospected"
  | "contacted"
  | "qualified"
  | "proposal"
  | "negotiation"
  | "verbal_close"
  | "closed_won";

type Scenario = "pessimistic" | "base" | "optimistic";

interface Deal {
  deal_id: string;
  company: string;
  sector: string;
  stage: Stage;
  value_eur: number;
  days_in_stage: number;
  agent_id: string;
  close_probability: number;
  sector_multiplier: number;
  weighted_value: number;
}

const STAGE_PROBABILITY: Record<Stage, number> = {
  prospected:   0.05,
  contacted:    0.12,
  qualified:    0.25,
  proposal:     0.45,
  negotiation:  0.70,
  verbal_close: 0.90,
  closed_won:   1.00,
};

const SECTOR_MULTIPLIERS: Record<string, number> = {
  pme: 1.00, avocat: 1.15, comptable: 1.10, notaire: 1.12,
  médecin: 0.95, dentiste: 0.98, immobilier: 1.08,
  restaurant: 0.85, hôtel: 0.90, artisan: 0.80, coiffeur: 0.75,
};

const SCENARIO_MODIFIERS: Record<Scenario, number> = {
  pessimistic: 0.65, base: 1.00, optimistic: 1.35,
};

const STAGE_LABELS: Record<Stage, string> = {
  prospected:   "Prospecté",
  contacted:    "Contacté",
  qualified:    "Qualifié",
  proposal:     "Proposition",
  negotiation:  "Négociation",
  verbal_close: "Accord verbal",
  closed_won:   "Signé",
};

function getSectorMultiplier(sector: string): number {
  const s = sector.toLowerCase();
  for (const [key, mult] of Object.entries(SECTOR_MULTIPLIERS)) {
    if (s.includes(key)) return mult;
  }
  return 1.0;
}

function getCloseProbability(stage: Stage, daysInStage: number): number {
  const base = STAGE_PROBABILITY[stage];
  const penalty = Math.max(0, (daysInStage - 14) * 0.005);
  return Math.max(0.01, Math.min(1.0, base - penalty));
}

const MOCK_DEALS: Omit<Deal, "close_probability" | "sector_multiplier" | "weighted_value">[] = [
  { deal_id: "d001", company: "Cabinet Dupont",       sector: "avocat",      stage: "verbal_close", value_eur: 1290, days_in_stage: 3,  agent_id: "3.5" },
  { deal_id: "d002", company: "Plomberie Martin",     sector: "artisan",     stage: "negotiation",  value_eur: 380,  days_in_stage: 7,  agent_id: "3.1" },
  { deal_id: "d003", company: "Cabinet Léger & Ass.", sector: "comptable",   stage: "proposal",     value_eur: 960,  days_in_stage: 5,  agent_id: "3.5" },
  { deal_id: "d004", company: "Dr. Moreau",           sector: "médecin",     stage: "qualified",    value_eur: 540,  days_in_stage: 12, agent_id: "2.3" },
  { deal_id: "d005", company: "Brasserie Le Zinc",    sector: "restaurant",  stage: "proposal",     value_eur: 420,  days_in_stage: 9,  agent_id: "3.2" },
  { deal_id: "d006", company: "Étude Notariale Blanc",sector: "notaire",     stage: "negotiation",  value_eur: 1140, days_in_stage: 4,  agent_id: "3.1" },
  { deal_id: "d007", company: "Agence Horizon",       sector: "immobilier",  stage: "contacted",    value_eur: 720,  days_in_stage: 6,  agent_id: "2.1" },
  { deal_id: "d008", company: "PME Solutions SAS",    sector: "pme",         stage: "verbal_close", value_eur: 890,  days_in_stage: 2,  agent_id: "3.5" },
  { deal_id: "d009", company: "Électricité Durand",   sector: "artisan",     stage: "prospected",   value_eur: 290,  days_in_stage: 20, agent_id: "1.3" },
  { deal_id: "d010", company: "Hôtel Belle Vue",      sector: "hôtel",       stage: "qualified",    value_eur: 680,  days_in_stage: 8,  agent_id: "2.5" },
  { deal_id: "d011", company: "Dr. Fontaine Dentiste",sector: "dentiste",    stage: "proposal",     value_eur: 560,  days_in_stage: 11, agent_id: "3.3" },
  { deal_id: "d012", company: "Coiffure Élégance",    sector: "coiffeur",    stage: "contacted",    value_eur: 190,  days_in_stage: 15, agent_id: "2.2" },
  { deal_id: "d013", company: "BTP Nord SAS",         sector: "pme",         stage: "negotiation",  value_eur: 1450, days_in_stage: 6,  agent_id: "3.1" },
  { deal_id: "d014", company: "Cabinet Rousseau",     sector: "avocat",      stage: "qualified",    value_eur: 870,  days_in_stage: 3,  agent_id: "2.4" },
  { deal_id: "d015", company: "Maçonnerie Bernard",   sector: "artisan",     stage: "proposal",     value_eur: 310,  days_in_stage: 7,  agent_id: "3.2" },
];

function enrichDeals(raw: typeof MOCK_DEALS): Deal[] {
  return raw.map((d) => {
    const cp = getCloseProbability(d.stage, d.days_in_stage);
    const sm = getSectorMultiplier(d.sector);
    return { ...d, close_probability: cp, sector_multiplier: sm, weighted_value: d.value_eur * cp * sm };
  });
}

function buildForecast(deals: Deal[], scenario: Scenario) {
  const modifier = SCENARIO_MODIFIERS[scenario];
  const weightedSum = deals.reduce((s, d) => s + d.weighted_value, 0);
  const expected = weightedSum * modifier;

  const byStage: Record<string, number> = {};
  const bySector: Record<string, number> = {};
  for (const d of deals) {
    byStage[d.stage]   = (byStage[d.stage]   ?? 0) + d.weighted_value;
    bySector[d.sector] = (bySector[d.sector] ?? 0) + d.weighted_value;
  }

  const lateStage = deals.filter((d) =>
    ["negotiation", "verbal_close", "proposal"].includes(d.stage)
  ).length;
  const confidence = Math.min(1, (deals.length / 20) * 0.4 + (lateStage / deals.length) * 0.4 + 0.2);

  const scenLabel = scenario === "pessimistic" ? "pessimiste" : scenario === "base" ? "de base" : "optimiste";
  const confLabel = confidence >= 0.7 ? "élevée" : confidence >= 0.4 ? "moyenne" : "faible";
  const rationale = `Scénario ${scenLabel} — ${deals.length} affaires en pipeline, ${lateStage} en phase avancée. Confiance ${confLabel} (${Math.round(confidence * 100)}%). Prévision : ${expected.toLocaleString("fr-FR", { maximumFractionDigits: 0 })}€.`;

  return {
    scenario,
    expected_revenue: Math.round(expected * 100) / 100,
    deals_count: deals.length,
    pipeline_value: Math.round(deals.reduce((s, d) => s + d.value_eur, 0) * 100) / 100,
    weighted_pipeline: Math.round(weightedSum * 100) / 100,
    by_stage: Object.fromEntries(Object.entries(byStage).map(([k, v]) => [k, Math.round(v * 100) / 100])),
    by_sector: Object.fromEntries(Object.entries(bySector).map(([k, v]) => [k, Math.round(v * 100) / 100])),
    confidence: Math.round(confidence * 1000) / 1000,
    rationale,
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/forecast/summary`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch { /* fall through */ }
  }

  const deals = enrichDeals(MOCK_DEALS);
  const scenarios = (["pessimistic", "base", "optimistic"] as Scenario[]).map((s) =>
    buildForecast(deals, s)
  );

  const byStageCount: Record<string, number> = {};
  for (const d of deals) {
    byStageCount[d.stage] = (byStageCount[d.stage] ?? 0) + 1;
  }

  const topDeals = [...deals].sort((a, b) => b.weighted_value - a.weighted_value).slice(0, 5);
  const staleDeals = deals.filter((d) => d.days_in_stage >= 14);

  return sealResponse(NextResponse.json({
    deals,
    scenarios,
    stage_labels: STAGE_LABELS,
    summary: {
      total_deals: deals.length,
      pipeline_value_eur: deals.reduce((s, d) => s + d.value_eur, 0),
      base_forecast: scenarios[1].expected_revenue,
      pessimistic_forecast: scenarios[0].expected_revenue,
      optimistic_forecast: scenarios[2].expected_revenue,
      confidence: scenarios[1].confidence,
      by_stage_count: byStageCount,
      stale_count: staleDeals.length,
    },
    top_deals: topDeals,
    stale_deals: staleDeals,
  }));
}
