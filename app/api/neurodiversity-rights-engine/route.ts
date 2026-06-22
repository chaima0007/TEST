import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[neurodiversity-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Neurodiversity Rights Engine Agent",
  domain: "neurodiversity_rights",
  total_entities: 8,
  avg_composite: 62.04,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { stigma_criminalization_autistic_pattern: 2, diagnostic_access_barrier: 2, educational_inclusion_denial_severity: 2, employment_discrimination_neurodivergent_scale: 2 },
  top_risk_entities: [
    "Chine — Autisme Institutionnalisé, Éducation Séparée & Stigmatisation Honte Familiale",
    "Inde — TDAH Non Reconnu Légalement, 40M Dyslexiques Sans Aménagement & Caste Diagnostic",
    "Afrique Sub-Sah. — Autisme = Sorcellerie, Exorcismes Forcés & Zéro École Inclusive",
  ],
  critical_alerts: [
    "Chine: stigma_criminalization_autistic_pattern",
    "Inde: diagnostic_access_barrier",
    "Afrique Sub-Sah.: educational_inclusion_denial_severity",
    "Brésil: employment_discrimination_neurodivergent_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_neurodiversity_rights_index: 6.2,
  data_sources: [
    "autistic_self_advocacy_network_asan_neurodiversity_rights_framework",
    "un_crpd_convention_rights_persons_disabilities_article24_inclusive_education",
    "lancet_psychiatry_adhd_autism_global_prevalence_access_report_2023",
  ],
  entities: [
    { id: "NDR-001", name: "Chine — Autisme Institutionnalisé, Éducation Séparée & Stigmatisation Honte Familiale", country: "Asie de l'Est", composite_score: 93.5, educational_inclusion_denial_severity_score: 95.0, employment_discrimination_neurodivergent_scale_score: 92.0, diagnostic_access_barrier_score: 92.0, stigma_criminalization_autistic_pattern_score: 95.0, risk_level: "critique", primary_pattern: "stigma_criminalization_autistic_pattern", estimated_neurodiversity_rights_index: 9.35, last_updated: "2026-06-21" },
    { id: "NDR-002", name: "Inde — TDAH Non Reconnu Légalement, 40M Dyslexiques Sans Aménagement & Caste Diagnostic", country: "Asie du Sud", composite_score: 90.95, educational_inclusion_denial_severity_score: 92.0, employment_discrimination_neurodivergent_scale_score: 88.0, diagnostic_access_barrier_score: 95.0, stigma_criminalization_autistic_pattern_score: 88.0, risk_level: "critique", primary_pattern: "diagnostic_access_barrier", estimated_neurodiversity_rights_index: 9.1, last_updated: "2026-06-21" },
    { id: "NDR-003", name: "Afrique Sub-Sah. — Autisme = Sorcellerie, Exorcismes Forcés & Zéro École Inclusive", country: "Afrique", composite_score: 89.25, educational_inclusion_denial_severity_score: 92.0, employment_discrimination_neurodivergent_scale_score: 85.0, diagnostic_access_barrier_score: 88.0, stigma_criminalization_autistic_pattern_score: 92.0, risk_level: "critique", primary_pattern: "educational_inclusion_denial_severity", estimated_neurodiversity_rights_index: 8.93, last_updated: "2026-06-21" },
    { id: "NDR-004", name: "Brésil — 2,4M Autistes Sans Services, Classes Spéciales Ségrégatrices & INSS Bloqué", country: "Amérique Latine", composite_score: 86.65, educational_inclusion_denial_severity_score: 88.0, employment_discrimination_neurodivergent_scale_score: 88.0, diagnostic_access_barrier_score: 85.0, stigma_criminalization_autistic_pattern_score: 85.0, risk_level: "critique", primary_pattern: "employment_discrimination_neurodivergent_scale", estimated_neurodiversity_rights_index: 8.67, last_updated: "2026-06-21" },
    { id: "NDR-005", name: "USA — ADA Gaps TDAH Emploi, Surdiagnostic Minorités & Prison Pipeline Neurodivers", country: "Amérique du Nord", composite_score: 53.35, educational_inclusion_denial_severity_score: 52.0, employment_discrimination_neurodivergent_scale_score: 55.0, diagnostic_access_barrier_score: 52.0, stigma_criminalization_autistic_pattern_score: 55.0, risk_level: "élevé", primary_pattern: "employment_discrimination_neurodivergent_scale", estimated_neurodiversity_rights_index: 5.34, last_updated: "2026-06-21" },
    { id: "NDR-006", name: "France — TDAH Sous-Diagnostiqué Adultes, Classe ULIS Insuffisante & Refus RQTH", country: "Europe", composite_score: 52.35, educational_inclusion_denial_severity_score: 52.0, employment_discrimination_neurodivergent_scale_score: 52.0, diagnostic_access_barrier_score: 55.0, stigma_criminalization_autistic_pattern_score: 50.0, risk_level: "élevé", primary_pattern: "diagnostic_access_barrier", estimated_neurodiversity_rights_index: 5.24, last_updated: "2026-06-21" },
    { id: "NDR-007", name: "Autistic Self Advocacy Network/ASAN — Neurodiversité Droits, CRPD Art.24 & Inclusion", country: "Global", composite_score: 25.85, educational_inclusion_denial_severity_score: 22.0, employment_discrimination_neurodivergent_scale_score: 28.0, diagnostic_access_barrier_score: 25.0, stigma_criminalization_autistic_pattern_score: 30.0, risk_level: "modéré", primary_pattern: "stigma_criminalization_autistic_pattern", estimated_neurodiversity_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "NDR-008", name: "ONU/CDPH — Convention Droits Personnes Handicap Art.24, SDG 4 Éducation Inclusive", country: "Global", composite_score: 4.4, educational_inclusion_denial_severity_score: 4.0, employment_discrimination_neurodivergent_scale_score: 5.0, diagnostic_access_barrier_score: 3.0, stigma_criminalization_autistic_pattern_score: 6.0, risk_level: "faible", primary_pattern: "educational_inclusion_denial_severity", estimated_neurodiversity_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/neurodiversity-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
