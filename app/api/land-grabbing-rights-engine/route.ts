import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[land-grabbing-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Land Grabbing Rights Engine Agent",
  domain: "land_grabbing_rights",
  total_entities: 8,
  avg_composite: 61.61,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_displacement_land_seizure_severity: 4, corporate_state_complicity_land_grab: 1, legal_title_recognition_absence_scale: 2, indigenous_community_consultation_gap: 1 },
  top_risk_entities: [
    "Cambodge — Accaparement Terres 730 000 Ha, Expulsions Forcées Villages & Complicité État-Sociétés Sucrières",
    "Éthiopie — Villagisation Forcée 1,5M Personnes, Concessions Agricoles Étrangères & Zéro Consultation",
    "Brésil/Amazonie — Garilampeiros Terres Autochtones, Déforestation Illégale & Agronégocio Impuni",
  ],
  critical_alerts: [
    "Cambodge: forced_displacement_land_seizure_severity",
    "Éthiopie: forced_displacement_land_seizure_severity",
    "Brésil/Amazonie: corporate_state_complicity_land_grab",
    "Inde: legal_title_recognition_absence_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_land_grabbing_rights_index: 6.16,
  data_sources: [
    "global_witness_land_grabbing_defenders_report",
    "grain_seized_the_2008_landgrab_for_food_and_financial_security",
    "oxfam_land_rights_commercial_agriculture_report",
  ],
  entities: [
    { id: "LGR-001", name: "Cambodge — Accaparement Terres 730 000 Ha, Expulsions Forcées Villages & Complicité État-Sociétés Sucrières", country: "Cambodge", composite_score: 93.75, forced_displacement_land_seizure_severity_score: 96.0, legal_title_recognition_absence_scale_score: 93.0, corporate_state_complicity_land_grab_score: 94.0, indigenous_community_consultation_gap_score: 91.0, risk_level: "critique", primary_pattern: "forced_displacement_land_seizure_severity", estimated_land_grabbing_rights_index: 9.38, last_updated: "2026-06-21" },
    { id: "LGR-002", name: "Éthiopie — Villagisation Forcée 1,5M Personnes, Concessions Agricoles Étrangères & Zéro Consultation", country: "Éthiopie", composite_score: 90.05, forced_displacement_land_seizure_severity_score: 93.0, legal_title_recognition_absence_scale_score: 89.0, corporate_state_complicity_land_grab_score: 90.0, indigenous_community_consultation_gap_score: 87.0, risk_level: "critique", primary_pattern: "forced_displacement_land_seizure_severity", estimated_land_grabbing_rights_index: 9.01, last_updated: "2026-06-21" },
    { id: "LGR-003", name: "Brésil/Amazonie — Garilampeiros Terres Autochtones, Déforestation Illégale & Agronégocio Impuni", country: "Brésil", composite_score: 88.25, forced_displacement_land_seizure_severity_score: 91.0, legal_title_recognition_absence_scale_score: 87.0, corporate_state_complicity_land_grab_score: 88.0, indigenous_community_consultation_gap_score: 86.0, risk_level: "critique", primary_pattern: "corporate_state_complicity_land_grab", estimated_land_grabbing_rights_index: 8.83, last_updated: "2026-06-21" },
    { id: "LGR-004", name: "Inde — Loi Acquisition Terres 2013 Contournée, Adivasis Expulsés Mines & Industries Sans Consentement", country: "Inde", composite_score: 85.7, forced_displacement_land_seizure_severity_score: 88.0, legal_title_recognition_absence_scale_score: 85.0, corporate_state_complicity_land_grab_score: 85.0, indigenous_community_consultation_gap_score: 84.0, risk_level: "critique", primary_pattern: "legal_title_recognition_absence_scale", estimated_land_grabbing_rights_index: 8.57, last_updated: "2026-06-21" },
    { id: "LGR-005", name: "Philippines — CARP Réforme Agraire Non Appliquée, Paysans Expulsés Plantations & Défenseurs Terres Assassinés", country: "Philippines", composite_score: 53.25, forced_displacement_land_seizure_severity_score: 56.0, legal_title_recognition_absence_scale_score: 52.0, corporate_state_complicity_land_grab_score: 53.0, indigenous_community_consultation_gap_score: 51.0, risk_level: "élevé", primary_pattern: "forced_displacement_land_seizure_severity", estimated_land_grabbing_rights_index: 5.33, last_updated: "2026-06-21" },
    { id: "LGR-006", name: "Afrique de l'Est — Acquisitions Foncières Éthiopie/Kenya/Tanzanie, Pastoralistes Expulsés & Titres Coutumiers Ignorés", country: "Afrique de l'Est", composite_score: 51.55, forced_displacement_land_seizure_severity_score: 54.0, legal_title_recognition_absence_scale_score: 52.0, corporate_state_complicity_land_grab_score: 51.0, indigenous_community_consultation_gap_score: 48.0, risk_level: "élevé", primary_pattern: "legal_title_recognition_absence_scale", estimated_land_grabbing_rights_index: 5.16, last_updated: "2026-06-21" },
    { id: "LGR-007", name: "Global Land Alliance/GRAIN — Base Données Accaparements, Plaidoyer Droits Paysans & Standards VGGT FAO", country: "Global", composite_score: 25.9, forced_displacement_land_seizure_severity_score: 24.0, legal_title_recognition_absence_scale_score: 28.0, corporate_state_complicity_land_grab_score: 26.0, indigenous_community_consultation_gap_score: 26.0, risk_level: "modéré", primary_pattern: "indigenous_community_consultation_gap", estimated_land_grabbing_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "LGR-008", name: "ONU/FAO — Directives Volontaires Gouvernance Foncière (VGGT), UNDRIP Terres & SDG 1.4 Droits Fonciers", country: "Global", composite_score: 4.45, forced_displacement_land_seizure_severity_score: 4.0, legal_title_recognition_absence_scale_score: 5.0, corporate_state_complicity_land_grab_score: 4.0, indigenous_community_consultation_gap_score: 5.0, risk_level: "faible", primary_pattern: "forced_displacement_land_seizure_severity", estimated_land_grabbing_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/land-grabbing-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
