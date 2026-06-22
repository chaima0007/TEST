import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[scorecard] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

type Tier = "A" | "B" | "C" | "D";

interface ScorecardData {
  prospect_id: string;
  company_name: string;
  sector: string;
  total_score: number;
  tier: Tier;
  bant_score: number;
  behavioral_score: number;
  temporal_score: number;
  market_fit_score: number;
  dimension_breakdown: Record<string, number>;
  notes: string;
  created_at: string;
  updated_at: string;
}

interface Summary {
  total: number;
  tier_A: number;
  tier_B: number;
  tier_C: number;
  tier_D: number;
  avg_score: number;
  weakest_dimension: string;
  dimension_averages: Record<string, number>;
  sector_breakdown: Record<string, { count: number; avg_score: number }>;
}

// Mirrors Python composite scoring
function bantComposite(b: number, a: number, n: number, t: number): number {
  return Math.round((b * 0.30 + a * 0.20 + n * 0.25 + t * 0.25) * 0.40);
}

function behavComposite(opened: boolean, replied: boolean, clicked: boolean, demo: boolean, web: boolean, quote: boolean): number {
  let s = 0;
  if (opened) s += 4; if (clicked) s += 6; if (replied) s += 8;
  if (web) s += 4; if (demo) s += 5; if (quote) s += 3;
  return Math.min(30, s);
}

function temporalComposite(days: number, respH: number | null, freq: number): number {
  const recency = days === 0 ? 10 : days <= 2 ? 9 : days <= 5 ? 7 : days <= 10 ? 5 : days <= 20 ? 2 : 0;
  const speed = respH === null ? 0 : respH <= 2 ? 6 : respH <= 24 ? 4 : respH <= 72 ? 2 : 0;
  const freqS = freq <= 0 ? 0 : freq <= 3 ? 4 : freq <= 7 ? 3 : freq <= 14 ? 1 : 0;
  return Math.min(20, recency + speed + freqS);
}

function marketComposite(sector: boolean, web: boolean, age: number, emp: number): number {
  let s = 0;
  if (sector) s += 4; if (web) s += 2;
  if (age >= 5) s += 2; else if (age >= 2) s += 1;
  if (emp >= 5) s += 2; else if (emp >= 1) s += 1;
  return Math.min(10, s);
}

function calcTier(score: number): Tier {
  if (score >= 80) return "A";
  if (score >= 60) return "B";
  if (score >= 40) return "C";
  return "D";
}

function mk(
  pid: string, company: string, sector: string,
  b: number, a: number, n: number, t: number,
  opened: boolean, replied: boolean, clicked: boolean, demo: boolean, web: boolean, quote: boolean,
  days: number, respH: number | null, freq: number,
  sectorMatch: boolean, hasWeb: boolean, age: number, emp: number,
  notes = ""
): ScorecardData {
  const bant = bantComposite(b, a, n, t);
  const behav = behavComposite(opened, replied, clicked, demo, web, quote);
  const temporal = temporalComposite(days, respH, freq);
  const fit = marketComposite(sectorMatch, hasWeb, age, emp);
  const total = Math.min(100, bant + behav + temporal + fit);
  return {
    prospect_id: pid, company_name: company, sector,
    total_score: total, tier: calcTier(total),
    bant_score: bant, behavioral_score: behav,
    temporal_score: temporal, market_fit_score: fit,
    dimension_breakdown: { bant, behavioral: behav, temporal, market_fit: fit },
    notes,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
}

const MOCK_SCORECARDS: ScorecardData[] = [
  mk("p001", "BTP Solutions SARL", "PME", 92, 85, 90, 80, true, true, true, true, true, true, 2, 3, 3, true, true, 8, 12),
  mk("p002", "Plomberie Martin", "artisan", 85, 75, 88, 70, true, true, true, false, true, true, 4, 6, 5, true, true, 6, 3),
  mk("p003", "Électricité Dubois", "artisan", 82, 70, 85, 65, true, true, false, true, true, false, 3, 4, 4, true, true, 5, 2),
  mk("p004", "SAS Rénovation Plus", "PME", 88, 80, 92, 75, true, true, true, true, false, true, 6, 12, 7, true, true, 10, 8),
  mk("p005", "Menuiserie Bernard", "artisan", 78, 65, 80, 60, true, true, false, true, true, false, 8, 8, 6, true, true, 7, 2),
  mk("p006", "Chauffage Moreau", "artisan", 76, 68, 78, 55, true, false, true, false, true, true, 5, null, 8, true, true, 4, 1),
  mk("p007", "Couverture Lefebvre", "artisan", 70, 60, 72, 50, true, false, true, false, true, false, 9, null, 10, true, false, 3, 2),
  mk("p008", "Carrelage Petit", "artisan", 65, 55, 68, 45, true, false, false, false, true, false, 12, null, 15, true, true, 2, 1),
  mk("p009", "Peinture Durand", "artisan", 55, 45, 60, 35, true, false, false, false, false, false, 15, null, 20, true, false, 4, 1),
  mk("p010", "Maçonnerie Roux", "artisan", 50, 40, 55, 30, false, false, false, false, false, false, 20, null, 25, true, true, 5, 2),
  mk("p011", "Isolation Thomas", "artisan", 45, 35, 48, 25, false, false, false, false, false, false, 10, null, 30, true, false, 3, 1),
  mk("p012", "Élagage Fontaine", "artisan", 20, 20, 25, 15, false, false, false, false, false, false, 25, null, 0, false, false, 1, 0),
];

const SORTED = [...MOCK_SCORECARDS].sort((a, b) => b.total_score - a.total_score);

function buildSummary(cards: ScorecardData[]): Summary {
  const tiers: Record<Tier, number> = { A: 0, B: 0, C: 0, D: 0 };
  const dimTotals = { bant: 0, behavioral: 0, temporal: 0, market_fit: 0 };
  const sectors: Record<string, number[]> = {};
  let totalScore = 0;

  for (const c of cards) {
    tiers[c.tier]++;
    dimTotals.bant += c.bant_score;
    dimTotals.behavioral += c.behavioral_score;
    dimTotals.temporal += c.temporal_score;
    dimTotals.market_fit += c.market_fit_score;
    totalScore += c.total_score;
    (sectors[c.sector] ??= []).push(c.total_score);
  }

  const n = cards.length || 1;
  const dimAvgs = {
    bant: Math.round((dimTotals.bant / n) * 10) / 10,
    behavioral: Math.round((dimTotals.behavioral / n) * 10) / 10,
    temporal: Math.round((dimTotals.temporal / n) * 10) / 10,
    market_fit: Math.round((dimTotals.market_fit / n) * 10) / 10,
  };

  // Weakest = lowest % of max (bant→40, behav→30, temporal→20, fit→10)
  const maxes = { bant: 40, behavioral: 30, temporal: 20, market_fit: 10 };
  const pcts = Object.entries(dimAvgs).map(([k, v]) => ({ k, pct: v / maxes[k as keyof typeof maxes] }));
  const weakest = pcts.sort((a, b) => a.pct - b.pct)[0]?.k ?? "";

  return {
    total: cards.length,
    tier_A: tiers.A, tier_B: tiers.B, tier_C: tiers.C, tier_D: tiers.D,
    avg_score: Math.round((totalScore / n) * 10) / 10,
    weakest_dimension: weakest,
    dimension_averages: dimAvgs,
    sector_breakdown: Object.fromEntries(
      Object.entries(sectors).map(([s, scores]) => [
        s,
        { count: scores.length, avg_score: Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 10) / 10 },
      ])
    ),
  };
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier = searchParams.get("tier");
  const limit = searchParams.get("limit");

  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/scorecard`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch { /* fall through */ }
  }

  let cards = SORTED;
  if (tier) cards = cards.filter((c) => c.tier === tier.toUpperCase());
  if (limit) cards = cards.slice(0, parseInt(limit));

  return sealResponse(NextResponse.json({ scorecards: cards, summary: buildSummary(MOCK_SCORECARDS) }));
}
