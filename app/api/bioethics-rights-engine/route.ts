import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[bioethics-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Bioethics Rights Engine Agent",
  domain: "bioethics_rights",
  total_entities: 8,
  avg_composite: 61.45,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { organ_harvesting_trafficking_scale: 2, non_consensual_experimentation_severity: 3, medical_ai_algorithmic_discrimination_gap: 2, genetic_data_surveillance_coercion: 1 },
  top_risk_entities: [
    "Chine — Prélèvement Organes Prisonniers Consciencieux Documenté Tribunal 2019, Falun Gong/Ouïghours & Marché Transplantations Forcées",
    "Pays en Développement — Essais Cliniques Multinationales Sans Consentement Éclairé, Standards Réduits & Exploitation Vulnérabilité",
    "Inde — Stérilisations Forcées Camps, Essais Médicaux Tribus, Brevets Ogm Biopiraterie & Données Aadhaar Vendues",
  ],
  critical_alerts: [
    "Chine: organ_harvesting_trafficking_scale",
    "Pays en Développement: non_consensual_experimentation_severity",
    "Inde: non_consensual_experimentation_severity",
    "USA Legacy/Tuskegee: non_consensual_experimentation_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_bioethics_rights_index: 6.15,
  data_sources: [
    "china_tribunal_organ_harvesting_final_judgment_2019",
    "declaration_of_helsinki_world_medical_association",
    "nuffield_council_bioethics_reports",
  ],
  entities: [
    { id: "BER-001", name: "Chine — Prélèvement Organes Prisonniers Consciencieux Documenté Tribunal 2019, Falun Gong/Ouïghours & Marché Transplantations Forcées", country: "Chine", composite_score: 94.0, non_consensual_experimentation_severity_score: 95.0, organ_harvesting_trafficking_scale_score: 97.0, genetic_data_surveillance_coercion_score: 93.0, medical_ai_algorithmic_discrimination_gap_score: 90.0, risk_level: "critique", primary_pattern: "organ_harvesting_trafficking_scale", estimated_bioethics_rights_index: 9.4, last_updated: "2026-06-21" },
    { id: "BER-002", name: "Pays en Développement — Essais Cliniques Multinationales Sans Consentement Éclairé, Standards Réduits & Exploitation Vulnérabilité", country: "Global Sud", composite_score: 90.3, non_consensual_experimentation_severity_score: 93.0, organ_harvesting_trafficking_scale_score: 87.0, genetic_data_surveillance_coercion_score: 89.0, medical_ai_algorithmic_discrimination_gap_score: 92.0, risk_level: "critique", primary_pattern: "non_consensual_experimentation_severity", estimated_bioethics_rights_index: 9.03, last_updated: "2026-06-21" },
    { id: "BER-003", name: "Inde — Stérilisations Forcées Camps, Essais Médicaux Tribus, Brevets Ogm Biopiraterie & Données Aadhaar Vendues", country: "Inde", composite_score: 87.2, non_consensual_experimentation_severity_score: 90.0, organ_harvesting_trafficking_scale_score: 84.0, genetic_data_surveillance_coercion_score: 88.0, medical_ai_algorithmic_discrimination_gap_score: 86.0, risk_level: "critique", primary_pattern: "non_consensual_experimentation_severity", estimated_bioethics_rights_index: 8.72, last_updated: "2026-06-21" },
    { id: "BER-004", name: "USA Legacy/Tuskegee — Expérimentations Prisonniers Guatemala 1945-56, Tests Armes Chimiques Soldats & Héritage Eugenics", country: "USA", composite_score: 84.7, non_consensual_experimentation_severity_score: 87.0, organ_harvesting_trafficking_scale_score: 81.0, genetic_data_surveillance_coercion_score: 83.0, medical_ai_algorithmic_discrimination_gap_score: 88.0, risk_level: "critique", primary_pattern: "non_consensual_experimentation_severity", estimated_bioethics_rights_index: 8.47, last_updated: "2026-06-21" },
    { id: "BER-005", name: "Europe — Biais Algorithmes Diagnostic IA Peau Sombre, RGPD Gaps Données Médicales & Essais Pédiatriques Consentement", country: "Europe", composite_score: 54.0, non_consensual_experimentation_severity_score: 52.0, organ_harvesting_trafficking_scale_score: 48.0, genetic_data_surveillance_coercion_score: 56.0, medical_ai_algorithmic_discrimination_gap_score: 62.0, risk_level: "élevé", primary_pattern: "medical_ai_algorithmic_discrimination_gap", estimated_bioethics_rights_index: 5.4, last_updated: "2026-06-21" },
    { id: "BER-006", name: "Moyen-Orient — Tourisme Transplantation Reins, Donneurs Pauvres Pakistan/Égypte & Absence Régulation", country: "Moyen-Orient", composite_score: 51.0, non_consensual_experimentation_severity_score: 50.0, organ_harvesting_trafficking_scale_score: 57.0, genetic_data_surveillance_coercion_score: 47.0, medical_ai_algorithmic_discrimination_gap_score: 50.0, risk_level: "élevé", primary_pattern: "organ_harvesting_trafficking_scale", estimated_bioethics_rights_index: 5.1, last_updated: "2026-06-21" },
    { id: "BER-007", name: "Comité International Bioéthique/Nuffield — Standards Consentement, Déclaration Helsinki & IA Médicale Éthique", country: "Global", composite_score: 26.15, non_consensual_experimentation_severity_score: 26.0, organ_harvesting_trafficking_scale_score: 24.0, genetic_data_surveillance_coercion_score: 27.0, medical_ai_algorithmic_discrimination_gap_score: 28.0, risk_level: "modéré", primary_pattern: "medical_ai_algorithmic_discrimination_gap", estimated_bioethics_rights_index: 2.62, last_updated: "2026-06-21" },
    { id: "BER-008", name: "ONU/UNESCO — Déclaration Universelle Bioéthique 2005, Comité Bioéthique & SDG 3 Santé Bien-Être", country: "Global", composite_score: 4.25, non_consensual_experimentation_severity_score: 4.0, organ_harvesting_trafficking_scale_score: 4.0, genetic_data_surveillance_coercion_score: 5.0, medical_ai_algorithmic_discrimination_gap_score: 4.0, risk_level: "faible", primary_pattern: "genetic_data_surveillance_coercion", estimated_bioethics_rights_index: 0.43, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/bioethics-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
