import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[bioethics-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Bioethics Engine Agent",
  domain: "bioethics",
  total_entities: 8,
  avg_composite: 57.07,
  confidence_score: 0.82,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { organ_harvesting_coercion: 1, forced_experimentation: 3, coercive_psychiatry: 2, medical_complicity_torture: 2 },
  top_risk_entities: [
    "Chine/Falun Gong/Ouïghours — Prélèvements Forcés d'Organes & Industrie Transplantation",
    "Corée du Nord — Expérimentation Chimique/Biologique sur Prisonniers & Camp 22",
    "Russie — Psychiatrie Punitive, Punitif Psychiatry & Dissidents Hospitalisés",
  ],
  critical_alerts: [
    "Chine/Falun Gong/Ouïghours: organ_harvesting_coercion",
    "Corée du Nord: forced_experimentation",
    "Russie: coercive_psychiatry",
    "USA/Guantánamo: medical_complicity_torture",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_bioethics_index: 5.71,
  data_sources: [
    "china_tribunal_2019_independent_tribunal_organ_harvesting_report",
    "un_coi_north_korea_commission_inquiry_2014_report",
    "who_guiding_principles_human_cell_tissue_organ_transplantation",
  ],
  entities: [
    { entity_id: "BIO-001", name: "Chine/Falun Gong/Ouïghours — Prélèvements Forcés d'Organes & Industrie Transplantation", country: "Asie du Nord-Est", composite_score: 88.35, forced_experimentation_score: 92.0, organ_harvesting_coercion_score: 95.0, coercive_psychiatry_score: 80.0, medical_complicity_torture_score: 85.0, risk_level: "critique", primary_pattern: "organ_harvesting_coercion", estimated_bioethics_index: 8.84, last_updated: "2026-06-20" },
    { entity_id: "BIO-002", name: "Corée du Nord — Expérimentation Chimique/Biologique sur Prisonniers & Camp 22", country: "Asie du Nord-Est", composite_score: 84.90, forced_experimentation_score: 88.0, organ_harvesting_coercion_score: 82.0, coercive_psychiatry_score: 80.0, medical_complicity_torture_score: 90.0, risk_level: "critique", primary_pattern: "forced_experimentation", estimated_bioethics_index: 8.49, last_updated: "2026-06-20" },
    { entity_id: "BIO-003", name: "Russie — Psychiatrie Punitive, Punitif Psychiatry & Dissidents Hospitalisés", country: "Europe de l'Est", composite_score: 78.00, forced_experimentation_score: 72.0, organ_harvesting_coercion_score: 70.0, coercive_psychiatry_score: 90.0, medical_complicity_torture_score: 82.0, risk_level: "critique", primary_pattern: "coercive_psychiatry", estimated_bioethics_index: 7.80, last_updated: "2026-06-20" },
    { entity_id: "BIO-004", name: "USA/Guantánamo — Médecins Tortionnaires, Force-Feeding & Complicité CIA", country: "Amérique du Nord", composite_score: 71.00, forced_experimentation_score: 68.0, organ_harvesting_coercion_score: 60.0, coercive_psychiatry_score: 72.0, medical_complicity_torture_score: 88.0, risk_level: "critique", primary_pattern: "medical_complicity_torture", estimated_bioethics_index: 7.10, last_updated: "2026-06-20" },
    { entity_id: "BIO-005", name: "Afrique/Essais Cliniques — Médicaments Expérimentaux & Consentement Fictif", country: "Afrique Sub-Saharienne", composite_score: 50.60, forced_experimentation_score: 52.0, organ_harvesting_coercion_score: 45.0, coercive_psychiatry_score: 55.0, medical_complicity_torture_score: 50.0, risk_level: "élevé", primary_pattern: "forced_experimentation", estimated_bioethics_index: 5.06, last_updated: "2026-06-20" },
    { entity_id: "BIO-006", name: "Inde/Bangladesh — Sujets Vulnérables, Stérilisations Forcées & Essais Non Consentis", country: "Asie du Sud", composite_score: 50.90, forced_experimentation_score: 48.0, organ_harvesting_coercion_score: 50.0, coercive_psychiatry_score: 52.0, medical_complicity_torture_score: 55.0, risk_level: "élevé", primary_pattern: "forced_experimentation", estimated_bioethics_index: 5.09, last_updated: "2026-06-20" },
    { entity_id: "BIO-007", name: "UE/Déclaration Helsinki — Lacunes Standards & Comité International Bioéthique", country: "Europe", composite_score: 28.40, forced_experimentation_score: 25.0, organ_harvesting_coercion_score: 30.0, coercive_psychiatry_score: 28.0, medical_complicity_torture_score: 32.0, risk_level: "modéré", primary_pattern: "medical_complicity_torture", estimated_bioethics_index: 2.84, last_updated: "2026-06-20" },
    { entity_id: "BIO-008", name: "ONU/UNESCO/Bioéthique — Déclaration Universelle Bioéthique, Code Nuremberg & OMS", country: "Global", composite_score: 4.40, forced_experimentation_score: 4.0, organ_harvesting_coercion_score: 5.0, coercive_psychiatry_score: 3.0, medical_complicity_torture_score: 6.0, risk_level: "faible", primary_pattern: "coercive_psychiatry", estimated_bioethics_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/bioethics-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
