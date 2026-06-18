import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockSequences = [
  {
    sequence_id: "seq_001",
    sequence_name: "SaaS Outreach — VP Sales",
    strategy: "balanced",
    overall_score: 84.2,
    status: "excellent",
    avg_open_rate_pct: 28.5,
    avg_reply_rate_pct: 8.2,
    conversion_rate_pct: 6.8,
    bounce_rate_pct: 1.2,
    estimated_pipeline_eur: 340000,
    recommended_strategy: "aggressive",
    sequence_signals: [
      "Séquence performante — score 84/100",
      "Taux de conversion excellent (6.8%) — séquence à dupliquer",
      "Liste propre — faible taux de bounce",
      "Séquence complète — bonne couverture du cycle de décision",
    ],
    risk_signals: [],
    step_optimizations: [
      {
        step_number: 1,
        step_type: "email",
        current_day_offset: 0,
        recommended_day_offset: 0,
        timing_score: 100,
        performance_score: 82,
        issues: [],
        recommendations: [],
      },
      {
        step_number: 2,
        step_type: "linkedin",
        current_day_offset: 3,
        recommended_day_offset: 3,
        timing_score: 100,
        performance_score: 88,
        issues: [],
        recommendations: ["Ajouter un lien CTA clair (case study, démo, calendly)"],
      },
      {
        step_number: 3,
        step_type: "email",
        current_day_offset: 7,
        recommended_day_offset: 7,
        timing_score: 100,
        performance_score: 75,
        issues: [],
        recommendations: [],
      },
      {
        step_number: 4,
        step_type: "phone",
        current_day_offset: 14,
        recommended_day_offset: 14,
        timing_score: 100,
        performance_score: 91,
        issues: [],
        recommendations: [],
      },
      {
        step_number: 5,
        step_type: "email",
        current_day_offset: 21,
        recommended_day_offset: 21,
        timing_score: 100,
        performance_score: 72,
        issues: [],
        recommendations: [],
      },
    ],
  },
  {
    sequence_id: "seq_002",
    sequence_name: "Fintech — CTO Outreach",
    strategy: "aggressive",
    overall_score: 68.4,
    status: "good",
    avg_open_rate_pct: 22.1,
    avg_reply_rate_pct: 6.4,
    conversion_rate_pct: 4.2,
    bounce_rate_pct: 2.8,
    estimated_pipeline_eur: 168000,
    recommended_strategy: "aggressive",
    sequence_signals: [
      "Séquence performante — score 68/100",
      "Conversion positive (4.2%) — optimisation marginale possible",
    ],
    risk_signals: [],
    step_optimizations: [
      {
        step_number: 1,
        step_type: "email",
        current_day_offset: 0,
        recommended_day_offset: 0,
        timing_score: 100,
        performance_score: 70,
        issues: [],
        recommendations: [],
      },
      {
        step_number: 2,
        step_type: "email",
        current_day_offset: 4,
        recommended_day_offset: 2,
        timing_score: 84,
        performance_score: 62,
        issues: ["Timing hors norme pour la stratégie aggressive"],
        recommendations: ["Réajuster le délai selon le calendrier optimal de la stratégie"],
      },
      {
        step_number: 3,
        step_type: "linkedin",
        current_day_offset: 4,
        recommended_day_offset: 4,
        timing_score: 100,
        performance_score: 78,
        issues: [],
        recommendations: [],
      },
      {
        step_number: 4,
        step_type: "phone",
        current_day_offset: 7,
        recommended_day_offset: 7,
        timing_score: 100,
        performance_score: 85,
        issues: [],
        recommendations: [],
      },
    ],
  },
  {
    sequence_id: "seq_003",
    sequence_name: "Mid-Market — Nurture Track",
    strategy: "nurture",
    overall_score: 52.7,
    status: "average",
    avg_open_rate_pct: 19.4,
    avg_reply_rate_pct: 3.8,
    conversion_rate_pct: 2.9,
    bounce_rate_pct: 1.8,
    estimated_pipeline_eur: 58000,
    recommended_strategy: "nurture",
    sequence_signals: [
      "Liste propre — faible taux de bounce",
    ],
    risk_signals: [
      "Conversion faible (2.9%) — revoir le ciblage et le message",
    ],
    step_optimizations: [
      {
        step_number: 1,
        step_type: "email",
        current_day_offset: 0,
        recommended_day_offset: 0,
        timing_score: 100,
        performance_score: 55,
        issues: ["Taux d'ouverture faible (19.4% vs 22% benchmark)"],
        recommendations: ["Tester un nouvel objet d'email — A/B test sur la ligne de sujet"],
      },
      {
        step_number: 2,
        step_type: "email",
        current_day_offset: 10,
        recommended_day_offset: 7,
        timing_score: 76,
        performance_score: 48,
        issues: ["Taux de réponse faible (3.8% vs 5% benchmark)"],
        recommendations: ["Raccourcir le message et ajouter un CTA plus direct"],
      },
      {
        step_number: 3,
        step_type: "linkedin",
        current_day_offset: 14,
        recommended_day_offset: 14,
        timing_score: 100,
        performance_score: 62,
        issues: [],
        recommendations: [],
      },
    ],
  },
  {
    sequence_id: "seq_004",
    sequence_name: "Enterprise — Reactivation",
    strategy: "reactivation",
    overall_score: 38.1,
    status: "poor",
    avg_open_rate_pct: 12.8,
    avg_reply_rate_pct: 1.9,
    conversion_rate_pct: 0.8,
    bounce_rate_pct: 4.2,
    estimated_pipeline_eur: 24000,
    recommended_strategy: "reactivation",
    sequence_signals: [],
    risk_signals: [
      "Taux de bounce élevé (4.2%) — nettoyer la liste",
      "Conversion faible (0.8%) — revoir le ciblage et le message",
      "Séquence sous-performante — révision complète recommandée",
    ],
    step_optimizations: [
      {
        step_number: 1,
        step_type: "email",
        current_day_offset: 0,
        recommended_day_offset: 0,
        timing_score: 100,
        performance_score: 28,
        issues: ["Taux d'ouverture faible (12.8% vs 22% benchmark)", "Taux de réponse faible"],
        recommendations: ["Tester un nouvel objet d'email — A/B test", "Raccourcir le message"],
      },
      {
        step_number: 2,
        step_type: "email",
        current_day_offset: 8,
        recommended_day_offset: 5,
        timing_score: 76,
        performance_score: 22,
        issues: ["Timing hors norme", "Taux de désabonnement élevé (3.2%)"],
        recommendations: ["Réajuster le délai", "Réduire la fréquence"],
      },
      {
        step_number: 3,
        step_type: "phone",
        current_day_offset: 12,
        recommended_day_offset: 12,
        timing_score: 100,
        performance_score: 45,
        issues: [],
        recommendations: [],
      },
    ],
  },
  {
    sequence_id: "seq_005",
    sequence_name: "Startup — Video Outreach",
    strategy: "aggressive",
    overall_score: 76.3,
    status: "good",
    avg_open_rate_pct: 38.2,
    avg_reply_rate_pct: 9.8,
    conversion_rate_pct: 5.5,
    bounce_rate_pct: 0.8,
    estimated_pipeline_eur: 82500,
    recommended_strategy: "aggressive",
    sequence_signals: [
      "Séquence performante — score 76/100",
      "Conversion positive (5.5%) — optimisation marginale possible",
      "Liste propre — faible taux de bounce",
    ],
    risk_signals: [],
    step_optimizations: [
      {
        step_number: 1,
        step_type: "video",
        current_day_offset: 0,
        recommended_day_offset: 0,
        timing_score: 100,
        performance_score: 88,
        issues: [],
        recommendations: [],
      },
      {
        step_number: 2,
        step_type: "email",
        current_day_offset: 2,
        recommended_day_offset: 2,
        timing_score: 100,
        performance_score: 72,
        issues: [],
        recommendations: [],
      },
      {
        step_number: 3,
        step_type: "linkedin",
        current_day_offset: 4,
        recommended_day_offset: 4,
        timing_score: 100,
        performance_score: 82,
        issues: [],
        recommendations: [],
      },
      {
        step_number: 4,
        step_type: "phone",
        current_day_offset: 7,
        recommended_day_offset: 7,
        timing_score: 100,
        performance_score: 91,
        issues: [],
        recommendations: [],
      },
    ],
  },
  {
    sequence_id: "seq_006",
    sequence_name: "Consulting — Cold Outreach",
    strategy: "balanced",
    overall_score: 18.4,
    status: "critical",
    avg_open_rate_pct: 8.2,
    avg_reply_rate_pct: 0.6,
    conversion_rate_pct: 0.0,
    bounce_rate_pct: 7.8,
    estimated_pipeline_eur: 0,
    recommended_strategy: "reactivation",
    sequence_signals: [],
    risk_signals: [
      "Taux de bounce élevé (7.8%) — nettoyer la liste",
      "Conversion faible (0.0%) — revoir le ciblage et le message",
      "Séquence sous-performante — révision complète recommandée",
      "Trop peu d'étapes — les prospects abandonnent avant la décision",
    ],
    step_optimizations: [
      {
        step_number: 1,
        step_type: "email",
        current_day_offset: 0,
        recommended_day_offset: 0,
        timing_score: 100,
        performance_score: 10,
        issues: ["Taux d'ouverture faible (8.2% vs 22%)", "Taux de désabonnement élevé (5.1%)"],
        recommendations: ["Tester un nouvel objet", "Réduire la fréquence"],
      },
      {
        step_number: 2,
        step_type: "email",
        current_day_offset: 20,
        recommended_day_offset: 7,
        timing_score: 0,
        performance_score: 8,
        issues: ["Timing hors norme", "Taux de réponse faible"],
        recommendations: ["Réajuster le délai", "Raccourcir le message"],
      },
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status = searchParams.get("status");
  const strategy = searchParams.get("strategy");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/email-sequence-optimizer`);
      if (status) url.searchParams.set("status", status);
      if (strategy) url.searchParams.set("strategy", strategy);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let sequences = [...mockSequences];
  if (status) sequences = sequences.filter((s) => s.status === status);
  if (strategy) sequences = sequences.filter((s) => s.strategy === strategy);

  const status_counts: Record<string, number> = {};
  const strategy_counts: Record<string, number> = {};
  let total_score = 0;
  let total_conv = 0;
  let total_pipeline = 0;

  for (const s of mockSequences) {
    status_counts[s.status] = (status_counts[s.status] || 0) + 1;
    strategy_counts[s.strategy] = (strategy_counts[s.strategy] || 0) + 1;
    total_score += s.overall_score;
    total_conv += s.conversion_rate_pct;
    total_pipeline += s.estimated_pipeline_eur;
  }

  const n = mockSequences.length;

  return NextResponse.json({
    sequences,
    summary: {
      total: n,
      status_counts,
      strategy_counts,
      avg_score: Math.round((total_score / n) * 10) / 10,
      avg_conversion_rate_pct: Math.round((total_conv / n) * 10) / 10,
      total_pipeline_eur: total_pipeline,
    },
  });
}
