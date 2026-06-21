import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[organ-trafficking-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Organ Trafficking Engine Agent",
  domain: "organ_trafficking",
  total_entities: 8,
  avg_composite: 58.79,
  confidence_score: 0.82,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_organ_extraction_scale: 2, donor_coercion_vulnerability: 2, prosecution_accountability_gap: 2, transplant_tourism_infrastructure: 2 },
  top_risk_entities: [
    "Chine — Prélèvements Forcés Prisonniers Conscience, Falun Gong/Ouïghours & Industrie Transplants",
    "Pakistan — Marché Reins Ruraux Pauvres, Chirurgiens Complices & Trafic Migratoire Lié",
    "Égypte/Afrique du Nord — Réfugiés Soudanais/Érythréens Vendant Organes & Cliniques Clandestines",
  ],
  critical_alerts: [
    "Chine: forced_organ_extraction_scale",
    "Pakistan: donor_coercion_vulnerability",
    "Égypte/Afrique du Nord: donor_coercion_vulnerability",
    "Kosovo/Balkans: prosecution_accountability_gap",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_organ_trafficking_index: 5.88,
  data_sources: [
    "david_matas_david_kilgour_bloody_harvest_organ_harvesting_china_report",
    "declaration_istanbul_custodian_group_organ_trafficking_transplant_tourism",
    "unodc_global_report_trafficking_persons_organ_removal_chapter",
  ],
  entities: [
    { id: "OT-001", name: "Chine — Prélèvements Forcés Prisonniers Conscience, Falun Gong/Ouïghours & Industrie Transplants", country: "Asie du Nord-Est", composite_score: 92.4, forced_organ_extraction_scale_score: 95.0, transplant_tourism_infrastructure_score: 92.0, donor_coercion_vulnerability_score: 90.0, prosecution_accountability_gap_score: 92.0, risk_level: "critique", primary_pattern: "forced_organ_extraction_scale", estimated_organ_trafficking_index: 9.24, last_updated: "2026-06-20" },
    { id: "OT-002", name: "Pakistan — Marché Reins Ruraux Pauvres, Chirurgiens Complices & Trafic Migratoire Lié", country: "Asie du Sud", composite_score: 83.85, forced_organ_extraction_scale_score: 82.0, transplant_tourism_infrastructure_score: 85.0, donor_coercion_vulnerability_score: 88.0, prosecution_accountability_gap_score: 80.0, risk_level: "critique", primary_pattern: "donor_coercion_vulnerability", estimated_organ_trafficking_index: 8.39, last_updated: "2026-06-20" },
    { id: "OT-003", name: "Égypte/Afrique du Nord — Réfugiés Soudanais/Érythréens Vendant Organes & Cliniques Clandestines", country: "Afrique du Nord", composite_score: 81.15, forced_organ_extraction_scale_score: 80.0, transplant_tourism_infrastructure_score: 78.0, donor_coercion_vulnerability_score: 85.0, prosecution_accountability_gap_score: 82.0, risk_level: "critique", primary_pattern: "donor_coercion_vulnerability", estimated_organ_trafficking_index: 8.12, last_updated: "2026-06-20" },
    { id: "OT-004", name: "Kosovo/Balkans — Affaire Medicus, Prisonniers Serbes Organes Volés & Impunité Partielle", country: "Europe du Sud-Est", composite_score: 79.15, forced_organ_extraction_scale_score: 78.0, transplant_tourism_infrastructure_score: 75.0, donor_coercion_vulnerability_score: 80.0, prosecution_accountability_gap_score: 85.0, risk_level: "critique", primary_pattern: "prosecution_accountability_gap", estimated_organ_trafficking_index: 7.92, last_updated: "2026-06-20" },
    { id: "OT-005", name: "Inde — Tourisme Transplants Rein, Loi THOA Mal Appliquée & Trafic États Ruraux", country: "Asie du Sud", composite_score: 53.85, forced_organ_extraction_scale_score: 52.0, transplant_tourism_infrastructure_score: 55.0, donor_coercion_vulnerability_score: 58.0, prosecution_accountability_gap_score: 50.0, risk_level: "élevé", primary_pattern: "transplant_tourism_infrastructure", estimated_organ_trafficking_index: 5.39, last_updated: "2026-06-20" },
    { id: "OT-006", name: "Israël/Patients Riches — Tourisme Transplants Vers Pakistan/Roumanie & Cadre Légal Insuffisant", country: "Moyen-Orient/Europe", composite_score: 49.65, forced_organ_extraction_scale_score: 48.0, transplant_tourism_infrastructure_score: 52.0, donor_coercion_vulnerability_score: 45.0, prosecution_accountability_gap_score: 55.0, risk_level: "élevé", primary_pattern: "prosecution_accountability_gap", estimated_organ_trafficking_index: 4.97, last_updated: "2026-06-20" },
    { id: "OT-007", name: "Déclaration Istanbul — Coalition Anti-Tourisme Transplant, Réformes & Suivi International", country: "Global", composite_score: 25.85, forced_organ_extraction_scale_score: 22.0, transplant_tourism_infrastructure_score: 25.0, donor_coercion_vulnerability_score: 28.0, prosecution_accountability_gap_score: 30.0, risk_level: "modéré", primary_pattern: "forced_organ_extraction_scale", estimated_organ_trafficking_index: 2.59, last_updated: "2026-06-20" },
    { id: "OT-008", name: "ONU/ONUDC — Protocole Palermo Organes, Rapport Trafic Êtres Humains & Standards Médicaux", country: "Global", composite_score: 4.4, forced_organ_extraction_scale_score: 4.0, transplant_tourism_infrastructure_score: 5.0, donor_coercion_vulnerability_score: 3.0, prosecution_accountability_gap_score: 6.0, risk_level: "faible", primary_pattern: "transplant_tourism_infrastructure", estimated_organ_trafficking_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/organ-trafficking-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
