import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Mock entities (8 client social profiles, 15 keys each) ────────────────────

const entities = [
  {
    id: "sme-001",
    client_name: "Boulangerie Vanderberg",
    sector: "restauration",
    platform: "Facebook",
    followers_count: 1200,
    monthly_reach: 4800,
    engagement_rate: 7.5,
    post_frequency_per_week: 6,
    ad_spend_eur_monthly: 2400,
    leads_generated_monthly: 48,
    cost_per_lead_eur: 50.0,
    conversion_rate: 55.0,
    roi_score: 85.0,
    composite_score: 75.6,
    risk_level: "critique",
  },
  {
    id: "sme-002",
    client_name: "Garage Motorsport Bruxelles",
    sector: "automobile",
    platform: "Google",
    followers_count: 3400,
    monthly_reach: 18000,
    engagement_rate: 8.2,
    post_frequency_per_week: 7,
    ad_spend_eur_monthly: 5000,
    leads_generated_monthly: 50,
    cost_per_lead_eur: 100.0,
    conversion_rate: 60.0,
    roi_score: 75.0,
    composite_score: 75.85,
    risk_level: "critique",
  },
  {
    id: "sme-003",
    client_name: "Cabinet Juridique Lefevre",
    sector: "juridique",
    platform: "LinkedIn",
    followers_count: 2800,
    monthly_reach: 9200,
    engagement_rate: 6.8,
    post_frequency_per_week: 5,
    ad_spend_eur_monthly: 3200,
    leads_generated_monthly: 44,
    cost_per_lead_eur: 72.73,
    conversion_rate: 62.0,
    roi_score: 70.0,
    composite_score: 69.2,
    risk_level: "critique",
  },
  {
    id: "sme-004",
    client_name: "Salon de Coiffure Élégance",
    sector: "beauté",
    platform: "Instagram",
    followers_count: 5600,
    monthly_reach: 22000,
    engagement_rate: 5.0,
    post_frequency_per_week: 2,
    ad_spend_eur_monthly: 900,
    leads_generated_monthly: 28,
    cost_per_lead_eur: 32.14,
    conversion_rate: 45.0,
    roi_score: 55.0,
    composite_score: 51.1,
    risk_level: "élevé",
  },
  {
    id: "sme-005",
    client_name: "Restaurant Le Moulin d'Or",
    sector: "restauration",
    platform: "Facebook",
    followers_count: 2100,
    monthly_reach: 8500,
    engagement_rate: 6.0,
    post_frequency_per_week: 4,
    ad_spend_eur_monthly: 1800,
    leads_generated_monthly: 35,
    cost_per_lead_eur: 51.43,
    conversion_rate: 42.0,
    roi_score: 50.0,
    composite_score: 53.0,
    risk_level: "élevé",
  },
  {
    id: "sme-006",
    client_name: "Agence Immo Bruxelles Sud",
    sector: "immobilier",
    platform: "Instagram",
    followers_count: 8900,
    monthly_reach: 35000,
    engagement_rate: 3.5,
    post_frequency_per_week: 3,
    ad_spend_eur_monthly: 1200,
    leads_generated_monthly: 18,
    cost_per_lead_eur: 66.67,
    conversion_rate: 25.0,
    roi_score: 30.0,
    composite_score: 30.85,
    risk_level: "modéré",
  },
  {
    id: "sme-007",
    client_name: "Clinique Dentaire Bruxelles Nord",
    sector: "médical",
    platform: "Google",
    followers_count: 1500,
    monthly_reach: 6200,
    engagement_rate: 1.5,
    post_frequency_per_week: 2,
    ad_spend_eur_monthly: 600,
    leads_generated_monthly: 8,
    cost_per_lead_eur: 75.0,
    conversion_rate: 12.0,
    roi_score: 10.0,
    composite_score: 12.6,
    risk_level: "faible",
  },
  {
    id: "sme-008",
    client_name: "École de Formation ProTech",
    sector: "formation",
    platform: "LinkedIn",
    followers_count: 4200,
    monthly_reach: 14000,
    engagement_rate: 2.0,
    post_frequency_per_week: 1,
    ad_spend_eur_monthly: 400,
    leads_generated_monthly: 10,
    cost_per_lead_eur: 40.0,
    conversion_rate: 18.0,
    roi_score: 15.0,
    composite_score: 17.75,
    risk_level: "faible",
  },
];

// ── Mock summary (13 keys) ─────────────────────────────────────────────────────

const summary = {
  total_profiles: 8,
  avg_engagement_rate: 5.06,
  avg_roi_score: 48.75,
  total_monthly_ad_spend: 15500,
  profiles_critique: 3,
  profiles_eleve: 2,
  profiles_modere: 1,
  profiles_faible: 2,
  top_risk_profile: "Garage Motorsport Bruxelles",
  top_risk_score: 75.85,
  patterns_detected: [
    "ROI négatif détecté",
    "engagement faible malgré budget élevé",
    "audience mal ciblée",
    "fréquence de publication insuffisante",
    "opportunité de croissance virale",
  ],
  avg_composite: 48.24,
  avg_estimated_social_index: 4.82,
};

// ── Route handler ──────────────────────────────────────────────────────────────

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>));
  }
  try {
    const url = new URL(`${SWARM_API_URL}/api/social-media-roi`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json() as Record<string, unknown>));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
