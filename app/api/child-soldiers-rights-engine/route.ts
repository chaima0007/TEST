import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[child-soldiers-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Child Soldiers Rights Engine Agent",
  domain: "child_soldiers_rights",
  total_entities: 8,
  avg_composite: 61.59,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_recruitment_underage_severity: 3, sexual_violence_child_combatant: 1, demobilization_reintegration_failure_scale: 2, accountability_commander_liability_gap: 2 },
  top_risk_entities: [
    "DRC — 15 000+ Enfants Soldats Actifs, M23/ADF & Muliples Groupes Armés, Recrutement Continu",
    "South Sudan — 19 000 Enfants Libérés 2018-23, Rechutes Recrutement & Viols Systématiques",
    "Myanmar — Tatmadaw Recrutement Enfants Documenté ONU, Post-Coup 2021 & Groupes Ethniques",
  ],
  critical_alerts: [
    "DRC: forced_recruitment_underage_severity",
    "South Sudan: sexual_violence_child_combatant",
    "Myanmar: forced_recruitment_underage_severity",
    "Sahel/Mali-Burkina: demobilization_reintegration_failure_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_child_soldiers_rights_index: 6.16,
  data_sources: [
    "unicef_children_and_armed_conflict_annual_report",
    "child_soldiers_international_global_report",
    "un_security_council_mrm_monitoring_reporting_mechanism",
  ],
  entities: [
    { entity_id: "CSR-001", name: "DRC — 15 000+ Enfants Soldats Actifs, M23/ADF & Muliples Groupes Armés, Recrutement Continu", country: "RDC", composite_score: 93.95, forced_recruitment_underage_severity_score: 96.0, demobilization_reintegration_failure_scale_score: 93.0, sexual_violence_child_combatant_score: 94.0, accountability_commander_liability_gap_score: 92.0, risk_level: "critique", primary_pattern: "forced_recruitment_underage_severity", estimated_child_soldiers_rights_index: 9.40, last_updated: "2026-06-21" },
    { entity_id: "CSR-002", name: "South Sudan — 19 000 Enfants Libérés 2018-23, Rechutes Recrutement & Viols Systématiques", country: "Soudan du Sud", composite_score: 90.95, forced_recruitment_underage_severity_score: 93.0, demobilization_reintegration_failure_scale_score: 90.0, sexual_violence_child_combatant_score: 91.0, accountability_commander_liability_gap_score: 89.0, risk_level: "critique", primary_pattern: "sexual_violence_child_combatant", estimated_child_soldiers_rights_index: 9.10, last_updated: "2026-06-21" },
    { entity_id: "CSR-003", name: "Myanmar — Tatmadaw Recrutement Enfants Documenté ONU, Post-Coup 2021 & Groupes Ethniques", country: "Myanmar", composite_score: 87.95, forced_recruitment_underage_severity_score: 90.0, demobilization_reintegration_failure_scale_score: 87.0, sexual_violence_child_combatant_score: 88.0, accountability_commander_liability_gap_score: 86.0, risk_level: "critique", primary_pattern: "forced_recruitment_underage_severity", estimated_child_soldiers_rights_index: 8.80, last_updated: "2026-06-21" },
    { entity_id: "CSR-004", name: "Sahel/Mali-Burkina — JNIM/GSIM Recrutement Enfants, Kamikazes Mineurs & Zéro DDR Fonctionnel", country: "Sahel", composite_score: 84.95, forced_recruitment_underage_severity_score: 87.0, demobilization_reintegration_failure_scale_score: 84.0, sexual_violence_child_combatant_score: 85.0, accountability_commander_liability_gap_score: 83.0, risk_level: "critique", primary_pattern: "demobilization_reintegration_failure_scale", estimated_child_soldiers_rights_index: 8.50, last_updated: "2026-06-21" },
    { entity_id: "CSR-005", name: "Yémen — Coalition+Houthis Recrutement Documenté, 3 700+ Enfants Vérifiés UNICEF 2023", country: "Yémen", composite_score: 53.95, forced_recruitment_underage_severity_score: 56.0, demobilization_reintegration_failure_scale_score: 53.0, sexual_violence_child_combatant_score: 54.0, accountability_commander_liability_gap_score: 52.0, risk_level: "élevé", primary_pattern: "forced_recruitment_underage_severity", estimated_child_soldiers_rights_index: 5.40, last_updated: "2026-06-21" },
    { entity_id: "CSR-006", name: "Somalie/Al-Shabaab — Recrutement Forcé Madrasas, Attentats Mineurs & AMISOM Incapacité", country: "Somalie", composite_score: 50.95, forced_recruitment_underage_severity_score: 53.0, demobilization_reintegration_failure_scale_score: 50.0, sexual_violence_child_combatant_score: 51.0, accountability_commander_liability_gap_score: 49.0, risk_level: "élevé", primary_pattern: "accountability_commander_liability_gap", estimated_child_soldiers_rights_index: 5.10, last_updated: "2026-06-21" },
    { entity_id: "CSR-007", name: "UNICEF/Child Soldiers International — DDR Enfants, Plaidoyer Protocole Facultatif & Réhabilitation", country: "Global", composite_score: 26.05, forced_recruitment_underage_severity_score: 27.0, demobilization_reintegration_failure_scale_score: 26.0, sexual_violence_child_combatant_score: 25.0, accountability_commander_liability_gap_score: 26.0, risk_level: "modéré", primary_pattern: "demobilization_reintegration_failure_scale", estimated_child_soldiers_rights_index: 2.61, last_updated: "2026-06-21" },
    { entity_id: "CSR-008", name: "ONU/Protocole Facultatif — OPAC 2002, Mécanisme MRM Surveillance & SDG 16.2 Violence Enfants", country: "Global", composite_score: 4.0, forced_recruitment_underage_severity_score: 4.0, demobilization_reintegration_failure_scale_score: 4.0, sexual_violence_child_combatant_score: 4.0, accountability_commander_liability_gap_score: 4.0, risk_level: "faible", primary_pattern: "accountability_commander_liability_gap", estimated_child_soldiers_rights_index: 0.40, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-soldiers-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
