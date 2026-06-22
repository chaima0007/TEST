import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[upsell-opportunity] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Mock data (mirrors UpsellOpportunityEngine Python class) ──────────────────

const entities = [
  {
    id: "OPP-001",
    client_name: "Immobilier Dubois & Associés",
    sector: "Immobilier",
    current_plan: "essentiel",
    current_mrr_eur: 149,
    recommended_upgrade: "performance",
    potential_mrr_eur: 299,
    delta_mrr_eur: 150,
    months_on_current_plan: 18,
    last_upsell_attempt_days: 45,
    engagement_signals: 9.0,
    decision_maker_access: true,
    upsell_probability: 82,
    composite_score: 66.95,
    risk_level: "critique",
  },
  {
    id: "OPP-002",
    client_name: "Restaurant Le Bocage",
    sector: "Restauration & Hôtellerie",
    current_plan: "performance",
    current_mrr_eur: 299,
    recommended_upgrade: "premium",
    potential_mrr_eur: 490,
    delta_mrr_eur: 191,
    months_on_current_plan: 20,
    last_upsell_attempt_days: 90,
    engagement_signals: 8.5,
    decision_maker_access: true,
    upsell_probability: 78,
    composite_score: 68.26,
    risk_level: "critique",
  },
  {
    id: "OPP-003",
    client_name: "Cabinet Médical Vaillant",
    sector: "Médical & Cabinets de Soin",
    current_plan: "essentiel",
    current_mrr_eur: 149,
    recommended_upgrade: "entreprise",
    potential_mrr_eur: 890,
    delta_mrr_eur: 741,
    months_on_current_plan: 14,
    last_upsell_attempt_days: 30,
    engagement_signals: 7.5,
    decision_maker_access: true,
    upsell_probability: 71,
    composite_score: 93.06,
    risk_level: "critique",
  },
  {
    id: "OPP-004",
    client_name: "Plomberie Martin & Fils",
    sector: "Artisans & Bâtiment",
    current_plan: "performance",
    current_mrr_eur: 299,
    recommended_upgrade: "premium",
    potential_mrr_eur: 490,
    delta_mrr_eur: 191,
    months_on_current_plan: 8,
    last_upsell_attempt_days: 60,
    engagement_signals: 6.0,
    decision_maker_access: false,
    upsell_probability: 54,
    composite_score: 47.36,
    risk_level: "élevé",
  },
  {
    id: "OPP-005",
    client_name: "Auto Garage Renard",
    sector: "Garages & Concessionnaires",
    current_plan: "essentiel",
    current_mrr_eur: 149,
    recommended_upgrade: "performance",
    potential_mrr_eur: 299,
    delta_mrr_eur: 150,
    months_on_current_plan: 16,
    last_upsell_attempt_days: 120,
    engagement_signals: 5.0,
    decision_maker_access: false,
    upsell_probability: 48,
    composite_score: 45.80,
    risk_level: "élevé",
  },
  {
    id: "OPP-006",
    client_name: "Coiffure Salon Élégance",
    sector: "Beauté & Bien-être",
    current_plan: "essentiel",
    current_mrr_eur: 149,
    recommended_upgrade: "performance",
    potential_mrr_eur: 299,
    delta_mrr_eur: 150,
    months_on_current_plan: 10,
    last_upsell_attempt_days: 200,
    engagement_signals: 4.0,
    decision_maker_access: false,
    upsell_probability: 32,
    composite_score: 34.45,
    risk_level: "modéré",
  },
  {
    id: "OPP-007",
    client_name: "Boulangerie Artisan Dupain",
    sector: "Alimentation & Commerce",
    current_plan: "essentiel",
    current_mrr_eur: 149,
    recommended_upgrade: "performance",
    potential_mrr_eur: 299,
    delta_mrr_eur: 100,
    months_on_current_plan: 2,
    last_upsell_attempt_days: 5,
    engagement_signals: 1.5,
    decision_maker_access: false,
    upsell_probability: 15,
    composite_score: 15.50,
    risk_level: "faible",
  },
  {
    id: "OPP-008",
    client_name: "École Privée Lumière",
    sector: "Éducation & Formation",
    current_plan: "performance",
    current_mrr_eur: 299,
    recommended_upgrade: "premium",
    potential_mrr_eur: 490,
    delta_mrr_eur: 80,
    months_on_current_plan: 1,
    last_upsell_attempt_days: 3,
    engagement_signals: 1.0,
    decision_maker_access: false,
    upsell_probability: 10,
    composite_score: 10.93,
    risk_level: "faible",
  },
];

const summary = {
  total_opportunities: 8,
  avg_current_mrr: 205.25,
  avg_potential_mrr: 444.5,
  total_delta_mrr: 1753,
  opps_critique: 3,
  opps_eleve: 2,
  opps_modere: 1,
  opps_faible: 2,
  top_opportunity_client: "Cabinet Médical Vaillant",
  top_opportunity_score: 93.06,
  patterns_detected: [
    "opportunité premium détectée",
    "client stagnant depuis 6+ mois",
    "signal d'engagement élevé",
    "décideur accessible",
    "expansion de contrat imminente",
  ],
  avg_composite: 47.79,
  avg_estimated_upsell_index: 4.78,
};

// ── Route ─────────────────────────────────────────────────────────────────────

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary } as Record<string, unknown>)
    ));
  }
  try {
    const url = new URL(`${SWARM_API_URL}/api/upsell-opportunity`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok)
      return sealResponse(NextResponse.json(
        sealResponse((await res.json()) as Record<string, unknown>)
      ));
  } catch {}
  return sealResponse(NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 }
  ));
}
