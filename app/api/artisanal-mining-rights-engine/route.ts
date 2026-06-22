import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[artisanal-mining-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Artisanal Mining Rights Engine Agent",
  domain: "artisanal_mining_rights",
  total_entities: 8,
  avg_composite: 60.83,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { child_labor_exploitation_scale: 2, armed_group_coercion_pattern: 2, mercury_toxic_exposure_severity: 2, legal_formalization_absence: 2 },
  top_risk_entities: [
    "RDC — 150K Enfants Mines Cobalt Katanga, Travail Forcé, Accidents & Chaîne EV Non Tracée",
    "Burkina Faso/Mali — Mines Or Artisanales, Groupes Armés Taxent Creuseurs & Enfants Recrutés",
    "Pérou — 70K Mineurs Or Madre de Dios, Mercure Contamination Amazonie & Déforestation 100K Ha",
  ],
  critical_alerts: [
    "RDC: child_labor_exploitation_scale",
    "Burkina Faso/Mali: armed_group_coercion_pattern",
    "Pérou: mercury_toxic_exposure_severity",
    "Philippines: legal_formalization_absence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_artisanal_mining_rights_index: 6.08,
  data_sources: [
    "alliance_responsible_mining_asm_global_mercury_child_labor_report",
    "pact_responsible_artisanal_mining_due_diligence_framework",
    "ilo_convention_176_mine_safety_artisanal_small_scale_mining",
  ],
  entities: [
    { id: "AM-001", name: "RDC — 150K Enfants Mines Cobalt Katanga, Travail Forcé, Accidents & Chaîne EV Non Tracée", country: "Afrique Centrale", composite_score: 92.5, child_labor_exploitation_scale_score: 95.0, mercury_toxic_exposure_severity_score: 88.0, legal_formalization_absence_score: 92.0, armed_group_coercion_pattern_score: 95.0, risk_level: "critique", primary_pattern: "child_labor_exploitation_scale", estimated_artisanal_mining_rights_index: 9.25, last_updated: "2026-06-21" },
    { id: "AM-002", name: "Burkina Faso/Mali — Mines Or Artisanales, Groupes Armés Taxent Creuseurs & Enfants Recrutés", country: "Afrique de l'Ouest", composite_score: 89.3, child_labor_exploitation_scale_score: 88.0, mercury_toxic_exposure_severity_score: 90.0, legal_formalization_absence_score: 88.0, armed_group_coercion_pattern_score: 92.0, risk_level: "critique", primary_pattern: "armed_group_coercion_pattern", estimated_artisanal_mining_rights_index: 8.93, last_updated: "2026-06-21" },
    { id: "AM-003", name: "Pérou — 70K Mineurs Or Madre de Dios, Mercure Contamination Amazonie & Déforestation 100K Ha", country: "Amérique Latine", composite_score: 85.95, child_labor_exploitation_scale_score: 82.0, mercury_toxic_exposure_severity_score: 95.0, legal_formalization_absence_score: 88.0, armed_group_coercion_pattern_score: 78.0, risk_level: "critique", primary_pattern: "mercury_toxic_exposure_severity", estimated_artisanal_mining_rights_index: 8.6, last_updated: "2026-06-21" },
    { id: "AM-004", name: "Philippines — 200K Mineurs Or Mercure, Accidents Effondrements & Typhons Inondent Sites", country: "Asie du Sud-Est", composite_score: 84.5, child_labor_exploitation_scale_score: 85.0, mercury_toxic_exposure_severity_score: 88.0, legal_formalization_absence_score: 88.0, armed_group_coercion_pattern_score: 75.0, risk_level: "critique", primary_pattern: "legal_formalization_absence", estimated_artisanal_mining_rights_index: 8.45, last_updated: "2026-06-21" },
    { id: "AM-005", name: "Tanzanie — Mines Tanzanite/Or, Travail Enfant, Effondrements & Absence Protection Travailleurs", country: "Afrique de l'Est", composite_score: 53.1, child_labor_exploitation_scale_score: 52.0, mercury_toxic_exposure_severity_score: 55.0, legal_formalization_absence_score: 55.0, armed_group_coercion_pattern_score: 50.0, risk_level: "élevé", primary_pattern: "child_labor_exploitation_scale", estimated_artisanal_mining_rights_index: 5.31, last_updated: "2026-06-21" },
    { id: "AM-006", name: "Colombie — Orpaillage Illégal, FARC Dissidents Contrôlent Zones, Déplacement & Mercure", country: "Amérique Latine", composite_score: 51.0, child_labor_exploitation_scale_score: 50.0, mercury_toxic_exposure_severity_score: 48.0, legal_formalization_absence_score: 52.0, armed_group_coercion_pattern_score: 55.0, risk_level: "élevé", primary_pattern: "armed_group_coercion_pattern", estimated_artisanal_mining_rights_index: 5.1, last_updated: "2026-06-21" },
    { id: "AM-007", name: "Alliance for Responsible Mining/ASM — Certification Fairtrade Or, Formalisation & Traçabilité", country: "Global", composite_score: 25.85, child_labor_exploitation_scale_score: 22.0, mercury_toxic_exposure_severity_score: 28.0, legal_formalization_absence_score: 25.0, armed_group_coercion_pattern_score: 30.0, risk_level: "modéré", primary_pattern: "legal_formalization_absence", estimated_artisanal_mining_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "AM-008", name: "OIT/Convention 176 Sécurité Mines — Protection ASM, SDG 8.7 Travail Enfant & ASGM Minamata", country: "Global", composite_score: 4.4, child_labor_exploitation_scale_score: 4.0, mercury_toxic_exposure_severity_score: 5.0, legal_formalization_absence_score: 3.0, armed_group_coercion_pattern_score: 6.0, risk_level: "faible", primary_pattern: "mercury_toxic_exposure_severity", estimated_artisanal_mining_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/artisanal-mining-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
