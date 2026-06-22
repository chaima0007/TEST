import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[proposals] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

type ProposalTier = "weak" | "fair" | "good" | "strong";

interface ProposalSignals {
  proposal_id: string;
  client_name: string;
  sector: string;
  deal_value_eur: number;
  client_budget_eur: number;
  competitor_count: number;
  has_incumbent: boolean;
  meetings_held: number;
  decision_maker_reached: boolean;
  days_to_deadline: number;
  has_roi_model: boolean;
  has_case_study: boolean;
  has_personalization: boolean;
  relationship_score: number;
  previous_deals_won: number;
  proposal_page_count: number;
  our_price_vs_market: number;
}

interface ScoredProposal {
  proposal: ProposalSignals;
  win_probability: number;
  proposal_tier: ProposalTier;
  dimension_scores: Record<string, number>;
  recommendations: string[];
  strengths: string[];
}

const MOCK_PROPOSALS: ProposalSignals[] = [
  { proposal_id: "prop_001", client_name: "Airbus Defence", sector: "aerospace", deal_value_eur: 320000, client_budget_eur: 380000, competitor_count: 2, has_incumbent: false, meetings_held: 5, decision_maker_reached: true, days_to_deadline: 30, has_roi_model: true, has_case_study: true, has_personalization: true, relationship_score: 82, previous_deals_won: 2, proposal_page_count: 18, our_price_vs_market: 0.95 },
  { proposal_id: "prop_002", client_name: "Total Energies", sector: "energy", deal_value_eur: 145000, client_budget_eur: 120000, competitor_count: 4, has_incumbent: true, meetings_held: 3, decision_maker_reached: true, days_to_deadline: 14, has_roi_model: true, has_case_study: false, has_personalization: true, relationship_score: 65, previous_deals_won: 1, proposal_page_count: 22, our_price_vs_market: 1.21 },
  { proposal_id: "prop_003", client_name: "LVMH Digital", sector: "luxury", deal_value_eur: 88000, client_budget_eur: 90000, competitor_count: 3, has_incumbent: false, meetings_held: 4, decision_maker_reached: true, days_to_deadline: 45, has_roi_model: true, has_case_study: true, has_personalization: true, relationship_score: 78, previous_deals_won: 0, proposal_page_count: 15, our_price_vs_market: 0.98 },
  { proposal_id: "prop_004", client_name: "Sanofi IT", sector: "pharma", deal_value_eur: 210000, client_budget_eur: 0, competitor_count: 5, has_incumbent: true, meetings_held: 2, decision_maker_reached: false, days_to_deadline: 7, has_roi_model: false, has_case_study: false, has_personalization: false, relationship_score: 40, previous_deals_won: 0, proposal_page_count: 8, our_price_vs_market: 1.45 },
  { proposal_id: "prop_005", client_name: "Bouygues Telecom", sector: "telecom", deal_value_eur: 175000, client_budget_eur: 200000, competitor_count: 2, has_incumbent: false, meetings_held: 6, decision_maker_reached: true, days_to_deadline: 60, has_roi_model: true, has_case_study: true, has_personalization: true, relationship_score: 88, previous_deals_won: 3, proposal_page_count: 16, our_price_vs_market: 0.88 },
  { proposal_id: "prop_006", client_name: "Vinci Construction", sector: "construction", deal_value_eur: 95000, client_budget_eur: 100000, competitor_count: 3, has_incumbent: false, meetings_held: 3, decision_maker_reached: true, days_to_deadline: 25, has_roi_model: false, has_case_study: true, has_personalization: true, relationship_score: 60, previous_deals_won: 0, proposal_page_count: 14, our_price_vs_market: 1.0 },
  { proposal_id: "prop_007", client_name: "Danone Digital", sector: "food", deal_value_eur: 62000, client_budget_eur: 70000, competitor_count: 1, has_incumbent: false, meetings_held: 2, decision_maker_reached: true, days_to_deadline: 35, has_roi_model: true, has_case_study: false, has_personalization: true, relationship_score: 55, previous_deals_won: 0, proposal_page_count: 12, our_price_vs_market: 0.92 },
  { proposal_id: "prop_008", client_name: "Crédit Mutuel", sector: "banking", deal_value_eur: 280000, client_budget_eur: 250000, competitor_count: 6, has_incumbent: true, meetings_held: 4, decision_maker_reached: true, days_to_deadline: 21, has_roi_model: true, has_case_study: true, has_personalization: false, relationship_score: 72, previous_deals_won: 1, proposal_page_count: 28, our_price_vs_market: 1.12 },
  { proposal_id: "prop_009", client_name: "Alstom Rail", sector: "transport", deal_value_eur: 420000, client_budget_eur: 450000, competitor_count: 2, has_incumbent: false, meetings_held: 7, decision_maker_reached: true, days_to_deadline: 55, has_roi_model: true, has_case_study: true, has_personalization: true, relationship_score: 91, previous_deals_won: 4, proposal_page_count: 19, our_price_vs_market: 0.93 },
  { proposal_id: "prop_010", client_name: "Leclerc Digital", sector: "retail", deal_value_eur: 48000, client_budget_eur: 40000, competitor_count: 4, has_incumbent: true, meetings_held: 1, decision_maker_reached: false, days_to_deadline: 5, has_roi_model: false, has_case_study: false, has_personalization: false, relationship_score: 30, previous_deals_won: 0, proposal_page_count: 4, our_price_vs_market: 1.20 },
];

const RECOMMENDATIONS: Record<string, string> = {
  budget_mismatch: "Revoir le prix — écart important avec le budget déclaré du client",
  no_roi_quantified: "Quantifier le ROI attendu avec des chiffres concrets",
  weak_competitive: "Renforcer la différenciation face aux concurrents identifiés",
  no_references: "Ajouter des références sectorielles pertinentes",
  low_relationship: "Intensifier le contact avec les décideurs avant soumission",
  poor_timing: "Reconsidérer le calendrier — période défavorable détectée",
  no_personalization: "Personnaliser davantage la proposition (nom, enjeux spécifiques)",
  missing_case_study: "Inclure une étude de cas similaire au secteur client",
  deadline_pressure: "Clarifier les délais — pression temporelle risque de dévaloriser l'offre",
  single_contact: "Élargir à plusieurs interlocuteurs (comité d'achat probable)",
};

function valueAlignment(p: ProposalSignals): { score: number; tips: string[]; strengths: string[] } {
  const tips: string[] = []; const strengths: string[] = [];
  let score: number;
  if (p.client_budget_eur <= 0) {
    score = 60;
  } else {
    const ratio = p.deal_value_eur / p.client_budget_eur;
    if (ratio <= 0.80) { score = 100; strengths.push("Proposition sous le budget client"); }
    else if (ratio <= 1.10) { score = 85; }
    else if (ratio <= 1.30) { score = 60; tips.push("budget_mismatch"); }
    else { score = Math.max(0, 100 - (ratio - 1) * 80); tips.push("budget_mismatch"); }
  }
  if (!p.has_roi_model) { score = Math.max(0, score - 15); tips.push("no_roi_quantified"); }
  else { strengths.push("ROI quantifié inclus"); }
  return { score, tips, strengths };
}

function competitivePosition(p: ProposalSignals): { score: number; tips: string[]; strengths: string[] } {
  const tips: string[] = []; const strengths: string[] = [];
  let base = Math.max(0, 100 - p.competitor_count * 15 - (p.has_incumbent ? 20 : 0));
  if (p.our_price_vs_market <= 0.90) { base = Math.min(100, base + 15); strengths.push("Prix compétitif vs marché"); }
  else if (p.our_price_vs_market >= 1.30) { base = Math.max(0, base - 20); tips.push("weak_competitive"); }
  if (!p.has_case_study) { tips.push("no_references"); base = Math.max(0, base - 10); }
  else { strengths.push("Étude de cas incluse"); }
  if (p.previous_deals_won > 0) {
    base = Math.min(100, base + p.previous_deals_won * 10);
    strengths.push(`${p.previous_deals_won} deal(s) précédent(s) remporté(s)`);
  }
  return { score: Math.max(0, base), tips, strengths };
}

function relationshipStrength(p: ProposalSignals): { score: number; tips: string[]; strengths: string[] } {
  const tips: string[] = []; const strengths: string[] = [];
  let score = p.relationship_score;
  if (!p.decision_maker_reached) { score = Math.max(0, score - 25); tips.push("low_relationship"); }
  else { strengths.push("Décideur contacté"); }
  const bonus = Math.min(30, p.meetings_held * 7.5);
  score = Math.min(100, score + bonus);
  if (p.meetings_held >= 3) { strengths.push(`${p.meetings_held} réunions tenues`); }
  else if (p.meetings_held === 0) { tips.push("single_contact"); }
  return { score, tips, strengths };
}

function timingFit(p: ProposalSignals): { score: number; tips: string[]; strengths: string[] } {
  const tips: string[] = []; const strengths: string[] = [];
  const days = p.days_to_deadline;
  if (days <= 0) return { score: 0, tips: ["deadline_pressure"], strengths: [] };
  let score: number;
  if (days <= 7) { score = 30; tips.push("deadline_pressure"); }
  else if (days <= 14) { score = 60; }
  else if (days <= 30) { score = 90; strengths.push("Délai favorable pour préparer la réponse"); }
  else if (days <= 60) { score = 100; strengths.push("Timing excellent"); }
  else { score = Math.max(60, 100 - (days - 60) * 0.5); }
  if (p.has_incumbent && days <= 14) { score = Math.max(0, score - 15); tips.push("poor_timing"); }
  return { score, tips, strengths };
}

function proposalQuality(p: ProposalSignals): { score: number; tips: string[]; strengths: string[] } {
  const tips: string[] = []; const strengths: string[] = [];
  const pages = p.proposal_page_count;
  let pageScore: number;
  if (pages < 5) { pageScore = 40; }
  else if (pages <= 20) { pageScore = 100; strengths.push("Longueur de proposition optimale"); }
  else if (pages <= 40) { pageScore = 75; }
  else { pageScore = Math.max(40, 75 - (pages - 40) * 1.5); }
  const persScore = p.has_personalization ? 100 : 50;
  if (!p.has_personalization) { tips.push("no_personalization"); }
  else { strengths.push("Proposition personnalisée"); }
  const csScore = p.has_case_study ? 100 : 60;
  if (!p.has_case_study) { tips.push("missing_case_study"); }
  const score = pageScore * 0.3 + persScore * 0.4 + csScore * 0.3;
  return { score, tips, strengths };
}

function scoreProposal(p: ProposalSignals): ScoredProposal {
  const va = valueAlignment(p);
  const cp = competitivePosition(p);
  const rs = relationshipStrength(p);
  const tf = timingFit(p);
  const pq = proposalQuality(p);

  const dimScores = {
    value_alignment: Math.round(va.score * 100) / 100,
    competitive_position: Math.round(cp.score * 100) / 100,
    relationship_strength: Math.round(rs.score * 100) / 100,
    timing_fit: Math.round(tf.score * 100) / 100,
    proposal_quality: Math.round(pq.score * 100) / 100,
  };

  const weights = { value_alignment: 0.20, competitive_position: 0.25, relationship_strength: 0.20, timing_fit: 0.15, proposal_quality: 0.20 };
  const composite = Object.entries(dimScores).reduce((s, [k, v]) => s + v * (weights as Record<string, number>)[k], 0);
  const prob = Math.round(Math.max(0, Math.min(1, 0.20 + (composite / 100) * 0.60)) * 10000) / 10000;

  let tier: ProposalTier;
  if (prob >= 0.65) tier = "strong";
  else if (prob >= 0.50) tier = "good";
  else if (prob >= 0.35) tier = "fair";
  else tier = "weak";

  const allTips = [...new Set([...va.tips, ...cp.tips, ...rs.tips, ...tf.tips, ...pq.tips])];
  const recommendations = allTips.map(k => RECOMMENDATIONS[k]).filter(Boolean);
  const strengths = [...va.strengths, ...cp.strengths, ...rs.strengths, ...tf.strengths, ...pq.strengths];

  return { proposal: p, win_probability: prob, proposal_tier: tier, dimension_scores: dimScores, recommendations, strengths };
}

function computeSummary(scored: ScoredProposal[]) {
  const count = scored.length;
  if (count === 0) return {
    total: 0,
    tier_counts: { weak: 0, fair: 0, good: 0, strong: 0 },
    avg_win_probability: 0,
    best_win_probability: 0,
    total_pipeline_eur: 0,
    expected_won_eur: 0,
  };
  const tier_counts = { weak: 0, fair: 0, good: 0, strong: 0 };
  for (const s of scored) tier_counts[s.proposal_tier]++;
  const avg = scored.reduce((s, p) => s + p.win_probability, 0) / count;
  const best = Math.max(...scored.map(s => s.win_probability));
  const pipeline = scored.reduce((s, p) => s + p.proposal.deal_value_eur, 0);
  const expected = scored.reduce((s, p) => s + p.proposal.deal_value_eur * p.win_probability, 0);
  return {
    total: count,
    tier_counts,
    avg_win_probability: Math.round(avg * 10000) / 10000,
    best_win_probability: Math.round(best * 10000) / 10000,
    total_pipeline_eur: Math.round(pipeline * 100) / 100,
    expected_won_eur: Math.round(expected * 100) / 100,
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/proposals`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch { /* fall through */ }
  }

  const scored = MOCK_PROPOSALS.map(scoreProposal).sort((a, b) => b.win_probability - a.win_probability);
  const summary = computeSummary(scored);

  return sealResponse(NextResponse.json({
    proposals: scored,
    summary,
    last_updated: new Date().toISOString(),
  }));
}
